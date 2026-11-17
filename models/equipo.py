from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Equipos de la academia
class Equipo(models.Model):
    _name = 'ebro_football_academy.equipo'
    _description = 'Equipo'
    _rec_name = 'nombreEquipo'

    nombreEquipo = fields.Char(string='Nombre del Equipo', required=True)
    categoriaEquipo = fields.Selection([
        ('juvenil', 'Juvenil'),
        ('cadete', 'Cadete'),
        ('infantil', 'Infantil'),
        ('alevin', 'Alevín'),
        ('benjamin', 'Benjamín')
    ], string='Categoría del Equipo', required=True)

    temporada = fields.Selection([
        ('2022-2023', '2022-2023'),
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027')
    ], string='Temporada', required=True)

    # Máximo de jugadores que caben en el equipo
    maxJugadores = fields.Integer(string='Máximo de Jugadores', required=True)
    activo = fields.Boolean(string='Activo', default=True)

    # Campos calculados: nº de jugadores y plazas libres
    # (store=True = se guardan en la base de datos)
    cantidad_jugadores = fields.Integer(string='Nº jugadores', compute='_calcular_plazas', store=True)
    plazas_libres = fields.Integer(string='Plazas libres', compute='_calcular_plazas', store=True)

    # Relaciones: jugadores, entrenador y entrenamientos del equipo
    jugador_ids = fields.One2many(
        'ebro_football_academy.jugador',
        'equipo_id',
        string='Jugadores'
    )

    entrenador_id = fields.Many2one(
        'ebro_football_academy.entrenador',
        string='Entrenador'
    )

    entrenamiento_ids = fields.One2many(
        'ebro_football_academy.entrenamiento',
        'equipo_id',
        string='Entrenamientos'
    )

    # Se recalcula si cambian los jugadores o el máximo
    @api.depends('jugador_ids', 'maxJugadores')
    def _calcular_plazas(self):
        for equipo in self:
            equipo.cantidad_jugadores = len(equipo.jugador_ids)
            equipo.plazas_libres = equipo.maxJugadores - len(equipo.jugador_ids)

    # Regla: no puede haber más jugadores que el máximo
    @api.constrains('jugador_ids', 'maxJugadores')
    def _comprobar_maximo_jugadores(self):
        for equipo in self:
            if len(equipo.jugador_ids) > equipo.maxJugadores:
                raise ValidationError("El equipo supera el máximo de jugadores permitido.")

    # Sube el máximo de jugadores
    def ampliar_plazas(self, cantidad):
        """Aumenta el máximo de jugadores del equipo"""
        for equipo in self:
            equipo.maxJugadores += cantidad

    # Devuelve el jugador más mayor del equipo
    #@api.returns('ebro_football_academy.jugador')
    def obtener_jugador_mayor(self):
        self.ensure_one()
        if self.jugador_ids:
            return self.jugador_ids.sorted('edad', reverse=True)[0]
        return self.env['ebro_football_academy.jugador']