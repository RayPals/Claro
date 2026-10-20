@echo off
setlocal
set CC=gcc
if not "%~1"=="" set CC=%~1
echo Building Claro (C89)...
%CC% -std=c89 -pedantic-errors -Werror=implicit-function-declaration src\claro.c -O0 -o claro.exe -Wl,--stack,16777216 -lm
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)
echo Built claro.exe
echo Run tests with: claro.exe test
