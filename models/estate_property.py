from odoo import fields, models, tools, api
from odoo.exceptions import UserError, AccessError
from odoo.tools.translate import _

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=tools.date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_orientation = fields.Selection([('north', 'North'), (['south', 'South']), ('east', 'East'), ('west', 'West')], string='Garden Orientation')
    garden_area = fields.Integer('Garden Area (sqm)')
    living_area = fields.Integer('Living Area (sqm)')
    total_area = fields.Integer('Total Area (sqm)', compute='_total_area')
    active = fields.Boolean(default=True)
    state = fields.Selection([('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('canceled','Canceled')], required=True, default='new')
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.uid)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float('Best Offer', compute='_get_best_offer', default=0)

    @api.depends('living_area', 'garden_area')
    def _total_area(self):
        for estateProperty in self:
            estateProperty.total_area = estateProperty.living_area + estateProperty.garden_area

    @api.depends('offer_ids')
    def _get_best_offer(self):
        for estateProperty in self:
            if len(estateProperty.offer_ids) == 0:
                estateProperty.best_price = 0
            else:
                estateProperty.best_price = max(estateProperty.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for estateProperty in self:
            if estateProperty.state == 'canceled':
                raise UserError(_("A canceled property cannot be set as sold"))
            else:
                estateProperty.state = 'sold'
        return True

    def action_cancel_property(self):
        for estateProperty in self:
            if estateProperty.state == 'sold':
                raise UserError(_("A sold property cannot be canceled"))
            else:
                estateProperty.state = 'canceled'
        return True