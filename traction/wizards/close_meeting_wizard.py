from odoo import models, fields, api, _
from datetime import datetime, timedelta


class CloseMeetingWizard(models.TransientModel):
    _name = 'close.meeting.wizard'
    _description = 'Close Meeting Wizard'

    meeting_id = fields.Many2one(comodel_name='calendar.event',
                                 string='Meeting',
                                 readonly=True)

    next_meeting_time = fields.Datetime(string='Next Meeting Time', )

    send_meeting_minutes = fields.Boolean(default=True)
    name = fields.Char(related='meeting_id.name', readonly=True)

    def default_get(self, fields_list):
        res = super(CloseMeetingWizard, self).default_get(fields_list)
        meeting = False
        if 'meeting_id' in fields_list and 'active_id' in self.env.context:
            meeting = self.env['calendar.event'].browse(self.env.context.get('active_id'))
            res.update({'meeting_id': meeting.id})
        if 'next_meeting_time' in fields_list:
            if meeting:
                res.update({'next_meeting_time': meeting.start + timedelta(days=7)})
            else:
                res.update({'next_meeting_time': False})
        if 'name' in fields_list:
            if not meeting:
                res.update({'name': False})
            else:
                res.update({'name': meeting.name})
        return res

    def action_close_meeting(self):
        self.ensure_one()
        self.meeting_id.action_close_meeting(
            send_minutes=self.send_meeting_minutes,
            next_meeting_time=self.next_meeting_time
        )
        return {
            'type': 'ir.actions.act_window_close',
            'context': self.env.context,
        }
