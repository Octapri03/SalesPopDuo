# -*- coding: utf-8 -*-

import random
from odoo import models, fields, api
from datetime import timedelta, datetime


class user(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'salespop users'

    #name = fields.Char(compute = "default_name_user", readonly = False)
    # #user_name = fields.Char()
    #mail = fields.Char(readonly = False, domain = [('mail','ilike','a')])
    password = fields.Char(readonly = False, default="1234", required = True)
    num_tel = fields.Char(readonly = False, default= "67654687")
    on_sale = fields.One2many('salespop.product', 'seller')
    valoracion = fields.One2many('salespop.valoracion', 'valoracion_usuario')

    is_user_pop = fields.Boolean(default = False)

class product(models.Model):
    _name = 'salespop.product'
    _description = 'salespop products'

    name = fields.Char()
    price = fields.Integer()
    categoria = fields.Many2one('salespop.category')
    description = fields.Char(required=False)
    ubication = fields.Char()
    publication_date = fields.Datetime(readonly=True, default=fields.Datetime.now)
    seller = fields.Many2one('res.partner', ondelete = "cascade")
    foto = fields.One2many('salespop.foto', 'product')

    default_image = fields.Image(compute='_get_img')

    def _get_img(self):
        for i in self:
            if i.foto != None:
                i.default_image = i.foto.photo
            else:
                i.default_image = i.template.image

    def _many2manyFoto(self):
        for b in self:
            b.foto = self.env['salespop.foto'].search([('product.id','=',b.id)]).id

    @api.onchange('price')
    def _default_name_product(self):                                             
            for f in self:
                if not f.name:
                    f.name = "product"+(str(random.randint(0, 99999)))
                if not f.price:
                    f.price = 77
                    

class category(models.Model):
    _name = 'salespop.category'
    _description = 'salespop categories'

    name = fields.Selection([('MOTOR', "Motor"), ('INMOBILIARIA', "Inmobiliaria"), ('JUEGOS', "Juegos"), ('INFORMATICA', "Informatica"), ('TELEFONIA', "Telefonia"), ('MODA', "Moda"), ('DEPORTES', "Deportes")], default = 'MOTOR')
    articulo_categoria = fields.One2many('salespop.product', 'categoria')

class valoracion(models.Model):
    _name = 'salespop.valoracion'
    _description = 'salespop valoracion'

    name = fields.Char()
    puntuacion = fields.Selection([('1', "MEDIOCRE"), ('2', "MALO"), ('3', "REGULAR"), ('4', "BUENO"), ('5', "MUY BUENO")], default = '1')
    valoracion_usuario = fields.Many2one('salespop.user', 'valoracion')

class foto(models.Model):
    _name = 'salespop.foto'
    _description = 'salespop foto'

    name = fields.Char()
    photo = fields.Image(size_width=200, max_height = 200, required = True)
    url_imagen = fields.Char()
    product = fields.Many2one('salespop.product')


class empleado(models.Model):
    _name = 'salespop.empleado'
    _description = 'salespop empleado'

    name = fields.Char()
    mail = fields.Char()
    password = fields.Char()


class product_wizard(models.TransientModel):
    _name = 'salespop.product_wizard'

    name = fields.Char()
    price = fields.Integer()
    categoria = fields.Many2one('salespop.category')
    description = fields.Char()
    ubication = fields.Char()
    publication_date = fields.Datetime(readonly=True, default=fields.Datetime.now)
    seller = fields.Many2one('res.partner', ondelete = "cascade")
    foto = fields.Many2many('salespop.foto')

    default_image = fields.Image(compute='_get_img')

    def launch(self):
        self.env['salespop.product'].create({'name':self.name, 'price':self.price, 'description':self.description, 'ubication':self.ubication})

        return {}


    @api.onchange('price')
    def _default_name_product(self):                                             
            for f in self:
                if not f.name:
                    f.name = "product"+(str(random.randint(0, 99999)))
                if not f.price:
                    f.price = 0