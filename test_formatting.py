#!/usr/bin/env python3
"""
Test du nouveau formatage des analyses
"""
import logging
from analyzer import MatchAnalyzer

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_formatting():
    """Test du nouveau formatage"""
    print("🎨 Test du nouveau formatage des analyses")
    print("=" * 50)
    
    try:
        # Créer l'analyseur
        analyzer = MatchAnalyzer()
        print("✅ Analyseur créé")
        
        # Test avec Real Madrid vs Barcelona
        print("\n" + "="*60)
        print("⚽ TEST: Real Madrid vs Barcelona")
        print("="*60)
        
        analysis = analyzer.analyze_match("Real Madrid", "Barcelona")
        
        if 'error' in analysis:
            print(f"❌ Erreur: {analysis['error']}")
        else:
            print("✅ Analyse réussie!")
            print("\n📊 RÉSULTAT FORMATÉ:")
            print("-" * 60)
            print(analysis.get('analysis', {}).get('analysis_text', 'N/A'))
            print("-" * 60)
        
        # Test avec Liverpool vs Chelsea
        print("\n" + "="*60)
        print("⚽ TEST: Liverpool vs Chelsea")
        print("="*60)
        
        analysis2 = analyzer.analyze_match("Liverpool", "Chelsea")
        
        if 'error' in analysis2:
            print(f"❌ Erreur: {analysis2['error']}")
        else:
            print("✅ Analyse réussie!")
            print("\n📊 RÉSULTAT FORMATÉ:")
            print("-" * 60)
            print(analysis2.get('analysis', {}).get('analysis_text', 'N/A'))
            print("-" * 60)
        
        print("\n🎉 Tests de formatage terminés!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_formatting()
