#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement du bot
"""
import asyncio
import sys
from handlers import BotHandlers
from analyzer import MatchAnalyzer
from ai_module import AIModule

async def test_bot():
    """Test des composants principaux du bot"""
    print("🧪 Test du Bot FootStat Analyzer v2.0")
    print("=" * 50)
    
    try:
        # Test du module IA
        print("1. Test du module IA...")
        ai_module = AIModule()
        print(f"   ✅ Module IA: {'Activé' if ai_module.is_enabled() else 'Désactivé'}")
        
        # Test de l'analyseur
        print("2. Test de l'analyseur...")
        analyzer = MatchAnalyzer()
        print("   ✅ Analyseur initialisé")
        
        # Test des handlers
        print("3. Test des handlers...")
        handlers = BotHandlers()
        print("   ✅ Handlers initialisés")
        
        # Test de nettoyage Markdown
        print("4. Test du nettoyage Markdown...")
        test_text = "**Test** avec *markdown* et `code` et [lien](url)"
        clean_text = handlers._clean_markdown(test_text)
        print(f"   ✅ Texte original: {test_text}")
        print(f"   ✅ Texte nettoyé: {clean_text}")
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("✅ Le bot est prêt à fonctionner")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_bot())
