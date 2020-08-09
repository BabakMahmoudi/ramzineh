from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List, Dict
import logging
#from .models.parnian_translation_branch import ParnianTranslationBranch
if TYPE_CHECKING:
    from odoo.addons.base.models.res_partner import Partner
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.sale.models.sale import SaleOrder, SaleOrderLine
else:
    Partner = models.Model
    ProductTemplate = models.Model
    ProductProduct = models.Model
    SaleOrderLine = models.Model
    SaleOrder = models.Model


class ProductSpec():
    def __init__(self, product_type="", paper_type="", glue_type="", bobin_size="", number_of_rows=0, width=0, length=0, role_length=0, role_width=0):
        self.product_type = product_type
        self.paper_type = paper_type
        self.glue_type = glue_type
        self.bobin_size = bobin_size
        self.number_of_rows = number_of_rows
        self.width = width
        self.length = length
        self.role_length = role_length
        self.role_width = role_width

    def has_type(self):
        self.product_type != ""


class _ramzineh():

    def test(self):
        return False

    def product_templates(self, model: models.Model):
        return model.env['product.template']

    def find_product(self, model: models.Model, spec: ProductSpec):
        p = self.product_templates(model)
        return p.find_spec(spec)
        filter = []
        if spec.product_type:
            filter.append(('rmz_product_type', '=', spec.product_type))
        if spec.paper_type:
            filter.append(('rmz_paper_type', '=', spec.paper_type))
        if spec.bobin_size:
            filter.append(('rmz_paper_type', '=', spec.paper_type))
        return p.search(filter)

        return p.search([('rmz_product_type', '=', spec.product_type), ('rmz_paper_type', '=', spec.paper_type)])
        return p.search([('rmz_product_type', '=', spec.product_type), ('rmz_paper_type', '=', spec.paper_type)])


Ramzineh = _ramzineh()
