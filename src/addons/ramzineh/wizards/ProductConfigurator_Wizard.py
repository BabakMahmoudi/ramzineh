from ..ramzineh import models, fields, api, Ramzineh, ProductSpec


class ProductConfiguratorWizard(models.TransientModel):
    _name = "ramzineh.productconfigurator.wizard"

    add_product = fields.Boolean()
    rmz_product_type = fields.Selection([
        ('J', 'jambo'),
        ('R', 'role'),
        ('L', 'label'),
        ('M', 'sayer')],
        string='Type')

    rmz_paper_type = fields.Selection([
        ('SDF', 'sadafi'),
        ('KGH', 'kaghazi'),
        ('MTK', 'metalize kaghazi'),
        ('LSH', 'laieh shavandeh'),
        ('GCH', 'gachi'),
        ('VOD', 'void'),
        ('TMP', 'tamper'),
        ('HRT', 'hararati'),
        ('TRN', 'transparent'),
        ('MTP', 'metalize pp'),
        ('AML', 'amval'),
        ('MSC', 'saier'),
    ], string='Paper Type')

    rmz_glue_type = fields.Selection([
        ('A', 'acronal'),
        ('H', 'hot melt'),
        ('MSC', 'saier'),
    ], string='Glue Type')

    rmz_bobin_size = fields.Selection([
        ('B', 'bozorg'),
        ('K', 'koochak'),
        ('M', 'saier'),
    ], string='Bobin Size')

    rmz_number_of_rows = fields.Integer(string='Number of Rows')
    rmz_width = fields.Integer(string='Label Width')
    rmz_length = fields.Integer(string='Label Length')
    rmz_role_length = fields.Integer(string='Role Length')
    rmz_role_width = fields.Integer(string='Role Width')

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sale Order",
        default=lambda self: self._default_sale_order_id(),
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    @api.model
    def _default_sale_order_id(self):
        #is_salorder = self.env.context.get('active_model','')=='sale.order'

        return self.env.context.get("active_id", False)

    def action_add_product(self):
        print('action_configure')
        p = Ramzineh.find_product(self,ProductSpec(
            self.rmz_product_type, self.rmz_paper_type, 
            self.rmz_glue_type, self.rmz_bobin_size,self.rmz_number_of_rows, self.rmz_width,
            self.rmz_length, self.rmz_role_length, self.rmz_role_width))
        print(p)
        
