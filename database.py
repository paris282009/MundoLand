"""
Sistema de base de datos SQLite para el bot
Manejo centralizado de datos
"""

import sqlite3
import json
import os
from datetime import datetime

DB_NAME = 'bot_data.db'

def init_database():
    """Inicializar la base de datos con todas las tablas"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabla de servidores agregados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers_directory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        server_name TEXT NOT NULL,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(guild_id, owner_id, ip, port)
    )
    ''')
    
    # Tabla de redes sociales (TikTok, YouTube)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS social_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        platform TEXT NOT NULL,
        username TEXT NOT NULL,
        url TEXT NOT NULL,
        added_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(guild_id, platform)
    )
    ''')
    
    # Tabla de botones agregados a mensajes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message_buttons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        button_label TEXT NOT NULL,
        button_url TEXT NOT NULL,
        added_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de encuestas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        votes TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("[DATABASE] Base de datos inicializada")

# ============== SERVIDORES ==============

def add_server(guild_id, owner_id, server_name, ip, port, description=""):
    """Agregar un servidor al directorio"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO servers_directory 
        (guild_id, owner_id, server_name, ip, port, description) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (guild_id, owner_id, server_name, ip, port, description))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_servers(guild_id):
    """Obtener todos los servidores de un guild"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM servers_directory WHERE guild_id = ?', (guild_id,))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_user_servers(guild_id, owner_id):
    """Obtener servidores del usuario"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM servers_directory WHERE guild_id = ? AND owner_id = ?',
        (guild_id, owner_id)
    )
    servers = cursor.fetchall()
    conn.close()
    return servers

def edit_server(server_id, owner_id, **kwargs):
    """Editar un servidor (solo el dueño puede)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Verificar que es el dueño
    cursor.execute('SELECT owner_id FROM servers_directory WHERE id = ?', (server_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != owner_id:
        conn.close()
        return False
    
    # Construir query dinámico
    fields = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [server_id]
    
    cursor.execute(f'UPDATE servers_directory SET {fields} WHERE id = ?', values)
    conn.commit()
    conn.close()
    return True

def delete_server(server_id, owner_id):
    """Eliminar un servidor"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT owner_id FROM servers_directory WHERE id = ?', (server_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != owner_id:
        conn.close()
        return False
    
    cursor.execute('DELETE FROM servers_directory WHERE id = ?', (server_id,))
    conn.commit()
    conn.close()
    return True

# ============== REDES SOCIALES ==============

def add_social_link(guild_id, platform, username, url, added_by):
    """Agregar enlace de red social"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO social_links (guild_id, platform, username, url, added_by)
        VALUES (?, ?, ?, ?, ?)
        ''', (guild_id, platform, username, url, added_by))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_social_link(guild_id, platform):
    """Obtener enlace de red social"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM social_links WHERE guild_id = ? AND platform = ?',
        (guild_id, platform)
    )
    result = cursor.fetchone()
    conn.close()
    return result

# ============== BOTONES ==============

def add_button_to_message(message_id, channel_id, guild_id, button_label, button_url, added_by):
    """Agregar botón a un mensaje"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO message_buttons 
    (message_id, channel_id, guild_id, button_label, button_url, added_by)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (message_id, channel_id, guild_id, button_label, button_url, added_by))
    conn.commit()
    conn.close()
    return True

def get_message_buttons(message_id):
    """Obtener botones de un mensaje"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT button_label, button_url FROM message_buttons WHERE message_id = ?', (message_id,))
    buttons = cursor.fetchall()
    conn.close()
    return buttons

# Inicializar DB al importar
if not os.path.exists(DB_NAME):
    init_database()
