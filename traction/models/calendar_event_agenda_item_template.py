from odoo import models, fields, api, _, Command


class CalendarEventAgendaItemTemplate(models.Model):
    _name = 'calendar.event.agenda.item.template'
    _description = 'Calendar Event Agenda Item Template'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )

    name = fields.Char(
        string='Topic',
        required=True,
    )

    duration = fields.Integer(
        string='Duration (minutes)',
        required=True,
        default=5,
    )

    description = fields.Text(
        string='Description / Notes',
    )

    template_ids = fields.Many2many(
        comodel_name='calendar.event.agenda.template',
        string='Agenda Templates',
        relation='calendar_event_agenda_item_template_rel',
        column1='item_id',
        column2='template_id',
    )

    def copy_as_agenda_items(self, agenda):
        """
        Create a new calendar.event.agenda.item based on this template and attach it to meeting.
        This method is applicable on Recordsets containing multiple records.

        :param agenda: The calendar.event.agenda record to which the new agenda items should be attached.
        :return: The agenda item created.
        """
        new_items = self.env['calendar.event.agenda.item']
        for rec in self:
            new_items |= rec._copy_as_agenda_item(agenda)
        return new_items

    def _copy_as_agenda_item(self, agenda):
        """
        Private helper method to execute the creation of a single agenda item from a template.

        :param meeting: The meeting to which the agenda item should be attached.
        :return: The newly created agenda item.
        """
        self.ensure_one()
        return self.env['calendar.event.agenda.item'].create({
            'sequence': self.sequence,
            'name': self.name,
            'duration': self.duration,
            'description': self.description,
            'agenda_id': agenda.id,
        })
