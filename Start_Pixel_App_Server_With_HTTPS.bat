@echo off
title AETHOS 365 PRO - Google Pixel HTTPS & PWA Launcher
cd /d "%~dp0"
echo ================================================================
echo       AETHOS 365 PRO - GOOGLE PIXEL SECURE APP LAUNCHER
echo ================================================================
echo.
echo 1. Starting local Node.js server on port 8080...
start "Aethos Local Server" /min node server_mobile_pixel.js
timeout /t 2 /nobreak >nul
echo.
echo 2. Establishing secure Cloudflare HTTPS Tunnel for Google Pixel...
echo    (This provides the SSL certificate required by Android Chrome to install WebAPKs)
echo.
npx cloudflared tunnel --url http://localhost:8080
pause
