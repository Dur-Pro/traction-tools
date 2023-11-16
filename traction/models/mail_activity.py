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

    meet_id = fields.Many2one(
        comodel_name='calendar.event',
        string='Meeting',
        copy=False
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
