@echo off
echo 🔥 FootStat Analyzer v2.0 - Démarrage Final 🔥
echo ================================================

echo.
echo 🛑 Arrêt des processus Python existants...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo.
echo 🔄 Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo 🧪 Test des composants...
python test_advanced_features.py
if errorlevel 1 (
    echo [ATTENTION] Test des composants échoué, mais on continue...
)

echo.
echo 🚀 Démarrage du bot FootStat Analyzer v2.0...
python start_final_v2.py

echo.
echo 👋 Bot arrêté. Appuyez sur une touche pour fermer...
pause >nul
