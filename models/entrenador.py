from odoo import models, fields


# Entrenadores de la academia
class Entrenador(models.Model):
    _name = 'ebro_football_academy.entrenador'
    _description = 'Entrenador'
    # Campo que se ve como nombre del registro
    _rec_name = 'nombreEntrenador'

    nombreEntrenador = fields.Char(string='Nombre', required=True)
    apellidoEntrenador = fields.Char(string='Apellidos', required=True)
    especialidadEntrenador = fields.Char(string='Especialidad')
    telefonoEntrenador = fields.Char(string='Teléfono')
    emailEntrenador = fields.Char(string='Email')
    # Binary = guarda la foto
    fotoEntrenador = fields.Binary(string='Foto')

    # Uno a muchos: lista de entrenamientos del entrenador
    entrenamiento_ids = fields.One2many(
        'ebro_football_academy.entrenamiento',
        'entrenador_id',
        string='Entrenamientos'
    )

    # Lista de equipos del entrenador
    equipo_ids = fields.One2many(
        'ebro_football_academy.equipo',
        'entrenador_id',
        string='Equipos'
    )

    # Devuelve el último entrenamiento (el de fecha más nueva)
    def obtener_ultimo_entrenamiento(self):
        self.ensure_one()
        if self.entrenamiento_ids:
            return self.entrenamiento_ids.sorted('fechaEntrenamiento', reverse=True)[0]
        return self.env['ebro_football_academy.entrenamiento']
