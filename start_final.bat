@echo off
title FootStat Analyzer v2.0 - Bot Telegram
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                FootStat Analyzer v2.0                       ║
echo  ║                Bot Telegram avec Mode IA                    ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

REM Arrêter tous les processus Python existants
echo [1/5] Arrêt des processus Python existants...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Activer l'environnement virtuel
echo [2/5] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

REM Vérifier les dépendances
echo [3/5] Vérification des dépendances...
python -c "import telegram, requests, openai; print('Dependances OK')" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Dependances manquantes - Installation...
    pip install -r requirements.txt
)

REM Test rapide des composants
echo [4/5] Test des composants...
python test_bot.py
if errorlevel 1 (
    echo [ATTENTION] Test des composants échoué, mais on continue...
)

REM Démarrer le bot
echo [5/5] Démarrage du bot...
echo.
echo  ✅ Bot démarré avec Mode IA activé
echo  📱 Votre bot est disponible sur Telegram
echo  🤖 Nom: Fut bollu Stat
echo  ⏹️  Appuyez sur Ctrl+C pour arrêter
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.

python main.py

echo.
echo  👋 Bot arrêté
pause
