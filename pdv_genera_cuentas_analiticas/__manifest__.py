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
	'summary': 'Cuando se genere la factura se le asigna la cuenta analitica que esta en la configuracion que tien el punto de venta',
	"description": "Cuando se genere la factura se le asigna la cuenta analitica que esta en la configuracion que tien el punto de venta",
	"website" : "https://www.appexbo.com/",
	"auto_install": False,
	"installable": True,
	'application': True,
	"license": "LGPL-3",
	"data": [
		'views/res_config_settings_pdv/settings.xml'
	],
}