# Kubernetes Deployment

This directory contains Kubernetes manifests for deploying llmplan directly without Helm.

## Files

- `manifests/namespace.yaml` - Namespace for llmplan
- `manifests/serviceaccount.yaml` - Service account
- `manifests/deployment.yaml` - Application deployment
- `manifests/service.yaml` - Service and LMStudio external service

## Quick Deploy

```bash
# Apply all manifests
kubectl apply -f k8s/manifests/

# Check deployment status
kubectl get pods -n llmplan

# Check service
kubectl get svc -n llmplan

# View logs
kubectl logs -f deployment/llmplan -n llmplan
```

## Port Forward for Testing

```bash
kubectl port-forward svc/llmplan 8000:8000 -n llmplan
```

Then test:

```bash
curl http://localhost:8000/api/v1/summary/health
```

## Cleanup

```bash
kubectl delete -f k8s/manifests/
```

## Notes

- Make sure to update the LMStudio service external name in `service.yaml` to point to your actual LMStudio host
- Adjust resource limits in `deployment.yaml` based on your cluster capacity
