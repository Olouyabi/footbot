"""
Utilitaires communs pour le bot FootStat Analyzer
Inclut le système de cache, gestion d'erreurs, et fonctions utilitaires
"""
import json
import time
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class CacheManager:
    """Gestionnaire de cache pour les données API"""
    
    def __init__(self, cache_dir: str = "cache", default_ttl: int = 300):
        """
        Initialise le gestionnaire de cache
        
        Args:
            cache_dir: Dossier pour stocker les fichiers de cache
            default_ttl: TTL par défaut en secondes (5 minutes)
        """
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self.memory_cache = {}  # Cache en mémoire pour les données fréquentes
        
        # Créer le dossier de cache s'il n'existe pas
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key: str, use_memory: bool = True) -> Optional[Any]:
        """
        Récupère une valeur du cache
        
        Args:
            key: Clé de cache
            use_memory: Utiliser le cache mémoire
            
        Returns:
            Valeur mise en cache ou None
        """
        # Essayer d'abord le cache mémoire
        if use_memory and key in self.memory_cache:
            data, timestamp, ttl = self.memory_cache[key]
            if time.time() - timestamp < ttl:
                logger.debug(f"Cache hit (memory): {key}")
                return data
            else:
                del self.memory_cache[key]
        
        # Essayer le cache fichier
        cache_file = os.path.join(self.cache_dir, f"{key.replace('/', '_')}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                timestamp = cache_data.get('timestamp', 0)
                ttl = cache_data.get('ttl', self.default_ttl)
                
                if time.time() - timestamp < ttl:
                    logger.debug(f"Cache hit (file): {key}")
                    data = cache_data.get('data')
                    # Mettre en cache mémoire
                    self.memory_cache[key] = (data, timestamp, ttl)
                    return data
                else:
                    # Supprimer le fichier expiré
                    os.remove(cache_file)
            except Exception as e:
                logger.error(f"Erreur lecture cache {key}: {e}")
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, use_memory: bool = True) -> bool:
        """
        Met une valeur en cache
        
        Args:
            key: Clé de cache
            value: Valeur à mettre en cache
            ttl: TTL en secondes (None = défaut)
            use_memory: Utiliser le cache mémoire
            
        Returns:
            True si succès
        """
        try:
            ttl = ttl or self.default_ttl
            timestamp = time.time()
            
            # Cache mémoire
            if use_memory:
                self.memory_cache[key] = (value, timestamp, ttl)
            
            # Cache fichier
            cache_file = os.path.join(self.cache_dir, f"{key.replace('/', '_')}.json")
            cache_data = {
                'data': value,
                'timestamp': timestamp,
                'ttl': ttl,
                'created_at': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"Erreur écriture cache {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Supprime une entrée du cache"""
        try:
            # Supprimer du cache mémoire
            if key in self.memory_cache:
                del self.memory_cache[key]
            
            # Supprimer le fichier de cache
            cache_file = os.path.join(self.cache_dir, f"{key.replace('/', '_')}.json")
            if os.path.exists(cache_file):
                os.remove(cache_file)
            
            logger.debug(f"Cache deleted: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur suppression cache {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Vide tout le cache"""
        try:
            # Vider le cache mémoire
            self.memory_cache.clear()
            
            # Supprimer tous les fichiers de cache
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
            
            logger.info("Cache cleared")
            return True
            
        except Exception as e:
            logger.error(f"Erreur clear cache: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques du cache"""
        memory_count = len(self.memory_cache)
        file_count = len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
        
        return {
            'memory_entries': memory_count,
            'file_entries': file_count,
            'cache_dir': self.cache_dir
        }

class ErrorHandler:
    """Gestionnaire d'erreurs centralisé"""
    
    ERROR_CODES = {
        'API_UNAVAILABLE': 'API temporairement indisponible',
        'INVALID_TEAM': 'Équipe non trouvée',
        'RATE_LIMIT': 'Limite de requêtes atteinte',
        'NETWORK_ERROR': 'Erreur de connexion',
        'PARSE_ERROR': 'Erreur de parsing des données',
        'CACHE_ERROR': 'Erreur de cache',
        'UNKNOWN_ERROR': 'Erreur inconnue'
    }
    
    @staticmethod
    def handle_api_error(error: Exception, context: str = "") -> Dict:
        """
        Gère les erreurs d'API et retourne un dictionnaire d'erreur
        
        Args:
            error: Exception levée
            context: Contexte de l'erreur
            
        Returns:
            Dictionnaire avec les informations d'erreur
        """
        error_str = str(error).lower()
        
        if 'rate limit' in error_str or '429' in error_str:
            error_code = 'RATE_LIMIT'
            user_message = "⏳ Trop de requêtes. Veuillez patienter avant de réessayer."
        elif 'not found' in error_str or '404' in error_str:
            error_code = 'INVALID_TEAM'
            user_message = "❌ Équipe non trouvée. Vérifiez le nom de l'équipe."
        elif 'network' in error_str or 'connect' in error_str:
            error_code = 'NETWORK_ERROR'
            user_message = "🌐 Problème de connexion. Veuillez réessayer."
        elif 'timeout' in error_str:
            error_code = 'NETWORK_ERROR'
            user_message = "⏰ Délai d'attente dépassé. Veuillez réessayer."
        else:
            error_code = 'API_UNAVAILABLE'
            user_message = "🔧 Service temporairement indisponible. Réessayez plus tard."
        
        error_info = {
            'code': error_code,
            'message': ErrorHandler.ERROR_CODES.get(error_code, 'Erreur inconnue'),
            'user_message': user_message,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'original_error': str(error)
        }
        
        logger.error(f"Erreur API ({error_code}): {error_info['message']} - {context}")
        return error_info
    
    @staticmethod
    def handle_parsing_error(error: Exception, context: str = "") -> Dict:
        """Gère les erreurs de parsing"""
        error_info = {
            'code': 'PARSE_ERROR',
            'message': 'Erreur de parsing des données',
            'user_message': '📄 Erreur lors du traitement des données.',
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'original_error': str(error)
        }
        
        logger.error(f"Erreur parsing: {context} - {str(error)}")
        return error_info
    
    @staticmethod
    def get_fallback_message(error_code: str) -> str:
        """Retourne un message de fallback selon le code d'erreur"""
        fallbacks = {
            'API_UNAVAILABLE': "🔄 Veuillez réessayer dans quelques instants.",
            'INVALID_TEAM': "💡 Essayez d'utiliser le nom complet de l'équipe.",
            'RATE_LIMIT': "⏳ Attendez une minute avant de faire une nouvelle requête.",
            'NETWORK_ERROR': "🌐 Vérifiez votre connexion internet.",
            'PARSE_ERROR': "📄 Contactez le support si le problème persiste.",
            'CACHE_ERROR': "🗄️ Problème de cache, réessayez.",
            'UNKNOWN_ERROR': "❓ Une erreur inattendue s'est produite."
        }
        
        return fallbacks.get(error_code, "❓ Erreur inconnue.")

class Paginator:
    """Gestionnaire de pagination pour les résultats"""
    
    def __init__(self, items_per_page: int = 3):
        """
        Initialise le paginateur
        
        Args:
            items_per_page: Nombre d'éléments par page
        """
        self.items_per_page = items_per_page
    
    def paginate(self, items: List[Any], current_page: int = 1) -> Dict:
        """
        Pagine une liste d'éléments
        
        Args:
            items: Liste à paginer
            current_page: Page actuelle (1-indexed)
            
        Returns:
            Dictionnaire avec les données paginées
        """
        if not items:
            return {
                'items': [],
                'current_page': 1,
                'total_pages': 0,
                'total_items': 0,
                'has_previous': False,
                'has_next': False,
                'start_index': 0,
                'end_index': 0
            }
        
        total_items = len(items)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        
        # Valider la page actuelle
        current_page = max(1, min(current_page, total_pages)) if total_pages > 0 else 1
        
        # Calculer les indices
        start_index = (current_page - 1) * self.items_per_page
        end_index = min(start_index + self.items_per_page, total_items)
        
        # Extraire les éléments de la page
        page_items = items[start_index:end_index]
        
        return {
            'items': page_items,
            'current_page': current_page,
            'total_pages': total_pages,
            'total_items': total_items,
            'has_previous': current_page > 1,
            'has_next': current_page < total_pages,
            'start_index': start_index + 1,
            'end_index': end_index,
            'previous_page': current_page - 1 if current_page > 1 else None,
            'next_page': current_page + 1 if current_page < total_pages else None
        }
    
    def create_navigation_keyboard(self, pagination_data: Dict, callback_prefix: str) -> List[List]:
        """
        Crée un clavier de navigation pour la pagination
        
        Args:
            pagination_data: Données de pagination
            callback_prefix: Préfixe pour les callbacks
            
        Returns:
            Liste de listes pour le clavier Telegram
        """
        keyboard = []
        
        # Boutons de navigation
        nav_buttons = []
        
        if pagination_data['has_previous']:
            nav_buttons.append(
                InlineKeyboardButton(
                    "◀️ Précédent", 
                    callback_data=f"{callback_prefix}_page_{pagination_data['previous_page']}"
                )
            )
        
        if pagination_data['has_next']:
            nav_buttons.append(
                InlineKeyboardButton(
                    "Suivant ▶️", 
                    callback_data=f"{callback_prefix}_page_{pagination_data['next_page']}"
                )
            )
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Indicateur de page
        info_button = InlineKeyboardButton(
            f"📄 Page {pagination_data['current_page']}/{pagination_data['total_pages']}",
            callback_data="page_info"
        )
        keyboard.append([info_button])
        
        return keyboard

class UserSettings:
    """Gestionnaire des paramètres utilisateur"""
    
    DEFAULT_LEAGUE = 'PL'
    DEFAULT_PAGE_SIZE = 3
    DEFAULT_AI_MODE = False
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
    
    def get_user_settings(self, user_id: int) -> Dict:
        """Récupère les paramètres d'un utilisateur"""
        cache_key = f"user_settings_{user_id}"
        settings = self.cache.get(cache_key)
        
        if settings is None:
            settings = {
                'league': self.DEFAULT_LEAGUE,
                'page_size': self.DEFAULT_PAGE_SIZE,
                'ai_mode': self.DEFAULT_AI_MODE,
                'language': 'fr',
                'notifications': True,
                'created_at': datetime.now().isoformat()
            }
            self.cache.set(cache_key, settings, ttl=86400)  # 24h
        
        return settings
    
    def update_user_setting(self, user_id: int, key: str, value: Any) -> bool:
        """Met à jour un paramètre utilisateur"""
        settings = self.get_user_settings(user_id)
        settings[key] = value
        settings['updated_at'] = datetime.now().isoformat()
        
        cache_key = f"user_settings_{user_id}"
        return self.cache.set(cache_key, settings, ttl=86400)
    
    def set_league(self, user_id: int, league: str) -> bool:
        """Définit la ligue préférée de l'utilisateur"""
        valid_leagues = ['PL', 'PD', 'SA', 'BL1', 'FL1', 'PPL', 'CL', 'EL']
        if league.upper() in valid_leagues:
            return self.update_user_setting(user_id, 'league', league.upper())
        return False
    
    def toggle_ai_mode(self, user_id: int) -> bool:
        """Bascule le mode IA"""
        settings = self.get_user_settings(user_id)
        new_mode = not settings.get('ai_mode', False)
        return self.update_user_setting(user_id, 'ai_mode', new_mode)

class LeagueManager:
    """Gestionnaire des ligues et compétitions"""
    
    LEAGUES = {
        'PL': {'name': 'Premier League', 'country': 'Angleterre', 'teams': 20},
        'PD': {'name': 'La Liga', 'country': 'Espagne', 'teams': 20},
        'SA': {'name': 'Serie A', 'country': 'Italie', 'teams': 20},
        'BL1': {'name': 'Bundesliga', 'country': 'Allemagne', 'teams': 18},
        'FL1': {'name': 'Ligue 1', 'country': 'France', 'teams': 20},
        'PPL': {'name': 'Primeira Liga', 'country': 'Portugal', 'teams': 18},
        'CL': {'name': 'Champions League', 'country': 'Europe', 'teams': 32},
        'EL': {'name': 'Europa League', 'country': 'Europe', 'teams': 48}
    }
    
    @classmethod
    def get_league_info(cls, league_code: str) -> Optional[Dict]:
        """Récupère les informations d'une ligue"""
        return cls.LEAGUES.get(league_code.upper())
    
    @classmethod
    def get_sformat(cls, league_code: str) -> str:
        """Retourne le format de saison pour une ligue"""
        league_info = cls.get_league_info(league_code)
        if not league_info:
            return "2024"
        
        # Logique pour calculer la saison actuelle
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Les saisons européennes commencent généralement en août
        if current_month >= 8:
            return f"{current_year}"
        else:
            return f"{current_year - 1}"
    
    @classmethod
    def get_all_leagues(cls) -> Dict:
        """Retourne toutes les ligues disponibles"""
        return cls.LEAGUES.copy()
    
    @classmethod
    def format_leagues_list(cls) -> str:
        """Formate la liste des ligues pour l'affichage"""
        lines = ["🏆 *Ligues disponibles :*\n"]
        
        for code, info in cls.LEAGUES.items():
            lines.append(f"• **{code}** - {info['name']} ({info['country']})")
        
        return "\n".join(lines)
