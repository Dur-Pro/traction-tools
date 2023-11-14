from odoo import api, fields, models
from datetime import timedelta


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
