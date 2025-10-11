"""
Configuration du Bot FootStat Analyzer
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration principale du bot"""
    
    # Tokens et clés API
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # URLs et endpoints
    FOOTBALL_API_BASE_URL = os.getenv('FOOTBALL_API_BASE_URL', 'https://api.football-data.org/v4')
    
    # Configuration des analyses
    DEFAULT_LEAGUE = os.getenv('DEFAULT_LEAGUE', 'PL')
    ANALYSIS_MODE = os.getenv('ANALYSIS_MODE', 'standard')
    AI_MODE_ENABLED = os.getenv('AI_MODE_ENABLED', 'false').lower() == 'true'
    
    # Messages du bot
    WELCOME_MESSAGE = r"""
⚽ *FootStat Analyzer v2.0* - Votre assistant d'analyse de football

Je peux analyser les matchs de football et vous fournir :
• 📊 Statistiques détaillées des équipes
• 🎯 Probabilités de résultats (victoire, nul, défaite)
• ⚡ Analyse de forme récente
• 🏠 Performances à domicile/extérieur
• 💡 Recommandations personnalisées

*Comment utiliser :*
Envoyez-moi une liste de matchs au format :
`Real Madrid vs Barcelona`
`Liverpool vs Chelsea`
`PSG vs Marseille`

Ou utilisez la commande /analyze suivi de vos matchs.

*Commandes disponibles :*
/start - Démarrer le bot
/help - Aide détaillée
/analyze - Analyser des matchs
/menu - Menu interactif complet
/footchat - Chat football avec l'IA
/ai_mode - Activer/désactiver le mode IA
"""
    
    HELP_MESSAGE = r"""
🔥 *FootStat Analyzer v2.0* - Guide d'utilisation 🔥

**📊 COMMANDES PRINCIPALES:**
• `/analyze` - Analyser des matchs de football
• `/standings [championnat]` - Classement d'un championnat
• `/teamstats [équipe]` - Statistiques détaillées d'une équipe
• `/compare [équipe1] [équipe2]` - Comparer deux équipes
• `/upcoming [championnat]` - Prochains matchs

**⚽ COMMENT UTILISER:**
1. Envoyez des matchs au format :
   `Real Madrid vs Barcelona`
   `Liverpool vs Chelsea`

2. Le bot analysera automatiquement chaque match

3. Recevez des prédictions détaillées avec :
   • Probabilités de victoire/nul/défaite
   • Pronostic buts (+2.5)
   • Niveau de risque
   • Analyse experte

**🏆 CHAMPIONNATS SUPPORTÉS:**
• Ligue 1, Premier League, La Liga
• Bundesliga, Serie A, Champions League

**🤖 MODE IA:**
Activez le mode IA pour des analyses plus détaillées et personnalisées.

**📈 FONCTIONNALITÉS:**
• Cache intelligent pour des réponses rapides
• Pagination pour les analyses multiples
• Gestion d'erreurs robuste
• Support multi-championnats
• Formatage amélioré avec emojis et barres visuelles

Utilisez `/help_advanced` pour voir toutes les commandes disponibles.
"""
