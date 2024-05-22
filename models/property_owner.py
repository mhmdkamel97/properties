from odoo import models, fields


class PropertyOwner(models.Model):
    _name = 'property.owner'

    name = fields.Char(requied=1)
    address = fields.Char()
    phone = fields.Char()
    property_ids = fields.One2many('property', 'property_owner_id')
