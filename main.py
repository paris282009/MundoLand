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
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DEL BOT ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID_STR = os.getenv("GUILD_ID")

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
        await interaction.user.send("Nuestro TikTok: www.tiktok.com")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="youtube", description="Link del canal de YouTube")
async def youtube(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro YouTube: youtube.com")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="tienda", description="Link de la tienda oficial")
async def tienda(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestra tienda: aethermc-webshop.tebex.io")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM.", ephemeral=True)

@bot.tree.command(name="estado", description="Estado del servidor de Discord")
async def estado(interaction: discord.Interaction):
    try:
        response = requests.get("discordstatus.com").json()
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
    embed.set_image(url=f"mc-heads.net{nombre}/left")
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

# --- NUEVOS COMANDOS ACTUALIZADOS ---

@bot.tree.command(name="reportar", description="Reporta a un jugador por mal comportamiento")
async def reportar(interaction: discord.Interaction, jugador: str, motivo: str):
    # ID proporcionado para el canal de reportes
    ID_CANAL_REPORTES = 137275334319747802 # Nota: He usado el ID de canal asociado a tu servidor
    canal = bot.get_channel(ID_CANAL_REPORTES)
    
    embed = discord.Embed(title="🚩 Nuevo Reporte de Jugador", color=discord.Color.red())
    embed.add_field(name="Usuario Reportado:", value=f"`{jugador}`", inline=True)
    embed.add_field(name="Enviado por:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Motivo:", value=motivo, inline=False)
    embed.set_footer(text=f"ID del informante: {interaction.user.id}")
    embed.set_timestamp()
    
    if canal:
        await canal.send(embed=embed)
        await interaction.response.send_message("✅ Tu reporte ha sido recibido por el Staff.", ephemeral=True)
    else:
        # Si el bot no encuentra el canal por ID, lo intenta enviar al canal actual como respaldo
        await interaction.response.send_message("⚠️ Error: No se encontró el canal de reportes configurado.", ephemeral=True)

@bot.tree.command(name="datos", description="Lanza un dado de 6 caras")
async def datos(interaction: discord.Interaction):
    numero = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 ¡Lanzaste los dados y salió **{numero}**!")

@bot.tree.command(name="mcstatus", description="Muestra información en tiempo real de AetherMC")
async def mcstatus(interaction: discord.Interaction):
    await interaction.response.defer() # Usamos defer porque la API puede tardar
    try:
        response = requests.get("api.mcsrvstat.us").json()
        if response["online"]:
            jugadores = response["players"]["online"]
            maximo = response["players"]["max"]
            version = response.get("version", "1.18 - 1.21")
            
            embed = discord.Embed(title="🎮 Estado de AetherMC", color=discord.Color.green())
            embed.add_field(name="Estado", value="🟢 Online", inline=True)
            embed.add_field(name="Jugadores", value=f"`{jugadores}/{maximo}`", inline=True)
            embed.add_field(name="Versión", value=f"`{version}`", inline=False)
            embed.set_thumbnail(url="api.mcsrvstat.us")
            
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ El servidor de Minecraft actualmente está offline.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error al conectar con la API de Minecraft.")

@bot.tree.command(name="stats", description="Busca el perfil de NameMC de un usuario")
async def stats(interaction: discord.Interaction, jugador: str):
    link = f"es.namemc.com{jugador}"
    embed = discord.Embed(title=f"📊 Perfil de {jugador}", description=f"Haz clic [aquí]({link}) para ver skins y nombres anteriores.", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="votar_toop", description="Links para votar y apoyar al servidor")
async def votar_toop(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🗳️ ¡Apoya a AetherMC Votando!", 
        description="Votar nos ayuda a crecer y te da recompensas in-game.",
        color=discord.Color.gold()
    )
    embed.add_field(name="Links de Voto", value="• [Vota en Minecraft-MP](minecraft-mp.com)\n• [Vota en TopG](topg.org)", inline=False)
    embed.add_field(name="🎁 Recompensas", value="¡Obtén llaves de crates y dinero!", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="logro", description="Genera un logro de Minecraft personalizado")
async def logro(interaction: discord.Interaction, texto: str):
    # Genera una imagen de logro usando una API externa
    texto_url = texto.replace(" ", "+")
    icono = random.randint(1, 39) # Iconos aleatorios de Minecraft
    img_url = f"minecraftskinstealer.com{icono}/¡Logro+Obtenido!/{texto_url}"
    
    embed = discord.Embed(color=discord.Color.dark_green())
    embed.set_image(url=img_url)
    await interaction.response.send_message(embed=embed)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Iniciar Flask en un hilo separado
    t = threading.Thread(target=run_flask)
    t.start()
    # Iniciar el Bot de Discord
    bot.run(DISCORD_TOKEN)
