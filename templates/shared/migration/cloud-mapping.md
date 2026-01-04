# Cloud Service Mapping Reference

## Overview

This reference provides service equivalents across major cloud providers to facilitate migration planning and multi-cloud architecture decisions.

---

## SERVICE_EQUIVALENTS

### Core Infrastructure Services

| Service Category | AWS | GCP | Azure | VK Cloud |
|------------------|-----|-----|-------|----------|
| **postgresql** | RDS PostgreSQL | Cloud SQL PostgreSQL | Azure Database for PostgreSQL | VK Cloud Databases (PostgreSQL) |
| **mysql** | RDS MySQL | Cloud SQL MySQL | Azure Database for MySQL | VK Cloud Databases (MySQL) |
| **redis** | ElastiCache for Redis | Memorystore for Redis | Azure Cache for Redis | VK Cloud Redis |
| **mongodb** | DocumentDB | MongoDB Atlas (Partner) | Cosmos DB (MongoDB API) | VK Cloud MongoDB |
| **kubernetes** | EKS | GKE | AKS | VK Cloud Kubernetes |
| **object-storage** | S3 | Cloud Storage | Blob Storage | VK Cloud S3 |
| **message-queue** | SQS | Pub/Sub | Azure Queue Storage | VK Cloud Message Queue |
| **streaming** | MSK (Kafka) | Pub/Sub | Event Hubs | VK Cloud Kafka |
| **load-balancer** | ALB/NLB | Cloud Load Balancing | Azure Load Balancer | VK Cloud Load Balancer |
| **cdn** | CloudFront | Cloud CDN | Azure CDN | VK Cloud CDN |
| **dns** | Route 53 | Cloud DNS | Azure DNS | VK Cloud DNS |
| **secrets** | Secrets Manager | Secret Manager | Key Vault | VK Cloud Secrets |
| **functions** | Lambda | Cloud Functions | Azure Functions | VK Cloud Functions |
| **container-registry** | ECR | Artifact Registry | ACR | VK Cloud Registry |

### Compute Services

| Service Category | AWS | GCP | Azure | VK Cloud |
|------------------|-----|-----|-------|----------|
| **vm** | EC2 | Compute Engine | Virtual Machines | VK Cloud Compute |
| **spot-instances** | Spot Instances | Preemptible VMs | Spot VMs | VK Cloud Spot |
| **auto-scaling** | Auto Scaling Groups | Managed Instance Groups | VM Scale Sets | VK Cloud Auto Scaling |

### Networking Services

| Service Category | AWS | GCP | Azure | VK Cloud |
|------------------|-----|-----|-------|----------|
| **vpc** | VPC | VPC | Virtual Network | VK Cloud VPC |
| **firewall** | Security Groups | Firewall Rules | Network Security Groups | VK Cloud Firewall |
| **nat** | NAT Gateway | Cloud NAT | NAT Gateway | VK Cloud NAT |
| **vpn** | VPN Gateway | Cloud VPN | VPN Gateway | VK Cloud VPN |

---

## SERVICE_DISCOVERY

### Docker Compose Analysis

```yaml
# Parse docker-compose.yml to identify services
discovery:
  source: docker-compose.yml
  detection_rules:
    - image_pattern: "postgres:*" → postgresql
    - image_pattern: "redis:*" → redis
    - image_pattern: "mongo:*" → mongodb
    - image_pattern: "mysql:*" → mysql
    - image_pattern: "kafka:*" → streaming
    - image_pattern: "rabbitmq:*" → message-queue
    - image_pattern: "nginx:*" → load-balancer
    - image_pattern: "minio:*" → object-storage
    - port: 5432 → postgresql
    - port: 6379 → redis
    - port: 27017 → mongodb
    - port: 3306 → mysql
    - port: 9092 → streaming
```

### Kubernetes Manifest Analysis

```yaml
# Parse k8s manifests to identify services
discovery:
  sources:
    - "k8s/*.yaml"
    - "kubernetes/**/*.yaml"
    - "deploy/*.yaml"
  detection_rules:
    kind_mappings:
      - Deployment → compute (container workload)
      - StatefulSet → stateful-service (database, cache)
      - Service/LoadBalancer → load-balancer
      - Ingress → ingress-controller
      - PersistentVolumeClaim → storage
      - ConfigMap → configuration
      - Secret → secrets
    annotation_hints:
      - "kubernetes.io/ingress.class" → ingress type
      - "service.beta.kubernetes.io/aws-load-balancer-type" → AWS ALB/NLB
```

### Service Dependency Graph

```
# Output format for discovered services
services:
  - name: api-service
    type: compute
    dependencies: [postgresql, redis]
    ports: [8080]
    replicas: 3
  - name: postgresql
    type: database
    storage: 100Gi
    version: "15"
  - name: redis
    type: cache
    mode: cluster
    nodes: 3
```

---

## NETWORK_TOPOLOGY_PLANNING

### VPC Architecture Template

```yaml
network_topology:
  vpc:
    cidr: "10.0.0.0/16"
    region: "${TARGET_REGION}"

  subnets:
    public:
      - name: public-a
        cidr: "10.0.1.0/24"
        az: a
        resources: [load-balancer, nat-gateway, bastion]
      - name: public-b
        cidr: "10.0.2.0/24"
        az: b
        resources: [load-balancer]

    private:
      - name: private-app-a
        cidr: "10.0.10.0/24"
        az: a
        resources: [kubernetes-nodes, application-servers]
      - name: private-app-b
        cidr: "10.0.11.0/24"
        az: b
        resources: [kubernetes-nodes, application-servers]

    data:
      - name: private-data-a
        cidr: "10.0.20.0/24"
        az: a
        resources: [postgresql, redis, elasticsearch]
      - name: private-data-b
        cidr: "10.0.21.0/24"
        az: b
        resources: [postgresql-replica, redis-replica]

  security_groups:
    web:
      inbound:
        - port: 443, source: "0.0.0.0/0"
        - port: 80, source: "0.0.0.0/0"
    app:
      inbound:
        - port: 8080, source: sg:web
        - port: 22, source: sg:bastion
    database:
      inbound:
        - port: 5432, source: sg:app
        - port: 6379, source: sg:app
```

---

## COST_ESTIMATION

### Pricing Reference (Monthly, USD)

| Service | AWS (us-east-1) | GCP (us-central1) | Azure (eastus) | VK Cloud (ru-msk) |
|---------|-----------------|-------------------|----------------|-------------------|
| **PostgreSQL db.m5.large** | ~$140 | ~$130 | ~$145 | ~$90 |
| **Redis cache.m5.large** | ~$120 | ~$110 | ~$125 | ~$80 |
| **K8s cluster (3 nodes)** | ~$220 | ~$200 | ~$230 | ~$150 |
| **S3/Storage (100GB)** | ~$2.30 | ~$2.00 | ~$2.10 | ~$1.50 |
| **Load Balancer (ALB)** | ~$25 | ~$20 | ~$22 | ~$15 |
| **NAT Gateway** | ~$45 | ~$45 | ~$40 | ~$30 |

### Cost Calculation Template

```yaml
cost_estimation:
  services:
    - name: postgresql
      tier: production
      instance: db.m5.large
      storage_gb: 100
      monthly_cost:
        aws: 140
        gcp: 130
        azure: 145
        vk_cloud: 90

    - name: redis
      tier: production
      instance: cache.m5.large
      nodes: 3
      monthly_cost:
        aws: 360
        gcp: 330
        azure: 375
        vk_cloud: 240

    - name: kubernetes
      nodes: 5
      instance: m5.large
      monthly_cost:
        aws: 370
        gcp: 340
        azure: 385
        vk_cloud: 250

  totals:
    aws: 870
    gcp: 800
    azure: 905
    vk_cloud: 580

  recommendation: |
    Based on pricing analysis:
    - VK Cloud offers 33% savings vs AWS for RU-based workloads
    - GCP provides best balance of cost/features for global reach
    - AWS recommended for enterprise compliance requirements
```

### Data Transfer Costs

| Transfer Type | AWS | GCP | Azure | VK Cloud |
|---------------|-----|-----|-------|----------|
| Egress (per GB) | $0.09 | $0.12 | $0.087 | $0.05 |
| Inter-region | $0.02 | $0.01 | $0.02 | $0.01 |
| Intra-region | Free | Free | Free | Free |

---

## Usage Notes

1. **Service Discovery**: Run discovery against existing infrastructure before migration planning
2. **Network Planning**: Adapt CIDR ranges to avoid conflicts with existing networks
3. **Cost Estimation**: Prices are approximate; use provider calculators for precise quotes
4. **VK Cloud**: Recommended for RU-region workloads with data residency requirements
