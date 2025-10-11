"""
Module des commandes avancées et nouvelles fonctionnalités pour le bot FootStat Analyzer
Ajoute des fonctionnalités professionnelles et un menu complet
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
from api_client import FootballAPIClient
from utils import CacheManager, UserSettings
from formatter import ProfessionalFormatter

logger = logging.getLogger(__name__)

class EnhancedCommands:
    """Gestionnaire des commandes avancées et nouvelles fonctionnalités"""
    
    def __init__(self):
        self.api_client = FootballAPIClient()
        self.cache = CacheManager(cache_dir="cache/enhanced", default_ttl=300)
        self.user_settings = UserSettings(self.cache)
        self.formatter = ProfessionalFormatter()
    
    async def get_live_scores(self, league_name: str = "Ligue 1") -> str:
        """Récupère les scores en direct d'une ligue"""
        try:
            leagues = {
                "ligue 1": "FL1",
                "premier league": "PL",
                "la liga": "PD",
                "bundesliga": "BL1",
                "serie a": "SA",
                "champions league": "CL"
            }
            
            league_code = leagues.get(league_name.lower(), "FL1")
            
            # Vérifier le cache
            cache_key = f"live_scores_{league_code}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_live_scores(cached_data, league_name)
            
            # Récupérer les matchs en cours
            matches_data = self.api_client._make_request(f"competitions/{league_code}/matches", {
                'status': 'IN_PLAY'
            })
            
            if not matches_data:
                return f"❌ Aucun match en cours pour {league_name}"
            
            # Mettre en cache (TTL court pour les scores en direct)
            self.cache.set(cache_key, matches_data, ttl=60)  # 1 minute
            
            return self.formatter.format_live_scores(matches_data, league_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des scores en direct: {e}")
            return f"❌ Erreur lors de la récupération des scores en direct"
    
    async def get_player_stats(self, player_name: str) -> str:
        """Récupère les statistiques d'un joueur"""
        try:
            # Vérifier le cache
            cache_key = f"player_stats_{player_name.lower()}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_player_stats(cached_data, player_name)
            
            # Générer des données simulées pour les joueurs populaires
            stats_data = self._generate_mock_player_stats(player_name)
            
            if not stats_data:
                return f"❌ Joueur '{player_name}' non trouvé dans notre base de données"
            
            # Mettre en cache
            self.cache.set(cache_key, stats_data, ttl=1800)  # 30 minutes
            
            return self.formatter.format_player_stats(stats_data, player_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats de joueur: {e}")
            return f"❌ Erreur lors de la récupération des statistiques de {player_name}"
    
    async def get_transfer_news(self, team_name: str = None) -> str:
        """Récupère les dernières nouvelles de transferts"""
        try:
            # Vérifier le cache
            cache_key = f"transfer_news_{team_name or 'all'}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_transfer_news(cached_data, team_name)
            
            # Simuler des données de transferts (en attendant une vraie API)
            transfer_data = self._generate_mock_transfer_data(team_name)
            
            # Mettre en cache
            self.cache.set(cache_key, transfer_data, ttl=3600)  # 1 heure
            
            return self.formatter.format_transfer_news(transfer_data, team_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des transferts: {e}")
            return f"❌ Erreur lors de la récupération des nouvelles de transferts"
    
    async def get_injury_report(self, team_name: str) -> str:
        """Récupère le rapport des blessures d'une équipe"""
        try:
            # Rechercher l'équipe
            team_data = self.api_client.search_team(team_name)
            if not team_data:
                return f"❌ Équipe '{team_name}' non trouvée"
            
            team_id = team_data['id']
            
            # Vérifier le cache
            cache_key = f"injury_report_{team_id}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_injury_report(cached_data, team_data['name'])
            
            # Simuler des données de blessures (en attendant une vraie API)
            injury_data = self._generate_mock_injury_data(team_name)
            
            # Mettre en cache
            self.cache.set(cache_key, injury_data, ttl=1800)
            
            return self.formatter.format_injury_report(injury_data, team_data['name'])
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du rapport de blessures: {e}")
            return f"❌ Erreur lors de la récupération du rapport de blessures"
    
    async def get_league_news(self, league_name: str = "Ligue 1") -> str:
        """Récupère les dernières nouvelles d'une ligue"""
        try:
            # Vérifier le cache
            cache_key = f"league_news_{league_name.lower()}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_league_news(cached_data, league_name)
            
            # Simuler des données de nouvelles (en attendant une vraie API)
            news_data = self._generate_mock_news_data(league_name)
            
            # Mettre en cache
            self.cache.set(cache_key, news_data, ttl=1800)
            
            return self.formatter.format_league_news(news_data, league_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des nouvelles: {e}")
            return f"❌ Erreur lors de la récupération des nouvelles de {league_name}"
    
    async def get_weather_impact(self, match_info: Dict) -> str:
        """Analyse l'impact de la météo sur un match"""
        try:
            # Simuler une analyse météo (en attendant une vraie API météo)
            weather_data = self._generate_mock_weather_data(match_info)
            
            return self.formatter.format_weather_impact(weather_data, match_info)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse météo: {e}")
            return f"❌ Erreur lors de l'analyse de l'impact météo"
    
    async def get_betting_odds(self, match_info: Dict) -> str:
        """Récupère les cotes de paris pour un match"""
        try:
            # Simuler des cotes (en attendant une vraie API de paris)
            odds_data = self._generate_mock_odds_data(match_info)
            
            return self.formatter.format_betting_odds(odds_data, match_info)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des cotes: {e}")
            return f"❌ Erreur lors de la récupération des cotes de paris"
    
    async def get_team_form_analysis(self, team_name: str, period: str = "last_5") -> str:
        """Analyse la forme d'une équipe sur une période donnée"""
        try:
            # Rechercher l'équipe
            team_data = self.api_client.search_team(team_name)
            if not team_data:
                return f"❌ Équipe '{team_name}' non trouvée"
            
            team_id = team_data['id']
            
            # Vérifier le cache
            cache_key = f"team_form_{team_id}_{period}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_team_form_analysis(cached_data, team_name, period)
            
            # Récupérer les matchs récents
            matches_data = self.api_client._make_request(f"teams/{team_id}/matches", {
                'status': 'FINISHED',
                'limit': 10
            })
            
            if not matches_data:
                return f"❌ Aucune donnée de forme disponible pour {team_name}"
            
            # Analyser la forme
            form_analysis = self._analyze_team_form(matches_data, team_name, period)
            
            # Mettre en cache
            self.cache.set(cache_key, form_analysis, ttl=1800)
            
            return self.formatter.format_team_form_analysis(form_analysis, team_name, period)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de forme: {e}")
            return f"❌ Erreur lors de l'analyse de la forme de {team_name}"
    
    async def get_head_to_head(self, team1_name: str, team2_name: str) -> str:
        """Récupère l'historique des confrontations entre deux équipes"""
        try:
            # Rechercher les équipes
            team1_data = self.api_client.search_team(team1_name)
            team2_data = self.api_client.search_team(team2_name)
            
            if not team1_data:
                return f"❌ Équipe '{team1_name}' non trouvée"
            if not team2_data:
                return f"❌ Équipe '{team2_name}' non trouvée"
            
            team1_id = team1_data['id']
            team2_id = team2_data['id']
            
            # Vérifier le cache
            cache_key = f"h2h_{team1_id}_{team2_id}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_head_to_head(cached_data, team1_name, team2_name)
            
            # Récupérer l'historique des confrontations
            h2h_data = self.api_client._make_request(f"teams/{team1_id}/matches", {
                'status': 'FINISHED',
                'limit': 20
            })
            
            if not h2h_data:
                return f"❌ Aucun historique de confrontation disponible"
            
            # Filtrer les matchs entre les deux équipes
            h2h_matches = self._filter_h2h_matches(h2h_data, team1_name, team2_name)
            
            # Analyser les confrontations
            h2h_analysis = self._analyze_h2h_matches(h2h_matches, team1_name, team2_name)
            
            # Mettre en cache
            self.cache.set(cache_key, h2h_analysis, ttl=3600)
            
            return self.formatter.format_head_to_head(h2h_analysis, team1_name, team2_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du H2H: {e}")
            return f"❌ Erreur lors de la récupération de l'historique des confrontations"
    
    async def get_league_statistics(self, league_name: str) -> str:
        """Récupère les statistiques générales d'une ligue"""
        try:
            leagues = {
                "ligue 1": "FL1",
                "premier league": "PL",
                "la liga": "PD",
                "bundesliga": "BL1",
                "serie a": "SA",
                "champions league": "CL"
            }
            
            league_code = leagues.get(league_name.lower(), "FL1")
            
            # Vérifier le cache
            cache_key = f"league_stats_{league_code}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self.formatter.format_league_statistics(cached_data, league_name)
            
            # Récupérer les statistiques de la ligue
            standings_data = self.api_client._make_request(f"competitions/{league_code}/standings")
            matches_data = self.api_client._make_request(f"competitions/{league_code}/matches", {
                'status': 'FINISHED',
                'limit': 100
            })
            
            if not standings_data or not matches_data:
                return f"❌ Impossible de récupérer les statistiques de {league_name}"
            
            # Analyser les statistiques
            league_stats = self._analyze_league_statistics(standings_data, matches_data)
            
            # Mettre en cache
            self.cache.set(cache_key, league_stats, ttl=3600)
            
            return self.formatter.format_league_statistics(league_stats, league_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats de ligue: {e}")
            return f"❌ Erreur lors de la récupération des statistiques de {league_name}"
    
    def _generate_mock_transfer_data(self, team_name: str = None) -> Dict:
        """Génère des données de transferts simulées"""
        transfers = [
            {
                "player": "Kylian Mbappé",
                "from_team": "PSG",
                "to_team": "Real Madrid",
                "fee": "180M€",
                "status": "Confirmé",
                "date": "2024-01-15"
            },
            {
                "player": "Erling Haaland",
                "from_team": "Borussia Dortmund",
                "to_team": "Manchester City",
                "fee": "60M€",
                "status": "Confirmé",
                "date": "2024-01-10"
            },
            {
                "player": "Jude Bellingham",
                "from_team": "Borussia Dortmund",
                "to_team": "Real Madrid",
                "fee": "103M€",
                "status": "Confirmé",
                "date": "2024-01-05"
            }
        ]
        
        if team_name:
            transfers = [t for t in transfers if team_name.lower() in t['from_team'].lower() or team_name.lower() in t['to_team'].lower()]
        
        return {"transfers": transfers}
    
    def _generate_mock_player_stats(self, player_name: str) -> Optional[Dict]:
        """Génère des données simulées pour les joueurs populaires"""
        player_name_lower = player_name.lower()
        
        # Base de données de joueurs populaires avec leurs statistiques
        players_db = {
            'mbappé': {
                'name': 'Kylian Mbappé',
                'position': 'Attaquant',
                'team': 'Paris Saint-Germain',
                'age': 25,
                'nationality': 'France',
                'stats': {
                    'goals': 28,
                    'assists': 8,
                    'matches_played': 35,
                    'minutes_played': 2980,
                    'goals_per_match': 0.8,
                    'assists_per_match': 0.23,
                    'rating': 8.7,
                    'form': 'Excellent'
                }
            },
            'messi': {
                'name': 'Lionel Messi',
                'position': 'Attaquant',
                'team': 'Inter Miami',
                'age': 36,
                'nationality': 'Argentine',
                'stats': {
                    'goals': 22,
                    'assists': 15,
                    'matches_played': 32,
                    'minutes_played': 2750,
                    'goals_per_match': 0.69,
                    'assists_per_match': 0.47,
                    'rating': 8.9,
                    'form': 'Excellent'
                }
            },
            'ronaldo': {
                'name': 'Cristiano Ronaldo',
                'position': 'Attaquant',
                'team': 'Al-Nassr',
                'age': 39,
                'nationality': 'Portugal',
                'stats': {
                    'goals': 35,
                    'assists': 6,
                    'matches_played': 38,
                    'minutes_played': 3420,
                    'goals_per_match': 0.92,
                    'assists_per_match': 0.16,
                    'rating': 8.5,
                    'form': 'Très bon'
                }
            },
            'haaland': {
                'name': 'Erling Haaland',
                'position': 'Attaquant',
                'team': 'Manchester City',
                'age': 24,
                'nationality': 'Norvège',
                'stats': {
                    'goals': 32,
                    'assists': 5,
                    'matches_played': 33,
                    'minutes_played': 2870,
                    'goals_per_match': 0.97,
                    'assists_per_match': 0.15,
                    'rating': 8.8,
                    'form': 'Excellent'
                }
            },
            'benzema': {
                'name': 'Karim Benzema',
                'position': 'Attaquant',
                'team': 'Al-Ittihad',
                'age': 36,
                'nationality': 'France',
                'stats': {
                    'goals': 18,
                    'assists': 7,
                    'matches_played': 28,
                    'minutes_played': 2450,
                    'goals_per_match': 0.64,
                    'assists_per_match': 0.25,
                    'rating': 8.2,
                    'form': 'Bon'
                }
            },
            'neymar': {
                'name': 'Neymar Jr',
                'position': 'Attaquant',
                'team': 'Al-Hilal',
                'age': 32,
                'nationality': 'Brésil',
                'stats': {
                    'goals': 15,
                    'assists': 12,
                    'matches_played': 25,
                    'minutes_played': 2100,
                    'goals_per_match': 0.6,
                    'assists_per_match': 0.48,
                    'rating': 8.3,
                    'form': 'Bon'
                }
            },
            'modric': {
                'name': 'Luka Modrić',
                'position': 'Milieu de terrain',
                'team': 'Real Madrid',
                'age': 38,
                'nationality': 'Croatie',
                'stats': {
                    'goals': 3,
                    'assists': 8,
                    'matches_played': 30,
                    'minutes_played': 2650,
                    'goals_per_match': 0.1,
                    'assists_per_match': 0.27,
                    'rating': 8.1,
                    'form': 'Bon'
                }
            },
            'de bruyne': {
                'name': 'Kevin De Bruyne',
                'position': 'Milieu de terrain',
                'team': 'Manchester City',
                'age': 33,
                'nationality': 'Belgique',
                'stats': {
                    'goals': 6,
                    'assists': 18,
                    'matches_played': 28,
                    'minutes_played': 2480,
                    'goals_per_match': 0.21,
                    'assists_per_match': 0.64,
                    'rating': 8.6,
                    'form': 'Excellent'
                }
            }
        }
        
        # Rechercher le joueur (recherche partielle)
        for key, player_data in players_db.items():
            if key in player_name_lower or player_name_lower in key:
                return player_data
        
        # Si pas trouvé, retourner None
        return None
    
    def _generate_mock_injury_data(self, team_name: str) -> Dict:
        """Génère des données de blessures simulées"""
        injuries = [
            {
                "player": "Neymar Jr",
                "injury": "Entorse de la cheville",
                "severity": "Moyenne",
                "expected_return": "2-3 semaines",
                "status": "En cours"
            },
            {
                "player": "Marquinhos",
                "injury": "Fatigue musculaire",
                "severity": "Légère",
                "expected_return": "1 semaine",
                "status": "En cours"
            }
        ]
        
        return {"injuries": injuries, "team": team_name}
    
    def _generate_mock_news_data(self, league_name: str) -> Dict:
        """Génère des données de nouvelles simulées"""
        news = [
            {
                "title": f"Actualités {league_name} - Semaine en cours",
                "summary": "Les dernières nouvelles de la ligue",
                "date": datetime.now().strftime('%Y-%m-%d'),
                "category": "Général"
            },
            {
                "title": "Transferts d'hiver en cours",
                "summary": "Les clubs se préparent pour le mercato d'hiver",
                "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                "category": "Transferts"
            }
        ]
        
        return {"news": news, "league": league_name}
    
    def _generate_mock_weather_data(self, match_info: Dict) -> Dict:
        """Génère des données météo simulées"""
        return {
            "temperature": "15°C",
            "conditions": "Nuageux",
            "humidity": "65%",
            "wind": "10 km/h",
            "impact": "Faible impact sur le jeu"
        }
    
    def _generate_mock_odds_data(self, match_info: Dict) -> Dict:
        """Génère des cotes de paris simulées"""
        return {
            "home_win": 2.10,
            "draw": 3.20,
            "away_win": 3.50,
            "over_2_5": 1.85,
            "under_2_5": 1.95,
            "both_teams_score": 1.70
        }
    
    def _analyze_team_form(self, matches_data: Dict, team_name: str, period: str) -> Dict:
        """Analyse la forme d'une équipe"""
        matches = matches_data.get('matches', [])
        
        # Prendre les matchs selon la période
        if period == "last_5":
            recent_matches = matches[-5:]
        elif period == "last_10":
            recent_matches = matches[-10:]
        else:
            recent_matches = matches
        
        # Analyser les résultats
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        
        for match in recent_matches:
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            score = match.get('score', {}).get('fullTime', {})
            
            home_goals = score.get('home', 0)
            away_goals = score.get('away', 0)
            
            if home_team == team_name:
                goals_for += home_goals
                goals_against += away_goals
                if home_goals > away_goals:
                    wins += 1
                elif home_goals == away_goals:
                    draws += 1
                else:
                    losses += 1
            else:
                goals_for += away_goals
                goals_against += home_goals
                if away_goals > home_goals:
                    wins += 1
                elif away_goals == home_goals:
                    draws += 1
                else:
                    losses += 1
        
        return {
            "period": period,
            "matches_analyzed": len(recent_matches),
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "form_rating": self._calculate_form_rating(wins, draws, losses, len(recent_matches))
        }
    
    def _filter_h2h_matches(self, matches_data: Dict, team1_name: str, team2_name: str) -> List[Dict]:
        """Filtre les matchs entre deux équipes spécifiques"""
        matches = matches_data.get('matches', [])
        h2h_matches = []
        
        for match in matches:
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            
            if ((home_team == team1_name and away_team == team2_name) or
                (home_team == team2_name and away_team == team1_name)):
                h2h_matches.append(match)
        
        return h2h_matches
    
    def _analyze_h2h_matches(self, h2h_matches: List[Dict], team1_name: str, team2_name: str) -> Dict:
        """Analyse les confrontations directes"""
        if not h2h_matches:
            return {"error": "Aucune confrontation directe trouvée"}
        
        team1_wins = 0
        team2_wins = 0
        draws = 0
        team1_goals = 0
        team2_goals = 0
        
        for match in h2h_matches:
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            score = match.get('score', {}).get('fullTime', {})
            
            home_goals = score.get('home', 0)
            away_goals = score.get('away', 0)
            
            if home_team == team1_name:
                team1_goals += home_goals
                team2_goals += away_goals
                if home_goals > away_goals:
                    team1_wins += 1
                elif home_goals == away_goals:
                    draws += 1
                else:
                    team2_wins += 1
            else:
                team1_goals += away_goals
                team2_goals += home_goals
                if away_goals > home_goals:
                    team1_wins += 1
                elif away_goals == home_goals:
                    draws += 1
                else:
                    team2_wins += 1
        
        return {
            "total_matches": len(h2h_matches),
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "draws": draws,
            "team1_goals": team1_goals,
            "team2_goals": team2_goals,
            "team1_name": team1_name,
            "team2_name": team2_name
        }
    
    def _analyze_league_statistics(self, standings_data: Dict, matches_data: Dict) -> Dict:
        """Analyse les statistiques générales d'une ligue"""
        standings = standings_data.get('standings', [])
        matches = matches_data.get('matches', [])
        
        if not standings or not matches:
            return {"error": "Données insuffisantes"}
        
        table = standings[0].get('table', [])
        
        # Statistiques générales
        total_teams = len(table)
        total_matches = len(matches)
        total_goals = sum(match.get('score', {}).get('fullTime', {}).get('home', 0) + 
                         match.get('score', {}).get('fullTime', {}).get('away', 0) 
                         for match in matches)
        
        # Moyennes
        avg_goals_per_match = total_goals / total_matches if total_matches > 0 else 0
        avg_goals_per_team = total_goals / total_teams if total_teams > 0 else 0
        
        return {
            "total_teams": total_teams,
            "total_matches": total_matches,
            "total_goals": total_goals,
            "avg_goals_per_match": avg_goals_per_match,
            "avg_goals_per_team": avg_goals_per_team,
            "most_goals_team": max(table, key=lambda x: x.get('goalsFor', 0)) if table else None,
            "least_goals_conceded": min(table, key=lambda x: x.get('goalsAgainst', 0)) if table else None
        }
    
    def _calculate_form_rating(self, wins: int, draws: int, losses: int, total_matches: int) -> str:
        """Calcule une note de forme basée sur les résultats"""
        if total_matches == 0:
            return "N/A"
        
        points = wins * 3 + draws
        max_points = total_matches * 3
        percentage = (points / max_points) * 100
        
        if percentage >= 80:
            return "Excellent"
        elif percentage >= 60:
            return "Bon"
        elif percentage >= 40:
            return "Moyen"
        elif percentage >= 20:
            return "Faible"
        else:
            return "Très faible"
