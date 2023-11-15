from odoo import api, models, fields, _
from datetime import datetime


class MailChannel(models.Model):
    _inherit = ['mail.channel']

    traction_team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        index=True
    )

    is_traction_team = fields.Boolean(string='Is Traction Team')

    @api.model
    def create(self, vals):
        if 'is_traction_team' in vals and vals['is_traction_team']:
            vals['traction_team_id'] = self.env['traction.team'].create({
                'name': vals.get('name', ''),
                'channel_ids': [(4, self.id)],
            }).id
        return super().create(vals)

    # @api.onchange('is_traction_team')
    # def _onchange_is_traction_team(self):
    #     if self.is_traction_team:
    #         self.traction_team_id = self.env['traction.team'].create({
    #             'name': self.name,
    #             'channel_ids': [(4, self.id)],
    #         })
    #     else:
    #         if self.traction_team_id:
    #             self.traction_team_id.unlink()
    #         self.traction_team_id = False
