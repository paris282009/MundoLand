import os
import discord
import requests
import threading
from flask import Flask
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# --- CONFIGURACIÓN DEL SERVIDOR WEB (FLASK) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Hola desde Flask! El bot está vivo."

def run_flask():
    # Render asigna un puerto automáticamente en la variable PORT
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DEL BOT ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID_STR = os.getenv("GUILD_ID")
GUILD_ID = int(GUILD_ID_STR) if GUILD_ID_STR else 0

intents = discord.Intents.default()
intents.members = True          
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

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

# --- TUS COMANDOS SLASH (SIN CAMBIOS) ---

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

# --- INICIO DE TODO ---
if __name__ == "__main__":
    # 1. Lanzamos el servidor web en un hilo aparte
    t = threading.Thread(target=run_flask)
    t.start()
    
    # 2. Ejecutamos el bot de Discord
    bot.run(DISCORD_TOKEN)
