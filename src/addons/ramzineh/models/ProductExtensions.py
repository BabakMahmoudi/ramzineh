from ..ramzineh import ProductTemplate, fields, api, models, Ramzineh, ProductSpec


class ProductTemplateExtensions(ProductTemplate):
    _inherit = "product.template"

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

    def find_spec(self, spec: ProductSpec, exact=True):

        filter = []
        if exact or spec.product_type:
            filter.append(('rmz_product_type', '=', spec.product_type))
        if exact or spec.paper_type:
            filter.append(('rmz_paper_type', '=', spec.paper_type))
        if exact or spec.bobin_size:
            filter.append(('rmz_bobin_size', '=', spec.bobin_size))
        if exact or spec.glue_type:
            filter.append(('rmz_glue_type', '=', spec.glue_type))
        if exact or spec.number_of_rows:
            filter.append(('rmz_number_of_rows', '=', spec.number_of_rows))
        if exact or spec.width:
            filter.append(('rmz_width', '=', spec.width))
        if exact or spec.length:
            filter.append(('rmz_length', '=', spec.length))
        if exact or spec.role_width:
            filter.append(('rmz_role_width', '=', spec.role_width))
        if exact or spec.role_length:
            filter.append(('rmz_role_length', '=', spec.role_length))
        return self.search(filter)
