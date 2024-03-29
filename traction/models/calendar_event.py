from odoo import api, fields, models, Command
from datetime import timedelta


class Meeting(models.Model):
    _name = "calendar.event"
    _inherit = ["calendar.event", "mail.activity.mixin"]

    duration = fields.Float(string='Duration (hours)')
    team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        index=True)
    allowed_user_ids = fields.Many2many(
        comodel_name="res.users",
        related="team_id.member_ids",
        string="Allowed Users",
    )
    agenda_id = fields.Many2one(
        string="Agenda",
        comodel_name="calendar.event.agenda",
    )
    agenda_item_ids = fields.One2many(
        string="Agenda Items",
        comodel_name="calendar.event.agenda.item",
        related="agenda_id.item_ids",
        readonly=False,
    )
    agenda_template_id = fields.Many2one(
        string="Agenda Template",
        comodel_name="calendar.event.agenda.template",
        related="team_id.agenda_template_id",
    )
    facilitator_id = fields.Many2one(
        string="Facilitator",
        help="The person responsible for managing the overall meeting flow.",
        comodel_name="res.users",
    )
    scribe_id = fields.Many2one(
        string='Scribe',
        help="The person assigned to take meeting minutes",
        comodel_name='res.users',
    )
    timekeeper_id = fields.Many2one(
        string="Timekeeper",
        help="The person assigned to keep the meeting running on time.",
        comodel_name='res.users',
    )
    headline_ids = fields.One2many(
        comodel_name='traction.headline',
        related='team_id.headline_ids',
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('team_id'):
                team_id = self.env['traction.team'].browse(vals.get('team_id'))
                vals['name'] = "Level 10 - " + team_id.name
                if 'privacy' not in vals:
                    vals['privacy'] = 'confidential'
                vals['partner_ids'] = [Command.link(member.partner_id.id) for member in team_id.member_ids]
        res = super().create(vals_list)
        for rec in res:
            if rec.team_id:
                rec.agenda_id = rec.agenda_template_id.generate_agenda(rec)
        return res

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

    def action_end(self):
        return {
            'name': 'Close Meeting',
            'type': 'ir.actions.act_window',
            'res_model': 'close.meeting.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_meeting_id': self.id}
        }

    def action_close_meeting(self, send_minutes=True, next_meeting_time=False):
        # TODO: Rewrite this code if it's wanted
        self.ensure_one()
        self.state = 'done'
        # Mark any discussed headlines as complete (close the mail.activity records related to them)
        for item in self.agenda_item_ids.filtered(lambda rec: rec.item_type == 'headline' and rec.discussed):
            item.activity_id.action_done()
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

    def action_open_issues_lists(self):
        self.ensure_one()
        return {
            "name": f"Issues Lists for {self.team_id.name}",
            "type": "ir.actions.act_window",
            "res_model": "traction.issues.list",
            "view_mode": "kanban",
            "domain": [["team_ids", "in", self.team_id.id]],
        }