import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

"""
Script para sincronizar comandos manualmente si Discord no los actualiza.
Útil cuando cambias muchos comandos a la vez.

Uso: python sync_commands.py
"""

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production').lower()
DEV_GUILD_ID = os.getenv('DEV_GUILD_ID')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    """Sincronizar comandos una vez que el bot está listo"""
    print(f"\nBot conectado como {bot.user}")
    
    try:
        if ENVIRONMENT == 'development' and DEV_GUILD_ID:
            dev_guild = discord.Object(id=int(DEV_GUILD_ID))
            synced = await bot.tree.sync(guild=dev_guild)
            print(f"✅ {len(synced)} comandos sincronizados en servidor de desarrollo")
        else:
            synced = await bot.tree.sync()
            print(f"✅ {len(synced)} comandos globales sincronizados")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Desconectar después de sincronizar
    await bot.close()

async def main():
    async with bot:
        # No cargar cogs, solo sincronizar
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
