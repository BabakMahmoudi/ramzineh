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
