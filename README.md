# TechServ Backend — Etapa 0

API base con autenticación **JWT local** (sin Supabase), usuarios/roles y health check.

## Alcance (Etapa 0)

- FastAPI + PostgreSQL local (Docker Compose) + Redis
- Auth propia: **bcrypt** (contraseñas) + **python-jose** (JWT)
- Modelo `users` + `companies`
- Endpoints de auth: `POST /auth/register`, `POST /auth/login`
- Endpoints protegidos: `GET /health`, `GET /me`, CRUD usuarios (admin)
- CI con GitHub Actions
- Documentación OpenAPI en `/docs`

## Inicio rápido

```bash
cp .env.example .env
docker compose up -d db redis
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

## Autenticación JWT (frontend)

### 1. Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{"email": "admin@techserv.local", "password": "admin123"}
```

Respuesta:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 2. Usar el token

```typescript
const res = await fetch(`${API_URL}/api/v1/me`, {
  headers: { Authorization: `Bearer ${access_token}` },
})
```

### 3. Registro (cliente, técnico, etc. — no administrador)

```http
POST /api/v1/auth/register
{"email": "...", "password": "...", "full_name": "...", "role": "cliente"}
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `JWT_SECRET_KEY` | Clave para firmar JWT (generar una larga y aleatoria) |
| `JWT_EXPIRE_MINUTES` | Duración del token (default 60) |
| `DATABASE_URL` | PostgreSQL async (FastAPI) |
| `DATABASE_URL_SYNC` | PostgreSQL sync (Alembic) |

Generar secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/v1/health` | No | Health check |
| POST | `/api/v1/auth/register` | No | Registro |
| POST | `/api/v1/auth/login` | No | Login → JWT |
| GET | `/api/v1/me` | JWT | Usuario autenticado |
| GET | `/api/v1/users` | Admin | Listar usuarios |
| POST | `/api/v1/users` | Admin | Crear usuario (con password) |
| PATCH | `/api/v1/users/{id}` | Admin | Actualizar usuario |

## Crear el primer administrador

Con la API levantada, un admin existente puede crear otro vía `POST /users`, o insertar en SQL:

```sql
-- password: admin123 (generar hash con POST /auth/register de un supervisor primero, o usar /users como admin seed)
```

**Opción recomendada:** crear el primer admin con script o `POST /api/v1/users` después de un seed manual.

Seed rápido vía registro + SQL para cambiar rol, o usar este flujo en Swagger:

1. `POST /auth/register` con rol `supervisor`
2. En DB: `UPDATE users SET role = 'administrador' WHERE email = '...';`
3. Login y usar `POST /users` para el resto

## Roles

`cliente`, `tecnico`, `supervisor`, `administrador`, `area_administrativa`

## Tests

```bash
python -m pytest
```

## Documentación de diseño

- [Diagrama de clases](docs/diagrama-de-clases.md)
- [Diagrama E/R](docs/diagrama-er.md)
- [Diagrama de secuencias](docs/diagrama-secuencias.md)
- [Casos de uso](docs/diagrama-casos-de-uso.md)
- [Diagrama de actividades](docs/diagrama-actividades.md)

> **Nota:** Auth ya no usa Supabase. JWT y usuarios viven en PostgreSQL local.
