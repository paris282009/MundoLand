import os
import discord
import requests
import threading
from flask import Flask
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import random
import asyncio
import datetime

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
# Manejo de error si GUILD_ID no existe
try:
    GUILD_ID = int(GUILD_ID_STR) if GUILD_ID_STR else 0
except ValueError:
    GUILD_ID = 0

intents = discord.Intents.default()
intents.members = True          
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} está conectado ✅")
    try:
        # Sincronización corregida: primero copia los comandos al gremio y luego sincroniza
        if GUILD_ID != 0:
            guild_obj = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild_obj)
            synced = await bot.tree.sync(guild=guild_obj)
            print(f"Comandos sincronizados en servidor {GUILD_ID}: {len(synced)}")
        else:
            synced = await bot.tree.sync()
            print(f"Comandos sincronizados globalmente: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# --- TUS COMANDOS SLASH ---

@bot.tree.command(name="tiktok", description="Link del TikTok oficial")
async def tiktok(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro TikTok: https://www.tiktok.com/@mundo.land5")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="youtube", description="Link del canal de YouTube")
async def youtube(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro YouTube: https://youtube.com/@elparis1")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="tienda", description="Link de la tienda oficial")
async def tienda(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestra tienda: https://aethermc-webshop.tebex.io/AetherMC-tienda")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="estado", description="Estado del servidor de Discord")
async def estado(interaction: discord.Interaction):
    try:
        response = requests.get("https://discordstatus.com/api/v2/status.json").json()
        status = response["status"]["description"]
        traducciones = {
            "All Systems Operational": "🟢 (Servidor abierto)",
            "Partial System Outage": "🟡 (Servidor inestable)",
            "Major System Outage": "🔴 (Servidor cerrado)"
        }
        estado_es = traducciones.get(status, f"⚠ ({status})")
        await interaction.response.send_message(estado_es)
    except:
        await interaction.response.send_message("⚠ (Error al obtener el estado)")

@bot.tree.command(name="ip", description="IP del servidor de Minecraft")
async def ip(interaction: discord.Interaction):
    embed = discord.Embed(
        title="AetherMC",
        description="*IP:* `aethermc.space`\n📌 Versión: 1.18 x +1.21 ",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say", description="Envía un mensaje a través del bot")
async def say(interaction: discord.Interaction, mensaje: str):
    if interaction.user.guild_permissions.administrator:
        await interaction.channel.send(mensaje)
        await interaction.response.send_message("Mensaje enviado.", ephemeral=True)
    else:
        await interaction.response.send_message("No tienes permisos.", ephemeral=True)

@bot.tree.command(name="decir_embed", description="Envía un mensaje elegante (Embed)")
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

@bot.tree.command(name="userinfo", description="Muestra información de un usuario")
async def userinfo(interaction: discord.Interaction, miembro: discord.Member = None):
    miembro = miembro or interaction.user
    embed = discord.Embed(title=f"👤 Info de {miembro.name}", color=discord.Color.blue())
    if miembro.avatar:
        embed.set_thumbnail(url=miembro.avatar.url)
    embed.add_field(name="ID", value=miembro.id, inline=True)
    embed.add_field(name="Se unió", value=miembro.joined_at.strftime("%d/%m/%Y") if miembro.joined_at else "Desconocido", inline=True)
    embed.add_field(name="Top Rol", value=miembro.top_role.mention, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mcskin", description="Muestra la skin de Minecraft de un jugador")
async def mcskin(interaction: discord.Interaction, nombre: str):
    embed = discord.Embed(title=f"Skin de {nombre}", color=discord.Color.green())
    embed.set_image(url=f"https://mc-heads.net/body/{nombre}/left")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sorteo", description="Elige un ganador al azar")
async def sorteo(interaction: discord.Interaction, premio: str):
    usuarios = [m for m in interaction.guild.members if not m.bot]
    if not usuarios:
        return await interaction.response.send_message("No hay usuarios para elegir.")
    ganador = random.choice(usuarios)
    await interaction.response.send_message(f"🎉 **SORTEO: {premio}** 🎉\n¡El ganador es {ganador.mention}!")

@bot.tree.command(name="votar", description="Crea una sugerencia (votos ✅/❌)")
async def votar(interaction: discord.Interaction, sugerencia: str):
    embed = discord.Embed(title="💡 Sugerencia", description=sugerencia, color=discord.Color.orange())
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

@bot.tree.command(name="encuesta", description="Encuesta de 2 opciones")
async def encuesta(interaction: discord.Interaction, pregunta: str, op1: str, op2: str):
    embed = discord.Embed(title="📊 Encuesta", description=f"**{pregunta}**\n\n1️⃣ {op1}\n2️⃣ {op2}", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")

@bot.tree.command(name="limpiar", description="Borra mensajes")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpiar(interaction: discord.Interaction, cantidad: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=cantidad)
    await interaction.followup.send(f"✅ Borrados {len(deleted)} mensajes.", ephemeral=True)

@bot.tree.command(name="recordatorio", description="Recordatorio en X minutos")
async def recordatorio(interaction: discord.Interaction, minutos: int, texto: str):
    await interaction.response.send_message(f"⏰ Te avisaré en {minutos} min.", ephemeral=True)
    await asyncio.sleep(minutos * 60)
    await interaction.user.send(f"🔔 **RECORDATORIO:** {texto}")

class TicketView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.green, emoji="📩", custom_id="tkt")
    async def open_t(self, it: discord.Interaction, button: discord.ui.Button):
        ch = await it.guild.create_text_channel(f"ticket-{it.user.name}", overwrites={
            it.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            it.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
        await it.response.send_message(f"Ticket en {ch.mention}", ephemeral=True)

@bot.tree.command(name="setup_ticket", description="Mensaje de tickets")
async def setup_ticket(interaction: discord.Interaction):
    await interaction.response.send_message(content="Pulsa para soporte", view=TicketView())

# --- INICIO DE TODO ---
if __name__ == "__main__":
    # Iniciar Flask en hilo "daemon" para que no bloquee el cierre del bot
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("Error: DISCORD_TOKEN no encontrado en el archivo .env")
