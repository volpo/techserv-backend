# TechServ Backend — Etapa 0

API base con autenticación JWT (Supabase Auth), usuarios/roles y health check.

## Alcance (Etapa 0)

- FastAPI + PostgreSQL + Redis (Docker Compose)
- Validación JWT con AuthX en el backend
- Modelo `users` + `companies`
- Endpoints: `GET /health`, `GET /me`, CRUD usuarios (solo administrador)
- CI con GitHub Actions
- Documentación OpenAPI en `/docs`

## Inicio rápido

```bash
cp .env.example .env
docker compose up -d db redis
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/v1/health` | No | Health check |
| GET | `/api/v1/me` | JWT | Usuario autenticado |
| GET | `/api/v1/users` | Admin | Listar usuarios |
| POST | `/api/v1/users` | Admin | Crear usuario |
| PATCH | `/api/v1/users/{id}` | Admin | Actualizar usuario |

## Roles

`cliente`, `tecnico`, `supervisor`, `administrador`, `area_administrativa`

## Tests

```bash
pytest
```

## Documentación de diseño

- [Diagrama de clases](docs/diagrama-de-clases.md)
- [Diagrama E/R](docs/diagrama-er.md)
- [Diagrama de secuencias](docs/diagrama-secuencias.md)
- [Casos de uso](docs/diagrama-casos-de-uso.md)
- [Diagrama de actividades](docs/diagrama-actividades.md)
