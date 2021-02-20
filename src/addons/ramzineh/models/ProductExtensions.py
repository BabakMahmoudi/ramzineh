from __future__ import annotations
from ..ramzineh import ProductTemplate, fields, api, models, Ramzineh, ProductSpec


class ProductTemplateExtensions(ProductTemplate):
    _inherit = "product.template"
    # Product type can be jambo/role/label/Miscelaneous(other)
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
        list(Ramzineh.constants.bobin_size.items()),
        string='Bobin Size')

    rmz_number_of_rows = fields.Integer(string='Number of Rows')
    rmz_total_count = fields.Integer(string='Total Count')
    rmz_width = fields.Integer(string='Label Width (mm)')
    rmz_length = fields.Integer(string='Label Length (mm)')
    rmz_role_length = fields.Integer(string='Role Length (m)')
    rmz_role_width = fields.Integer(string='Role Width (cm)')
    rmz_printed_text = fields.Char(string="Printed Text")

    def _get_default_sale_uom_id(self):
        spec = self._to_spec()
        res = False
        if spec.is_paper() and spec.total_count>0:
            res = self.env['uom.uom'].get_by_spec(spec)
        if not res:
            res = self.env["uom.uom"].search([], limit=1, order='id').id
        return res

    rmz_sale_uom_id = fields.Many2one(
        'uom.uom', 'Sale Unit of Measure',
        default=_get_default_sale_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")



    def get_product_by_specs(self, spec: ProductSpec, auto_create=False) -> ProductTemplateExtensions:
        items = self.find_spec(spec)
        res = items[0] if len(items) > 0 else False
        if not res and auto_create:
            res = self.create({
                'rmz_product_type': spec.product_type,
                'rmz_paper_type': spec.paper_type,
                'rmz_glue_type': spec.glue_type,
                'rmz_bobin_size': spec.bobin_size,
                'rmz_number_of_rows': spec.number_of_rows,
                'rmz_total_count': spec.total_count,
                'rmz_width': spec.width,
                'rmz_length': spec.length,
                'rmz_role_length': spec.role_length,
                'rmz_role_width': spec.role_width,
                'rmz_printed_text': spec.printed_label
            })

        return res

    def find_spec(self, spec: ProductSpec, exact=True) -> ProductTemplateExtensions:
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
        if exact or spec.total_count:
            filter.append(('rmz_total_count', '=', spec.total_count))
        if exact or spec.width:
            filter.append(('rmz_width', '=', spec.width))
        if exact or spec.length:
            filter.append(('rmz_length', '=', spec.length))
        if exact or spec.role_width:
            filter.append(('rmz_role_width', '=', spec.role_width))
        if exact or spec.role_length:
            filter.append(('rmz_role_length', '=', spec.role_length))
        return self.search(filter)

    def _to_spec(self):
        return ProductSpec(
            self.rmz_product_type, self.rmz_paper_type,
            self.rmz_glue_type, self.rmz_bobin_size, self.rmz_number_of_rows, self.rmz_total_count, self.rmz_width,
            self.rmz_length, self.rmz_role_length, self.rmz_role_width, self.rmz_printed_text)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            name = vals.get('name', '')
            spec = ProductSpec(
                product_type=vals.get('rmz_product_type'),
                paper_type=vals.get('rmz_paper_type'),
                glue_type=vals.get('rmz_glue_type'),
                bobin_size=vals.get('rmz_bobin_size'),
                role_length=vals.get('rmz_role_length'),
                role_width=vals.get('rmz_role_width'),
                width=vals.get('rmz_width'),
                length=vals.get('rmz_length'),
                number_of_rows=vals.get('rmz_number_of_rows'),
                total_count=vals.get('rmz_total_count'),
                printed_label=vals.get('rmz_printed_text'),

            )
            if spec.is_paper():
                if Ramzineh.constants.use_code_for_name:
                    vals['name'] = spec.get_code()
                    vals['description_sale']=spec.get_description()
                else:
                    vals['default_code'] = spec.get_code()
                    vals['name']=spec.get_description()


            pass
        return super(ProductTemplateExtensions, self).create(vals_list)

    def write(self, vals):
        res = super(ProductTemplateExtensions, self).write(vals)
        for _p in self:
            p: ProductTemplateExtensions = _p
            s = p._to_spec()
            if s.is_paper():
                c =s.get_code()
                n = s.get_description()
                if Ramzineh.constants.use_code_for_name:
                    if p.name!= n:
                        res = super(ProductTemplateExtensions,
                                    self).write({'name': c})
                    if p.name != p.description_sale:
                        res = super(ProductTemplateExtensions,
                                    self).write({'description_sale': n})
                else:
                    if p.default_code != c:
                        res = super(ProductTemplateExtensions,
                                    self).write({'default_code': c})
                    if p.name!= n:
                        res = super(ProductTemplateExtensions,
                                    self).write({'name': n})
                    # if p.name != p.description_sale:
                    #     res = super(ProductTemplateExtensions,
                    #                 self).write({'description_sale': n})




        return res

    @api.onchange('rmz_paper_type', 'rmz_product_type', 'rmz_glue_type', 'rmz_bobin_size',
    'rmz_number_of_rows', 'rmz_total_count', 'rmz_width', 'rmz_length', 'rmz_role_length',
    'rmz_role_width', 'rmz_printed_text')
    def _recompute_name(self):
        for record in self:
            record.name=self._to_spec().get_code()

