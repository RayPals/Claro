@echo off
rem Run from the Claro folder after the VC6 VCVARS32.BAT environment setup.
rem Keep this file compatible with the Windows 98 SE COMMAND.COM shell.
echo Building Claro for Windows 98 SE with Microsoft Visual C++ 6.0...
cl @build98.rsp
