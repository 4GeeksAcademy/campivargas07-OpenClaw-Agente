---
name: notificaciones-entrega
description: "Revisar diariamente proyectos pendientes con deadline y alertar si faltan menos de 48h o hay entregas críticas."
allowed-tools: [exec]
---

# Notificaciones proactivas de entregas

Usa esta skill cuando el usuario necesite alertas automáticas sobre fechas límite próximas. Se ejecuta diariamente vía cron y envía notificaciones a Telegram si hay urgencias.

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- `deadlines.json` en el workspace con los deadlines configurados
- Canal Telegram activo para recibir notificaciones

## Flujo de revisión diaria

1. Leer `deadlines.json` del workspace
2. Consultar API de 4Geeks para proyectos pendientes (`task_type=PROJECT&task_status=PENDING`)
3. Para cada proyecto con deadline:
   - Calcular tiempo restante vs. ahora (UTC)
   - Si faltan **≤ 48 horas** → ALERTA ROJA 🚨
   - Si faltan **≤ 7 días** → AVISO PREVENTIVO ⏳
4. Para proyectos pendientes sin deadline:
   - Marcar como "sin fecha asignada" → aviso para que el usuario asigne una
5. Enviar resumen al usuario por Telegram

## Lógica de alertas

| Condición | Tipo | Mensaje |
|---|---|---|
| Deadline ≤ 48h | 🚨 **CRÍTICA** | "¡El proyecto X vence en menos de 48 horas!" |
| Deadline ≤ 7 días | ⏳ **Preventivo** | "Te quedan N días para entregar el proyecto X" |
| Proyecto pendiente sin deadline | ⚠️ **Recordatorio** | "Tienes el proyecto X pendiente sin fecha límite" |
| Todo en orden | ✅ **Tranquilidad** | "No hay urgencias. Tus proyectos están bajo control." |

## Formato de salida (Telegram)

```
🚨 ALERTA DE ENTREGAS
======================

🔴 CRÍTICO — Vence pronto:
  📦 My 4Geeks Assistant — Teaching OpenClaw
     ⏰ 05 Ago — FALTAN 28 HORAS 🚨
     ⚠️ Prioridad: ALTA (proyecto principal)

⏳ PRÓXIMOS — Vencen esta semana:
  📦 Voice Command API
     ⏰ 10 Ago — Faltan 12 días

✅ AL DÍA:
  24 proyectos completados sin novedad
```

## Instalación

La skill se ejecuta automáticamente mediante un cron diario a las 9:00 AM (hora México):

```bash
openclaw cron add \
  --name "notificaciones-entrega" \
  --description "Revisión diaria de deadlines próximos" \
  --cron "0 9 * * *" \
  --tz "America/Mexico_City" \
  --channel telegram \
  --to "5969598217" \
  --message "Ejecuta la skill notificaciones-entrega para hoy" \
  --timeout-seconds 60 \
  --announce \
  --expect-final
```

## Notas

- Las alertas solo se envían si hay proyectos con deadline ≤ 7 días
- Si no hay urgencias, se envía un mensaje corto de "todo tranquilo"
- Los proyectos completados (DONE) se ignoran
- Los deadlines se gestionan con la skill `deadlines`