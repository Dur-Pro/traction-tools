from odoo import api, fields, models, _
from datetime import timedelta


class MeetingAgendaItem(models.Model):
    _name = 'calendar.event.agenda.item'
    _description = 'Meeting Agenda Item'
    _order = 'sequence asc'

    agenda_id = fields.Many2one(
        string="Agenda",
        comodel_name="calendar.event.agenda",
        ondelete="cascade",
    )
    meeting_id = fields.Many2one(
        string='Event',
        comodel_name='calendar.event',
        related="agenda_id.meeting_id",
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    name = fields.Char(
        string='Topic',
        required=True,
    )
    duration = fields.Integer(
        string="Duration (minutes)",
        required=True,
    )
    description = fields.Html(
        string='Description',
    )
    discussed = fields.Boolean(
        string='Discussed',
    )

    def action_discussed(self):
        return self.write({'discussed': True})

    def action_reset(self):
        return self.write({'discussed': False})
