"""
Module d'analyse des matchs de football
Contient la logique d'analyse et de prédiction
"""
import re
from typing import Dict, List, Tuple, Optional
from api_client import FootballAPIClient

class MatchAnalyzer:
    """Analyseur de matchs de football"""
    
    def __init__(self):
        self.api_client = FootballAPIClient()
    
    def parse_match_input(self, match_text: str) -> List[Tuple[str, str]]:
        """Parse le texte d'entrée pour extraire les matchs"""
        matches = []
        lines = match_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Patterns pour détecter les matchs
            patterns = [
                r'(.+?)\s+vs\s+(.+)',  # "Team A vs Team B"
                r'(.+?)\s+v\s+(.+)',    # "Team A v Team B"
                r'(.+?)\s+-\s+(.+)',    # "Team A - Team B"
                r'(.+?)\s+contre\s+(.+)', # "Team A contre Team B"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    team1 = match.group(1).strip()
                    team2 = match.group(2).strip()
                    matches.append((team1, team2))
                    break
        
        return matches
    
    def analyze_match(self, team1_name: str, team2_name: str) -> Dict:
        """Analyse un match entre deux équipes"""
        # Rechercher les équipes
        team1_data = self.api_client.search_team(team1_name)
        team2_data = self.api_client.search_team(team2_name)
        
        if not team1_data:
            return {'error': f'Équipe "{team1_name}" non trouvée'}
        if not team2_data:
            return {'error': f'Équipe "{team2_name}" non trouvée'}
        
        # Récupérer les données d'analyse
        prediction_data = self.api_client.get_match_prediction_data(
            team1_data['id'], team2_data['id']
        )
        
        # Effectuer l'analyse
        analysis = self._perform_analysis(prediction_data)
        
        return {
            'match': f"{team1_name} vs {team2_name}",
            'team1': team1_data,
            'team2': team2_data,
            'analysis': analysis
        }
    
    def _perform_analysis(self, data: Dict) -> Dict:
        """Effectue l'analyse détaillée du match"""
        team1_form = data['team1']['form']
        team2_form = data['team2']['form']
        
        # Calculer les probabilités
        probabilities = self._calculate_probabilities(team1_form, team2_form)
        
        # Calculer le niveau de risque
        risk_level = self._calculate_risk_level(team1_form, team2_form)
        
        # Générer l'analyse textuelle
        analysis_text = self._generate_analysis_text(data, probabilities, risk_level)
        
        return {
            'probabilities': probabilities,
            'risk_level': risk_level,
            'analysis_text': analysis_text,
            'team1_form': team1_form,
            'team2_form': team2_form
        }
    
    def _calculate_probabilities(self, team1_form: Dict, team2_form: Dict) -> Dict:
        """Calcule les probabilités de résultats"""
        # Facteurs d'analyse
        team1_win_rate = team1_form.get('win_rate', 0)
        team2_win_rate = team2_form.get('win_rate', 0)
        
        team1_avg_goals = team1_form.get('avg_goals_scored', 0)
        team2_avg_goals = team2_form.get('avg_goals_scored', 0)
        
        team1_goals_conceded = team1_form.get('avg_goals_conceded', 0)
        team2_goals_conceded = team2_form.get('avg_goals_conceded', 0)
        
        # Calcul des probabilités (simplifié)
        # Probabilité de victoire équipe 1
        prob_team1_win = (team1_win_rate + (100 - team2_win_rate)) / 2
        
        # Probabilité de victoire équipe 2
        prob_team2_win = (team2_win_rate + (100 - team1_win_rate)) / 2
        
        # Probabilité de match nul (basée sur les performances défensives)
        prob_draw = min(30, (team1_goals_conceded + team2_goals_conceded) * 10)
        
        # Normaliser les probabilités
        total_prob = prob_team1_win + prob_team2_win + prob_draw
        prob_team1_win = (prob_team1_win / total_prob) * 100
        prob_team2_win = (prob_team2_win / total_prob) * 100
        prob_draw = (prob_draw / total_prob) * 100
        
        # Probabilité de plus de 2.5 buts
        total_avg_goals = team1_avg_goals + team2_avg_goals
        prob_over_2_5 = min(80, max(20, total_avg_goals * 20))
        
        return {
            'team1_win': round(prob_team1_win, 1),
            'team2_win': round(prob_team2_win, 1),
            'draw': round(prob_draw, 1),
            'over_2_5': round(prob_over_2_5, 1),
            'under_2_5': round(100 - prob_over_2_5, 1)
        }
    
    def _calculate_risk_level(self, team1_form: Dict, team2_form: Dict) -> str:
        """Calcule le niveau de risque du match"""
        # Facteurs de risque
        team1_consistency = abs(team1_form.get('win_rate', 50) - 50)
        team2_consistency = abs(team2_form.get('win_rate', 50) - 50)
        
        # Différence de forme entre les équipes
        form_difference = abs(team1_form.get('win_rate', 50) - team2_form.get('win_rate', 50))
        
        # Calcul du risque
        risk_score = (team1_consistency + team2_consistency + form_difference) / 3
        
        if risk_score < 20:
            return "Faible"
        elif risk_score < 40:
            return "Moyen"
        else:
            return "Élevé"
    
    def _generate_analysis_text(self, data: Dict, probabilities: Dict, risk_level: str) -> str:
        """Génère l'analyse textuelle du match avec un formatage amélioré"""
        team1_name = data['team1']['stats'].get('name', 'Équipe 1')
        team2_name = data['team2']['stats'].get('name', 'Équipe 2')
        
        team1_form = data['team1']['form']
        team2_form = data['team2']['form']
        
        # Header avec style amélioré
        analysis = f"🔥 ANALYSE FOOTBALL 🔥\n"
        analysis += f"╔═══════════════════════════════════════╗\n"
        analysis += f"║           {team1_name} vs {team2_name}           ║\n"
        analysis += f"╚═══════════════════════════════════════╝\n\n"

        # Forme récente avec emojis
        analysis += f"📊 FORME RÉCENTE (5 derniers matchs)\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        
        # Forme équipe 1
        form1_emoji = self._get_form_emoji(team1_form)
        analysis += f"│ {form1_emoji} {team1_name}\n"
        analysis += f"│ {team1_form.get('form', 'N/A')} ({self._get_form_stats(team1_form)})\n"
        
        # Forme équipe 2
        form2_emoji = self._get_form_emoji(team2_form)
        analysis += f"│ {form2_emoji} {team2_name}\n"
        analysis += f"│ {team2_form.get('form', 'N/A')} ({self._get_form_stats(team2_form)})\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Statistiques avec barres visuelles
        analysis += f"⚽ STATISTIQUES DÉTAILLÉES\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        
        # Stats équipe 1
        team1_goals_for = team1_form.get('avg_goals_scored', 0)
        team1_goals_against = team1_form.get('avg_goals_conceded', 0)
        analysis += f"│ 🏠 {team1_name}\n"
        analysis += f"│ Buts marqués: {team1_goals_for:.1f} {self._create_bar(team1_goals_for, 3)}\n"
        analysis += f"│ Buts encaissés: {team1_goals_against:.1f} {self._create_bar(team1_goals_against, 3, reverse=True)}\n"
        
        # Stats équipe 2
        team2_goals_for = team2_form.get('avg_goals_scored', 0)
        team2_goals_against = team2_form.get('avg_goals_conceded', 0)
        analysis += f"│ 🚌 {team2_name}\n"
        analysis += f"│ Buts marqués: {team2_goals_for:.1f} {self._create_bar(team2_goals_for, 3)}\n"
        analysis += f"│ Buts encaissés: {team2_goals_against:.1f} {self._create_bar(team2_goals_against, 3, reverse=True)}\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Prédictions avec barres de probabilité
        analysis += f"🎯 PRÉDICTIONS DU MATCH\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        
        win1_prob = probabilities.get('team1_win', 0)
        draw_prob = probabilities.get('draw', 0)
        win2_prob = probabilities.get('team2_win', 0)
        
        analysis += f"│ 🏆 {team1_name}: {win1_prob:.1f}% {self._create_probability_bar(win1_prob)}\n"
        analysis += f"│ 🤝 Match nul: {draw_prob:.1f}% {self._create_probability_bar(draw_prob)}\n"
        analysis += f"│ 🏆 {team2_name}: {win2_prob:.1f}% {self._create_probability_bar(win2_prob)}\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Pronostic buts
        over_25_prob = probabilities.get('over_2_5', 0)
        under_25_prob = probabilities.get('under_2_5', 0)
        
        analysis += f"⚽ PRONOSTIC BUTS (+2.5)\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        analysis += f"│ ✅ Plus de 2.5: {over_25_prob:.1f}% {self._create_probability_bar(over_25_prob)}\n"
        analysis += f"│ ❌ Moins de 2.5: {under_25_prob:.1f}% {self._create_probability_bar(under_25_prob)}\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Niveau de risque avec emoji
        risk_emoji = self._get_risk_emoji(risk_level)
        analysis += f"⚠️ NIVEAU DE RISQUE: {risk_emoji} {risk_level.upper()}\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        analysis += f"│ {self._get_risk_description(risk_level)}\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Analyse détaillée
        analysis += f"💡 ANALYSE EXPERTE\n"
        analysis += f"┌─────────────────────────────────────┐\n"
        analysis += f"│ {self._generate_match_commentary(data, probabilities, risk_level)}\n"
        analysis += f"└─────────────────────────────────────┘\n\n"

        # Footer
        analysis += f"🤖 Analyse générée par FootStat Analyzer v2.0\n"
        analysis += f"📅 {self._get_current_time()}\n"

        return analysis
    
    def _generate_match_commentary(self, data: Dict, probabilities: Dict, risk_level: str) -> str:
        """Génère un commentaire d'analyse du match"""
        team1_form = data['team1']['form']
        team2_form = data['team2']['form']
        
        commentary = ""
        
        # Analyse de la forme
        if team1_form.get('win_rate', 0) > 70:
            commentary += "L'équipe à domicile affiche une excellente forme récente. "
        elif team1_form.get('win_rate', 0) < 30:
            commentary += "L'équipe à domicile traverse une période difficile. "
        
        if team2_form.get('win_rate', 0) > 70:
            commentary += "L'équipe visiteuse arrive en confiance. "
        elif team2_form.get('win_rate', 0) < 30:
            commentary += "L'équipe visiteuse semble en difficulté. "
        
        # Analyse offensive/défensive
        team1_offense = team1_form.get('avg_goals_scored', 0)
        team2_defense = team2_form.get('avg_goals_conceded', 0)
        
        if team1_offense > 2 and team2_defense > 1.5:
            commentary += "Le potentiel offensif de l'équipe à domicile face à une défense fragile pourrait être décisif. "
        
        # Analyse des buts
        total_avg_goals = team1_offense + team2_form.get('avg_goals_scored', 0)
        if total_avg_goals > 3:
            commentary += "Les deux équipes sont prolifiques devant le but, un match riche en buts est probable. "
        elif total_avg_goals < 2:
            commentary += "Les statistiques suggèrent un match plutôt défensif. "
        
        # Recommandation finale
        if probabilities['team1_win'] > 50:
            commentary += f"L'équipe à domicile semble avoir un léger avantage statistique."
        elif probabilities['team2_win'] > 50:
            commentary += f"L'équipe visiteuse pourrait surprendre selon les données récentes."
        else:
            commentary += f"Un match équilibré où le nul reste une possibilité sérieuse."
        
        return commentary
    
    def analyze_multiple_matches(self, matches_text: str) -> List[Dict]:
        """Analyse plusieurs matchs"""
        matches = self.parse_match_input(matches_text)
        results = []
        
        for team1, team2 in matches:
            try:
                analysis = self.analyze_match(team1, team2)
                results.append(analysis)
            except Exception as e:
                results.append({
                    'match': f"{team1} vs {team2}",
                    'error': f"Erreur lors de l'analyse: {str(e)}"
                })
        
        return results
    
    def _get_form_emoji(self, form_data: Dict) -> str:
        """Retourne un emoji basé sur la forme de l'équipe"""
        win_rate = form_data.get('win_rate', 0)
        if win_rate >= 80:
            return "🔥"
        elif win_rate >= 60:
            return "⚡"
        elif win_rate >= 40:
            return "⚖️"
        elif win_rate >= 20:
            return "⚠️"
        else:
            return "❌"
    
    def _get_form_stats(self, form_data: Dict) -> str:
        """Retourne les statistiques de forme formatées"""
        wins = form_data.get('wins', 0)
        draws = form_data.get('draws', 0)
        losses = form_data.get('losses', 0)
        win_rate = form_data.get('win_rate', 0)
        return f"{wins}V-{draws}N-{losses}D ({win_rate:.0f}%)"
    
    def _create_bar(self, value: float, max_value: float, reverse: bool = False) -> str:
        """Crée une barre visuelle pour les statistiques"""
        if max_value == 0:
            return "░" * 10
        
        ratio = min(value / max_value, 1.0)
        filled = int(ratio * 10)
        empty = 10 - filled
        
        if reverse:
            return "🟢" * empty + "🔴" * filled
        else:
            return "🟢" * filled + "🔴" * empty
    
    def _create_probability_bar(self, probability: float) -> str:
        """Crée une barre de probabilité visuelle"""
        filled = int(probability / 5)  # 5% par bloc
        empty = 20 - filled
        return "█" * filled + "░" * empty
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """Retourne un emoji basé sur le niveau de risque"""
        risk_emojis = {
            "Faible": "🟢",
            "Moyen": "🟡", 
            "Élevé": "🔴"
        }
        return risk_emojis.get(risk_level, "❓")
    
    def _get_risk_description(self, risk_level: str) -> str:
        """Retourne une description du niveau de risque"""
        descriptions = {
            "Faible": "Match prévisible, peu de surprises attendues. Les statistiques sont claires et cohérentes.",
            "Moyen": "Match équilibré avec quelques incertitudes. Les équipes sont de niveau comparable.",
            "Élevé": "Match très imprévisible avec beaucoup d'incertitudes. Attention aux surprises !"
        }
        return descriptions.get(risk_level, "Niveau de risque indéterminé")
    
    def _get_current_time(self) -> str:
        """Retourne l'heure actuelle formatée"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y à %H:%M")
