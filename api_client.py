"""
Client API pour récupérer les données de football
Utilise l'API Football-Data.org
"""
import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
from config import Config
from utils import CacheManager, ErrorHandler

# Configuration du logger
logger = logging.getLogger(__name__)

class FootballAPIClient:
    """Client pour interagir avec l'API Football-Data.org"""
    
    def __init__(self):
        self.api_key = Config.FOOTBALL_API_KEY
        self.base_url = Config.FOOTBALL_API_BASE_URL
        self.headers = {
            'X-Auth-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        self.cache = CacheManager(cache_dir="cache/football_api", default_ttl=600)  # 10 minutes
        self.error_handler = ErrorHandler()
        
    def _make_request(self, endpoint: str, params: Dict = None, use_cache: bool = True) -> Optional[Dict]:
        """Effectue une requête à l'API avec gestion d'erreurs et cache"""
        # Créer une clé de cache
        cache_key = f"api_{endpoint}_{hash(str(params)) if params else 'default'}"
        
        # Vérifier le cache si activé
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Mettre en cache si succès
                if use_cache:
                    self.cache.set(cache_key, data, ttl=600)  # 10 minutes
                return data
            elif response.status_code == 429:  # Rate limit
                error_info = self.error_handler.handle_api_error(
                    Exception(f"Rate limit exceeded: {response.status_code}"), 
                    f"API endpoint: {endpoint}"
                )
                raise Exception(error_info['user_message'])
            elif response.status_code == 404:
                error_info = self.error_handler.handle_api_error(
                    Exception("Resource not found"), 
                    f"API endpoint: {endpoint}"
                )
                return None
            else:
                error_info = self.error_handler.handle_api_error(
                    Exception(f"API error: {response.status_code} - {response.text}"), 
                    f"API endpoint: {endpoint}"
                )
                return None
                
        except requests.exceptions.Timeout:
            error_info = self.error_handler.handle_api_error(
                Exception("Request timeout"), 
                f"API endpoint: {endpoint}"
            )
            raise Exception(error_info['user_message'])
        except requests.exceptions.ConnectionError:
            error_info = self.error_handler.handle_api_error(
                Exception("Connection error"), 
                f"API endpoint: {endpoint}"
            )
            raise Exception(error_info['user_message'])
        except requests.exceptions.RequestException as e:
            error_info = self.error_handler.handle_api_error(e, f"API endpoint: {endpoint}")
            raise Exception(error_info['user_message'])
    
    def search_team(self, team_name: str) -> Optional[Dict]:
        """Recherche une équipe par nom"""
        try:
            # Recherche dans les équipes populaires
            teams_data = self._make_request("teams")
            if not teams_data:
                logger.error("Aucune donnée d'équipes reçue de l'API")
                return None
                
            # Normaliser le nom de l'équipe pour la recherche
            normalized_name = team_name.lower().strip()
            logger.info(f"Recherche de l'équipe: {normalized_name}")
            
            # Liste des équipes populaires pour le fallback
            popular_teams = {
                'real madrid': {'id': 86, 'name': 'Real Madrid CF', 'shortName': 'Real Madrid'},
                'barcelona': {'id': 81, 'name': 'FC Barcelona', 'shortName': 'Barcelona'},
                'liverpool': {'id': 64, 'name': 'Liverpool FC', 'shortName': 'Liverpool'},
                'chelsea': {'id': 61, 'name': 'Chelsea FC', 'shortName': 'Chelsea'},
                'manchester united': {'id': 66, 'name': 'Manchester United FC', 'shortName': 'Man United'},
                'manchester city': {'id': 65, 'name': 'Manchester City FC', 'shortName': 'Man City'},
                'arsenal': {'id': 57, 'name': 'Arsenal FC', 'shortName': 'Arsenal'},
                'tottenham': {'id': 73, 'name': 'Tottenham Hotspur FC', 'shortName': 'Tottenham'},
                'psg': {'id': 524, 'name': 'Paris Saint-Germain FC', 'shortName': 'PSG'},
                'marseille': {'id': 516, 'name': 'Olympique de Marseille', 'shortName': 'Marseille'},
                'juventus': {'id': 109, 'name': 'Juventus FC', 'shortName': 'Juventus'},
                'milan': {'id': 98, 'name': 'AC Milan', 'shortName': 'Milan'},
                'inter': {'id': 108, 'name': 'Inter Milan', 'shortName': 'Inter'},
                'bayern': {'id': 5, 'name': 'FC Bayern München', 'shortName': 'Bayern Munich'},
                'dortmund': {'id': 4, 'name': 'Borussia Dortmund', 'shortName': 'Dortmund'},
            }
            
            # Vérifier d'abord dans les équipes populaires
            if normalized_name in popular_teams:
                logger.info(f"Équipe trouvée dans la liste populaire: {popular_teams[normalized_name]}")
                return popular_teams[normalized_name]
            
            # Recherche dans les données de l'API
            for team in teams_data.get('teams', []):
                team_name_lower = team.get('name', '').lower()
                short_name_lower = team.get('shortName', '').lower()
                
                if (normalized_name in team_name_lower or 
                    normalized_name in short_name_lower or
                    any(word in team_name_lower for word in normalized_name.split()) or
                    any(word in short_name_lower for word in normalized_name.split())):
                    logger.info(f"Équipe trouvée dans l'API: {team.get('name')}")
                    return team
                    
            logger.warning(f"Équipe non trouvée: {team_name}")
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche d'équipe {team_name}: {e}")
            return None
    
    def get_team_matches(self, team_id: int, limit: int = 10) -> List[Dict]:
        """Récupère les matchs récents d'une équipe"""
        params = {
            'limit': limit,
            'status': 'FINISHED'
        }
        
        matches_data = self._make_request(f"teams/{team_id}/matches", params)
        if matches_data:
            return matches_data.get('matches', [])
        return []
    
    def get_team_statistics(self, team_id: int) -> Dict:
        """Récupère les statistiques d'une équipe"""
        stats_data = self._make_request(f"teams/{team_id}")
        if stats_data:
            return {
                'name': stats_data.get('name', ''),
                'shortName': stats_data.get('shortName', ''),
                'founded': stats_data.get('founded', ''),
                'venue': stats_data.get('venue', ''),
                'website': stats_data.get('website', ''),
                'squad': stats_data.get('squad', [])
            }
        return {}
    
    def analyze_team_form(self, team_id: int) -> Dict:
        """Analyse la forme récente d'une équipe"""
        matches = self.get_team_matches(team_id, 10)
        if not matches:
            return {'error': 'Aucun match récent trouvé'}
        
        # Analyser les 5 derniers matchs
        recent_matches = matches[:5]
        
        wins = 0
        draws = 0
        losses = 0
        goals_scored = 0
        goals_conceded = 0
        home_performance = {'wins': 0, 'draws': 0, 'losses': 0}
        away_performance = {'wins': 0, 'draws': 0, 'losses': 0}
        
        for match in recent_matches:
            home_team = match.get('homeTeam', {})
            away_team = match.get('awayTeam', {})
            score = match.get('score', {})
            
            # Déterminer si l'équipe jouait à domicile ou à l'extérieur
            is_home = home_team.get('id') == team_id
            
            if is_home:
                team_score = score.get('fullTime', {}).get('home', 0)
                opponent_score = score.get('fullTime', {}).get('away', 0)
            else:
                team_score = score.get('fullTime', {}).get('away', 0)
                opponent_score = score.get('fullTime', {}).get('home', 0)
            
            goals_scored += team_score
            goals_conceded += opponent_score
            
            # Déterminer le résultat
            if team_score > opponent_score:
                wins += 1
                if is_home:
                    home_performance['wins'] += 1
                else:
                    away_performance['wins'] += 1
            elif team_score == opponent_score:
                draws += 1
                if is_home:
                    home_performance['draws'] += 1
                else:
                    away_performance['draws'] += 1
            else:
                losses += 1
                if is_home:
                    home_performance['losses'] += 1
                else:
                    away_performance['losses'] += 1
        
        total_matches = len(recent_matches)
        
        return {
            'total_matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_rate': (wins / total_matches * 100) if total_matches > 0 else 0,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'avg_goals_scored': goals_scored / total_matches if total_matches > 0 else 0,
            'avg_goals_conceded': goals_conceded / total_matches if total_matches > 0 else 0,
            'home_performance': home_performance,
            'away_performance': away_performance,
            'form': self._calculate_form_string(wins, draws, losses)
        }
    
    def _calculate_form_string(self, wins: int, draws: int, losses: int) -> str:
        """Calcule une chaîne de forme (ex: WWDLW)"""
        form_chars = []
        total = wins + draws + losses
        
        # Approximation basée sur les pourcentages
        win_chars = int((wins / total) * 5) if total > 0 else 0
        draw_chars = int((draws / total) * 5) if total > 0 else 0
        loss_chars = 5 - win_chars - draw_chars
        
        form_chars.extend(['W'] * win_chars)
        form_chars.extend(['D'] * draw_chars)
        form_chars.extend(['L'] * loss_chars)
        
        return ''.join(form_chars[:5])
    
    def get_match_prediction_data(self, team1_id: int, team2_id: int) -> Dict:
        """Récupère les données pour prédire un match"""
        team1_form = self.analyze_team_form(team1_id)
        team2_form = self.analyze_team_form(team2_id)
        
        team1_stats = self.get_team_statistics(team1_id)
        team2_stats = self.get_team_statistics(team2_id)
        
        return {
            'team1': {
                'id': team1_id,
                'stats': team1_stats,
                'form': team1_form
            },
            'team2': {
                'id': team2_id,
                'stats': team2_stats,
                'form': team2_form
            }
        }
