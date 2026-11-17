{
    'name': 'Ebro Football Academy',
    'version': '19.0.1.0',
    'category': 'Sports',
    'summary': 'Gestión de jugadores, entrenadores y entrenamientos',
    'description': 'Módulo para gestionar una academia de fútbol.',
    'author': 'José Javier Pasamar Acón',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/jugador_views.xml',
        'views/entrenador_views.xml',
        'views/entrenamiento_views.xml',
        'views/equipo_views.xml',
        'views/instalacion_views.xml',
        'views/menus.xml',
    ],
    # datos de ejemplo
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    # application=True es que sale como aplicación en el menú principal
    'application': True,
}
