from odoo import models, fields, api, Command


class TractionRockUpdate(models.Model):
    _name = "traction.rock.update"
    _description = "Rock Status Update"

    summary = fields.Char(required=True)
    status = fields.Selection(
        selection=(
            ("on_track", "On Track"),
            ("off_track", "Off Track"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ),
        required=True,
    )
    rock_id = fields.Many2one(
        comodel_name="traction.rock",
        string="Rock",
        required=True,
    )
    comments = fields.Text()
    date = fields.Date(
        required=True,
    )
    meeting_ids = fields.Many2many(
        comodel_name="calendar.event",
        relation="traction_rock_update_meeting_rel",
        column1="rock_update_id",
        column2="meeting_id",
        compute="_compute_meeting_ids",
        store=True,
    )

    @api.depends("date", "rock_id")
    def _compute_meeting_ids(self):
        for rec in self:
            meeting_ids = self.env["calendar.event"]
            for team in rec.rock_id.team_ids:
                after = team.meeting_ids.filtered(
                    lambda meeting: meeting.start_date >= self.date
                ).sorted("start_date")
                if after:
                    meeting_ids |= after[0]
            rec.meeting_ids = [Command.set(meeting_ids)]
