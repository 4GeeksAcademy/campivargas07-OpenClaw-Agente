---
name: weekly-plan
description: >-
  Genera un plan semanal priorizado en Google Doc y crea eventos clave en Calendar.
  Usa cuando el usuario pida plan de semana, organizar la semana, priorizar
  objetivos semanales, o preparar el lunes.
---

# Plan de Semana

Convierte objetivos semanales en un Doc estructurado y bloques de tiempo en Calendar.

## Prerrequisitos

- Composio: ClickUp, Calendar, Drive/Docs vía `mcporter`
- Timezone: `America/Mexico_City`
- Confirmación antes de crear eventos (AGENTS.md)

## Configuración (primera vez)

Guardar en TOOLS.md:

```markdown
### 📅 Planes Semanales
- **Carpeta Drive:** [folder_id o nombre]
- **Formato título:** Plan Semana YYYY-Www
```

## Flujo

### 1. Recopilar input

Pedir o inferir:
- **Objetivos** de la semana (lista del usuario)
- **Enfoque:** estudio / clientes / mixto
- **Restricciones:** días no disponibles, horarios preferidos
- **Incluir ClickUp:** sí/no (default: sí — traer pendientes con vencimiento esta semana)

### 2. Contexto existente

**Calendar de la semana:**

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

**ClickUp pendientes (si aplica):**

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "CLICKUP_GET_TASKS", "arguments": {"list_id": "LIST_ID", "include_closed": false}}]' \
  sync_response_to_workbench=false
```

### 3. Generar plan priorizado

**Estructura del Doc:**

```markdown
# Plan Semana 2026-W30 (21–27 Jul)

## Objetivo de la semana
[1 frase que resuma el foco]

## P1 — Crítico (hacer sí o sí)
- [ ] Objetivo 1 — estimado Xh — deadline día
- [ ] Objetivo 2 — ...

## P2 — Importante (si hay tiempo)
- [ ] ...

## P3 — Nice to have
- [ ] ...

## Distribución por día

### Lunes
- AM: [bloque] — [tarea]
- PM: [bloque] — [tarea]

### Martes
...

## Checklist de cierre (viernes)
- [ ] ¿Completé P1?
- [ ] ¿Actualicé ClickUp?
- [ ] ¿Registré aprendizajes en diario?
```

**Reglas de priorización:**
- Deadlines de ClickUp → P1 automático
- Entregas de clientes → P1
- Estudio/inglés → mínimo 2 bloques en la semana (P2)
- No más de 3 ítems en P1

### 4. Crear Google Doc

```bash
mcporter call composio.COMPOSIO_SEARCH_TOOLS \
  queries='[{"use_case": "create Google Doc with title and content"}]' \
  session='{"generate_id": true}'
```

Título: `Plan Semana YYYY-Www`

### 5. Proponer eventos de Calendar

Seleccionar 3–5 bloques críticos de P1:

```
📅 Eventos propuestos:

1. Lun 09:00–11:00 — Deep work: Módulo Python
2. Mié 10:00–12:00 — Entrega diseño VB
3. Jue 16:00–17:00 — Sesión inglés
4. Vie 09:00–10:00 — Review semanal + ClickUp

¿Creo estos bloques?
```

**Siempre pedir confirmación.**

### 6. Crear eventos

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLECALENDAR_CREATE_EVENT", "arguments": {
    "calendar_id": "primary",
    "summary": "📋 Deep work: Módulo Python",
    "start_datetime": "YYYY-MM-DDTHH:MM:SS",
    "event_duration_hour": 2,
    "event_duration_minutes": 0,
    "timezone": "America/Mexico_City",
    "description": "Plan Semana YYYY-Www — P1\nDoc: [link]"
  }}]' \
  sync_response_to_workbench=false
```

Verificar que no solapen eventos existentes (paso 2).

### 7. Guardar referencia en memoria

Añadir a `memory/YYYY-MM-DD.md`:

```markdown
## Plan Semana YYYY-Www
- Doc: [link]
- P1: [lista corta]
- Eventos creados: [n]
```

### 8. Confirmar

```
✅ Plan de semana listo

📄 Plan Semana 2026-W30
   🔗 [Abrir en Google Docs](...)

📅 4 bloques creados en Calendar
   • Lun 09:00 — Deep work: Módulo Python
   • Mié 10:00 — Entrega diseño VB
   • ...

Buena semana, Carlos 🕵️
```

## Reglas

- Ejecutar domingo noche o lunes mañana (sugerir al usuario)
- No crear más de 5 eventos por plan
- Respetar restricciones del usuario ("martes no disponible")
- Si la semana ya tiene muchos eventos, reducir bloques propuestos

## Triggers

- "plan de semana"
- "organiza mi semana"
- "qué hago esta semana"
- "prepara el lunes"
- "prioriza mis objetivos"
