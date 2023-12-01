from odoo import api, fields, models, _
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
        string='Related Activity'
    )

    identify_discuss_solve_id = fields.Many2one(
        comodel_name='traction.identify_discuss_solve',
        related='activity_id.identify_discuss_solve_id',
        readonly=False,
    )

    def action_discussed(self):
        return self.write({'discussed': True})

    def action_reset(self):
        return self.write({'discussed': False})

    def action_start_ids(self):
        self.ensure_one()
        if not self.identify_discuss_solve_id:
            self.identify_discuss_solve_id = self.env['traction.identify_discuss_solve'].create({
                'issue_id': self.activity_id.id,
                'meeting_ids': [(4, self.event_id.id)]
            })
        return {
            'name': (_('Issue IDS')),
            'view_mode': 'form',
            'res_model': 'traction.identify_discuss_solve',
            'res_id': self.identify_discuss_solve_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
