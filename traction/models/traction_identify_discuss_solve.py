from odoo import api, fields, models
from datetime import timedelta


class IdentifyDiscussSolve(models.Model):
    _name = "traction.identify_discuss_solve"
    _description = "Issue identification, discussion and solution"
    _inherit = ['mail.thread']

    issue_id = fields.Many2one(
        comodel_name='mail.activity',
        domain=[('activity_type_id.name', '=', 'Issue')],
        string="Issue"
    )

    meeting_ids = fields.Many2many(
        comodel_name='calendar.event',
        string="Meetings",
        relation='calendar_event_identify_discuss_solve_rel',
        column1='identify_discuss_solve_id',
        column2='meeting_id',
        help="Meetings when the issue was discussed."
    )

    identify = fields.Html()
    discuss = fields.Html()
    solve = fields.Html()
    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('solved', 'Solved')
        ],
        default='open'
    )

    name = fields.Char(related='issue_id.summary', readonly=False)

    date_raised = fields.Datetime(string='Raised on:',
                                  related='issue_id.create_date',
                                  readonly=True)

    raised_by = fields.Many2one(string='Raised by:',
                                related='issue_id.create_uid',
                                readonly=True)

    def action_solve(self):
        self.issue_id.action_done()
        self.state = 'solved'

    @api.model_create_multi
    def create(self, vals_list):
        #  Set the followers to the meeting attendees list
        res = super().create(vals_list)
        for rec in res:
            rec.message_subscribe(rec.meeting_ids.partner_ids.ids)
        return res

