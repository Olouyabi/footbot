"""
Module IA pour améliorer les analyses de matchs
Utilise OpenAI pour générer des analyses plus humaines et détaillées
"""
import openai
from typing import Dict, List, Optional
from config import Config

class AIModule:
    """Module d'intelligence artificielle pour l'analyse de matchs"""
    
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.enabled = Config.AI_MODE_ENABLED
        
        if self.enabled and self.api_key:
            openai.api_key = self.api_key
        else:
            self.enabled = False
    
    def enhance_analysis(self, analysis_data: Dict) -> str:
        """Améliore une analyse existante avec l'IA"""
        if not self.enabled:
            return analysis_data.get('analysis_text', '')
        
        try:
            # Préparer le prompt pour l'IA
            prompt = self._create_analysis_prompt(analysis_data)
            
            # Appeler l'API OpenAI avec timeout
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,  # Réduire pour éviter les timeouts
                temperature=0.7,
                timeout=10  # Timeout de 10 secondes
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erreur IA (timeout ou autre): {e}")
            # Retourner l'analyse de base en cas d'erreur
            return analysis_data.get('analysis_text', '')
    
    def generate_detailed_prediction(self, analysis_data: Dict) -> str:
        """Génère une prédiction détaillée avec l'IA"""
        if not self.enabled:
            return self._generate_basic_prediction(analysis_data)
        
        try:
            prompt = self._create_prediction_prompt(analysis_data)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_prediction_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erreur IA prédiction: {e}")
            return self._generate_basic_prediction(analysis_data)
    
    def generate_match_summary(self, analyses: List[Dict]) -> str:
        """Génère un résumé de plusieurs analyses"""
        if not self.enabled:
            return self._generate_basic_summary(analyses)
        
        try:
            prompt = self._create_summary_prompt(analyses)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_summary_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erreur IA résumé: {e}")
            return self._generate_basic_summary(analyses)
    
    def _get_system_prompt(self) -> str:
        """Prompt système pour l'analyse"""
        return """Tu es un expert en football et analyste sportif. 
        Ton rôle est d'améliorer les analyses de matchs de football en les rendant plus humaines, 
        détaillées et engageantes. Tu dois :
        - Utiliser un langage naturel et accessible
        - Ajouter des insights pertinents basés sur les données
        - Mentionner des facteurs tactiques et psychologiques
        - Garder un ton professionnel mais convivial
        - Structurer l'information de manière claire"""
    
    def _get_prediction_system_prompt(self) -> str:
        """Prompt système pour les prédictions"""
        return """Tu es un expert en prédictions de matchs de football. 
        Basé sur les statistiques fournies, donne une prédiction claire et argumentée.
        Inclus :
        - Un score probable
        - Les facteurs clés du match
        - Une recommandation de pari (si applicable)
        - Les risques à considérer"""
    
    def _get_summary_system_prompt(self) -> str:
        """Prompt système pour les résumés"""
        return """Tu es un analyste sportif qui résume plusieurs analyses de matchs.
        Crée un résumé concis qui :
        - Met en évidence les matchs les plus intéressants
        - Identifie les tendances communes
        - Donne des recommandations générales
        - Reste accessible et informatif"""
    
    def _create_analysis_prompt(self, analysis_data: Dict) -> str:
        """Crée le prompt pour améliorer l'analyse"""
        match = analysis_data.get('match', '')
        probabilities = analysis_data.get('analysis', {}).get('probabilities', {})
        team1_form = analysis_data.get('analysis', {}).get('team1_form', {})
        team2_form = analysis_data.get('analysis', {}).get('team2_form', {})
        risk_level = analysis_data.get('analysis', {}).get('risk_level', '')
        
        prompt = f"""
        Améliore cette analyse de match de football :
        
        Match : {match}
        
        Probabilités :
        - Victoire équipe 1 : {probabilities.get('team1_win', 0)}%
        - Match nul : {probabilities.get('draw', 0)}%
        - Victoire équipe 2 : {probabilities.get('team2_win', 0)}%
        - Plus de 2.5 buts : {probabilities.get('over_2.5', 0)}%
        
        Forme équipe 1 : {team1_form.get('form', 'N/A')} ({team1_form.get('win_rate', 0)}% victoires)
        Forme équipe 2 : {team2_form.get('form', 'N/A')} ({team2_form.get('win_rate', 0)}% victoires)
        
        Niveau de risque : {risk_level}
        
        Rends cette analyse plus humaine, détaillée et engageante en ajoutant des insights tactiques et psychologiques.
        """
        
        return prompt
    
    def _create_prediction_prompt(self, analysis_data: Dict) -> str:
        """Crée le prompt pour la prédiction"""
        match = analysis_data.get('match', '')
        probabilities = analysis_data.get('analysis', {}).get('probabilities', {})
        
        prompt = f"""
        Basé sur ces données, donne une prédiction détaillée pour le match :
        
        {match}
        
        Probabilités :
        - Victoire équipe 1 : {probabilities.get('team1_win', 0)}%
        - Match nul : {probabilities.get('draw', 0)}%
        - Victoire équipe 2 : {probabilities.get('team2_win', 0)}%
        
        Prédiction attendue :
        - Score probable
        - Facteurs clés
        - Recommandation
        """
        
        return prompt
    
    def _create_summary_prompt(self, analyses: List[Dict]) -> str:
        """Crée le prompt pour le résumé"""
        matches_info = []
        for analysis in analyses:
            if 'error' not in analysis:
                match = analysis.get('match', '')
                probabilities = analysis.get('analysis', {}).get('probabilities', {})
                risk = analysis.get('analysis', {}).get('risk_level', '')
                matches_info.append(f"{match} - Risque: {risk}")
        
        prompt = f"""
        Résume ces analyses de matchs de football :
        
        {chr(10).join(matches_info)}
        
        Crée un résumé qui identifie les matchs les plus intéressants et les tendances communes.
        """
        
        return prompt
    
    def _generate_basic_prediction(self, analysis_data: Dict) -> str:
        """Génère une prédiction basique sans IA"""
        probabilities = analysis_data.get('analysis', {}).get('probabilities', {})
        match = analysis_data.get('match', '')
        
        team1_win = probabilities.get('team1_win', 0)
        team2_win = probabilities.get('team2_win', 0)
        draw = probabilities.get('draw', 0)
        
        if team1_win > team2_win and team1_win > draw:
            prediction = f"Victoire probable de l'équipe à domicile ({team1_win}%)"
        elif team2_win > team1_win and team2_win > draw:
            prediction = f"Victoire probable de l'équipe visiteuse ({team2_win}%)"
        else:
            prediction = f"Match nul probable ({draw}%)"
        
        return f"🎯 *Prédiction pour {match} :*\n{prediction}"
    
    def _generate_basic_summary(self, analyses: List[Dict]) -> str:
        """Génère un résumé basique sans IA"""
        total_matches = len(analyses)
        successful_analyses = [a for a in analyses if 'error' not in a]
        
        summary = f"📊 *Résumé de {total_matches} analyses :*\n\n"
        
        if successful_analyses:
            high_risk_matches = [a for a in successful_analyses 
                               if a.get('analysis', {}).get('risk_level') == 'Élevé']
            
            summary += f"• {len(successful_analyses)} analyses réussies\n"
            summary += f"• {len(high_risk_matches)} matchs à risque élevé\n"
            
            if high_risk_matches:
                summary += "\n⚠️ *Matchs à surveiller :*\n"
                for match in high_risk_matches[:3]:
                    summary += f"• {match.get('match', '')}\n"
        
        return summary
    
    def is_enabled(self) -> bool:
        """Vérifie si le mode IA est activé"""
        return self.enabled
    
    def toggle_mode(self) -> bool:
        """Active/désactive le mode IA"""
        self.enabled = not self.enabled
        return self.enabled
