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

    agenda_item_ids = fields.One2many(
        string='Agenda Items',
        comodel_name='calendar.event.agenda.item',
        inverse_name='event_id',
    )

    action_item_ids = fields.One2many(
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
        readonly=False,
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
                rec.agenda_item_ids = rec.team_id.generate_new_meeting_agenda(self)
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

    def action_start(self):
        self.ensure_one()
        self.state = 'in_progress'
        for headline in self.headline_ids:
            item = self.add_agenda_item(
                name=headline.summary,
                description=headline.note,
                item_type='headline',
                activity_id=headline.id
            )
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

    def add_agenda_item(self, name: str, description: str = "", item_type: str = 'other', section_subtype: str = None,
                        duration=5, activity_id=None):
        """ Add an item to the agenda of this calendar event. Passing type='issue' or type='headline' will
        attempt to add the item to the appropriate section in the agenda (assuming one exists).

        :param name: Name of the agenda item
        :param description: The description of the agenda item
        :param item_type: The type of agenda item to add. See item_type field in
                          traction/models/calendar_event_action_item.py
        :param section_subtype: 'issue', 'headline' or None. Applicable only if type=='section'
        :param duration: The duration of the agenda item, in minutes
        :param activity_id: The activity to attach the new agenda item to (issue or headline, usually)

        :return: Recordset containing the items created
        """
        self.ensure_one()
        sequence = self._get_next_sequence(section_type=item_type)

        return self.env['calendar.event.agenda.item'].create({
            'name': name,
            'description': description,
            'sequence': sequence,
            'item_type': item_type,
            'section_subtype': section_subtype,
            'duration': duration,
            'event_id': self.id,
            'activity_id': activity_id,
        })

    def _get_next_sequence(self, section_type=None):
        # Put it at the end by default
        sequence = max(self.agenda_item_ids.mapped('sequence')) + 1
        section_type = ({
            'issue': 'issues',
            'headline': 'headlines',
        }).get(section_type, False)
        if section_type in ('issues', 'headlines'):
            new_section_item = self.agenda_item_ids.filtered(
                lambda item: item.item_type == 'section' and item.section_subtype == section_type
            )
            if new_section_item:
                new_section_item = new_section_item[0]
                sections = list(self.agenda_item_ids.sorted('sequence', reverse=True).filtered(
                    lambda item: item.item_type == 'section'
                ))
                # Check if there are other sections. If so, we need to figure out what sequence number to use.
                if len(sections) > 1:
                    all_items = list(self.agenda_item_ids.sorted('sequence', reverse=True))
                    next_section = sections[sections.index(new_section_item) + 1]
                    next_section_index = all_items.index(next_section)
                    last_item_in_section = all_items[next_section_index - 1]
                    if last_item_in_section.sequence == next_section.sequence - 1:
                        # We need to bump the next items to higher sequence numbers
                        for item in all_items[next_section_index:]:
                            item.sequence += 10
                    sequence = last_item_in_section.sequence + 1
        return sequence
