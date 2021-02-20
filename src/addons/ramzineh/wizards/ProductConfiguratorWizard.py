from ..ramzineh import models, fields, api, Ramzineh, ProductSpec, Constants


class ProductConfiguratorWizard(models.TransientModel):
    _name = "ramzineh.productconfigurator.wizard"
    add_product = fields.Boolean()
    rmz_product_type = fields.Selection(
        list(Ramzineh.constants.product_types.items()),
        string='Type')
    rmz_paper_type = fields.Selection(
        list(Ramzineh.constants.paper_types.items()),
        string='Paper Type')

    rmz_glue_type = fields.Selection(
        list(Ramzineh.constants.glue_types.items()),
        string='Glue Type')

    rmz_bobin_size = fields.Selection(
        list(Ramzineh.constants.bobin_size.items()), string='Bobin Size')

    rmz_number_of_rows = fields.Integer(string='Number of Rows')
    rmz_total_count = fields.Integer(string='Total Count')
    rmz_width = fields.Integer(string='Label Width (mm)')
    rmz_length = fields.Integer(string='Label Length (mm)')
    rmz_role_length = fields.Integer(string='Role Length (m)')
    rmz_role_width = fields.Integer(string='Role Width (cm)')
    rmz_printed_text = fields.Char(string="Printed Text")
    product_id = fields.Many2one('product.template', 
        string="Found:",
        compute='_compute_product_id', readonly=True)

    product_name=fields.Char(compute = "_compute_name", string="Name", readonly = True)
    product_desc=fields.Char(compute = "_compute_desc", string="Description", readonly = True)
    rmz_error = fields.Char(compute = "_compute_error", string="Error", readonly = True)
    rmz_warn = fields.Char(compute = "_compute_warn", string="Warn", readonly = True)

    sale_order_id=fields.Many2one(
        "sale.order",
        "Sale Order",
        default = lambda self: self._default_sale_order_id(),
        required = True,
        readonly = True,
        ondelete = "cascade",
    )

    def _to_spec(self):
        return ProductSpec(
            self.rmz_product_type, self.rmz_paper_type,
            self.rmz_glue_type, self.rmz_bobin_size, self.rmz_number_of_rows, self.rmz_total_count, self.rmz_width,
            self.rmz_length, self.rmz_role_length, self.rmz_role_width, self.rmz_printed_text)


    @api.depends('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _compute_name(self):
        for record in self:
            record.product_name=self._to_spec().get_code()

    @api.depends('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _compute_desc(self):
        for record in self:
            record.product_desc=self._to_spec().get_description()

    @api.depends('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _compute_product_id(self):
        for record in self:
            record.product_id=Ramzineh.product_templates(self).get_product_by_specs(self._to_spec(), False)
    
    @api.depends('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _compute_error(self):
        for record in self:
            record.rmz_error= self._to_spec().error()
    
    @api.depends('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _compute_warn(self):
        for record in self:
            record.rmz_warn= self._to_spec().warn()




    @api.model
    def _default_sale_order_id(self):
        is_salorder = self.env.context.get('active_model','')=='sale.order'
        return  self.env.context.get("active_id", False) if is_salorder else False

    def action_create(self):
        Ramzineh.product_templates(self).get_product_by_specs(
            self._to_spec(), auto_create = True)
        return {"type": "ir.actions.do_nothing", }


    def action_add_product(self):
        print('action_configure')
        p = Ramzineh.product_templates(self).get_product_by_specs(self._to_spec())
        p1 = self.env['product.product'].browse(self.product_id.id)
        if self.product_id and self.env.context.get('active_model','')=='sale.order':
            saleorder = self.env.context.get("active_id", False) 
            if saleorder:
                #self.refresh()
                #self.env['sale.order.line'].refresh()
                #self.env['product.product'].refresh()
                self.env['sale.order.line'].create([{
                'order_id': saleorder,
                #'product_template_id': p.id,
                'product_id': p.product_variant_id.id,
            }])
            return {}
        
        return {"type": "ir.actions.do_nothing", }
