# Back-End-2026

Proyecto Django con dos módulos CRUD principales:

- **Agenda**: administración de contactos con búsqueda.
- **Inventario**: administración de productos.

## Requisitos

- Python 3.11+ (recomendado)
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Copia `/home/runner/work/Back-End-2026/Back-End-2026/.env.example` a `.env` y ajusta valores:

```env
SECRET_KEY=change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_HOST=localhost
DB_PORT=5432
DB_NAME=back_end_2026
DB_USER=postgres
DB_PASSWORD=postgres
```

Notas:

- Si defines todas las variables `DB_*`, el proyecto usa PostgreSQL.
- Si faltan variables `DB_*`, el proyecto usa SQLite local (`db.sqlite3`) para desarrollo.

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Ejecutar servidor

```bash
python manage.py runserver
```

## Ejecutar pruebas

```bash
python manage.py test Agenda inventario
```

## Rutas disponibles

### Agenda

- `GET /contactos/` listado + búsqueda (`?q=texto`)
- `GET|POST /contactos/nuevo/` crear contacto
- `GET /contactos/<id>/` detalle
- `GET|POST /contactos/<id>/editar/` actualizar
- `GET|POST /contactos/<id>/eliminar/` eliminar
- `GET /contactos/filtro/` acceso alternativo al listado filtrado

### Inventario

- `GET /productos/` listado
- `GET|POST /productos/nuevo/` crear producto
- `GET /productos/<id>/` detalle
- `GET|POST /productos/<id>/editar/` actualizar
- `GET|POST /productos/<id>/eliminar/` eliminar

## Funcionalidad del Caso 3

- Corrección de vistas CRUD para asegurar `HttpResponse` en todos los caminos.
- Re-render de formularios inválidos en Agenda e Inventario con errores de validación.
- Validación de modelo para impedir `precio` y `stock` negativos en productos.
- Configuración segura de `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` por entorno.
- Cobertura de pruebas para CRUD completo, validaciones y búsqueda en Agenda.
