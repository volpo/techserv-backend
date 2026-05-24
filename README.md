# TechServ Backend — Etapa 0

API base con autenticación JWT (Supabase Auth), usuarios/roles y health check.

## Alcance (Etapa 0)

- FastAPI + PostgreSQL + Redis (Docker Compose)
- Validación JWT de Supabase en el backend
- Modelo `users` + `companies` (sync con `auth.users` de Supabase)
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

## Autenticación JWT (frontend)

```typescript
const { data: { session } } = await supabase.auth.getSession()
const token = session?.access_token

const res = await fetch(`${API_URL}/api/v1/me`, {
  headers: { Authorization: `Bearer ${token}` },
})
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

## Supabase — sync de usuarios

Al registrarse en Supabase Auth, crear el perfil en `users` con el mismo UUID:

```sql
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email, full_name, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
    COALESCE(NEW.raw_user_meta_data->>'role', 'cliente')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

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
