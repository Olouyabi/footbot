# 🔧 Guide de Configuration - FootStat Analyzer v2.0

## ⚠️ Problème Actuel : Configuration Manquante

Vous recevez l'erreur : `❌ Clé API Football manquante ! Veuillez configurer FOOTBALL_API_KEY dans le fichier .env`

## 🚀 Solution Rapide

### 1. Créer le fichier `.env`

Créez un fichier nommé `.env` à la racine de votre projet avec le contenu suivant :

```env
# Configuration du Bot Telegram FootStat Analyzer
TELEGRAM_BOT_TOKEN=votre_token_bot_ici
FOOTBALL_API_KEY=votre_cle_football_data_ici
FOOTBALL_API_BASE_URL=https://api.football-data.org/v4
OPENAI_API_KEY=votre_cle_openai_ici
DEFAULT_LEAGUE=PL
ANALYSIS_MODE=standard
AI_MODE_ENABLED=false
```

### 2. Obtenir les Clés API

#### 🤖 Token Telegram Bot (OBLIGATOIRE)

1. Ouvrez Telegram et cherchez [@BotFather](https://t.me/botfather)
2. Envoyez `/start`
3. Envoyez `/newbot`
4. Donnez un nom à votre bot (ex: "Mon FootStat Bot")
5. Donnez un username (ex: "mon_footstat_bot")
6. **Copiez le token** qui ressemble à : `123456789:ABCDEFGHJKLmnopqrstuvwxyz123456789`
7. Remplacez `votre_token_bot_ici` par ce token

#### ⚽ Clé Football Data (OBLIGATOIRE)

1. Allez sur [Football-Data.org](https://www.football-data.org/)
2. Cliquez sur "Sign Up" pour créer un compte gratuit
3. Connectez-vous et allez dans "API Access"
4. Générez une nouvelle clé API (elle ressemble à : `abc123def456ghi789`)
5. Remplacez `votre_cle_football_data_ici` par cette clé

#### 🧠 Clé OpenAI (OPTIONNEL)

Si vous voulez le mode IA amélioré :

1. Allez sur [OpenAI Platform](https://platform.openai.com/)
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Créez une nouvelle clé secrète
5. Remplacez `votre_cle_openai_ici` par cette clé

### 3. Configuration Minimale pour Démarrer

**Pour tester rapidement sans mode IA :**

```env
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHJKLmnopqrstuvwxyz123456789
FOOTBALL_API_KEY=abc123def456ghi789
FOOTBALL_API_BASE_URL=https://api.football-data.org/v4
AI_MODE_ENABLED=false
```

**Pour activer le mode IA :**

```env
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHJKLmnopqrstuvwxyz123456789
FOOTBALL_API_KEY=abc123def456ghi789
OPENAI_API_KEY=sk-abc123def456ghi789
FOOTBALL_API_BASE_URL=https://api.football-data.org/v4
AI_MODE_ENABLED=true
```

## 🛠️ Commande PowerShell pour Créer le Fichier

Dans votre terminal PowerShell, exécutez :

```powershell
# Créer le fichier .env avec votre token
echo "TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHJKLmnopqrstuvwxyz123456789" > .env
echo "FOOTBALL_API_KEY=abc123def456ghi789" >> .env
echo "FOOTBALL_API_BASE_URL=https://api.football-data.org/v4" >> .env
echo "AI_MODE_ENABLED=false" >> .env
```

**N'oubliez pas de remplacer les valeurs d'exemple par vos vraies clés !**

## ✅ Test de Configuration

Après avoir créé le fichier `.env`, lancez :

```bash
python main.py
```

Vous devriez voir :
```
✅ Bot FootStat Analyzer v2.0 démarré avec succès !
📊 Mode IA: Désactivé
⚽ API Football: https://api.football-data.org/v4
🗄️ Cache initialisé
🚀 Bot prêt à recevoir des commandes!
```

## 🔍 Vérification Rapide

Pour vérifier que vos clés fonctionnent :

```bash
python demo_advanced_features.py
```

## 📞 Support

Si vous avez encore des problèmes :

1. **Vérifiez que le fichier `.env` est bien dans le dossier racine**
2. **Vérifiez qu'il n'y a pas d'espaces autour du `=`**
3. **Vérifiez que vos clés API sont valides**
4. **Consultez les logs d'erreur pour plus de détails**

---

**Note importante :** Ne partagez jamais vos clés API publiquement !
