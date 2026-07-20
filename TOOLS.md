# TOOLS.md - Notas y Conexiones de agentclaw

Skills definen _cómo_ funcionan las herramientas. Este archivo es para _tus_ detalles específicos.

---

## 📦 Conexiones Composio

Composio conecta apps externas para que pueda interactuar con ellas. Se usan a través de mcporter.

### ✅ ClickUp 📋
**Estado:** Activa (alias: default)

**Para qué usarla:** Gestión de proyectos, tareas y seguimiento.

**Herramientas principales:**
- `CLICKUP_GET_TASKS` — Obtener tareas de una lista
- `CLICKUP_CREATE_TASK` — Crear tarea nueva
- `CLICKUP_UPDATE_TASK` — Actualizar tarea existente

**Ejemplos de uso real:**
- "Crea una tarea en ClickUp para investigar APIs de IA"
- "Muéstrame las tareas pendientes de esta semana"
- "Actualiza el estado de la tarea X a 'En Progreso'"

**Parámetros clave al crear tarea:**
| Campo | Requerido | Tipo | Notas |
|---|---|---|---|
| `list_id` | 🔴 Sí | string | ID de la lista donde crear |
| `name` | 🔴 Sí | string | Nombre visible de la tarea |
| `description` | 🟢 Opcional | string | Descripción detallada |
| `priority` | 🟢 Opcional | integer | 1=Urgente, 2=Alta, 3=Normal, 4=Baja |
| `status` | 🟢 Opcional | string | Estado (ej: "To Do", "In Progress") |
| `due_date` | 🟢 Opcional | integer | Unix timestamp en milisegundos |
| `assignees` | 🟢 Opcional | array | IDs de usuarios asignados |
| `tags` | 🟢 Opcional | array | Etiquetas para categorizar |

---

### ✅ Google Calendar 📅
**Estado:** Activa (alias: default)

**Para qué usarla:** Gestión de calendario, bloques de tiempo, recordatorios.

**Herramientas principales:**
- `GOOGLECALENDAR_CREATE_EVENT` — Crear evento nuevo
- `GOOGLECALENDAR_FIND_EVENT` — Buscar eventos existentes
- `GOOGLECALENDAR_FIND_FREE_SLOTS` — Encontrar espacios libres
- `GOOGLECALENDAR_DELETE_EVENT` — Eliminar evento

**Ejemplos de uso real:**
- "Agenda una reunión mañana a las 10 AM por 1 hora"
- "¿Qué tengo en el calendario para hoy?"
- "Encuentra espacios libres el viernes en la tarde"
- "Crea un evento para el partido de MLB del viernes"

**Parámetros clave al crear evento:**
| Campo | Requerido | Tipo | Default | Notas |
|---|---|---|---|---|
| `start_datetime` | 🔴 Sí | string | — | ISO 8601: YYYY-MM-DDTHH:MM:SS |
| `summary` | 🟢 Opcional | string | — | Título del evento |
| `event_duration_hour` | 🟢 Opcional | integer | 1 | Duración en horas |
| `event_duration_minutes` | 🟢 Opcional | integer | 0 | Minutos extra (0-59) |
| `calendar_id` | 🟢 Opcional | string | "primary" | Calendario a usar |
| `timezone` | 🟢 Opcional | string | "America/Mexico_City" | Zona horaria |
| `attendees` | 🟢 Opcional | array | [] | Emails de invitados |
| `description` | 🟢 Opcional | string | — | Descripción del evento |
| `location` | 🟢 Opcional | string | — | Ubicación física |
| `create_meeting_room` | 🟢 Opcional | boolean | True | Crea Google Meet link |
| `recurrence` | 🟢 Opcional | array | — | Reglas RRULE para eventos recurrentes |
| `visibility` | 🟢 Opcional | string | "default" | "default", "public", "private" |

---

### ✅ Google Drive ☁️
**Estado:** Activa (alias: default)

**Para qué usarla:** Búsqueda y gestión de archivos en la nube.

**Herramientas principales:**
- `GOOGLEDRIVE_FIND_FILE` — Buscar archivos y carpetas

**Ejemplos de uso real:**
- "Busca el archivo de diseño del proyecto X en Drive"
- "Encuentra todas las presentaciones que compartí este mes"
- "Busca la carpeta de entregas de la escuela"

**Parámetros clave:**
| Campo | Requerido | Tipo | Notas |
|---|---|---|---|
| `q` | 🟢 Opcional | string | Query tipo Google: `name contains 'MLB'` |
| `folder_id` | 🟢 Opcional | string | Limitar búsqueda a carpeta específica |
| `pageSize` | 🟢 Opcional | integer | Resultados por página (default: 100) |
| `orderBy` | 🟢 Opcional | string | Orden: `modifiedTime desc`, `name` |
| `spaces` | 🟢 Opcional | string | "drive", "appDataFolder", "photos" |

---

### ⏳ Gmail 📧
**Estado:** Iniciando (alias: personal) — pendiente de autorización

**Para qué usarla:** Gestión de correo, automatización de respuestas.

**Herramientas principales (cuando esté activa):**
- `GMAIL_SEND_EMAIL` — Enviar correos
- `GMAIL_FETCH_EMAILS` — Leer bandeja de entrada
- `GMAIL_SEARCH_EMAILS` — Buscar correos específicos

**Ejemplos futuros:**
- "¿Hay correos urgentes sin leer?"
- "Envía un email a [cliente] con el resumen del proyecto"
- "Busca el correo de confirmación de [servicio]"

---

### ⏳ Slack 💬
**Estado:** Iniciando (alias: default, work) — pendiente de autorización

**Para qué usarla:** Comunicación laboral, búsqueda de mensajes, notificaciones.

**Herramientas principales (cuando esté activa):**
- `SLACK_SEND_MESSAGE` — Enviar mensaje a canal/DM
- `SLACK_SEARCH_MESSAGES` — Buscar mensajes históricos

**Ejemplos futuros:**
- "Envía un mensaje al canal #general diciendo X"
- "Busca el mensaje de [persona] sobre [tema]"

---

### ✅ SeatGeek 🎟️
**Estado:** Sin autenticación requerida (API pública)

**Para qué usarla:** Buscar eventos deportivos y de entretenimiento.

**Herramientas principales:**
- `SEAT_GEEK_SEARCH_EVENTS` — Buscar eventos (MLB, conciertos, etc.)

**Ejemplos de uso real:**
- "¿Qué juegos de MLB hay hoy?"
- "Busca conciertos en mi ciudad este fin de semana"

---

### ✅ Composio Search 🔍
**Estado:** Sin autenticación requerida

**Para qué usarla:** Búsqueda web general.

**Herramientas principales:**
- `COMPOSIO_SEARCH_WEB` — Buscar información en internet

---

## 🚀 Auto-Push a GitHub

Cada modificación a archivos del workspace se sube automáticamente a:
- **Repo:** `4GeeksAcademy/campivargas07-OpenClaw-Agente`
- **Branch:** `main`
- **Origen:** `git@github.com:4GeeksAcademy/campivargas07-OpenClaw-Agente.git`

**Archivos NO trackeados:** `openclaw-workspace-state.json`

---

## ⚾ Script MLB

- **Archivo:** `openclaw-connection/mlb.py`
- **Uso:** `python3 mlb.py [YYYYMMDD]`
- **Fuente:** ESPN API pública
- **Muestra:** Partidos, horarios, canales de TV, récords, odds