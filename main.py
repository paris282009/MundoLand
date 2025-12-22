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
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================================================
# 🚀 BOT READY
# ======================================================
@bot.event
async def on_ready():
    print(f"🟢 {bot.user} conectado correctamente")
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ {len(synced)} comandos sincronizados en el servidor")
        else:
            synced = await bot.tree.sync()
            print(f"🌍 {len(synced)} comandos globales sincronizados")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

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
        "🌍 AetherMC",
        "**IP:** `aethermc.space`\n**Versiones:** 1.18 → 1.21"
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

    ip = "aethermc.space"
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
# 🎫 SISTEMA DE TICKETS (BOTONES)
# ======================================================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Abrir Ticket", style=discord.ButtonStyle.green)
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        categoria = discord.utils.get(guild.categories, name="🎫 TICKETS")
        if not categoria:
            categoria = await guild.create_category("🎫 TICKETS")

        canal = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=categoria
        )
        await canal.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await canal.set_permissions(guild.default_role, read_messages=False)

        await canal.send(f"🎫 Ticket creado por {interaction.user.mention}")
        await interaction.response.send_message("✅ Ticket creado", ephemeral=True)

@bot.tree.command(name="ticket", description="Abrir panel de tickets")
async def ticket(interaction: discord.Interaction):
    embed = embed_base(
        "🎫 Soporte AetherMC",
        "Pulsa el botón para crear un ticket con el staff"
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

@bot.tree.command(name="setup_ticket", description="Configura el panel de tickets")
@discord.app_commands.checks.has_permissions(administrator=True)
async def setup_ticket(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫 Sistema de Tickets",
        description=(
            "Bienvenido al sistema de soporte de **AetherMC**\n\n"
            "Pulsa el botón de abajo para crear un ticket y "
            "el staff te atenderá lo antes posible."
        ),
        color=discord.Color.green()
    )

    await interaction.response.send_message(
        embed=embed,
        view=TicketView()
    )

# ======================================================
# ▶️ EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)



