# LLMPlan Helm Charts

## Quick Start

### Install from OCI Registry (Recommended)

```bash
# Add the Helm repository
helm repo add llmplan oci://registry-1.docker.io/eunheejo/llmplan

# Install the chart
helm install my-llmplan llmplan/llmplan
```

### Install from GitHub Pages

```bash
# Add the Helm repository
helm repo add llmplan https://eun2ce.github.io/llmplan

# Update repository
helm repo update

# Install the chart
helm install my-llmplan llmplan/llmplan
```

### Install from Local Chart

```bash
# Clone the repository
git clone https://github.com/eun2ce/llmplan.git
cd llmplan

# Install the chart
helm install my-llmplan charts/llmplan
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter               | Description                    | Default            |
| ----------------------- | ------------------------------ | ------------------ |
| `image.repository`      | Container image repository     | `eunheejo/llmplan` |
| `image.tag`             | Container image tag            | `latest`           |
| `service.type`          | Kubernetes service type        | `ClusterIP`        |
| `service.port`          | Service port                   | `8000`             |
| `lmstudio.enabled`      | Enable LMStudio service        | `true`             |
| `lmstudio.externalName` | External LMStudio service name | `""`               |

## LMStudio Configuration

### External LMStudio Service

If you have LMStudio running on a specific host:

```bash
helm install my-llmplan charts/llmplan \
  --set lmstudio.enabled=true \
  --set lmstudio.externalName=my-lmstudio-host.local
```

### Local LMStudio (Docker Desktop)

For local development with Docker Desktop:

```bash
helm install my-llmplan charts/llmplan \
  --set lmstudio.enabled=true
```

## Upgrading

```bash
# Update repository
helm repo update

# Upgrade release
helm upgrade my-llmplan llmplan/llmplan
```

## Uninstalling

```bash
helm uninstall my-llmplan
```
