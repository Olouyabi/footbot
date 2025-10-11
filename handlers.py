"""
Gestionnaires de commandes et messages pour le bot Telegram
"""
import logging
from typing import Dict, List, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from analyzer import MatchAnalyzer
from ai_module import AIModule
from advanced_commands import AdvancedCommands
from enhanced_commands import EnhancedCommands
from formatter import ProfessionalFormatter
from football_chat import FootballChat
from config import Config
from utils import UserSettings, Paginator, LeagueManager, ErrorHandler

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotHandlers:
    """Gestionnaires pour le bot Telegram"""
    
    def __init__(self):
        self.analyzer = MatchAnalyzer()
        self.ai_module = AIModule()
        self.advanced_commands = AdvancedCommands()
        self.enhanced_commands = EnhancedCommands()
        self.formatter = ProfessionalFormatter()
        self.football_chat = FootballChat()
        self.user_settings = UserSettings(self.analyzer.api_client.cache)
        self.paginator = Paginator(items_per_page=3)
        self.league_manager = LeagueManager()
        self.error_handler = ErrorHandler()
        self.user_cache = {}  # Cache temporaire pour les analyses en cours
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /start"""
        user = update.effective_user
        logger.info(f"Utilisateur {user.id} ({user.username}) a démarré le bot")
        
        # Message de bienvenue simple et sécurisé
        welcome_text = r"""⚽ *FootStat Analyzer v2.0* - Votre assistant d'analyse de football

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
/ai_mode - Activer/désactiver le mode IA"""
        
        try:
            await update.message.reply_text(
                welcome_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur parsing Markdown: {e}")
            # Fallback sans Markdown
            await update.message.reply_text(
                """⚽ FootStat Analyzer v2.0 - Votre assistant d'analyse de football

Je peux analyser les matchs de football et vous fournir :
• 📊 Statistiques détaillées des équipes
• 🎯 Probabilités de résultats (victoire, nul, défaite)
• ⚡ Analyse de forme récente
• 🏠 Performances à domicile/extérieur
• 💡 Recommandations personnalisées

Comment utiliser :
Envoyez-moi une liste de matchs au format :
Real Madrid vs Barcelona
Liverpool vs Chelsea
PSG vs Marseille

Ou utilisez la commande /analyze suivi de vos matchs.

Commandes disponibles :
/start - Démarrer le bot
/help - Aide détaillée
/analyze - Analyser des matchs
/menu - Menu interactif complet
/footchat - Chat football avec l'IA
/ai_mode - Activer/désactiver le mode IA"""
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /help"""
        await update.message.reply_text(
            Config.HELP_MESSAGE,
            parse_mode='Markdown'
        )
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /analyze"""
        if not context.args:
            await update.message.reply_text(
                "❌ Veuillez spécifier des matchs à analyser.\n\n"
                "Exemple : /analyze Real Madrid vs Barcelona"
            )
            return
        
        # Reconstituer le texte des matchs
        matches_text = ' '.join(context.args)
        await self._process_matches(update, context, matches_text)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire amélioré de la commande /analyze avec options"""
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        
        if not context.args:
            # Afficher les options d'analyse
            keyboard = [
                [InlineKeyboardButton("🏆 Ligues disponibles", callback_data="show_leagues")],
                [InlineKeyboardButton("⚙️ Paramètres", callback_data="show_settings")],
                [InlineKeyboardButton("❓ Aide Analyse", callback_data="help_analyze")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"🔍 *Analyse de matchs*\n\n"
                f"Ligue actuelle: **{user_settings['league']}**\n"
                f"Mode IA: **{'Activé' if user_settings['ai_mode'] else 'Désactivé'}**\n\n"
                "Envoyez vos matchs ou utilisez les options ci-dessous :",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        # Analyser les arguments
        matches_text = ' '.join(context.args)
        
        # Vérifier s'il y a des options spéciales
        if matches_text.startswith('--league'):
            league_arg = matches_text.split(' ', 1)[1] if ' ' in matches_text else ''
            await self._handle_league_change(update, league_arg)
            return
        elif matches_text.startswith('--ai'):
            ai_arg = matches_text.split(' ', 1)[1] if ' ' in matches_text else ''
            await self._handle_ai_toggle(update, ai_arg)
            return
        
        # Analyser les matchs
        await self._process_matches(update, context, matches_text)
    
    async def set_league_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /set_league"""
        user_id = update.effective_user.id
        
        if not context.args:
            leagues_text = self.league_manager.format_leagues_list()
            await update.message.reply_text(
                f"{leagues_text}\n\n"
                "Utilisez /set_league CODE pour changer votre ligue préférée.\n"
                "Exemple: /set_league PL",
                parse_mode='Markdown'
            )
            return
        
        league_code = context.args[0].upper()
        if self.user_settings.set_league(user_id, league_code):
            league_info = self.league_manager.get_league_info(league_code)
            await update.message.reply_text(
                f"✅ Ligue changée pour **{league_info['name']}** ({league_code})",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Code de ligue invalide. Utilisez /set_league pour voir les options disponibles."
            )
    
    async def toggle_ia_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /toggle_ia"""
        user_id = update.effective_user.id
        
        new_mode = self.user_settings.toggle_ai_mode(user_id)
        action = "activé" if new_mode else "désactivé"
        
        await update.message.reply_text(
            f"🤖 Mode IA **{action}** !\n\n"
            f"{'Les analyses seront améliorées avec l\'IA.' if new_mode else 'Retour aux analyses standard.'}",
            parse_mode='Markdown'
        )
    
    async def ai_mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /ai_mode (compatibilité)"""
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        
        if not context.args:
            # Afficher le statut actuel
            current_mode = user_settings.get('ai_mode', False)
            status = "activé" if current_mode else "désactivé"
            await update.message.reply_text(
                f"🤖 Mode IA actuellement : *{status}*\n\n"
                "Utilisez /ai_mode on pour activer\n"
                "Utilisez /ai_mode off pour désactiver\n"
                "Ou utilisez /toggle_ia pour basculer",
                parse_mode='Markdown'
            )
            return
        
        mode_arg = context.args[0].lower()
        
        if mode_arg in ['on', 'enable', 'true', '1']:
            self.user_settings.update_user_setting(user_id, 'ai_mode', True)
            await update.message.reply_text(
                "🤖 Mode IA *activé* ! Les analyses seront améliorées avec l'intelligence artificielle.",
                parse_mode='Markdown'
            )
        elif mode_arg in ['off', 'disable', 'false', '0']:
            self.user_settings.update_user_setting(user_id, 'ai_mode', False)
            await update.message.reply_text(
                "🤖 Mode IA *désactivé*. Retour aux analyses standard.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Argument invalide. Utilisez 'on' ou 'off', ou utilisez /toggle_ia."
            )
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /settings"""
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        
        league_info = self.league_manager.get_league_info(user_settings['league'])
        
        keyboard = [
            [InlineKeyboardButton("🏆 Changer de ligue", callback_data="change_league")],
            [InlineKeyboardButton("🤖 Mode IA", callback_data="toggle_ai_mode")],
            [InlineKeyboardButton("📊 Statistiques", callback_data="show_stats")],
            [InlineKeyboardButton("🗑️ Vider le cache", callback_data="clear_cache")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        settings_text = f"⚙️ *Paramètres utilisateur*\n\n"
        settings_text += f"🏆 **Ligue :** {league_info['name']} ({league_info['country']})\n"
        settings_text += f"🤖 **Mode IA :** {'Activé' if user_settings['ai_mode'] else 'Désactivé'}\n"
        settings_text += f"📄 **Langue :** {user_settings['language']}\n"
        settings_text += f"🔔 **Notifications :** {'Activées' if user_settings['notifications'] else 'Désactivées'}\n"
        settings_text += f"📅 **Créé le :** {user_settings['created_at'][:10]}"
        
        await update.message.reply_text(
            settings_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def standings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher le classement d'un championnat avec formatage professionnel"""
        try:
            league_name = " ".join(context.args) if context.args else "Ligue 1"
            
            # Récupérer les données brutes
            leagues = {
                "ligue 1": "FL1",
                "premier league": "PL", 
                "la liga": "PD",
                "bundesliga": "BL1",
                "serie a": "SA",
                "champions league": "CL"
            }
            
            league_code = leagues.get(league_name.lower(), "FL1")
            
            # Récupérer les données de l'API
            standings_data = self.analyzer.api_client._make_request(f"competitions/{league_code}/standings")
            
            if standings_data:
                # Utiliser le nouveau formateur
                formatted_standings = self.formatter.format_league_standings(standings_data, league_name)
                await self._safe_send_message(update, formatted_standings)
            else:
                # Fallback vers l'ancien système
                standings = await self.advanced_commands.get_league_standings(league_name)
                await self._safe_send_message(update, standings)
                
        except Exception as e:
            logger.error(f"Erreur commande standings: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération du classement: {str(e)}")
    
    async def team_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les statistiques d'une équipe"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❓ Veuillez spécifier le nom d'une équipe.\n\n"
                    "Exemple: `/teamstats Real Madrid`",
                    parse_mode='Markdown'
                )
                return
            
            team_name = " ".join(context.args)
            stats = await self.advanced_commands.get_team_stats(team_name)
            await self._safe_send_message(update, stats)
        except Exception as e:
            logger.error(f"Erreur commande team_stats: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des statistiques: {str(e)}")
    
    async def upcoming_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les prochains matchs"""
        try:
            league_name = " ".join(context.args) if context.args else "Ligue 1"
            upcoming = await self.advanced_commands.get_upcoming_matches(league_name)
            await self._safe_send_message(update, upcoming)
        except Exception as e:
            logger.error(f"Erreur commande upcoming: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des matchs à venir: {str(e)}")
    
    async def compare_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour comparer deux équipes"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❓ Veuillez spécifier deux équipes à comparer.\n\n"
                    "Exemple: `/compare Real Madrid Barcelona`",
                    parse_mode='Markdown'
                )
                return
            
            team1 = context.args[0]
            team2 = " ".join(context.args[1:])
            
            comparison = await self.advanced_commands.compare_teams(team1, team2)
            await self._safe_send_message(update, comparison)
        except Exception as e:
            logger.error(f"Erreur commande compare: {e}")
            await self._send_error_message(update, f"Erreur lors de la comparaison: {str(e)}")
    
    async def help_advanced_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande d'aide pour les fonctionnalités avancées"""
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        
        # Utiliser le nouveau formateur pour créer un menu professionnel
        help_text = self.formatter.format_main_menu(user_settings)
        
        # Ajouter les nouvelles commandes
        enhanced_help = f"""

🚀 **NOUVELLES FONCTIONNALITÉS v2.0** 🚀

**📊 COMMANDES D'ANALYSE AVANCÉES:**
• `/analyze` - Analyser des matchs avec formatage professionnel
• `/compare [équipe1] [équipe2]` - Comparer deux équipes
• `/teamstats [équipe]` - Statistiques détaillées d'une équipe
• `/playerstats [joueur]` - Statistiques d'un joueur
• `/form [équipe]` - Analyse de forme d'une équipe
• `/h2h [équipe1] [équipe2]` - Historique des confrontations

**🏆 COMMANDES CHAMPIONNATS:**
• `/standings [championnat]` - Classement avec design professionnel
• `/upcoming [championnat]` - Prochains matchs
• `/live [championnat]` - Scores en direct
• `/league_stats [championnat]` - Statistiques de ligue
• `/set_league [championnat]` - Définir le championnat par défaut

**📰 COMMANDES ACTUALITÉS:**
• `/news [championnat]` - Dernières nouvelles
• `/transfers [équipe]` - Nouvelles de transferts
• `/injuries [équipe]` - Rapport de blessures

**🎯 COMMANDES SPÉCIALISÉES:**
• `/odds [match]` - Cotes de paris
• `/weather [match]` - Impact météo
• `/menu` - Menu interactif complet

**⚙️ COMMANDES PARAMÈTRES:**
• `/settings` - Afficher vos paramètres
• `/toggle_ia` - Activer/désactiver le mode IA
• `/ai_mode` - Mode IA avancé

**📈 CHAMPIONNATS SUPPORTÉS:**
• Ligue 1, Premier League, La Liga
• Bundesliga, Serie A, Champions League

**💡 EXEMPLES D'UTILISATION:**
```
/analyze
Real Madrid vs Barcelona
Liverpool vs Chelsea

/standings Premier League
/teamstats PSG
/compare Manchester City Arsenal
/playerstats Mbappé
/live Ligue 1
/news Premier League
```

**✨ AMÉLIORATIONS v2.0:**
• Formatage professionnel avec emojis et bordures
• Nouvelles commandes spécialisées
• Menu interactif complet
• Analyses plus détaillées
• Interface utilisateur améliorée
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    # Nouvelles commandes avancées
    async def live_scores_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les scores en direct"""
        try:
            league_name = " ".join(context.args) if context.args else "Ligue 1"
            live_scores = await self.enhanced_commands.get_live_scores(league_name)
            await self._safe_send_message(update, live_scores)
        except Exception as e:
            logger.error(f"Erreur commande live_scores: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des scores en direct: {str(e)}")
    
    async def player_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les statistiques d'un joueur"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❓ Veuillez spécifier le nom d'un joueur.\n\n"
                    "Exemple: `/playerstats Mbappé`",
                    parse_mode='Markdown'
                )
                return
            
            player_name = " ".join(context.args)
            player_stats = await self.enhanced_commands.get_player_stats(player_name)
            await self._safe_send_message(update, player_stats)
        except Exception as e:
            logger.error(f"Erreur commande player_stats: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des statistiques: {str(e)}")
    
    async def transfer_news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les nouvelles de transferts"""
        try:
            team_name = " ".join(context.args) if context.args else None
            transfer_news = await self.enhanced_commands.get_transfer_news(team_name)
            await self._safe_send_message(update, transfer_news)
        except Exception as e:
            logger.error(f"Erreur commande transfer_news: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des transferts: {str(e)}")
    
    async def injury_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher le rapport de blessures"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❓ Veuillez spécifier le nom d'une équipe.\n\n"
                    "Exemple: `/injuries PSG`",
                    parse_mode='Markdown'
                )
                return
            
            team_name = " ".join(context.args)
            injury_report = await self.enhanced_commands.get_injury_report(team_name)
            await self._safe_send_message(update, injury_report)
        except Exception as e:
            logger.error(f"Erreur commande injury_report: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération du rapport de blessures: {str(e)}")
    
    async def league_news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les nouvelles de ligue"""
        try:
            league_name = " ".join(context.args) if context.args else "Ligue 1"
            league_news = await self.enhanced_commands.get_league_news(league_name)
            await self._safe_send_message(update, league_news)
        except Exception as e:
            logger.error(f"Erreur commande league_news: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des nouvelles: {str(e)}")
    
    async def team_form_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour analyser la forme d'une équipe"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❓ Veuillez spécifier le nom d'une équipe.\n\n"
                    "Exemple: `/form PSG`",
                    parse_mode='Markdown'
                )
                return
            
            team_name = " ".join(context.args)
            team_form = await self.enhanced_commands.get_team_form_analysis(team_name)
            await self._safe_send_message(update, team_form)
        except Exception as e:
            logger.error(f"Erreur commande team_form: {e}")
            await self._send_error_message(update, f"Erreur lors de l'analyse de forme: {str(e)}")
    
    async def head_to_head_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour l'historique des confrontations"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❓ Veuillez spécifier deux équipes.\n\n"
                    "Exemple: `/h2h Real Madrid Barcelona`",
                    parse_mode='Markdown'
                )
                return
            
            team1 = context.args[0]
            team2 = " ".join(context.args[1:])
            
            h2h = await self.enhanced_commands.get_head_to_head(team1, team2)
            await self._safe_send_message(update, h2h)
        except Exception as e:
            logger.error(f"Erreur commande head_to_head: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération de l'historique: {str(e)}")
    
    async def league_statistics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour les statistiques de ligue"""
        try:
            league_name = " ".join(context.args) if context.args else "Ligue 1"
            league_stats = await self.enhanced_commands.get_league_statistics(league_name)
            await self._safe_send_message(update, league_stats)
        except Exception as e:
            logger.error(f"Erreur commande league_statistics: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des statistiques: {str(e)}")
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher le menu interactif complet"""
        try:
            user_id = update.effective_user.id
            user_settings = self.user_settings.get_user_settings(user_id)
            
            # Créer le menu interactif avec boutons
            keyboard = [
                [
                    InlineKeyboardButton("🔍 Analyser", callback_data="menu_analyze"),
                    InlineKeyboardButton("🏆 Classements", callback_data="menu_standings")
                ],
                [
                    InlineKeyboardButton("📊 Stats Équipes", callback_data="menu_team_stats"),
                    InlineKeyboardButton("⭐ Stats Joueurs", callback_data="menu_player_stats")
                ],
                [
                    InlineKeyboardButton("📅 Prochains Matchs", callback_data="menu_upcoming"),
                    InlineKeyboardButton("⚡ Scores en Direct", callback_data="menu_live")
                ],
                [
                    InlineKeyboardButton("📰 Actualités", callback_data="menu_news"),
                    InlineKeyboardButton("💰 Transferts", callback_data="menu_transfers")
                ],
                [
                    InlineKeyboardButton("💬 Chat IA", callback_data="menu_chat"),
                    InlineKeyboardButton("🎯 Prédictions", callback_data="menu_predictions")
                ],
                [
                    InlineKeyboardButton("⚙️ Paramètres", callback_data="menu_settings"),
                    InlineKeyboardButton("❓ Aide", callback_data="menu_help")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Utiliser le formateur pour créer un menu professionnel
            menu_text = self.formatter.format_main_menu(user_settings)
            
            await update.message.reply_text(
                menu_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Erreur commande menu: {e}")
            await self._send_error_message(update, f"Erreur lors de l'affichage du menu: {str(e)}")
    
    # Commandes de chat football avec l'IA
    async def footchat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour démarrer une conversation avec l'IA sur le football"""
        try:
            user_id = update.effective_user.id
            
            # Démarrer une nouvelle session de chat
            welcome_message = await self.football_chat.start_chat_session(user_id)
            
            # Créer des boutons d'action
            keyboard = [
                [
                    InlineKeyboardButton("📊 Statistiques Chat", callback_data="chat_stats"),
                    InlineKeyboardButton("❌ Terminer Chat", callback_data="end_chat")
                ],
                [
                    InlineKeyboardButton("💡 Sujets Populaires", callback_data="chat_topics"),
                    InlineKeyboardButton("🎯 Prédictions", callback_data="chat_predictions")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Erreur commande footchat: {e}")
            await self._send_error_message(update, f"Erreur lors du démarrage du chat: {str(e)}")
    
    async def endchat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour terminer la conversation avec l'IA"""
        try:
            user_id = update.effective_user.id
            
            if not self.football_chat.is_chat_active(user_id):
                await update.message.reply_text(
                    "❌ Aucune conversation active. Utilisez `/footchat` pour commencer une discussion !",
                    parse_mode='Markdown'
                )
                return
            
            # Terminer la session
            end_message = self.football_chat.end_chat_session(user_id)
            
            await update.message.reply_text(
                end_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erreur commande endchat: {e}")
            await self._send_error_message(update, f"Erreur lors de la fermeture du chat: {str(e)}")
    
    async def chatstats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande pour afficher les statistiques de la conversation"""
        try:
            user_id = update.effective_user.id
            
            if not self.football_chat.is_chat_active(user_id):
                await update.message.reply_text(
                    "❌ Aucune conversation active. Utilisez `/footchat` pour commencer une discussion !",
                    parse_mode='Markdown'
                )
                return
            
            # Récupérer les statistiques
            stats_message = self.football_chat.get_chat_stats(user_id)
            
            await update.message.reply_text(
                stats_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erreur commande chatstats: {e}")
            await self._send_error_message(update, f"Erreur lors de la récupération des stats: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire des messages texte avec support du chat IA"""
        message_text = update.message.text.strip()
        user_id = update.effective_user.id
        
        # Vérifier si l'utilisateur est en mode chat
        if self.football_chat.is_chat_active(user_id):
            # Traiter comme un message de chat
            chat_response = await self.football_chat.process_message(user_id, message_text)
            
            # Créer des boutons d'action pour le chat
            keyboard = [
                [
                    InlineKeyboardButton("📊 Stats Chat", callback_data="chat_stats"),
                    InlineKeyboardButton("❌ Terminer", callback_data="end_chat")
                ],
                [
                    InlineKeyboardButton("💡 Sujets", callback_data="chat_topics"),
                    InlineKeyboardButton("🎯 Prédictions", callback_data="chat_predictions")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                chat_response,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        # Vérifier si le message contient des matchs
        if self._contains_matches(message_text):
            await self._process_matches(update, context, message_text)
        else:
            # Message d'aide avec suggestion de chat
            help_message = """❓ Je ne reconnais pas de matchs dans votre message.

**Options disponibles :**

🔍 **Analyser des matchs :**
```
Real Madrid vs Barcelona
Liverpool vs Chelsea
```

💬 **Discuter de football :**
Utilisez `/footchat` pour commencer une conversation avec l'IA !

📱 **Autres commandes :**
• `/menu` - Menu complet
• `/help` - Aide détaillée
• `/standings` - Classements
• `/teamstats` - Statistiques d'équipe"""
            
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown'
            )
    
    async def _process_matches(self, update: Update, context: ContextTypes.DEFAULT_TYPE, matches_text: str, page: int = 1):
        """Traite les matchs et génère les analyses avec pagination"""
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        
        # Message de chargement
        loading_msg = await update.message.reply_text(
            "⚽ Analyse en cours... Veuillez patienter."
        )
        
        try:
            # Construire la clé de cache pour ces analyses
            cache_key = f"user_analysis_{user_id}_{hash(matches_text)}"
            
            # Vérifier si les analyses sont déjà en cache
            cached_analyses = self.user_cache.get(cache_key)
            
            if cached_analyses is None:
                # Analyser les matchs
                try:
                    analyses = self.analyzer.analyze_multiple_matches(matches_text)
                    
                    if not analyses:
                        await loading_msg.edit_text(
                            "❌ Aucun match valide trouvé dans votre message.\n\n"
                            "Format attendu :\n"
                            "Real Madrid vs Barcelona\n"
                            "Liverpool vs Chelsea"
                        )
                        return
                    
                    # Mettre en cache temporaire
                    self.user_cache[cache_key] = analyses
                    cached_analyses = analyses
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'analyse des matchs: {e}")
                    await loading_msg.edit_text(
                        f"❌ Erreur lors de l'analyse : {str(e)}\n\n"
                        "Veuillez réessayer ou contacter le support."
                    )
                    return
            
            # Utiliser la pagination
            pagination_data = self.paginator.paginate(cached_analyses, page)
            
            if not pagination_data['items']:
                await loading_msg.edit_text(
                    "❌ Aucun élément à afficher pour cette page."
                )
                return
            
            # Générer les réponses pour la page actuelle
            user_ai_enabled = user_settings.get('ai_mode', False)
            
            for i, analysis in enumerate(pagination_data['items']):
                if 'error' in analysis:
                    await self._send_error_message(update, analysis)
                else:
                    await self._send_analysis_message(update, analysis, user_ai_enabled)
                
                # Ajouter un délai entre les messages pour éviter le spam
                if i < len(pagination_data['items']) - 1:
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id,
                        action='typing'
                    )
            
            # Supprimer le message de chargement
            await loading_msg.delete()
            
            # Ajouter les boutons de navigation si nécessaire
            if pagination_data['total_pages'] > 1:
                await self._send_pagination_navigation(update, pagination_data, cache_key)
            
            # Envoyer un résumé de la page si plusieurs éléments
            if len(pagination_data['items']) > 1:
                await self._send_page_summary(update, pagination_data, user_ai_enabled)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {e}")
        
            # Utiliser le gestionnaire d'erreur pour une meilleure gestion
            error_info = self.error_handler.handle_api_error(e, "Analyse de matchs")
            
            await loading_msg.edit_text(
                f"❌ {error_info['user_message']}\n\n"
                f"{self.error_handler.get_fallback_message(error_info['code'])}"
            )
    
    def _clean_markdown(self, text: str) -> str:
        """Nettoie et valide le Markdown pour Telegram"""
        if not text:
            return text
        
        # Supprimer complètement le Markdown problématique
        import re
        
        # Supprimer tous les caractères Markdown
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # *texte* -> texte
        text = re.sub(r'_([^_]+)_', r'\1', text)    # _texte_ -> texte
        text = re.sub(r'`([^`]+)`', r'\1', text)    # `texte` -> texte
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # [texte](url) -> texte
        
        # Remplacer les caractères spéciaux problématiques
        text = text.replace('\\', '/')
        text = text.replace('*', '•')
        text = text.replace('_', '-')
        text = text.replace('`', "'")
        text = text.replace('[', '(')
        text = text.replace(']', ')')
        
        # Nettoyer les caractères de contrôle
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Limiter la longueur du message
        if len(text) > 4000:
            text = text[:4000] + "\n\n... (message tronqué)"
        
        return text
    
    async def _safe_send_message(self, update: Update, text: str, parse_mode: str = None, reply_markup=None):
        """Envoie un message de manière sécurisée sans Markdown"""
        # Nettoyer le texte complètement
        clean_text = self._clean_markdown(text)
        
        # Diviser le message en plusieurs parties si trop long
        max_length = 3000
        if len(clean_text) > max_length:
            parts = []
            current_part = ""
            lines = clean_text.split('\n')
            
            for line in lines:
                if len(current_part + line + '\n') > max_length:
                    if current_part:
                        parts.append(current_part.strip())
                        current_part = line + '\n'
                    else:
                        # Ligne trop longue, la diviser
                        words = line.split(' ')
                        temp_line = ""
                        for word in words:
                            if len(temp_line + word + ' ') > max_length:
                                if temp_line:
                                    parts.append(temp_line.strip())
                                    temp_line = word + ' '
                                else:
                                    parts.append(word)
                            else:
                                temp_line += word + ' '
                        current_part = temp_line
                else:
                    current_part += line + '\n'
            
            if current_part:
                parts.append(current_part.strip())
            
            # Envoyer chaque partie
            for i, part in enumerate(parts):
                try:
                    if i == 0:
                        await update.message.reply_text(
                            part,
                            reply_markup=reply_markup
                        )
                    else:
                        await update.message.reply_text(part)
                except Exception as e:
                    logger.error(f"Erreur envoi message partie {i}: {e}")
                    # Envoyer un message d'erreur simple
                    await update.message.reply_text(f"Erreur d'affichage de la partie {i+1}")
        else:
            # Message court, envoi normal
            try:
                await update.message.reply_text(
                    clean_text,
                    reply_markup=reply_markup
                )
            except Exception as e:
                logger.error(f"Erreur envoi message: {e}")
                # Message de fallback
                await update.message.reply_text(
                    "❌ Erreur d'affichage. Veuillez réessayer.",
                    reply_markup=reply_markup
                )
    
    async def _send_analysis_message(self, update: Update, analysis: Dict, ai_enabled: bool):
        """Envoie un message d'analyse avec le nouveau formatage professionnel"""
        try:
            # Utiliser le nouveau formateur professionnel
            formatted_message = self.formatter.format_match_analysis(analysis)
            
            # Améliorer avec l'IA si activé
            if ai_enabled and self.ai_module.is_enabled():
                enhanced_message = self.ai_module.enhance_analysis(analysis)
                if enhanced_message:
                    # Combiner le formatage professionnel avec l'amélioration IA
                    formatted_message = f"{formatted_message}\n\n🤖 **ANALYSE IA AMÉLIORÉE**\n{enhanced_message}"
            
            # Ajouter des boutons d'action
            keyboard = [
                [
                    InlineKeyboardButton("🎯 Prédiction", callback_data=f"pred_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}"),
                    InlineKeyboardButton("📊 Détails", callback_data=f"details_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}")
                ],
                [
                    InlineKeyboardButton("⚡ Scores en Direct", callback_data=f"live_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}"),
                    InlineKeyboardButton("📰 Actualités", callback_data=f"news_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Envoyer le message formaté
            await self._safe_send_message(update, formatted_message, None, reply_markup)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message d'analyse: {e}")
            # Fallback vers l'ancien système
            match_name = analysis.get('match', '')
            analysis_data = analysis.get('analysis', {})
            message = analysis_data.get('analysis_text', '')
            await self._safe_send_message(update, message)
    
    async def _send_error_message(self, update: Update, analysis: Dict):
        """Envoie un message d'erreur"""
        match_name = analysis.get('match', '')
        error_msg = analysis.get('error', 'Erreur inconnue')
        
        message = f"❌ Erreur pour {match_name} :\n{error_msg}"
        await self._safe_send_message(update, message)
    
    async def _send_summary(self, update: Update, analyses: List[Dict], ai_enabled: bool):
        """Envoie un résumé des analyses"""
        successful_analyses = [a for a in analyses if 'error' not in a]
        
        if not successful_analyses:
            return
        
        summary_text = f"📋 Résumé de {len(successful_analyses)} analyses :\n\n"
        
        # Améliorer avec l'IA si activé
        if ai_enabled and self.ai_module.is_enabled():
            enhanced_summary = self.ai_module.generate_match_summary(successful_analyses)
            if enhanced_summary:
                summary_text = enhanced_summary
        else:
            # Résumé basique
            for analysis in successful_analyses:
                match = analysis.get('match', '')
                risk = analysis.get('analysis', {}).get('risk_level', '')
                probabilities = analysis.get('analysis', {}).get('probabilities', {})
                
                summary_text += f"• {match} - Risque: {risk}\n"
                summary_text += f"  Probabilité victoire domicile: {probabilities.get('team1_win', 0)}%\n\n"
        
        await update.message.reply_text(
            summary_text,
            parse_mode='Markdown'
        )
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire des Perfum de pagination et nouvelles fonctionnalités"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = update.effective_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        user_ai_enabled = user_settings.get('ai_mode', False)
        
        try:
            if data.startswith('pred_'):
                # Afficher une prédiction détaillée
                team_ids = data.replace('pred_', '').split('_')
                if len(team_ids) == 2:
                    await self._show_prediction(query, team_ids[0], team_ids[1], user_ai_enabled)
            
            elif data.startswith('details_'):
                # Afficher plus de détails
                team_ids = data.replace('details_', '').split('_')
                if len(team_ids) == 2:
                    await self._show_details(query, team_ids[0], team_ids[1])
            
            elif data.startswith('_page_'):
                # Navigation de pagination
                page_num = int(data.split('_')[2])
                cache_key = '_'.join(data.split('_')[0:2])
                
                # Récupérer les analyses en cache
                cached_analyses = self.user_cache.get(cache_key)
                if cached_analyses:
                    await self._process_matches_callback(query, cached_analyses, page_num, user_ai_enabled)
                else:
                    await query.edit_message_text("❌ Session expirée. Réessayez l'analyse.")
            
            elif data == 'show_leagues':
                # Afficher les ligues disponibles
                leagues_text = self.league_manager.format_leagues_list()
                keyboard = [
                    [InlineKeyboardButton("🏠 Retour", callback_data="back_to_analyze")],
                    [InlineKeyboardButton("⚙️ Paramètres", callback_data="show_settings")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    f"{leagues_text}\n\nUtilisez /set_league CODE pour changer votre ligue préférée.",
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            elif data == 'show_settings':
                # Afficher les paramètres
                await self._show_settings_menu(query)
            
            elif data == 'change_league':
                # Changer de ligue
                await self._show_league_selection(query)
            
            elif data == 'toggle_ai_mode':
                # Basculer le mode IA
                new_mode = self.user_settings.toggle_ai_mode(user_id)
                action = "activé" if new_mode else "désactivé"
                
                await query.answer(f"Mode IA {action}!", show_alert=True)
                await self._show_settings_menu(query)
            
            elif data == 'show_stats':
                # Afficher les statistiques du cache
                cache_stats = self.user_settings.cache.get_stats()
                
                stats_text = f"📊 *Statistiques du cache :*\n\n"
                stats_text += f"• Entrées en mémoire : {cache_stats['memory_entries']}\n"
                stats_text += f"• Fichiers de cache : {cache_stats['file_entries']}\n"
                stats_text += f"• Dossier : `{cache_stats['cache_dir']}`"
                
                keyboard = [
                    [InlineKeyboardButton("🗑️ Vider le cache", callback_data="clear_cache")],
                    [InlineKeyboardButton("🏠 Retour", callback_data="show_settings")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    stats_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            elif data == 'clear_cache':
                # Vider le cache
                self.user_settings.cache.clear()
                self.user_cache.clear()  # Vider aussi le cache temporaire
                
                await query.answer("Cache vidé!", show_alert=True)
                await self._show_settings_menu(query)
            
            elif data == 'back_to_analyze':
                # Retour à l'analyse
                user_settings = self.user_settings.get_user_settings(user_id)
                league_info = self.league_manager.get_league_info(user_settings['league'])
                
                keyboard = [
                    [InlineKeyboardButton("🏆 Ligues disponibles", callback_data="show_leagues")],
                    [InlineKeyboardButton("⚙️ Paramètres", callback_data="show_settings")],
                    [InlineKeyboardButton("❓ Aide Analyse", callback_data="help_analyze")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    f"🔍 *Analyse de matchs*\n\n"
                    f"Ligue actuelle: **{user_settings['league']}**\n"
                    f"Mode IA: **{'Activé' if user_settings['ai_mode'] else 'Désactivé'}**\n\n"
                    "Envoyez vos matchs ou utilisez les options ci-dessous :",
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            elif data == 'help_analyze':
                # Aide pour l'analyse
                help_text = """
❓ *Aide pour l'analyse :*

📝 **Format des matchs :**
```
Real Madrid vs Barcelona
Liverpool vs Chelsea
PSG vs Marseille
```

⚙️ **Options avancées :**
• `/analyze --league PL` - Changer de ligue
• `/analyze --ai on` - Activer le mode IA

🎯 **Types d'analyses :**
• Probabilités de victoire/nul/défaite
• Plus de 2.5 buts dans le match
• Analyse de forme récente
• Performances à domicile/extérieur
• Niveau de risque

🏆 **Ligues supportées :**
PL (Premier League), PD (La Liga), SA (Serie A), 
BL1 (Bundesliga), FL1 (Ligue 1), PPL (Primeira Liga), 
CL (Champions League), EL (Europa League)
"""
                
                keyboard = [[InlineKeyboardButton("🏠 Retour", callback_data="back_to_analyze")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    help_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
                
            elif data.startswith('league_'):
                # Sélection de ligue
                league_code = data.replace('league_', '')
                if self.user_settings.set_league(user_id, league_code):
                    league_info = self.league_manager.get_league_info(league_code)
                    await query.answer(f"Ligue changée pour {league_info['name']}!", show_alert=True)
                    await self._show_settings_menu(query)
                else:
                    await query.answer("Erreur lors du changement de ligue!", show_alert=True)
            
            # Gestion des callbacks de chat
            elif data == 'chat_stats':
                # Afficher les statistiques de chat
                if self.football_chat.is_chat_active(user_id):
                    stats_message = self.football_chat.get_chat_stats(user_id)
                    await query.edit_message_text(stats_message, parse_mode='Markdown')
                else:
                    await query.answer("Aucune session de chat active!", show_alert=True)
            
            elif data == 'end_chat':
                # Terminer le chat
                if self.football_chat.is_chat_active(user_id):
                    end_message = self.football_chat.end_chat_session(user_id)
                    await query.edit_message_text(end_message, parse_mode='Markdown')
                else:
                    await query.answer("Aucune session de chat active!", show_alert=True)
            
            elif data == 'chat_topics':
                # Afficher les sujets de discussion
                topics_message = """💡 **Sujets de discussion populaires :**

⚽ **Matchs et Analyses :**
• Analyser un match récent
• Prédire le résultat d'un match
• Comparer deux équipes

🏆 **Championnats :**
• Discuter de la Ligue 1
• Analyser la Premier League
• Parler de la Champions League

⭐ **Joueurs :**
• Analyser les performances
• Discuter des transferts
• Comparer les joueurs

📊 **Statistiques :**
• Analyser les données
• Interpréter les tendances
• Faire des prédictions

🎯 **Tactiques :**
• Discuter des formations
• Analyser les stratégies
• Comparer les styles de jeu

Que veux-tu discuter ? 😊"""
                
                await query.edit_message_text(topics_message, parse_mode='Markdown')
            
            elif data == 'chat_predictions':
                # Afficher les options de prédictions
                predictions_message = """🎯 **Prédictions Football :**

Je peux t'aider à prédire :

⚽ **Résultats de matchs :**
• Victoire, nul ou défaite
• Score probable
• Facteurs clés

📊 **Performances :**
• Forme des équipes
• Tendances récentes
• Statistiques historiques

🏆 **Championnats :**
• Classements futurs
• Équipes favorites
• Surprises possibles

⭐ **Joueurs :**
• Performances attendues
• Impact sur les matchs
• Forme actuelle

Donne-moi un match ou une équipe et je te ferai une analyse détaillée ! 🚀"""
                
                await query.edit_message_text(predictions_message, parse_mode='Markdown')
            
            # Gestion des callbacks de menu
            elif data == 'menu_chat':
                # Démarrer le chat depuis le menu
                if not self.football_chat.is_chat_active(user_id):
                    welcome_message = await self.football_chat.start_chat_session(user_id)
                    
                    keyboard = [
                        [
                            InlineKeyboardButton("📊 Stats Chat", callback_data="chat_stats"),
                            InlineKeyboardButton("❌ Terminer Chat", callback_data="end_chat")
                        ],
                        [
                            InlineKeyboardButton("💡 Sujets Populaires", callback_data="chat_topics"),
                            InlineKeyboardButton("🎯 Prédictions", callback_data="chat_predictions")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await query.edit_message_text(
                        welcome_message,
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
                else:
                    await query.answer("Une session de chat est déjà active! Utilisez /endchat pour la terminer.", show_alert=True)
            
            elif data == 'menu_predictions':
                # Afficher les options de prédictions depuis le menu
                predictions_menu = """🎯 **Prédictions et Analyses :**

**Commandes disponibles :**

⚽ **Analyses de matchs :**
• `/analyze` - Analyser des matchs
• `/compare` - Comparer deux équipes
• `/h2h` - Historique des confrontations

📊 **Statistiques :**
• `/teamstats` - Stats d'équipe
• `/playerstats` - Stats de joueur
• `/form` - Analyse de forme

🏆 **Championnats :**
• `/standings` - Classements
• `/upcoming` - Prochains matchs
• `/league_stats` - Statistiques de ligue

💬 **Chat avec l'IA :**
• `/footchat` - Discuter de football
• Prédictions personnalisées
• Analyses détaillées

Que veux-tu analyser ? 🚀"""
                
                keyboard = [
                    [
                        InlineKeyboardButton("💬 Chat IA", callback_data="menu_chat"),
                        InlineKeyboardButton("🔍 Analyser", callback_data="menu_analyze")
                    ],
                    [
                        InlineKeyboardButton("🏠 Menu Principal", callback_data="back_to_menu")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    predictions_menu,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            elif data == 'back_to_menu':
                # Retour au menu principal
                user_settings = self.user_settings.get_user_settings(user_id)
                menu_text = self.formatter.format_main_menu(user_settings)
                
                keyboard = [
                    [
                        InlineKeyboardButton("🔍 Analyser", callback_data="menu_analyze"),
                        InlineKeyboardButton("🏆 Classements", callback_data="menu_standings")
                    ],
                    [
                        InlineKeyboardButton("📊 Stats Équipes", callback_data="menu_team_stats"),
                        InlineKeyboardButton("⭐ Stats Joueurs", callback_data="menu_player_stats")
                    ],
                    [
                        InlineKeyboardButton("📅 Prochains Matchs", callback_data="menu_upcoming"),
                        InlineKeyboardButton("⚡ Scores en Direct", callback_data="menu_live")
                    ],
                    [
                        InlineKeyboardButton("📰 Actualités", callback_data="menu_news"),
                        InlineKeyboardButton("💰 Transferts", callback_data="menu_transfers")
                    ],
                    [
                        InlineKeyboardButton("💬 Chat IA", callback_data="menu_chat"),
                        InlineKeyboardButton("🎯 Prédictions", callback_data="menu_predictions")
                    ],
                    [
                        InlineKeyboardButton("⚙️ Paramètres", callback_data="menu_settings"),
                        InlineKeyboardButton("❓ Aide", callback_data="menu_help")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    menu_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            else:
                await query.edit_message_text("❓ Action non reconnue.")
                
        except Exception as e:
            logger.error(f"Erreur callback query: {e}")
            await query.edit_message_text("❌ Une erreur s'est produite. Veuillez réessayer.")
    
    async def _show_prediction(self, query, team1_id: str, team2_id: str, ai_enabled: bool):
        """Affiche une prédiction détaillée"""
        try:
            # Récupérer les données de prédiction
            prediction_data = self.analyzer.api_client.get_match_prediction_data(
                int(team1_id), int(team2_id)
            )
            
            # Générer la prédiction
            if ai_enabled and self.ai_module.is_enabled():
                prediction_text = self.ai_module.generate_detailed_prediction(prediction_data)
            else:
                prediction_text = self.ai_module._generate_basic_prediction(prediction_data)
            
            await query.edit_message_text(
                prediction_text,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erreur prédiction: {e}")
            await query.edit_message_text(
                "❌ Impossible de générer la prédiction."
            )
    
    async def _show_details(self, query, team1_id: str, team2_id: str):
        """Affiche des détails supplémentaires"""
        try:
            # Récupérer les statistiques détaillées
            team1_stats = self.analyzer.api_client.get_team_statistics(int(team1_id))
            team2_stats = self.analyzer.api_client.get_team_statistics(int(team2_id))
            
            details_text = f"📊 *Détails des équipes :*\n\n"
            
            if team1_stats:
                details_text += f"🏠 *{team1_stats.get('name', 'Équipe 1')} :*\n"
                details_text += f"• Fondée en : {team1_stats.get('founded', 'N/A')}\n"
                details_text += f"• Stade : {team1_stats.get('venue', 'N/A')}\n"
                details_text += f"• Site web : {team1_stats.get('website', 'N/A')}\n\n"
            
            if team2_stats:
                details_text += f"✈️ *{team2_stats.get('name', 'Équipe 2')} :*\n"
                details_text += f"• Fondée en : {team2_stats.get('founded', 'N/A')}\n"
                details_text += f"• Stade : {team2_stats.get('venue', 'N/A')}\n"
                details_text += f"• Site web : {team2_stats.get('website', 'N/A')}\n"
            
            await query.edit_message_text(
                details_text,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erreur détails: {e}")
            await query.edit_message_text(
                "❌ Impossible de récupérer les détails."
            )
    
    def _contains_matches(self, text: str) -> bool:
        """Vérifie si le texte contient des matchs"""
        import re
        
        patterns = [
            r'\bvs\b',
            r'\bv\b',
            r'\bcontre\b',
            r'\b-\b'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    async def _send_pagination_navigation(self, update: Update, pagination_data: Dict, cache_key: str):
        """Envoie les boutons de navigation pour la pagination"""
        keyboard_data = self.paginator.create_navigation_keyboard(pagination_data, cache_key)
        keyboard = []
        
        for row in keyboard_data:
            buttons = []
            for button_data in row:
                buttons.append(InlineKeyboardButton(button_data.text, callback_data=button_data.callback_data))
            if buttons:
                keyboard.append(buttons)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        navigation_text = f"📄 **Page {pagination_data['current_page']}/{pagination_data['total_pages']}**\n"
        navigation_text += f"Éléments {pagination_data['start_index']}-{pagination_data['end_index']} sur {pagination_data['total_items']}"
        
        await update.message.reply_text(
            navigation_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def _send_page_summary(self, update: Update, pagination_data: Dict, ai_enabled: bool):
        """Envoie un résumé de la page courante"""
        successful_analyses = [a for a in pagination_data['items'] if 'error' not in a]
        
        if not successful_analyses:
            return
        
        summary_text = f"📋 *Résumé de la page {pagination_data['current_page']} :*\n\n"
        
        # Améliorer avec l'IA si activé
        if ai_enabled and self.ai_module.is_enabled():
            enhanced_summary = self.ai_module.generate_match_summary(successful_analyses)
            if enhanced_summary:
                summary_text = enhanced_summary
        else:
            # Résumé basique
            for analysis in successful_analyses:
                match = analysis.get('match', '')
                risk = analysis.get('analysis', {}).get('risk_level', '')
                probabilities = analysis.get('analysis', {}).get('probabilities', {})
                
                summary_text += f"• {match} - Risque: {risk}\n"
                summary_text += f"  Probabilité victoire domicile: {probabilities.get('team1_win', 0)}%\n\n"
        
        await update.message.reply_text(
            summary_text,
            parse_mode='Markdown'
        )
    
    async def _handle_league_change(self, update: Update, league_arg: str):
        """Gère le changement de ligue via /analyze"""
        user_id = update.effective_user.id
        
        if not league_arg:
            await self.set_league_command(update, None)
            return
        
        league_code = league_arg.upper()
        if self.user_settings.set_league(user_id, league_code):
            league_info = self.league_manager.get_league_info(league_code)
            await update.message.reply_text(
                f"✅ Ligue changée pour **{league_info['name']}** ({league_code})\n\n"
                "Vous pouvez maintenant analyser des matchs de cette ligue.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Code de ligue invalide. Utilisez /set_league pour voir les options."
            )
    
    async def _handle_ai_toggle(self, update: Update, ai_arg: str):
        """Gère le changement de mode IA via /analyze"""
        user_id = update.effective_user.id
        
        if not ai_arg:
            await self.toggle_ia_command(update, None)
            return
        
        ai_arg = ai_arg.lower()
        if ai_arg in ['on', 'enable', 'true', '1']:
            self.user_settings.update_user_setting(user_id, 'ai_mode', True)
            await update.message.reply_text(
                "🤖 Mode IA *activé* !\n\n"
                "Les analyses seront améliorées avec l'intelligence artificielle.",
                parse_mode='Markdown'
            )
        elif ai_arg in ['off', 'disable', 'false', '0']:
            self.user_settings.update_user_setting(user_id, 'ai_mode', False)
            await update.message.reply_text(
                "🤖 Mode IA *désactivé*.\n\n"
                "Retour aux analyses standard.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Argument invalide. Utilisez 'on' ou 'off', ou utilisez /toggle_ia."
            )

    async def _send_summary(self, update: Update, analyses: List[Dict], ai_enabled: bool):
        """Envoie un résumé des analyses (fonction existante mise à jour)"""
        successful_analyses = [a for a in analyses if 'error' not in a]
        
        if not successful_analyses:
            return
        
        summary_text = f"📋 Résumé de {len(successful_analyses)} analyses :\n\n"
        
        # Améliorer avec l'IA si activé
        if ai_enabled and self.ai_module.is_enabled():
            enhanced_summary = self.ai_module.generate_match_summary(successful_analyses)
            if enhanced_summary:
                summary_text = enhanced_summary
        else:
            # Résumé basique
            for analysis in successful_analyses[:5]:  # Limiter à 5 pour éviter le spam
                match = analysis.get('match', '')
                risk = analysis.get('analysis', {}).get('risk_level', '')
                probabilities = analysis.get('analysis', {}).get('probabilities', {})
                
                summary_text += f"• {match} - Risque: {risk}\n"
                summary_text += f"  Probabilité victoire domicile: {probabilities.get('team1_win', 0)}%\n\n"
        
        await update.message.reply_text(
            summary_text,
            parse_mode='Markdown'
        )

    async def _show_settings_menu(self, query):
        """Affiche le menu des paramètres"""
        user_id = query.from_user.id
        user_settings = self.user_settings.get_user_settings(user_id)
        league_info = self.league_manager.get_league_info(user_settings['league'])
        
        keyboard = [
            [InlineKeyboardButton("🏆 Changer de ligue", callback_data="change_league")],
            [InlineKeyboardButton("🤖 Mode IA", callback_data="toggle_ai_mode")],
            [InlineKeyboardButton("📊 Statistiques", callback_data="show_stats")],
            [InlineKeyboardButton("🗑️ Vider le cache", callback_data="clear_cache")],
            [InlineKeyboardButton("🏠 Retour à l'analyse", callback_data="back_to_analyze")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        settings_text = f"⚙️ *Paramètres utilisateur*\n\n"
        settings_text += f"🏆 **Ligue :** {league_info['name']} ({league_info['country']})\n"
        settings_text += f"🤖 **Mode IA :** {'Activé' if user_settings['ai_mode'] else 'Désactivé'}\n"
        settings_text += f"📄 **Langue :** {user_settings['language']}\n"
        settings_text += f"🔔 **Notifications :** {'Activées' if user_settings['notifications'] else 'Désactivées'}"
        
        await query.edit_message_text(
            settings_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def _show_league_selection(self, query):
        """Affiche la sélection de ligue"""
        leagues = self.league_manager.get_all_leagues()
        keyboard = []
        
        # Créer des boutons pour chaque ligue (2 par ligne)
        league_items = list(leagues.items())
        for i in range(0, len(league_items), 2):
            row = []
            for j in range(2):
                if i + j < len(league_items):
                    code, info = league_items[i + j]
                    row.append(InlineKeyboardButton(
                        f"{code} ({info['name'][:15]})", 
                        callback_data=f"league_{code}"
                    ))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🏠 Retour aux paramètres", callback_data="show_settings")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🏆 *Sélectionnez votre ligue préférée :*",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def _process_matches_callback(self, query, analyses, page, user_ai_enabled):
        """Traite les matchs pour affichage callback (pagination)"""
        try:
            pagination_data = self.paginator.paginate(analyses, page)
            
            if not pagination_data['items']:
                await query.edit_message_text("❌ Aucun élément à afficher pour cette page.")
                return
            
            # Envoyer les analyses de la page
            for i, analysis in enumerate(pagination_data['items']):
                if i == 0:
                    # Premier élément - éditer le message existant
                    if 'error' in analysis:
                        await query.edit_message_text(f"❌ *Erreur pour {analysis.get('match', '')} :*\n{analysis.get('error', '')}")
                    else:
                        await self._send_analysis_callback(query, analysis, user_ai_enabled)
                else:
                    # Autres éléments - nouveaux messages
                    chat_id = query.message.chat_id
                    if 'error' in analysis:
                        await query.bot.send_message(
                            chat_id,
                            f"❌ *Erreur pour {analysis.get('match', '')} :*\n{analysis.get('error', '')}",
                            parse_mode='Markdown'
                        )
                    else:
                        keyboard = [
                            [
                                InlineKeyboardButton("🎯 Prédiction", callback_data=f"pred_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}"),
                                InlineKeyboardButton("📊 Détails", callback_data=f"details_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}")
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        analysis_text = analysis.get('analysis', {}).get('analysis_text', '')
                        if user_ai_enabled and self.ai_module.is_enabled():
                            enhanced_text = self.ai_module.enhance_analysis(analysis)
                            if enhanced_text:
                                analysis_text = enhanced_text
                        
                        await query.bot.send_message(
                            chat_id,
                            analysis_text,
                            parse_mode='Markdown',
                            reply_markup=reply_markup
                        )
            
            # Ajouter la navigation de pagination
            await self._send_pagination_callback(query, pagination_data, f"user_analysis_{query.from_user.id}_{hash(str(analyses))}")
            
        except Exception as e:
            logger.error(f"Erreur process_matches_callback: {e}")
            await query.edit_message_text("❌ Erreur lors du traitement de la pagination.")
    
    async def _send_analysis_callback(self, query, analysis, ai_enabled):
        """Envoie l'analyse via callback"""
        analysis_text = analysis.get('analysis', {}).get('analysis_text', '')
        
        if ai_enabled and self.ai_module.is_enabled():
            enhanced_text = self.ai_module.enhance_analysis(analysis)
            if enhanced_text:
                analysis_text = enhanced_text
        
        keyboard = [
            [
                InlineKeyboardButton("🎯 Prédiction", callback_data=f"pred_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}"),
                InlineKeyboardButton("📊 Détails", callback_data=f"details_{analysis.get('team1', {}).get('id', '')}_{analysis.get('team2', {}).get('id', '')}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            analysis_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def _send_pagination_callback(self, query, pagination_data, cache_key):
        """Envoie la navigation pagination via callback"""
        keyboard_data = self.paginator.create_navigation_keyboard(pagination_data, cache_key)
        keyboard = []
        
        for row in keyboard_data:
            buttons = []
            for button_data in row:
                buttons.append(InlineKeyboardButton(button_data.text, callback_data=button_data.callback_data))
            if buttons:
                keyboard.append(buttons)
        
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            navigation_text = f"📄 **Page {pagination_data['current_page']}/{pagination_data['total_pages']}**\n"
            navigation_text += f"Éléments {pagination_data['start_index']}-{pagination_data['end_index']} sur {pagination_data['total_items']}"
            
            await query.bot.send_message(
                query.message.chat_id,
                navigation_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    
    def get_handlers(self):
        """Retourne la liste des gestionnaires avec toutes les nouvelles commandes"""
        return [
            # Commandes de base
            CommandHandler("start", self.start_command),
            CommandHandler("help", self.help_command),
            CommandHandler("help_advanced", self.help_advanced_command),
            CommandHandler("menu", self.menu_command),
            
            # Commandes d'analyse
            CommandHandler("analyze", self.analyze_command),
            CommandHandler("compare", self.compare_command),
            CommandHandler("teamstats", self.team_stats_command),
            CommandHandler("playerstats", self.player_stats_command),
            CommandHandler("form", self.team_form_command),
            CommandHandler("h2h", self.head_to_head_command),
            
            # Commandes championnats
            CommandHandler("standings", self.standings_command),
            CommandHandler("upcoming", self.upcoming_command),
            CommandHandler("live", self.live_scores_command),
            CommandHandler("league_stats", self.league_statistics_command),
            CommandHandler("set_league", self.set_league_command),
            
            # Commandes actualités
            CommandHandler("news", self.league_news_command),
            CommandHandler("transfers", self.transfer_news_command),
            CommandHandler("injuries", self.injury_report_command),
            
            # Commandes paramètres
            CommandHandler("settings", self.settings_command),
            CommandHandler("toggle_ia", self.toggle_ia_command),
            CommandHandler("ai_mode", self.ai_mode_command),
            
            # Commandes chat football IA
            CommandHandler("footchat", self.footchat_command),
            CommandHandler("endchat", self.endchat_command),
            CommandHandler("chatstats", self.chatstats_command),
            
            # Gestionnaires de messages et callbacks
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message),
            CallbackQueryHandler(self.handle_callback_query)
        ]
