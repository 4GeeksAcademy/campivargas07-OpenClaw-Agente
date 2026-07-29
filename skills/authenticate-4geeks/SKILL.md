---
name: authenticate-4geeks
description: "Validar token de 4Geeks Academy (BreatheCode): verificar vigencia, checar sesión activa, y devolver resultado claro."
allowed-tools: [exec]
---

# Autenticación 4Geeks Academy (BreatheCode)

Usa esta skill cuando el usuario pida validar su sesión en 4Geeks Academy, verificar si el token sigue activo, o autenticarse en la API de estudiantes (BreatheCode).

## Prerrequisitos

- `BREATHECODE_TOKEN` definido en `~/.openclaw/.env`
- El token se obtiene mediante `POST /v1/auth/login/` con email y contraseña
- **Nunca hardcodear el token** en scripts, SKILL.md ni en el chat

## Base URL

```
https://breathecode.herokuapp.com
```

## Autenticación

Header requerido en todas las llamadas:

```http
Authorization: Token {BREATHECODE_TOKEN}
```

## Verificar autenticación

```bash
bash skills/authenticate-4geeks/test-auth.sh
```

## Interpretación de respuestas

| Código | Significado | Acción |
|---|---|---|
| **200** | Token válido | Sesión activa. Mostrar datos del usuario. |
| **401** | Token inválido o expirado | Pedir nuevo login. |
| **403** | Token válido, falta header Academy | Sesión activa (error de filtro, no de auth). |

## Endpoints de verificación

### GET /v1/admissions/user/me

Sin parámetros. Devuelve datos del usuario, email, cohortes.

### GET /v1/admissions/academy/cohort/me

Requiere `Academy: {id}` en header o `?academy={id}` en query.
Devuelve cohortes del estudiante filtrados por academia.

## Flujo completo

1. Leer `BREATHECODE_TOKEN` de `~/.openclaw/.env`
2. Hacer GET a `/v1/admissions/user/me`
3. Si **200 OK** → mostrar:
   - Nombre completo
   - Email
   - Fecha de creación de cuenta
   - Número de cohortes
   - Si el token expira pronto (< 24h), advertir
4. Si **401** → avisar que el token expiró y pedir credenciales para renovarlo
5. Si **403** → igual considerar como sesión activa (el 403 es por falta de academy_id, no por token malo)

## Solución de problemas

1. **401 Unauthorized**: el token expiró o fue revocado. Hacer POST a `/v1/auth/login/` con email y password.
2. **Variable vacía**: revisar que `BREATHECODE_TOKEN` esté en `~/.openclaw/.env`
3. **Conexión fallida**: verificar que la URL base sea correcta (`breathecode.herokuapp.com`)