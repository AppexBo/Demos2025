{
	"name" : "PDV genera cuenta analiticas",
	"version" : "17.0.0.0",
	"category" : "Point of Sale",
	"depends" : [
		'base',
		'point_of_sale',
		'account',
		'analytic',
	],
	"author": "AppexBo",
	'summary': 'Cuando se genere una venta o devolucion de algun producto en el punto de venta este se asignara y generara su cuenta analitica correspondiente de entrada o salida segun la sucursal',
	"description": "Cuando se genere una venta o devolucion de algun producto en el punto de venta este se asignara y generara su cuenta analitica correspondiente de entrada o salida segun la sucursal",
	"website" : "https://www.appexbo.com/",
	"auto_install": False,
	"installable": True,
	'application': True,
	"license": "LGPL-3",
	"data": [
        #'views/pos_order_line_form.xml'
		#'views/res_config_settings_pdv/settings.xml'
	],
}