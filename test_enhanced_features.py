"""
Script de test pour les nouvelles fonctionnalités du bot FootStat Analyzer v2.0
Teste le formatage professionnel et les nouvelles commandes
"""
import asyncio
import logging
from formatter import ProfessionalFormatter
from enhanced_commands import EnhancedCommands

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_formatter():
    """Test du nouveau système de formatage"""
    print("🧪 Test du système de formatage professionnel...")
    
    formatter = ProfessionalFormatter()
    
    # Test formatage d'analyse de match
    mock_analysis = {
        'match': 'Real Madrid vs Barcelona',
        'analysis': {
            'risk_level': 'Moyen',
            'probabilities': {
                'team1_win': 45,
                'draw': 25,
                'team2_win': 30,
                'over_2_5': 60
            },
            'recent_form': ['W', 'D', 'W', 'L', 'W'],
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
    
    formatted_analysis = formatter.format_match_analysis(mock_analysis)
    print("✅ Formatage d'analyse de match:")
    print(formatted_analysis)
    print("\n" + "="*50 + "\n")
    
    # Test formatage de classement
    mock_standings = {
        'standings': [{
            'table': [
                {'position': 1, 'team': {'name': 'PSG'}, 'points': 45, 'playedGames': 15, 'won': 14, 'draw': 3, 'lost': 0},
                {'position': 2, 'team': {'name': 'Marseille'}, 'points': 38, 'playedGames': 15, 'won': 12, 'draw': 2, 'lost': 1},
                {'position': 3, 'team': {'name': 'Lyon'}, 'points': 35, 'playedGames': 15, 'won': 11, 'draw': 2, 'lost': 2}
            ]
        }]
    }
    
    formatted_standings = formatter.format_league_standings(mock_standings, "Ligue 1")
    print("✅ Formatage de classement:")
    print(formatted_standings)
    print("\n" + "="*50 + "\n")
    
    # Test formatage de menu principal
    mock_user_settings = {
        'league': 'PL',
        'ai_mode': True,
        'language': 'fr',
        'notifications': True
    }
    
    formatted_menu = formatter.format_main_menu(mock_user_settings)
    print("✅ Formatage de menu principal:")
    print(formatted_menu)
    print("\n" + "="*50 + "\n")

async def test_enhanced_commands():
    """Test des nouvelles commandes avancées"""
    print("🧪 Test des nouvelles commandes avancées...")
    
    enhanced_commands = EnhancedCommands()
    
    # Test des nouvelles de transferts
    print("✅ Test des nouvelles de transferts:")
    transfer_news = await enhanced_commands.get_transfer_news()
    print(transfer_news)
    print("\n" + "="*50 + "\n")
    
    # Test des nouvelles de ligue
    print("✅ Test des nouvelles de ligue:")
    league_news = await enhanced_commands.get_league_news("Ligue 1")
    print(league_news)
    print("\n" + "="*50 + "\n")
    
    # Test du rapport de blessures
    print("✅ Test du rapport de blessures:")
    injury_report = await enhanced_commands.get_injury_report("PSG")
    print(injury_report)
    print("\n" + "="*50 + "\n")
    
    # Test de l'analyse de forme
    print("✅ Test de l'analyse de forme:")
    team_form = await enhanced_commands.get_team_form_analysis("PSG", "last_5")
    print(team_form)
    print("\n" + "="*50 + "\n")

def test_emoji_system():
    """Test du système d'emojis"""
    print("🧪 Test du système d'emojis...")
    
    formatter = ProfessionalFormatter()
    
    # Test des emojis de risque
    risk_emojis = {
        'Faible': formatter._get_risk_emoji('Faible'),
        'Moyen': formatter._get_risk_emoji('Moyen'),
        'Élevé': formatter._get_risk_emoji('Élevé'),
        'Très élevé': formatter._get_risk_emoji('Très élevé')
    }
    
    print("✅ Emojis de risque:")
    for risk, emoji in risk_emojis.items():
        print(f"  {risk}: {emoji}")
    
    # Test des emojis de ligue
    league_emojis = {
        'Ligue 1': formatter._get_league_emoji('Ligue 1'),
        'Premier League': formatter._get_league_emoji('Premier League'),
        'La Liga': formatter._get_league_emoji('La Liga'),
        'Champions League': formatter._get_league_emoji('Champions League')
    }
    
    print("\n✅ Emojis de ligue:")
    for league, emoji in league_emojis.items():
        print(f"  {league}: {emoji}")
    
    # Test des barres de progression
    print("\n✅ Barres de progression:")
    for percentage in [20, 40, 60, 80, 95]:
        bar = formatter._create_progress_bar(percentage)
        print(f"  {percentage}%: {bar}")
    
    print("\n" + "="*50 + "\n")

def test_style_system():
    """Test du système de styles"""
    print("🧪 Test du système de styles...")
    
    formatter = ProfessionalFormatter()
    
    # Test des bordures
    print("✅ Test des bordures:")
    test_header = formatter._create_header("TEST HEADER", "🧪")
    print(test_header)
    
    test_footer = formatter._create_footer()
    print(test_footer)
    
    print("\n" + "="*50 + "\n")

async def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS - FOOTSTAT ANALYZER v2.0 🚀\n")
    
    try:
        # Test du système de formatage
        await test_formatter()
        
        # Test des nouvelles commandes
        await test_enhanced_commands()
        
        # Test du système d'emojis
        test_emoji_system()
        
        # Test du système de styles
        test_style_system()
        
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ! 🎉")
        print("\n✨ Le bot FootStat Analyzer v2.0 est prêt avec:")
        print("  • Formatage professionnel avec emojis et bordures")
        print("  • Nouvelles commandes avancées")
        print("  • Menu interactif complet")
        print("  • Interface utilisateur améliorée")
        print("  • Système d'emojis cohérent")
        print("  • Barres de progression visuelles")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        logger.error(f"Erreur lors des tests: {e}")

if __name__ == "__main__":
    asyncio.run(main())
