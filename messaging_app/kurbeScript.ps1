# PowerShell script for Kubernetes Local Cluster Setup
# Windows-compatible version of kurbeScript

Write-Host "=== Kubernetes Local Cluster Setup Script ===" -ForegroundColor Green
Write-Host "Objective: Learn how to set up and use Kubernetes locally" -ForegroundColor Yellow
Write-Host ""

# Ensure minikube is installed
Write-Host "Step 1: Ensuring minikube is installed..." -ForegroundColor Cyan
try {
    $minikubeVersion = minikube version
    Write-Host "✅ minikube is installed" -ForegroundColor Green
    Write-Host $minikubeVersion
} catch {
    Write-Host "❌ Error: minikube is not installed. Please install minikube first." -ForegroundColor Red
    Write-Host "Installation instructions:"
    Write-Host "  - Visit: https://minikube.sigs.k8s.io/docs/start/"
    Write-Host "  - Or use package managers:"
    Write-Host "    • Windows: choco install minikube"
    Write-Host "    • Or download from: https://github.com/kubernetes/minikube/releases/latest"
    exit 1
}

# Ensure kubectl is installed
Write-Host ""
Write-Host "Step 2: Checking if kubectl is installed..." -ForegroundColor Cyan
try {
    $kubectlVersion = kubectl version --client
    Write-Host "✅ kubectl is installed" -ForegroundColor Green
    Write-Host $kubectlVersion
} catch {
    Write-Host "❌ Error: kubectl is not installed. Please install kubectl first." -ForegroundColor Red
    Write-Host "Visit: https://kubernetes.io/docs/tasks/tools/"
    exit 1
}

# Start Kubernetes cluster
Write-Host ""
Write-Host "Step 3: Starting Kubernetes cluster on your machine..." -ForegroundColor Cyan
Write-Host "Using minikube to create a local Kubernetes cluster..."

try {
    minikube start --driver=docker
    Write-Host "✅ Kubernetes cluster started successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start Kubernetes cluster" -ForegroundColor Red
    exit 1
}

# Wait for cluster to be ready
Write-Host ""
Write-Host "Waiting for cluster to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verify cluster is running
Write-Host ""
Write-Host "Step 4: Verifying that the cluster is running using kubectl cluster-info..." -ForegroundColor Cyan
try {
    kubectl cluster-info
    Write-Host "✅ Cluster info retrieved successfully - Cluster is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to retrieve cluster info - Cluster may not be running properly" -ForegroundColor Red
    exit 1
}

# Get cluster nodes
Write-Host ""
Write-Host "Step 5: Getting cluster nodes information..." -ForegroundColor Cyan
kubectl get nodes

# Retrieve available pods
Write-Host ""
Write-Host "Step 6: Retrieving the available pods..." -ForegroundColor Cyan
Write-Host "Listing all pods across all namespaces:"
kubectl get pods --all-namespaces

Write-Host ""
Write-Host "Pod count summary:"
$podCount = (kubectl get pods --all-namespaces --no-headers | Measure-Object).Count
Write-Host "Total pods: $podCount"

# Enable useful addons
Write-Host ""
Write-Host "Step 7: Enabling useful addons for local development..." -ForegroundColor Cyan
Write-Host "Enabling ingress addon..."
minikube addons enable ingress

Write-Host "Enabling metrics-server addon..."
minikube addons enable metrics-server

Write-Host ""
Write-Host "=== Kubernetes Local Setup Complete ===" -ForegroundColor Green
Write-Host "🎉 Your local Kubernetes cluster is now running and ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Summary of what was accomplished:"
Write-Host "✅ 1. Ensured minikube is installed"
Write-Host "✅ 2. Started Kubernetes cluster on your machine"
Write-Host "✅ 3. Verified cluster is running using kubectl cluster-info"
Write-Host "✅ 4. Retrieved available pods"
Write-Host "✅ 5. Enabled useful addons (ingress, metrics-server)"
Write-Host ""
Write-Host "Next steps for learning Kubernetes locally:"
Write-Host "  kubectl get pods --all-namespaces    # List all pods"
Write-Host "  kubectl get services                 # List all services"
Write-Host "  kubectl get nodes                    # List cluster nodes"
Write-Host "  minikube dashboard                   # Open Kubernetes web dashboard"
Write-Host "  kubectl create deployment test --image=nginx  # Create a test deployment"
Write-Host ""
Write-Host "Cluster management commands:"
Write-Host "  minikube status    # Check cluster status"
Write-Host "  minikube stop      # Stop the cluster"
Write-Host "  minikube start     # Start the cluster"
Write-Host "  minikube delete    # Delete the cluster completely"
