from __future__ import annotations
from ..ramzineh import UoM, api, fields, ProductSpec


class UoMExtensions(UoM):
    _inherit = 'uom.uom'

    def get_units_category(self):
        return self.env['uom.category'].search([], limit=1, order='id')
    
    def get_by_spec(self, spec: ProductSpec, auto_create=True) -> UoMExtensions:
        res:UoMExtensions = False
        if spec.is_paper() and spec.total_count > 100:
            units_cat = self.get_units_category()
            name = spec.get_unit_name()
            items = self.search([('category_id','=',units_cat.id),('name','=',name)])
            res = items[0] if len(items)>0 else False
            if not res:
                res = self.sudo().create({
                    'category_id' : units_cat.id,
                    'name':name,
                    'uom_type':'smaller',
                    'factor':spec.total_count

                })
        else:
            res = self.search([], limit=1, order='id').id
        return res
