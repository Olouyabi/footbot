"""
Script pour redémarrer proprement le bot FootStat Analyzer v2.0
"""
import subprocess
import sys
import time
import os

def kill_python_processes():
    """Arrête tous les processus Python"""
    try:
        print("🛑 Arrêt des processus Python existants...")
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, text=True)
        print("✅ Processus Python arrêtés")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Erreur lors de l'arrêt des processus: {e}")

def start_bot():
    """Démarre le bot"""
    try:
        print("🚀 Démarrage du bot FootStat Analyzer v2.0...")
        subprocess.Popen([sys.executable, "start_enhanced_bot.py"])
        print("✅ Bot démarré avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

def main():
    """Fonction principale"""
    print("🔄 Redémarrage du bot FootStat Analyzer v2.0...")
    
    # Arrêter les processus existants
    kill_python_processes()
    
    # Démarrer le bot
    start_bot()
    
    print("\n🎉 Redémarrage terminé!")
    print("📱 Le bot est maintenant disponible sur Telegram")

if __name__ == "__main__":
    main()
