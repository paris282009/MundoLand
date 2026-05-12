"""
Configuración centralizada del bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot
TOKEN = os.getenv('TOKEN')
PREFIX = '/'

# Colores para embeds
COLORS = {
    'success': 0x00ff00,
    'error': 0xff0000,
    'info': 0x0000ff,
    'warning': 0xffff00,
    'purple': 0x9900ff,
}

# Comandos restringidos (solo owner o permisos especiales)
ADMIN_COMMANDS = [
    'say', 'say_embed', 'limpiar', 
    'tiktok_agregar', 'youtube_agregar', 
    'add_boton'
]

# Permisos por defecto
DEFAULT_PERMISSIONS = {
    'encuesta': 'everyone',
    'datos': 'everyone',
    'estado': 'everyone',
    'avatar': 'everyone',
    'userinfo': 'everyone',
    'stats': 'everyone',
    'serveradd': 'everyone',
    'serveredit': 'user_only',
    'servidores': 'everyone',
    'tienda': 'everyone',
}
