from odoo import api, fields, models, exceptions, _

class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    name = fields.Char('Title', required=True)
    date_list = fields.Date('Date Created', copy=False, default=fields.Date.today(), readonly=True)
    state = fields.Selection(selection=[('new', 'New'), ('in_progress', 'In Progress'), ('on_hold', 'On Hold'),
                                                    ('finished', 'Finished'), ('cancel', 'Cancelled')],
                             default='new', required=True, copy=False, string='State')
    status_name = fields.Many2one('status.list', string='Status', default='New', compute='_compute_status', store=True)
    detail_ids = fields.One2many('shopping.list.detail', 'list_id', string='Detail', copy=False)
    active = fields.Boolean('Active', default=True)

    @api.depends('state')
    def _compute_status(self):
        if self.state == 'new':
            self.status_name = self.env['status.list'].search([('name', 'ilike', self.state)])
        elif self.state == 'in_progress':
            self.status_name = 'In Progress'
        elif self.state == 'on_hold':
            self.status_name = 'On Hold'
        elif self.state == 'finished':
            self.status_name = 'Finished'
        elif self.state == 'cancel':
            self.status_name = 'Cancel'

    def action_set_finished(self):
        for record in self:
            if record.state == 'cancel':
                raise exceptions.UserError(_('You can not finish a list that is cancelled'))
            record.state = 'finished'

    def action_set_cancel(self):
        for record in self:
            if record.state == 'finished':
                raise  exceptions.UserError(_('You can not cancel a list that is finished'))
            record.state = 'cancel'

