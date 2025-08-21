# -*- coding: utf-8 -*-
{
    'name': "POS Multi sesiones",
    'summary': """Multi sesiones de usuario""",
    'description': """Agrege una session adicional para personas que deceen compartir el mismo usuario, con distinto contacto. Las sessiones pueden estar guardadas en el directorio local del navegador, si se decea que no guarde las sesiones iniciadas, restrinja desde la configuracion del navegador del usuario.""",
    'author': "Luis Fernando Hinojosa Flores",
    'category': 'Sales/CRM',
    'version': '0.2',
    'depends': ['base','web','multi_user_sessions', 'point_of_sale'],
    'data' : [],
    'license': 'LGPL-3',
}
