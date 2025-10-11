"""
Module des commandes avancées du bot
Contient les nouvelles fonctionnalités et commandes
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from api_client import FootballAPIClient
from utils import CacheManager, UserSettings

logger = logging.getLogger(__name__)

class AdvancedCommands:
    """Gestionnaire des commandes avancées"""
    
    def __init__(self):
        self.api_client = FootballAPIClient()
        self.cache = CacheManager(cache_dir="cache/advanced", default_ttl=300)
        self.user_settings = UserSettings(self.cache)
    
    async def get_league_standings(self, league_name: str = "Ligue 1") -> str:
        """Récupère le classement d'un championnat"""
        try:
            # Mapping des championnats populaires
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
            cache_key = f"standings_{league_code}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self._format_standings(cached_data, league_name)
            
            # Récupérer les données de l'API
            standings_data = self.api_client._make_request(f"competitions/{league_code}/standings")
            
            if not standings_data:
                return f"❌ Impossible de récupérer le classement de {league_name}"
            
            # Mettre en cache
            self.cache.set(cache_key, standings_data, ttl=1800)  # 30 minutes
            
            return self._format_standings(standings_data, league_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement: {e}")
            return f"❌ Erreur lors de la récupération du classement de {league_name}"
    
    def _format_standings(self, data: Dict, league_name: str) -> str:
        """Formate le classement pour l'affichage"""
        try:
            standings = data.get('standings', [])
            if not standings:
                return f"❌ Aucun classement disponible pour {league_name}"
            
            # Prendre le premier groupe (généralement le classement général)
            table = standings[0].get('table', [])
            
            result = f"🏆 CLASSEMENT {league_name.upper()} 🏆\n"
            result += f"╔═══════════════════════════════════════╗\n"
            result += f"║ Pos │ Équipe           │ Pts │ J │ V │ N │ D ║\n"
            result += f"╠═══════════════════════════════════════╣\n"
            
            for i, team in enumerate(table[:10]):  # Top 10
                position = team.get('position', i+1)
                team_name = team.get('team', {}).get('name', 'N/A')[:15]
                points = team.get('points', 0)
                played = team.get('playedGames', 0)
                won = team.get('won', 0)
                drawn = team.get('draw', 0)
                lost = team.get('lost', 0)
                
                # Emoji pour les positions spéciales
                pos_emoji = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else "🔸"
                
                result += f"║ {pos_emoji} {position:2d} │ {team_name:<15} │ {points:3d} │ {played:2d} │ {won:2d} │ {drawn:2d} │ {lost:2d} ║\n"
            
            result += f"╚═══════════════════════════════════════╝\n"
            result += f"📅 Mis à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du formatage du classement: {e}")
            return f"❌ Erreur lors du formatage du classement"
    
    async def get_team_stats(self, team_name: str) -> str:
        """Récupère les statistiques détaillées d'une équipe"""
        try:
            # Rechercher l'équipe
            team_data = self.api_client.search_team(team_name)
            if not team_data:
                return f"❌ Équipe '{team_name}' non trouvée"
            
            team_id = team_data['id']
            
            # Vérifier le cache
            cache_key = f"team_stats_{team_id}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self._format_team_stats(cached_data, team_data['name'])
            
            # Récupérer les statistiques
            stats_data = self.api_client._make_request(f"teams/{team_id}/matches", {
                'status': 'FINISHED',
                'limit': 10
            })
            
            if not stats_data:
                return f"❌ Aucune statistique disponible pour {team_name}"
            
            # Mettre en cache
            self.cache.set(cache_key, stats_data, ttl=1800)
            
            return self._format_team_stats(stats_data, team_data['name'])
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats d'équipe: {e}")
            return f"❌ Erreur lors de la récupération des statistiques de {team_name}"
    
    def _format_team_stats(self, data: Dict, team_name: str) -> str:
        """Formate les statistiques d'équipe"""
        try:
            matches = data.get('matches', [])
            
            # Calculer les statistiques
            total_matches = len(matches)
            wins = 0
            draws = 0
            losses = 0
            goals_for = 0
            goals_against = 0
            
            for match in matches:
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
            
            # Calculer les moyennes
            win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
            avg_goals_for = goals_for / total_matches if total_matches > 0 else 0
            avg_goals_against = goals_against / total_matches if total_matches > 0 else 0
            
            # Formatage
            result = f"📊 STATISTIQUES {team_name.upper()} 📊\n"
            result += f"╔═══════════════════════════════════════╗\n"
            result += f"║ 📈 PERFORMANCE GÉNÉRALE                ║\n"
            result += f"╠═══════════════════════════════════════╣\n"
            result += f"║ Matchs joués: {total_matches:2d}                    ║\n"
            result += f"║ Victoires: {wins:2d} ({win_rate:5.1f}%)           ║\n"
            result += f"║ Nuls: {draws:2d}                        ║\n"
            result += f"║ Défaites: {losses:2d}                      ║\n"
            result += f"╠═══════════════════════════════════════╣\n"
            result += f"║ ⚽ BUTS                                ║\n"
            result += f"╠═══════════════════════════════════════╣\n"
            result += f"║ Buts marqués: {goals_for:2d} ({avg_goals_for:4.1f}/match)      ║\n"
            result += f"║ Buts encaissés: {goals_against:2d} ({avg_goals_against:4.1f}/match)    ║\n"
            result += f"║ Différence: +{goals_for - goals_against:2d}                    ║\n"
            result += f"╚═══════════════════════════════════════╝\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du formatage des stats d'équipe: {e}")
            return f"❌ Erreur lors du formatage des statistiques"
    
    async def get_upcoming_matches(self, league_name: str = "Ligue 1", days: int = 7) -> str:
        """Récupère les prochains matchs d'un championnat"""
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
            cache_key = f"upcoming_{league_code}_{days}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self._format_upcoming_matches(cached_data, league_name)
            
            # Récupérer les matchs à venir
            from_date = datetime.now().strftime('%Y-%m-%d')
            to_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            matches_data = self.api_client._make_request(f"competitions/{league_code}/matches", {
                'dateFrom': from_date,
                'dateTo': to_date,
                'status': 'SCHEDULED'
            })
            
            if not matches_data:
                return f"❌ Aucun match à venir pour {league_name}"
            
            # Mettre en cache
            self.cache.set(cache_key, matches_data, ttl=1800)
            
            return self._format_upcoming_matches(matches_data, league_name)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs à venir: {e}")
            return f"❌ Erreur lors de la récupération des matchs à venir"
    
    def _format_upcoming_matches(self, data: Dict, league_name: str) -> str:
        """Formate les matchs à venir"""
        try:
            matches = data.get('matches', [])
            
            if not matches:
                return f"❌ Aucun match programmé pour {league_name}"
            
            result = f"📅 PROCHAINS MATCHS - {league_name.upper()} 📅\n"
            result += f"╔═══════════════════════════════════════╗\n"
            
            for match in matches[:10]:  # Limiter à 10 matchs
                home_team = match.get('homeTeam', {}).get('name', 'N/A')
                away_team = match.get('awayTeam', {}).get('name', 'N/A')
                match_date = match.get('utcDate', '')
                
                # Formater la date
                try:
                    dt = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%d/%m %H:%M')
                except:
                    formatted_date = "Date inconnue"
                
                result += f"║ {formatted_date} │ {home_team} vs {away_team} ║\n"
            
            result += f"╚═══════════════════════════════════════╝\n"
            result += f"📊 {len(matches)} match(s) programmé(s)\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du formatage des matchs à venir: {e}")
            return f"❌ Erreur lors du formatage des matchs à venir"
    
    async def compare_teams(self, team1_name: str, team2_name: str) -> str:
        """Compare deux équipes"""
        try:
            # Récupérer les données des deux équipes
            team1_data = self.api_client.search_team(team1_name)
            team2_data = self.api_client.search_team(team2_name)
            
            if not team1_data:
                return f"❌ Équipe '{team1_name}' non trouvée"
            if not team2_data:
                return f"❌ Équipe '{team2_name}' non trouvée"
            
            # Récupérer les statistiques
            team1_stats = await self.get_team_stats(team1_name)
            team2_stats = await self.get_team_stats(team2_name)
            
            # Formatage de la comparaison
            result = f"⚖️ COMPARAISON D'ÉQUIPES ⚖️\n"
            result += f"╔═══════════════════════════════════════╗\n"
            result += f"║ {team1_name} vs {team2_name} ║\n"
            result += f"╚═══════════════════════════════════════╝\n\n"
            
            result += f"🏠 {team1_name}\n"
            result += f"┌─────────────────────────────────────┐\n"
            result += f"│ {team1_stats.split('╔')[1].split('╚')[0] if '╔' in team1_stats else 'Stats non disponibles'} │\n"
            result += f"└─────────────────────────────────────┘\n\n"
            
            result += f"🚌 {team2_name}\n"
            result += f"┌─────────────────────────────────────┐\n"
            result += f"│ {team2_stats.split('╔')[1].split('╚')[0] if '╔' in team2_stats else 'Stats non disponibles'} │\n"
            result += f"└─────────────────────────────────────┘\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de la comparaison d'équipes: {e}")
            return f"❌ Erreur lors de la comparaison des équipes"
