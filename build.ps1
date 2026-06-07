param(
  [string]$CC = "gcc",
  [string]$Out = "claro.exe"
)

Write-Host "Building Claro v1.18.26..." -ForegroundColor Cyan
& $CC "-std=c99" "src\claro.c" "-O0" "-o" $Out "-lm"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Built: $Out" -ForegroundColor Green
Write-Host "Run tests with: .\$Out test" -ForegroundColor Green
Write-Host "Try a lesson with: .\$Out lessons\01_hello.claro" -ForegroundColor Green
