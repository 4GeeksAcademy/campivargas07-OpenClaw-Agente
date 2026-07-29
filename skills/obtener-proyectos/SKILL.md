---
name: obtener-proyectos
description: "Consultar la API de 4Geeks Academy y listar proyectos asignados con nombre, estado y cohorte."
allowed-tools: [exec]
---

# Obtener proyectos de 4Geeks Academy

Usa esta skill cuando el usuario pida ver sus proyectos de 4Geeks Academy, consultar el estado de sus entregas, o listar proyectos pendientes.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- Token válido (usar skill `authenticate-4geeks` si hay duda)

## Endpoint

```
GET https://breathecode.herokuapp.com/v1/assignment/user/me/task
```

## Parámetros útiles

| Parámetro | Valor | Efecto |
|---|---|---|
| `task_type` | `PROJECT` | Solo proyectos (excluye ejercicios, lecciones, quizzes) |
| `task_status` | `PENDING`, `DONE`, `APPROVED`, `REJECTED` | Filtrar por estado |
| `cohort` | id del cohorte | Filtrar por cohorte específico |
| `limit` | número | Máximo de resultados por página |
| `offset` | número | Paginación |

## Flujo

1. Leer `BREATHECODE_TOKEN` de `~/.openclaw/.env`
2. Hacer GET a `/v1/assignment/user/me/task?task_type=PROJECT&limit=50`
3. Procesar la respuesta y mostrar:

### Formato de salida

```
📋 Tus proyectos en 4Geeks Academy:

=== PENDIENTES (2) ===
  • My 4Geeks Assistant
    Cohorte: Advanced personal assistants with Openclaw
    Creado: 2026-07-15

=== COMPLETADOS (24) ===
  • Build a Digital Postcard with HTML/CSS ✅
    Cohorte: AI Engineering Introduction
```

## Interpretación de estados

| Estado | Significado |
|---|---|
| **PENDING** | Pendiente — no entregado aún |
| **DONE** | Completado — entregado |
| **APPROVED** | Aprobado — calificado y aceptado |
| **REJECTED** | Rechazado — requiere correcciones |

## Notas

- La API devuelve hasta 100 resultados por página
- Usar `limit` + `offset` para paginar si hay más de 100 proyectos
- El token se pasa en header: `Authorization: Token {token}`
- No se necesita academy_id para este endpoint