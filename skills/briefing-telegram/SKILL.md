---
name: briefing-telegram
description: >-
  Envía un briefing diario por Telegram con eventos de Calendar, tareas prioritarias
  de ClickUp, noticias de IA (modelos, desarrollo, imágenes, ads, agentes) y partidos MLB.
  Usa cuando el usuario pida briefing, qué tengo hoy, resumen del día, noticias de IA,
  o en heartbeats/cron matutinos.
---

# Briefing Matutino por Telegram

Resume el día en un mensaje corto y accionable para Telegram.

## Prerrequisitos

- Composio (Calendar, ClickUp, Search) vía `mcporter`
- Skill `telegram-messaging` para envío
- Timezone: `America/Mexico_City`
- Script MLB: `python3 openclaw-connection/mlb.py [YYYYMMDD]`

## Flujo

### 1. Determinar fecha

- Sin argumento → hoy en timezone México
- Con argumento → fecha específica

### 2. Obtener eventos de Calendar (próximas 24h)

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLECALENDAR_FIND_EVENT", "arguments": {
    "calendar_id": "primary",
    "time_min": "YYYY-MM-DDT00:00:00",
    "time_max": "YYYY-MM-DDT23:59:59",
    "timezone": "America/Mexico_City"
  }}]' \
  sync_response_to_workbench=false
```

Ordenar por hora. Mostrar solo eventos futuros si es tarde.

### 3. Obtener tareas ClickUp prioritarias

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "CLICKUP_GET_TASKS", "arguments": {"list_id": "LIST_ID", "include_closed": false}}]' \
  sync_response_to_workbench=false
```

**Seleccionar top 3–5:**
1. Vencen hoy o mañana
2. Prioridad urgente/alta
3. Asignadas a Carlos

### 4. MLB (opcional)

```bash
python3 openclaw-connection/mlb.py $(date +%Y%m%d)
```

Incluir solo si hay juegos. Omitir si offseason o All-Star break sin partidos.

### 5. Noticias de IA (siempre incluir)

Buscar noticias recientes (últimas 24–48h) con `COMPOSIO_SEARCH_WEB`. Ejecutar 2–3 búsquedas en paralelo para cubrir los temas de Carlos:

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[
    {"tool_slug": "COMPOSIO_SEARCH_WEB", "arguments": {"query": "AI news today new models LLM releases"}},
    {"tool_slug": "COMPOSIO_SEARCH_WEB", "arguments": {"query": "AI development tools agents automation news today"}},
    {"tool_slug": "COMPOSIO_SEARCH_WEB", "arguments": {"query": "AI image generation video ads marketing news today"}}
  ]' \
  sync_response_to_workbench=false
```

**Temas a cubrir (rotar según lo más relevante del día):**
| Categoría | Qué buscar |
|---|---|
| Modelos | Nuevos LLMs, fine-tunes, benchmarks, open source |
| Desarrollo | Frameworks, APIs, agentes, MCP, SDKs, coding AI |
| Imágenes/video | Generación, edición, avatares, video AI |
| Ads/marketing | AI en publicidad, creativos, copy, automatización |
| Herramientas | Lanzamientos, updates, integraciones |

**Seleccionar top 3–5 noticias:**
1. Publicadas en las últimas 48h (preferir 24h)
2. Relevantes para AI Engineering, diseño o marketing de Carlos
3. Sin duplicados entre búsquedas
4. Priorizar fuentes confiables (blogs oficiales, TechCrunch, The Verge, Hugging Face, OpenAI, Anthropic, Google AI, etc.)

**Formato por noticia:** título corto + 1 línea de contexto. Link opcional si cabe en Telegram.

### 6. Componer mensaje

**Formato (sin tablas, bullets simples):**

```
🕵️ Briefing — Lunes 20 Jul

📅 HOY
• 10:00 — Reunión cliente VB (1h)
• 14:00 — 🎯 Diseño parrilla agosto (90min)
• 18:00 — Sesión inglés (45min)

📋 PENDIENTES
• [P1] Entregar diseño VB — vence hoy 6PM
• [P2] Investigar APIs de IA
• [P3] Revisar brief Aleatica

🤖 IA HOY
• OpenAI lanza GPT-5 mini — modelo más barato para agentes
• Google actualiza Gemini con generación de video nativa
• Midjourney v7 mejora consistencia de personajes en ads
• Cursor anuncia soporte MCP para skills custom
• Meta lanza modelo open source para imágenes publicitarias

⚾ MLB
• Yankees vs Red Sox — 7:05 PM ET, ESPN

Buen día, Carlos 🕵️
```

**Reglas de formato:**
- Máximo 7 ítems accionables en Calendario + Pendientes
- Sección 🤖 IA: 3–5 noticias siempre (es el diferenciador del briefing)
- Sin tablas Markdown (Telegram)
- Tono directo (SOUL.md)
- Omitir sección vacía (no poner "📋 PENDIENTES" si no hay tareas; 🤖 IA siempre va)

### 7. Enviar por Telegram

Usar skill `telegram-messaging`:

```bash
clawlink_call_tool --tool "telegram_send_message" \
  --params '{"chat_id": "CHAT_ID", "text": "MENSAJE_DEL_BRIEFING"}'
```

**Chat ID:** usar el de la sesión activa (`5969598217` para Carlos) o el configurado en TOOLS.md.

### 8. Confirmar en chat

Si se ejecuta desde webchat, confirmar brevemente: "Briefing enviado a Telegram ✅"

## Heartbeat / Cron

Para automatizar, añadir a `HEARTBEAT.md`:

```markdown
- [ ] Briefing matutino (lun–vie, 8:00 AM CDMX) → skill briefing-telegram
```

O configurar cron de OpenClaw para las 8:00 AM `America/Mexico_City`.

## Reglas

- No enviar entre 23:00–08:00 CDMX salvo que Carlos lo pida
- Si no hay nada urgente: mensaje corto ("Día tranquilo — sin eventos ni deadlines hoy")
- No incluir info privada de otros usuarios

## Triggers

- "briefing"
- "qué tengo hoy"
- "resumen del día"
- "dame mi agenda"
- "noticias de IA"
- "qué hay nuevo en AI"
