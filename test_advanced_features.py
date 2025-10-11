"""
Script de test pour les nouvelles fonctionnalités avancées
"""
import asyncio
import logging
from advanced_commands import AdvancedCommands
from analyzer import MatchAnalyzer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_advanced_features():
    """Test des fonctionnalités avancées"""
    print("🔥 Test des fonctionnalités avancées FootStat Analyzer v2.0")
    print("=" * 60)
    
    # Initialiser les composants
    advanced_commands = AdvancedCommands()
    analyzer = MatchAnalyzer()
    
    print("\n1. Test du formatage amélioré des analyses...")
    try:
        # Test d'analyse avec le nouveau formatage
        analysis = analyzer.analyze_match("Real Madrid", "Barcelona")
        if 'error' not in analysis:
            print("✅ Formatage amélioré fonctionne")
            print("📊 Aperçu de l'analyse:")
            print(analysis.get('analysis', {}).get('analysis_text', '')[:200] + "...")
        else:
            print(f"❌ Erreur dans l'analyse: {analysis['error']}")
    except Exception as e:
        print(f"❌ Erreur lors du test d'analyse: {e}")
    
    print("\n2. Test des commandes avancées...")
    
    # Test classement
    print("\n📊 Test du classement Ligue 1...")
    try:
        standings = await advanced_commands.get_league_standings("Ligue 1")
        print("✅ Récupération du classement réussie")
        print("📈 Aperçu du classement:")
        print(standings[:300] + "..." if len(standings) > 300 else standings)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du classement: {e}")
    
    # Test statistiques d'équipe
    print("\n⚽ Test des statistiques d'équipe...")
    try:
        team_stats = await advanced_commands.get_team_stats("PSG")
        print("✅ Récupération des statistiques d'équipe réussie")
        print("📊 Aperçu des statistiques:")
        print(team_stats[:300] + "..." if len(team_stats) > 300 else team_stats)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des stats d'équipe: {e}")
    
    # Test matchs à venir
    print("\n📅 Test des matchs à venir...")
    try:
        upcoming = await advanced_commands.get_upcoming_matches("Premier League")
        print("✅ Récupération des matchs à venir réussie")
        print("📅 Aperçu des matchs:")
        print(upcoming[:300] + "..." if len(upcoming) > 300 else upcoming)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des matchs à venir: {e}")
    
    # Test comparaison d'équipes
    print("\n⚖️ Test de comparaison d'équipes...")
    try:
        comparison = await advanced_commands.compare_teams("Manchester City", "Arsenal")
        print("✅ Comparaison d'équipes réussie")
        print("⚖️ Aperçu de la comparaison:")
        print(comparison[:300] + "..." if len(comparison) > 300 else comparison)
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison d'équipes: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Tests des fonctionnalités avancées terminés !")
    print("\n📋 RÉSUMÉ DES NOUVELLES FONCTIONNALITÉS:")
    print("• Formatage amélioré avec emojis et barres visuelles")
    print("• Commandes /standings, /teamstats, /upcoming, /compare")
    print("• Support de multiples championnats")
    print("• Cache intelligent pour des réponses rapides")
    print("• Gestion d'erreurs robuste")
    print("• Interface utilisateur améliorée")

if __name__ == "__main__":
    asyncio.run(test_advanced_features())
