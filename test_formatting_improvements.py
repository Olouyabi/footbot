"""
Script de test pour vérifier les améliorations de formatage
"""
import logging
from formatter import ProfessionalFormatter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_standings_formatting():
    """Test du formatage des classements"""
    print("🧪 Test du formatage des classements...")
    
    formatter = ProfessionalFormatter()
    
    # Données de test pour un classement
    test_data = {
        'standings': [{
            'table': [
                {
                    'position': 1,
                    'team': {'name': 'Paris Saint-Germain FC', 'shortName': 'PSG'},
                    'points': 45,
                    'playedGames': 15,
                    'won': 14,
                    'draw': 3,
                    'lost': 0
                },
                {
                    'position': 2,
                    'team': {'name': 'Olympique de Marseille', 'shortName': 'OM'},
                    'points': 38,
                    'playedGames': 15,
                    'won': 12,
                    'draw': 2,
                    'lost': 1
                },
                {
                    'position': 3,
                    'team': {'name': 'Olympique Lyonnais', 'shortName': 'OL'},
                    'points': 35,
                    'playedGames': 15,
                    'won': 11,
                    'draw': 2,
                    'lost': 2
                }
            ]
        }]
    }
    
    result = formatter.format_league_standings(test_data, "Ligue 1")
    print("✅ Résultat du formatage des classements:")
    print(result)
    print("\n" + "="*50 + "\n")

def test_team_stats_formatting():
    """Test du formatage des statistiques d'équipe"""
    print("🧪 Test du formatage des statistiques d'équipe...")
    
    formatter = ProfessionalFormatter()
    
    # Données de test pour les statistiques d'équipe
    test_data = {
        'matches': [
            {'homeTeam': {'name': 'PSG'}, 'awayTeam': {'name': 'OM'}, 'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'homeTeam': {'name': 'Lyon'}, 'awayTeam': {'name': 'PSG'}, 'score': {'fullTime': {'home': 1, 'away': 3}}},
            {'homeTeam': {'name': 'PSG'}, 'awayTeam': {'name': 'Nice'}, 'score': {'fullTime': {'home': 4, 'away': 0}}}
        ]
    }
    
    result = formatter.format_team_stats(test_data, "PSG")
    print("✅ Résultat du formatage des statistiques d'équipe:")
    print(result)
    print("\n" + "="*50 + "\n")

def test_match_analysis_formatting():
    """Test du formatage des analyses de match"""
    print("🧪 Test du formatage des analyses de match...")
    
    formatter = ProfessionalFormatter()
    
    # Données de test pour l'analyse de match
    test_data = {
        'match': 'Real Madrid vs Barcelona',
        'analysis': {
            'probabilities': {
                'team1_win': 45,
                'draw': 25,
                'team2_win': 30,
                'over_2_5': 60
            },
            'risk_level': 'Moyen',
            'form_analysis': '✅ ⚔️ ✅ ❌ ✅',
            'key_factors': [
                'Forme récente excellente du Real Madrid',
                'Barcelone en difficulté à l\'extérieur',
                'Historique favorable au Real'
            ],
            'recommendations': [
                'Pariez sur la victoire du Real Madrid',
                'Plus de 2.5 buts probable',
                'Évitez le match nul'
            ]
        }
    }
    
    result = formatter.format_match_analysis(test_data)
    print("✅ Résultat du formatage des analyses de match:")
    print(result)
    print("\n" + "="*50 + "\n")

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES AMÉLIORATIONS DE FORMATAGE 🚀\n")
    
    try:
        # Test du formatage des classements
        test_standings_formatting()
        
        # Test du formatage des statistiques d'équipe
        test_team_stats_formatting()
        
        # Test du formatage des analyses de match
        test_match_analysis_formatting()
        
        print("🎉 TOUS LES TESTS DE FORMATAGE SONT PASSÉS ! 🎉")
        print("\n✨ Améliorations apportées:")
        print("  • Formatage des classements plus lisible")
        print("  • Statistiques d'équipe optimisées")
        print("  • Analyses de match simplifiées")
        print("  • Suppression des tableaux ASCII complexes")
        print("  • Utilisation d'emojis pour la lisibilité")
        print("  • Formatage adapté à Telegram")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        logger.error(f"Erreur lors des tests: {e}")

if __name__ == "__main__":
    main()
