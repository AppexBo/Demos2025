{
	"name" : "Campo del Punto de venta siempre activado en facturacion",
	"version" : "17.0.0.0",
	'category': 'Point of Sale',
    'depends': [
        'point_of_sale',
    ],
	'author': 'Erick Denis Mercado Oudalova',
    'maintainer': 'AppexBo',
	'summary': 'Para que siempre se genere una factura en el pdv',
	"description": "Para que siempre se genere una factura en el pdv",
	"website" : "https://www.appexbo.com/",
	"auto_install": False,
	"installable": True,
	"license": "LGPL-3",
	"data": [
	],
	'assets': {
        'point_of_sale._assets_pos': [
            'invoice_all_time_pdv/static/**/*',
        ],
    },
}