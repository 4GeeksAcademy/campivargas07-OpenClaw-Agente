# SKILL_LOG.md — Skills de Integración con 4Geeks Academy

> Registro de skills creadas el 29 de julio de 2026 para gestionar el progreso académico de Carlos Vargas en 4Geeks Academy mediante la API de BreatheCode.

---

## 📦 Skill 1: authenticate-4geeks

**Propósito:** Validar el token de acceso contra la API de 4Geeks Academy y confirmar que la sesión está activa.

### 1. Solicitud en lenguaje natural

> "Crea una skill para validar mi autenticación. Debe tomar mi token de acceso, verificar que sea válido y comprobar que la sesión permanezca activa."

### 2. Skill creada

Se actualizó la skill existente `skills/authenticate-4geeks/` para que use la API de BreatheCode (`breathecode.herokuapp.com`) en lugar de `api.4geeks.io`. Incluye:

- Script `test-auth.sh` que lee `BREATHECODE_TOKEN` del entorno
- GET a `/v1/admissions/user/me` con header `Authorization: Token {token}`
- Interpretación de códigos: 200 → OK, 401 → inválido, 403 → OK pero sin academy

### 3. Prueba de funcionamiento

```
$ source ~/.openclaw/.env && bash skills/authenticate-4geeks/test-auth.sh

🔐 Verificando autenticación con 4Geeks Academy...
✅ HTTP 200 — Token válido. Sesión activa.
  Usuario: Carlos Vargas
  Email: campivargas@gmail.com
  Cohortes: 22
  Cuenta creada: 2026-04-27
```

---

## 📦 Skill 2: obtener-proyectos

**Propósito:** Consultar la API y listar todos los proyectos asignados con su nombre y estado actual.

### 1. Solicitud en lenguaje natural

> "Crea una skill llamada obtener_proyectos que consulte la API y me traiga la lista completa de proyectos que tengo asignados."

### 2. Skill creada

Se creó `skills/obtener-proyectos/SKILL.md` con:
- GET a `/v1/assignment/user/me/task?task_type=PROJECT&limit=50`
- Clasificación por estado: PENDING, DONE, APPROVED, REJECTED
- Formato de salida agrupado por estado y cohorte

### 3. Prueba de funcionamiento

```
📋 Tus proyectos en 4Geeks Academy

🔴 PENDIENTES (2)
  • My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress
  • Voice Command API - Talk to Your Task List

✅ COMPLETADOS (24)
  • Build a Digital Postcard with HTML/CSS ✅
  • Setting Up Your Personal AI Agent with OpenClaw ✅
  • ... (22 más)

Total: 26 proyectos
```

---

## 📦 Skill 3: pendientes

**Propósito:** Filtrar la lista para mostrar únicamente tareas pendientes (proyectos, ejercicios y lecciones), agrupadas por cohorte.

### 1. Solicitud en lenguaje natural

> "Necesito una skill que filtre mi lista de proyectos para mostrarme únicamente lo que tengo pendiente. Debe decirme de forma específica qué entregas o tareas me faltan por completar."

### 2. Skill creada

Se creó `skills/pendientes/SKILL.md` con:
- GET a `/v1/assignment/user/me/task?task_status=PENDING&limit=50`
- Agrupación por tipo: PROJECT, EXERCISE, LESSON
- Agrupación por cohorte dentro de cada tipo
- Fechas de creación como referencia

### 3. Prueba de funcionamiento

```
🔴 PENDIENTES — 25 tareas por completar

📦 PROYECTOS (2)
  • My 4Geeks Assistant
  • Voice Command API

📝 EJERCICIOS (21)
  [Working with AI coding agents] — 9 ejercicios
  [Backend development with Coding Agents] — 6 ejercicios
  [Advanced personal assistants with Openclaw] — 3 ejercicios
  ...

📖 LECCIONES (2)
  • Logical conditions in Python explained
  • Learning to program with Python
```

---

## 📦 Skill 4: progreso

**Propósito:** Calcular y mostrar un resumen global del curso: porcentaje de avance, proyectos completados vs. pendientes, desglose por cohorte, y calificación promedio si está disponible.

### 1. Solicitud en lenguaje natural

> "Crea una skill para ver mi progreso general en el curso. Debe calcular y mostrarme un resumen global: porcentaje total de avance, cantidad de proyectos completados vs. pendientes, y mi calificación promedio actual si está disponible."

### 2. Skill creada

Se creó `skills/progreso/SKILL.md` con:
- GET a `/v1/assignment/user/me/task?limit=100` con paginación (`offset=100`)
- Cálculo: (DONE + APPROVED) / total * 100
- Desglose por cohorte con porcentaje individual
- Estados: ✅ 100%, ⏳ 50-99%, 🔴 <50%

### 3. Prueba de funcionamiento

```
📊 PROGRESO EN 4GEEKS ACADEMY

🎯 Total: 108/133 completadas (81%)

=== PROYECTOS ===
✅ Completados: 24
🔴 Pendientes: 2

=== POR COHORTE ===
✅ Web UI fundamentals with Tailwind — 15/15 (100%)
✅ Personal assistants with Openclaw — 12/12 (100%)
✅ Command Line, Git and Github — 6/6 (100%)
✅ Coding Fundamentals with Typescript — 20/20 (100%)
⏳ AI Engineering Introduction — 26/27 (96%)
⏳ Frontend development with Coding Agents — 20/21 (95%)
🔴 Working with AI coding agents — 6/15 (40%)
🔴 Advanced personal assistants with Openclaw — 3/7 (43%)
🔴 Backend development with Coding Agents — 0/7 (0%)
🔴 Coding fundamentals with Python — 0/3 (0%)

=== CALIFICACIONES ===
No hay calificaciones disponibles en la API.
```

---

## 📦 Skill 5: deadlines

**Propósito:** Gestionar fechas límite para proyectos, guardarlas localmente y mostrar cuenta regresiva en días y horas.

### 1. Solicitud en lenguaje natural

> "Pon la fecha límite del Proyecto 1 para el 5 de agosto a las 11:59 PM"

> "Crea una skill para gestionar y asignar fechas límite a mis entregas de proyectos."

### 2. Skill creada

Se creó `skills/deadlines/SKILL.md` y `deadlines.json` con:
- Almacenamiento local en JSON (la API de BreatheCode no soporta `due_date` vía PUT)
- Cálculo de tiempo restante: días y horas hasta el deadline
- Detección de vencidos (🚨), urgentes (🔥 HOY), y próximos (⏳)
- Listado de proyectos sin deadline

### 3. Prueba de funcionamiento

```
⏰ DEADLINES DE PROYECTOS

=== CON DEADLINE ASIGNADO ===
📦 My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress
   ⏰ 05 Aug 2026 23:59
   ⏳ 7 días 17 horas restantes

📦 Voice Command API - Talk to Your Task List
   ⏰ 10 Aug 2026 23:59
   ⏳ 12 días 17 horas restantes

=== SIN DEADLINE (24 proyectos) ===
   ✅ Todos completados
```

---

## 📦 Skill 6: notificaciones-entrega

**Propósito:** Revisar diariamente los proyectos pendientes y enviar alerta a Telegram si un deadline está próximo o hay entregas críticas.

### 1. Solicitud en lenguaje natural

> "Crea una skill de notificaciones proactivas para mis entregas. Debe revisar diariamente mis proyectos pendientes y enviarme una alerta prioritaria si una fecha límite está a menos de 48 horas de vencer."

### 2. Skill creada + Cron

Se creó `skills/notificaciones-entrega/SKILL.md` y un cron diario con:

| Nivel | Condición | Acción |
|---|---|---|
| 🚨 CRÍTICA | Deadline ≤ 48h | Alerta urgente a Telegram |
| ⏳ Preventivo | Deadline ≤ 7 días | Aviso de días restantes |
| ⚠️ Recordatorio | Pendiente sin deadline | Sugerir asignar fecha |
| ✅ Tranquilidad | Todo en orden | "No hay urgencias" |

**Cron configurado:**
- Horario: `0 9 * * *` (9:00 AM CDMX)
- Entrega: Telegram a `chat_id 5969598217`
- Timeout: 60 segundos

### 3. Prueba de funcionamiento

```
🚨 NOTIFICACIONES DE ENTREGA — 29 Jul 2026

✅ Todo tranquilo
  No hay proyectos con deadline próximo.

📊 RESUMEN
  Proyectos con deadline: 2
  🔴 Críticos: 0
  ⏳ Próximos: 0
  ✅ Sin urgencia: 2
```

---

## 📦 Skill 7: feedback-proyectos

**Propósito:** Extraer y resumir el feedback de los evaluadores en proyectos calificados, resaltar comentarios principales y generar puntos clave de mejora.

### 1. Solicitud en lenguaje natural

> "Crea una skill para extraer y resumir el feedback de mis proyectos en estado 'calificado'. Debe mostrarme la nota obtenida, resaltar los comentarios principales del evaluador y generar una lista de puntos clave para mejorar."

### 2. Skill creada

Se creó `skills/feedback-proyectos/SKILL.md` con:
- GET a `/v1/assignment/user/me/task?task_type=PROJECT&limit=50`
- Filtro por `revision_status: APPROVED` / `PENDING`
- Extracción de feedback del campo `description`
- Generación automática de puntos clave de mejora

### 3. Prueba de funcionamiento

```
📋 FEEDBACK DE PROYECTOS

🏆 APROBADOS (23)
  🔹 Build a Digital Postcard with HTML/CSS
     ⭐ Excelente trabajo...
  🔹 Setting Up Your Personal AI Agent with OpenClaw
     ⭐ Muy bien el agente con ojo de Halcón Carlos!
  ...

⏳ PENDIENTE DE REVISIÓN (1)
  ⚠️ Enhacing development with agent skills
     Feedback: "has entregado el enlace incorrecto..."

=== PUNTOS CLAVE PARA MEJORAR ===
🎯 1. Trabajar en inglés (variables, commits, docs)
🎯 2. Implementar retos sugeridos (CSV, setTimeout, iconos)
🎯 3. Verificar enlaces de entrega antes de entregar
🎯 4. Seguir con la calidad actual — bien valorada
```

---

## Resumen General

| # | Skill | Archivo | ¿Qué hace? |
|---|---|---|---|
| 1 | 🔐 `authenticate-4geeks` | `skills/authenticate-4geeks/` | Valida token contra API |
| 2 | 📋 `obtener-proyectos` | `skills/obtener-proyectos/` | Lista proyectos con estado |
| 3 | 🔴 `pendientes` | `skills/pendientes/` | Filtra solo tareas sin completar |
| 4 | 📊 `progreso` | `skills/progreso/` | Resumen global 81% |
| 5 | ⏰ `deadlines` | `skills/deadlines/` + `deadlines.json` | Fechas límite con countdown |
| 6 | 🚨 `notificaciones-entrega` | `skills/notificaciones-entrega/` + cron | Alertas diarias a Telegram |
| 7 | 📋 `feedback-proyectos` | `skills/feedback-proyectos/` | Feedback y puntos de mejora |

**Tokens utilizados:**
- `BREATHECODE_TOKEN` — guardado en `~/.openclaw/.env` (fuera del repo)
- `TELEGRAM_TOKEN` — guardado en `openclaw.json`
- Base URL: `https://breathecode.herokuapp.com`
- Academy ID: 6 (4Geeks Madrid)

**Fecha de creación:** 29 de julio de 2026
**Autor:** agentclaw 🕵️ + Carlos Vargas  