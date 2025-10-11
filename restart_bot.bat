@echo off
echo.
echo ========================================
echo   REDEMARRAGE FOOTSTAT ANALYZER v2.0
echo ========================================
echo.
echo 🛑 Arrêt des processus existants...
taskkill /F /IM python.exe >nul 2>&1
echo ✅ Processus arrêtés
echo.
echo ⏳ Attente de 3 secondes...
timeout /t 3 /nobreak >nul
echo.
echo 🚀 Démarrage du bot...
python start_enhanced_bot.py
echo.
echo ========================================
echo   BOT ARRETE
echo ========================================
pause
