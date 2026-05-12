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

# Inicializar bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Cargar Cogs
async def load_cogs():
    """Cargar todos los cogs de la carpeta 'cogs'"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"[COGS] {filename} cargado")

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    print(f"Bot conectado como {bot.user}")
    print(f"Número de servidores: {len(bot.guilds)}")
    
    # Sincronizar comandos slash
    try:
        GUILD_ID = os.getenv('ID_GUILD')
        guild = discord.Object(id=int(GUILD_ID))
        await bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"[SYNC] {len(synced)} comandos slash sincronizados")
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
