from odoo import api, fields, models, _, SUPERUSER_ID
import datetime
from datetime import datetime, date
from pytz import timezone

SKIP_MODEL = ['_unknown', 'base', 'base_import.mapping', 'base_import.tests.models.char',
              'base_import.tests.models.char.noreadonly', 'base_import.tests.models.char.readonly',
              'base_import.tests.models.char.required', 'base_import.tests.models.char.states',
              'base_import.tests.models.char.stillreadonly', 'base_import.tests.models.complex',
              'base_import.tests.models.float', 'base_import.tests.models.m2o',
              'base_import.tests.models.m2o.related',
              'base_import.tests.models.m2o.required', 'base_import.tests.models.m2o.required.related',
              'base_import.tests.models.o2m', 'base_import.tests.models.o2m.child',
              'base_import.tests.models.preview',
              'format.address.mixin', 'ir.actions.act_url', 'ir.actions.act_window', 'ir.actions.act_window.view',
              'ir.actions.act_window_close', 'ir.actions.actions', 'ir.actions.client', 'ir.actions.report',
              'ir.actions.server', 'ir.actions.todo', 'ir.attachment', 'ir.autovacuum', 'ir.config_parameter',
              'ir.cron', 'ir.default', 'ir.exports', 'ir.exports.line', 'ir.fields.converter', 'ir.filters',
              'ir.http', 'ir.logging', 'ir.mail_server', 'ir.model', 'ir.model.access', 'ir.model.constraint',
              'ir.model.data', 'ir.model.fields', 'ir.model.relation', 'ir.module.category', 'ir.module.module',
              'ir.module.module.dependency', 'ir.module.module.exclusion', 'ir.property', 'ir.qweb',
              'ir.qweb.field',
              'ir.qweb.field.barcode', 'ir.qweb.field.contact', 'ir.qweb.field.date', 'ir.qweb.field.datetime',
              'ir.qweb.field.duration', 'ir.qweb.field.float', 'ir.qweb.field.float_time', 'ir.qweb.field.html',
              'ir.qweb.field.image', 'ir.qweb.field.integer', 'ir.qweb.field.many2many', 'ir.qweb.field.many2one',
              'ir.qweb.field.monetary', 'ir.qweb.field.qweb', 'ir.qweb.field.relative', 'ir.qweb.field.selection',
              'ir.qweb.field.text', 'ir.rule', 'ir.sequence.date_range', 'ir.server.object.lines', 'ir.translation',
              'ir.ui.menu', 'ir.ui.view', 'ir.ui.view.custom', 'report.base.report_irmodulereference',
              'report.layout',
              'web_editor.converter.test', 'web_editor.converter.test.sub', 'web_tour.tour', 'mail.tracking.value',
              'mail.mail',
              'mail.message', 'res.users.log', 'iap.account', 'wizard.merge.data']


class TractionIssue(models.Model):
    _name = "traction.issue"
    _description = "Issue"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _today(self):
        """Get the current date in the user's time zone."""
        return datetime.now(timezone(self.env.user.tz or 'GMT')).date()

    @api.model
    def fetch_model_list(self):
        model_list = []
        for model in self.env['ir.model'].sudo().search([('transient', '=', False)], order='name'):
            if model.model in SKIP_MODEL:
                continue
            model_list += [(model.model, model.name + " (%s)" % (model.model))]
        return model_list

    @api.model
    def _current_user(self):
        return self.env.user

    active = fields.Boolean(
        default=True,
    )
    name = fields.Char(
        readonly=False,
    )
    sequence = fields.Integer(
        default=1
    )
    tag_ids = fields.Many2many(
        comodel_name="traction.issue.tag",
        relation="traction_issue_tag_rel",
        column1="issue_id",
        column2="tag_id",
        string="Tags",
        help="Tags to help categorize the issue.",
    )
    stage_id = fields.Many2one(
        comodel_name="traction.issue.stage",
        string="Stage",
        tracking=True,
        index=True,
        group_expand="_read_group_stage_ids",
        domain="[('issues_list_id', '=', issues_list_id)]",
        copy=False,
    )

    # stage_id_selection = fields.Selection(
    #     compute="_compute_stage_id_selection",
    #     selection="_get_stages",
    #     inverse="_inverse_stage_id_selection",
    # )
    issues_list_id = fields.Many2one(
        comodel_name="traction.issues.list",
    )
    related_record = fields.Reference(
        selection='fetch_model_list',
        string='Related Record',
        compute_sudo=True,
    )
    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('solved', 'Solved')
        ],
        compute="_compute_state",
    )
    date_raised = fields.Datetime(
        string='Raised on:',
        readonly=True,
        default=_today,
    )
    days_open = fields.Integer(
        string="Days open",
        compute="_compute_days_open",
    )
    date_solved = fields.Datetime(
        string="Solved on:",
        compute="_compute_date_solved",
        store=True,
    )
    raised_by = fields.Many2one(
        comodel_name='res.users',
        string='Raised by:',
        readonly=True,
        default=_current_user,
    )
    identify = fields.Html(
        help="Notes on issue identification.",
        tracking=True,
    )
    discuss = fields.Html(
        help="Notes on issue discussion.",
        tracking=True,

    )
    solve = fields.Html(
        help="Notes on possible and selected solutions.",
        tracking=True,
    )
    allowed_user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Allowed Users",
        compute="_compute_allowed_user_ids",
        store=True,
        compute_sudo=True,
    )

    @api.depends_context("res_model", "res_id")
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "related_record" in fields_list:
            res_model = self.env.context.get("res_model", False)
            res_id = self.env.context.get("res_id", False)
            if res_model and res_id:
                rec = self.env[res_model].browse(res_id)
                res['related_record'] = rec
            else:
                res['related_record'] = False
        return res

    @api.depends("state")
    def _compute_date_solved(self):
        for rec in self:
            if rec.state == "open":
                rec.date_solved = False
            elif rec.state == "solved" and rec.date_solved:
                rec.date_solved = rec.date_solved
            else:  # rec.state == "solved" and not rec.date_solved
                # We just moved from open to solved, set the date
                rec.date_solved = datetime.now()

    @api.model
    def save_and_close(self):
        return {
            "type": "ir.actions.act_window_close",
        }

    @api.depends("date_raised", "date_solved")
    def _compute_days_open(self):
        for rec in self:
            if rec.date_solved:
                rec.days_open = (rec.date_solved - rec.date_raised).days
            else:
                rec.days_open = (datetime.now() - rec.date_raised).days

    @api.depends("issues_list_id", "issues_list_id.team_ids", "issues_list_id.team_ids.member_ids")
    def _compute_allowed_user_ids(self):
        for rec in self:
            rec.allowed_user_ids = rec.issues_list_id.mapped('team_ids').mapped('member_ids')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_issues_list_id' in self.env.context:
            search_domain = ['|', ('issues_list_id', '=', self.env.context['default_issues_list_id'])] + search_domain
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.depends('stage_id', 'stage_id.is_closing_stage')
    def _compute_state(self):
        for rec in self:
            rec.state = 'solved' if rec.stage_id.is_closing_stage else 'open'

    # @api.depends_context('active_id')
    # def _get_stages(self):
    #     stages = self.env['traction.issue.stage'].search([('issues_list_id', 'in', self.mapped('issues_list_id').ids)])
    #     return [(stage.id, stage.name) for stage in stages]
    #
    # @api.depends('stage_id')
    # def _compute_stage_id_selection(self):
    #     for rec in self:
    #         rec.stage_id_selection = str(rec.stage_id.id)
    #
    # def _inverse_stage_id_selection(self):
    #     for rec in self:
    #         rec.stage_id = self.env['traction.issue.stage'].browse(int(rec.stage_id_selection))