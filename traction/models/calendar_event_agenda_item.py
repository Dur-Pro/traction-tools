from odoo import api, fields, models
from datetime import timedelta


class MeetingAgendaItem(models.Model):
    _name = 'calendar.event.agenda.item'
    _description = 'Meeting Agenda Item'
    _order = 'sequence asc'

    event_id = fields.Many2one(
        string='Event',
        comodel_name='calendar.event',
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
    duration = fields.Integer(
        string="Duration (minutes)",
        required=True,
    )
    item_type = fields.Selection(
        selection=[
            ('section', 'Section'),
            ('headline', 'Headline'),
            ('issue', 'Issue'),
            ('other', 'Other'),
        ])
    section_subtype = fields.Selection(
        selection=[
            ('issues', 'Issues'),
            ('headlines', 'Headlines'),
        ])
    description = fields.Html(
        string='Description / Notes',
    )
    discussed = fields.Boolean(
        string='Discussed',
    )
    activity_id = fields.Many2one(
        comodel_name='mail.activity',
        string='Related Activity')

    def action_discussed(self):
        return self.write({'discussed': True})

    def action_reset(self):
        return self.write({'discussed': False})
