from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1)
    description = fields.Text()
    date_availability = fields.Date()
    selling_price = fields.Float()
    discount = fields.Integer("discount_%")
    new_price = fields.Float(compute='_compute_new_price')
    bedrooms = fields.Integer()
    garden = fields.Boolean()
    active = fields.Boolean(default=1)  # archiving
    sequence = fields.Char(default='NEW', readonly=1)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    property_owner_id = fields.Many2one('property.owner')
    owner_address = fields.Char(related='property_owner_id.address')
    owner_phone = fields.Char(related='property_owner_id.phone')

    tags_ids = fields.Many2many('tags')

    line_ids = fields.One2many('property.line', 'property_id')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'this name is already exist!'),
    ]

    @api.depends('selling_price', 'discount')
    def _compute_new_price(self):
        for rec in self:
            rec.new_price = rec.selling_price - (rec.selling_price * rec.discount / 100)

    # validation for bedrooms field
    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('enter number of bedrooms')
            elif rec.bedrooms < 0:
                raise ValidationError('enter positive number')

    @api.constrains('discount')
    def _check_discount(self):
        for rec in self:
            if rec.discount > 100:
                raise ValidationError('discount have to be from 0 to 100')
            elif rec.discount < 0:
                raise ValidationError('enter positive number')

    # adding sequence
    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.sequence == 'NEW':
            res.sequence = self.env['ir.sequence'].next_by_code('property_seq')
            return res

    def draft_action(self):
        for rec in self:
            rec.state = 'draft'

    def pending_action(self):
        for rec in self:
            rec.state = 'pending'

    def sold_action(self):
        for rec in self:
            rec.state = 'sold'

    def closed_action(self):
        for rec in self:
            rec.state = 'closed'


class PropertyLine(models.Model):
    _name = "property.line"
    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
