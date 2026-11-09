#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
: "${API_USERNAME:?Define API_USERNAME con un usuario Django}"
: "${API_PASSWORD:?Define API_PASSWORD con la contraseña Django}"

login_payload=$(python -c 'import json, os; print(json.dumps({"username": os.environ["API_USERNAME"], "password": os.environ["API_PASSWORD"]}))')
tokens=$(curl --fail-with-body --silent --show-error \
  -H "Content-Type: application/json" \
  -d "$login_payload" \
  "$API_BASE_URL/api/token/")
access_token=$(python -c 'import json, sys; print(json.load(sys.stdin)["access"])' <<<"$tokens")
refresh_token=$(python -c 'import json, sys; print(json.load(sys.stdin)["refresh"])' <<<"$tokens")

echo "1. Acceso sin token (se espera HTTP 401)"
curl --silent --show-error --output /dev/null --write-out "HTTP %{http_code}\n" \
  "$API_BASE_URL/api/contactos/"

echo "2. Listar contactos con JWT"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $access_token" \
  "$API_BASE_URL/api/contactos/"
echo

echo "3. Crear contacto"
created=$(curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Contacto de prueba API","telefono":"+56 9 1234 5678","correo":"prueba@example.com","direccion":"Santiago"}' \
  "$API_BASE_URL/api/contactos/")
printf '%s\n' "$created"
contact_id=$(python -c 'import json, sys; print(json.load(sys.stdin)["id"])' <<<"$created")

echo "4. Actualizar contacto $contact_id"
curl --fail-with-body --silent --show-error \
  -X PUT \
  -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Contacto actualizado API","telefono":"+56 9 8765 4321","correo":"actualizado@example.com","direccion":"Valparaiso"}' \
  "$API_BASE_URL/api/contactos/$contact_id/"
echo

echo "5. Consultar contacto $contact_id"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $access_token" \
  "$API_BASE_URL/api/contactos/$contact_id/"
echo

echo "6. Eliminar contacto $contact_id"
curl --fail-with-body --silent --show-error \
  -X DELETE \
  -H "Authorization: Bearer $access_token" \
  --output /dev/null --write-out "HTTP %{http_code}\n" \
  "$API_BASE_URL/api/contactos/$contact_id/"

echo "7. Renovar token"
curl --fail-with-body --silent --show-error \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$refresh_token\"}" \
  "$API_BASE_URL/api/token/refresh/"
echo
