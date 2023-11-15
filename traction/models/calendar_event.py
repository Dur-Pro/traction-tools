from odoo import api, fields, models, Command
from datetime import timedelta


class Meeting(models.Model):
    _inherit = ["calendar.event"]

    duration = fields.Float(string='Duration (hours)')

    state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('done', 'Done')
        ]
    )

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

    unsolved_issues = fields.One2many(
        comodel_name='mail.activity',
        related='team_id.issue_ids',
        readonly=True
    )

    issues_discussed = fields.Many2many(
        comodel_name='traction.identify_discuss_solve',
        relation='calendar_event_identify_discuss_solve_rel',
        column1='meeting_id',
        column2='identify_discuss_solve_id'
    )

    headline_ids = fields.One2many(
        comodel_name='mail.activity',
        related='team_id.headline_ids',
        readonly=True
    )

    @api.model
    def create(self, vals):
        if vals.get('team_id'):
            team_id = self.env['traction.team'].browse(vals.get('team_id'))
            vals['name'] = "Level 10 - " + team_id.name
            if 'privacy' not in vals:
                vals['privacy'] = 'confidential'
            vals['partner_ids'] = [Command.link(member.partner_id.id) for member in team_id.member_ids]
        return super(Meeting, self).create(vals)

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
            event.is_responsible_user = (
                    self.env.user == event.user_id or
                    self.env.user == event.note_taker_user_id or
                    self.env.user._is_admin()
            )

    def action_send_mm(self):
        template = self.env.ref('traction.meeting_minutes_document')
        for event in self:
            recipient_ids = [(4, pid) for pid in event.partner_ids.ids]
            print(recipient_ids)
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
