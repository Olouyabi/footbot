"""
Script de test pour la commande /playerstats
"""
import asyncio
import logging
from enhanced_commands import EnhancedCommands

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_player_stats():
    """Test de la commande playerstats"""
    print("🧪 Test de la commande /playerstats...")
    
    enhanced_commands = EnhancedCommands()
    
    # Test avec différents joueurs
    test_players = [
        "Mbappé",
        "Messi", 
        "Ronaldo",
        "Haaland",
        "Benzema",
        "Neymar",
        "Modric",
        "De Bruyne",
        "Joueur Inconnu"  # Pour tester le cas d'erreur
    ]
    
    for player in test_players:
        print(f"\n--- Test avec {player} ---")
        try:
            result = await enhanced_commands.get_player_stats(player)
            print(f"✅ Résultat pour {player}:")
            print(result)
        except Exception as e:
            print(f"❌ Erreur pour {player}: {e}")
        
        print("\n" + "="*50)

def main():
    """Fonction principale de test"""
    print("🚀 TEST DE LA COMMANDE /PLAYERSTATS 🚀\n")
    
    try:
        asyncio.run(test_player_stats())
        
        print("\n🎉 TOUS LES TESTS SONT TERMINÉS ! 🎉")
        print("\n✨ Joueurs supportés:")
        print("  • Mbappé - Kylian Mbappé (PSG)")
        print("  • Messi - Lionel Messi (Inter Miami)")
        print("  • Ronaldo - Cristiano Ronaldo (Al-Nassr)")
        print("  • Haaland - Erling Haaland (Manchester City)")
        print("  • Benzema - Karim Benzema (Al-Ittihad)")
        print("  • Neymar - Neymar Jr (Al-Hilal)")
        print("  • Modric - Luka Modrić (Real Madrid)")
        print("  • De Bruyne - Kevin De Bruyne (Manchester City)")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        logger.error(f"Erreur lors des tests: {e}")

if __name__ == "__main__":
    main()
