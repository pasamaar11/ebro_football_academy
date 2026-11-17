from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Entrenamientos de la academia
class Entrenamiento(models.Model):
    _name = 'ebro_football_academy.entrenamiento'
    _description = 'Entrenamiento'

    nombreEntrenamiento = fields.Char(string='Nombre', required=True)
    fechaEntrenamiento = fields.Date(string='Fecha', required=True)
    duracionEntrenamiento = fields.Float(string='Duración (horas)')
    # Datetime = guarda día y hora. Por defecto pone el momento actual.
    # El calendario usa este campo.
    fechaHoraInicio = fields.Datetime(string='Fecha y hora de inicio',
                                    default=fields.Datetime.now)
    observaciones = fields.Text(string='Observaciones')

    # Entrenador del entrenamiento (obligatorio)
    entrenador_id = fields.Many2one(
        'ebro_football_academy.entrenador',
        string='Entrenador',
        required=True
    )

    # Jugadores que van (muchos a muchos)
    jugador_ids = fields.Many2many(
        'ebro_football_academy.jugador',
        'entrenamiento_jugador_rel',
        'entrenamiento_id',
        'jugador_id',
        string='Jugadores'
    )

    # Equipo y lugar (no son obligatorios)
    equipo_id = fields.Many2one(
        'ebro_football_academy.equipo',
        string='Equipo',
    )

    instalacion_id = fields.Many2one(
        'ebro_football_academy.instalacion',
        string='Instalación',
    )

    # @api.constrains = comprueba una regla al guardar
    # Regla: la duración tiene que ser mayor que 0
    @api.constrains('duracionEntrenamiento')
    def _comprobar_duracion(self):
        for entrenamiento in self:
            if entrenamiento.duracionEntrenamiento <= 0:
                raise ValidationError("La duración debe ser mayor que 0.")
