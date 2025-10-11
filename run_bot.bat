@echo off
echo ========================================
echo  FootStat Analyzer v2.0 - Bot Telegram
echo ========================================
echo.

REM Arrêter tous les processus Python existants
echo [1/4] Arrêt des processus Python existants...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

REM Activer l'environnement virtuel
echo [2/4] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

REM Vérifier les dépendances
echo [3/4] Vérification des dépendances...
python -c "import telegram, requests, openai; print('Dependances OK')" 2>nul
if errorlevel 1 (
    echo ERREUR: Dependances manquantes
    echo Installation des dependances...
    pip install -r requirements.txt
)

REM Démarrer le bot
echo [4/4] Démarrage du bot...
echo.
echo ✅ Bot démarré avec Mode IA activé
echo 📱 Votre bot est disponible sur Telegram
echo ⏹️  Appuyez sur Ctrl+C pour arrêter
echo.
python main.py

pause
