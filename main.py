import os
import webserver
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# --- SECCIÓN CORREGIDA ---
# Configurar intents
intents = discord.Intents.default()
intents.members = True          # Para ver a los miembros
intents.message_content = True  # <--- ESTA ES LA LÍNEA QUE FALTABA
# -------------------------

bot = commands.Bot(command_prefix="!", intents=intents)


# Sincronización
@bot.event
async def on_ready():
    print(f"{bot.user} está conectado ✅")
    try:
        # Esto sincroniza tus comandos /slash con el servidor
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")


# /tiktok
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="tiktok", description="Recibe el link del TikTok oficial")
async def tiktok(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro TikTok: https://www.tiktok.com/@mundo.land5?_r=1&_t=ZS-92Pte028pC1")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM (quizá los tienes bloqueados).", ephemeral=True)


# /youtube
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="youtube", description="Recibe el link del canal de YouTube")
async def youtube(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestro YouTube: https://youtube.com/@elparis1?si=KJ8KL2j9AxFUXjpM")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM (quizá los tienes bloqueados).", ephemeral=True)


# /tienda
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="tienda", description="Recibe el link de la tienda oficial")
async def tienda(interaction: discord.Interaction):
    try:
        await interaction.user.send("Nuestra tienda: https://aethermc-webshop.tebex.io/AetherMC-tienda")
        await interaction.response.send_message("Te envié el link por DM", ephemeral=True)
    except:
        await interaction.response.send_message("No pude enviarte DM (quizá los tienes bloqueados).", ephemeral=True)


# /estado
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="estado", description="Muestra si el servidor de Discord está abierto o cerrado")
async def estado(interaction: discord.Interaction):
    try:
        response = requests.get("https://discordstatus.com/api/v2/status.json").json()
        status = response["status"]["description"]

        traducciones = {
            "All Systems Operational": "🟢 (Servidor abierto)",
            "Partial System Outage": "🟡 (Servidor inestable)",
            "Major System Outage": "🔴 (Servidor cerrado)",
            "Minor Service Outage": "🟠 (Problemas menores)"
        }

        estado_es = traducciones.get(status, "⚠ (Estado desconocido)")
        await interaction.response.send_message(estado_es)

    except Exception:
        await interaction.response.send_message("⚠ (Error al obtener el estado)")


# /ip
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="ip", description="Muestra la IP de nuestro servidor de Minecraft")
async def ip(interaction: discord.Interaction):
    embed = discord.Embed(
        title="AetherMC",
        description="*IP:* `aethermc.space`\n📌 Versión: 1.18 x +1.21 ",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

# /say
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="say", description="Envía un mensaje a través del bot")
@commands.has_permissions(administrator=True) # Solo administradores pueden usarlo
async def say(interaction: discord.Interaction, mensaje: str):
    # Envía el mensaje al canal donde se usó el comando
    await interaction.channel.send(mensaje)
    # Responde de forma invisible para que no ensucie el chat
    await interaction.response.send_message("Mensaje enviado con éxito.", ephemeral=True)

    # /decir_embed
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="decir_embed", description="Envía un mensaje elegante en un cuadro (Embed)")
@commands.has_permissions(administrator=True)
async def decir_embed(interaction: discord.Interaction, titulo: str, descripcion: str, color_hex: str = "FFD700"):
    try:
        # Convertir el color de Hexadecimal a entero de Discord
        color_int = int(color_hex.replace("#", ""), 16)
        
        embed = discord.Embed(
            title=titulo,
            description=descripcion.replace("\\n", "\n"), # Permite usar \n para saltos de línea
            color=color_int
        )
        
        # Opcional: Pie de página con el nombre del servidor
        embed.set_footer(text=f"Enviado por: {interaction.user.name}")
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed enviado correctamente.", ephemeral=True)
        
    except ValueError:
        await interaction.response.send_message("Error: El formato de color debe ser Hex (ejemplo: FF0000 para rojo).", ephemeral=True)

webserver.keep_alive()
bot.run(DISCORD_TOKEN)