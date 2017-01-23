# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    def onchange_calculate_volume(self, cr, uid, ids, length, high, width, dimensional_uom_id, context=None):
        v = {}
        if not length or not high or not width or not dimensional_uom_id:
            volume = False
        else:
            dimensional_uom = self.pool.get('product.uom').browse(cr, uid, dimensional_uom_id, context=context)
            length_m = self.get_measure_in_meters(length, dimensional_uom)
            high_m = self.get_measure_in_meters(high, dimensional_uom)
            width_m = self.get_measure_in_meters(width, dimensional_uom)
            if not length_m or not high_m or not width_m:
                volume = False
            else:
                volume = length_m * high_m * width_m / 1000000000
        v['volume'] = volume
        return {'value': v}



            
    def get_measure_in_meters(self, measure, dimensional_uom):
        if not dimensional_uom:
            return None
        
        measure = float(measure)    
        if dimensional_uom.name == 'mm':
            return measure
        elif dimensional_uom.name == 'cm':
            return measure * 10
        elif dimensional_uom.name == 'm':
            return measure / 1000
        else:
            return None
    
    _columns = {
        'length': fields.float('Largo (mm)'), # Largo
        'high': fields.float('Espesor (mm)'), # Alto
        'width': fields.float('Ancho (mm)'), # Ancho
        'dimensional_uom': fields.many2one('product.uom', 'UdM dimensional',
                                           domain="[('category_id.name', '=', 'Length / Distance')]",
                                           help='Unidad de Medida Dimensional para Largo, Alto y Ancho'),
        'uv_id': fields.many2one('product.uv', 'UV'),
        'area': fields.float('Area (m2)'),
        'lt': fields.integer('LT (%)'),
        'hard_coating': fields.integer('Hard Coating'),
        'cant_pallet': fields.integer('Cant/Pallet'),
        'peso_pallet': fields.integer('Peso/Pallet (kg)'),
        'color_id': fields.many2one('product.color', 'Color'),
        'familia_id': fields.many2one('product.familia', 'Familia'),

    }

product_product()



class product_color(osv.osv):

    _name = 'product.color'
    _description = 'Colores'

    _columns = {    
   'name': fields.char('Nombre', required=True)
       }

class product_uv(osv.osv):

    _name = 'product.uv'
    _description = 'UV'
    
    _columns = {    
   'name': fields.integer('UV', required=True)
       }

class product_familia(osv.osv):

    _name = 'product.familia'
    _description = 'Familia'
    
    _columns = {    
   'name': fields.char('Familia', required=True)
       }



