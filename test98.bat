@echo off
rem Run only in a fresh extracted Claro test folder.
if exist native.ok del native.ok
if not exist osprobe.exe goto wrongos
osprobe.exe --require-win98se >oscheck.txt
if errorlevel 1 goto wrongos
claro98.exe --version >nver.txt
if errorlevel 1 goto failed
claro98.exe test >ntests.txt
if errorlevel 1 goto failed
claro98.exe validate >ncheck.txt
if errorlevel 1 goto failed
echo Automated native checks passed. Manual console and file checks are still required.
echo PASS>native.ok
goto end
:wrongos
echo Native target not verified. Check oscheck.txt and the probe message.
goto end
:failed
echo Claro checks failed. Keep the logs; do not report acceptance.
:end
