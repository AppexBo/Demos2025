# -*- coding: utf-8 -*-

from odoo import api, models, fields,SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.http import request


import logging
_logger = logging.getLogger(__name__)

USER_ID = 2

class ResUsers(models.Model):
    _inherit = ['res.users']

    
    
    
    # enable_multi_user = fields.Boolean(
    #     string='Multi usuario',
    #     help='Usuario usado para ser compartido por mas de una persona en el login.'
    # )
    
    # reference_user = fields.Boolean(
    #     string='Usuario interno',
    #     help='Usuario interno de referencia para multi usuarios.'
    # )
    
    
    # muip = fields.Char(
    #     string='IP computadora',
    #     help='Dirección de localhost, que apunta a la propia computadora.',
    #     default='n/a',
    #     copy=False
    # )

    
    mu_password = fields.Char(
        string='Contraseña (MU)',
        help='Contraseña multi usuario',
        copy=False
    )
    

    # def gmuip(self):
    #     MUIP = request.httprequest.headers.get('X-Forwarded-For', request.httprequest.remote_addr)
    #     _logger.info(f"IP: {MUIP}")
    #     return MUIP
    
    # @api.constrains('muip')
    # def _check_muip(self):
    #     for record in self:
    #         if not record.muip:
    #             record.write({'muip' : 'n/a'})
    #         if record.reference_user and record.muip and record.muip != 'n/a':
    #             res_muser_ids = record.search([('reference_user','=',True),('active','=',False) ,('id','!=',record.id),('muip','=',record.muip)])
    #             if len(res_muser_ids)>0:
    #                 raise UserError(f"La IP {record.muip}, esta en configurado para otro usuario.")
                
                
    # def muid(self, MUIP = False):
    #     return self.sudo().search([('reference_user','=',True),('muip','=',MUIP),('active','=',False)], limit=1)
    

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        switch = False
        user_id = False
        if USER_ID:
            with cls.pool.cursor() as cr:
                env = api.Environment(cr, USER_ID, {})
                if env.user.has_group('base.group_system'):
                    RES_USER : ResUsers = env['res.users']
                    user_id = RES_USER.search([('login','=',login),('mu_password','=',password), ('active','=',False)], limit=1)
                    admin_id = RES_USER.browse(USER_ID)
                    _logger.info(f"USUARIO: {user_id}")
                    if user_id and admin_id:
                        switch, login, password = True, admin_id.login, admin_id.mu_password
                    else:
                        _logger.info(f"Usuario: {login}, no es un multi usuario")
        
        UID =  super().authenticate(db, login, password, user_agent_env)
        
        if switch and user_id:
            return user_id.id
        return UID