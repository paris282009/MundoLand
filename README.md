# Bot de Discord - MundoLand 2.0

Bot multifuncional para Discord con sistema modular de Cogs.

## Instalación

1. **Clonar el repositorio**
```bash
git clone tu-repo
cd tu-repo
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env y agregar tu TOKEN de Discord
```

4. **Ejecutar el bot**
```bash
python main.py
```

## Estructura del Proyecto

```
.
├── main.py                 # Archivo principal del bot
├── webserver.py            # Servidor web para mantener vivo
├── config.py               # Configuración centralizada
├── database.py             # Manejo de base de datos SQLite
├── requirements.txt        # Dependencias
├── .env.example            # Variables de entorno de ejemplo
├── .env                    # Variables de entorno (no subir a GitHub)
├── bot_data.db             # Base de datos (se crea automáticamente)
└── cogs/                   # Módulos del bot
    ├── utility.py          # Encuestas, /say, /say-embed, /limpiar
    ├── information.py      # /datos, /estado, /avatar, /userinfo
    ├── integrations.py     # /stats, /tiktok, /youtube
    ├── server_system.py    # /serveradd, /serveredit, /servidores, /add-boton
    └── shop.py             # /tienda (estructura)
```

## Comandos Disponibles

### Utilidad
- `/encuesta <pregunta> <opciones>` - Crear votación
- `/say <mensaje>` - Enviar mensaje personalizado (admin)
- `/say_embed <titulo> <descripcion>` - Enviar embed personalizado (admin)
- `/limpiar <cantidad>` - Borrar mensajes (admin)

### Información
- `/datos` - Info del servidor
- `/estado` - Estado del servidor
- `/avatar [usuario]` - Ver avatar
- `/userinfo [usuario]` - Info del usuario

### Integraciones
- `/stats <usuario>` - Stats de Minecraft (NameMC)
- `/tiktok_agregar <usuario> <url>` - Configurar TikTok (owner)
- `/tiktok` - Ver TikTok del servidor
- `/youtube_agregar <canal> <url>` - Configurar YouTube (owner)
- `/youtube` - Ver YouTube del servidor

### Sistema de Servidores
- `/serveradd <nombre> <ip> <puerto> [descripcion]` - Registrar servidor
- `/serveredit <id> [nuevo_nombre] [descripcion]` - Editar servidor
- `/servidores` - Listar todos los servidores
- `/add_boton <message_id> <nombre> <url>` - Agregar botón a mensaje (admin)

### Tienda
- `/tienda` - Ver tienda (en construcción)

## Permisos Restringidos

Los siguientes comandos solo funcionan en ciertos niveles:

| Comando | Restricción |
|---------|------------|
| `/say` | Administrador |
| `/say_embed` | Administrador |
| `/limpiar` | Administrador |
| `/tiktok_agregar` | Dueño del servidor |
| `/youtube_agregar` | Dueño del servidor |
| `/add_boton` | Administrador |

## Base de Datos

El bot usa SQLite (`bot_data.db`) para almacenar:
- Servidores registrados
- Enlaces de redes sociales
- Botones agregados a mensajes
- Encuestas

Las tablas se crean automáticamente al iniciar el bot.

## Despliegue

### Replit
1. Conectar repositorio GitHub
2. Agregar TOKEN en Secrets
3. Ejecutar `python main.py`

### Railway/Render
1. Conectar repositorio GitHub
2. Agregar variable `TOKEN` en variables de entorno
3. Command: `python main.py`

### Otros hosts
El webserver incorporado mantiene el bot activo respondiendo a peticiones HTTP en puerto 5000.

## Agregar Nuevos Comandos

1. Crear nuevo archivo en `cogs/`
```python
from discord.ext import commands
from discord import app_commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ejemplo", description="Comando de ejemplo")
    async def ejemplo(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hola!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

2. El bot cargará automáticamente el cog.

## Troubleshooting

**El bot no responde**: Verifica que el TOKEN sea correcto en `.env`

**Comandos no aparecen**: Espera 1-2 minutos para que se sincronicen los slash commands

**Error de base de datos**: Borra `bot_data.db` y reinicia el bot

## Licencia

Todos los derechos reservados.

## Soporte

Para reportar bugs o sugerir características, abre un issue en GitHub.
