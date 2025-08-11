# Helm Charts

This directory contains Helm charts for deploying llmplan to Kubernetes.

## Installation

### Add Helm Repository

```bash
helm repo add llmplan https://eun2ce.github.io/llmplan
helm repo update
```

### Install from Repository

```bash
# Install with default values
helm install llmplan llmplan/llmplan

# Install with custom values
helm install llmplan llmplan/llmplan -f my-values.yaml

# Install in specific namespace
helm install llmplan llmplan/llmplan --namespace llmplan --create-namespace
```

### Install from OCI Registry (Docker Hub)

```bash
# Install from OCI registry
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan

# With specific version
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan --version 0.1.0
```

### Install from Local Chart

```bash
# From the project root
helm install llmplan ./charts/llmplan

# With custom values
helm install llmplan ./charts/llmplan -f ./charts/llmplan/my-values.yaml
```

## Configuration

### Basic Configuration

```yaml
# my-values.yaml
image:
  tag: "latest"

replicaCount: 2

resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 1000m
    memory: 1Gi

config:
  lmstudio:
    baseUrl: "http://your-lmstudio-host:1234/v1"

lmstudio:
  externalName: "your-lmstudio-host.example.com"
```

### Ingress Configuration

```yaml
# Enable ingress
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: llmplan.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: llmplan-tls
      hosts:
        - llmplan.example.com
```

### Autoscaling

```yaml
# Enable HPA
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## Management

```bash
# Upgrade
helm upgrade llmplan llmplan/llmplan

# Check status
helm status llmplan

# Uninstall
helm uninstall llmplan

# List releases
helm list
```

## Development

```bash
# Lint chart
helm lint charts/llmplan

# Template and check output
helm template llmplan charts/llmplan

# Dry run
helm install llmplan charts/llmplan --dry-run --debug
```
