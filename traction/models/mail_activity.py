from odoo import api, models, fields, tools, _
from odoo.tools import is_html_empty
from odoo.exceptions import ValidationError
from datetime import datetime


class MailActivity(models.Model):
    _inherit = "mail.activity"

    team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        copy=False
    )

    agenda_item_ids = fields.One2many(
        comodel_name='calendar.event.agenda.item',
        string='Agenda Items',
        inverse_name='activity_id',
    )
    action_item_ids = fields.One2many(
        comodel_name='calendar.event.action.item',
        string='Meeting Action Items',
        inverse_name='activity_id',
    )
    issue_discuss_solve_ids = fields.Many2one(
        comodel_name='traction.identify_discuss_solve',
        # inverse_name='issue_id',
        string='Discussion'
    )

    priority = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Important'),
            ('2', 'Very Important'),
            ('3', 'Urgent'),
        ],
        default='0',
        index=True,
        store=True)

    state = fields.Selection(
        selection_add=[
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        store=True)

    needs_team_id = fields.Boolean(compute='_compute_needs_team_id')

    can_be_added_to_agenda = fields.Boolean(compute='_compute_can_be_added_to_agenda')
    @api.depends('activity_type_id')
    def _compute_needs_team_id(self):
        for record in self:
            record.needs_team_id = record.activity_type_id in [
                self.env.ref('traction.mail_activity_data_issue'),
                self.env.ref('traction.mail_activity_data_headline')]

    @api.constrains('activity_type_id', 'team_id')
    @api.depends('needs_team_id')
    def _check_team_id(self):
        if self.needs_team_id and not self.team_id:
            raise ValidationError(_('Traction Team is required for this activity type.'))

    def action_start_ids(self):
        self.ensure_one()
        if not self.issue_discuss_solve_ids:
            self.issue_discuss_solve_ids = self.env['traction.identify_discuss_solve'].create({
                'issue_id': self.id,
                'meeting_ids': [(4, self.env.context.get('active_id'))]
            })
        return {
            'name': (_('Issue IDS')),
            'view_mode': 'form',
            'res_model': 'traction.identify_discuss_solve',
            'res_id': self.issue_discuss_solve_ids.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def action_done(self):
        res = super().action_done()
        if 'reload_on_close' in self.env.context and self.env.context.get('reload_on_close'):
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        return res

    def action_done_schedule_next(self):
        res = super().action_done_schedule_next()
        if 'reload_on_close' in self.env.context:
            res['context']['reload_on_close'] = self.env.context.get('reload_on_close')
        return res

    def action_close_dialog(self):
        res =super().action_close_dialog()
        if 'reload_on_close' in self.env.context and self.env.context.get('reload_on_close'):
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        return res

    @api.depends_context('active_id')
    def action_add_to_agenda(self):
        event = self.env['calendar.event'].browse(self.env.context.get('active_id'))
        issue_type = self.env.ref('traction.mail_activity_data_issue')
        headline_type = self.env.ref('traction.mail_activity_data_headline')
        for rec in self:
            item_type = ({
                issue_type: 'issue',
                headline_type: 'headline',
            }).get(rec.activity_type_id, None)
            item = event.add_agenda_item(
                name=rec.summary,
                description=rec.note,
                item_type=item_type,
            )
            rec.write({'agenda_item_ids': [(4, item.id)]})

    @api.depends_context('active_id', 'issues_list_mode')
    @api.depends('agenda_item_ids')
    def _compute_can_be_added_to_agenda(self):
        ctx = self.env.context
        active_id = ctx.get('active_id', False)
        if not ctx.get('issues_list_mode', False) or not active_id:
            self.can_be_added_to_agenda = False
        event = self.env['calendar.event'].browse(active_id)
        if not event:
            self.can_be_added_to_agenda = False
        for rec in self:
            rec.can_be_added_to_agenda = not bool(
                rec.agenda_item_ids.filtered(lambda item: item in event.agenda_item_ids))

    def default_get(self, fields):
        res = super().default_get(fields)
        if 'activity_type_id' in fields:
            view_mode = self.env.context.get('traction_mode', False)
            if view_mode:
                res.update({
                    'activity_type_id': ({
                        'issue': self.env.ref('traction.mail_activity_data_issue'),
                        'headline': self.env.ref('traction.mail_activity_data_headline'),
                    }).get(str(view_mode), False)
                })
        return res
