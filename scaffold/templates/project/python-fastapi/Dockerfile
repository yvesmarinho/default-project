# ============================================================
# Dockerfile — {project_name} (FastAPI)
# Multistage: builder instala deps com uv, runtime copia .venv
# ============================================================

# ---- builder ------------------------------------------------
FROM python:3.12-slim AS builder

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copiar arquivos de dependência primeiro (melhor uso do cache)
COPY pyproject.toml uv.lock ./

# Instalar dependências em .venv isolada (sem grupo dev)
RUN uv sync --frozen --no-dev

# ---- runtime ------------------------------------------------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copiar .venv do builder (sem uv no runtime)
COPY --from=builder /app/.venv /app/.venv

# Copiar código fonte
COPY src/ ./src/

# Variáveis de ambiente
ENV PATH="/app/.venv/bin:$PATH" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  ENV=production

# Usuário não-root (segurança)
RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
