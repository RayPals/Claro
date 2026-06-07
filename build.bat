@echo off
setlocal
set CC=gcc
if not "%~1"=="" set CC=%~1
echo Building Claro v1.18.26...
%CC% -std=c99 src\claro.c -O0 -o claro.exe -lm
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)
echo Built claro.exe
echo Run tests with: claro.exe test
