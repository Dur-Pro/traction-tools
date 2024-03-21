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
        compute='_compute_member_ids',
        store=True,
        compute_sudo=True,
    )
    channel_ids = fields.One2many(
        comodel_name='discuss.channel',
        inverse_name='traction_team_id',
        string='Channels'
    )
    issues_list_ids = fields.Many2many(
        comodel_name='traction.issues.list',
        string='Issues Lists',
        relation='traction_team_issues_list_rel',
        column1='team_id',
        column2='issues_list_id',
        help="Issues lists that this team is tracking."
    )
    headline_ids = fields.One2many(
        comodel_name='traction.headline',
        inverse_name="team_id",
        string='Headlines'
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
    issues_count = fields.Integer(compute='_compute_issues_count', compute_sudo=True)
    agenda_template_id = fields.Many2one(
        string="Default Meeting Agenda",
        comodel_name="calendar.event.agenda.template",
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.agenda_template_id = self.env.ref('traction.calendar_event_agenda_template_default')
        return res

    @api.depends('meeting_ids')
    def _compute_next_meeting(self):
        for rec in self:
            upcoming_meetings = rec.meeting_ids.filtered(
                lambda meeting: meeting.start > datetime.now()
            ).sorted(key=lambda meeting: meeting.start)
            rec.next_meeting_id = upcoming_meetings and upcoming_meetings[0]

    @api.depends('issues_list_ids')
    def _compute_issues_count(self):
        for rec in self:
            rec.issues_count = sum(rec.issues_list_ids.mapped('issues_count'))

    @api.depends('channel_ids', 'channel_ids.channel_partner_ids', 'channel_ids.channel_partner_ids.user_ids')
    def _compute_member_ids(self):
        for rec in self:
            rec.member_ids = rec.channel_ids.mapped('channel_partner_ids').mapped('user_ids')

    def action_open_issues_lists(self):
        self.ensure_one()
        return {
            "name": f"Issues for {self.name}",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,form",
            "res_model": "traction.issues.list",
            "domain": [["team_ids", "in", [self.id]]],
            "context": {"default_team_ids": [self.id]}
        }
