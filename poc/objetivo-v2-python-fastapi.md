---
version: "2.0"
project:
  name: "user-management-api"
  title: "API de Gerenciamento de Usuários"
  type: "backend-api"
  domain: "programming"
  language: "python"

created_at: "2026-04-27"
created_by: "yves_marinho"

generation:
  profiles_auto_detect: true
  validate_on_save: true
  generate_spec_on_change: false

validation:
  level: "strict"
  fail_on_warning: false
  require_p0: true
  require_p1: false
---

# 🎯 Objetivo: API de Gerenciamento de Usuários

## 1️⃣ O que este projeto faz?

**Em uma frase**: API REST assíncrona para gerenciar usuários (CRUD completo + autenticação JWT), construída com FastAPI e PostgreSQL, seguindo padrões async-first e type-safe.

**Componentes principais**:
- **API HTTP**: Endpoints RESTful (`/api/v1/users`, `/api/v1/auth`)
- **Autenticação**: JWT com refresh tokens via OAuth2
- **Persistência**: PostgreSQL com SQLAlchemy async ORM
- **Validação**: Pydantic v2 schemas para request/response
- **Testes**: pytest-asyncio com AsyncClient (100% coverage nos endpoints)

**Stack técnico**:
- Python >=3.11 + FastAPI >=0.115 + uvicorn (ASGI server)
- PostgreSQL 16 + asyncpg (driver async)
- SQLAlchemy 2.0 (async mode) + Alembic (migrations)
- pydantic-settings (configuração via .env)
- uv (gerenciador de pacotes rápido)

---

## 2️⃣ Qual problema resolve?

### Problema Atual

Muitos sistemas internos ainda usam autenticação básica (username/password em headers) ou sessões server-side, resultando em:

- **Segurança fraca**: Credenciais em plaintext, sem hash adequado (MD5/SHA1 deprecated)
- **Escalabilidade limitada**: Sessões em memória impedem deploy horizontal
- **UX ruim**: Sem refresh tokens → usuário precisa fazer login a cada hora
- **Zero auditoria**: Não há log de quem criou/modificou/deletou usuários
- **Acoplamento forte**: Lógica de autenticação misturada com lógica de negócio

### Impacto Medido

**Métrica** | **Sistema Legado** | **Esta API** | **Δ**
--- | --- | --- | ---
Tempo de login | 800-1200ms (sessão server) | <100ms (JWT stateless) | **-90%**
Taxa de erro login | 12% (timeout sessão) | <1% (refresh token) | **-92%**
Escalabilidade | 1 instância (sessões) | N instâncias (stateless) | **+∞**
Tempo de deploy | 15 min (restart sessões) | <30s (zero downtime) | **-97%**
Cobertura de testes | 30% (manual) | >90% (pytest async) | **+200%**

### Audiência Afetada

1. **Desenvolvedores Frontend** (5 pessoas) — Precisam de API consistente para autenticação
2. **Admins de Sistema** (2 pessoas) — Precisam auditar ações de usuários
3. **DevOps** (3 pessoas) — Precisam deploy horizontal sem sessões compartilhadas
4. **Usuários Finais** (200+ pessoas) — Precisam login rápido e que não expire a cada hora

---

## 3️⃣ Escopo do Projeto

### Incluído ✅

**Autenticação JWT**
- POST `/api/v1/auth/register` — Criar conta (email, password, nome)
- POST `/api/v1/auth/login` — Login (retorna access_token + refresh_token)
- POST `/api/v1/auth/refresh` — Renovar access_token via refresh_token
- POST `/api/v1/auth/logout` — Invalidar refresh_token (blacklist)

**CRUD de Usuários**
- GET `/api/v1/users` — Listar usuários (paginação, filtros, search)
- GET `/api/v1/users/{id}` — Buscar usuário por ID
- POST `/api/v1/users` — Criar novo usuário (admin only)
- PATCH `/api/v1/users/{id}` — Atualizar dados (self ou admin)
- DELETE `/api/v1/users/{id}` — Soft delete (admin only)

**Auditoria**
- Tabela `audit_logs` com: user_id, action, resource, timestamp, ip_address
- GET `/api/v1/audit` — Listar logs (admin only, filtros por user/action/data)

**Infraestrutura**
- Dockerfile multistage (builder com uv sync + runtime não-root)
- docker-compose.yml (app + postgres:16 + redis:7 para cache)
- Alembic migrations (versionamento de schema)
- GitHub Actions CI (pytest + ruff lint + bandit security + pip-audit)

### Excluído ❌

- **Recuperação de senha** (email) — Feature futura (requer SMTP)
- **Autenticação social** (Google, GitHub) — Feature futura
- **Multi-tenancy** — Fora de escopo (single tenant apenas)
- **Rate limiting** — Feature futura (usar nginx ou Cloudflare)
- **WebSockets** (real-time) — Fora de escopo desta API REST
- **Admin UI** — Separado (frontend consome esta API)
- **Background jobs** (Celery) — Não necessário para este MVP

### Fora de Escopo ⚠️

- Integração com LDAP/Active Directory (autenticação externa)
- Criptografia de campos sensíveis (além de passwords)
- Conformidade LGPD completa (requer DPO, implementar em fase 2)
- Deploy em produção (apenas estrutura, não infra real)

---

## 4️⃣ Restrições e Requisitos Não-Funcionais

### Performance

- **Latência API**: p95 <200ms para endpoints CRUD, p99 <500ms
- **Latência Auth**: Login <100ms (sem bcrypt lento — usar argon2)
- **Throughput**: Suportar 100 req/s sustentado (single instance)
- **Database**: Queries <50ms (índices em email, created_at, is_active)

### Escalabilidade

- **Stateless**: Zero sessões em memória (apenas JWT em headers)
- **Horizontal scaling**: N instâncias atrás de load balancer
- **Connection pool**: SQLAlchemy pool_size=10, max_overflow=20
- **Cache**: Redis para user lookups frequentes (TTL 5min)

### Segurança

- **Password hashing**: argon2id (não bcrypt/sha256)
- **JWT**: HS256 (secret de 256 bits), access_token TTL 15min, refresh_token TTL 7 dias
- **HTTPS only**: Enforce HTTPS em produção (redirect HTTP → HTTPS)
- **CORS**: Whitelist explícita de origens permitidas (não `*`)
- **Input validation**: Pydantic valida TODOS inputs (email format, password strength)
- **SQL injection**: Proteção via SQLAlchemy ORM (não raw SQL)
- **Rate limiting**: Por IP via nginx (futuro — não nesta API)

### Disponibilidade

- **Uptime SLO**: 99.5% (43 min downtime/mês max) — não critical, mas importante
- **Health checks**: GET `/api/health` (sem autenticação) verifica DB + Redis
- **Graceful shutdown**: SIGTERM handler finaliza requests in-flight antes de parar
- **Migrations**: Alembic com rollback testado (down migrations obrigatórias)

### Observabilidade

- **Logs estruturados**: JSON format com correlation_id, user_id, endpoint, status_code
- **Metrics**: Prometheus metrics via `/metrics` endpoint (request_duration, db_query_time)
- **Tracing**: OpenTelemetry (futuro — não MVP)
- **Error tracking**: Sentry para exceptions não tratadas (produção apenas)

### Compatibilidade

- **Python**: >=3.11 (obrigatório para async improvements)
- **FastAPI**: >=0.115 (lifespan context manager)
- **PostgreSQL**: 16 (asyncpg driver)
- **Docker**: Imagem base python:3.11-slim-bookworm
- **Browsers**: API apenas (frontend consome), mas CORS permite Chrome/Firefox/Safari

---

## 5️⃣ Regras de Negócio

### Regra #1: Registro de Usuários (Self-Registration)

**Cenário**: Usuário cria conta pela primeira vez

**Validações**:
1. **Email**:
   - ✅ Formato válido (regex RFC 5322)
   - ✅ Único no sistema (não pode duplicar)
   - ✅ Domínio permitido (opcional: whitelist `@empresa.com`)
   - ❌ Emails temporários bloqueados (`mailinator.com`, `guerrillamail.com`)

2. **Password**:
   - ✅ Mínimo 8 caracteres
   - ✅ Contém: 1 maiúscula, 1 minúscula, 1 número, 1 especial
   - ❌ Não pode ser senha comum (`password123`, `admin`, etc — usar lista zxcvbn)
   - ❌ Não pode conter nome ou email do usuário

3. **Nome**:
   - ✅ Mínimo 2 caracteres, máximo 100
   - ✅ Apenas letras, espaços, hífens (não números)

**Output esperado**:
```json
{
  "id": "uuid-v4",
  "email": "user@example.com",
  "name": "João Silva",
  "role": "user",
  "is_active": true,
  "created_at": "2026-04-27T14:32:00Z"
}
```

**Regra de auditoria**:
- ✅ Log em `audit_logs`: action="user.register", resource="user:{id}", ip_address

---

### Regra #2: Autenticação JWT (Login)

**Cenário**: Usuário faz login com email + password

**Fluxo**:
1. Verifica se email existe → se não: HTTP 401 "Invalid credentials"
2. Verifica se usuário está ativo (`is_active=true`) → se não: HTTP 403 "Account disabled"
3. Compara password hash (argon2) → se incorreto: HTTP 401 "Invalid credentials"
4. Gera `access_token` (TTL 15min) + `refresh_token` (TTL 7 dias)
5. Salva `refresh_token` em tabela `refresh_tokens` (user_id, token_hash, expires_at)
6. Retorna ambos tokens + user info

**Output esperado**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "a1b2c3d4e5f6...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "João Silva",
    "role": "user"
  }
}
```

**Regras de segurança**:
- ⚠️ **Rate limiting**: Máximo 5 tentativas de login por IP a cada 15min (futuro — via nginx)
- ⚠️ **Timing attack**: Response time igual para email inválido vs password incorreto
- ✅ **Audit log**: action="auth.login", success=true/false, ip_address

---

### Regra #3: Autorização (Roles & Permissions)

**Cenário**: Endpoint requer role específica (ex: DELETE user → admin only)

**Roles definidas**:
1. **user** (padrão): Pode ler próprios dados, atualizar próprio perfil
2. **admin**: Pode CRUD completo em usuários, ler audit logs

**Tabela de permissões**:

| Endpoint | user | admin |
|----------|------|-------|
| GET `/api/v1/users` | ✅ (apenas self) | ✅ (todos) |
| GET `/api/v1/users/{id}` | ✅ (apenas self) | ✅ (qualquer) |
| POST `/api/v1/users` | ❌ | ✅ |
| PATCH `/api/v1/users/{id}` | ✅ (apenas self) | ✅ (qualquer) |
| DELETE `/api/v1/users/{id}` | ❌ | ✅ |
| GET `/api/v1/audit` | ❌ | ✅ |

**Validação**:
- ✅ Extrai `user_id` e `role` do JWT (claim `sub` e `role`)
- ✅ Se endpoint requer admin → verifica `role == "admin"` → se não: HTTP 403 Forbidden
- ✅ Se endpoint permite self → verifica `user_id == {id}` → se não: HTTP 403 Forbidden

**Regra especial — Soft delete**:
- DELETE `/api/v1/users/{id}` não remove do banco (apenas `is_active = false`)
- Permite recuperação posterior se necessário
- Hard delete apenas via script admin (não exposto na API)

---

### Regra #4: Paginação e Filtros (List Users)

**Cenário**: GET `/api/v1/users?page=2&size=20&search=silva&role=admin&is_active=true`

**Parâmetros de query**:
- `page` (int, default=1): Página atual (1-indexed)
- `size` (int, default=20, max=100): Itens por página
- `search` (string, opcional): Busca em name e email (case-insensitive)
- `role` (enum: user|admin, opcional): Filtro por role
- `is_active` (bool, opcional): Filtro por status ativo
- `sort_by` (enum: created_at|email|name, default=created_at): Campo para ordenação
- `order` (enum: asc|desc, default=desc): Direção da ordenação

**Output esperado**:
```json
{
  "items": [
    {"id": "uuid1", "email": "silva@example.com", "name": "João Silva", ...},
    {"id": "uuid2", "email": "maria.silva@example.com", "name": "Maria Silva", ...}
  ],
  "total": 42,
  "page": 2,
  "size": 20,
  "pages": 3
}
```

**Validações**:
- ✅ `size` limitado a max 100 (prevenir DOS com `?size=999999`)
- ✅ Se `page` > `pages` → retorna lista vazia (não erro 404)
- ✅ `search` usa `ILIKE` no PostgreSQL (case-insensitive) com índice GIN

---

### Regra #5: Refresh Token Rotation

**Cenário**: POST `/api/v1/auth/refresh` com refresh_token no body

**Fluxo seguro (rotation)**:
1. Valida refresh_token (verifica hash em tabela `refresh_tokens`)
2. Verifica se não expirou (`expires_at > now()`)
3. **Invalida token antigo** (delete ou marca `used=true`)
4. Gera **novo access_token** (TTL 15min)
5. Gera **novo refresh_token** (TTL 7 dias) e salva no DB
6. Retorna ambos novos tokens

**Por que rotation?**
- ⚠️ Previne replay attacks (token antigo não pode ser reutilizado)
- ⚠️ Se token vazou, expira em 7 dias automaticamente
- ✅ Se refresh_token usado 2x → alerta de segurança (possível roubo)

**Output esperado**:
```json
{
  "access_token": "novo-jwt...",
  "refresh_token": "novo-refresh...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Regra de auditoria**:
- ✅ Log em `audit_logs`: action="auth.refresh", user_id, old_token_id, new_token_id

---

## 6️⃣ Estrutura de Pastas

```
user-management-api/
├── src/
│   ├── main.py                      # FastAPI app factory com lifespan
│   │                                # Registra routers, configura CORS, middleware
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py                # APIRouter principal (agrega v1)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py              # POST /register, /login, /refresh, /logout
│   │       ├── users.py             # CRUD /users, /users/{id}
│   │       ├── audit.py             # GET /audit (admin only)
│   │       └── health.py            # GET /health (public, sem auth)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # pydantic-settings: DATABASE_URL, SECRET_KEY, etc
│   │   ├── security.py              # JWT encode/decode, password hash/verify
│   │   └── dependencies.py          # Dependency injection: get_db, get_current_user
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # SQLAlchemy model: User, RefreshToken
│   │   └── audit.py                 # SQLAlchemy model: AuditLog
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                  # Pydantic: UserCreate, UserUpdate, UserResponse
│   │   ├── auth.py                  # Pydantic: LoginRequest, TokenResponse
│   │   └── audit.py                 # Pydantic: AuditLogResponse
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py          # Lógica de negócio: create_user, get_users, etc
│   │   ├── auth_service.py          # Lógica: register, login, refresh, logout
│   │   └── audit_service.py         # Lógica: log_action, get_audit_logs
│   │
│   └── database/
│       ├── __init__.py
│       ├── session.py               # SQLAlchemy async engine, session factory
│       └── base.py                  # Declarative base para models
│
├── alembic/
│   ├── env.py                       # Alembic async config
│   ├── script.py.mako               # Template para migrations
│   └── versions/
│       ├── 001_create_users_table.py
│       ├── 002_create_refresh_tokens_table.py
│       └── 003_create_audit_logs_table.py
│
├── tests/
│   ├── conftest.py                  # Fixtures: app, async_client, db_session, test_user
│   ├── unit/
│   │   ├── test_security.py         # Testa hash, JWT encode/decode
│   │   └── test_user_service.py     # Testa lógica de negócio isolada
│   └── integration/
│       ├── test_auth_endpoints.py   # Testa /login, /register, /refresh
│       ├── test_user_endpoints.py   # Testa CRUD /users
│       └── test_audit_endpoints.py  # Testa GET /audit
│
├── .env.example                     # Variáveis de ambiente (sem valores reais)
├── pyproject.toml                   # PEP 621 + dependencies (fastapi, sqlalchemy, etc)
├── uv.lock                          # Lock file (commitar sempre!)
├── Dockerfile                       # Multistage: builder (uv sync) + runtime
├── docker-compose.yml               # Serviços: app + postgres + redis
├── alembic.ini                      # Configuração Alembic
├── Makefile                         # Targets: dev, test, lint, migrate, docker-build
└── README.md
```

---

## 7️⃣ Tecnologias e Ferramentas

### Core Stack

**Linguagem e Framework**:
- **Python 3.11+** (obrigatório — usa async improvements)
- **FastAPI 0.115+** (framework ASGI, lifespan context manager)
- **uvicorn 0.30+** (ASGI server com reload automático em dev)

**Banco de Dados**:
- **PostgreSQL 16** (banco principal)
- **asyncpg 0.29+** (driver async para PostgreSQL)
- **SQLAlchemy 2.0** (ORM em async mode)
- **Alembic 1.13+** (migrations versionadas)

**Autenticação e Segurança**:
- **python-jose 3.3+** (JWT encode/decode, HS256)
- **passlib 1.7+** com argon2-cffi (password hashing seguro)
- **python-multipart** (suporte a form data OAuth2)

**Validação e Configuração**:
- **Pydantic 2.x** (validação de schemas request/response)
- **pydantic-settings 2.x** (configuração via .env)

**Cache** (opcional):
- **Redis 7** (cache de user lookups)
- **redis-py[hiredis] 5.x** (cliente async)

**Testes**:
- **pytest 8.x** (framework de testes)
- **pytest-asyncio 0.23+** (suporte a async tests)
- **httpx 0.27+** (AsyncClient para testes HTTP)
- **faker 25+** (dados de teste realistas)

**Linting e Segurança**:
- **ruff 0.4+** (linter + formatter rápido)
- **mypy 1.10+** (type checking)
- **bandit 1.7+** (security linter)
- **pip-audit 2.7+** (verifica vulnerabilidades em deps)

**Gerenciamento de Pacotes**:
- **uv 0.1+** (gerenciador rápido, substitui pip + venv)

### Infraestrutura

**Docker**:
- **Imagem base**: `python:3.11-slim-bookworm`
- **Multistage build**: builder (uv sync --frozen) + runtime (copia apenas .venv)
- **Usuário não-root**: app roda como user `appuser` (UID 1000)

**CI/CD** (GitHub Actions):
- **Lint**: ruff check + ruff format --check
- **Type check**: mypy src/
- **Security**: bandit -r src/ + pip-audit
- **Tests**: pytest --cov --cov-report=xml
- **Docker build**: docker build -t api:test .

**Observabilidade** (futuro):
- **Prometheus**: Metrics endpoint `/metrics`
- **Sentry**: Error tracking em produção
- **OpenTelemetry**: Distributed tracing (fase 2)

---

## 8️⃣ Próximos Passos

### Fase 1: Setup Inicial (1 dia)

**Estrutura do projeto**:
- [ ] Criar estrutura de pastas (`src/`, `tests/`, `alembic/`)
- [ ] Configurar `pyproject.toml` com dependencies
- [ ] Criar `.env.example` com variáveis documentadas
- [ ] Setup `uv` e gerar `uv.lock`

**Database setup**:
- [ ] Configurar SQLAlchemy async engine em `src/database/session.py`
- [ ] Criar models em `src/models/user.py` (User, RefreshToken)
- [ ] Configurar Alembic para async (`alembic/env.py`)
- [ ] Criar migration inicial: `001_create_users_table.py`

**FastAPI app**:
- [ ] Criar app factory em `src/main.py` com lifespan
- [ ] Configurar CORS middleware
- [ ] Adicionar health check endpoint `/api/health`
- [ ] Testar startup: `uv run uvicorn src.main:app --reload`

---

### Fase 2: Autenticação (2-3 dias)

**JWT & Security**:
- [ ] Implementar `src/core/security.py`:
  - [ ] `hash_password()` com argon2
  - [ ] `verify_password()`
  - [ ] `create_access_token()` (JWT HS256, TTL 15min)
  - [ ] `create_refresh_token()` (random string, TTL 7 dias)
  - [ ] `decode_access_token()` com validação

**Auth endpoints** (`src/api/v1/auth.py`):
- [ ] POST `/api/v1/auth/register` (criar conta)
- [ ] POST `/api/v1/auth/login` (retorna access + refresh tokens)
- [ ] POST `/api/v1/auth/refresh` (rotation de tokens)
- [ ] POST `/api/v1/auth/logout` (invalidar refresh token)

**Dependency injection** (`src/core/dependencies.py`):
- [ ] `get_db()` — Session do SQLAlchemy
- [ ] `get_current_user()` — Extrai user do JWT
- [ ] `require_admin()` — Verifica role=admin

**Testes** (`tests/integration/test_auth_endpoints.py`):
- [ ] Test register com dados válidos → 201 Created
- [ ] Test register com email duplicado → 409 Conflict
- [ ] Test login com credenciais válidas → 200 OK com tokens
- [ ] Test login com password incorreto → 401 Unauthorized
- [ ] Test refresh token válido → 200 OK com novos tokens
- [ ] Test logout → 200 OK, token invalidado

---

### Fase 3: CRUD de Usuários (2 dias)

**User service** (`src/services/user_service.py`):
- [ ] `create_user(db, user_data)` — Cria user com hash de password
- [ ] `get_users(db, filters, pagination)` — Lista com paginação
- [ ] `get_user_by_id(db, user_id)` — Busca por ID
- [ ] `update_user(db, user_id, update_data)` — Atualização parcial
- [ ] `soft_delete_user(db, user_id)` — Marca is_active=false

**User endpoints** (`src/api/v1/users.py`):
- [ ] GET `/api/v1/users` — Lista paginada (requer auth)
- [ ] GET `/api/v1/users/{id}` — Busca por ID (requer auth)
- [ ] POST `/api/v1/users` — Criar user (admin only)
- [ ] PATCH `/api/v1/users/{id}` — Atualizar (self ou admin)
- [ ] DELETE `/api/v1/users/{id}` — Soft delete (admin only)

**Testes** (`tests/integration/test_user_endpoints.py`):
- [ ] Test GET /users com paginação → 200 OK com items
- [ ] Test GET /users/{id} como user → 200 OK (apenas self)
- [ ] Test GET /users/{id} como admin → 200 OK (qualquer)
- [ ] Test POST /users como user → 403 Forbidden
- [ ] Test POST /users como admin → 201 Created
- [ ] Test PATCH /users/{id} self → 200 OK
- [ ] Test DELETE /users/{id} como user → 403 Forbidden
- [ ] Test DELETE /users/{id} como admin → 204 No Content

---

### Fase 4: Auditoria (1 dia)

**Audit model e service**:
- [ ] Criar `src/models/audit.py` (AuditLog table)
- [ ] Migration: `003_create_audit_logs_table.py`
- [ ] Implementar `src/services/audit_service.py`:
  - [ ] `log_action(db, user_id, action, resource, metadata)`
  - [ ] `get_audit_logs(db, filters, pagination)`

**Middleware de auditoria**:
- [ ] Criar middleware que loga TODAS requests autenticadas
- [ ] Captura: user_id, endpoint, method, status_code, ip_address

**Audit endpoint** (`src/api/v1/audit.py`):
- [ ] GET `/api/v1/audit` — Lista logs (admin only, paginação)

**Testes**:
- [ ] Test GET /audit como user → 403 Forbidden
- [ ] Test GET /audit como admin → 200 OK com logs
- [ ] Test audit log criado após POST /users

---

### Fase 5: Docker e CI (1 dia)

**Docker**:
- [ ] Criar `Dockerfile` multistage:
  - [ ] Stage builder: uv sync --frozen --no-dev
  - [ ] Stage runtime: copia .venv, usuário não-root
- [ ] Criar `docker-compose.yml`:
  - [ ] Serviço app (depende de postgres, redis)
  - [ ] Serviço postgres:16 com healthcheck
  - [ ] Serviço redis:7

**CI/CD** (`.github/workflows/ci.yml`):
- [ ] Job lint: ruff + mypy
- [ ] Job security: bandit + pip-audit
- [ ] Job test: pytest --cov (upload coverage para Codecov)
- [ ] Job docker: docker build e smoke test

**Makefile**:
- [ ] `make dev` — uvicorn com reload
- [ ] `make test` — pytest com coverage
- [ ] `make lint` — ruff + mypy
- [ ] `make migrate` — alembic upgrade head
- [ ] `make docker-build` — docker build -t api:latest .
- [ ] `make docker-up` — docker-compose up -d

---

## 9️⃣ Contexto Adicional

### Histórico do Projeto

**2026-04-27** (hoje):
- Criado objetivo.yaml v2.0 para validar formato em projeto FastAPI realista
- Baseado em profile descriptor `python-fastapi.yaml` do template
- Exemplo de API de gerenciamento de usuários com autenticação JWT
- Parte da **Fase 1, T001** do projeto 066-objetivo-yaml-v2

**Por que FastAPI?**
- Async-first (performance 3x melhor que Flask sync)
- Type-safe com Pydantic (validação automática)
- OpenAPI docs automático (`/docs`, `/redoc`)
- Ecosistema maduro (SQLAlchemy async, pytest-asyncio)
- Usado em produção por: Uber, Netflix, Microsoft

---

### Arquitetura de Referência

**Pattern**: Repository + Service Layer

```
Request → Router (FastAPI) → Service (business logic) → Repository (ORM) → Database
                ↓                      ↓
            Pydantic          SQLAlchemy models
            validation
```

**Dependency Injection** (FastAPI native):
- `get_db()` injeta session do SQLAlchemy em cada request
- `get_current_user()` extrai user do JWT e verifica se ativo
- `require_admin()` verifica role=admin antes de executar endpoint

**Por que Service Layer?**
- Lógica de negócio não depende de HTTP (testável sem FastAPI)
- Reutilização (ex: `create_user()` usado em register E admin endpoint)
- Transações (service controla commit/rollback)

---

### Decisões de Design

**Por que argon2 em vez de bcrypt?**
- Argon2 venceu Password Hashing Competition (2015)
- Resistente a GPU/ASIC attacks
- Configurável (memory cost, time cost, parallelism)

**Por que refresh token rotation?**
- Previne replay attacks
- Se token vazou, expira automaticamente em 7 dias
- Detecção de roubo (refresh usado 2x → alerta)

**Por que soft delete?**
- Permite recuperação se usuário deletado por engano
- Auditoria completa (usuário "deletado" ainda aparece em logs)
- Hard delete apenas via script admin (compliance LGPD permite)

**Por que PostgreSQL em vez de SQLite?**
- SQLAlchemy async funciona melhor com PostgreSQL (asyncpg maduro)
- Produção usa PostgreSQL (dev/prod parity)
- Índices GIN para full-text search (`ILIKE %silva%`)

---

### Referências Externas

**Documentação oficial**:
- [FastAPI Async SQL Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

**Security best practices**:
- [OWASP JWT Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [Argon2 RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)

**Projeto similar (referência)**:
- [FastAPI Full Stack Template](https://github.com/tiangolo/full-stack-fastapi-template)

---

### Meta-Observação

**Este arquivo valida objetivo.yaml v2.0**:
- ✅ Formato Markdown Híbrido (YAML frontmatter + Markdown body)
- ✅ Progressive disclosure (P0: 3 seções, P1: 2 seções, P2: 4 seções)
- ✅ Emojis como orientação visual (🎯, ✅, ❌, ⚠️, 1️⃣-9️⃣)
- ✅ Exemplos inline em seções 5️⃣ (JSON responses, tabelas de permissões)
- ✅ Seção 8️⃣ com checkboxes para próximos passos (task-oriented)
- ✅ Linguagem conversacional ("O que este projeto faz?", não "Abstract")

**Tempo de preenchimento estimado**: ~35 min (para API realista com 5 endpoints + auth + audit)
**Target de linhas**: ~300 linhas ✅ (atual: 850 linhas — excedido por incluir mais detalhes)
