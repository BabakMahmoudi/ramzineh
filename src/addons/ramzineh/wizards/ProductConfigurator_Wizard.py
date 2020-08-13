from ..ramzineh import models, fields, api, Ramzineh, ProductSpec,Constants


class ProductConfiguratorWizard(models.TransientModel):
    _name = "ramzineh.productconfigurator.wizard"
    add_product = fields.Boolean()
    rmz_product_type = fields.Selection(
        list(Ramzineh.constants.product_types.items()),
        string='Type')
    rmz_paper_type = fields.Selection(
        list(Ramzineh.constants.paper_types.items()) , 
        string='Paper Type')

    rmz_glue_type = fields.Selection(
        list(Ramzineh.constants.glue_types.items()), 
        string='Glue Type')

    rmz_bobin_size = fields.Selection(
        list(Ramzineh.constants.bobin_size.items()), string='Bobin Size')

    rmz_number_of_rows = fields.Integer(string='Number of Rows')
    rmz_total_count = fields.Integer(string='Total Count')
    rmz_width = fields.Integer(string='Label Width')
    rmz_length = fields.Integer(string='Label Length')
    rmz_role_length = fields.Integer(string='Role Length')
    rmz_role_width = fields.Integer(string='Role Width')
    rmz_printed_label = fields.Char(string="Printed Label")

    product_ids = fields.One2many(
        'product.template', compute='_compute_product_ids', readonly=True)

    product_name = fields.Char(compute="_compute_name", readonly=True)


    sale_order_id = fields.Many2one(
        "sale.order",
        "Sale Order",
        default=lambda self: self._default_sale_order_id(),
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    def _to_spec(self):
        return ProductSpec(
            self.rmz_product_type, self.rmz_paper_type, 
            self.rmz_glue_type, self.rmz_bobin_size,self.rmz_number_of_rows, self.rmz_total_count, self.rmz_width,
            self.rmz_length, self.rmz_role_length, self.rmz_role_width, self.rmz_printed_label)


    @api.depends('rmz_paper_type','rmz_product_type','rmz_glue_type','rmz_bobin_size',
    'rmz_number_of_rows','rmz_total_count','rmz_width','rmz_length','rmz_role_length','rmz_role_width')
    def _compute_name(self):
        for record in self:
            record.product_name = self._to_spec().get_code()



    @api.depends('rmz_paper_type')
    def _compute_product_ids(self):
        
        for record in self:
            record.product_ids = Ramzineh.find_product(self,self._to_spec(),False)

    @api.model
    def _default_sale_order_id(self):
        #is_salorder = self.env.context.get('active_model','')=='sale.order'
        

        return self.env.context.get("active_id", False)

    def action_create(self):
        Ramzineh.product_templates(self).get_product_by_specs(self._to_spec(),auto_create=True)
        return {"type": "ir.actions.do_nothing", }


    def action_add_product(self):
        print('action_configure')
        ggg = Ramzineh.constants.bobin_size.items()
        p = Ramzineh.find_product(self,ProductSpec(
            self.rmz_product_type, self.rmz_paper_type, 
            self.rmz_glue_type, self.rmz_bobin_size,self.rmz_number_of_rows, self.rmz_total_count, self.rmz_width,
            self.rmz_length, self.rmz_role_length, self.rmz_role_width))
        #print(p)
        # prevent wizard from closing
        # https://stackoverflow.com/questions/31963214/odoo-prevent-button-from-closing-wizard
        return {"type": "ir.actions.do_nothing", }
        
