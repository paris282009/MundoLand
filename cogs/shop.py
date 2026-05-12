"""
Cog de Tienda: /tienda (estructura base, listo para agregar funcionalidad)
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tienda", description="Ver la tienda del servidor")
    async def tienda(self, interaction: discord.Interaction):
        """Mostrar tienda (estructura base)"""
        
        embed = discord.Embed(
            title="Tienda del Servidor",
            description="Bienvenido a nuestra tienda. Los productos se cargarán aquí pronto.",
            color=COLORS['purple']
        )
        
        embed.add_field(
            name="Estado",
            value="🔧 En construcción",
            inline=False
        )
        
        embed.add_field(
            name="Características Próximas",
            value="• Catálogo de productos\n• Sistema de compra\n• Gestión de carrito",
            inline=False
        )
        
        embed.set_footer(text="Estructura lista para agregar funcionalidad en GitHub")
        
        await interaction.response.send_message(embed=embed)
    
    # ============== ESTRUCTURA PARA AGREGAR PRODUCTOS ==============
    # Aquí es donde irá la funcionalidad de compra
    # Ejemplo de estructura comentada:
    
    """
    @app_commands.command(name="comprar", description="Comprar un producto")
    @app_commands.describe(producto_id="ID del producto")
    async def comprar(self, interaction: discord.Interaction, producto_id: int):
        # TODO: Implementar lógica de compra
        # 1. Verificar que el producto existe
        # 2. Verificar fondos del usuario
        # 3. Procesar transacción
        # 4. Dar el producto al usuario
        pass
    
    @app_commands.command(name="mis_compras", description="Ver tus compras")
    async def mis_compras(self, interaction: discord.Interaction):
        # TODO: Mostrar historial de compras del usuario
        pass
    """

async def setup(bot):
    await bot.add_cog(ShopCog(bot))
