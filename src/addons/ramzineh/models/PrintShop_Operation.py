
from ..ramzineh import api,models,fields,Ramzineh,StockMove,ProductProduct
class PrintShopOpertaion(models.Model):
    _name =Ramzineh.constants.ps_operation_model_name
    name = fields.Char()
    slit_input_product_id = fields.Many2one("product.product", string="Input")
    slit_widths = fields.Char(string="Slit Width")


    def action_execute(self):
        print("executing")
        moves = self.env["stock.move"]
        product_id:ProductProduct = self.env["product.product"].search([])[0]
        location_id = self.env["stock.location"].search([('name','=','Stock')])[0] 
        dest_location_id = self.env["stock.location"].search([('name','=','Pre-Production')])[0]  
        move:StockMove = moves.create({
            'name':'test3',
            'product_id':product_id.id,
            'product_uom':product_id.uom_id.id,
            'location_id':location_id.id,
            'location_dest_id':dest_location_id.id,
            'product_uom_qty':2.0,



        })
        print(move)
        move._action_done()










    



