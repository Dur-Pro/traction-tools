from odoo import api, fields, models
from datetime import timedelta


class Meeting(models.Model):
    _inherit = ["calendar.event"]

    state = fields.Selection(selection=[('pending', 'Pending'),
                                        ('in_progress', 'In Progress'),
                                        ('done', 'Done')])
    team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        index=True)

    note_taker_user_id = fields.Many2one(
        string='Note Taker',
        comodel_name='res.users',
    )

    absent_partner_ids = fields.Many2many(
        string='Absent Members',
        comodel_name='res.partner',
        relation='calendar_event_absent_res_partner_rel',
        domain="[('id', 'in', partner_ids)]",
    )

    agenda_items = fields.One2many(
        string='Agenda Items',
        comodel_name='calendar.event.agenda.item',
        inverse_name='event_id',
    )

    action_items = fields.One2many(
        string='Action / Decision Items',
        comodel_name='calendar.event.action.item',
        inverse_name='event_id',
    )

    closing_conclusion_notes = fields.Text(
        string='Closing / Conclusion Notes',
    )

    is_responsible_user = fields.Boolean(
        string='Is Responsible User',
        compute='_compute_is_responsible_user',
    )

    ids_items = fields.One2many('traction.identify_discuss_solve', 'meeting_ids',
                                string='Issues Discussed')

    unsolved_issues = fields.One2many(comodel_name='mail.activity', related='team_id.issue_ids', readonly=True)
    issues_discussed = fields.Many2many(comodel_name='traction.identify_discuss_solve',
                                        relation='calendar_event_identify_discuss_solve_rel',
                                        column1='meeting_id', column2='identify_discuss_solve_id', )
    headline_ids = fields.One2many(comodel_name='mail.activity', related='team_id.headline_ids', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('team_id'):
            team_id = self.env['traction.team'].browse(vals.get('team_id'))
            vals['name'] = "Level 10 - " + team_id.name

        result = super(Meeting, self).create(vals)
        return result

    @api.onchange('team_id')
    def _rename_meet(self):
        for meeting in self:
            if meeting.team_id:
                meeting.name = "Level 10 - " + meeting.team_id.name
            else:
                meeting.name = "Replace me please"
            meeting.update({'name': meeting.name})

    def _compute_is_responsible_user(self):
        for event in self:
            event.is_responsible_user = (self.env.user == event.user_id or
                                         self.env.user == event.note_taker_user_id or
                                         self.env.user._is_admin())

    def action_send_mm(self):
        template = self.env.ref('traction.meeting_minutes_document')
        for event in self:
            recipient_ids = [(4, pid) for pid in event.partner_ids.ids]
            # TODO: Make a mail template and use it here for sending with the report as attachment
            # template.send_mail(event.id, email_values={'recipient_ids': recipient_ids})

    def _compute_unsolved_issues(self):
        for event in self:
            event.unsolved_issues = event.traction_items.filtered(lambda x: x.state == 'open')

    def action_end(self):
        return {
            'name': 'Close Meeting',
            'type': 'ir.actions.act_window',
            'res_model': 'close.meeting.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_meeting_id': self.id}
        }

    def action_start(self):
        self.ensure_one()
        self.state = 'in_progress'
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'res_id': self.id,
        }

    def action_close_meeting(self, send_minutes=True, next_meeting_time=False):
        self.ensure_one()
        self.state = 'done'
        if send_minutes:
            self.action_send_mm()
        if next_meeting_time:
            self.env['calendar.event'].create({
                'name': self.name,
                'start': next_meeting_time,
                'stop': next_meeting_time + timedelta(hours=self.duration),
                'team_id': self.team_id.id,
            })

    def view_details(self):
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'res_id': self.id,
        }


class IdentifyDiscussSolve(models.Model):
    _name = "traction.identify_discuss_solve"
    _description = "Issue identification, discussion and solution"
    _inherit = ['mail.thread']

    issue_id = fields.Many2one(comodel_name='mail.activity',
                               domain=[('activity_type_id.name', '=', 'Issue')],
                               string="Issue", )
    meeting_ids = fields.Many2many(comodel_name='calendar.event', string="Meetings",
                                   relation='calendar_event_identify_discuss_solve_rel',
                                   column1='identify_discuss_solve_id', column2='meeting_id',
                                   help="Meetings when the issue was discussed.")

    identify = fields.Html()
    discuss = fields.Html()
    solve = fields.Html()
    state = fields.Selection(selection=[('open', 'Open'), ('solved', 'Solved')], default='open')
    name = fields.Char(related='issue_id.summary', readonly=False)
    date_raised = fields.Datetime(related='issue_id.create_date', readonly=True)
    raised_by = fields.Many2one(related='issue_id.create_uid', readonly=True)

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


class MeetingAgendaItem(models.Model):
    _name = 'calendar.event.agenda.item'
    _description = 'Meeting Agenda Item'
    _order = 'sequence asc'

    event_id = fields.Many2one(
        string='Event',
        comodel_name='calendar.event',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    name = fields.Char(
        string='Topic',
        required=True,
    )
    description = fields.Text(
        string='Description / Notes',
    )
    discussed = fields.Boolean(
        string='Discussed',
    )

    def action_discussed(self):
        return self.write({'discussed': True})

    def action_reset(self):
        return self.write({'discussed': False})


class MeetingActionItem(models.Model):
    _name = 'calendar.event.action.item'
    _description = 'Meeting Action Item'
    _order = 'sequence asc'

    event_id = fields.Many2one(
        string='Event',
        comodel_name='calendar.event',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    name = fields.Char(
        string='Action / Decision',
        required=True,
    )
    agenda_item_id = fields.Many2one(
        string='Agenda Item',
        comodel_name='calendar.event.agenda.item',
        help='Related Agenda Item',
    )
    user_id = fields.Many2one(
        string='Responsible',
        comodel_name='res.users',
    )
    user_ids = fields.Many2many(
        string='Assigned To',
        comodel_name='res.users',
        relation='calendar_event_action_item_users',
        column1='action_item_id',
        column2='user_id',
    )
    date_deadline = fields.Date(
        string='Deadline',
    )
    description = fields.Html(
        string='Description / Notes',
    )
