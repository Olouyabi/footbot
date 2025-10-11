"""
Script de démarrage final pour FootStat Analyzer v2.0
Inclut toutes les nouvelles fonctionnalités et améliorations
"""
import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    logger.info("🔍 Vérification des dépendances...")
    
    required_packages = [
        'telegram',
        'requests', 
        'python-dotenv',
        'pandas',
        'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package} installé")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} manquant")
    
    if missing_packages:
        logger.error(f"📦 Packages manquants: {', '.join(missing_packages)}")
        logger.info("💡 Installez-les avec: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_config():
    """Vérifie la configuration du bot"""
    logger.info("⚙️ Vérification de la configuration...")
    
    # Vérifier le fichier .env
    env_file = Path('.env')
    if not env_file.exists():
        logger.error("❌ Fichier .env manquant")
        logger.info("💡 Créez un fichier .env avec vos clés API")
        return False
    
    # Vérifier les variables d'environnement
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'FOOTBALL_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ Configuration valide")
    return True

def create_directories():
    """Crée les répertoires nécessaires"""
    logger.info("📁 Création des répertoires...")
    
    directories = [
        'cache',
        'cache/football_api',
        'cache/advanced',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Répertoire {directory} créé")

def test_components():
    """Teste les composants principaux"""
    logger.info("🧪 Test des composants...")
    
    try:
        # Test des imports
        from main import main
        from handlers import BotHandlers
        from analyzer import MatchAnalyzer
        from advanced_commands import AdvancedCommands
        from ai_module import AIModule
        
        logger.info("✅ Imports réussis")
        
        # Test d'initialisation des composants
        handlers = BotHandlers()
        analyzer = MatchAnalyzer()
        advanced = AdvancedCommands()
        
        logger.info("✅ Initialisation des composants réussie")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test des composants: {e}")
        return False

def kill_existing_processes():
    """Arrête les processus Python existants"""
    logger.info("🛑 Arrêt des processus existants...")
    
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
        logger.info("✅ Processus arrêtés")
    except Exception as e:
        logger.warning(f"⚠️ Impossible d'arrêter les processus: {e}")

def start_bot():
    """Démarre le bot"""
    logger.info("🚀 Démarrage du bot FootStat Analyzer v2.0...")
    
    try:
        # Importer et exécuter le main
        from main import main
        main()
    except KeyboardInterrupt:
        logger.info("👋 Arrêt du bot par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🔥 FootStat Analyzer v2.0 - Démarrage Final 🔥")
    print("=" * 60)
    
    # Vérifications préliminaires
    if not check_dependencies():
        logger.error("❌ Dépendances manquantes. Arrêt.")
        return False
    
    if not check_config():
        logger.error("❌ Configuration invalide. Arrêt.")
        return False
    
    # Préparation
    create_directories()
    kill_existing_processes()
    
    # Test des composants
    if not test_components():
        logger.error("❌ Test des composants échoué. Arrêt.")
        return False
    
    # Démarrage du bot
    logger.info("🎉 Toutes les vérifications sont passées !")
    logger.info("🚀 Démarrage du bot...")
    
    return start_bot()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
