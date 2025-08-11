# LLMPlan Helm Charts

## Quick Start

### Install from OCI Registry

```bash
# Install directly from OCI registry
helm install my-llmplan oci://registry-1.docker.io/eunheejo/llmplan

# Or with specific version
helm install my-llmplan oci://registry-1.docker.io/eunheejo/llmplan --version 0.1.0
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
# Upgrade to latest version
helm upgrade my-llmplan oci://registry-1.docker.io/eunheejo/llmplan

# Or upgrade to specific version
helm upgrade my-llmplan oci://registry-1.docker.io/eunheejo/llmplan --version 0.1.1
```

## Uninstalling

```bash
helm uninstall my-llmplan
```
