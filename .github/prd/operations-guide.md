# LLMPlan 운영 가이드

## 🚀 배포 가이드

### 프로덕션 배포

#### 1. Helm을 통한 배포

```bash
# 네임스페이스 생성
kubectl create namespace llmplan

# Helm 차트 배포
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan \
  --set image.tag=v0.1.0 \
  --set resources.limits.memory=2Gi \
  --set resources.limits.cpu=1000m \
  --set lmstudio.externalName=lmstudio.internal.company.com

# 배포 상태 확인
helm status llmplan -n llmplan
kubectl get pods -n llmplan
```

#### 2. 환경별 설정

**개발 환경:**

```bash
helm install llmplan-dev oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan-dev --create-namespace \
  --set image.tag=main \
  --set resources.requests.cpu=250m \
  --set resources.requests.memory=256Mi \
  --set env.DEBUG=true
```

**스테이징 환경:**

```bash
helm install llmplan-staging oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan-staging --create-namespace \
  --set image.tag=latest \
  --set replicaCount=2 \
  --set env.DEBUG=false
```

**프로덕션 환경:**

```bash
helm install llmplan-prod oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan-prod --create-namespace \
  --set image.tag=v0.1.0 \
  --set replicaCount=3 \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=3 \
  --set autoscaling.maxReplicas=20 \
  --set resources.limits.memory=2Gi \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=llmplan.company.com
```

### 업데이트 및 롤백

#### 업데이트

```bash
# 새 버전으로 업데이트
helm upgrade llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan \
  --set image.tag=v0.1.1

# 설정만 변경
helm upgrade llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan \
  --reuse-values \
  --set resources.limits.memory=4Gi
```

#### 롤백

```bash
# 이전 버전으로 롤백
helm rollback llmplan 1 -n llmplan

# 롤백 히스토리 확인
helm history llmplan -n llmplan
```

## 📊 모니터링

### 헬스체크

#### 서비스 상태 확인

```bash
# Kubernetes 내부에서
kubectl exec -it deployment/llmplan -n llmplan -- \
  curl http://localhost:8000/api/v1/summary/health

# 외부에서 (포트 포워딩)
kubectl port-forward svc/llmplan 8000:8000 -n llmplan
curl http://localhost:8000/api/v1/summary/health
```

#### 예상 응답

```json
// 정상
{
  "status": "healthy",
  "service_name": "Text Summarization Service",
  "timestamp": "2025-01-01T00:00:00Z",
  "details": "All systems operational"
}

// 비정상 (LMStudio 연결 실패)
{
  "status": "unhealthy",
  "service_name": "Text Summarization Service",
  "timestamp": "2025-01-01T00:00:00Z",
  "details": "LMStudio service is not responding"
}
```

### 로그 모니터링

#### 로그 확인

```bash
# 실시간 로그
kubectl logs -f deployment/llmplan -n llmplan

# 최근 100줄
kubectl logs --tail=100 deployment/llmplan -n llmplan

# 에러 로그만 필터링
kubectl logs deployment/llmplan -n llmplan | grep ERROR

# 특정 시간 범위
kubectl logs deployment/llmplan -n llmplan --since=1h
```

#### 로그 레벨별 의미

- **INFO**: 정상적인 요약 요청/응답
- **WARNING**: 입력 검증 실패, 재시도 발생
- **ERROR**: LMStudio 연결 실패, 요약 생성 실패
- **CRITICAL**: 서비스 시작 실패, 설정 오류

### 리소스 모니터링

#### CPU/메모리 사용량

```bash
# Pod 리소스 사용량
kubectl top pods -n llmplan

# 노드 리소스 사용량
kubectl top nodes

# 상세 리소스 정보
kubectl describe pod -l app.kubernetes.io/name=llmplan -n llmplan
```

#### HPA 상태 확인

```bash
# HPA 상태
kubectl get hpa -n llmplan

# HPA 상세 정보
kubectl describe hpa llmplan -n llmplan

# 스케일링 이벤트
kubectl get events --field-selector reason=SuccessfulRescale -n llmplan
```

## 🔧 문제 해결

### 일반적인 문제들

#### 1. Pod가 시작되지 않음

```bash
# Pod 상태 확인
kubectl get pods -n llmplan

# Pod 이벤트 확인
kubectl describe pod <pod-name> -n llmplan

# 일반적인 원인:
# - 이미지 Pull 실패: 네트워크 또는 권한 문제
# - 리소스 부족: 노드에 CPU/메모리 부족
# - 설정 오류: ConfigMap, Secret 누락
```

#### 2. 헬스체크 실패 (503 에러)

```bash
# LMStudio 서비스 상태 확인
kubectl get svc lmstudio -n llmplan
kubectl get endpoints lmstudio -n llmplan

# LMStudio 연결 테스트
kubectl exec -it deployment/llmplan -n llmplan -- \
  curl -v http://lmstudio:1234/v1/models

# 해결 방법:
# - LMStudio 서비스 재시작
# - 네트워크 정책 확인
# - DNS 해상도 확인
```

#### 3. 응답 시간이 느림

```bash
# 요약 API 성능 테스트
time curl -X POST http://localhost:8000/api/v1/summary/ \
  -H "Content-Type: application/json" \
  -d '{"text": "테스트 텍스트..."}'

# 병목 지점 확인:
# - LMStudio 모델 로딩 상태
# - 네트워크 지연
# - Pod 리소스 제한
```

#### 4. 메모리 부족 (OOMKilled)

```bash
# Pod 재시작 이벤트 확인
kubectl get events --field-selector reason=Killing -n llmplan

# 메모리 사용량 확인
kubectl top pods -n llmplan

# 해결 방법:
helm upgrade llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --reuse-values \
  --set resources.limits.memory=2Gi \
  --set resources.requests.memory=1Gi
```

### 응급 상황 대응

#### 서비스 완전 중단

```bash
# 1. 즉시 스케일 업
kubectl scale deployment llmplan --replicas=5 -n llmplan

# 2. 이전 버전으로 긴급 롤백
helm rollback llmplan -n llmplan

# 3. 트래픽 우회 (Ingress 설정 변경)
kubectl patch ingress llmplan -n llmplan -p '{"spec":{"rules":[]}}'
```

#### 부분적 장애

```bash
# 1. 문제가 있는 Pod만 재시작
kubectl delete pod <problematic-pod> -n llmplan

# 2. 설정만 변경하여 빠른 수정
kubectl patch deployment llmplan -n llmplan -p \
  '{"spec":{"template":{"spec":{"containers":[{"name":"llmplan","env":[{"name":"LMSTUDIO_TIMEOUT","value":"60"}]}]}}}}'
```

## 🔧 유지보수

### 정기 점검 (주간)

#### 1. 시스템 상태 점검

```bash
# 전체 상태 스냅샷
kubectl get all -n llmplan
helm status llmplan -n llmplan
kubectl top pods -n llmplan
```

#### 2. 로그 분석

```bash
# 에러 로그 통계
kubectl logs deployment/llmplan -n llmplan --since=168h | \
  grep ERROR | wc -l

# 요약 요청 통계
kubectl logs deployment/llmplan -n llmplan --since=168h | \
  grep "POST /api/v1/summary" | wc -l
```

#### 3. 성능 메트릭 확인

```bash
# 평균 응답 시간 (로그 기반)
kubectl logs deployment/llmplan -n llmplan --since=24h | \
  grep "completed in" | \
  awk '{print $NF}' | \
  awk '{sum+=$1; count++} END {print "Average:", sum/count, "ms"}'
```

### 정기 업데이트 (월간)

#### 1. 보안 업데이트

```bash
# 최신 이미지로 업데이트
helm upgrade llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --reuse-values \
  --set image.tag=latest
```

#### 2. 설정 최적화

```bash
# 리소스 사용량 기반 조정
# CPU 사용률이 지속적으로 낮으면 요청량 감소
# 메모리 사용률이 높으면 제한량 증가
```

### 백업 및 복구

#### 설정 백업

```bash
# Helm values 백업
helm get values llmplan -n llmplan > llmplan-values-backup.yaml

# Kubernetes 리소스 백업
kubectl get all -n llmplan -o yaml > llmplan-k8s-backup.yaml
```

#### 복구

```bash
# Helm으로 복구
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan \
  -f llmplan-values-backup.yaml

# Kubernetes 리소스 복구
kubectl apply -f llmplan-k8s-backup.yaml
```

## 📈 성능 최적화

### 스케일링 전략

#### 수평 스케일링 (HPA)

```yaml
# values.yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

#### 수직 스케일링 (VPA)

```yaml
# VPA 설정 (별도 설치 필요)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: llmplan-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llmplan
  updatePolicy:
    updateMode: "Auto"
```

### 리소스 튜닝

#### CPU 최적화

- **요청량**: 실제 사용량의 80% 수준
- **제한량**: 요청량의 2배 이하
- **스케일링**: CPU 70% 기준으로 HPA 설정

#### 메모리 최적화

- **요청량**: 최소 필요량 + 10% 여유
- **제한량**: 요청량의 1.5-2배
- **모니터링**: OOMKilled 이벤트 주의 깊게 관찰

### 네트워크 최적화

#### LMStudio 연결 최적화

```yaml
# values.yaml
env:
  LMSTUDIO_TIMEOUT: "30" # 응답 대기 시간
  LMSTUDIO_MAX_RETRIES: "3" # 재시도 횟수
```

#### 서비스 메시 (향후)

- Istio/Linkerd를 통한 트래픽 관리
- 회로 차단기 패턴
- 부하 분산 최적화
