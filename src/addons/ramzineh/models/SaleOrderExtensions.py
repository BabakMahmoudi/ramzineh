from ..ramzineh import SaleOrder, SaleOrderLine

class SaleOrderExtensions(SaleOrder):
    _inherit = "sale.order"

class SaleOrderLineExtensions(SaleOrderLine):
    _inherit = "sale.order.line"