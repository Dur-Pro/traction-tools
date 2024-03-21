from odoo import api, models, fields, _
from datetime import datetime


class MailChannel(models.Model):
    _inherit = ['discuss.channel']

    traction_team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        index=True
    )

    is_traction_team = fields.Boolean(string='Is Traction Team')

    def _process_traction_team_in_vals(self, vals):
        if 'is_traction_team' in vals and vals['is_traction_team'] and not self.traction_team_id:
            # See if there is already a team by this name to link
            team = self.env['traction.team'].search([
                ('name', '=', self.name)
            ])
            if team:
                self.traction_team_id = team
            else:
                self.env['traction.team'].create({
                    'name': self.name,
                    'channel_ids': [(4, self.id)],
                })
        if 'is_traction_team' in vals and not vals['is_traction_team']:
            self.traction_team_id = False

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._process_traction_team_in_vals(vals)
        return res

    def write(self, vals):
        super().write(vals)
        self._process_traction_team_in_vals(vals)

