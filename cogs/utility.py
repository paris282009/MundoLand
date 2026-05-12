"""
Cog de Utilidad: Encuestas, /say, /say-embed, /limpiar
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from database import add_button_to_message
import asyncio

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ============== ENCUESTAS ==============
    
    @app_commands.command(name="encuesta", description="Crear una encuesta interactiva")
    @app_commands.describe(pregunta="Pregunta de la encuesta", opciones="Opciones separadas por |")
    async def encuesta(self, interaction: discord.Interaction, pregunta: str, opciones: str):
        """Crear encuesta con reacciones"""
        opciones_list = [opt.strip() for opt in opciones.split('|')]
        
        if len(opciones_list) < 2 or len(opciones_list) > 10:
            await interaction.response.send_message(
                "Debes proporcionar entre 2 y 10 opciones",
                ephemeral=True
            )
            return
        
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = discord.Embed(
            title="📊 Encuesta",
            description=pregunta,
            color=COLORS['info']
        )
        
        for i, opcion in enumerate(opciones_list):
            embed.add_field(name=f"{emojis[i]} Opción {i+1}", value=opcion, inline=False)
        
        embed.set_footer(text=f"Encuesta creada por {interaction.user}")
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        for i in range(len(opciones_list)):
            await message.add_reaction(emojis[i])
    
    # ============== SAY ==============
    
    @app_commands.command(name="say", description="Enviar un mensaje (solo admin)")
    @app_commands.describe(mensaje="El mensaje a enviar")
    async def say(self, interaction: discord.Interaction, mensaje: str):
        """Comando say solo para administradores"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Crear embed con opciones de personalización
        embed = discord.Embed(
            title="Editor de Mensajes",
            description=f"Mensaje: {mensaje}",
            color=COLORS['info']
        )
        
        view = MessageEditorView(self.bot, interaction.user, mensaje, interaction.channel)
        await interaction.followup.send(embed=embed, view=view)
    
    # ============== SAY-EMBED ==============
    
    @app_commands.command(name="say_embed", description="Enviar un embed personalizado (solo admin)")
    @app_commands.describe(titulo="Título del embed", descripcion="Descripción")
    async def say_embed(self, interaction: discord.Interaction, titulo: str, descripcion: str):
        """Comando say-embed para administradores"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=COLORS['purple']
        )
        
        view = EmbedEditorView(self.bot, interaction.user, titulo, descripcion, interaction.channel)
        await interaction.followup.send(embed=embed, view=view)
    
    # ============== LIMPIAR ==============
    
    @app_commands.command(name="limpiar", description="Borrar mensajes (solo admin)")
    @app_commands.describe(cantidad="Cantidad de mensajes a borrar (1-100)")
    async def limpiar(self, interaction: discord.Interaction, cantidad: int):
        """Comando para limpiar mensajes"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return
        
        if cantidad < 1 or cantidad > 100:
            await interaction.response.send_message(
                "Cantidad debe estar entre 1 y 100",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            deleted = await interaction.channel.purge(limit=cantidad)
            await interaction.followup.send(
                f"Se borraron {len(deleted)} mensajes",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"Error al borrar mensajes: {str(e)}",
                ephemeral=True
            )

# ============== VISTAS (VIEWS) ==============

class MessageEditorView(discord.ui.View):
    """Vista para editar mensajes"""
    
    def __init__(self, bot, user, mensaje, channel):
        super().__init__()
        self.bot = bot
        self.user = user
        self.mensaje = mensaje
        self.channel = channel
        self.color = COLORS['purple']
        self.image_url = None
        self.fields = []
    
    @discord.ui.button(label="Color", style=discord.ButtonStyle.primary)
    async def color_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ColorModal(self))
    
    @discord.ui.button(label="Imagen", style=discord.ButtonStyle.secondary)
    async def image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal(self))
    
    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.success)
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            description=self.mensaje,
            color=self.color
        )
        
        if self.image_url:
            embed.set_image(url=self.image_url)
        
        await self.channel.send(embed=embed)
        await interaction.response.send_message("Mensaje enviado", ephemeral=True)
        self.stop()

class EmbedEditorView(discord.ui.View):
    """Vista para editar embeds"""
    
    def __init__(self, bot, user, titulo, descripcion, channel):
        super().__init__()
        self.bot = bot
        self.user = user
        self.titulo = titulo
        self.descripcion = descripcion
        self.channel = channel
        self.color = COLORS['purple']
        self.image_url = None
    
    @discord.ui.button(label="Color", style=discord.ButtonStyle.primary)
    async def color_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ColorModal(self))
    
    @discord.ui.button(label="Imagen", style=discord.ButtonStyle.secondary)
    async def image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal(self))
    
    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.success)
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.titulo,
            description=self.descripcion,
            color=self.color
        )
        
        if self.image_url:
            embed.set_image(url=self.image_url)
        
        await self.channel.send(embed=embed)
        await interaction.response.send_message("Embed enviado", ephemeral=True)
        self.stop()

class ColorModal(discord.ui.Modal, title="Cambiar Color"):
    """Modal para cambiar color del embed"""
    
    color_input = discord.ui.TextInput(
        label="Color en Hex (ej: FF0000)",
        placeholder="FF0000"
    )
    
    def __init__(self, view):
        super().__init__()
        self.view = view
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            color_hex = self.color_input.value.replace("#", "")
            self.view.color = int(color_hex, 16)
            await interaction.response.send_message("Color actualizado", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Color inválido", ephemeral=True)

class ImageModal(discord.ui.Modal, title="Agregar Imagen"):
    """Modal para agregar imagen"""
    
    url_input = discord.ui.TextInput(
        label="URL de la imagen",
        placeholder="https://ejemplo.com/imagen.png"
    )
    
    def __init__(self, view):
        super().__init__()
        self.view = view
    
    async def on_submit(self, interaction: discord.Interaction):
        self.view.image_url = self.url_input.value
        await interaction.response.send_message("Imagen agregada", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
