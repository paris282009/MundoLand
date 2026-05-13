# 🤖 MundoLand Bot - Actualización Multi-Servidor

## ¿Qué es esto?

Esta es la **versión actualizada** de tu bot que ahora:
- ✅ Funciona en **múltiples servidores**
- ✅ Los comandos se **actualizan correctamente** en Discord
- ✅ Es **completamente público** (cualquiera puede añadirlo)

## 📁 Archivos que necesitas

### Principales
- **`main.py`** - Código del bot actualizado (REEMPLAZA el tuyo)
- **`.env.example`** - Variables de entorno de referencia

### Ayuda & Documentación
- **`INICIO_AQUI.txt`** - 👈 Empieza aquí (5 min lectura)
- **`RESUMEN_RAPIDO.txt`** - Resumen visual de los pasos
- **`ACTUALIZACION_GUIA.md`** - Guía completa y detallada
- **`EXPLICACION_TECNICA.md`** - Cómo funciona técnicamente

### Herramientas
- **`sync_commands.py`** - Script para sincronizar comandos manualmente

## 🚀 Inicio rápido (30 segundos)

1. Descarga `main.py` y reemplaza el tuyo
2. Lee `INICIO_AQUI.txt` (tiene los pasos paso-a-paso)
3. Sigue las 6 fases (toma ~30 min total)

## 🔑 Variables de Entorno

### En Render (Producción)
```
DISCORD_TOKEN=tu_token_aqui
ENVIRONMENT=production
```

### Local (Desarrollo - Opcional)
```
DISCORD_TOKEN=tu_token_aqui
ENVIRONMENT=development
DEV_GUILD_ID=123456789
```

## 📊 Antes vs Después

### Antes ❌
- Bot solo en 1 servidor
- Comandos antiguos no desaparecían
- No se podía añadir a otros servidores

### Después ✅
- Bot en infinitos servidores
- Comandos se actualizan correctamente
- Sincronización automática en Render

## ⏱️ Tiempos de sincronización

- **Desarrollo (Local)**: ~5 segundos (instantáneo)
- **Producción (Render)**: Hasta 1 hora (es normal de Discord)

## 📖 ¿Cuál archivo leer?

- **Soy nuevo en esto**: Lee `INICIO_AQUI.txt`
- **Quiero más detalles**: Lee `ACTUALIZACION_GUIA.md`
- **Me interesa la técnica**: Lee `EXPLICACION_TECNICA.md`
- **Solo quiero los pasos**: Lee `RESUMEN_RAPIDO.txt`

## ✅ Checklist final

- [ ] Descargué `main.py`
- [ ] Actualicé mi repositorio GitHub
- [ ] Configuré variables en Render
- [ ] Hice deploy en Render
- [ ] Esperé ~1 hora
- [ ] Probé en otro servidor

## 🆘 Problemas?

### Los comandos tardan mucho
→ Es normal (hasta 1 hora de Discord). Espera.

### Los comandos no aparecen en otro servidor
→ Espera 1 hora más o usa ENVIRONMENT=development localmente

### El bot no conecta
→ Verifica DISCORD_TOKEN es correcto

### Veo errores de cogs
→ Verifica que los archivos estén en `./cogs/`

## 💡 Extras

Para probar cambios **instantáneamente** en desarrollo:
1. Cambia a `ENVIRONMENT=development` + `DEV_GUILD_ID`
2. Los cambios aparecen en ~5 segundos
3. (Solo funciona en ese servidor de prueba)

## 📝 Licencia

Misma que tu proyecto original.

---

**¿Preguntas? Lee `INICIO_AQUI.txt` primero** 👈
