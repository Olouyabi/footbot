#!/usr/bin/env python3
"""
Script de demonstration des fonctionnalites avancees du bot FootStat Analyzer
"""
import asyncio
import logging
from utils import CacheManager, ErrorHandler, Paginator, UserSettings, LeagueManager

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def demo_cache_system():
    """Demonstre le systeme de cache"""
    print("\n=== DEMONSTRATION DU SYSTEME DE CACHE ===")
    
    cache = CacheManager(cache_dir="demo_cache", default_ttl=30)
    
    # Test de base
    test_data = {"team": "Barcelona", "wins": 5, "losses": 1}
    cache.set("test_team", test_data, ttl=10)
    
    cached_result = cache.get("test_team")
    print(f"Donnees mises en cache et recuperees: {cached_result}")
    
    # Test de statistiques
    stats = cache.get_stats()
    print(f"Statistiques du cache: {stats}")
    
    # Test de vidage
    cache.clear()
    cleared_stats = cache.get_stats()
    print(f"Cache vide. Nouvelles statistiques: {cleared_stats}")

async def demo_error_handling():
    """Demonstre la gestion d'erreurs amelioree"""
    print("\n=== DEMONSTRATION DE LA GESTION D'ERREURS ===")
    
    error_handler = ErrorHandler()
    
    # Simulation d'erreurs API
    test_errors = [
        Exception("Rate limit exceeded: 429"),
        Exception("Team not found: 404"),
        Exception("Network connection failed"),
        Exception("Request timeout"),
        Exception("Unknown API error: 500")
    ]
    
    for error in test_errors:
        error_info = error_handler.handle_api_error(error, "Test API call")
        print(f"Erreur: {error_info['code']}")
        print(f"Message utilisateur: {error_info['user_message']}")
        print(f"Message fallback: {error_handler.get_fallback_message(error_info['code'])}")
        print("---")

async def demo_pagination():
    """Demonstre le systeme de pagination"""
    print("\n=== DEMONSTRATION DE LA PAGINATION ===")
    
    paginator = Paginator(items_per_page=3)
    
    # Donnees de test (analyses de matchs)
    test_matches = [
        {"match": "Real Madrid vs Barcelona", "risk": "Faible"},
        {"match": "Liverpool vs Chelsea", "risk": "Moyen"},
        {"match": "PSG vs Marseille", "risk": "Eleve"},
        {"match": "Bayern vs Dortmund", "risk": "Faible"},
        {"match": "Juventus vs Inter", "risk": "Moyen"},
        {"match": "Man City vs Arsenal", "risk": "Moyen"},
        {"match": "Atletico vs Sevilla", "risk": "Eleve"},
    ]
    
    # Test pagination
    for page in [1, 2, 3]:
        pagination_data = paginator.paginate(test_matches, page)
        print(f"\nPage {page}/{pagination_data['total_pages']}:")
        print(f"   Elements {pagination_data['start_index']}-{pagination_data['end_index']}")
        print(f"   Precedent: {pagination_data.get('previous_page', 'N/A')}")
        print(f"   Suivant: {pagination_data.get('next_page', 'N/A')}")
        
        for item in pagination_data['items']:
            print(f"   - {item['match']} - Risque: {item['risk']}")

async def demo_user_settings():
    """Demonstre la gestion des parametres utilisateur"""
    print("\n=== DEMONSTRATION DES PARAMETRES UTILISATEUR ===")
    
    cache = CacheManager()
    user_settings = UserSettings(cache)
    
    test_user_id = 12345
    
    # Recuperation des parametres par defaut
    settings = user_settings.get_user_settings(test_user_id)
    print(f"Parametres utilisateur {test_user_id}: {settings}")
    
    # Changement de ligue
    if user_settings.set_league(test_user_id, 'PL'):
        league_info = LeagueManager.get_league_info('PL')
        print(f"Ligue changee: {league_info['name']}")
    
    # Basculement du mode IA
    new_mode = user_settings.toggle_ai_mode(test_user_id)
    print(f"Mode IA: {'Active' if new_mode else 'Desactive'}")

async def demo_league_manager():
    """Demonstre le gestionnaire de ligues"""
    print("\n=== DEMONSTRATION DU GESTIONNAIRE DE LIGUES ===")
    
    league_manager = LeagueManager()
    
    print("Toutes les ligues supportees:")
    all_leagues = league_manager.get_all_leagues()
    for code, info in all_leagues.items():
        print(f"   - {code}: {info['name']} ({info['country']}) - {info['teams']} equipes")
    
    print(f"\nInformations detaillees Premier League:")
    pl_info = league_manager.get_league_info('PL')
    print(f"   {pl_info}")

async def main():
    """Fonction principale de demonstration"""
    print("Demonstration des Fonctionnalites Avancees - FootStat Analyzer v2.0")
    print("=" * 80)
    
    try:
        await demo_cache_system()
        await demo_error_handling()
        await demo_pagination()
        await demo_user_settings()
        await demo_league_manager()
        
        print("\nToutes les demonstrations se sont executees avec succes!")
        print("Consultez ADVANCED_FEATURES.md pour plus de details.")
        
    except Exception as e:
        logger.error(f"Erreur lors de la demonstration: {e}")
        print(f"Erreur: {e}")
    
    finally:
        # Nettoyage
        print("\nNettoyage des fichiers de demonstration...")
        import shutil
        import os
        
        for demo_dir in ["demo_cache", "demo_integration_cache"]:
            if os.path.exists(demo_dir):
                shutil.rmtree(demo_dir)
                print(f"   Dossier {demo_dir} supprime")

if __name__ == "__main__":
    # Creer le dossier de demonstration
    import os
    os.makedirs("demo_cache", exist_ok=True)
    os.makedirs("demo_integration_cache", exist_ok=True)
    
    # Executer la demonstration
    asyncio.run(main())
