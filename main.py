"""
Point d'entrée principal du bot FootStat Analyzer
"""
import logging
import os
import asyncio
from telegram.ext import Application
from config import Config
from handlers import BotHandlers
from utils import CacheManager

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale pour démarrer le bot"""
    
    # Vérifier la configuration
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("❌ Token Telegram manquant ! Veuillez configurer TELEGRAM_BOT_TOKEN dans le fichier .env")
        return
    
    if not Config.FOOTBALL_API_KEY:
        logger.error("❌ Clé API Football manquante ! Veuillez configurer FOOTBALL_API_KEY dans le fichier .env")
        return
    
    logger.info("🚀 Démarrage du bot FootStat Analyzer...")
    
    # Créer l'application Telegram
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Initialiser les gestionnaires
    bot_handlers = BotHandlers()
    handlers = bot_handlers.get_handlers()
    
    # Ajouter les gestionnaires à l'application
    for handler in handlers:
        application.add_handler(handler)
    
    # Gestionnaire d'erreurs global
    async def error_handler(update, context):
        """Gestionnaire d'erreurs global"""
        logger.error(f"Erreur: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Une erreur inattendue s'est produite. Veuillez réessayer."
            )
    
    application.add_error_handler(error_handler)
    
    # Fonction de démarrage
    async def post_init(application):
        """Fonctions à exécuter après l'initialisation"""
        logger.info("✅ Bot FootStat Analyzer v2.0 démarré avec succès !")
        logger.info(f"📊 Mode IA: {'Activé' if Config.AI_MODE_ENABLED else 'Désactivé'}")
        logger.info(f"⚽ API Football: {Config.FOOTBALL_API_BASE_URL}")
        
        # Initialiser le système de cache
        cache_manager = CacheManager()
        logger.info(f"🗄️ Cache initialisé: {(cache_manager.get_stats())}")
        
        # Créer les dossiers nécessaires
        os.makedirs("cache/football_api", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Afficher les informations de configuration
        if Config.AI_MODE_ENABLED and not Config.OPENAI_API_KEY:
            logger.warning("⚠️ Mode IA activé mais clé OpenAI manquante")
        
        logger.info("🚀 Bot prêt à recevoir des commandes!")
    
    # Ajouter la fonction post_init
    application.post_init = post_init
    
    # Fonction d'arrêt
    async def shutdown():
        """Fonction d'arrêt propre"""
        logger.info("🛑 Arrêt du bot FootStat Analyzer...")
    
    # Démarrer le bot
    try:
        logger.info("🔄 Démarrage du polling...")
        application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
    finally:
        logger.info("👋 Bot arrêté")

if __name__ == '__main__':
    main()
