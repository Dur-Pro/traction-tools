from odoo import api, models, fields, _
from datetime import datetime


class TractionTeam(models.Model):
    _name = 'traction.team'
    _description = 'Traction Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')

    member_ids = fields.Many2many(
        comodel_name='res.users',
        string='All Members',
        compute='_compute_member_ids'
    )

    channel_ids = fields.One2many(
        comodel_name='mail.channel',
        inverse_name='traction_team_id',
        string='Channels'
    )

    activity_ids = fields.One2many(
        comodel_name='mail.activity',
        inverse_name='team_id',
        string='Activity'
    )

    issue_ids = fields.One2many(
        comodel_name='mail.activity',
        compute='_compute_issues_headlines',
        inverse='_inverse_issues_headlines',
        string='Issues'
    )

    headline_ids = fields.One2many(
        comodel_name='mail.activity',
        compute='_compute_issues_headlines',
        inverse='_inverse_issues_headlines',
        string='Headlines'
    )

    measurable_ids = fields.Many2many(
        comodel_name='traction.measurable',
        string='Measurable'
    )

    meeting_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='team_id',
        string='Meetings'
    )

    next_meeting_id = fields.Many2one(
        comodel_name='calendar.event',
        compute='_compute_next_meeting',
    )

    next_meeting_time = fields.Datetime(related='next_meeting_id.start')
    next_meeting_duration = fields.Float(related='next_meeting_id.duration')
    issues_count = fields.Integer(compute='_compute_issues_count')

    agenda_template_id = fields.Many2one(
        comodel_name='calendar.event.agenda.template',
        string='Default Meeting Agenda',
        help='The agenda used by default when a meeting is created. '
             'Does not apply to meetings created as next meeting when closing a meeting.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.agenda_template_id = self.env.ref('traction.calendar_event_agenda_template_default')
        return res

    @api.depends('meeting_ids')
    def _compute_next_meeting(self):
        for rec in self:
            rec.next_meeting_id = rec.meeting_ids.filtered(
                lambda meeting: meeting.start > datetime.now()
            ).sorted(key=lambda meeting: meeting.start)

    @api.depends('issue_ids')
    def _compute_issues_count(self):
        for rec in self:
            rec.issues_count = len(rec.issue_ids)

    @api.depends('channel_ids.channel_partner_ids')
    def _compute_member_ids(self):
        for record in self:
            members = record.member_ids
            for channel in record.channel_ids:
                members |= channel.channel_partner_ids.user_ids
            record.member_ids = members

    @api.depends('activity_ids')
    def _compute_issues_headlines(self):
        for rec in self:
            rec.issue_ids = rec.activity_ids.filtered(lambda l: l.activity_type_id == self.env.ref(
                'traction.mail_activity_data_issue'))
            rec.headline_ids = rec.activity_ids.filtered(
                lambda l: l.activity_type_id == self.env.ref('traction.mail_activity_data_headline'))

    def _inverse_issues_headlines(self):
        pass

    def generate_new_meeting_agenda(self, meeting):
        """
        Generate a new meeting agenda from this team's default meeting agenda template. Applicable on singletons only.

        :param meeting: The meeting to which the new agenda should be attached.
        :return: The Recordset containing the newly created agenda items.
        """
        self.ensure_one()
        return self.agenda_template_id.generate_new_meeting_agenda_items(meeting)
