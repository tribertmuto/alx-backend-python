# PowerShell script to verify Kubernetes setup on Windows
Write-Host "=== Kubernetes Setup Verification ===" -ForegroundColor Green
Write-Host ""

# Check if kurbeScript.ps1 exists
if (Test-Path "messaging_app/kurbeScript.ps1") {
    Write-Host "✅ kurbeScript.ps1 exists" -ForegroundColor Green
    
    # Check if it's not empty
    if ((Get-Item "messaging_app/kurbeScript.ps1").Length -gt 0) {
        Write-Host "✅ kurbeScript.ps1 is not empty" -ForegroundColor Green
    } else {
        Write-Host "❌ kurbeScript.ps1 is empty" -ForegroundColor Red
    }
} else {
    Write-Host "❌ kurbeScript.ps1 does not exist" -ForegroundColor Red
}

# Check if original kurbeScript exists
if (Test-Path "messaging_app/kurbeScript") {
    Write-Host "✅ kurbeScript (bash version) exists" -ForegroundColor Green
} else {
    Write-Host "❌ kurbeScript (bash version) does not exist" -ForegroundColor Red
}

# Check if minikube is installed
Write-Host ""
Write-Host "Checking minikube installation..." -ForegroundColor Cyan
try {
    $minikubeVersion = minikube version
    Write-Host "✅ minikube is installed" -ForegroundColor Green
    Write-Host $minikubeVersion
} catch {
    Write-Host "❌ minikube is not installed" -ForegroundColor Red
    Write-Host "Please install minikube from: https://minikube.sigs.k8s.io/docs/start/"
}

# Check if kubectl is installed
Write-Host ""
Write-Host "Checking kubectl installation..." -ForegroundColor Cyan
try {
    $kubectlVersion = kubectl version --client
    Write-Host "✅ kubectl is installed" -ForegroundColor Green
    Write-Host $kubectlVersion
} catch {
    Write-Host "❌ kubectl is not installed" -ForegroundColor Red
    Write-Host "Please install kubectl from: https://kubernetes.io/docs/tasks/tools/"
}

Write-Host ""
Write-Host "=== Verification Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "To use the Kubernetes setup scripts:"
Write-Host "1. Run: .\messaging_app\kurbeScript.ps1   # For Windows PowerShell"
Write-Host "2. Or use: bash messaging_app/kurbeScript  # For WSL/Git Bash"
