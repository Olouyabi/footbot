# ⚽ FootStat Analyzer - Bot Telegram d'Analyse de Matchs de Football

Un bot Telegram intelligent qui analyse les matchs de football et fournit des prédictions détaillées basées sur les statistiques récentes des équipes.

## 🚀 Fonctionnalités

- **Analyse automatique** de matchs de football
- **Probabilités estimées** (victoire, nul, défaite, +2.5 buts)
- **Analyse de forme récente** des équipes
- **Performances à domicile/extérieur**
- **Niveau de risque** (faible, moyen, élevé)
- **Mode IA optionnel** pour des analyses plus humaines
- **Interface Telegram intuitive** avec boutons interactifs

## 📋 Prérequis

- Python 3.12.9
- Token de bot Telegram
- Clé API Football-Data.org
- Clé API OpenAI (optionnel, pour le mode IA)

## 🛠️ Installation

1. **Cloner le projet** (si applicable) ou utiliser les fichiers fournis

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement** :
   - Copiez le fichier `.env.example` vers `.env`
   - Remplissez les valeurs suivantes :
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   FOOTBALL_API_KEY=your_football_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🔧 Configuration

### Obtenir un Token Telegram Bot

1. Contactez [@BotFather](https://t.me/botfather) sur Telegram
2. Utilisez la commande `/newbot`
3. Suivez les instructions pour créer votre bot
4. Copiez le token fourni dans votre fichier `.env`

### Obtenir une Clé API Football

1. Visitez [Football-Data.org](https://www.football-data.org/)
2. Créez un compte gratuit
3. Générez une clé API
4. Copiez la clé dans votre fichier `.env`

### Obtenir une Clé API OpenAI (Optionnel)

1. Visitez [OpenAI Platform](https://platform.openai.com/)
2. Créez un compte et ajoutez des crédits
3. Générez une clé API
4. Copiez la clé dans votre fichier `.env`

## 🚀 Démarrage

```bash
python main.py
```

Le bot devrait démarrer et afficher :
```
🚀 Démarrage du bot FootStat Analyzer...
✅ Bot FootStat Analyzer démarré avec succès !
📊 Mode IA: Activé/Désactivé
⚽ API Football: https://api.football-data.org/v4
🔄 Démarrage du polling...
```

## 📱 Utilisation

### Commandes Disponibles

- `/start` - Démarrer le bot et voir les instructions
- `/help` - Aide détaillée
- `/analyze` - Analyser des matchs spécifiques
- `/ai_mode` - Activer/désactiver le mode IA

### Format des Matchs

Envoyez vos matchs au format :
```
Real Madrid vs Barcelona
Liverpool vs Chelsea
PSG vs Marseille
```

Ou utilisez la commande :
```
/analyze Real Madrid vs Barcelona
```

### Exemples d'Utilisation

1. **Analyse simple** :
   ```
   Real Madrid vs Barcelona
   ```

2. **Analyse multiple** :
   ```
   Real Madrid vs Barcelona
   Liverpool vs Chelsea
   PSG vs Marseille
   ```

3. **Activer le mode IA** :
   ```
   /ai_mode on
   ```

## 🏗️ Architecture du Code

```
footbot/
├── main.py              # Point d'entrée principal
├── config.py            # Configuration et messages
├── handlers.py           # Gestionnaires Telegram
├── analyzer.py          # Logique d'analyse des matchs
├── api_client.py        # Client API Football-Data.org
├── ai_module.py         # Module IA (OpenAI)
├── requirements.txt     # Dépendances Python
├── .env                 # Variables d'environnement
└── README.md           # Documentation
```

### Description des Modules

- **`main.py`** : Point d'entrée, initialise le bot Telegram
- **`config.py`** : Configuration centralisée et messages du bot
- **`handlers.py`** : Gestion des commandes et messages Telegram
- **`analyzer.py`** : Logique d'analyse et calcul des probabilités
- **`api_client.py`** : Interface avec l'API Football-Data.org
- **`ai_module.py`** : Intégration OpenAI pour analyses améliorées

## 📊 Types d'Analyses

### Probabilités Calculées

- **Victoire équipe à domicile**
- **Victoire équipe visiteuse**
- **Match nul**
- **Plus de 2.5 buts**
- **Moins de 2.5 buts**

### Facteurs d'Analyse

- **Forme récente** (5 derniers matchs)
- **Moyenne de buts marqués/encaissés**
- **Performances à domicile/extérieur**
- **Taux de victoire**
- **Consistance des résultats**

### Niveaux de Risque

- 🟢 **Faible** : Match prévisible
- 🟡 **Moyen** : Match équilibré
- 🔴 **Élevé** : Match imprévisible

## 🤖 Mode IA

Le mode IA utilise OpenAI GPT-3.5-turbo pour :

- **Améliorer les analyses** avec un langage plus humain
- **Ajouter des insights tactiques** et psychologiques
- **Générer des prédictions détaillées** avec scores probables
- **Créer des résumés** de plusieurs analyses

### Activation du Mode IA

```bash
/ai_mode on
```

## 🔧 Configuration Avancée

### Variables d'Environnement

```env
# Obligatoires
TELEGRAM_BOT_TOKEN=your_token
FOOTBALL_API_KEY=your_api_key

# Optionnelles
OPENAI_API_KEY=your_openai_key
FOOTBALL_API_BASE_URL=https://api.football-data.org/v4
DEFAULT_LEAGUE=PL
ANALYSIS_MODE=standard
AI_MODE_ENABLED=false
```

### Personnalisation

Vous pouvez modifier :
- **Messages du bot** dans `config.py`
- **Logique d'analyse** dans `analyzer.py`
- **Seuils de probabilité** dans `analyzer.py`
- **Prompts IA** dans `ai_module.py`

## 🐛 Dépannage

### Erreurs Communes

1. **Token Telegram invalide** :
   ```
   ❌ Token Telegram manquant !
   ```
   → Vérifiez votre token dans `.env`

2. **Clé API Football manquante** :
   ```
   ❌ Clé API Football manquante !
   ```
   → Obtenez une clé sur Football-Data.org

3. **Équipe non trouvée** :
   ```
   ❌ Équipe "Nom Équipe" non trouvée
   ```
   → Utilisez le nom exact de l'équipe

4. **Rate limit API** :
   ```
   Rate limit atteint, attente de 60 secondes...
   ```
   → Le bot attend automatiquement

### Logs

Les logs sont affichés dans la console :
```
2024-01-15 10:30:00 - INFO - Bot FootStat Analyzer démarré avec succès !
2024-01-15 10:30:01 - INFO - Utilisateur 123456 a démarré le bot
```

## 📈 Améliorations Futures

- [ ] Support de plus d'APIs football
- [ ] Analyse de joueurs individuels
- [ ] Prédictions de scores exacts
- [ ] Intégration de données en temps réel
- [ ] Interface web complémentaire
- [ ] Base de données pour l'historique

## 📄 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📞 Support

Pour toute question ou problème :
1. Vérifiez la section Dépannage
2. Consultez les logs d'erreur
3. Vérifiez votre configuration `.env`

---

**FootStat Analyzer** - Votre assistant intelligent pour l'analyse de matchs de football ! ⚽
