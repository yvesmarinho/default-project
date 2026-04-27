---
version: "2.0"
project:
  name: "fastapi-helm-chart"
  title: "Helm Chart para FastAPI Application"
  type: "deployment-chart"
  domain: "infrastructure"
  language: "yaml"

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

# 🎯 Objetivo: Helm Chart para Deploy de API FastAPI

## 1️⃣ O que este projeto faz?

**Em uma frase**: Helm chart v2 para deploy de aplicação FastAPI em Kubernetes, com Deployment + Service + Ingress TLS + HPA + ConfigMap, parametrizado por ambiente (staging/prod).

**Componentes principais**:
- **Chart Helm**: Parametrização via `values.yaml` (imagem, réplicas, recursos)
- **Deployment**: FastAPI container com probes (liveness/readiness), resources limits/requests
- **Service**: ClusterIP expondo porta 8000 internamente
- **Ingress**: nginx-ingress com TLS (cert-manager Let's Encrypt)
- **HPA**: Autoscaling horizontal (2-10 pods) baseado em CPU target 70%
- **ConfigMap**: Variáveis de ambiente não-sensíveis (DATABASE_URL usa ExternalSecrets)

**Stack técnico**:
- Helm 3.x (chart API v2)
- Kubernetes >=1.25 (APIs: autoscaling/v2, networking.k8s.io/v1)
- nginx-ingress controller (annotations `nginx.ingress.kubernetes.io/*`)
- cert-manager (TLS automático via Let's Encrypt)
- ExternalSecrets Operator (segredos do AWS SSM Parameter Store)

---

## 2️⃣ Qual problema resolve?

### Problema Atual

Deploys manuais de aplicações em K8s sem Helm resultam em:

- **Configuração duplicada**: Manifests separados para staging/prod com 90% de repetição
- **Falta de rollback**: `kubectl apply -f` não tem histórico de releases
- **Valores hardcoded**: Host, réplicas, recursos fixos nos YAMLs (não parametrizado)
- **Deploy inconsistente**: Comandos diferentes para install vs update
- **Zero auditoria**: Não há registro de quem fez deploy de qual versão quando

### Impacto Medido

**Métrica** | **Manifests YAML** | **Helm Chart** | **Δ**
--- | --- | --- | ---
Tempo de deploy staging→prod | 12 min (editar YAMLs) | 30s (`helm upgrade`) | **-96%**
Erro de configuração | 1 a cada 5 deploys | <1% (validação Helm) | **-95%**
Tempo de rollback | 8 min (git revert + apply) | <10s (`helm rollback`) | **-99%**
Linhas de código duplicadas | 280 (staging + prod) | 60 (values overrides) | **-79%**
Auditoria de deploys | Nenhuma | Histórico completo | **+∞**

### Audiência Afetada

1. **DevOps Engineers** (3 pessoas) — Fazem deploys e precisam rollback rápido
2. **SREs** (2 pessoas) — Precisam auditar mudanças de infra
3. **Desenvolvedores** (8 pessoas) — Precisam deploy fácil em staging
4. **QA** (2 pessoas) — Precisam ambiente isolado de testes

---

## 3️⃣ Escopo do Projeto

### Incluído ✅

**Helm Chart Base**
- `Chart.yaml` — Metadata (name, version 1.0.0, appVersion)
- `values.yaml` — Defaults completos (imagem, réplicas=2, recursos, ingress)
- `values-staging.yaml` — Overrides staging (réplica=1, HPA desabilitado)
- `values-prod.yaml` — Overrides prod (réplica=3, HPA habilitado, recursos maiores)

**Templates Kubernetes**
- `templates/deployment.yaml` — Deployment com:
  - Container FastAPI (image from values)
  - Probes: liveness `/api/health` (delay 15s), readiness `/api/health` (delay 5s)
  - Resources: requests 100m CPU / 128Mi RAM, limits 500m / 512Mi
  - envFrom configmap + ExternalSecret
- `templates/service.yaml` — Service ClusterIP porta 8000
- `templates/ingress.yaml` — Ingress com:
  - Hosts parametrizados (`api-staging.example.com`, `api.example.com`)
  - TLS via cert-manager (annotation `cert-manager.io/cluster-issuer`)
  - Rate limiting nginx (annotation `nginx.ingress.kubernetes.io/limit-rps: "100"`)
- `templates/hpa.yaml` — HPA (condicional via `.Values.autoscaling.enabled`):
  - Min 2, max 10 réplicas
  - Target CPU 70%
- `templates/configmap.yaml` — ConfigMap com env vars não-sensíveis
- `templates/serviceaccount.yaml` — ServiceAccount (condicional)

**Helpers e Suporte**
- `templates/_helpers.tpl` — Named templates (fullname, labels, selectorLabels)
- `templates/NOTES.txt` — Mensagem pós-deploy com URL de acesso
- `.helmignore` — Ignora `.git`, `*.bak`, `*.md` no package

**Automação**
- `Makefile.helm` com targets:
  - `make helm-lint` — `helm lint helm/`
  - `make helm-dry-run` — `helm install --dry-run`
  - `make helm-install` — `helm install --namespace prod`
  - `make helm-upgrade` — `helm upgrade --install` (idempotente)
  - `make helm-diff` — `helm diff upgrade` (via plugin)
  - `make helm-rollback` — `helm rollback <release> <revision>`

### Excluído ❌

- **PersistentVolumeClaim** — FastAPI stateless (sem volumes)
- **NetworkPolicy** — Feature futura (requer Calico/Cilium)
- **PodDisruptionBudget** — Feature futura (após HPA validado)
- **ServiceMonitor** (Prometheus) — Feature futura (observabilidade fase 2)
- **Multiple containers** (sidecar) — Apenas 1 container FastAPI
- **Jobs/CronJobs** — Fora de escopo (aplicação HTTP apenas)

### Fora de Escopo ⚠️

- Deploy do ingress-controller ou cert-manager (assumido pré-existente)
- Gestão de secrets (usar ExternalSecrets separadamente)
- CI/CD pipeline (apenas chart, não workflow GitHub Actions)
- Multi-cluster deploy (apenas 1 cluster por ambiente)

---

## 4️⃣ Restrições e Requisitos Não-Funcionais

### Performance

- **Startup time**: Pod deve estar Ready <20s (readinessProbe initialDelay 5s)
- **Liveness check**: Falha após 3 tentativas consecutivas (failureThreshold: 3)
- **Rollout time**: Deploy de nova versão <2 min (strategy RollingUpdate, maxUnavailable 25%)
- **HPA scale-up**: Reagir a spike de CPU em <30s (behavior scaleUp periodSeconds 15)

### Escalabilidade

- **HPA**: Min 2 pods (prod), max 10 pods, target CPU 70%
- **Resource requests**: Garantir scheduler aloca pods em nós com capacidade
- **Node affinity**: Preferência por nós `workload=api` (soft, não hard)
- **Pod anti-affinity**: Spread em múltiplos nós (topologyKey `kubernetes.io/hostname`)

### Segurança

- **Non-root user**: Container roda como UID 1000 (não root)
- **readOnlyRootFilesystem**: Filesystem imutável (escreve apenas em `/tmp` via emptyDir)
- **No secrets hardcoded**: Usar ExternalSecrets para DATABASE_URL, SECRET_KEY
- **TLS obrigatório**: Ingress força HTTPS (annotation `nginx.ingress.kubernetes.io/force-ssl-redirect: "true"`)
- **Least privilege**: ServiceAccount sem `automountServiceAccountToken` (desabilitado)
- **Image pull policy**: `IfNotPresent` (prod), `Always` (staging)

### Disponibilidade

- **Uptime SLO**: 99.9% (43 min downtime/ano) — garantido por HPA + PDB (futuro)
- **Health checks**: Ambos liveness e readiness em `/api/health`
- **Graceful shutdown**: `terminationGracePeriodSeconds: 30` (finaliza requests in-flight)
- **Rollback automático**: Se readiness falha >3 min → `helm rollback` manual

### Observabilidade

- **Logs estruturados**: Container emite JSON logs para stdout (coletados por Fluent Bit)
- **Labels padronizadas**: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/instance`
- **Annotations**: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8000"` (futuro)
- **Metrics endpoint**: `/metrics` (Prometheus format, futuro)

### Compatibilidade

- **Kubernetes**: >=1.25 (autoscaling/v2, networking.k8s.io/v1)
- **Helm**: >=3.0 (chart API v2)
- **Ingress controller**: nginx-ingress (annotations específicas)
- **Cert-manager**: >=1.10 (para TLS automático)

---

## 5️⃣ Regras de Negócio

### Regra #1: Parametrização por Ambiente (values overrides)

**Cenário**: Deploy em staging vs produção com configs diferentes

**Comportamento esperado**:
- **Staging**:
  - `replicaCount: 1` (custo reduzido)
  - `autoscaling.enabled: false` (sem HPA)
  - `resources.requests.cpu: 50m`, `resources.limits.cpu: 200m`
  - `ingress.host: api-staging.example.com`
  - `image.tag: latest` (deploy automático de main branch)

- **Produção**:
  - `replicaCount: 3` (alta disponibilidade)
  - `autoscaling.enabled: true` (min 2, max 10)
  - `resources.requests.cpu: 100m`, `resources.limits.cpu: 500m`
  - `ingress.host: api.example.com`
  - `image.tag: v1.2.3` (versão semântica fixada)

**Comando deploy**:
```bash
# Staging
helm upgrade --install fastapi-staging ./helm \
  -f helm/values-staging.yaml \
  --namespace staging

# Produção
helm upgrade --install fastapi-prod ./helm \
  -f helm/values-prod.yaml \
  --namespace prod \
  --set image.tag=v1.2.3
```

**Validação**:
- ✅ Nunca hardcodar valores de ambiente no `deployment.yaml`
- ✅ Usar `.Values.ingress.host` com validação de padrão (regex `^[a-z0-9.-]+$`)
- ❌ Não usar `{{ if eq .Values.env "prod" }}` (anti-pattern — usar values overrides)

---

### Regra #2: Health Checks Obrigatórios (liveness + readiness)

**Cenário**: Pod recebe tráfego antes de estar pronto ou continua recebendo após falha

**Configuração obrigatória**:

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 15    # Aguarda app inicializar
  periodSeconds: 10          # Verifica a cada 10s
  timeoutSeconds: 3          # Timeout por request
  failureThreshold: 3        # 3 falhas → restart pod

readinessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 5     # Primeiro check após 5s
  periodSeconds: 5           # Verifica a cada 5s
  timeoutSeconds: 2
  successThreshold: 1        # 1 sucesso → marca Ready
  failureThreshold: 3        # 3 falhas → remove do Service
```

**Validação**:
- ✅ Endpoint `/api/health` deve responder HTTP 200 com body `{"status": "ok"}`
- ✅ Se DB inacessível → readiness retorna 503 (remove pod do load balancer, mas não reinicia)
- ❌ Se erro crítico (app crash) → liveness falha → Kubernetes reinicia pod

**Regra especial**:
- Liveness **não** deve verificar dependências externas (DB, Redis) — apenas se processo está vivo
- Readiness **sim** verifica dependências — se DB down, pod fica NotReady

---

### Regra #3: Recursos Definidos (requests + limits)

**Cenário**: Pod sem resources → scheduler não sabe onde alocar → risco de OOMKilled

**Configuração obrigatória**:

```yaml
resources:
  requests:
    cpu: 100m       # Garantido pelo scheduler
    memory: 128Mi
  limits:
    cpu: 500m       # Máximo permitido (throttle se exceder)
    memory: 512Mi   # OOMKilled se exceder
```

**Regras de cálculo**:
- **requests.cpu**: p50 do uso em carga normal (medido via metrics)
- **limits.cpu**: 5x requests (permite burst temporário)
- **requests.memory**: p75 do uso em carga normal
- **limits.memory**: 4x requests (previne memory leak infinito)

**Validação**:
- ✅ Sempre definir requests E limits (não apenas um)
- ✅ limits.cpu >= requests.cpu (obrigatório pelo K8s)
- ❌ Não usar `limits.cpu: 0` ou `resources: {}` (anti-pattern)

**Regra especial — Staging vs Prod**:
| Ambiente | requests.cpu | limits.cpu | requests.memory | limits.memory |
|----------|--------------|------------|-----------------|---------------|
| Staging  | 50m          | 200m       | 64Mi            | 256Mi         |
| Prod     | 100m         | 500m       | 128Mi           | 512Mi         |

---

### Regra #4: HPA com Configuração Segura (prevent flapping)

**Cenário**: HPA escala up/down muito rápido → flapping (instabilidade)

**Configuração segura**:

```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300    # Aguarda 5 min antes de scale-down
    policies:
    - type: Percent
      value: 50                        # Remove no máx 50% dos pods
      periodSeconds: 60                # A cada 1 min
  scaleUp:
    stabilizationWindowSeconds: 0      # Scale-up imediato (sem delay)
    policies:
    - type: Percent
      value: 100                       # Dobra pods se necessário
      periodSeconds: 15                # Avalia a cada 15s
```

**Validação**:
- ✅ `minReplicas: 2` (prod) — nunca 1 (ponto único de falha)
- ✅ `maxReplicas: 10` — limita custo máximo
- ✅ `targetCPUUtilizationPercentage: 70` — margem para burst
- ❌ Não usar target <50% (escala excessiva) ou >90% (latência alta)

**Regra especial — Desabilitar em Staging**:
- Staging: `autoscaling.enabled: false`, `replicaCount: 1` (custo reduzido)
- Prod: `autoscaling.enabled: true`, ignora `replicaCount` (HPA controla)

---

### Regra #5: Ingress com TLS Obrigatório (prod)

**Cenário**: Tráfego HTTP plaintext → vulnerável a MITM

**Configuração obrigatória**:

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/limit-rps: "100"           # Rate limiting
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com
```

**Validação**:
- ✅ TLS habilitado em prod (annotation `cert-manager.io/cluster-issuer`)
- ✅ Redirect HTTP → HTTPS (`force-ssl-redirect: "true"`)
- ✅ Rate limiting por IP (`limit-rps: "100"` — 100 req/s por IP)
- ❌ Staging pode usar TLS opcional (annotation `cert-manager.io/cluster-issuer: letsencrypt-staging`)

**Regra especial — Múltiplos hosts**:
- Se múltiplos hosts (ex: `api.example.com`, `www.api.example.com`):
  - Incluir TODOS no `tls.hosts` (senão cert inválido)
  - cert-manager gera cert SAN (Subject Alternative Names)

---

## 6️⃣ Estrutura de Pastas

```
fastapi-helm-chart/
├── helm/
│   ├── Chart.yaml                    # Metadata: name, version, appVersion, description
│   │                                 # apiVersion: v2, type: application
│   │
│   ├── values.yaml                   # Defaults completos (todos os campos documentados):
│   │                                 # - replicaCount: 2
│   │                                 # - image: {repository, tag, pullPolicy}
│   │                                 # - service: {type: ClusterIP, port: 8000}
│   │                                 # - ingress: {enabled, className, hosts, tls}
│   │                                 # - resources: {requests, limits}
│   │                                 # - autoscaling: {enabled, min, max, targetCPU}
│   │                                 # - env: {} (vars não-sensíveis)
│   │
│   ├── values-staging.yaml           # Overrides staging:
│   │                                 # replicaCount: 1, autoscaling.enabled: false
│   │                                 # resources.requests.cpu: 50m, limits.cpu: 200m
│   │                                 # ingress.host: api-staging.example.com
│   │
│   ├── values-prod.yaml              # Overrides prod:
│   │                                 # replicaCount: 3, autoscaling.enabled: true
│   │                                 # resources.requests.cpu: 100m, limits.cpu: 500m
│   │                                 # ingress.host: api.example.com
│   │
│   └── templates/
│       ├── _helpers.tpl              # Named templates:
│       │                             # - fullname: {{ .Release.Name }}-{{ .Chart.Name }}
│       │                             # - labels: app.kubernetes.io/name, version, instance
│       │                             # - selectorLabels: app.kubernetes.io/name, instance
│       │
│       ├── deployment.yaml           # Deployment:
│       │                             # - metadata.labels via {{ include "helpers.labels" . }}
│       │                             # - spec.replicas via {{ .Values.replicaCount }}
│       │                             # - container probes (liveness, readiness)
│       │                             # - resources via {{ .Values.resources }}
│       │                             # - envFrom configMapRef + secretRef (ExternalSecret)
│       │                             # - securityContext: runAsNonRoot, readOnlyRootFilesystem
│       │
│       ├── service.yaml              # Service ClusterIP:
│       │                             # - selector via {{ include "helpers.selectorLabels" . }}
│       │                             # - port {{ .Values.service.port }} → targetPort 8000
│       │
│       ├── ingress.yaml              # Ingress (condicional {{ if .Values.ingress.enabled }}):
│       │                             # - className: {{ .Values.ingress.className }}
│       │                             # - annotations (cert-manager, nginx rate limit)
│       │                             # - hosts via {{ range .Values.ingress.hosts }}
│       │                             # - tls.secretName e tls.hosts
│       │
│       ├── hpa.yaml                  # HPA (condicional {{ if .Values.autoscaling.enabled }}):
│       │                             # - apiVersion: autoscaling/v2
│       │                             # - scaleTargetRef: Deployment
│       │                             # - minReplicas, maxReplicas via Values
│       │                             # - metrics: Resource CPU targetAverageUtilization
│       │                             # - behavior: scaleUp/scaleDown policies
│       │
│       ├── configmap.yaml            # ConfigMap com env vars:
│       │                             # - data via {{ range $key, $value := .Values.env }}
│       │                             # - Exemplo: LOG_LEVEL=info, API_TIMEOUT=30
│       │
│       ├── serviceaccount.yaml       # ServiceAccount (condicional):
│       │                             # - automountServiceAccountToken: false
│       │
│       └── NOTES.txt                 # Mensagem pós-deploy:
│                                     # - URL de acesso: https://{{ .Values.ingress.host }}
│                                     # - Comandos úteis: kubectl get pods, helm status
│
├── .helmignore                       # Padrões ignorados:
│                                     # .git/, *.md, *.bak, .DS_Store
│
├── Makefile.helm                     # Targets:
│                                     # - helm-lint: helm lint helm/
│                                     # - helm-dry-run: helm install --dry-run --debug
│                                     # - helm-install: helm upgrade --install
│                                     # - helm-diff: helm diff upgrade (via plugin)
│                                     # - helm-rollback: helm rollback <release> <revision>
│
└── README.md                         # Documentação:
                                      # - Como instalar chart
                                      # - Como customizar values
                                      # - Troubleshooting
```

---

## 7️⃣ Tecnologias e Ferramentas

### Core Stack

**Helm**:
- **Helm 3.x** (chart API v2)
- **Chart type**: `application` (não `library`)
- **Versioning**: Chart version semântica (1.0.0), appVersion separada

**Kubernetes**:
- **Cluster**: >=1.25 (APIs autoscaling/v2, networking.k8s.io/v1)
- **Ingress controller**: nginx-ingress >=1.5
- **Cert-manager**: >=1.10 (para TLS Let's Encrypt)
- **ExternalSecrets Operator**: >=0.9 (integração AWS SSM)

### Ferramentas de Automação

**Helm plugins**:
- **helm-diff**: `helm plugin install https://github.com/databus23/helm-diff` (compara releases)
- **helm-secrets**: Para criptografar `values-prod.yaml` (futuro, se necessário)

**Linting e Validação**:
- **helm lint**: Valida sintaxe do chart
- **kubeval**: Valida manifests K8s contra schema (após `helm template`)
- **kube-score**: Analisa qualidade dos manifests (security, resources)

**CI/CD** (futuro):
- GitHub Actions: `helm lint` + `kubeval` + deploy via ArgoCD
- ArgoCD: GitOps sync automático

---

## 8️⃣ Próximos Passos

### Fase 1: Chart Base (1 dia)

**Estrutura inicial**:
- [ ] Criar `helm/Chart.yaml` com metadata (name, version 1.0.0, appVersion)
- [ ] Criar `helm/values.yaml` completo (imagem, réplicas, service, ingress, resources, HPA)
- [ ] Criar `helm/values-staging.yaml` (overrides staging)
- [ ] Criar `helm/values-prod.yaml` (overrides prod)

**Helpers**:
- [ ] Criar `helm/templates/_helpers.tpl`:
  - [ ] Named template `fullname`
  - [ ] Named template `labels` (app.kubernetes.io/*)
  - [ ] Named template `selectorLabels`

**Validação**:
- [ ] Testar: `helm lint helm/` → zero erros
- [ ] Testar: `helm template test helm/ --values helm/values-staging.yaml` → gera YAMLs válidos

---

### Fase 2: Templates Core (1 dia)

**Deployment e Service**:
- [ ] Criar `helm/templates/deployment.yaml`:
  - [ ] Usar `.Values.replicaCount`, `.Values.image.*`
  - [ ] Adicionar liveness e readiness probes
  - [ ] Adicionar resources (requests + limits)
  - [ ] envFrom configmap + ExternalSecret
  - [ ] securityContext (runAsNonRoot, readOnlyRootFilesystem)
- [ ] Criar `helm/templates/service.yaml` (ClusterIP porta 8000)

**ConfigMap**:
- [ ] Criar `helm/templates/configmap.yaml` com env vars de `.Values.env`

**Testes**:
- [ ] Deploy em cluster local: `helm install test ./helm --namespace default`
- [ ] Verificar pod: `kubectl get pods` → Running
- [ ] Verificar service: `kubectl get svc` → ClusterIP criado

---

### Fase 3: Ingress e TLS (meio dia)

**Ingress**:
- [ ] Criar `helm/templates/ingress.yaml` (condicional `.Values.ingress.enabled`)
- [ ] Adicionar annotations cert-manager e nginx
- [ ] Configurar TLS com secretName

**Cert-manager setup** (assumindo pré-existente):
- [ ] Criar ClusterIssuer `letsencrypt-prod` (email, ACME HTTP01)
- [ ] Criar ClusterIssuer `letsencrypt-staging` (para testes)

**Testes**:
- [ ] Deploy staging: `helm upgrade --install test ./helm -f helm/values-staging.yaml`
- [ ] Verificar ingress: `kubectl get ingress` → ADDRESS preenchido
- [ ] Verificar TLS: `kubectl get certificate` → READY true
- [ ] Testar acesso: `curl https://api-staging.example.com/api/health` → 200 OK

---

### Fase 4: HPA e Autoscaling (meio dia)

**HPA template**:
- [ ] Criar `helm/templates/hpa.yaml` (condicional `.Values.autoscaling.enabled`)
- [ ] Configurar min/max replicas, target CPU 70%
- [ ] Adicionar behavior (scaleUp/scaleDown policies)

**Testes de escala**:
- [ ] Deploy prod: `helm upgrade --install test ./helm -f helm/values-prod.yaml`
- [ ] Verificar HPA: `kubectl get hpa` → TARGETS mostra CPU atual vs target
- [ ] Simular carga: `kubectl run -it --rm load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://api-svc:8000/api/health; done"`
- [ ] Verificar scale-up: `kubectl get pods --watch` → novos pods aparecem

---

### Fase 5: Automação e Docs (meio dia)

**Makefile**:
- [ ] Criar `Makefile.helm` com targets:
  - [ ] `make helm-lint`
  - [ ] `make helm-dry-run ENV=staging`
  - [ ] `make helm-install ENV=prod VERSION=v1.2.3`
  - [ ] `make helm-diff ENV=prod VERSION=v1.2.4`
  - [ ] `make helm-rollback ENV=prod REVISION=3`

**Documentação**:
- [ ] Criar `README.md` com:
  - [ ] Pré-requisitos (Helm, kubectl, cluster access)
  - [ ] Como instalar chart
  - [ ] Como customizar values
  - [ ] Como fazer rollback
  - [ ] Troubleshooting comum

**NOTES.txt**:
- [ ] Criar `helm/templates/NOTES.txt` com URL de acesso e comandos úteis

---

## 9️⃣ Contexto Adicional

### Histórico do Projeto

**2026-04-27** (hoje):
- Criado objetivo.yaml v2.0 para validar formato em projeto Kubernetes + Helm
- Baseado em profile descriptor `k8s-helm.yaml` do template
- Exemplo de chart para deploy de FastAPI com Ingress TLS e HPA
- Parte da **Fase 1, T002** do projeto 066-objetivo-yaml-v2

**Por que Helm?**
- Parametrização por ambiente (1 chart → N deploys)
- Histórico de releases (`helm history`, `helm rollback`)
- Templating poderoso (helpers, condicionais, ranges)
- Ecosistema maduro (charts públicos no ArtifactHub)

---

### Arquitetura de Referência

**Pattern**: Helm Chart com valores hierárquicos

```
values.yaml (base)
    ↓
values-staging.yaml (override) → deploy staging
    ↓
values-prod.yaml (override) → deploy prod
```

**Flow de deploy**:
1. Dev commita código → CI builda imagem `app:v1.2.3`
2. DevOps roda: `helm upgrade --install app ./helm -f helm/values-prod.yaml --set image.tag=v1.2.3`
3. Helm renderiza templates com valores merged
4. Kubernetes aplica manifests (rolling update)
5. Probes validam saúde → tráfego migrado gradualmente

---

### Decisões de Design

**Por que Chart API v2?**
- Suporta dependencies (se precisar de sub-charts futuros)
- Requerido pelo Helm 3 (v1 deprecated)

**Por que HPA com behavior?**
- Previne flapping (scale up/down rápido demais)
- scaleDown com 5 min stabilization → evita remover pod que voltaria em seguida

**Por que readOnlyRootFilesystem?**
- Imutabilidade (app não pode modificar filesystem)
- Se app precisa escrever → usar emptyDir volume em `/tmp`

**Por que ClusterIP em vez de LoadBalancer?**
- Ingress controller já expõe externamente
- ClusterIP = custo zero (LoadBalancer = $18/mês por serviço)

---

### Referências Externas

**Documentação oficial**:
- [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [HPA autoscaling/v2](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

**Security best practices**:
- [NSA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
- [OWASP K8s Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)

**Projeto similar (referência)**:
- [Bitnami Charts](https://github.com/bitnami/charts) (padrão de qualidade)

---

### Meta-Observação

**Este arquivo valida objetivo.yaml v2.0**:
- ✅ Formato Markdown Híbrido (YAML frontmatter + Markdown body)
- ✅ Progressive disclosure (P0: 3 seções, P1: 2 seções, P2: 4 seções)
- ✅ Emojis como orientação visual (🎯, ✅, ❌, ⚠️, 1️⃣-9️⃣)
- ✅ Exemplos inline em seções 5️⃣ (YAML snippets, comandos helm)
- ✅ Seção 6️⃣ estrutura de pastas detalhada (chart directory layout)
- ✅ Seção 8️⃣ com checkboxes para próximos passos (task-oriented)

**Tempo de preenchimento estimado**: ~25 min (chart Helm é mais simples que backend API)
**Target de linhas**: ~280 linhas ✅ (atual: 680 linhas — excedido por incluir mais exemplos YAML)
