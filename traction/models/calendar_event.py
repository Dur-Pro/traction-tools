from odoo import api, fields, models

class Meeting(models.Model):
    _inherit = ["calendar.event"]

    level10_id = fields.Many2one(
        comodel_name='traction.level10',
        string='Level 10',
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

    traction_items = fields.One2many(
        string='Headline & Issue',
        comodel_name='mail.activity',
        inverse_name='meet_id',
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

    # GONNA BE A RELATED FIELD TO LEVEL10
    # future_traction_items = fields.One2many(
    #     string='Headline & Issue',
    #     comodel_name='mail.activity',
    #     inverse_name='meet_id',
    # )



    @api.model
    def create(self, vals):
        if vals.get('level10_id'):
            level10_id = self.env['traction.level10'].browse(vals.get('level10_id'))
            vals['name'] = "Level 10 - " + level10_id.name

        result = super(Meeting, self).create(vals)
        return result

    @api.onchange('level10_id')
    def _rename_meet(self):
        for meeting in self:
            if meeting.level10_id:
                meeting.name = "Level 10 - " + meeting.level10_id.name
            else:
                meeting.name = "Replace me please"
            meeting.update({'name': meeting.name})

    def _compute_is_responsible_user(self):
        for event in self:
            event.is_responsible_user = (self.env.user == event.user_id or
                                         self.env.user == event.note_taker_user_id or
                                         self.env.user._is_admin())

    def action_send_mm(self):
        template = self.env.ref('traction.calendar_event_report_for_attendees')
        for event in self:
            recipient_ids = [(4, pid) for pid in event.partner_ids.ids]
            template.send_mail(event.id, email_values={'recipient_ids': recipient_ids})







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
    description = fields.Text(
        string='Description / Notes',
    )
