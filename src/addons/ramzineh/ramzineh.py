from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List, Dict
import logging
#from .models.parnian_translation_branch import ParnianTranslationBranch
if TYPE_CHECKING:
    from odoo.addons.base.models.res_partner import Partner
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.sale.models.sale import SaleOrder, SaleOrderLine
    from odoo.addons.mrp.models.mrp_production import MrpProduction
    from odoo.addons.stock.models.stock_move import StockMove
    from odoo.addons.stock.models.stock_move_line import StockMoveLine
    from odoo.addons.uom.models.uom_uom import UoM
    from .models.ProductExtensions import ProductTemplateExtensions
    from .models.UnitOfMeasureExtensions import UoMExtensions
else:
    Partner = models.Model
    ProductTemplate = models.Model
    ProductProduct = models.Model
    SaleOrderLine = models.Model
    SaleOrder = models.Model
    ProductTemplateExtensions = models.Model
    MrpProduction = models.Model
    StockMove = models.Model
    StockMoveLine = models.Model
    UoM = models.Model
    UoMExtensions = models.Model


class Constants():
    use_code_for_name = True
    ps_operation_model_name ="ramzineh.ps.operation"
    product_types = {
        'J': 'جامبو',
        'R': 'رول',
        'L': 'لیبل',
        'M': 'متفرقه'
    }

    paper_types = {
        'SDF': 'صدفی',
        'KGH': 'کاغذی',
        'MTK': 'متالایز کاغذی',
        'LSH': 'لایه شونده',
        'GCH': 'گچی',
        'VOD': 'ووید',
        'TMP': 'تمپر',
        'HRT': 'حرارتی',
        'TRN': 'ترنسپرنت',
        'MTP': 'متالایز پ پ',
        'AML': 'اموال',
        'ASL' :'اصلات',
        'SCR' :'اسکرچ',
        'MSC': 'متفرقه',
    }

    glue_types = {
        'A': 'آکرونال',
        'H': 'هات ملت',
        'M': 'متفرقه',
    }

    bobin_size = {
        'B': 'بوبین بزرگ',
        'K': 'بوبین کوچک',
        'M': 'بوبین متفرقه',
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

    def is_paper(self):
        """
            True if it is actually a paper product/raw material, comapred to other products that
            can be stored such as glues, painting colors etc. Paper products
            will obey our naming/coding convention.
        """
        return self.product_type == 'J' or self.product_type == 'L' or self.product_type == 'R'
    
    def is_label(self):
        """
            True if it is a die-cutted label. Label needs the cutting dimensions in their specifications.
        """
        return self.product_type=='L'

    def has_type(self):
        self.product_type != ""

    def get_code(self):
        """
            Returns a code/name for this product spec.
        """
        result = ''
        if self.is_paper():
            result = '{}-{}-{}-{}x{}'.format(self.product_type, self.paper_type,
                                             self.glue_type, self.role_width, self.role_length)
        if self.product_type == 'L':
            result += '-{}-{}x{}-{}x{}'.format(self.bobin_size, self.width,
                                               self.length, self.number_of_rows, self.total_count)
            if (self.printed_label and self.printed_label != ''):
                result += '-"{}"'.format(self.printed_label)
        return result
    
    def get_unit_name(self):
        res = False
        if self.is_paper() and self.total_count>0:
            res = 'X{}'.format(self.total_count)
        return res

        

    def get_description(self):
        """
            Returns a descriptive text for this product spec.
        """
        result = ''
        if self.is_paper():
            result = '{} {} {} ({} در {})'.format(
                Constants.product_types.get(self.product_type, ''),
                Constants.paper_types.get(self.paper_type, ''),
                Constants.glue_types.get(self.glue_type, ''),
                self.role_width, self.role_length)
            if self.is_label():
                result = '{} {} {} در {}، {}، {}، {} ردیفه، {} عددی'.format(
                Constants.product_types.get(self.product_type, ''),
                Constants.paper_types.get(self.paper_type, ''),
                self.width, self.length,
                Constants.glue_types.get(self.glue_type, ''),
                Constants.bobin_size.get(self.bobin_size, ''),
                self.number_of_rows, self.total_count
                )
                # result = '{} {} {}'.format(
                #     Constants.product_types.get(self.product_type, ''),
                #     Constants.paper_types.get(self.paper_type, ''),
                #     Constants.glue_types.get(self.glue_type, ''))
                # result += ' {} سایز:{} در {} (م.م)   {} ردیفه {} عددی'.format(
                #     Constants.bobin_size.get(self.bobin_size, ''),
                #     self.width, self.length, self.number_of_rows, self.total_count
                # )

        return result
    
    def error(self):
        result =''
        if self.is_paper():
            if self.role_length<1:
                return 'طول رول'
            if self.role_width<1:
                return 'عرض رول'
            if self.paper_type==False:
                return 'نوع کاغذ'
            if self.glue_type==False:
                return 'نوع چسب'
            if self.is_label():
                if self.length<5:
                    return 'طول لیبل'
                if self.width<5:
                    return 'عرض لیبل'
                if self.number_of_rows<1:
                    return 'تعداد ردیف'
                if self.total_count<100:
                    return 'تعداد'
                if self.bobin_size==False:
                    return 'بوبین'

        
            
        return result

    def warn(self):
        return ''



class _ramzineh():

    constants = Constants()

    def test(self):
        return False

    def product_templates(self, model: models.Model) -> ProductTemplateExtensions:
        return model.env['product.template']

    def find_product(self, model: models.Model, spec: ProductSpec, exact=True):
        p = self.product_templates(model)
        return p.find_spec(spec, exact)


Ramzineh = _ramzineh()
