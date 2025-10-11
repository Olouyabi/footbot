"""
Module de formatage professionnel pour le bot FootStat Analyzer
Améliore l'affichage des résultats avec un design moderne et professionnel
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

class ProfessionalFormatter:
    """Gestionnaire de formatage professionnel pour les résultats"""
    
    # Emojis et symboles pour un affichage moderne
    EMOJIS = {
        'trophy': '🏆',
        'medal_gold': '🥇',
        'medal_silver': '🥈', 
        'medal_bronze': '🥉',
        'soccer': '⚽',
        'chart': '📊',
        'calendar': '📅',
        'clock': '🕐',
        'fire': '🔥',
        'star': '⭐',
        'target': '🎯',
        'warning': '⚠️',
        'check': '✅',
        'cross': '❌',
        'arrow_up': '📈',
        'arrow_down': '📉',
        'home': '🏠',
        'away': '✈️',
        'vs': '⚔️',
        'goal': '🥅',
        'card_yellow': '🟨',
        'card_red': '🟥',
        'substitution': '🔄',
        'injury': '🏥',
        'money': '💰',
        'trending': '📈',
        'shield': '🛡️',
        'lightning': '⚡',
        'heart': '❤️',
        'brain': '🧠',
        'robot': '🤖',
        'crown': '👑',
        'diamond': '💎',
        'rocket': '🚀',
        'magic': '✨',
        'thunder': '⚡',
        'sun': '☀️',
        'moon': '🌙',
        'rainbow': '🌈',
        'newspaper': '📰',
        'bullet': '•'
    }
    
    # Couleurs et styles pour Telegram
    STYLES = {
        'header': '🔹',
        'section': '🔹',
        'subheader': '▫️',
        'bullet': '•',
        'dash': '─',
        'pipe': '│',
        'corner_tl': '┌',
        'corner_tr': '┐',
        'corner_bl': '└',
        'corner_br': '┘',
        'cross': '┼',
        'line_h': '─',
        'line_v': '│'
    }
    
    def __init__(self):
        self.max_width = 35  # Largeur maximale pour Telegram
        self.use_emojis = True
        self.use_boxes = True
    
    def format_match_analysis(self, analysis: Dict) -> str:
        """Formate une analyse de match de manière professionnelle"""
        try:
            match_name = analysis.get('match', 'Match inconnu')
            analysis_data = analysis.get('analysis', {})
            
            # En-tête principal
            header = self._create_header(f"ANALYSE DE MATCH", self.EMOJIS['target'])
            
            # Informations du match
            match_info = self._format_match_info(match_name, analysis_data)
            
            # Probabilités
            probabilities = self._format_probabilities(analysis_data.get('probabilities', {}))
            
            # Analyse détaillée
            detailed_analysis = self._format_detailed_analysis(analysis_data)
            
            # Recommandations
            recommendations = self._format_recommendations(analysis_data)
            
            # Pied de page
            footer = self._create_footer()
            
            # Assembler le tout
            result = f"{header}\n{match_info}\n{probabilities}\n{detailed_analysis}\n{recommendations}\n{footer}"
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur formatage analyse: {e}")
            return self._format_error("Erreur lors du formatage de l'analyse")
    
    def format_league_standings(self, data: Dict, league_name: str) -> str:
        """Formate le classement d'une ligue de manière professionnelle"""
        try:
            standings = data.get('standings', [])
            if not standings:
                return self._format_error(f"Aucun classement disponible pour {league_name}")
            
            table = standings[0].get('table', [])
            
            # En-tête avec emoji de la ligue
            league_emoji = self._get_league_emoji(league_name)
            header = self._create_header(f"CLASSEMENT {league_name.upper()}", league_emoji)
            
            # Tableau de classement stylisé
            standings_table = self._create_standings_table(table[:10])  # Top 10
            
            # Statistiques de la ligue
            league_stats = self._format_league_stats(table, league_name)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{standings_table}\n{league_stats}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage classement: {e}")
            return self._format_error("Erreur lors du formatage du classement")
    
    def format_team_stats(self, data: Dict, team_name: str) -> str:
        """Formate les statistiques d'équipe de manière professionnelle"""
        try:
            matches = data.get('matches', [])
            
            # En-tête
            header = self._create_header(f"STATISTIQUES {team_name.upper()}", self.EMOJIS['chart'])
            
            # Calculer les statistiques
            stats = self._calculate_team_stats(matches, team_name)
            
            # Affichage des performances
            performance = self._format_performance_stats(stats)
            
            # Forme récente
            recent_form = self._format_recent_form(matches, team_name)
            
            # Statistiques offensives/défensives
            offensive_defensive = self._format_offensive_defensive_stats(stats)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{performance}\n{recent_form}\n{offensive_defensive}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage stats équipe: {e}")
            return self._format_error("Erreur lors du formatage des statistiques")
    
    def format_upcoming_matches(self, data: Dict, league_name: str) -> str:
        """Formate les prochains matchs de manière professionnelle"""
        try:
            matches = data.get('matches', [])
            
            if not matches:
                return self._format_error(f"Aucun match programmé pour {league_name}")
            
            # En-tête
            header = self._create_header(f"PROCHAINS MATCHS - {league_name.upper()}", self.EMOJIS['calendar'])
            
            # Liste des matchs
            matches_list = self._format_matches_list(matches[:10])
            
            # Statistiques des matchs
            match_stats = self._format_match_statistics(matches)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{matches_list}\n{match_stats}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage matchs à venir: {e}")
            return self._format_error("Erreur lors du formatage des matchs à venir")
    
    def format_team_comparison(self, team1_data: Dict, team2_data: Dict, team1_name: str, team2_name: str) -> str:
        """Formate une comparaison d'équipes de manière professionnelle"""
        try:
            # En-tête
            header = self._create_header(f"COMPARAISON D'ÉQUIPES", self.EMOJIS['vs'])
            
            # Informations des équipes
            teams_info = self._format_teams_info(team1_name, team2_name)
            
            # Comparaison des statistiques
            comparison = self._format_statistics_comparison(team1_data, team2_data, team1_name, team2_name)
            
            # Analyse comparative
            analysis = self._format_comparative_analysis(team1_data, team2_data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{teams_info}\n{comparison}\n{analysis}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage comparaison: {e}")
            return self._format_error("Erreur lors du formatage de la comparaison")
    
    def format_main_menu(self, user_settings: Dict) -> str:
        """Formate le menu principal de manière professionnelle"""
        try:
            # En-tête avec emoji du bot
            header = self._create_header("FOOTSTAT ANALYZER v2.0", self.EMOJIS['robot'])
            
            # Informations utilisateur
            user_info = self._format_user_info(user_settings)
            
            # Menu des commandes
            commands_menu = self._format_commands_menu()
            
            # Statistiques du bot
            bot_stats = self._format_bot_stats()
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{user_info}\n{commands_menu}\n{bot_stats}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage menu: {e}")
            return self._format_error("Erreur lors du formatage du menu")
    
    def _create_header(self, title: str, emoji: str = None) -> str:
        """Crée un en-tête stylisé"""
        if not self.use_boxes:
            return f"{emoji} {title} {emoji}" if emoji else title
        
        emoji_text = f" {emoji} " if emoji else ""
        title_text = f"{emoji_text}{title}{emoji_text}"
        
        # Calculer la largeur nécessaire
        width = max(len(title_text) + 4, 25)
        
        # Créer l'en-tête avec des bordures
        top_border = self.STYLES['corner_tl'] + self.STYLES['line_h'] * (width - 2) + self.STYLES['corner_tr']
        title_line = self.STYLES['line_v'] + title_text.center(width - 2) + self.STYLES['line_v']
        bottom_border = self.STYLES['corner_bl'] + self.STYLES['line_h'] * (width - 2) + self.STYLES['corner_br']
        
        return f"{top_border}\n{title_line}\n{bottom_border}"
    
    def _create_footer(self) -> str:
        """Crée un pied de page avec timestamp"""
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        footer_text = f"📅 Mis à jour: {timestamp} | 🤖 FootStat Analyzer v2.0"
        
        if not self.use_boxes:
            return footer_text
        
        width = len(footer_text) + 4
        top_border = self.STYLES['corner_tl'] + self.STYLES['line_h'] * (width - 2) + self.STYLES['corner_tr']
        footer_line = self.STYLES['line_v'] + footer_text.center(width - 2) + self.STYLES['line_v']
        bottom_border = self.STYLES['corner_bl'] + self.STYLES['line_h'] * (width - 2) + self.STYLES['corner_br']
        
        return f"{top_border}\n{footer_line}\n{bottom_border}"
    
    def _format_match_info(self, match_name: str, analysis_data: Dict) -> str:
        """Formate les informations du match"""
        risk_level = analysis_data.get('risk_level', 'Moyen')
        risk_emoji = self._get_risk_emoji(risk_level)
        
        info = f"{self.STYLES['header']} **INFORMATIONS DU MATCH**\n"
        info += f"{self.STYLES['bullet']} Match: {match_name}\n"
        info += f"{self.STYLES['bullet']} Niveau de risque: {risk_emoji} {risk_level}\n"
        
        # Ajouter des informations supplémentaires si disponibles
        if 'match_date' in analysis_data:
            info += f"{self.STYLES['bullet']} Date: {analysis_data['match_date']}\n"
        
        if 'competition' in analysis_data:
            info += f"{self.STYLES['bullet']} Compétition: {analysis_data['competition']}\n"
        
        return info
    
    def _format_probabilities(self, probabilities: Dict) -> str:
        """Formate les probabilités de manière lisible"""
        if not probabilities:
            return ""
        
        prob_text = f"{self.STYLES['section']} **PROBABILITÉS**\n\n"
        
        # Probabilités de résultat
        if 'team1_win' in probabilities:
            team1_prob = probabilities['team1_win']
            draw_prob = probabilities.get('draw', 0)
            team2_prob = probabilities.get('team2_win', 0)
            
            prob_text += f"🏠 **Victoire domicile:** {self._get_risk_emoji(team1_prob)} {team1_prob}%\n"
            prob_text += f"⚔️ **Match nul:** {self._get_risk_emoji(draw_prob)} {draw_prob}%\n"
            prob_text += f"✈️ **Victoire extérieur:** {self._get_risk_emoji(team2_prob)} {team2_prob}%\n\n"
        
        # Probabilités de buts
        if 'over_2_5' in probabilities:
            over_prob = probabilities['over_2_5']
            under_prob = 100 - over_prob
            
            prob_text += f"{self.STYLES['subheader']} **PARIS SUR LES BUTS**\n"
            prob_text += f"⭐ **Plus de 2.5 buts:** {self._get_risk_emoji(over_prob)} {over_prob}%\n"
            prob_text += f"⚔️ **Moins de 2.5 buts:** {self._get_risk_emoji(under_prob)} {under_prob}%\n\n"
        
        return prob_text
    
    def _format_detailed_analysis(self, analysis_data: Dict) -> str:
        """Formate l'analyse détaillée"""
        analysis_text = f"{self.STYLES['header']} **ANALYSE DÉTAILLÉE**\n"
        
        # Forme récente
        if 'recent_form' in analysis_data:
            form = analysis_data['recent_form']
            analysis_text += f"{self.STYLES['bullet']} Forme récente: {self._format_recent_form_display(form)}\n"
        
        # Performances à domicile/extérieur
        if 'home_away_stats' in analysis_data:
            stats = analysis_data['home_away_stats']
            analysis_text += f"{self.STYLES['bullet']} Performance domicile: {stats.get('home_performance', 'N/A')}\n"
            analysis_text += f"{self.STYLES['bullet']} Performance extérieur: {stats.get('away_performance', 'N/A')}\n"
        
        # Facteurs clés
        if 'key_factors' in analysis_data:
            factors = analysis_data['key_factors']
            analysis_text += f"\n{self.STYLES['subheader']} **FACTEURS CLÉS**\n"
            for factor in factors[:3]:  # Limiter à 3 facteurs
                analysis_text += f"{self.STYLES['bullet']} {factor}\n"
        
        return analysis_text
    
    def _format_recommendations(self, analysis_data: Dict) -> str:
        """Formate les recommandations"""
        recommendations = analysis_data.get('recommendations', [])
        
        if not recommendations:
            return ""
        
        rec_text = f"{self.STYLES['header']} **RECOMMANDATIONS**\n"
        
        for i, rec in enumerate(recommendations[:3], 1):  # Limiter à 3 recommandations
            emoji = self.EMOJIS['star'] if i == 1 else self.EMOJIS['bullet']
            rec_text += f"{emoji} {rec}\n"
        
        return rec_text
    
    def _create_standings_table(self, table: List[Dict]) -> str:
        """Crée un tableau de classement optimisé pour Telegram"""
        if not table:
            return "❌ Aucune donnée de classement disponible"
        
        # Format simple et lisible pour Telegram
        standings_text = f"{self.STYLES['header']} **TOP 10**\n\n"
        
        for team in table[:10]:  # Limiter à 10 équipes
            position = team.get('position', 0)
            team_name = team.get('team', {}).get('shortName', team.get('team', {}).get('name', 'N/A'))
            points = team.get('points', 0)
            played = team.get('playedGames', 0)
            won = team.get('won', 0)
            drawn = team.get('draw', 0)
            lost = team.get('lost', 0)
            
            # Emoji pour les positions spéciales
            pos_emoji = self._get_position_emoji(position)
            
            # Format compact et lisible
            standings_text += f"{pos_emoji} **{position}.** {team_name}\n"
            standings_text += f"   📊 {points} pts | {played}J | {won}V-{drawn}N-{lost}D\n\n"
        
        return standings_text
    
    def _format_league_stats(self, table: List[Dict], league_name: str) -> str:
        """Formate les statistiques de la ligue"""
        if not table:
            return ""
        
        total_teams = len(table)
        total_matches = sum(team.get('playedGames', 0) for team in table) // 2  # Diviser par 2 car chaque match compte pour 2 équipes
        
        stats_text = f"{self.STYLES['header']} **STATISTIQUES DE LA LIGUE**\n"
        stats_text += f"{self.STYLES['bullet']} Nombre d'équipes: {total_teams}\n"
        stats_text += f"{self.STYLES['bullet']} Matchs joués: {total_matches}\n"
        
        # Équipe en tête
        if table:
            leader = table[0]
            leader_name = leader.get('team', {}).get('name', 'N/A')
            leader_points = leader.get('points', 0)
            stats_text += f"{self.STYLES['bullet']} Leader: {leader_name} ({leader_points} pts)\n"
        
        return stats_text
    
    def _calculate_team_stats(self, matches: List[Dict], team_name: str) -> Dict:
        """Calcule les statistiques d'une équipe"""
        stats = {
            'total_matches': len(matches),
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for': 0,
            'goals_against': 0,
            'recent_form': [],
            'home_wins': 0,
            'away_wins': 0
        }
        
        for match in matches:
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            score = match.get('score', {}).get('fullTime', {})
            
            home_goals = score.get('home', 0)
            away_goals = score.get('away', 0)
            
            if home_team == team_name:
                # Match à domicile
                stats['goals_for'] += home_goals
                stats['goals_against'] += away_goals
                
                if home_goals > away_goals:
                    stats['wins'] += 1
                    stats['home_wins'] += 1
                    stats['recent_form'].append('W')
                elif home_goals == away_goals:
                    stats['draws'] += 1
                    stats['recent_form'].append('D')
                else:
                    stats['losses'] += 1
                    stats['recent_form'].append('L')
            else:
                # Match à l'extérieur
                stats['goals_for'] += away_goals
                stats['goals_against'] += home_goals
                
                if away_goals > home_goals:
                    stats['wins'] += 1
                    stats['away_wins'] += 1
                    stats['recent_form'].append('W')
                elif away_goals == home_goals:
                    stats['draws'] += 1
                    stats['recent_form'].append('D')
                else:
                    stats['losses'] += 1
                    stats['recent_form'].append('L')
        
        # Calculer les moyennes
        if stats['total_matches'] > 0:
            stats['win_rate'] = (stats['wins'] / stats['total_matches']) * 100
            stats['avg_goals_for'] = stats['goals_for'] / stats['total_matches']
            stats['avg_goals_against'] = stats['goals_against'] / stats['total_matches']
        else:
            stats['win_rate'] = 0
            stats['avg_goals_for'] = 0
            stats['avg_goals_against'] = 0
        
        return stats
    
    def _format_performance_stats(self, stats: Dict) -> str:
        """Formate les statistiques de performance de manière lisible"""
        perf_text = f"{self.STYLES['section']} **PERFORMANCES GÉNÉRALES**\n\n"
        
        # Statistiques principales en format compact
        total_matches = stats.get('total_matches', 0)
        wins = stats.get('wins', 0)
        draws = stats.get('draws', 0)
        losses = stats.get('losses', 0)
        points = stats.get('points', 0)
        
        win_rate = stats.get('win_rate', 0)
        draw_rate = stats.get('draw_rate', 0)
        loss_rate = stats.get('loss_rate', 0)
        
        perf_text += f"📊 **Matchs:** {total_matches} | **Points:** {points}\n\n"
        perf_text += f"✅ **Victoires:** {wins} ({win_rate:.1f}%)\n"
        perf_text += f"⚔️ **Nuls:** {draws} ({draw_rate:.1f}%)\n"
        perf_text += f"❌ **Défaites:** {losses} ({loss_rate:.1f}%)\n\n"
        
        # Statistiques de buts
        goals_for = stats.get('goals_for', 0)
        goals_against = stats.get('goals_against', 0)
        avg_goals_for = stats.get('avg_goals_for', 0)
        avg_goals_against = stats.get('avg_goals_against', 0)
        goal_diff = goals_for - goals_against
        
        perf_text += f"🥅 **Buts marqués:** {goals_for} ({avg_goals_for:.1f}/match)\n"
        perf_text += f"🛡️ **Buts encaissés:** {goals_against} ({avg_goals_against:.1f}/match)\n"
        diff_emoji = "📈" if goal_diff > 0 else "📉" if goal_diff < 0 else "⚖️"
        perf_text += f"{diff_emoji} **Différence:** {goal_diff:+d}\n\n"
        
        # Forme récente
        form_score = stats.get('form_score', 0)
        perf_text += f"📈 **Forme actuelle:** {self._get_form_emoji(form_score)} {form_score:.1f}/10\n"
        
        return perf_text
    
    def _format_recent_form(self, matches: List[Dict], team_name: str) -> str:
        """Formate la forme récente"""
        if not matches:
            return ""
        
        # Prendre les 5 derniers matchs
        recent_matches = matches[-5:]
        form_chars = []
        
        for match in recent_matches:
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            score = match.get('score', {}).get('fullTime', {})
            
            home_goals = score.get('home', 0)
            away_goals = score.get('away', 0)
            
            if home_team == team_name:
                if home_goals > away_goals:
                    form_chars.append('W')
                elif home_goals == away_goals:
                    form_chars.append('D')
                else:
                    form_chars.append('L')
            else:
                if away_goals > home_goals:
                    form_chars.append('W')
                elif away_goals == home_goals:
                    form_chars.append('D')
                else:
                    form_chars.append('L')
        
        form_text = f"{self.STYLES['header']} **FORME RÉCENTE**\n"
        form_text += f"{self.STYLES['bullet']} 5 derniers matchs: {self._format_recent_form_display(form_chars)}\n"
        
        return form_text
    
    def _format_recent_form_display(self, form_chars: List[str]) -> str:
        """Formate l'affichage de la forme récente avec des emojis"""
        form_display = ""
        for char in form_chars:
            if char == 'W':
                form_display += f"{self.EMOJIS['check']} "
            elif char == 'D':
                form_display += f"{self.EMOJIS['vs']} "
            else:  # L
                form_display += f"{self.EMOJIS['cross']} "
        
        return form_display.strip()
    
    def _format_offensive_defensive_stats(self, stats: Dict) -> str:
        """Formate les statistiques offensives et défensives"""
        off_def_text = f"{self.STYLES['header']} **ANALYSE OFFENSIVE/DÉFENSIVE**\n"
        
        # Performance offensive
        offensive_rating = min(100, (stats['avg_goals_for'] / 3) * 100)  # Normaliser sur 3 buts
        off_def_text += f"{self.STYLES['bullet']} Attaque: {self._create_progress_bar(offensive_rating)} {offensive_rating:.0f}%\n"
        
        # Performance défensive
        defensive_rating = max(0, 100 - (stats['avg_goals_against'] / 2) * 100)  # Normaliser sur 2 buts
        off_def_text += f"{self.STYLES['bullet']} Défense: {self._create_progress_bar(defensive_rating)} {defensive_rating:.0f}%\n"
        
        # Performance à domicile vs extérieur
        home_performance = (stats['home_wins'] / max(1, stats['total_matches'] // 2)) * 100
        away_performance = ((stats['wins'] - stats['home_wins']) / max(1, stats['total_matches'] // 2)) * 100
        
        off_def_text += f"\n{self.STYLES['subheader']} **DOMICILE vs EXTÉRIEUR**\n"
        off_def_text += f"{self.STYLES['bullet']} {self.EMOJIS['home']} Domicile: {self._create_progress_bar(home_performance)} {home_performance:.0f}%\n"
        off_def_text += f"{self.STYLES['bullet']} {self.EMOJIS['away']} Extérieur: {self._create_progress_bar(away_performance)} {away_performance:.0f}%\n"
        
        return off_def_text
    
    def _format_matches_list(self, matches: List[Dict]) -> str:
        """Formate la liste des matchs à venir"""
        if not matches:
            return ""
        
        matches_text = f"{self.STYLES['header']} **PROCHAINS MATCHS**\n"
        
        for i, match in enumerate(matches, 1):
            home_team = match.get('homeTeam', {}).get('name', 'N/A')
            away_team = match.get('awayTeam', {}).get('name', 'N/A')
            match_date = match.get('utcDate', '')
            
            # Formater la date
            try:
                dt = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%d/%m %H:%M')
            except:
                formatted_date = "Date inconnue"
            
            # Emoji pour le numéro du match
            match_emoji = f"{i}️⃣" if i <= 10 else f"{i}."
            
            matches_text += f"{match_emoji} {formatted_date} │ {home_team} {self.EMOJIS['vs']} {away_team}\n"
        
        return matches_text
    
    def _format_match_statistics(self, matches: List[Dict]) -> str:
        """Formate les statistiques des matchs"""
        if not matches:
            return ""
        
        total_matches = len(matches)
        
        # Grouper par jour
        matches_by_day = {}
        for match in matches:
            try:
                dt = datetime.fromisoformat(match.get('utcDate', '').replace('Z', '+00:00'))
                day = dt.strftime('%A %d/%m')
                if day not in matches_by_day:
                    matches_by_day[day] = 0
                matches_by_day[day] += 1
            except:
                pass
        
        stats_text = f"{self.STYLES['header']} **STATISTIQUES**\n"
        stats_text += f"{self.STYLES['bullet']} Total de matchs: {total_matches}\n"
        stats_text += f"{self.STYLES['bullet']} Jours avec matchs: {len(matches_by_day)}\n"
        
        if matches_by_day:
            most_matches_day = max(matches_by_day.items(), key=lambda x: x[1])
            stats_text += f"{self.STYLES['bullet']} Jour le plus chargé: {most_matches_day[0]} ({most_matches_day[1]} matchs)\n"
        
        return stats_text
    
    def _format_teams_info(self, team1_name: str, team2_name: str) -> str:
        """Formate les informations des équipes"""
        info_text = f"{self.STYLES['header']} **ÉQUIPES EN COMPARISON**\n"
        info_text += f"┌─────────────────────────────────────┐\n"
        info_text += f"│ {self.EMOJIS['home']} {team1_name:<30} │\n"
        info_text += f"│ {self.EMOJIS['vs']} VS                                │\n"
        info_text += f"│ {self.EMOJIS['away']} {team2_name:<30} │\n"
        info_text += f"└─────────────────────────────────────┘\n"
        
        return info_text
    
    def _format_statistics_comparison(self, team1_data: Dict, team2_data: Dict, team1_name: str, team2_name: str) -> str:
        """Formate la comparaison des statistiques"""
        # Cette fonction serait implémentée avec les vraies données des équipes
        comp_text = f"{self.STYLES['header']} **COMPARAISON DES STATISTIQUES**\n"
        comp_text += f"{self.STYLES['bullet']} Comparaison détaillée des performances...\n"
        
        return comp_text
    
    def _format_comparative_analysis(self, team1_data: Dict, team2_data: Dict) -> str:
        """Formate l'analyse comparative"""
        analysis_text = f"{self.STYLES['header']} **ANALYSE COMPARATIVE**\n"
        analysis_text += f"{self.STYLES['bullet']} Analyse des forces et faiblesses...\n"
        
        return analysis_text
    
    def _format_user_info(self, user_settings: Dict) -> str:
        """Formate les informations utilisateur"""
        info_text = f"{self.STYLES['header']} **VOS PARAMÈTRES**\n"
        info_text += f"{self.STYLES['bullet']} Ligue préférée: {user_settings.get('league', 'PL')}\n"
        info_text += f"{self.STYLES['bullet']} Mode IA: {'Activé' if user_settings.get('ai_mode', False) else 'Désactivé'}\n"
        info_text += f"{self.STYLES['bullet']} Langue: {user_settings.get('language', 'fr')}\n"
        
        return info_text
    
    def _format_commands_menu(self) -> str:
        """Formate le menu des commandes"""
        menu_text = f"{self.STYLES['header']} **COMMANDES DISPONIBLES**\n"
        
        commands = [
            ("/analyze", "Analyser des matchs", self.EMOJIS['target']),
            ("/standings", "Classement d'une ligue", self.EMOJIS['trophy']),
            ("/teamstats", "Stats d'une équipe", self.EMOJIS['chart']),
            ("/upcoming", "Prochains matchs", self.EMOJIS['calendar']),
            ("/compare", "Comparer deux équipes", self.EMOJIS['vs']),
            ("/footchat", "Chat avec l'IA", "💬"),
            ("/settings", "Paramètres", self.EMOJIS['robot']),
            ("/help", "Aide complète", self.EMOJIS['brain'])
        ]
        
        for cmd, desc, emoji in commands:
            menu_text += f"{emoji} `{cmd}` - {desc}\n"
        
        return menu_text
    
    def _format_bot_stats(self) -> str:
        """Formate les statistiques du bot"""
        stats_text = f"{self.STYLES['header']} **STATISTIQUES DU BOT**\n"
        stats_text += f"{self.STYLES['bullet']} Version: 2.0\n"
        stats_text += f"{self.STYLES['bullet']} Statut: {self.EMOJIS['check']} Opérationnel\n"
        stats_text += f"{self.STYLES['bullet']} Mode IA: {self.EMOJIS['robot']} Disponible\n"
        
        return stats_text
    
    def _create_progress_bar(self, percentage: float, width: int = 10) -> str:
        """Crée une barre de progression visuelle"""
        filled = int((percentage / 100) * width)
        empty = width - filled
        
        # Choisir l'emoji selon le pourcentage
        if percentage >= 80:
            emoji = self.EMOJIS['fire']
        elif percentage >= 60:
            emoji = self.EMOJIS['star']
        elif percentage >= 40:
            emoji = self.EMOJIS['vs']
        else:
            emoji = self.EMOJIS['warning']
        
        bar = "█" * filled + "░" * empty
        return f"{emoji} {bar}"
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """Retourne l'emoji correspondant au niveau de risque"""
        risk_emojis = {
            'Faible': self.EMOJIS['check'],
            'Moyen': self.EMOJIS['warning'],
            'Élevé': self.EMOJIS['cross'],
            'Très élevé': self.EMOJIS['thunder']
        }
        return risk_emojis.get(risk_level, self.EMOJIS['vs'])
    
    def _get_form_emoji(self, score: float) -> str:
        """Retourne un emoji basé sur le score de forme"""
        if score >= 8:
            return self.EMOJIS['fire']
        elif score >= 6:
            return self.EMOJIS['star']
        elif score >= 4:
            return self.EMOJIS['vs']
        else:
            return self.EMOJIS['warning']
    
    def _get_league_emoji(self, league_name: str) -> str:
        """Retourne l'emoji correspondant à la ligue"""
        league_emojis = {
            'Ligue 1': self.EMOJIS['trophy'],
            'Premier League': self.EMOJIS['crown'],
            'La Liga': self.EMOJIS['sun'],
            'Bundesliga': self.EMOJIS['lightning'],
            'Serie A': self.EMOJIS['diamond'],
            'Champions League': self.EMOJIS['rocket'],
            'Europa League': self.EMOJIS['star']
        }
        return league_emojis.get(league_name, self.EMOJIS['trophy'])
    
    def _get_position_emoji(self, position: int) -> str:
        """Retourne l'emoji correspondant à la position"""
        if position == 1:
            return self.EMOJIS['medal_gold']
        elif position == 2:
            return self.EMOJIS['medal_silver']
        elif position == 3:
            return self.EMOJIS['medal_bronze']
        elif position <= 4:
            return self.EMOJIS['trophy']
        else:
            return " "
    
    def format_live_scores(self, data: Dict, league_name: str) -> str:
        """Formate les scores en direct"""
        try:
            matches = data.get('matches', [])
            
            if not matches:
                return self._format_error(f"Aucun match en cours pour {league_name}")
            
            # En-tête
            header = self._create_header(f"SCORES EN DIRECT - {league_name.upper()}", self.EMOJIS['lightning'])
            
            # Liste des matchs en cours
            live_matches = self._format_live_matches_list(matches)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{live_matches}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage scores en direct: {e}")
            return self._format_error("Erreur lors du formatage des scores en direct")
    
    def format_player_stats(self, data: Dict, player_name: str) -> str:
        """Formate les statistiques d'un joueur"""
        try:
            # En-tête
            header = self._create_header(f"STATISTIQUES - {player_name.upper()}", self.EMOJIS['star'])
            
            # Informations du joueur
            player_info = self._format_player_info(data, player_name)
            
            # Statistiques de performance
            performance = self._format_player_performance(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{player_info}\n{performance}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage stats joueur: {e}")
            return self._format_error("Erreur lors du formatage des statistiques du joueur")
    
    def format_transfer_news(self, data: Dict, team_name: str = None) -> str:
        """Formate les nouvelles de transferts"""
        try:
            transfers = data.get('transfers', [])
            
            if not transfers:
                return self._format_error("Aucune nouvelle de transfert disponible")
            
            # En-tête
            title = f"TRANSFERTS - {team_name.upper()}" if team_name else "DERNIERS TRANSFERTS"
            header = self._create_header(title, self.EMOJIS['money'])
            
            # Liste des transferts
            transfers_list = self._format_transfers_list(transfers)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{transfers_list}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage transferts: {e}")
            return self._format_error("Erreur lors du formatage des transferts")
    
    def format_injury_report(self, data: Dict, team_name: str) -> str:
        """Formate le rapport de blessures"""
        try:
            injuries = data.get('injuries', [])
            
            if not injuries:
                return f"✅ Aucune blessure signalée pour {team_name}"
            
            # En-tête
            header = self._create_header(f"RAPPORT DE BLESSURES - {team_name.upper()}", self.EMOJIS['injury'])
            
            # Liste des blessures
            injuries_list = self._format_injuries_list(injuries)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{injuries_list}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage blessures: {e}")
            return self._format_error("Erreur lors du formatage du rapport de blessures")
    
    def format_league_news(self, data: Dict, league_name: str) -> str:
        """Formate les nouvelles de ligue"""
        try:
            news = data.get('news', [])
            
            if not news:
                return self._format_error(f"Aucune nouvelle disponible pour {league_name}")
            
            # En-tête
            header = self._create_header(f"ACTUALITÉS - {league_name.upper()}", self.EMOJIS['trending'])
            
            # Liste des nouvelles
            news_list = self._format_news_list(news)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{news_list}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage nouvelles: {e}")
            return self._format_error("Erreur lors du formatage des nouvelles")
    
    def format_weather_impact(self, data: Dict, match_info: Dict) -> str:
        """Formate l'impact météo sur un match"""
        try:
            # En-tête
            header = self._create_header("IMPACT MÉTÉO", self.EMOJIS['sun'])
            
            # Conditions météo
            weather_conditions = self._format_weather_conditions(data)
            
            # Impact sur le match
            impact_analysis = self._format_weather_impact_analysis(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{weather_conditions}\n{impact_analysis}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage météo: {e}")
            return self._format_error("Erreur lors du formatage de l'impact météo")
    
    def format_betting_odds(self, data: Dict, match_info: Dict) -> str:
        """Formate les cotes de paris"""
        try:
            # En-tête
            header = self._create_header("COTES DE PARIS", self.EMOJIS['money'])
            
            # Cotes principales
            main_odds = self._format_main_odds(data)
            
            # Cotes spéciales
            special_odds = self._format_special_odds(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{main_odds}\n{special_odds}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage cotes: {e}")
            return self._format_error("Erreur lors du formatage des cotes")
    
    def format_team_form_analysis(self, data: Dict, team_name: str, period: str) -> str:
        """Formate l'analyse de forme d'une équipe"""
        try:
            # En-tête
            period_text = "5 derniers matchs" if period == "last_5" else "10 derniers matchs"
            header = self._create_header(f"FORME - {team_name.upper()}", self.EMOJIS['trending'])
            
            # Résumé de la forme
            form_summary = self._format_form_summary(data, period_text)
            
            # Détails de la forme
            form_details = self._format_form_details(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{form_summary}\n{form_details}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage forme: {e}")
            return self._format_error("Erreur lors du formatage de l'analyse de forme")
    
    def format_head_to_head(self, data: Dict, team1_name: str, team2_name: str) -> str:
        """Formate l'historique des confrontations"""
        try:
            if "error" in data:
                return self._format_error(data["error"])
            
            # En-tête
            header = self._create_header(f"CONFRONTATIONS DIRECTES", self.EMOJIS['vs'])
            
            # Résumé H2H
            h2h_summary = self._format_h2h_summary(data, team1_name, team2_name)
            
            # Statistiques détaillées
            h2h_stats = self._format_h2h_statistics(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{h2h_summary}\n{h2h_stats}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage H2H: {e}")
            return self._format_error("Erreur lors du formatage de l'historique des confrontations")
    
    def format_league_statistics(self, data: Dict, league_name: str) -> str:
        """Formate les statistiques de ligue"""
        try:
            if "error" in data:
                return self._format_error(data["error"])
            
            # En-tête
            header = self._create_header(f"STATISTIQUES - {league_name.upper()}", self.EMOJIS['chart'])
            
            # Statistiques générales
            general_stats = self._format_general_league_stats(data)
            
            # Records de la ligue
            league_records = self._format_league_records(data)
            
            # Pied de page
            footer = self._create_footer()
            
            return f"{header}\n{general_stats}\n{league_records}\n{footer}"
            
        except Exception as e:
            logger.error(f"Erreur formatage stats ligue: {e}")
            return self._format_error("Erreur lors du formatage des statistiques de ligue")
    
    def _format_live_matches_list(self, matches: List[Dict]) -> str:
        """Formate la liste des matchs en direct"""
        matches_text = f"{self.STYLES['header']} **MATCHS EN COURS**\n"
        
        for match in matches:
            home_team = match.get('homeTeam', {}).get('name', 'N/A')
            away_team = match.get('awayTeam', {}).get('name', 'N/A')
            score = match.get('score', {}).get('fullTime', {})
            
            home_goals = score.get('home', 0)
            away_goals = score.get('away', 0)
            
            # Emoji pour le statut
            status_emoji = self.EMOJIS['lightning']
            
            matches_text += f"{status_emoji} {home_team} {home_goals}-{away_goals} {away_team}\n"
        
        return matches_text
    
    def _format_player_info(self, data: Dict, player_name: str) -> str:
        """Formate les informations d'un joueur"""
        info_text = f"{self.STYLES['section']} **INFORMATIONS DU JOUEUR**\n\n"
        
        # Utiliser le nom complet du joueur si disponible
        full_name = data.get('name', player_name)
        position = data.get('position', 'N/A')
        age = data.get('age', 'N/A')
        nationality = data.get('nationality', 'N/A')
        team = data.get('team', 'N/A')
        
        info_text += f"👤 **Nom:** {full_name}\n"
        info_text += f"⚽ **Position:** {position}\n"
        info_text += f"🏢 **Équipe:** {team}\n"
        info_text += f"🎂 **Âge:** {age} ans\n"
        info_text += f"🌍 **Nationalité:** {nationality}\n\n"
        
        return info_text
    
    def _format_player_performance(self, data: Dict) -> str:
        """Formate les performances d'un joueur"""
        stats = data.get('stats', {})
        
        perf_text = f"{self.STYLES['section']} **PERFORMANCES**\n\n"
        
        # Statistiques principales
        goals = stats.get('goals', 0)
        assists = stats.get('assists', 0)
        matches_played = stats.get('matches_played', 0)
        minutes_played = stats.get('minutes_played', 0)
        rating = stats.get('rating', 0)
        form = stats.get('form', 'N/A')
        
        perf_text += f"🥅 **Buts:** {goals}\n"
        perf_text += f"⭐ **Passes décisives:** {assists}\n"
        perf_text += f"📊 **Matchs joués:** {matches_played}\n"
        perf_text += f"⏱️ **Minutes jouées:** {minutes_played}\n\n"
        
        # Statistiques par match
        goals_per_match = stats.get('goals_per_match', 0)
        assists_per_match = stats.get('assists_per_match', 0)
        
        perf_text += f"📈 **Moyennes par match:**\n"
        perf_text += f"• Buts: {goals_per_match:.2f}/match\n"
        perf_text += f"• Passes décisives: {assists_per_match:.2f}/match\n\n"
        
        # Note et forme
        perf_text += f"⭐ **Note générale:** {rating}/10\n"
        perf_text += f"📈 **Forme actuelle:** {form}\n"
        
        return perf_text
    
    def _format_transfers_list(self, transfers: List[Dict]) -> str:
        """Formate la liste des transferts"""
        transfers_text = f"{self.STYLES['header']} **DERNIERS TRANSFERTS**\n"
        
        for transfer in transfers:
            player = transfer.get('player', 'N/A')
            from_team = transfer.get('from_team', 'N/A')
            to_team = transfer.get('to_team', 'N/A')
            fee = transfer.get('fee', 'N/A')
            status = transfer.get('status', 'N/A')
            
            status_emoji = self.EMOJIS['check'] if status == 'Confirmé' else self.EMOJIS['warning']
            
            transfers_text += f"{status_emoji} **{player}**\n"
            transfers_text += f"   {from_team} → {to_team}\n"
            transfers_text += f"   💰 {fee} | 📅 {transfer.get('date', 'N/A')}\n\n"
        
        return transfers_text
    
    def _format_injuries_list(self, injuries: List[Dict]) -> str:
        """Formate la liste des blessures"""
        injuries_text = f"{self.STYLES['header']} **BLESSURES ACTUELLES**\n"
        
        for injury in injuries:
            player = injury.get('player', 'N/A')
            injury_type = injury.get('injury', 'N/A')
            severity = injury.get('severity', 'N/A')
            return_date = injury.get('expected_return', 'N/A')
            
            severity_emoji = self._get_injury_severity_emoji(severity)
            
            injuries_text += f"{severity_emoji} **{player}**\n"
            injuries_text += f"   🏥 {injury_type}\n"
            injuries_text += f"   ⏰ Retour prévu: {return_date}\n\n"
        
        return injuries_text
    
    def _format_news_list(self, news: List[Dict]) -> str:
        """Formate la liste des nouvelles"""
        news_text = f"{self.STYLES['header']} **DERNIÈRES ACTUALITÉS**\n"
        
        for article in news:
            title = article.get('title', 'N/A')
            summary = article.get('summary', 'N/A')
            date = article.get('date', 'N/A')
            category = article.get('category', 'N/A')
            
            category_emoji = self._get_news_category_emoji(category)
            
            news_text += f"{category_emoji} **{title}**\n"
            news_text += f"   📝 {summary}\n"
            news_text += f"   📅 {date}\n\n"
        
        return news_text
    
    def _format_weather_conditions(self, data: Dict) -> str:
        """Formate les conditions météo"""
        weather_text = f"{self.STYLES['header']} **CONDITIONS MÉTÉO**\n"
        weather_text += f"┌─────────────────────────────────────┐\n"
        weather_text += f"│ 🌡️ Température: {data.get('temperature', 'N/A'):<20} │\n"
        weather_text += f"│ ☁️ Conditions: {data.get('conditions', 'N/A'):<20} │\n"
        weather_text += f"│ 💧 Humidité: {data.get('humidity', 'N/A'):<22} │\n"
        weather_text += f"│ 💨 Vent: {data.get('wind', 'N/A'):<25} │\n"
        weather_text += f"└─────────────────────────────────────┘\n"
        
        return weather_text
    
    def _format_weather_impact_analysis(self, data: Dict) -> str:
        """Formate l'analyse de l'impact météo"""
        impact_text = f"{self.STYLES['header']} **IMPACT SUR LE MATCH**\n"
        impact_text += f"{self.STYLES['bullet']} {data.get('impact', 'Impact non évalué')}\n"
        
        return impact_text
    
    def _format_main_odds(self, data: Dict) -> str:
        """Formate les cotes principales"""
        odds_text = f"{self.STYLES['header']} **COTES PRINCIPALES**\n"
        odds_text += f"┌─────────────────────────────────────┐\n"
        odds_text += f"│ 🏠 Victoire domicile: {data.get('home_win', 0):<15} │\n"
        odds_text += f"│ ⚖️ Match nul: {data.get('draw', 0):<20} │\n"
        odds_text += f"│ ✈️ Victoire extérieur: {data.get('away_win', 0):<12} │\n"
        odds_text += f"└─────────────────────────────────────┘\n"
        
        return odds_text
    
    def _format_special_odds(self, data: Dict) -> str:
        """Formate les cotes spéciales"""
        special_text = f"{self.STYLES['header']} **COTES SPÉCIALES**\n"
        special_text += f"┌─────────────────────────────────────┐\n"
        special_text += f"│ ⚽ Plus de 2.5 buts: {data.get('over_2_5', 0):<15} │\n"
        special_text += f"│ 🥅 Moins de 2.5 buts: {data.get('under_2_5', 0):<14} │\n"
        special_text += f"│ 🎯 Les deux marquent: {data.get('both_teams_score', 0):<12} │\n"
        special_text += f"└─────────────────────────────────────┘\n"
        
        return special_text
    
    def _format_form_summary(self, data: Dict, period_text: str) -> str:
        """Formate le résumé de forme"""
        summary_text = f"{self.STYLES['header']} **RÉSUMÉ DE FORME ({period_text})**\n"
        
        wins = data.get('wins', 0)
        draws = data.get('draws', 0)
        losses = data.get('losses', 0)
        form_rating = data.get('form_rating', 'N/A')
        
        summary_text += f"┌─────────────────────────────────────┐\n"
        summary_text += f"│ {self.EMOJIS['check']} Victoires: {wins:<25} │\n"
        summary_text += f"│ {self.EMOJIS['vs']} Nuls: {draws:<28} │\n"
        summary_text += f"│ {self.EMOJIS['cross']} Défaites: {losses:<24} │\n"
        summary_text += f"│ {self.EMOJIS['star']} Note: {form_rating:<26} │\n"
        summary_text += f"└─────────────────────────────────────┘\n"
        
        return summary_text
    
    def _format_form_details(self, data: Dict) -> str:
        """Formate les détails de forme"""
        details_text = f"{self.STYLES['header']} **DÉTAILS**\n"
        
        goals_for = data.get('goals_for', 0)
        goals_against = data.get('goals_against', 0)
        matches_analyzed = data.get('matches_analyzed', 0)
        
        details_text += f"{self.STYLES['bullet']} Buts marqués: {goals_for}\n"
        details_text += f"{self.STYLES['bullet']} Buts encaissés: {goals_against}\n"
        details_text += f"{self.STYLES['bullet']} Matchs analysés: {matches_analyzed}\n"
        
        return details_text
    
    def _format_h2h_summary(self, data: Dict, team1_name: str, team2_name: str) -> str:
        """Formate le résumé H2H"""
        summary_text = f"{self.STYLES['header']} **RÉSUMÉ DES CONFRONTATIONS**\n"
        
        team1_wins = data.get('team1_wins', 0)
        team2_wins = data.get('team2_wins', 0)
        draws = data.get('draws', 0)
        total_matches = data.get('total_matches', 0)
        
        summary_text += f"┌─────────────────────────────────────┐\n"
        summary_text += f"│ {self.EMOJIS['home']} {team1_name}: {team1_wins} victoires{' ' * (15 - len(team1_name))} │\n"
        summary_text += f"│ {self.EMOJIS['vs']} Nuls: {draws}{' ' * 25} │\n"
        summary_text += f"│ {self.EMOJIS['away']} {team2_name}: {team2_wins} victoires{' ' * (15 - len(team2_name))} │\n"
        summary_text += f"│ 📊 Total: {total_matches} matchs{' ' * 18} │\n"
        summary_text += f"└─────────────────────────────────────┘\n"
        
        return summary_text
    
    def _format_h2h_statistics(self, data: Dict) -> str:
        """Formate les statistiques H2H"""
        stats_text = f"{self.STYLES['header']} **STATISTIQUES**\n"
        
        team1_goals = data.get('team1_goals', 0)
        team2_goals = data.get('team2_goals', 0)
        team1_name = data.get('team1_name', 'Équipe 1')
        team2_name = data.get('team2_name', 'Équipe 2')
        
        stats_text += f"{self.STYLES['bullet']} {team1_name}: {team1_goals} buts\n"
        stats_text += f"{self.STYLES['bullet']} {team2_name}: {team2_goals} buts\n"
        
        return stats_text
    
    def _format_general_league_stats(self, data: Dict) -> str:
        """Formate les statistiques générales de ligue"""
        stats_text = f"{self.STYLES['header']} **STATISTIQUES GÉNÉRALES**\n"
        
        total_teams = data.get('total_teams', 0)
        total_matches = data.get('total_matches', 0)
        total_goals = data.get('total_goals', 0)
        avg_goals_per_match = data.get('avg_goals_per_match', 0)
        
        stats_text += f"┌─────────────────────────────────────┐\n"
        stats_text += f"│ {self.EMOJIS['trophy']} Équipes: {total_teams:<26} │\n"
        stats_text += f"│ {self.EMOJIS['calendar']} Matchs: {total_matches:<27} │\n"
        stats_text += f"│ {self.EMOJIS['goal']} Buts: {total_goals:<29} │\n"
        stats_text += f"│ {self.EMOJIS['chart']} Moyenne/match: {avg_goals_per_match:.1f}{' ' * 15} │\n"
        stats_text += f"└─────────────────────────────────────┘\n"
        
        return stats_text
    
    def _format_league_records(self, data: Dict) -> str:
        """Formate les records de la ligue"""
        records_text = f"{self.STYLES['header']} **RECORDS DE LA LIGUE**\n"
        
        most_goals_team = data.get('most_goals_team')
        least_goals_conceded = data.get('least_goals_conceded')
        
        if most_goals_team:
            team_name = most_goals_team.get('team', {}).get('name', 'N/A')
            goals = most_goals_team.get('goalsFor', 0)
            records_text += f"{self.STYLES['bullet']} Meilleure attaque: {team_name} ({goals} buts)\n"
        
        if least_goals_conceded:
            team_name = least_goals_conceded.get('team', {}).get('name', 'N/A')
            goals = least_goals_conceded.get('goalsAgainst', 0)
            records_text += f"{self.STYLES['bullet']} Meilleure défense: {team_name} ({goals} buts encaissés)\n"
        
        return records_text
    
    def _get_injury_severity_emoji(self, severity: str) -> str:
        """Retourne l'emoji correspondant à la gravité de la blessure"""
        severity_emojis = {
            'Légère': self.EMOJIS['check'],
            'Moyenne': self.EMOJIS['warning'],
            'Grave': self.EMOJIS['cross'],
            'Très grave': self.EMOJIS['thunder']
        }
        return severity_emojis.get(severity, self.EMOJIS['injury'])
    
    def _get_news_category_emoji(self, category: str) -> str:
        """Retourne l'emoji correspondant à la catégorie de nouvelle"""
        category_emojis = {
            'Général': self.EMOJIS['newspaper'],
            'Transferts': self.EMOJIS['money'],
            'Blessures': self.EMOJIS['injury'],
            'Matchs': self.EMOJIS['soccer'],
            'Championnat': self.EMOJIS['trophy']
        }
        return category_emojis.get(category, self.EMOJIS['trending'])
    
    def _format_error(self, message: str) -> str:
        """Formate un message d'erreur"""
        error_text = f"{self.EMOJIS['cross']} **ERREUR**\n"
        error_text += f"{self.STYLES['bullet']} {message}\n"
        error_text += f"{self.STYLES['bullet']} Veuillez réessayer ou contacter le support.\n"
        
        return error_text
