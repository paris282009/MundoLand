"""
Cog de Información: /datos, /estado, /avatar, /userinfo
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from datetime import datetime

class InformationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ============== DATOS ==============
    
    @app_commands.command(name="datos", description="Ver información del servidor")
    async def datos(self, interaction: discord.Interaction):
        """Mostrar información del servidor"""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"Información de {guild.name}",
            color=COLORS['info']
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        
        embed.add_field(name="ID del Servidor", value=guild.id, inline=False)
        embed.add_field(name="Dueño", value=f"<@{guild.owner_id}>", inline=False)
        embed.add_field(name="Creado", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=False)
        embed.add_field(name="Miembros Totales", value=guild.member_count, inline=True)
        embed.add_field(name="Canales", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Nivel de Verificación", value=guild.verification_level, inline=True)
        embed.add_field(name="Región", value=guild.region if hasattr(guild, 'region') else "No disponible", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    # ============== ESTADO ==============
    
    @app_commands.command(name="estado", description="Ver estado del servidor")
    async def estado(self, interaction: discord.Interaction):
        """Mostrar estado del servidor Discord"""
        guild = interaction.guild
        
        online = sum(1 for m in guild.members if m.status != discord.Status.offline)
        offline = guild.member_count - online
        
        embed = discord.Embed(
            title="Estado del Servidor",
            color=COLORS['success']
        )
        
        embed.add_field(name="Estado", value="🟢 En línea", inline=False)
        embed.add_field(name="Miembros En Línea", value=f"{online}/{guild.member_count}", inline=True)
        embed.add_field(name="Miembros Offline", value=offline, inline=True)
        embed.add_field(name="Canales Activos", value=len([c for c in guild.channels if isinstance(c, discord.TextChannel)]), inline=True)
        embed.add_field(name="Canales de Voz", value=len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)]), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    # ============== AVATAR ==============
    
    @app_commands.command(name="avatar", description="Ver tu avatar")
    @app_commands.describe(usuario="Usuario (opcional)")
    async def avatar(self, interaction: discord.Interaction, usuario: discord.User = None):
        """Mostrar avatar de un usuario"""
        user = usuario or interaction.user
        
        embed = discord.Embed(
            title=f"Avatar de {user.name}",
            color=COLORS['purple']
        )
        
        embed.set_image(url=user.avatar.url)
        embed.add_field(name="Usuario", value=f"@{user.name}#{user.discriminator}", inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Cuenta creada", value=f"<t:{int(user.created_at.timestamp())}:R>", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    # ============== USERINFO ==============
    
    @app_commands.command(name="userinfo", description="Ver información de usuario")
    @app_commands.describe(usuario="Usuario (opcional)")
    async def userinfo(self, interaction: discord.Interaction, usuario: discord.User = None):
        """Mostrar información detallada del usuario"""
        user = usuario or interaction.user
        member = interaction.guild.get_member(user.id)
        
        embed = discord.Embed(
            title=f"Información de {user.name}",
            color=COLORS['info']
        )
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
        
        embed.add_field(name="Usuario", value=f"{user.mention}", inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value="Sí" if user.bot else "No", inline=True)
        embed.add_field(name="Cuenta creada", value=f"<t:{int(user.created_at.timestamp())}:R>", inline=False)
        
        if member:
            embed.add_field(name="Se unió al servidor", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=False)
            embed.add_field(name="Roles", value=f"{len(member.roles) - 1}", inline=True)
            
            if member.roles[1:]:
                roles_text = ", ".join([r.mention for r in member.roles[1:][:5]])
                if len(member.roles) > 6:
                    roles_text += f"... y {len(member.roles) - 6} más"
                embed.add_field(name="Primeros Roles", value=roles_text, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InformationCog(bot))
