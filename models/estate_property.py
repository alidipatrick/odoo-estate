from odoo import fields, models, tools

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=tools.date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([('north', 'North'), (['south', 'South']), ('east', 'East'), ('west', 'West')], string='Garden Orientation')
    active = fields.Boolean(default=True)
    state = fields.Selection([('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('canceled','Canceled')], required=True, default='new')