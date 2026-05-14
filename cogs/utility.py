"""
Cog de Utilidad: Encuestas, /say, /decir_embed, /limpiar, /emoji_id
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
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
    
    @app_commands.command(name="say", description="Enviar un mensaje de texto (solo admin)")
    @app_commands.describe(mensaje="El mensaje a enviar")
    async def say(self, interaction: discord.Interaction, mensaje: str):
        """Comando say solo para administradores - Solo texto, sin embed"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(mensaje)
        await interaction.followup.send("✅ Mensaje enviado.", ephemeral=True)
    
    # ============== DECIR EMBED (Menú interactivo tipo Nekotina) ==============
    
    @app_commands.command(name="decir_embed", description="Crear embed con menú personalizado (solo admin)")
    async def decir_embed(self, interaction: discord.Interaction):
        """Comando decir_embed con menú interactivo para crear embeds"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return
        
        await interaction.response.send_modal(EmbedCreatorModal(interaction.channel))
    
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
    
    # ============== EMOJI_ID ==============
    
    @app_commands.command(name="emoji_id", description="Lista de emojis animados y sus IDs")
    async def emoji_id(self, interaction: discord.Interaction):
        """Comando para listar emojis animados del servidor"""
        await interaction.response.defer()
        
        # Obtener servidor actual
        guild = interaction.guild
        
        if not guild:
            await interaction.followup.send("Este comando solo funciona en servidores")
            return
        
        # Filtrar emojis animados
        animated_emojis = [emoji for emoji in guild.emojis if emoji.animated]
        
        if not animated_emojis:
            embed = discord.Embed(
                title="❌ No hay emojis animados",
                description="Este servidor no tiene emojis animados",
                color=COLORS['error']
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Crear embeds (máximo 25 campos por embed)
        embeds = []
        current_embed = discord.Embed(
            title="🎬 Emojis Animados",
            description=f"Total: {len(animated_emojis)} emojis animados",
            color=COLORS['purple']
        )
        
        for i, emoji in enumerate(animated_emojis):
            # Cada 25 emojis, crear un nuevo embed
            if i > 0 and i % 25 == 0:
                embeds.append(current_embed)
                current_embed = discord.Embed(
                    title="🎬 Emojis Animados (continuación)",
                    color=COLORS['purple']
                )
            
            # Añadir campo con emoji, nombre e ID
            current_embed.add_field(
                name=f"{emoji} {emoji.name}",
                value=f"```ID: {emoji.id}```",
                inline=False
            )
        
        # Añadir el último embed
        embeds.append(current_embed)
        
        # Enviar embeds
        for embed in embeds:
            await interaction.followup.send(embed=embed)


# ============== MODALES ==============

class EmbedCreatorModal(discord.ui.Modal, title="Crear Embed"):
    """Modal para crear un embed completo con opciones tipo Nekotina"""
    
    titulo = discord.ui.TextInput(
        label="Título",
        placeholder="Título del embed...",
        required=False,
        max_length=256
    )
    
    descripcion = discord.ui.TextInput(
        label="Descripción",
        placeholder="Descripción del embed...",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=4000
    )
    
    color_hex = discord.ui.TextInput(
        label="Color (hex)",
        placeholder="Ej: ff0000 (rojo) - sin el #",
        required=False,
        max_length=6
    )
    
    autor = discord.ui.TextInput(
        label="Autor",
        placeholder="Nombre del autor...",
        required=False,
        max_length=256
    )
    
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
    
    async def on_submit(self, interaction: discord.Interaction):
        # Color
        try:
            color = int(self.color_hex.value.strip(), 16) if self.color_hex.value.strip() else COLORS['purple']
        except ValueError:
            color = COLORS['purple']

        embed = discord.Embed(
            title=self.titulo.value or None,
            description=self.descripcion.value or None,
            color=color
        )

        if self.autor.value.strip():
            embed.set_author(name=self.autor.value.strip())

        # Mostrar menú para más opciones
        await interaction.response.defer(ephemeral=True)
        view = EmbedEditorView(embed, self.channel)
        await interaction.followup.send(
            "Elige qué más quieres agregar al embed:",
            view=view,
            ephemeral=True
        )


class EmbedEditorView(discord.ui.View):
    """Vista interactiva para editar embeds"""
    
    def __init__(self, embed: discord.Embed, channel):
        super().__init__()
        self.embed = embed
        self.channel = channel
        self.image_url = None
        self.thumbnail_url = None
        self.footer_text = None
    
    @discord.ui.button(label="📷 Imagen Principal", style=discord.ButtonStyle.primary)
    async def image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal(self, "principal"))
    
    @discord.ui.button(label="🖼️ Imagen de Perfil", style=discord.ButtonStyle.primary)
    async def thumbnail_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal(self, "thumbnail"))
    
    @discord.ui.button(label="📝 Pie de Página", style=discord.ButtonStyle.secondary)
    async def footer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FooterModal(self))
    
    @discord.ui.button(label="📤 Enviar Embed", style=discord.ButtonStyle.success)
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.image_url:
            self.embed.set_image(url=self.image_url)
        if self.thumbnail_url:
            self.embed.set_thumbnail(url=self.thumbnail_url)
        if self.footer_text:
            self.embed.set_footer(text=self.footer_text)
        
        await self.channel.send(embed=self.embed)
        await interaction.response.send_message("✅ Embed enviado correctamente", ephemeral=True)
        self.stop()


class ImageModal(discord.ui.Modal, title="Agregar Imagen"):
    """Modal para agregar imágenes"""
    
    url_input = discord.ui.TextInput(
        label="URL de la imagen",
        placeholder="https://ejemplo.com/imagen.png",
        required=True
    )
    
    def __init__(self, view: EmbedEditorView, image_type: str):
        super().__init__()
        self.view = view
        self.image_type = image_type
    
    async def on_submit(self, interaction: discord.Interaction):
        url = self.url_input.value.strip()
        
        if self.image_type == "principal":
            self.view.image_url = url
            mensaje = "✅ Imagen principal agregada"
        else:
            self.view.thumbnail_url = url
            mensaje = "✅ Imagen de perfil agregada"
        
        await interaction.response.send_message(mensaje, ephemeral=True)


class FooterModal(discord.ui.Modal, title="Pie de Página"):
    """Modal para agregar pie de página"""
    
    footer_input = discord.ui.TextInput(
        label="Texto del pie de página",
        placeholder="Texto que aparece abajo...",
        required=True,
        max_length=2048
    )
    
    def __init__(self, view: EmbedEditorView):
        super().__init__()
        self.view = view
    
    async def on_submit(self, interaction: discord.Interaction):
        self.view.footer_text = self.footer_input.value.strip()
        await interaction.response.send_message("✅ Pie de página agregado", ephemeral=True)


async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
