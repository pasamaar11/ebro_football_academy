from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Jugadores de la academia
class Jugador(models.Model):
    _name = 'ebro_football_academy.jugador'
    _description = 'Jugador'

    nombreJugador = fields.Char(string='Nombre', required=True, help='Nombre del jugador')
    apellidoJugador = fields.Char(string='Apellido', required=True, help='Apellido del jugador')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    # La edad se calcula sola (mira _calcular_edad)
    edad = fields.Integer(string='Edad', compute='_calcular_edad')
    # Binary = sirve para guardar una imagen (la foto)
    fotoJugador = fields.Binary(string='Foto')

    # Selection = lista con opciones fijas
    posicionJugador = fields.Selection([
        ('portero', 'Portero'),
        ('defensa', 'Defensa'),
        ('centrocampista', 'Centrocampista'),
        ('delantero', 'Delantero')
    ], string='Posición', required=True, help='Posición del jugador')

    categoriaJugador = fields.Selection([
        ('juvenil', 'Juvenil'),
        ('cadete', 'Cadete'),
        ('infantil', 'Infantil'),
        ('alevin', 'Alevín'),
        ('benjamin', 'Benjamín')
    ], string='Categoría', required=True, help='Categoría del jugador')

    # Muchos a muchos: un jugador va a muchos entrenamientos
    # y a un entrenamiento van muchos jugadores
    entrenamiento_ids = fields.Many2many(
        comodel_name='ebro_football_academy.entrenamiento',
        relation='entrenamiento_jugador_rel',
        column1='jugador_id',
        column2='entrenamiento_id',
        string='Entrenamientos'
    )

    # Muchos a uno: un jugador tiene un solo equipo
    equipo_id = fields.Many2one(
        'ebro_football_academy.equipo',
        string='Equipo'
    )

    # Calcula la edad con la fecha de nacimiento.
    # @api.depends = se vuelve a calcular cuando cambia la fecha
    @api.depends('fecha_nacimiento')
    def _calcular_edad(self):
        hoy = fields.Date.today()
        for jugador in self:
            if jugador.fecha_nacimiento:
                # Error si la fecha de nacimiento es futura
                if jugador.fecha_nacimiento > hoy:
                    raise ValidationError(
                        "La fecha de nacimiento no puede ser futura.")
                # Años de diferencia, y resta 1 si aún no ha cumplido años
                jugador.edad = hoy.year - jugador.fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (jugador.fecha_nacimiento.month, jugador.fecha_nacimiento.day))
            else:
                jugador.edad = 0

    # Al elegir equipo, pone su categoría y avisa si está lleno
    @api.onchange('equipo_id')
    def _al_cambiar_equipo(self):
        if self.equipo_id:
            self.categoriaJugador = self.equipo_id.categoriaEquipo
            if self.equipo_id.plazas_libres <= 0:
                return {'warning': {
                    'title': 'Equipo completo',
                    'message': 'Este equipo ya no tiene plazas libres.'}}
        else:
            self.categoriaJugador = False
