class PosConfig(models.Model):
    _name = 'pos.config'
    
    pos_analytic_account_ids = fields.Many2many(
        'account.analytic.account', 
        string='Cuentas analíticas', 
        domain=lambda self: [('company_id', '=', self.env.company.id)],
        copy=False
    )