---
name: feedback-proyectos
description: "Extraer y resumir el feedback de proyectos calificados de 4Geeks: comentarios del evaluador, puntos clave de mejora y nota obtenida."
allowed-tools: [exec]
---

# Feedback de proyectos 4Geeks Academy

Usa esta skill cuando el usuario quiera ver el feedback de sus proyectos calificados, conocer los comentarios del evaluador, identificar áreas de mejora, o generar una lista de puntos clave para próximas entregas.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- Token válido (usar skill `authenticate-4geeks` si hay duda)

## Endpoint

```
GET https://breathecode.herokuapp.com/v1/assignment/user/me/task?task_type=PROJECT&limit=50
```

## Flujo

1. Leer `BREATHECODE_TOKEN` de `~/.openclaw/.env`
2. Hacer GET a `/v1/assignment/user/me/task?task_type=PROJECT&limit=50`
3. Filtrar proyectos con `revision_status` = APPROVED o PENDING
4. Para cada uno, extraer el feedback del campo `description`

## Interpretación

| Campo | Significado |
|---|---|
| `revision_status: APPROVED` | Proyecto calificado y aprobado |
| `revision_status: PENDING` | Pendiente de revisión |
| `description` | Feedback del evaluador (ahí van los comentarios) |
| `task_status: DONE` | Marca de completado |

Nota: La API no devuelve calificaciones numéricas. El feedback es cualitativo.

## Formato de salida

```
📋 FEEDBACK DE PROYECTOS
=========================

🏆 APROBADOS (23)

🔹 Build a Digital Postcard with HTML/CSS
   ⭐ Feedback: Excelente trabajo con el proyecto...
   🔧 Mejora: [identificada del feedback]

🔹 Mi proyecto X
   ⭐ Feedback: ...
   🔧 Mejora: ...

⏳ PENDIENTE DE REVISIÓN (1)

🔸 Enhacing development with agent skills
   ⚠️ Feedback: Entregaste el enlace incorrecto...
   📌 Acción requerida: Revisar y reentregar

=== PUNTOS CLAVE PARA MEJORAR ===
🔹 Trabajar en inglés (nombres de variables, commits, docs)
🔹 Implementar funcionalidades extra sugeridas (setTimeout, CSV export)
🔹 Mejorar UX/UI (iconos intuitivos modo claro/oscuro)
```

## Notas

- No hay calificaciones numéricas en la API — solo feedback cualitativo
- El feedback está en el campo `description` de cada tarea
- Los proyectos con `revision_status: PENDING` pueden tener feedback pendiente de leer
- Los puntos clave de mejora se extraen analizando el feedback del evaluador