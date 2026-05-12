"""
Cog de Sistema de Servidores: /serveradd, /serveredit, /servidores, /add-boton
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from database import (
    add_server, get_all_servers, get_user_servers,
    edit_server, delete_server, add_button_to_message
)

class ServerSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ============== AGREGAR SERVIDOR ==============
    
    @app_commands.command(name="serveradd", description="Agregar tu servidor al directorio")
    @app_commands.describe(
        nombre="Nombre del servidor",
        ip="IP del servidor",
        puerto="Puerto",
        descripcion="Descripción (opcional)"
    )
    async def serveradd(
        self,
        interaction: discord.Interaction,
        nombre: str,
        ip: str,
        puerto: int,
        descripcion: str = "Sin descripción"
    ):
        """Agregar servidor al directorio público"""
        
        # Validar puerto
        if puerto < 1 or puerto > 65535:
            await interaction.response.send_message(
                "Puerto debe estar entre 1 y 65535",
                ephemeral=True
            )
            return
        
        success = add_server(
            interaction.guild.id,
            interaction.user.id,
            nombre,
            ip,
            puerto,
            descripcion
        )
        
        if success:
            embed = discord.Embed(
                title="Servidor Agregado",
                color=COLORS['success']
            )
            embed.add_field(name="Nombre", value=nombre, inline=False)
            embed.add_field(name="IP:Puerto", value=f"{ip}:{puerto}", inline=False)
            embed.add_field(name="Descripción", value=descripcion, inline=False)
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "Este servidor ya está registrado",
                ephemeral=True
            )
    
    # ============== EDITAR SERVIDOR ==============
    
    @app_commands.command(name="serveredit", description="Editar tu servidor")
    @app_commands.describe(
        servidor_id="ID del servidor a editar",
        nuevo_nombre="Nuevo nombre (opcional)",
        nueva_descripcion="Nueva descripción (opcional)"
    )
    async def serveredit(
        self,
        interaction: discord.Interaction,
        servidor_id: int,
        nuevo_nombre: str = None,
        nueva_descripcion: str = None
    ):
        """Editar un servidor (solo el dueño)"""
        
        updates = {}
        if nuevo_nombre:
            updates['server_name'] = nuevo_nombre
        if nueva_descripcion:
            updates['description'] = nueva_descripcion
        
        if not updates:
            await interaction.response.send_message(
                "Debes proporcionar al menos un campo para actualizar",
                ephemeral=True
            )
            return
        
        success = edit_server(servidor_id, interaction.user.id, **updates)
        
        if success:
            await interaction.response.send_message(
                "Servidor actualizado correctamente",
                ephemeral=False
            )
        else:
            await interaction.response.send_message(
                "No encontrado o no tienes permiso para editar este servidor",
                ephemeral=True
            )
    
    # ============== LISTAR SERVIDORES ==============
    
    @app_commands.command(name="servidores", description="Ver todos los servidores registrados")
    async def servidores(self, interaction: discord.Interaction):
        """Mostrar lista de servidores"""
        servers = get_all_servers(interaction.guild.id)
        
        if not servers:
            await interaction.response.send_message(
                "No hay servidores registrados en este servidor",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"Servidores Registrados ({len(servers)})",
            color=COLORS['info']
        )
        
        for i, server in enumerate(servers, 1):
            server_id, guild_id, owner_id, name, ip, port, desc, _ = server
            
            embed.add_field(
                name=f"{i}. {name}",
                value=f"IP: {ip}:{port}\nDueño: <@{owner_id}>\nDescripción: {desc}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    # ============== AGREGAR BOTÓN A MENSAJE ==============
    
    @app_commands.command(name="add_boton", description="Agregar botón a un mensaje (solo admin)")
    @app_commands.describe(
        message_id="ID del mensaje",
        nombre_boton="Nombre del botón",
        url="URL del botón"
    )
    async def add_boton(
        self,
        interaction: discord.Interaction,
        message_id: int,
        nombre_boton: str,
        url: str
    ):
        """Agregar botón a un mensaje existente"""
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Solo administradores pueden usar este comando",
                ephemeral=True
            )
            return
        
        try:
            # Buscar el mensaje en todos los canales
            message = None
            for channel in interaction.guild.text_channels:
                try:
                    message = await channel.fetch_message(message_id)
                    break
                except discord.NotFound:
                    continue
            
            if not message:
                await interaction.response.send_message(
                    "Mensaje no encontrado",
                    ephemeral=True
                )
                return
            
            # Agregar botón a la BD
            add_button_to_message(
                message_id,
                message.channel.id,
                interaction.guild.id,
                nombre_boton,
                url,
                interaction.user.id
            )
            
            # Crear vista con botón
            view = discord.ui.View()
            view.add_item(discord.ui.Button(
                label=nombre_boton,
                url=url,
                style=discord.ButtonStyle.link
            ))
            
            # Actualizar mensaje
            await message.edit(view=view)
            
            await interaction.response.send_message(
                f"Botón '{nombre_boton}' agregado al mensaje",
                ephemeral=True
            )
        
        except Exception as e:
            await interaction.response.send_message(
                f"Error al agregar botón: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(ServerSystemCog(bot))
