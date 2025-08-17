# PowerShell script to test all Kubernetes scripts
Write-Host "=== Testing All Kubernetes Scripts ===" -ForegroundColor Green
Write-Host ""

# Test all scripts
$scripts = @{
    "kurbeScript" = @{
        "Path" = "messaging_app/kurbeScript"
        "Type" = "Bash Script"
        "Purpose" = "Kubernetes cluster setup"
    }
    "kurbeScript.ps1" = @{
        "Path" = "messaging_app/kurbeScript.ps1"
        "Type" = "PowerShell Script"
        "Purpose" = "Windows Kubernetes cluster setup"
    }
    "kubctl-0x01" = @{
        "Path" = "messaging_app/kubctl-0x01"
        "Type" = "Bash Script"
        "Purpose" = "Scaling and load testing"
    }
    "kubctl-0x01.ps1" = @{
        "Path" = "messaging_app/kubctl-0x01.ps1"
        "Type" = "PowerShell Script"
        "Purpose" = "Windows scaling and load testing"
    }
}

$allGood = $true

foreach ($scriptName in $scripts.Keys) {
    $scriptInfo = $scripts[$scriptName]
    $path = $scriptInfo.Path
    
    Write-Host "Testing $scriptName..." -ForegroundColor Cyan
    
    if (Test-Path $path) {
        $fileInfo = Get-Item $path
        $size = $fileInfo.Length
        
        if ($size -gt 0) {
            Write-Host "  ✅ $scriptName exists and is not empty ($size bytes)" -ForegroundColor Green
            Write-Host "     Type: $($scriptInfo.Type)" -ForegroundColor Gray
            Write-Host "     Purpose: $($scriptInfo.Purpose)" -ForegroundColor Gray
        } else {
            Write-Host "  ❌ $scriptName is empty" -ForegroundColor Red
            $allGood = $false
        }
    } else {
        Write-Host "  ❌ $scriptName does not exist" -ForegroundColor Red
        $allGood = $false
    }
    
    Write-Host ""
}

# Summary
Write-Host "=== Summary ===" -ForegroundColor Green
if ($allGood) {
    Write-Host "✅ All Kubernetes scripts are present and valid" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some issues found with scripts" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Usage Instructions ===" -ForegroundColor Green
Write-Host "For Windows (PowerShell):"
Write-Host "  .\messaging_app\kurbeScript.ps1"
Write-Host "  .\messaging_app\kubctl-0x01.ps1"
Write-Host ""
Write-Host "For Linux/Mac/WSL (Bash):"
Write-Host "  bash messaging_app/kurbeScript"
Write-Host "  bash messaging_app/kubctl-0x01"
Write-Host ""
Write-Host "For verification:"
Write-Host "  .\messaging_app\verify_k8s_setup.ps1"
