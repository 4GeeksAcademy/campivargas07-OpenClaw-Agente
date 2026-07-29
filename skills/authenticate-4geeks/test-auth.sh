#!/usr/bin/env bash
# Prueba de autenticación contra la API de 4Geeks Academy (BreatheCode).
# Requiere BREATHECODE_TOKEN en el entorno (~/.openclaw/.env).

set -euo pipefail

if [[ -z "${BREATHECODE_TOKEN:-}" ]]; then
  echo "ERROR: BREATHECODE_TOKEN no está definido en el entorno."
  echo "Ejecuta: curl -s -L -X POST https://breathecode.herokuapp.com/v1/auth/login/"
  echo "  -H 'Content-Type: application/json'"
  echo "  -d '{\"email\": \"tu@email.com\", \"password\": \"***\"}'"
  echo "y guarda el token en ~/.openclaw/.env como BREATHECODE_TOKEN=..."
  exit 1
fi

echo "🔐 Verificando autenticación con 4Geeks Academy..."
echo "Endpoint: GET https://breathecode.herokuapp.com/v1/admissions/user/me"
echo ""

response_file="$(mktemp)"
http_code="$(
  curl -sS -L -o "$response_file" -w "%{http_code}" \
    -H "Authorization: Token ${BREATHECODE_TOKEN}" \
    "https://breathecode.herokuapp.com/v1/admissions/user/me"
)"

body="$(cat "$response_file")"
rm -f "$response_file"

case "$http_code" in
  200)
    echo "✅ HTTP 200 — Token válido. Sesión activa."
    echo "$body" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'  Usuario: {d.get(\"first_name\",\"\")} {d.get(\"last_name\",\"\")}')
print(f'  Email: {d.get(\"email\",\"\")}')
print(f'  Cohortes: {len(d.get(\"cohorts\",[]))}')
print(f'  Cuenta creada: {d.get(\"date_joined\",\"\")[:10]}')
"
    exit 0
    ;;
  401)
    echo "❌ HTTP 401 — Token inválido o expirado."
    echo "   Necesitas iniciar sesión de nuevo para obtener un token fresco."
    exit 1
    ;;
  403)
    echo "⚠️  HTTP 403 — Token válido, pero falta academy_id."
    echo "   La sesión está activa aunque falte filtrar por academia."
    exit 0
    ;;
  *)
    echo "⚠️  HTTP $http_code — Respuesta inesperada."
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    exit 1
    ;;
esac