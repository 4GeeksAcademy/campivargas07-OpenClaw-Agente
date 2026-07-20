---
name: clickup-to-calendar
description: >-
  Convierte tareas pendientes de ClickUp en bloques de tiempo en Google Calendar.
  Usa cuando el usuario pida agendar tareas, bloquear tiempo para pendientes,
  sincronizar ClickUp con Calendar, o reservar horas para deep work.
---

# ClickUp → Calendar

Lee tareas de ClickUp sin bloque de tiempo y crea eventos en Google Calendar.

## Prerrequisitos

- Composio activo vía `mcporter` (ver [TOOLS.md](../../TOOLS.md))
- ClickUp y Google Calendar conectados
- Timezone: `America/Mexico_City` (UTC-6)

## Flujo

### 1. Obtener tareas pendientes

```bash
mcporter call composio.COMPOSIO_SEARCH_TOOLS \
  queries='[{"use_case": "get pending tasks from ClickUp list"}]' \
  session='{"generate_id": true}'
```

Luego ejecutar con `COMPOSIO_MULTI_EXECUTE_TOOL`:

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "CLICKUP_GET_TASKS", "arguments": {"list_id": "LIST_ID", "include_closed": false}}]' \
  sync_response_to_workbench=false
```

**Filtros a aplicar en la respuesta:**
- Estado ≠ completado/cerrado
- Sin evento de Calendar ya vinculado (buscar por nombre en descripción o tag `calendar-blocked`)
- Priorizar: vencimiento esta semana → prioridad urgente/alta → sin fecha

Si el usuario no da `list_id`, preguntar o usar el workspace/lista documentado en TOOLS.md.

### 2. Revisar calendario existente

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLECALENDAR_FIND_EVENT", "arguments": {"calendar_id": "primary", "time_min": "YYYY-MM-DDT00:00:00", "time_max": "YYYY-MM-DDT23:59:59"}}]' \
  sync_response_to_workbench=false
```

### 3. Encontrar slots libres

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLECALENDAR_FIND_FREE_SLOTS", "arguments": {"calendar_id": "primary", "time_min": "YYYY-MM-DDT09:00:00", "time_max": "YYYY-MM-DDT18:00:00", "timezone": "America/Mexico_City"}}]' \
  sync_response_to_workbench=false
```

**Defaults de duración:**
| Prioridad ClickUp | Duración |
|---|---|
| Urgente (1) | 90 min |
| Alta (2) | 60 min |
| Normal (3) | 45 min |
| Baja (4) | 30 min |

**Preferencias de horario (si el usuario no especifica):**
- Deep work / diseño / código → mañanas (9:00–12:00)
- Admin / seguimiento → tardes (14:00–17:00)

### 4. Proponer y confirmar

Mostrar preview antes de crear:

```
📋 Tareas a bloquear (3):

1. [P1] Diseño VB Parrilla — Mié 10:00–11:30
2. [P2] Investigar APIs IA — Jue 09:00–10:00
3. [P3] Revisar brief cliente — Vie 15:00–15:45

¿Creo estos bloques en Calendar?
```

**Siempre pedir confirmación** antes de crear eventos (AGENTS.md).

### 5. Crear eventos

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLECALENDAR_CREATE_EVENT", "arguments": {
    "calendar_id": "primary",
    "summary": "🎯 Nombre de tarea",
    "start_datetime": "YYYY-MM-DDTHH:MM:SS",
    "event_duration_hour": 1,
    "event_duration_minutes": 30,
    "timezone": "America/Mexico_City",
    "description": "ClickUp: https://app.clickup.com/t/TASK_ID\nPrioridad: Alta\n---\nBloqueado por agentclaw"
  }}]' \
  sync_response_to_workbench=false
```

### 6. Confirmar resultado

```
✅ 3 bloques creados en Calendar

📌 Diseño VB Parrilla — Mié 10:00–11:30
   🔗 https://app.clickup.com/t/86ajejh1y

📌 Investigar APIs IA — Jue 09:00–10:00
   🔗 https://app.clickup.com/t/...
```

## Reglas

- No solapar eventos existentes
- Máximo 5 bloques por ejecución (evitar saturar el calendario)
- Si no hay slots libres, sugerir mover o acortar duración
- Prefijo `🎯` en título para distinguir bloques de trabajo vs reuniones

## Triggers

- "bloquea mis tareas de ClickUp"
- "agenda pendientes en el calendario"
- "reserva tiempo para deep work"
- "sincroniza ClickUp con Calendar"
