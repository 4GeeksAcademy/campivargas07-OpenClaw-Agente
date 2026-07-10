# Notas de Conexión — API Key LiteLLM

## Problema
- Al enviar mensajes desde Telegram, OpenClaw respondía con error 401.
- Los logs mostraban: `Invalid proxy server token passed` apuntando a LiteLLM.
- El gateway estaba activo y Telegram configuraba correctamente el bot, pero las respuestas fallaban.

## Causa Raíz
- El archivo `openclaw.json` tenía configurado el `baseUrl` del proveedor LiteLLM (`https://llm.4geeks.ai/v1`) pero **no tenía definido el `apiKey`**.
- Sin API key, el proxy de 4Geeks rechazaba cualquier solicitud de inferencia.

## Decisión de Configuración
- Se agregó la entrada `models.providers.litellm.apiKey` con el token proporcionado por 4Geeks (`sk-nbY…ApGg`).
- El API key se guarda directamente en `openclaw.json` (no como variable de entorno).
- Se reinició el gateway (`systemctl --user restart openclaw-gateway.service`) para aplicar el cambio.

## Lecciones
- `openclaw onboard` no siempre restaura todas las claves de API — hay que verificar manualmente.
- El comando `openclaw config set` escribe cambios en `openclaw.json` pero requiere reinicio del gateway.
- Revisar `models.providers.<proveedor>.apiKey` debe ser parte del checklist post-onboarding.