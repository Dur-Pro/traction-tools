from odoo import models, fields, api, _, Command


class CalendarEventAgendaTemplate(models.Model):
    _name = 'calendar.event.agenda.template'
    _description = 'Calendar Event Agenda Template'

    name = fields.Char()
    agenda_item_ids = fields.Many2many(
        string='Agenda Items',
        comodel_name='calendar.event.agenda.item.template',
        relation='calendar_event_agenda_item_template_rel',
        column1='template_id',
        column2='item_id',
    )

    traction_team_ids = fields.One2many(
        comodel_name='traction.team',
        inverse_name='agenda_template_id',
    )
    # TODO: Look at adding other template items like duration, start time, etc.

    def generate_new_meeting_agenda_items(self, meeting):
        """
        Generate a full meeting agenda from this template and attach it to meeting.

        :param meeting: The meeting to which newly created agenda items should be linked.
        :return: Recordset containing the created calendar.event.agenda.item records (already attached to meeting)
        """
        return self.agenda_item_ids.copy_as_agenda_items(meeting)

