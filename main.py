import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import threading
from flask import Flask

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '/'

# Determinar modo: desarrollo (local) o producción (Render)
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production').lower()
DEV_GUILD_ID = os.getenv('DEV_GUILD_ID')  # Solo usado en desarrollo

# Inicializar bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Cargar Cogs
async def load_cogs():
    """Cargar todos los cogs de la carpeta 'cogs'"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"[COGS] {filename} cargado correctamente")
            except Exception as e:
                print(f"[ERROR] Error cargando {filename}: {e}")

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    print(f"\n{'='*50}")
    print(f"Bot conectado como {bot.user}")
    print(f"Número de servidores: {len(bot.guilds)}")
    print(f"Entorno: {ENVIRONMENT}")
    print(f"{'='*50}\n")
    
    # Sincronizar comandos slash
    try:
        if ENVIRONMENT == 'development' and DEV_GUILD_ID:
            # Modo DESARROLLO: sincronizar solo en servidor específico (instantáneo)
            dev_guild = discord.Object(id=int(DEV_GUILD_ID))
            synced = await bot.tree.sync(guild=dev_guild)
            print(f"[SYNC] {len(synced)} comandos sincronizados en servidor de desarrollo")
            print(f"[INFO] Servidor de desarrollo ID: {DEV_GUILD_ID}")
        else:
            # Modo PRODUCCIÓN: sincronizar globalmente (para múltiples servidores)
            synced = await bot.tree.sync()
            print(f"[SYNC] {len(synced)} comandos globales sincronizados")
            print(f"[INFO] Los comandos pueden tardar hasta 1 hora en aparecer en Discord")
            print(f"[INFO] El bot ahora funciona en múltiples servidores")
    except Exception as e:
        print(f"[ERROR] Error sincronizando comandos: {e}")
    
    # Cambiar estado del bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="/ayuda para ver comandos"
        )
    )

@bot.event
async def on_guild_join(guild):
    """Cuando el bot se une a un nuevo servidor"""
    print(f"Bot añadido a {guild.name} (ID: {guild.id})")

# Webserver para evitar que se apague
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot activo', 200

def run_webserver():
    """Ejecutar webserver en background"""
    app.run(host='0.0.0.0', port=5000)

# Iniciar bot
async def main():
    """Función principal"""
    async with bot:
        # Iniciar webserver en thread separado
        webserver_thread = threading.Thread(target=run_webserver, daemon=True)
        webserver_thread.start()
        print("[WEBSERVER] Iniciado en puerto 5000")
        
        # Cargar cogs
        await load_cogs()
        
        # Conectar bot
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
