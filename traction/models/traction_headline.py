from odoo import models, fields, api, _


class TractionHeadline(models.Model):
    _name = "traction.headline"
    _description = "Headline"

    team_id = fields.Many2one(
        comodel_name="traction.team",
        string="Team",
    )
    summary = fields.Char(
        string="Summary",
        translate=True,
        help="Just the headline please!",
    )
    extra_info = fields.Html(
        string="Extra Information",
        translate=True,
        help="Extra Information",
    )
    status = fields.Selection(
        selection=(
            ('new', 'New'),
            ('discussed', 'Discussed'),
        )
    )

    def action_recommunicate(self):
        """
        JUST A STUB. This method should take a headline and raise a wizard for recommunicating it to other teams and/or
        other users (as a notification).
        """
        # TODO: Write this functionality
        pass

    def action_done(self):
        self.write({"status": "discussed"})

    def save_and_close(self):
        return {"type": "ir.actions.act_window_close"}
