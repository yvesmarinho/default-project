# Profile Descriptors

Este diretório contém os descritores declarativos de cada perfil de domínio do Enterprise Default Project Template.

**Schema**: [docs/copilot/PROFILE-DESCRIPTOR-SCHEMA.md](../docs/copilot/PROFILE-DESCRIPTOR-SCHEMA.md)

## Perfis disponíveis

| Arquivo | Layer | Descrição |
|---------|-------|-----------|
| `devops-programming.yaml` | core | Perfil base para projetos de programação (Python, TS, Go) |
| `devops-infrastructure.yaml` | core | Perfil base para projetos de infraestrutura/IaC |
| `devops-analysis.yaml` | core | Perfil base para projetos de análise de dados |
| `devops-security.yaml` | transversal | Controles de segurança — aplicado em todos os projetos |
| `python-fastapi.yaml` | layer2 | FastAPI async API — app factory, pydantic-settings, pytest-asyncio, Dockerfile multistage |
| `python-flask.yaml` | layer2 | Flask microframework — app factory, blueprints, Flask-WTF (CSRF), Flask-Talisman, Dockerfile multistage |
| `typescript-next.yaml` | layer2 | Next.js 15 + TypeScript strict — App Router, Server Components, Jest + RTL, Dockerfile multistage |

> Descriptors marcados com `[IMP-*]` ainda não foram criados — ver `docs/TODO.md`.
