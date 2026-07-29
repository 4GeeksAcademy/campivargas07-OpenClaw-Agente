---
name: pendientes
description: "Filtrar tareas pendientes de 4Geeks Academy: proyectos, ejercicios y lecciones no completados, con fechas límite si existen."
allowed-tools: [exec]
---

# Tareas pendientes de 4Geeks Academy

Usa esta skill cuando el usuario quiera ver solo lo que le falta por hacer en 4Geeks Academy: proyectos sin entregar, ejercicios pendientes, lecciones sin completar, con fechas límite si las hay.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- Token válido (usar skill `authenticate-4geeks` si hay duda)

## Endpoint

```
GET https://breathecode.herokuapp.com/v1/assignment/user/me/task
```

## Parámetros

| Parámetro | Valor | Efecto |
|---|---|---|
| `task_status` | `PENDING` | Solo pendientes |
| `limit` | `50` | Suficiente para la mayoría de casos |

## Flujo

1. Leer `BREATHECODE_TOKEN` de `~/.openclaw/.env`
2. Hacer GET a `/v1/assignment/user/me/task?task_status=PENDING&limit=50`
3. Agrupar resultados por tipo: PROJECT, EXERCISE, LESSON, QUIZ
4. Mostrar en orden de prioridad: proyectos primero, luego ejercicios, luego lecciones

### Formato de salida

```
🔴 PENDIENTES — 25 tareas por completar

=== PROYECTOS (2) ===
  • My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress
    Cohorte: Advanced personal assistants with Openclaw
    ⏰ Sin fecha límite

  • Voice Command API - Talk to Your Task List
    Cohorte: Backend development with Coding Agents
    ⏰ Sin fecha límite

=== EJERCICIOS (21) ===
  • Using Coding Agents
    Cohorte: Working with AI coding agents
    Creado: 2026-07-03

  • Introduction to Generative AI for Beginners
    Cohorte: Working with AI coding agents

  ...

=== LECCIONES (2) ===
  • Logical conditions in Python explained
    Cohorte: Coding fundamentals with Python
```

## Interpretación de estados

Todos los items tienen status `PENDING`. No hay fechas límite configuradas en la mayoría de los casos.

## Notas

- La API no siempre devuelve `due_date` para cada tarea
- Si no hay `due_date`, se muestra la fecha de creación como referencia
- Agrupar por cohorte ayuda a priorizar: cohortes más recientes primero