#!/usr/bin/env python3
"""
Test simple de l'analyse de matchs
"""
import logging
from analyzer import MatchAnalyzer

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_analysis():
    """Test de l'analyse de matchs"""
    print("🧪 Test de l'analyse de matchs")
    print("=" * 40)
    
    try:
        # Créer l'analyseur
        analyzer = MatchAnalyzer()
        print("✅ Analyseur créé")
        
        # Test avec Real Madrid vs Barcelona
        print("\n⚽ Test: Real Madrid vs Barcelona")
        analysis = analyzer.analyze_match("Real Madrid", "Barcelona")
        
        if 'error' in analysis:
            print(f"❌ Erreur: {analysis['error']}")
        else:
            print("✅ Analyse réussie!")
            print(f"   Match: {analysis.get('match', 'N/A')}")
            print(f"   Équipe 1: {analysis.get('team1', {}).get('name', 'N/A')}")
            print(f"   Équipe 2: {analysis.get('team2', {}).get('name', 'N/A')}")
        
        # Test avec Liverpool vs Chelsea
        print("\n⚽ Test: Liverpool vs Chelsea")
        analysis2 = analyzer.analyze_match("Liverpool", "Chelsea")
        
        if 'error' in analysis2:
            print(f"❌ Erreur: {analysis2['error']}")
        else:
            print("✅ Analyse réussie!")
            print(f"   Match: {analysis2.get('match', 'N/A')}")
            print(f"   Équipe 1: {analysis2.get('team1', {}).get('name', 'N/A')}")
            print(f"   Équipe 2: {analysis2.get('team2', {}).get('name', 'N/A')}")
        
        print("\n🎉 Tests terminés!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis()
