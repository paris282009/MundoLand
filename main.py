import os
import webserver
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# 1. Cargar variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Usamos un valor por defecto (0) por si el .env falla momentáneamente
GUILD_ID_STR = os.getenv("GUILD_ID")
GUILD_ID = int(GUILD_ID_STR) if GUILD_ID_STR else 0

# 2. Configurar intents
intents = discord.Intents.default()
intents.members = True          
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Arrancar servidor de hosting (Keep Alive)
webserver.keep_alive()

# --- EVENTOS ---
@bot.event
async def on_ready():
    print(f"{bot.user} está conectado ✅")
    try:
        if GUILD_ID != 0:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            print(f"Comandos sincronizados: {len(synced)}")
        else:
            print("Error: GUILD_ID no encontrado en el archivo .env")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# --- COMANDOS /SLASH ---

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="tiktok", description="Link del TikTok oficial")
async def tiktok(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro TikTok: https://www.tiktok.com/@mundo.land5")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="youtube", description="Link del canal de YouTube")
async def youtube(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro YouTube: https://youtube.com/@elparis1")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="tienda", description="Link de la tienda oficial")
async def tienda(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestra tienda: https://aethermc-webshop.tebex.io/AetherMC-tienda")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="estado", description="Estado del servidor de Discord")
async def estado(interaction: discord.Interaction):
    try:
        response = requests.get("https://discordstatus.com/api/v2/status.json").json()
        status = response["status"]["description"]
        traducciones = {
            "All Systems Operational": "🟢 (Servidor abierto)",
            "Partial System Outage": "🟡 (Servidor inestable)",
            "Major System Outage": "🔴 (Servidor cerrado)"
        }
        estado_es = traducciones.get(status, "⚠ (Estado desconocido)")
        await interaction.response.send_message(estado_es)
    except:
        await interaction.response.send_message("⚠ (Error al obtener el estado)")

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="ip", description="IP del servidor de Minecraft")
async def ip(interaction: discord.Interaction):
    embed = discord.Embed(
        title="AetherMC",
        description="*IP:* `aethermc.space`\n📌 Versión: 1.18 x +1.21 ",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="say", description="Envía un mensaje a través del bot")
async def say(interaction: discord.Interaction, mensaje: str):
    if interaction.user.guild_permissions.administrator:
        await interaction.channel.send(mensaje)
        await interaction.response.send_message("Mensaje enviado.", ephemeral=True)
    else:
        await interaction.response.send_message("No tienes permisos.", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="decir_embed", description="Envía un mensaje elegante (Embed)")
async def decir_embed(interaction: discord.Interaction, titulo: str, descripcion: str, color_hex: str = "FFD700"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("No tienes permisos.", ephemeral=True)
    try:
        color_int = int(color_hex.replace("#", ""), 16)
        embed = discord.Embed(title=titulo, description=descripcion.replace("\\n", "\n"), color=color_int)
        embed.set_footer(text=f"Enviado por: {interaction.user.name}")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed enviado.", ephemeral=True)
    except ValueError:
        await interaction.response.send_message("Error: Formato Hex inválido.", ephemeral=True)

# 4. Ejecución del Bot
bot.run(DISCORD_TOKEN)