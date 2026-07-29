---
name: progreso
description: "Calcular y mostrar el progreso general en 4Geeks Academy: % de avance, proyectos completados vs pendientes, y desglose por cohorte."
allowed-tools: [exec]
---

# Progreso general en 4Geeks Academy

Usa esta skill cuando el usuario quiera saber su avance global en el curso: porcentaje completado, proyectos vs pendientes, desglose por cohorte, y calificación si está disponible.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- Token válido (usar skill `authenticate-4geeks` si hay duda)

## Endpoint

```
GET https://breathecode.herokuapp.com/v1/assignment/user/me/task?limit=100
```

## Flujo

1. Leer `BREATHECODE_TOKEN` de `~/.openclaw/.env`
2. Hacer GET a `/v1/assignment/user/me/task?limit=100` (primera página)
3. Si `count > 100`, hacer GET a `?limit=100&offset=100` (segunda página)
4. Combinar resultados y calcular:

### Cálculos

| Métrica | Fórmula |
|---|---|
| **% Global** | (DONE + APPROVED) / Total * 100 |
| **Proyectos completados** | PROJECT + (DONE o APPROVED) |
| **Proyectos pendientes** | PROJECT + PENDING |
| **Por cohorte** | Agrupar por cohort, calcular por cada uno |

### Formato de salida

```
📊 PROGRESO EN 4GEEKS ACADEMY
==============================

🎯 Total: 120/133 completadas (90%)

=== PROYECTOS ===
✅ Completados: 24
🔴 Pendientes: 2

=== POR COHORTE ===
• AI Engineering Introduction: 26/27 (96% ✅)
• Advanced personal assistants with Openclaw: 1/3 (33% 🔴)
• Backend development with Coding Agents: 0/3 (0% 🔴)
• Working with AI coding agents: 3/7 (43% ⏳)
• Coding Fundamentals with Typescript: 11/11 (100% ✅)
• Command Line, Git and Github: 5/5 (100% ✅)
• Frontend development with Coding Agents: 16/17 (94% ✅)
• Personal assistants with Openclaw: 11/11 (100% ✅)
• Web UI fundamentals with Tailwind: 15/15 (100% ✅)
• Coding fundamentals with Python: 0/1 (0% 🔴)

=== CALIFICACIONES ===
(Si la API devuelve notas, se muestran aquí.
Actualmente no hay calificaciones disponibles en la API.)
```

## Notas

- La API limita a 100 resultados por página
- Usar paginación con `offset` si `count > 100`
- Las calificaciones pueden no estar disponibles en la API de estudiantes
- Los estados posibles: PENDING, DONE, APPROVED, REJECTED