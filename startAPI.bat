echo off
pushd %~dp0
echo Iniciando..
echo.
echo Logfile: %~dp0logs\api.log
runManager.exe > .\logs\api.log
PAUSE