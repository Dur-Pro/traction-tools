from odoo import api, models, fields, _
from datetime import datetime


class TractionRock(models.Model):
    _name = "traction.rock"
    _description = "Rock"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Html()
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        index=True,
    )
    team_ids = fields.Many2many(
        comodel_name="traction.team",
        string="Teams",
        relation="traction_rock_team_rel",
        column1="rock_id",
        column2="team_id",
    )
    start_date = fields.Date()
    due_date = fields.Date()
    status_update_ids = fields.One2many(
        comodel_name="traction.rock.update",
        inverse_name="rock_id",
    )
