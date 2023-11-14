from odoo import api, models, fields, tools, _
from odoo.tools import is_html_empty
from odoo.exceptions import ValidationError


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

    @api.constrains('activity_type_id')
    def _check_team_id(self):
        for record in self:
            if (record.activity_type_id == self.env.ref('traction.mail_activity_data_issue')) and (
                    record.team_id == False):
                raise ValidationError("Issues need to be assign to Traction Team")
        # all records passed the test, don't return anything

    def action_start_ids(self):
        self.ensure_one()
        if not self.issue_discuss_solve_ids:
            self.issue_discuss_solve_ids = self.env['traction.identify_discuss_solve'].create({
                'issue_id': self.id,
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
        # Fix the CybroAddons version by making sure we call the original method
        messages, next_activities = super()._action_done()
        self.write({'state': 'done'})
        if self.recurring:
            next_activities += self.env['mail.activity'].create({
                'res_id': self.res_id,
                'res_model_id': self.res_model_id.id,
                'summary': self.summary,
                'priority': self.priority,
                'date_deadline': self.new_date,
                'recurring': self.recurring,
                'interval': self.interval,
                'activity_type_id': self.activity_type_id.id,
                'new_date': self.get_date(),
                'user_id': self.user_id.id
            })
        return messages.ids and messages.ids[0] or False
