@echo off
setlocal
if not exist claro.exe (
  call build.bat
  if errorlevel 1 exit /b 1
)
claro.exe test
