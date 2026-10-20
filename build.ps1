param(
  [string]$CC = "gcc",
  [string]$Out = "claro.exe"
)

Write-Host "Building Claro (C89)..." -ForegroundColor Cyan
& $CC "-std=c89" "-pedantic-errors" "-Werror=implicit-function-declaration" "src\claro.c" "-O0" "-o" $Out "-Wl,--stack,16777216" "-lm"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Built: $Out" -ForegroundColor Green
Write-Host "Run tests with: .\$Out test" -ForegroundColor Green
Write-Host "Try a lesson with: .\$Out lessons\01_hello.claro" -ForegroundColor Green
