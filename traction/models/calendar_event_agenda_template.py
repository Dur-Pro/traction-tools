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

    def generate_agenda(self, meeting):
        """
        Generate a new calendar.event.agenda for a specific calendar.event. Expected to be called on a single record.

        :param meeting: The calendar.event record to which this agenda pertains.
        """
        self.ensure_one()
        agenda = self.env['calendar.event.agenda'].create({
            'meeting_ids': [Command.set([meeting.id])],
        })
        self.agenda_item_ids.copy_as_agenda_items(agenda)
        return agenda
