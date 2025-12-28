#!/usr/bin/env bash
# Deploy application using Helm or docker-compose
# Called by ship.sh for --only deploy or full cycle

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# =============================================================================
# CONFIGURATION
# =============================================================================

ENV=""
CONFIG=""
STATE_DIR=""
GIT_SHA=""
FEATURE_SLUG=""
DRY_RUN=false
VERBOSE=false

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --state-dir)
            STATE_DIR="$2"
            shift 2
            ;;
        --git-sha)
            GIT_SHA="$2"
            shift 2
            ;;
        --feature-slug)
            FEATURE_SLUG="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log() {
    echo "[deploy] $1"
}

log_verbose() {
    [[ "$VERBOSE" == "true" ]] && echo "[deploy:verbose] $1"
}

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

check_deployed_version() {
    local version_file="$STATE_DIR/deployed-version.json"

    if [[ ! -f "$version_file" ]]; then
        log "No existing deployment found"
        return 1
    fi

    local deployed_sha=$(jq -r '.git_sha' "$version_file" 2>/dev/null || echo "")

    if [[ "$deployed_sha" == "$GIT_SHA" ]]; then
        log "Version $GIT_SHA already deployed"
        return 0
    fi

    log "Current deployed version: $deployed_sha"
    log "New version to deploy: $GIT_SHA"
    return 1
}

save_deployed_version() {
    local version_file="$STATE_DIR/deployed-version.json"
    local namespace="$1"

    cat > "$version_file" << EOF
{
  "git_sha": "$GIT_SHA",
  "feature_slug": "$FEATURE_SLUG",
  "namespace": "$namespace",
  "environment": "$ENV",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

    log "Saved deployment version to $version_file"
}

# =============================================================================
# LOCAL DEPLOYMENT (docker-compose)
# =============================================================================

deploy_local() {
    log "Deploying to local environment..."

    local repo_root=$(get_repo_root)
    local compose_dir="$repo_root/.speckit/local"
    local compose_file="$compose_dir/docker-compose.yml"

    mkdir -p "$compose_dir"

    # Check for existing docker-compose.yml
    local source_compose=""
    if [[ -f "$repo_root/docker-compose.yml" ]]; then
        source_compose="$repo_root/docker-compose.yml"
    elif [[ -f "$repo_root/docker-compose.yaml" ]]; then
        source_compose="$repo_root/docker-compose.yaml"
    fi

    if [[ -n "$source_compose" ]]; then
        # Use existing docker-compose
        log "Using existing docker-compose from $source_compose"
        cp "$source_compose" "$compose_file"
    else
        # Generate from deploy.yaml
        log "Generating docker-compose.yml..."
        generate_docker_compose "$compose_file"
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Dry run - would execute:"
        echo "  docker-compose -f $compose_file up -d"
        return 0
    fi

    # Start services
    log "Starting local services..."
    docker-compose -f "$compose_file" up -d --build

    # Wait for health
    log "Waiting for services to be healthy..."
    sleep 5

    # Check status
    docker-compose -f "$compose_file" ps

    save_deployed_version "local"

    log "Local deployment complete"
    log "Application available at: http://localhost:8080"
}

generate_docker_compose() {
    local output_file="$1"

    cat > "$output_file" << 'EOF'
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: app_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: localdev
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Application
  app:
    build:
      context: ../..
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      NODE_ENV: development
      DATABASE_URL: postgres://postgres:localdev@postgres:5432/app_dev
      REDIS_URL: redis://redis:6379
      DEBUG: "true"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres-data:
  redis-data:
EOF
}

# =============================================================================
# KUBERNETES DEPLOYMENT (Helm)
# =============================================================================

deploy_kubernetes() {
    log "Deploying to Kubernetes ($ENV)..."

    local repo_root=$(get_repo_root)
    local namespace="staging-$FEATURE_SLUG"
    local release_name="app"

    # Production uses fixed namespace
    if [[ "$ENV" == "production" ]]; then
        namespace="production"
    fi

    log "Target namespace: $namespace"

    # Check for Helm chart
    local chart_path="$repo_root/helm/app"
    if [[ ! -d "$chart_path" ]]; then
        log "Helm chart not found at $chart_path"
        log "Creating basic Helm chart..."
        create_helm_chart "$chart_path"
    fi

    # Create namespace if not exists
    if [[ "$DRY_RUN" != "true" ]]; then
        kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f -
    fi

    # Load infrastructure outputs
    local infra_outputs="$STATE_DIR/infra-outputs.json"
    local db_host=""
    local redis_host=""

    if [[ -f "$infra_outputs" ]]; then
        db_host=$(jq -r '.database_host.value // empty' "$infra_outputs" 2>/dev/null || echo "")
        redis_host=$(jq -r '.redis_host.value // empty' "$infra_outputs" 2>/dev/null || echo "")
    fi

    # Build Helm command
    local helm_cmd="helm upgrade --install $release_name $chart_path"
    helm_cmd+=" --namespace $namespace"
    helm_cmd+=" --set image.tag=$GIT_SHA"
    helm_cmd+=" --set ingress.host=$FEATURE_SLUG.$ENV.example.com"
    helm_cmd+=" --set replicaCount=2"

    # Add values files if they exist
    local base_values="$repo_root/helm/values/base.yaml"
    local env_values="$repo_root/helm/values/$ENV.yaml"

    [[ -f "$base_values" ]] && helm_cmd+=" --values $base_values"
    [[ -f "$env_values" ]] && helm_cmd+=" --values $env_values"

    # Add infrastructure connections if available
    [[ -n "$db_host" ]] && helm_cmd+=" --set env.DATABASE_HOST=$db_host"
    [[ -n "$redis_host" ]] && helm_cmd+=" --set env.REDIS_HOST=$redis_host"

    # Deployment options
    helm_cmd+=" --wait --timeout=5m"
    helm_cmd+=" --atomic"

    if [[ "$DRY_RUN" == "true" ]]; then
        helm_cmd+=" --dry-run"
        log "Dry run - would execute:"
        echo "  $helm_cmd"
    fi

    log "Deploying with Helm..."
    log_verbose "Command: $helm_cmd"

    eval "$helm_cmd"

    if [[ "$DRY_RUN" != "true" ]]; then
        # Wait for rollout
        log "Waiting for rollout to complete..."
        kubectl rollout status deployment/$release_name -n "$namespace" --timeout=5m

        save_deployed_version "$namespace"
    fi

    log "Kubernetes deployment complete"
    log "Application available at: https://$FEATURE_SLUG.$ENV.example.com"
}

create_helm_chart() {
    local chart_path="$1"

    mkdir -p "$chart_path/templates"

    # Chart.yaml
    cat > "$chart_path/Chart.yaml" << 'EOF'
apiVersion: v2
name: app
description: Application Helm chart generated by speckit
type: application
version: 1.0.0
appVersion: "1.0.0"
EOF

    # values.yaml
    cat > "$chart_path/values.yaml" << 'EOF'
replicaCount: 2

image:
  repository: app
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  host: app.example.com
  tls:
    enabled: true

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

env: {}

livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
EOF

    # Deployment template
    cat > "$chart_path/templates/deployment.yaml" << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
    app: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.targetPort }}
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe | nindent 12 }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe | nindent 12 }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
EOF

    # Service template
    cat > "$chart_path/templates/service.yaml" << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
  selector:
    app: {{ .Release.Name }}
EOF

    # Ingress template
    cat > "$chart_path/templates/ingress.yaml" << 'EOF'
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  {{- if .Values.ingress.tls.enabled }}
  tls:
    - hosts:
        - {{ .Values.ingress.host }}
      secretName: {{ .Release.Name }}-tls
  {{- end }}
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ .Release.Name }}
                port:
                  number: {{ .Values.service.port }}
{{- end }}
EOF

    log "Created basic Helm chart at $chart_path"
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    if [[ -z "$ENV" || -z "$STATE_DIR" ]]; then
        echo "Missing required arguments" >&2
        exit 1
    fi

    log "Deploying application for environment: $ENV"
    log_verbose "Config: $CONFIG"
    log_verbose "Git SHA: $GIT_SHA"
    log_verbose "Feature slug: $FEATURE_SLUG"

    # Check if already deployed
    if check_deployed_version; then
        log "Skipping deploy - version already deployed"
        exit 0
    fi

    # Deploy based on environment
    case "$ENV" in
        local)
            deploy_local
            ;;
        staging|production)
            deploy_kubernetes
            ;;
        *)
            log "Unknown environment: $ENV"
            exit 1
            ;;
    esac

    log "Deploy complete"
}

main "$@"
