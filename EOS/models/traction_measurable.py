from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'traction.measurable'
    _description = 'Description'

    name = fields.Char()
