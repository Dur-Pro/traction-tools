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

    item_type = fields.Selection(
        selection=[
            ('section', 'Section'),
            ('headline', 'Headline'),
            ('issue', 'Issue'),
            ('other', 'Other'),
        ]
    )

    section_subtype = fields.Selection(
        selection=[
            ('issues', 'Issues'),
            ('headlines', 'Headlines'),
        ])
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

    def copy_as_agenda_items(self, meeting):
        """
        Create a new calendar.event.agenda.item based on this template and attach it to meeting.
        This method is applicable on Recordsets containing multiple records.

        :param meeting: The meeting record to which the new agenda item should be attached.
        :return: The agenda item created.
        """
        new_items = self.env['calendar.event.agenda.item']
        for rec in self:
            new_items |= rec._copy_as_agenda_item(meeting)
        return new_items

    def _copy_as_agenda_item(self, meeting):
        """
        Private helper method to execute the creation of a single agenda item from a template.

        :param meeting: The meeting to which the agenda item should be attached.
        :return: The newly created agenda item.
        """
        self.ensure_one()
        return self.env['calendar.event.agenda.item'].create({
            'name': self.name,
            'duration': self.duration,
            'item_type': self.item_type,
            'section_subtype': self.section_subtype,
            'description': self.description,
            'event_id': meeting.id,
        })