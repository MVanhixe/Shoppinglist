from odoo import api, fields, models

class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    name = fields.Char('Title', required=True)