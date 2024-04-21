from odoo import models, fields, api
from odoo.tools import date_utils
from datetime import date, datetime, time, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity (days)', default='7')
    date_deadline = fields.Date('Deadline', compute='_get_deadline', inverse='_inverse_deadline')

    @api.depends('validity', 'date_deadline')
    def _get_deadline(self):
        for offer in self:
            if offer.create_date:
                created = offer.create_date
            else:
                created = fields.Date.today()
            offer.date_deadline = date_utils.add(created, days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date:
                created = offer.create_date
            else:
                created = fields.Date.today()
            offer.validity = (offer.date_deadline - created.date()).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            other_offers = self.search([('id', '!=', offer.id)])
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True