from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List, Dict
import logging
#from .models.parnian_translation_branch import ParnianTranslationBranch
if TYPE_CHECKING:
    from odoo.addons.base.models.res_partner import Partner
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.sale.models.sale import SaleOrder, SaleOrderLine
    from .models.ProductExtensions import ProductTemplateExtensions
else:
    Partner = models.Model
    ProductTemplate = models.Model
    ProductProduct = models.Model
    SaleOrderLine = models.Model
    SaleOrder = models.Model
    ProductTemplateExtensions = models.Model


class Constants():
    
    product_types= {
        'J':'jambo',
        'R':'role',
        'L':'label',
        'M': 'sayer'
    }
    
    paper_types = {
        'SDF':'sadafi',
        'KGH': 'kaghazi',
        'MTK': 'metalize kaghazi',
        'LSH': 'laieh shavandeh',
        'GCH': 'gachi',
        'VOD': 'void',
        'TMP': 'tamper',
        'HRT': 'hararati',
        'TRN': 'transparent',
        'MTP': 'metalize pp',
        'AML': 'amval',
        'MSC': 'saier',
    }
    
    glue_types = {
        'A': 'acronal',
        'H': 'hot melt',
        'M': 'saier',
    }
    
    bobin_size = {
        'B': 'bozorg',
        'K': 'koochak',
        'M': 'saier',
    }

    


class ProductSpec():
    def __init__(self, product_type="", paper_type="", glue_type="", 
        bobin_size="", number_of_rows=0, total_count=0, width=0, length=0, 
        role_length=0, role_width=0, printed_label=""):
        self.product_type = product_type
        self.paper_type = paper_type
        self.glue_type = glue_type
        self.bobin_size = bobin_size
        self.number_of_rows = number_of_rows
        self.total_count = total_count
        self.width = width
        self.length = length
        self.role_length = role_length
        self.role_width = role_width
        self.printed_label = printed_label

    def is_label(self):
        return self.product_type=='J' or self.product_type=='L' or self.product_type=='R'
    def has_type(self):
        self.product_type != ""

    def get_code(self):
        result = ''
        result = '{}-{}-{}-{}x{}-{}-{}x{}-{}x{} {}'.format(self.product_type,self.paper_type,
        self.glue_type, self.role_width,self.role_length,
        self.bobin_size,self.width, self.length,self.number_of_rows, self.total_count, 
        self.printed_label )

        return result


class _ramzineh():

    constants = Constants()

    def test(self):
        return False
    def product_templates(self, model: models.Model)->ProductTemplateExtensions:
        return model.env['product.template']

    def find_product(self, model: models.Model, spec: ProductSpec, exact=True):
        p = self.product_templates(model)
        return p.find_spec(spec, exact)


Ramzineh = _ramzineh()
