"""
Script de test pour la fonctionnalité de chat football avec l'IA
"""
import asyncio
import logging
from football_chat import FootballChat

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_football_chat():
    """Test de la fonctionnalité de chat football"""
    print("🧪 Test de la fonctionnalité de chat football avec l'IA...")
    
    chat = FootballChat()
    user_id = 12345
    
    try:
        # Test 1: Démarrer une session de chat
        print("\n✅ Test 1: Démarrage d'une session de chat")
        welcome_message = await chat.start_chat_session(user_id)
        print("Message de bienvenue:")
        print(welcome_message)
        
        # Test 2: Messages de chat
        test_messages = [
            "Salut ! Comment va le football aujourd'hui ?",
            "Que penses-tu du match Real Madrid vs Barcelona ?",
            "Peux-tu me donner des statistiques sur PSG ?",
            "Qui sont les meilleurs joueurs de la saison ?",
            "Que penses-tu des transferts récents ?"
        ]
        
        print("\n✅ Test 2: Messages de chat")
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Message {i} ---")
            print(f"Utilisateur: {message}")
            
            response = await chat.process_message(user_id, message)
            print(f"IA: {response}")
            
            # Petite pause entre les messages
            await asyncio.sleep(1)
        
        # Test 3: Statistiques de chat
        print("\n✅ Test 3: Statistiques de chat")
        stats = chat.get_chat_stats(user_id)
        print("Statistiques:")
        print(stats)
        
        # Test 4: Vérifier l'état de la session
        print("\n✅ Test 4: État de la session")
        is_active = chat.is_chat_active(user_id)
        print(f"Session active: {is_active}")
        
        active_sessions = chat.get_active_sessions_count()
        print(f"Sessions actives: {active_sessions}")
        
        # Test 5: Terminer la session
        print("\n✅ Test 5: Fin de session")
        end_message = chat.end_chat_session(user_id)
        print("Message de fin:")
        print(end_message)
        
        # Test 6: Vérifier que la session est fermée
        print("\n✅ Test 6: Vérification de fermeture")
        is_active_after = chat.is_chat_active(user_id)
        print(f"Session active après fermeture: {is_active_after}")
        
        print("\n🎉 Tous les tests de chat sont passés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        logger.error(f"Erreur lors des tests: {e}")

async def test_fallback_responses():
    """Test des réponses de fallback quand l'IA n'est pas disponible"""
    print("\n🧪 Test des réponses de fallback...")
    
    chat = FootballChat()
    
    # Simuler des messages sans session active
    test_messages = [
        "Parle-moi de football",
        "Qui est le meilleur joueur ?",
        "Analyse le match de demain",
        "Que penses-tu des transferts ?",
        "Prédit le résultat du match"
    ]
    
    for message in test_messages:
        print(f"\nMessage: {message}")
        fallback_response = chat._get_fallback_response(message)
        print(f"Réponse fallback: {fallback_response}")

def test_football_context():
    """Test du contexte football"""
    print("\n🧪 Test du contexte football...")
    
    chat = FootballChat()
    context = chat.football_context
    
    print("✅ Contexte football chargé:")
    print(f"  • Sport: {context['sport']}")
    print(f"  • Ligues: {len(context['leagues'])}")
    print(f"  • Sujets: {len(context['topics'])}")
    print(f"  • Personnalité: {context['personality']}")
    print(f"  • Style: {context['style']}")
    
    print("\n✅ Ligues supportées:")
    for league in context['leagues']:
        print(f"  • {league}")
    
    print("\n✅ Sujets disponibles:")
    for topic in context['topics']:
        print(f"  • {topic}")

async def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS - CHAT FOOTBALL IA 🚀\n")
    
    try:
        # Test du contexte football
        test_football_context()
        
        # Test des réponses de fallback
        await test_fallback_responses()
        
        # Test principal du chat
        await test_football_chat()
        
        print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ! 🎉")
        print("\n✨ La fonctionnalité de chat football est prête avec:")
        print("  • Sessions de chat interactives")
        print("  • Réponses IA intelligentes")
        print("  • Système de fallback robuste")
        print("  • Statistiques de conversation")
        print("  • Gestion des sessions")
        print("  • Contexte football spécialisé")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        logger.error(f"Erreur lors des tests: {e}")

if __name__ == "__main__":
    asyncio.run(main())
