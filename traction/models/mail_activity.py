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

    # TODO: Figure out how to properly link the activities to the meetings to keep a trace of what was discussed
    # def _action_done(self, feedback=False, attachment_ids=None):
    #     issue_type = self.env.ref('traction.mail_activity_data_issue')
    #     headline_type = self.env.ref('traction.mail_activity_data_headline')
    #     if self.meet_id:
    #         if self.activity_type_id == headline_type:
    #             self.meet_id.message_post(
    #                 subject=f"Headline: {self.summary}",
    #                 body=f"""Headline discussed at {datetime.now():%Y-%m-%d %H:%M}\n{self.note}""",
    #                 message_type="comment",
    #             )
    #         elif self.activity_type_id == issue_type:
    #             self.meet_id.message_post(
    #                 subject=f"Issue: {self.summary}",
    #                 body=f"Issue closed at {datetime.now():%Y-%m-%d %H:%M}. See issues tab for more details.\n"
    #                      f"{self.note}",
    #                 message_type="comment",
    #             )
    #     return super()._action_done()