#!/usr/bin/env python3
"""
Script de démarrage sécurisé pour le bot FootStat Analyzer
Évite les conflits d'instances multiples
"""
import os
import sys
import time
import subprocess
import signal
from pathlib import Path

def kill_existing_python_processes():
    """Arrête tous les processus Python existants"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
        else:  # Unix/Linux
            subprocess.run(['pkill', '-f', 'python.*main.py'], 
                         capture_output=True, check=False)
        time.sleep(2)
        print("✅ Processus Python existants arrêtés")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'arrêt des processus: {e}")

def check_bot_status():
    """Vérifie si le bot est déjà en cours d'exécution"""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                                  capture_output=True, text=True)
            return 'main.py' in result.stdout
        else:  # Unix/Linux
            result = subprocess.run(['pgrep', '-f', 'main.py'], 
                                  capture_output=True, text=True)
            return bool(result.stdout.strip())
    except Exception:
        return False

def start_bot():
    """Démarre le bot de manière sécurisée"""
    print("🚀 Démarrage du Bot FootStat Analyzer v2.0...")
    print("=" * 50)
    
    # Vérifier si le bot est déjà en cours
    if check_bot_status():
        print("⚠️ Le bot semble déjà en cours d'exécution")
        response = input("Voulez-vous l'arrêter et redémarrer ? (o/n): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            kill_existing_python_processes()
        else:
            print("❌ Démarrage annulé")
            return
    
    # Vérifier les fichiers de configuration
    if not Path('.env').exists():
        print("❌ Fichier .env manquant!")
        print("📝 Créez le fichier .env avec vos clés API")
        return
    
    # Vérifier les dépendances
    try:
        import telegram
        import requests
        import openai
        print("✅ Toutes les dépendances sont installées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installez les dépendances avec: pip install -r requirements.txt")
        return
    
    # Démarrer le bot
    try:
        print("🤖 Démarrage du bot avec mode IA activé...")
        print("📱 Votre bot sera disponible sur Telegram")
        print("⏹️ Appuyez sur Ctrl+C pour arrêter le bot")
        print("=" * 50)
        
        # Importer et lancer le bot
        from main import main
        main()
        
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du bot demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("🔧 Vérifiez votre configuration dans le fichier .env")

if __name__ == "__main__":
    start_bot()
