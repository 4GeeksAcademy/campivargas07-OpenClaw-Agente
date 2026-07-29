---
name: deadlines
description: "Gestionar fechas límite de proyectos de 4Geeks: definir, actualizar y consultar deadlines con cuenta regresiva."
allowed-tools: [exec, write]
---

# Gestión de deadlines para proyectos 4Geeks

Usa esta skill cuando el usuario quiera asignar una fecha límite a un proyecto, consultar cuánto tiempo le queda, o actualizar un deadline existente.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- Token válido (usar skill `authenticate-4geeks` si hay duda)
- Los deadlines se guardan en `~/.openclaw/workspace/deadlines.json`

## Archivo de deadlines

Los deadlines se almacenan en un archivo local (`deadlines.json`) porque la API de 4Geeks no soporta asignar fechas límite. Formato:

```json
{
  "953310": {
    "title": "My 4Geeks Assistant",
    "due_date": "2026-08-05T23:59:59Z",
    "created_at": "2026-07-29T06:00:00Z"
  }
}
```

## Comandos

### Asignar deadline a un proyecto

```
Asigna deadline al proyecto "Voice Command API" para el 10 de agosto
```

Flujo:
1. Buscar el proyecto por nombre en la API (`task_type=PROJECT`)
2. Obtener su ID
3. Preguntar al usuario la fecha y hora deseada
4. Guardar en `deadlines.json` con formato ISO 8601
5. Calcular y mostrar tiempo restante

### Consultar deadlines

```
Muéstrame mis deadlines
```

Flujo:
1. Leer `deadlines.json`
2. Para cada deadline, calcular tiempo restante
3. Mostrar proyectos con deadline y los que no tienen

### Actualizar deadline

```
Cambia el deadline de "My 4Geeks Assistant" al 15 de agosto
```

Flujo:
1. Buscar en `deadlines.json`
2. Actualizar la fecha
3. Recalcular tiempo restante

## Formato de salida

```
⏰  DEADLINES DE PROYECTOS
===========================

=== CON DEADLINE ASIGNADO ===
📦 My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress
   ⏰ 05 Ago 2026 23:59
   ⏳ 7 días 14 horas restantes

📦 Voice Command API - Talk to Your Task List
   ⏰ 10 Ago 2026 23:59
   ⏳ 12 días 5 horas restantes

=== SIN DEADLINE (24 proyectos) ===
   • Build a Digital Postcard with HTML/CSS ✅
   • Setting Up Your Personal AI Agent with OpenClaw ✅
   ...
```

## Cuenta regresiva

Calcular días y horas restantes:

```python
from datetime import datetime
due_dt = datetime.fromisoformat(due_date.replace('Z','+00:00'))
now = datetime.now()
remaining = (due_dt - now).days
hours = int((due_dt - now).seconds / 3600)
```

## Notas

- Los deadlines se guardan localmente, no en la API de 4Geeks
- Si el deadline ya pasó, mostrar "🚨 VENCIDO — hace X días"
- Los proyectos ya completados pueden tener deadline histórico
- El archivo `deadlines.json` está en el workspace y se sube a GitHub