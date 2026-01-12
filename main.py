import os
import discord
import requests
import threading
from flask import Flask
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import random
import datetime
import asyncio
import time

START_TIME = time.time()

# ======================================================
# 🌐 SERVIDOR WEB (FLASK) – KEEP ALIVE
# ======================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot activo – AetherMC"

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# ======================================================
# ⚙️ CONFIGURACIÓN DEL BOT
# ======================================================

# Si usas Render, NO necesitas load_dotenv()
# load_dotenv()  <-- comentar o borrar

# Leer variables de entorno
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN no definido en las variables de entorno de Render")

GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID")) if os.getenv("VOICE_CHANNEL_ID") else None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================================================
# 🎧 FUNCION PARA UNIR AL CANAL DE VOZ + RADIO 24/7
# ======================================================
RADIO_URL = "http://stream.freemusicradio.nl:8100/stream"  # <-- Reemplaza con la URL de tu radio

async def unir_al_voice():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ No se pudo encontrar el servidor")
        return

    canal = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)
    if not canal:
        print("❌ No se encontró el canal de voz")
        return

    vc = guild.voice_client
    if not vc:
        vc = await canal.connect()
        print(f"🎧 Bot conectado al canal {canal.name}")

        # Reproducir radio automáticamente
        vc.play(
            discord.FFmpegPCMAudio(
                RADIO_URL,
                options="-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            )
        )
        print("🎵 Radio 24/7 iniciada")
    else:
        print("🎧 Bot ya estaba conectado a un canal de voz")
        # Si ya estaba conectado, puedes hacer que inicie radio solo si no está sonando
        if not vc.is_playing():
            vc.play(
                discord.FFmpegPCMAudio(
                    RADIO_URL,
                    options="-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                )
            )
            print("🎵 Radio 24/7 iniciada")

# ======================================================
# 🚀 BOT READY
# ======================================================
@bot.event
async def on_ready():
    print(f"🟢 Bot conectado como {bot.user}")

    # Sincronizar comandos
    try:
        if GUILD_ID:
            guild_obj = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild_obj)
            synced = await bot.tree.sync(guild=guild_obj)
            print(f"✅ {len(synced)} comandos sincronizados")
        else:
            synced = await bot.tree.sync()
            print(f"🌍 {len(synced)} comandos globales sincronizados")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    # Conectar al canal de voz
    await unir_al_voice()


# ======================================================
# 🎨 FUNCIÓN BASE PARA EMBEDS
# ======================================================
def embed_base(titulo, descripcion, color=discord.Color.gold()):
    embed = discord.Embed(
        title=titulo,
        description=descripcion,
        color=color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="AetherMC • Sistema Oficial")
    return embed

# ======================================================
# 🔗 REDES SOCIALES
# ======================================================
@bot.tree.command(name="tiktok", description="TikTok oficial")
async def tiktok(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=embed_base("🎵 TikTok", "👉 https://www.tiktok.com"),
        ephemeral=True
    )

@bot.tree.command(name="youtube", description="YouTube oficial")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=embed_base("▶️ YouTube", "👉 https://www.youtube.com"),
        ephemeral=True
    )

@bot.tree.command(name="tienda", description="Tienda oficial")
async def tienda(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=embed_base("🛒 Tienda Oficial", "👉 https://aethermc-webshop.tebex.io"),
        ephemeral=True
    )

# ======================================================
# 📡 ESTADO DISCORD
# ======================================================
@bot.tree.command(name="estado", description="Estado de Discord")
async def estado(interaction: discord.Interaction):
    try:
        r = requests.get("https://discordstatus.com/api/v2/status.json").json()
        estado = r["status"]["description"]
        await interaction.response.send_message(f"📡 Estado de Discord: **{estado}**")
    except:
        await interaction.response.send_message("⚠️ Error al obtener el estado")

# ======================================================
# ⛏️ MINECRAFT
# ======================================================
@bot.tree.command(name="ip", description="IP del servidor")
async def ip(interaction: discord.Interaction):
    embed = embed_base(
        "🌍 Mutation's Network",
        "**IP:** `mutations.fun`\n**Versiones:** 1.18 → 1.21"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mcskin", description="Skin de Minecraft")
async def mcskin(interaction: discord.Interaction, nombre: str):
    embed = embed_base(f"🧱 Skin de {nombre}", "")
    embed.set_image(url=f"https://mc-heads.net/body/{nombre}/300")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mcstatus", description="Estado del servidor Minecraft")
async def mcstatus(interaction: discord.Interaction):

    # RESPONDEMOS INMEDIATO (clave para host gratis)
    await interaction.response.send_message(
        "⏳ Consultando el estado del servidor...",
        ephemeral=False
    )

    ip = "mutations.fun"
    puerto_bedrock = 19132

    try:
        java = requests.get(
            f"https://api.mcsrvstat.us/2/{ip}",
            timeout=5
        ).json()

        bedrock = requests.get(
            f"https://api.mcsrvstat.us/bedrock/2/{ip}:{puerto_bedrock}",
            timeout=5
        ).json()

        embed = discord.Embed(
            title="🎮 Estado del Servidor AetherMC",
            description=f"🌍 **IP:** `{ip}`",
            color=discord.Color.green()
        )

        if java.get("online"):
            embed.add_field(
                name="☕ Java",
                value=f"🟢 Online\n👥 {java['players']['online']}/{java['players']['max']}",
                inline=False
            )
        else:
            embed.add_field(
                name="☕ Java",
                value="🔴 Offline",
                inline=False
            )

        if bedrock.get("online"):
            embed.add_field(
                name="📱 Bedrock",
                value=f"🟢 Online\n👥 {bedrock['players']['online']}/{bedrock['players']['max']}",
                inline=False
            )
        else:
            embed.add_field(
                name="📱 Bedrock",
                value="🔴 Offline",
                inline=False
            )

        await interaction.edit_original_response(
            content=None,
            embed=embed
        )

    except:
        await interaction.edit_original_response(
            content="⚠️ No se pudo obtener el estado del servidor."
        )


@bot.tree.command(name="stats", description="Perfil NameMC")
async def stats(interaction: discord.Interaction, jugador: str):
    link = f"https://es.namemc.com/profile/{jugador}"
    embed = embed_base(
        f"📊 Perfil de {jugador}",
        f"[Ver en NameMC]({link})"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="logro", description="Logro de Minecraft")
async def logro(interaction: discord.Interaction, texto: str):
    texto = texto.replace(" ", "+")
    icono = random.randint(1, 39)
    url = f"https://minecraftskinstealer.com/achievement/{icono}/Logro+Obtenido!/{texto}"
    embed = embed_base("🏆 Logro Desbloqueado", "")
    embed.set_image(url=url)
    await interaction.response.send_message(embed=embed)

# ======================================================
# 🧑 USUARIOS
# ======================================================
@bot.tree.command(name="userinfo", description="Información de usuario")
async def userinfo(interaction: discord.Interaction, miembro: discord.Member = None):
    miembro = miembro or interaction.user
    embed = embed_base(
        f"👤 {miembro}",
        f"🆔 ID: `{miembro.id}`\n🎖 Rol: {miembro.top_role.mention}"
    )
    if miembro.avatar:
        embed.set_thumbnail(url=miembro.avatar.url)
    await interaction.response.send_message(embed=embed)

# ======================================================
# 🎉 DIVERSIÓN
# ======================================================
@bot.tree.command(name="datos", description="Lanza un dado")
async def datos(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 Salió **{random.randint(1,6)}**")

@bot.tree.command(name="sorteo", description="Sorteo aleatorio")
async def sorteo(interaction: discord.Interaction, premio: str):
    usuarios = [m for m in interaction.guild.members if not m.bot]
    ganador = random.choice(usuarios)
    await interaction.response.send_message(f"🎉 **{premio}**\n🏆 Ganador: {ganador.mention}")

# ======================================================
# 🗳️ VOTACIONES
# ======================================================
@bot.tree.command(name="votar", description="Sugerencia con votos")
async def votar(interaction: discord.Interaction, sugerencia: str):
    embed = embed_base("💡 Sugerencia", sugerencia, discord.Color.orange())
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

@bot.tree.command(name="encuesta", description="Encuesta")
async def encuesta(interaction: discord.Interaction, pregunta: str, op1: str, op2: str):
    embed = embed_base(
        "📊 Encuesta",
        f"**{pregunta}**\n\n1️⃣ {op1}\n2️⃣ {op2}",
        discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")

@bot.tree.command(name="votar_toop", description="Links para votar")
async def votar_toop(interaction: discord.Interaction):
    embed = embed_base(
        "🗳️ Apoya al servidor",
        "• https://minecraft-mp.com\n• https://topg.org"
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ======================================================
# 🛡️ MODERACIÓN
# ======================================================
@bot.tree.command(name="say", description="Hablar como el bot")
async def say(interaction: discord.Interaction, mensaje: str):
    if interaction.user.guild_permissions.administrator:
        await interaction.channel.send(mensaje)
        await interaction.response.send_message("✅ Enviado", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Sin permisos", ephemeral=True)

@bot.tree.command(name="decir_embed", description="Embed avanzado")
async def decir_embed(interaction: discord.Interaction, titulo: str, descripcion: str, color_hex: str = "FFD700"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Sin permisos", ephemeral=True)
    try:
        color = int(color_hex.replace("#",""),16)
        embed = discord.Embed(
            title=titulo,
            description=descripcion.replace("\\n","\n"),
            color=color
        )
        embed.set_footer(text=f"Enviado por {interaction.user}")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ Embed enviado", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Color inválido", ephemeral=True)

@bot.tree.command(name="limpiar", description="Borrar mensajes")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpiar(interaction: discord.Interaction, cantidad: int):
    await interaction.response.defer(ephemeral=True)
    borrados = await interaction.channel.purge(limit=cantidad)
    await interaction.followup.send(f"🧹 {len(borrados)} mensajes borrados", ephemeral=True)

@bot.tree.command(name="reportar", description="Reportar jugador")
async def reportar(interaction: discord.Interaction, jugador: str, motivo: str):
    ID_CANAL_REPORTES = 137275334319747802
    canal = bot.get_channel(ID_CANAL_REPORTES)
    embed = embed_base(
        "🚩 Nuevo Reporte",
        f"👤 Jugador: `{jugador}`\n📝 Motivo: {motivo}\n🙋 Reportado por: {interaction.user.mention}",
        discord.Color.red()
    )
    if canal:
        await canal.send(embed=embed)
        await interaction.response.send_message("✅ Reporte enviado", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Canal no encontrado", ephemeral=True)

# ======================================================
# 🎫 SISTEMA DE TICKETS (BOTONES) MEJORADO
# ======================================================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Abrir Ticket", style=discord.ButtonStyle.green)
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild

        # Nombre de la categoría donde se crearán los tickets
        categoria_nombre = "Soporte"  # <-- Cambia esto si quieres otro nombre
        categoria = discord.utils.get(guild.categories, name=categoria_nombre)
        if not categoria:
            categoria = await guild.create_category(categoria_nombre)

        # Nombre del canal de ticket
        canal_nombre = f"soporte-{interaction.user.name}"  # <-- Cambia prefijo si quieres
        canal = await guild.create_text_channel(
            name=canal_nombre,
            category=categoria
        )

        # Permisos para el usuario que creó el ticket
        await canal.set_permissions(interaction.user, read_messages=True, send_messages=True)
        # El resto de usuarios no pueden ver
        await canal.set_permissions(guild.default_role, read_messages=False)

        # Permisos para Staff
        staff = discord.utils.get(guild.roles, name="Staff")  # <-- Cambia nombre del rol si es distinto
        if staff:
            await canal.set_permissions(staff, read_messages=True, send_messages=True)

        # Mensaje inicial dentro del ticket
        await canal.send(
            f"🎫 Ticket creado por {interaction.user.mention}\n"
            "Escribe tu problema o consulta y espera que el staff te atienda."
        )

        # Respuesta efímera al usuario
        await interaction.response.send_message("✅ Ticket creado", ephemeral=True)



    @bot.event
async def on_ready():
    print(f"🟢 Bot conectado como {bot.user}")

    # =========================
    # Sincronización de comandos
    # =========================
    try:
        if GUILD_ID:
            guild_obj = bot.get_guild(GUILD_ID)
            if not guild_obj:
                # Si el bot aún no tiene cache del guild
                guild_obj = await bot.fetch_guild(GUILD_ID)

            # Copiar comandos globales al guild
            bot.tree.copy_global_to(guild=guild_obj)
            synced = await bot.tree.sync(guild=guild_obj)
            print(f"✅ {len(synced)} comandos sincronizados en el servidor")
        else:
            synced = await bot.tree.sync()
            print(f"🌍 {len(synced)} comandos globales sincronizados")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    # Conectar al canal de voz
    await unir_al_voice()
  
# =========================
# COMANDOS UTILIDAD
# =========================

# /ping → Muestra la latencia del bot
@bot.tree.command(name="ping", description="Muestra la latencia del bot")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latencia: **{latency} ms**")

# /uptime → Muestra cuánto tiempo lleva encendido el bot
@bot.tree.command(name="uptime", description="Muestra el tiempo que lleva encendido el bot")
async def uptime(interaction: discord.Interaction):
    segundos = int(time.time() - START_TIME)
    tiempo_str = str(datetime.timedelta(seconds=segundos))
    await interaction.response.send_message(f"⏱️ Uptime del bot: **{tiempo_str}**")

# /serverinfo → Información del servidor
@bot.tree.command(name="serverinfo", description="Muestra información del servidor")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"📊 Información de {guild.name}",
        color=discord.Color.blurple()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="🆔 ID", value=guild.id, inline=True)
    embed.add_field(name="👥 Miembros", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Creado", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🚀 Boosts", value=guild.premium_subscription_count, inline=True)
    embed.set_footer(text=f"Solicitado por {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

# /avatar → Muestra el avatar de un usuario o del propio
@bot.tree.command(name="avatar", description="Muestra el avatar de un usuario")
@app_commands.describe(usuario="Usuario del que quieres ver el avatar")
async def avatar(interaction: discord.Interaction, usuario: discord.Member = None):
    usuario = usuario or interaction.user
    embed = discord.Embed(
        title=f"🖼️ Avatar de {usuario.name}",
        color=discord.Color.blue()
    )
    embed.set_image(url=usuario.display_avatar.url)
    await interaction.response.send_message(embed=embed)


# ======================================================
# 🎵 COMANDOS DE RADIO 24/7
# ======================================================


# Función para conectar al canal de voz y reproducir radio
async def conectar_radio(guild, url=RADIO_URL):
    canal = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)
    if not canal:
        print("❌ Canal de voz no encontrado")
        return

    vc = guild.voice_client
    if not vc:
        vc = await canal.connect()
    
    if not vc.is_playing():
        vc.play(
            discord.FFmpegPCMAudio(
                url,
                options="-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            )
        )
        print(f"🎶 Reproduciendo radio en {canal.name}")

# /radio → estado de la radio
@bot.tree.command(name="radio", description="Muestra el estado de la radio")
async def radio(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc or not vc.is_connected():
        await interaction.response.send_message("❌ El bot no está conectado a un canal de voz.")
        return

    if vc.is_playing():
        await interaction.response.send_message("🎶 La radio está sonando actualmente.")
    else:
        await interaction.response.send_message("❌ La radio no está activa.")

# /radio_detener → detener la radio
@bot.tree.command(name="radio_detener", description="Detiene la radio")
async def radio_detener(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc or not vc.is_connected():
        await interaction.response.send_message("❌ El bot no está conectado a un canal de voz.")
        return

    if vc.is_playing():
        vc.stop()
        await interaction.response.send_message("⏹️ Radio detenida.")
    else:
        await interaction.response.send_message("❌ La radio no está activa.")


# /radio_cambiar → Cambiar URL
@bot.tree.command(name="radio_cambiar", description="Cambia la emisora de radio a una predeterminada")
async def radio_cambiar(interaction: discord.Interaction):
    # Nueva URL de radio que quieres usar
    nueva_url = "http://stream.freemusicradio.nl:8100/stream"  # <-- Cambia aquí si quieres otra emisora

    vc = interaction.guild.voice_client
    if not vc:
        canal = discord.utils.get(interaction.guild.voice_channels, id=VOICE_CHANNEL_ID)
        if not canal:
            await interaction.response.send_message("❌ Canal de voz no encontrado")
            return
        vc = await canal.connect()

    if vc.is_playing():
        vc.stop()
    
    vc.play(
        discord.FFmpegPCMAudio(
            nueva_url,
            options="-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        )
    )
    global RADIO_URL
    RADIO_URL = nueva_url
    await interaction.response.send_message(f"🔄 Radio cambiada a la emisora: {nueva_url}")



# ======================================================
# ▶️ EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)








