"""
Module de chat football avec l'IA pour le bot FootStat Analyzer v2.0
Permet aux utilisateurs de discuter de football avec l'intelligence artificielle
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from ai_module import AIModule
from formatter import ProfessionalFormatter

logger = logging.getLogger(__name__)

class FootballChat:
    """Gestionnaire de chat football avec l'IA"""
    
    def __init__(self):
        self.ai_module = AIModule()
        self.formatter = ProfessionalFormatter()
        self.chat_sessions = {}  # Sessions de chat par utilisateur
        self.football_context = self._load_football_context()
    
    def _load_football_context(self) -> Dict:
        """Charge le contexte football pour l'IA"""
        return {
            "sport": "football",
            "leagues": [
                "Ligue 1", "Premier League", "La Liga", "Bundesliga", 
                "Serie A", "Champions League", "Europa League"
            ],
            "topics": [
                "matchs", "équipes", "joueurs", "transferts", "tactiques",
                "statistiques", "prédictions", "actualités", "blessures",
                "classements", "buts", "performances", "formes"
            ],
            "personality": "expert football passionné et informatif",
            "style": "conversationnel mais professionnel"
        }
    
    async def start_chat_session(self, user_id: int) -> str:
        """Démarre une nouvelle session de chat"""
        try:
            # Initialiser la session
            self.chat_sessions[user_id] = {
                "started_at": datetime.now(),
                "message_count": 0,
                "context": self.football_context.copy(),
                "conversation_history": []
            }
            
            # Message de bienvenue personnalisé
            welcome_message = await self._generate_welcome_message(user_id)
            
            return self.formatter._create_header("CHAT FOOTBALL IA", "🤖") + "\n\n" + welcome_message
            
        except Exception as e:
            logger.error(f"Erreur démarrage session chat: {e}")
            return "❌ Erreur lors du démarrage de la conversation. Veuillez réessayer."
    
    async def process_message(self, user_id: int, message: str) -> str:
        """Traite un message de l'utilisateur"""
        try:
            # Vérifier si la session existe
            if user_id not in self.chat_sessions:
                return await self.start_chat_session(user_id)
            
            session = self.chat_sessions[user_id]
            session["message_count"] += 1
            
            # Ajouter le message à l'historique
            session["conversation_history"].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now()
            })
            
            # Générer la réponse de l'IA
            ai_response = await self._generate_ai_response(user_id, message, session)
            
            # Ajouter la réponse à l'historique
            session["conversation_history"].append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now()
            })
            
            # Formater la réponse
            formatted_response = self._format_chat_response(ai_response, session)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Erreur traitement message chat: {e}")
            return "❌ Désolé, j'ai rencontré un problème. Pouvez-vous reformuler votre question ?"
    
    async def _generate_welcome_message(self, user_id: int) -> str:
        """Génère un message de bienvenue personnalisé"""
        try:
            if not self.ai_module.is_enabled():
                return self._get_fallback_welcome()
            
            # Prompt pour l'IA
            prompt = f"""
Tu es un expert football passionné et informatif. Tu viens de commencer une conversation avec un utilisateur sur le football.

Contexte:
- Tu es intégré dans un bot d'analyse football (FootStat Analyzer v2.0)
- Tu peux discuter de tous les aspects du football
- Tu es passionné, informatif et engageant
- Tu utilises des emojis appropriés
- Tu peux donner des analyses, prédictions et conseils

Génère un message de bienvenue chaleureux et engageant (2-3 phrases maximum) qui:
1. Salue l'utilisateur
2. Exprime ta passion pour le football
3. Invite à la discussion
4. Mentionne quelques sujets que tu peux aborder

Style: Conversationnel, passionné, avec des emojis football appropriés.
"""
            
            response = self.ai_module.enhance_analysis({"analysis": {"analysis_text": prompt}})
            return response if response else self._get_fallback_welcome()
            
        except Exception as e:
            logger.error(f"Erreur génération message bienvenue: {e}")
            return self._get_fallback_welcome()
    
    async def _generate_ai_response(self, user_id: int, message: str, session: Dict) -> str:
        """Génère une réponse de l'IA basée sur le message de l'utilisateur"""
        try:
            if not self.ai_module.is_enabled():
                return self._get_fallback_response(message)
            
            # Construire le contexte de la conversation
            context = self._build_conversation_context(session)
            
            # Prompt pour l'IA
            prompt = f"""
Tu es un expert football passionné et informatif intégré dans FootStat Analyzer v2.0.

CONTEXTE FOOTBALL:
- Ligues: {', '.join(self.football_context['leagues'])}
- Sujets: {', '.join(self.football_context['topics'])}
- Tu es un expert avec des connaissances approfondies

HISTORIQUE DE LA CONVERSATION:
{context}

MESSAGE DE L'UTILISATEUR: "{message}"

INSTRUCTIONS:
1. Réponds de manière naturelle et engageante
2. Utilise des emojis football appropriés
3. Sois informatif mais conversationnel
4. Si c'est une question technique, donne des détails
5. Si c'est une opinion, partage ton expertise
6. Reste dans le contexte football
7. Limite ta réponse à 3-4 phrases maximum
8. Utilise un ton passionné mais professionnel

Réponds maintenant:
"""
            
            response = self.ai_module.enhance_analysis({"analysis": {"analysis_text": prompt}})
            return response if response else self._get_fallback_response(message)
            
        except Exception as e:
            logger.error(f"Erreur génération réponse IA: {e}")
            return self._get_fallback_response(message)
    
    def _build_conversation_context(self, session: Dict) -> str:
        """Construit le contexte de la conversation"""
        history = session.get("conversation_history", [])
        
        if not history:
            return "Aucun historique de conversation."
        
        # Prendre les 5 derniers échanges
        recent_history = history[-10:]  # 5 échanges (10 messages)
        
        context_lines = []
        for msg in recent_history:
            role = "Utilisateur" if msg["role"] == "user" else "IA"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            context_lines.append(f"{role}: {content}")
        
        return "\n".join(context_lines)
    
    def _format_chat_response(self, response: str, session: Dict) -> str:
        """Formate la réponse de chat"""
        try:
            # Ajouter des informations de session
            message_count = session["message_count"]
            session_duration = datetime.now() - session["started_at"]
            duration_minutes = int(session_duration.total_seconds() / 60)
            
            # Formater la réponse
            formatted = f"🤖 **IA Football Expert**\n\n"
            formatted += f"{response}\n\n"
            formatted += f"💬 Messages: {message_count} | ⏱️ Durée: {duration_minutes}min"
            
            # Ajouter des suggestions de sujets
            if message_count % 3 == 0:  # Tous les 3 messages
                suggestions = self._get_topic_suggestions()
                formatted += f"\n\n💡 **Sujets à explorer:**\n{suggestions}"
            
            return formatted
            
        except Exception as e:
            logger.error(f"Erreur formatage réponse chat: {e}")
            return f"🤖 **IA Football Expert**\n\n{response}"
    
    def _get_topic_suggestions(self) -> str:
        """Génère des suggestions de sujets"""
        suggestions = [
            "⚽ Analyser un match récent",
            "🏆 Discuter d'un championnat",
            "📊 Comparer des équipes",
            "🎯 Prédire un résultat",
            "💰 Parler des transferts",
            "🏥 Évoquer les blessures",
            "📈 Analyser les performances",
            "🎮 Discuter des tactiques"
        ]
        
        # Sélectionner 3 suggestions aléatoires
        import random
        selected = random.sample(suggestions, 3)
        return "\n".join([f"• {s}" for s in selected])
    
    def _get_fallback_welcome(self) -> str:
        """Message de bienvenue de fallback"""
        return """⚽ Salut ! Je suis ton expert football IA ! 

Je suis là pour discuter de tout ce qui concerne le football : matchs, équipes, joueurs, tactiques, transferts, et bien plus encore !

Que veux-tu savoir sur le football aujourd'hui ? 🚀"""
    
    def _get_fallback_response(self, message: str) -> str:
        """Réponse de fallback quand l'IA n'est pas disponible"""
        message_lower = message.lower()
        
        # Réponses basiques basées sur des mots-clés
        if any(word in message_lower for word in ["match", "jeu", "game"]):
            return "⚽ Les matchs sont toujours passionnants ! Quel match t'intéresse ? Je peux analyser les statistiques, les tactiques, ou prédire le résultat !"
        
        elif any(word in message_lower for word in ["équipe", "team", "club"]):
            return "🏆 Les équipes ont chacune leur style et leur histoire ! De quelle équipe veux-tu parler ? Je connais bien les grandes équipes européennes !"
        
        elif any(word in message_lower for word in ["joueur", "player", "footballeur"]):
            return "⭐ Les joueurs sont le cœur du football ! Qui t'intéresse ? Je peux parler de leurs performances, leur style de jeu, ou leurs statistiques !"
        
        elif any(word in message_lower for word in ["transfert", "transfer", "mercato"]):
            return "💰 Les transferts sont toujours excitants ! Le mercato d'hiver approche. De quels transferts veux-tu discuter ?"
        
        elif any(word in message_lower for word in ["prédiction", "prediction", "pronostic"]):
            return "🎯 J'adore faire des prédictions ! Donne-moi un match et je t'expliquerai mon analyse basée sur les statistiques et la forme des équipes !"
        
        else:
            return "⚽ Intéressant ! Peux-tu me dire plus sur ce qui t'intéresse ? Je peux parler de matchs, équipes, joueurs, tactiques, transferts, et bien d'autres sujets football !"
    
    def end_chat_session(self, user_id: int) -> str:
        """Termine une session de chat"""
        try:
            if user_id not in self.chat_sessions:
                return "❌ Aucune session de chat active."
            
            session = self.chat_sessions[user_id]
            message_count = session["message_count"]
            session_duration = datetime.now() - session["started_at"]
            duration_minutes = int(session_duration.total_seconds() / 60)
            
            # Supprimer la session
            del self.chat_sessions[user_id]
            
            return f"""👋 **Session de chat terminée !**

📊 **Statistiques de la conversation:**
• Messages échangés: {message_count}
• Durée: {duration_minutes} minutes
• Sujets abordés: Football ⚽

Merci pour cette discussion passionnante ! N'hésite pas à revenir pour discuter de football ! 🚀"""
            
        except Exception as e:
            logger.error(f"Erreur fin session chat: {e}")
            return "❌ Erreur lors de la fermeture de la session."
    
    def get_chat_stats(self, user_id: int) -> str:
        """Retourne les statistiques de la session de chat"""
        try:
            if user_id not in self.chat_sessions:
                return "❌ Aucune session de chat active."
            
            session = self.chat_sessions[user_id]
            message_count = session["message_count"]
            session_duration = datetime.now() - session["started_at"]
            duration_minutes = int(session_duration.total_seconds() / 60)
            
            return f"""📊 **Statistiques de la conversation:**

• Messages échangés: {message_count}
• Durée de la session: {duration_minutes} minutes
• Statut IA: {'✅ Activée' if self.ai_module.is_enabled() else '❌ Désactivée'}
• Sujets disponibles: {len(self.football_context['topics'])}"""
            
        except Exception as e:
            logger.error(f"Erreur stats chat: {e}")
            return "❌ Erreur lors de la récupération des statistiques."
    
    def is_chat_active(self, user_id: int) -> bool:
        """Vérifie si une session de chat est active"""
        return user_id in self.chat_sessions
    
    def get_active_sessions_count(self) -> int:
        """Retourne le nombre de sessions actives"""
        return len(self.chat_sessions)
