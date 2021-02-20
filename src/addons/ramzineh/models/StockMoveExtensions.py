

from ..ramzineh import api,models,fields,Ramzineh, StockMove,StockMoveLine

class StockMoveExtensions(StockMove):
    _inherit = "stock.move"

class StockMoveLineExtensions(StockMoveLine):
    _inherit = "stock.move.line"
