from odoo import api, fields, models
from datetime import timedelta


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

