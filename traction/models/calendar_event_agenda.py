from odoo import models, fields, api, _


class Agenda(models.Model):
    _name="calendar.event.agenda"
    _description="Meeting Agenda"

    name=fields.Char(
        compute="_compute_name",
        store=True
    )

    meeting_id = fields.Many2one(
        comodel_name="calendar.event",
        compute="_compute_meeting_id",
        ondelete="cascade",
        store=True,
    )

    meeting_ids = fields.One2many(
        comodel_name="calendar.event",
        inverse_name="agenda_id",
    )

    item_ids = fields.One2many(
        comodel_name="calendar.event.agenda.item",
        inverse_name="agenda_id",
    )

    @api.depends("meeting_id")
    def _compute_name(self):
        for rec in self:
            if not rec.meeting_id:
                rec.name = "New Agenda"
            else:
                meeting_date = rec.meeting_id.start.strftime("%Y-%m-%d")
                rec.name = f"{meeting_date} - {rec.name}"

    @api.depends("meeting_ids")
    def _compute_meeting_id(self):
        for rec in self:
            rec.meeting_id = rec.meeting_ids and rec.meeting_ids[0] or False