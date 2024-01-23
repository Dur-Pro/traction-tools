from odoo import api, fields, models, _
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
        for model in self.env['ir.model'].search([('transient', '=', False)], order='name'):
            if model.model in SKIP_MODEL:
                continue
            model_list += [(model.model, model.name + " (%s)" % (model.model))]
        return model_list

    @api.model
    def _current_user(self):
        return self.env.user

    name = fields.Char(
        readonly=False,
    )
    tag_ids = fields.Many2many(
        comodel_name="traction.issue.tag",
        relation="traction_issue_tag_rel",
        column1="issue_id",
        column2="tag_id",
        string="Tags",
        help="Tags to help categorize the issue.",
    )
    issues_list_id = fields.Many2one(
        comodel_name="traction.issues.list",
    )
    related_record = fields.Reference(
        selection='fetch_model_list',
        string='Related Record',
    )
    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('solved', 'Solved')
        ],
        default='open'
    )
    date_raised = fields.Datetime(
        string='Raised on:',
        readonly=True,
        default=_today,
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
