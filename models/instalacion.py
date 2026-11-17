from odoo import models, fields


# Sitios donde se entrena (campos y gimnasio)
class Instalacion(models.Model):
    _name = 'ebro_football_academy.instalacion'
    _description = 'Instalación'
    _rec_name = 'nombreInstalacion'

    nombreInstalacion = fields.Char(
        string='Nombre',
        required=True
    )

    tipo = fields.Selection(
        [
            ('f11', 'Campo de fútbol 11'),
            ('f7', 'Campo de fútbol 7'),
            ('gimnasio', 'Gimnasio')
        ],
        string='Tipo de instalación',
        required=True
    )

    ubicacion = fields.Char(string='Ubicación')

    capacidad = fields.Integer(string='Capacidad')

    superficie = fields.Float(string='Superficie (m²)')

    descripcion = fields.Text(string='Descripción')

    # Binary = guarda la foto
    fotoInstalacion = fields.Binary(string='Foto')

    # Si se puede usar (por defecto sí)
    disponible = fields.Boolean(
        string='Disponible',
        default=True
    )
