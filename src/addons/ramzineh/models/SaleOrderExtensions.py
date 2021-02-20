from ..ramzineh import SaleOrder, SaleOrderLine, api,fields,Ramzineh,ProductTemplateExtensions

class SaleOrderExtensions(SaleOrder):
    _inherit = "sale.order"
    # rmz_reference = fields.Char()

class SaleOrderLineExtensions(SaleOrderLine):
    _inherit = "sale.order.line"

    #ramzineh_units = fields.Float(string="Units")
    rmz_qty_roles = fields.Float(compute="_compute_qty_roles", string="Qty Roles")
    def action_select(self):
        print('here')
        m = self.env['ramzineh.productconfigurator.wizard']
    
    @api.depends('product_uom_qty','product_uom')
    def _compute_qty_roles(self):
        for _rec in self:
            rec:SaleOrderExtensions = _rec
            p:ProductTemplateExtensions = rec.product_template_id
            if p and p._to_spec().total_count>0 :
                rec.rmz_qty_roles = rec.product_uom_qty/p._to_spec().total_count
            else:
                rec.rmz_qty_roles = 0
    
    @api.onchange('product_id')
    def product_id_change(self):
        print('here')
        res = super(SaleOrderLineExtensions, self).product_id_change()
        p:ProductTemplateExtensions = self.product_template_id
        if p:
            self.product_uom = p._get_default_sale_uom_id()
        return res
        
        