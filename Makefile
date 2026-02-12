# Enterprise Default Project Template - Makefile
# This Makefile automates the creation of the complete project structure
# and provides common development tasks

.PHONY: help init structure dirs docs github specify src tests scripts config docker clean install-deps

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

## help: Display this help message
help:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  Enterprise Default Project Template - Makefile Help      ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@echo ""
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /' | awk -F: '{printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

## init: Initialize complete project structure (recommended for new projects)
init:
	@echo "$(BLUE)🚀 Initializing Enterprise Project Structure...$(NC)"
	@$(MAKE) structure
	@$(MAKE) create-base-files
	@echo "$(GREEN)✅ Project structure created successfully!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Run 'make setup-python' or 'make setup-node' to configure your language"
	@echo "  2. Run 'make install-deps' to install dependencies"
	@echo "  3. Run 'make dev' to start development"

## structure: Create complete directory structure
structure: dirs github specify docs src tests scripts config docker
	@echo "$(GREEN)✅ Directory structure created$(NC)"

## dirs: Create base directories
dirs:
	@echo "$(BLUE)📁 Creating base directories...$(NC)"
	@mkdir -p .vscode
	@mkdir -p .secrets
	@if [ -d .secrets ] && [ ! -f .secrets/.gitkeep ]; then \
		echo "# This directory stores sensitive files" > .secrets/README.md; \
		echo "# Add your secrets here (certificates, keys, etc.)" >> .secrets/README.md; \
		echo "# These files are ignored by git" >> .secrets/README.md; \
	fi

## github: Create GitHub-related directories and files
github:
	@echo "$(BLUE)📁 Creating GitHub structure...$(NC)"
	@mkdir -p .github/workflows
	@mkdir -p .github/ISSUE_TEMPLATE

## specify: Create Speckit directories
specify:
	@echo "$(BLUE)📁 Creating Speckit structure...$(NC)"
	@mkdir -p .specify/specs

## docs: Create documentation directories
docs:
	@echo "$(BLUE)📁 Creating documentation structure...$(NC)"
	@mkdir -p docs/architecture
	@mkdir -p docs/api
	@mkdir -p docs/guides

## src: Create source code directories
src:
	@echo "$(BLUE)📁 Creating source code structure...$(NC)"
	@mkdir -p src/core/models
	@mkdir -p src/core/interfaces
	@mkdir -p src/core/services
	@mkdir -p src/data/repositories
	@mkdir -p src/data/factories
	@mkdir -p src/data/migrations
	@mkdir -p src/presentation/views
	@mkdir -p src/presentation/presenters
	@mkdir -p src/presentation/viewmodels
	@mkdir -p src/infrastructure/config
	@mkdir -p src/infrastructure/logging
	@mkdir -p src/infrastructure/security
	@mkdir -p src/shared/constants
	@mkdir -p src/shared/helpers
	@mkdir -p src/shared/validators

## tests: Create test directories
tests:
	@echo "$(BLUE)📁 Creating test structure...$(NC)"
	@mkdir -p tests/unit
	@mkdir -p tests/integration
	@mkdir -p tests/e2e

## scripts: Create script directories
scripts:
	@echo "$(BLUE)📁 Creating scripts structure...$(NC)"
	@mkdir -p scripts/setup
	@mkdir -p scripts/build
	@mkdir -p scripts/deploy

## config: Create configuration directories
config:
	@echo "$(BLUE)📁 Creating configuration structure...$(NC)"
	@mkdir -p config

## docker: Create Docker directories
docker:
	@echo "$(BLUE)📁 Creating Docker structure...$(NC)"
	@mkdir -p docker

## create-base-files: Create base configuration files
create-base-files:
	@echo "$(BLUE)📝 Creating base files...$(NC)"
	@$(MAKE) create-gitignore
	@$(MAKE) create-env-example
	@$(MAKE) create-editorconfig
	@$(MAKE) create-github-files
	@$(MAKE) create-speckit-config
	@$(MAKE) create-docker-files
	@$(MAKE) create-config-files
	@$(MAKE) create-readme-files
	@echo "$(GREEN)✅ Base files created$(NC)"

## create-gitignore: Create .gitignore file
create-gitignore:
	@if [ ! -f .gitignore ]; then \
		echo "$(BLUE)Creating .gitignore...$(NC)"; \
		echo "# Dependencies" > .gitignore; \
		echo "node_modules/" >> .gitignore; \
		echo "__pycache__/" >> .gitignore; \
		echo "*.pyc" >> .gitignore; \
		echo "venv/" >> .gitignore; \
		echo ".venv/" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Environment variables" >> .gitignore; \
		echo ".env" >> .gitignore; \
		echo ".env.local" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Secrets and sensitive data" >> .gitignore; \
		echo ".secrets/" >> .gitignore; \
		echo "*.key" >> .gitignore; \
		echo "*.pem" >> .gitignore; \
		echo "*.crt" >> .gitignore; \
		echo "*.p12" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Build outputs" >> .gitignore; \
		echo "dist/" >> .gitignore; \
		echo "build/" >> .gitignore; \
		echo "*.egg-info/" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# IDE" >> .gitignore; \
		echo ".idea/" >> .gitignore; \
		echo "*.swp" >> .gitignore; \
		echo "*.swo" >> .gitignore; \
		echo ".DS_Store" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Logs" >> .gitignore; \
		echo "*.log" >> .gitignore; \
		echo "logs/" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Testing" >> .gitignore; \
		echo "coverage/" >> .gitignore; \
		echo ".coverage" >> .gitignore; \
		echo ".pytest_cache/" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# OS" >> .gitignore; \
		echo "Thumbs.db" >> .gitignore; \
		echo "$(GREEN)✅ .gitignore created$(NC)"; \
	fi

## create-env-example: Create .env.example file
create-env-example:
	@if [ ! -f .env.example ]; then \
		echo "$(BLUE)Creating .env.example...$(NC)"; \
		echo "# Application Configuration" > .env.example; \
		echo "APP_NAME=my-project" >> .env.example; \
		echo "APP_ENV=development" >> .env.example; \
		echo "APP_PORT=3000" >> .env.example; \
		echo "APP_DEBUG=true" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Database Configuration" >> .env.example; \
		echo "DB_HOST=localhost" >> .env.example; \
		echo "DB_PORT=5432" >> .env.example; \
		echo "DB_NAME=myapp_db" >> .env.example; \
		echo "DB_USER=myapp_user" >> .env.example; \
		echo "DB_PASSWORD=secure_password" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Authentication" >> .env.example; \
		echo "JWT_SECRET=your-secret-key-change-in-production" >> .env.example; \
		echo "JWT_EXPIRATION=3600" >> .env.example; \
		echo "" >> .env.example; \
		echo "# External Services" >> .env.example; \
		echo "API_KEY=your-api-key" >> .env.example; \
		echo "$(GREEN)✅ .env.example created$(NC)"; \
	fi

## create-editorconfig: Create .editorconfig file
create-editorconfig:
	@if [ ! -f .editorconfig ]; then \
		echo "$(BLUE)Creating .editorconfig...$(NC)"; \
		echo "root = true" > .editorconfig; \
		echo "" >> .editorconfig; \
		echo "[*]" >> .editorconfig; \
		echo "charset = utf-8" >> .editorconfig; \
		echo "end_of_line = lf" >> .editorconfig; \
		echo "insert_final_newline = true" >> .editorconfig; \
		echo "trim_trailing_whitespace = true" >> .editorconfig; \
		echo "" >> .editorconfig; \
		echo "[*.{js,ts,jsx,tsx,json}]" >> .editorconfig; \
		echo "indent_style = space" >> .editorconfig; \
		echo "indent_size = 2" >> .editorconfig; \
		echo "" >> .editorconfig; \
		echo "[*.{py}]" >> .editorconfig; \
		echo "indent_style = space" >> .editorconfig; \
		echo "indent_size = 4" >> .editorconfig; \
		echo "" >> .editorconfig; \
		echo "[*.{md}]" >> .editorconfig; \
		echo "trim_trailing_whitespace = false" >> .editorconfig; \
		echo "$(GREEN)✅ .editorconfig created$(NC)"; \
	fi

## create-github-files: Create GitHub workflow and template files
create-github-files:
	@echo "$(BLUE)Creating GitHub files...$(NC)"
	@if [ ! -f .github/workflows/ci.yml ]; then \
		echo "name: CI" > .github/workflows/ci.yml; \
		echo "" >> .github/workflows/ci.yml; \
		echo "on:" >> .github/workflows/ci.yml; \
		echo "  push:" >> .github/workflows/ci.yml; \
		echo "    branches: [ main, develop ]" >> .github/workflows/ci.yml; \
		echo "  pull_request:" >> .github/workflows/ci.yml; \
		echo "    branches: [ main, develop ]" >> .github/workflows/ci.yml; \
		echo "" >> .github/workflows/ci.yml; \
		echo "jobs:" >> .github/workflows/ci.yml; \
		echo "  test:" >> .github/workflows/ci.yml; \
		echo "    runs-on: ubuntu-latest" >> .github/workflows/ci.yml; \
		echo "    steps:" >> .github/workflows/ci.yml; \
		echo "      - uses: actions/checkout@v3" >> .github/workflows/ci.yml; \
		echo "      - name: Run tests" >> .github/workflows/ci.yml; \
		echo "        run: make test" >> .github/workflows/ci.yml; \
	fi
	@if [ ! -f .github/PULL_REQUEST_TEMPLATE.md ]; then \
		echo "## Description" > .github/PULL_REQUEST_TEMPLATE.md; \
		echo "" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "Brief description of changes" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "## Type of Change" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "- [ ] Bug fix" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "- [ ] New feature" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "- [ ] Breaking change" >> .github/PULL_REQUEST_TEMPLATE.md; \
		echo "- [ ] Documentation update" >> .github/PULL_REQUEST_TEMPLATE.md; \
	fi
	@echo "$(GREEN)✅ GitHub files created$(NC)"

## create-speckit-config: Create Speckit configuration
create-speckit-config:
	@if [ ! -f .specify/config.json ]; then \
		echo "$(BLUE)Creating Speckit config...$(NC)"; \
		echo "{" > .specify/config.json; \
		echo "  \"version\": \"2.0\"," >> .specify/config.json; \
		echo "  \"organization\": \"your-org\"," >> .specify/config.json; \
		echo "  \"project\": \"default-project\"," >> .specify/config.json; \
		echo "  \"specs\": {" >> .specify/config.json; \
		echo "    \"outputPath\": \"docs/api\"," >> .specify/config.json; \
		echo "    \"format\": \"openapi-3.0\"" >> .specify/config.json; \
		echo "  }" >> .specify/config.json; \
		echo "}" >> .specify/config.json; \
		echo "$(GREEN)✅ Speckit config created$(NC)"; \
	fi

## create-docker-files: Create Docker configuration files
create-docker-files:
	@if [ ! -f docker/Dockerfile ]; then \
		echo "$(BLUE)Creating Dockerfile...$(NC)"; \
		echo "FROM node:18-alpine" > docker/Dockerfile; \
		echo "" >> docker/Dockerfile; \
		echo "WORKDIR /app" >> docker/Dockerfile; \
		echo "" >> docker/Dockerfile; \
		echo "COPY package*.json ./" >> docker/Dockerfile; \
		echo "RUN npm install" >> docker/Dockerfile; \
		echo "" >> docker/Dockerfile; \
		echo "COPY . ." >> docker/Dockerfile; \
		echo "" >> docker/Dockerfile; \
		echo "EXPOSE 3000" >> docker/Dockerfile; \
		echo "" >> docker/Dockerfile; \
		echo "CMD [\"npm\", \"start\"]" >> docker/Dockerfile; \
	fi
	@if [ ! -f docker/docker-compose.yml ]; then \
		echo "$(BLUE)Creating docker-compose.yml...$(NC)"; \
		echo "version: '3.8'" > docker/docker-compose.yml; \
		echo "" >> docker/docker-compose.yml; \
		echo "services:" >> docker/docker-compose.yml; \
		echo "  app:" >> docker/docker-compose.yml; \
		echo "    build:" >> docker/docker-compose.yml; \
		echo "      context: .." >> docker/docker-compose.yml; \
		echo "      dockerfile: docker/Dockerfile" >> docker/docker-compose.yml; \
		echo "    ports:" >> docker/docker-compose.yml; \
		echo "      - \"3000:3000\"" >> docker/docker-compose.yml; \
		echo "    environment:" >> docker/docker-compose.yml; \
		echo "      - NODE_ENV=development" >> docker/docker-compose.yml; \
		echo "    volumes:" >> docker/docker-compose.yml; \
		echo "      - ..:/app" >> docker/docker-compose.yml; \
		echo "      - /app/node_modules" >> docker/docker-compose.yml; \
	fi
	@echo "$(GREEN)✅ Docker files created$(NC)"

## create-config-files: Create environment-specific config files
create-config-files:
	@if [ ! -f config/development.json ]; then \
		echo "$(BLUE)Creating config files...$(NC)"; \
		echo "{" > config/development.json; \
		echo "  \"env\": \"development\"," >> config/development.json; \
		echo "  \"debug\": true," >> config/development.json; \
		echo "  \"api\": {" >> config/development.json; \
		echo "    \"baseUrl\": \"http://localhost:3000\"" >> config/development.json; \
		echo "  }" >> config/development.json; \
		echo "}" >> config/development.json; \
		echo "{" > config/staging.json; \
		echo "  \"env\": \"staging\"," >> config/staging.json; \
		echo "  \"debug\": false," >> config/staging.json; \
		echo "  \"api\": {" >> config/staging.json; \
		echo "    \"baseUrl\": \"https://staging.example.com\"" >> config/staging.json; \
		echo "  }" >> config/staging.json; \
		echo "}" >> config/staging.json; \
		echo "{" > config/production.json; \
		echo "  \"env\": \"production\"," >> config/production.json; \
		echo "  \"debug\": false," >> config/production.json; \
		echo "  \"api\": {" >> config/production.json; \
		echo "    \"baseUrl\": \"https://api.example.com\"" >> config/production.json; \
		echo "  }" >> config/production.json; \
		echo "}" >> config/production.json; \
		echo "$(GREEN)✅ Config files created$(NC)"; \
	fi

## create-readme-files: Create README files for major directories
create-readme-files:
	@echo "$(BLUE)Creating README files for directories...$(NC)"
	@echo "# Core Business Logic" > src/core/README.md
	@echo "" >> src/core/README.md
	@echo "This directory contains the core business logic of the application." >> src/core/README.md
	@echo "# Data Access Layer" > src/data/README.md
	@echo "" >> src/data/README.md
	@echo "This directory contains repositories and data access implementations." >> src/data/README.md
	@echo "# Presentation Layer" > src/presentation/README.md
	@echo "" >> src/presentation/README.md
	@echo "This directory contains the MVP presentation layer components." >> src/presentation/README.md
	@echo "# Tests" > tests/README.md
	@echo "" >> tests/README.md
	@echo "This directory contains all test suites for the application." >> tests/README.md
	@echo "$(GREEN)✅ README files created$(NC)"

## setup-python: Setup Python project structure
setup-python:
	@echo "$(BLUE)🐍 Setting up Python project...$(NC)"
	@if [ ! -f requirements.txt ]; then \
		echo "# Core dependencies" > requirements.txt; \
		echo "fastapi>=0.104.0" >> requirements.txt; \
		echo "uvicorn>=0.24.0" >> requirements.txt; \
		echo "pydantic>=2.5.0" >> requirements.txt; \
		echo "" >> requirements.txt; \
		echo "# Development dependencies" >> requirements.txt; \
		echo "pytest>=7.4.0" >> requirements.txt; \
		echo "pytest-cov>=4.1.0" >> requirements.txt; \
		echo "black>=23.11.0" >> requirements.txt; \
		echo "flake8>=6.1.0" >> requirements.txt; \
		echo "mypy>=1.7.0" >> requirements.txt; \
	fi
	@if [ ! -f requirements-dev.txt ]; then \
		echo "# Development-only dependencies" > requirements-dev.txt; \
		echo "-r requirements.txt" >> requirements-dev.txt; \
		echo "ipython>=8.17.0" >> requirements-dev.txt; \
		echo "ipdb>=0.13.13" >> requirements-dev.txt; \
	fi
	@if [ ! -f setup.py ]; then \
		echo "from setuptools import setup, find_packages" > setup.py; \
		echo "" >> setup.py; \
		echo "setup(" >> setup.py; \
		echo "    name='default-project'," >> setup.py; \
		echo "    version='0.1.0'," >> setup.py; \
		echo "    packages=find_packages()," >> setup.py; \
		echo "    install_requires=[" >> setup.py; \
		echo "        'fastapi>=0.104.0'," >> setup.py; \
		echo "        'uvicorn>=0.24.0'," >> setup.py; \
		echo "    ]," >> setup.py; \
		echo ")" >> setup.py; \
	fi
	@echo "$(GREEN)✅ Python project setup complete$(NC)"

## setup-node: Setup Node.js/TypeScript project structure
setup-node:
	@echo "$(BLUE)📘 Setting up Node.js project...$(NC)"
	@if [ ! -f package.json ]; then \
		echo "{" > package.json; \
		echo "  \"name\": \"default-project\"," >> package.json; \
		echo "  \"version\": \"1.0.0\"," >> package.json; \
		echo "  \"description\": \"Enterprise Default Project Template\"," >> package.json; \
		echo "  \"main\": \"dist/index.js\"," >> package.json; \
		echo "  \"scripts\": {" >> package.json; \
		echo "    \"dev\": \"nodemon src/index.ts\"," >> package.json; \
		echo "    \"build\": \"tsc\"," >> package.json; \
		echo "    \"start\": \"node dist/index.js\"," >> package.json; \
		echo "    \"test\": \"jest\"," >> package.json; \
		echo "    \"test:watch\": \"jest --watch\"," >> package.json; \
		echo "    \"test:coverage\": \"jest --coverage\"," >> package.json; \
		echo "    \"lint\": \"eslint src/**/*.ts\"," >> package.json; \
		echo "    \"format\": \"prettier --write \\\"src/**/*.ts\\\"\"" >> package.json; \
		echo "  }," >> package.json; \
		echo "  \"keywords\": [\"template\", \"enterprise\", \"mvp\"]," >> package.json; \
		echo "  \"author\": \"Vya-Jobs Team\"," >> package.json; \
		echo "  \"license\": \"MIT\"" >> package.json; \
		echo "}" >> package.json; \
	fi
	@if [ ! -f tsconfig.json ]; then \
		echo "{" > tsconfig.json; \
		echo "  \"compilerOptions\": {" >> tsconfig.json; \
		echo "    \"target\": \"ES2020\"," >> tsconfig.json; \
		echo "    \"module\": \"commonjs\"," >> tsconfig.json; \
		echo "    \"outDir\": \"./dist\"," >> tsconfig.json; \
		echo "    \"rootDir\": \"./src\"," >> tsconfig.json; \
		echo "    \"strict\": true," >> tsconfig.json; \
		echo "    \"esModuleInterop\": true," >> tsconfig.json; \
		echo "    \"skipLibCheck\": true," >> tsconfig.json; \
		echo "    \"forceConsistentCasingInFileNames\": true," >> tsconfig.json; \
		echo "    \"resolveJsonModule\": true," >> tsconfig.json; \
		echo "    \"declaration\": true," >> tsconfig.json; \
		echo "    \"declarationMap\": true," >> tsconfig.json; \
		echo "    \"sourceMap\": true" >> tsconfig.json; \
		echo "  }," >> tsconfig.json; \
		echo "  \"include\": [\"src/**/*\"]," >> tsconfig.json; \
		echo "  \"exclude\": [\"node_modules\", \"dist\", \"tests\"]" >> tsconfig.json; \
		echo "}" >> tsconfig.json; \
	fi
	@echo "$(GREEN)✅ Node.js project setup complete$(NC)"

## install-deps: Install project dependencies
install-deps:
	@if [ -f package.json ]; then \
		echo "$(BLUE)📦 Installing Node.js dependencies...$(NC)"; \
		npm install; \
	fi
	@if [ -f requirements.txt ]; then \
		echo "$(BLUE)📦 Installing Python dependencies...$(NC)"; \
		pip install -r requirements.txt; \
	fi
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

## dev: Start development server
dev:
	@if [ -f package.json ]; then \
		npm run dev; \
	elif [ -f requirements.txt ]; then \
		uvicorn main:app --reload; \
	else \
		echo "$(RED)❌ No package.json or requirements.txt found$(NC)"; \
	fi

## build: Build the project
build:
	@echo "$(BLUE)🔨 Building project...$(NC)"
	@if [ -f package.json ]; then \
		npm run build; \
	elif [ -f setup.py ]; then \
		python setup.py build; \
	fi
	@echo "$(GREEN)✅ Build complete$(NC)"

## test: Run all tests
test:
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@if [ -f package.json ]; then \
		npm test; \
	elif [ -f requirements.txt ]; then \
		pytest; \
	fi

## lint: Run linting
lint:
	@echo "$(BLUE)🔍 Running linter...$(NC)"
	@if [ -f package.json ]; then \
		npm run lint; \
	elif [ -f requirements.txt ]; then \
		flake8 src/; \
	fi

## format: Format code
format:
	@echo "$(BLUE)✨ Formatting code...$(NC)"
	@if [ -f package.json ]; then \
		npm run format; \
	elif [ -f requirements.txt ]; then \
		black src/; \
	fi

## docker-build: Build Docker image
docker-build:
	@echo "$(BLUE)🐳 Building Docker image...$(NC)"
	@docker build -f docker/Dockerfile -t default-project:latest .
	@echo "$(GREEN)✅ Docker image built$(NC)"

## docker-up: Start Docker containers
docker-up:
	@echo "$(BLUE)🐳 Starting Docker containers...$(NC)"
	@docker-compose -f docker/docker-compose.yml up -d
	@echo "$(GREEN)✅ Containers started$(NC)"

## docker-down: Stop Docker containers
docker-down:
	@echo "$(BLUE)🐳 Stopping Docker containers...$(NC)"
	@docker-compose -f docker/docker-compose.yml down
	@echo "$(GREEN)✅ Containers stopped$(NC)"

## clean: Remove generated files and directories
clean:
	@echo "$(BLUE)🧹 Cleaning project...$(NC)"
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf __pycache__/
	@rm -rf .pytest_cache/
	@rm -rf coverage/
	@rm -rf node_modules/
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@echo "$(GREEN)✅ Project cleaned$(NC)"

## status: Show project status and structure
status:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  Project Status                                            ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Directory Structure:$(NC)"
	@tree -L 2 -I 'node_modules|__pycache__|*.pyc|.git' || ls -la
	@echo ""
	@echo "$(YELLOW)Configuration Files:$(NC)"
	@ls -1 | grep -E '(package.json|requirements.txt|Makefile|README.md|Dockerfile|docker-compose.yml)' || echo "  No config files found"

##
## ═══════════════════════════════════════════════════════════════════════
## TEMPLATE MANAGEMENT
## ═══════════════════════════════════════════════════════════════════════
##

## init-new-project: Initialize a new project from this template
init-new-project:
	@if [ -z "$(NAME)" ]; then \
		echo "$(RED)Error: Project name required$(NC)"; \
		echo ""; \
		echo "Usage: make init-new-project NAME=my-project"; \
		echo ""; \
		echo "The name must:"; \
		echo "  - Use only lowercase letters (a-z)"; \
		echo "  - Use numbers (0-9)"; \
		echo "  - Use hyphens (-) to separate words"; \
		echo ""; \
		echo "Examples:"; \
		echo "  make init-new-project NAME=my-app"; \
		echo "  make init-new-project NAME=api-v2"; \
		echo "  make init-new-project NAME=data-processor-2024"; \
		exit 1; \
	fi
	@echo "$(BLUE)🚀 Initializing new project: $(NAME)$(NC)"
	@./scripts/init-new-project.sh $(NAME)

## setup-shared-configs: Setup shared configuration repository
setup-shared-configs:
	@echo "$(BLUE)📦 Setting up shared configuration repository...$(NC)"
	@if [ -d "$$HOME/Documentos/DevOps/.copilot-shared" ]; then \
		echo "$(YELLOW)⚠ Shared configs already exist at ~/Documentos/DevOps/.copilot-shared$(NC)"; \
		read -p "Overwrite? (y/N): " confirm; \
		if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
			echo "$(YELLOW)Cancelled$(NC)"; \
			exit 0; \
		fi; \
	fi
	@mkdir -p "$$HOME/Documentos/DevOps/.copilot-shared"/{rules,scripts,templates,docs}
	@echo "$(GREEN)✅ Shared directory structure created$(NC)"
	@echo ""
	@echo "$(BLUE)Copying configuration files...$(NC)"
	@cp .copilot-rules.md "$$HOME/Documentos/DevOps/.copilot-shared/rules/" 2>/dev/null || true
	@cp .copilot-git-rules.md "$$HOME/Documentos/DevOps/.copilot-shared/rules/" 2>/dev/null || true
	@cp .copilot-strict-enforcement.md "$$HOME/Documentos/DevOps/.copilot-shared/rules/" 2>/dev/null || true
	@cp .copilot-strict-rules.md "$$HOME/Documentos/DevOps/.copilot-shared/rules/" 2>/dev/null || true
	@cp .copilot-file-rules.sh "$$HOME/Documentos/DevOps/.copilot-shared/rules/" 2>/dev/null || true
	@echo "$(GREEN)✅ Configuration files copied$(NC)"
	@echo ""
	@echo "$(BLUE)Copying scripts...$(NC)"
	@cp scripts/setup-project-links.sh "$$HOME/Documentos/DevOps/.copilot-shared/scripts/" 2>/dev/null || true
	@cp scripts/check-project-links.sh "$$HOME/Documentos/DevOps/.copilot-shared/scripts/" 2>/dev/null || true
	@chmod +x "$$HOME/Documentos/DevOps/.copilot-shared/scripts"/*.sh
	@echo "$(GREEN)✅ Scripts copied and made executable$(NC)"
	@echo ""
	@echo "$(BLUE)Copying documentation...$(NC)"
	@if [ -f "docs/SHARED_CONFIGS_SOLUTION.md" ]; then \
		cp docs/SHARED_CONFIGS_SOLUTION.md "$$HOME/Documentos/DevOps/.copilot-shared/docs/" 2>/dev/null || true; \
		echo "$(GREEN)✅ Documentation copied$(NC)"; \
	else \
		echo "$(YELLOW)⚠ SHARED_CONFIGS_SOLUTION.md not found (may already be moved)$(NC)"; \
	fi
	@echo ""
	@echo "$(BLUE)Initializing Git repository...$(NC)"
	@cd "$$HOME/Documentos/DevOps/.copilot-shared" && \
		if [ ! -d .git ]; then \
			git init && \
			git add . && \
			git commit -m "feat: Initial shared configs"; \
			echo "$(GREEN)✅ Git repository initialized$(NC)"; \
		else \
			echo "$(YELLOW)⚠ Git already initialized$(NC)"; \
		fi
	@echo ""
	@echo "$(GREEN)🎉 Shared configuration repository ready!$(NC)"
	@echo ""
	@echo "$(YELLOW)Location: $$HOME/Documentos/DevOps/.copilot-shared/$(NC)"
	@echo ""
	@echo "$(YELLOW)Structure created:$(NC)"
	@echo "  rules/     - Copilot configuration files"
	@echo "  scripts/   - Automation scripts"
	@echo "  templates/ - Project templates"
	@echo "  docs/      - Shared documentation"
	@echo ""
	@echo "$(YELLOW)Suggested aliases (add to ~/.zshrc or ~/.bashrc):$(NC)"
	@echo '  alias copilot-setup="$$HOME/Documentos/DevOps/.copilot-shared/scripts/setup-project-links.sh"'
	@echo '  alias copilot-check="$$HOME/Documentos/DevOps/.copilot-shared/scripts/check-project-links.sh"'
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Setup links for this project:"
	@echo "     make setup-project-links"
	@echo "  2. Or create a new project:"
	@echo "     make init-new-project NAME=my-project"

## setup-project-links: Setup symlinks to shared configs for this project
setup-project-links:
	@echo "$(BLUE)🔗 Setting up symlinks to shared configs...$(NC)"
	@if [ ! -d "$$HOME/Documentos/DevOps/.copilot-shared" ]; then \
		echo "$(RED)Error: Shared configs not found$(NC)"; \
		echo ""; \
		echo "Run first: make setup-shared-configs"; \
		exit 1; \
	fi
	@"$$HOME/Documentos/DevOps/.copilot-shared/scripts/setup-project-links.sh" .
	@echo "$(GREEN)✅ Symlinks configured$(NC)"

## check-project-links: Verify symlinks status
check-project-links:
	@echo "$(BLUE)🔍 Checking symlinks status...$(NC)"
	@if [ ! -d "$$HOME/Documentos/DevOps/.copilot-shared" ]; then \
		echo "$(RED)Error: Shared configs not found$(NC)"; \
		exit 1; \
	fi
	@"$$HOME/Documentos/DevOps/.copilot-shared/scripts/check-project-links.sh" .
