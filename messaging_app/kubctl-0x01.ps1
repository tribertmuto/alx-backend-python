# PowerShell script for Kubernetes Scaling and Load Testing
# Windows-compatible version of kubctl-0x01

Write-Host "=== Kubernetes Scaling and Load Testing Script ===" -ForegroundColor Green
Write-Host ""

# Check if kubectl is available
try {
    kubectl version --client | Out-Null
    Write-Host "✅ kubectl is available" -ForegroundColor Green
} catch {
    Write-Host "Error: kubectl is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if wrk is available for load testing
try {
    $wrkVersion = wrk --version
    Write-Host "✅ wrk is available for load testing" -ForegroundColor Green
    $WRK_AVAILABLE = $true
} catch {
    Write-Host "Warning: wrk is not installed. Load testing will be skipped." -ForegroundColor Yellow
    Write-Host "To install wrk:"
    Write-Host "  • Download from: https://github.com/wg/wrk"
    Write-Host "  • Or use: choco install wrk (if Chocolatey is installed)"
    $WRK_AVAILABLE = $false
}

Write-Host ""
Write-Host "Checking current deployment status..."
kubectl get deployments

Write-Host ""
Write-Host "Current pods before scaling:"
kubectl get pods -l app=django-messaging-app

Write-Host ""
Write-Host "Scaling Django messaging app deployment to 3 replicas..."
kubectl scale deployment django-messaging-app --replicas=3

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Scaling command executed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to scale deployment" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=django-messaging-app --timeout=300s

Write-Host ""
Write-Host "Verifying scaled pods are running..."
kubectl get pods -l app=django-messaging-app

Write-Host ""
Write-Host "Deployment status after scaling:"
kubectl get deployments django-messaging-app

Write-Host ""
Write-Host "Service endpoints:"
kubectl get endpoints django-messaging-service

# Load testing with wrk (if available)
if ($WRK_AVAILABLE) {
    Write-Host ""
    Write-Host "Starting load testing..."
    
    # Get the service URL
    Write-Host "Setting up port-forward for load testing..."
    Start-Process -NoNewWindow -FilePath "kubectl" -ArgumentList "port-forward", "service/django-messaging-service", "8080:80"
    Start-Sleep -Seconds 5
    
    Write-Host "Running load test with wrk for 30 seconds, 4 threads, 12 connections..."
    wrk -t4 -c12 -d30s http://localhost:8080/
    
    Write-Host "Load testing completed."
} else {
    Write-Host ""
    Write-Host "⚠️  wrk not available, skipping load testing"
    Write-Host "To test manually, run:"
    Write-Host "  kubectl port-forward service/django-messaging-service 8080:80"
    Write-Host "  curl http://localhost:8080/"
}

Write-Host ""
Write-Host "=== Resource Usage Monitoring ==="
Write-Host ""

# Check if metrics-server is available
Write-Host "Checking metrics server availability..."
try {
    kubectl top node | Out-Null
    Write-Host "✅ Metrics server is available" -ForegroundColor Green
    Write-Host ""
    Write-Host "Node resource usage:"
    kubectl top nodes
    
    Write-Host ""
    Write-Host "Pod resource usage:"
    kubectl top pods -l app=django-messaging-app
} catch {
    Write-Host "⚠️  Metrics server not available or not ready yet" -ForegroundColor Yellow
    Write-Host "To enable metrics server in minikube:"
    Write-Host "  minikube addons enable metrics-server"
    Write-Host "  Wait a few minutes for metrics to be available"
}

Write-Host ""
Write-Host "Pod resource requests and limits:"
kubectl describe pods -l app=django-messaging-app | Select-String -Pattern "Limits|Requests" -Context 2

Write-Host ""
Write-Host "=== Scaling Test Complete ==="
Write-Host "Summary:"
Write-Host "- Scaled deployment to 3 replicas"
Write-Host "- Verified pods are running"
Write-Host "- Monitored resource usage"
if ($WRK_AVAILABLE) {
    Write-Host "- Performed load testing"
}
Write-Host ""
Write-Host "To scale back down: kubectl scale deployment django-messaging-app --replicas=1"
