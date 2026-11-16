# Back-End-2026

## Desarrollo local

1. Copia `.env.example` a `.env`, conserva las credenciales de PostgreSQL y genera una clave local con:

   ```powershell
   .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

   Pega el resultado en `SECRET_KEY` de `.env`. No compartas ni subas `.env`.

2. Desde esta carpeta, inicia Django:

   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver
   ```

## API desplegada

- Base de la API: https://back-end-2026.vercel.app/api/
- Contactos: https://back-end-2026.vercel.app/api/contactos/
- Obtener token: `POST /api/token/`
- Renovar token: `POST /api/token/refresh/`

La API de contactos requiere `Authorization: Bearer <token>`. Las credenciales de PostgreSQL y `SECRET_KEY` deben configurarse como variables de entorno en Vercel. Para producción, usa `DEBUG=False`, define `ALLOWED_HOSTS` con el host exacto de la API y configura `CORS_ALLOWED_ORIGINS` con el origen exacto del frontend desplegado. Cambiar `SECRET_KEY` invalida los JWT emitidos previamente.
