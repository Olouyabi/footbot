# 🚀 Fonctionnalités Avancées - FootStat Analyzer

Ce document détaille les nouvelles fonctionnalités ajoutées au bot FootStat Analyzer.

## 📦 Nouvelles Fonctionnalités

### 🗄️ Système de Cache
- **Cache en mémoire** pour les données fréquemment accessées
- **Cache fichier** pour la persistance des données
- **TTL configurable** (Time To Live) pour chaque entrée
- **Nettoyage automatique** des entrées expirées
- **Statistiques de cache** disponibles

### ⚠️ Gestion d'Erreurs Améliorée
- **Gestionnaire d'erreurs centralisé** avec codes d'erreur
- **Messages d'erreur contextuels** pour l'utilisateur
- **Logs détaillés** pour le debugging
- **Récupération automatique** après rate limiting
- **Fallback gracieux** en cas d'erreur API

### 📄 Pagination
- **Navigation entre pages** avec boutons Précédent/Suivant
- **Affichage par lots** (3 éléments par page par défaut)
- **Cache temporaire** pour les analyses en cours
- **Navigation contextuelle** avec callbacks
- **Indicateurs de progression** (Page X/Y)

### ⚙️ Commandes Avancées

#### `/analyze`
- **Interface interactive** avec boutons
- **Options ligne de commande**:
  - `--league PL` : Changer de ligue
  - `--ai on/off` : Activer/désactiver le mode IA
- **Affichage des paramètres** actuels
- **Aide contextuelle** intégrée

#### `/set_league`
- **8 ligues supportées** (PL, PD, SA, BL1, FL1, PPL, CL, EL)
- **Sélection interactive** par boutons
- **Information des ligues** (nom, pays, nombre d'équipes)
- **Validation** des codes de ligue

#### `/toggle_ia`
- **Basculement simple** du mode IA
- **Confirmation visuelle** du changement
- **Persistance** des préférences utilisateur

#### `/settings`
- **Interface graphique** des paramètres
- **Gestion des préférences** utilisateur
- **Statistiques de cache**
- **Vidage du cache** disponible

### 🏆 Gestionnaire de Ligues

```python
CLASS LeagueManager:
    - get_league_info(league_code) -> Dict
    - format_leagues_list() -> str
    - get_all_leagues() -> Dict
```

**Ligues supportées :**
- **PL** : Premier League (Angleterre, 20 équipes)
- **PD** : La Liga (Espagne, 20 équipes)  
- **SA** : Serie A (Italie, 20 équipes)
- **BL1** : Bundesliga (Allemagne, 18 équipes)
- **FL1** : Ligue 1 (France, 20 équipes)
- **PPL** : Primeira Liga (Portugal, 18 équipes)
- **CL** : Champions League (Europe, 32 équipes)
- **EL** : Europa League (Europe, 48 équipes)

## 🛠️ Architecture Technique

### Fichiers Ajoutés

#### `utils.py`
```python
class CacheManager:
    - get(key) -> Optional[Any]
    - set(key, value, ttl) -> bool
    - delete(key) -> bool
    - clear() -> bool
    - get_stats() -> Dict

class ErrorHandler:
    - handle_api_error(error, context) -> Dict
    - handle_parsing_error(error, context) -> Dict
    - get_fallback_message(error_code) -> str

class Paginator:
    - paginate(items, page) -> Dict
    - create_navigation_keyboard(data, prefix) -> List

class UserSettings:
    - get_user_settings(user_id) -> Dict
    - update_user_setting(user_id, key, value) -> bool
    - set_league(user_id, league) -> bool
    - toggle_ai_mode(user_id) -> bool

class LeagueManager:
    - get_league_info(league_code) -> Optional[Dict]
    - get_all_leagues() -> Dict
    - format_leagues_list() -> str
```

### Méthodes Ajoutées à `api_client.py`
- Intégration du **CacheManager** pour toutes les requêtes API
- **Gestion d'erreurs améliorée** avec `ErrorHandler`
- **Retry automatique** en cas de rate limiting
- **Logging détaillé** des requêtes et erreurs

### Méthodes Ajoutées à `handlers.py`
- **Navigation callback** pour la pagination
- **Paramètres utilisateur** persistants
- **Interface graphique** pour les settings
- **Gestion d'état** pour les analyses en cours

## 📊 Cache et Performance

### Configuration du Cache
```python
# Cache API Football
cache_dir: "cache/football_api"
default_ttl: 600 secondes (10 minutes)

# Cache utilisateur temporaire
user_cache: mémoire (durée de session)

# Cache paramètres utilisateur
user_settings_ttl: 86400 secondes (24h)
```

### Optimisations
- **Cache hierarchique** (mémoire → fichier → API)
- **Invalidation intelligente** selon le type de données
- **Compression** des données en cache
- **Indexation** pour accès rapide

## 🎯 Utilisation Avancée

### Exemples de Commandes

```bash
# Analyse avec changement de ligue
/analyze --league PD Real Madrid vs Barcelona

# Activation du mode IA inline
/analyze --ai on Liverpool vs Chelsea

# Récupération des paramètres
/settings

# Changement de ligue spécifique
/set_league BL1

# Basculement rapide du mode IA
/toggle_ia
```

### Interface Graphique

Le bot utilise maintenant des **boutons interactifs** pour :
- ✅ Navigation pagination
- ✅ Sélection de ligues
- ✅ Paramètres utilisateur
- ✅ Actions rapides (prédictions, détails)
- ✅ Aide contextuelle

## 🔧 Configuration Avancée

### Variables d'Environnement

```env
# Cache (nouvelles variables)
CACHE_DIR=cache
DEFAULT_CACHE_TTL=600
USER_CACHE_TTL=3600

# Pagination
ITEMS_PER_PAGE=3
MAX_PAGES_DISPLAY=10

# Ligues
DEFAULT_LEAGUE=PL
SUPPORTED_LEAGUES=PL,PD,SA,BL1,FL1,PPL,CL,EL

# Mode développement
DEBUG_CACHE=false
VERBOSE_LOGGING=true
```

### Personnalisation

Vous pouvez personnaliser :
- **TTL du cache** par type de données
- **Nombre d'éléments** par page
- **Messages d'erreur** personnalisés
- **Seuils de rate limiting**
- **Couleurs** de l'interface

## 🐛 Debugging

### Logs de Debug
```python
# Activer les logs détaillés
logging.getLogger().setLevel(logging.DEBUG)

# Logs spécifiques au cache
logger.debug(f"Cache hit: {key}")
logger.debug(f"Cache set: {key} (TTL: {ttl}s)")

# Logs d'erreur avec contexte
logger.error(f"API Error: {error_code} - {context}")
```

### Statistiques Disponibles
- 📊 **Entrées cache** (mémoire + fichier)
- ⏱️ **Temps d'exécution** des requêtes
- 🎯 **Taux de succès** des API calls
- 👥 **Sessions utilisateur** actives
- 💾 **Utilisation mémoire** du cache

## 📈 Métriques et Monitoring

### Indicateurs de Performance
- **Temps de réponse** moyen des analyses
- **Taux de cache hit** (efficacité du cache)
- **Erreurs API** par type
- **Utilisation des commandes** par fonctionnalité

### Alertes Configurables
- ⚠️ **Rate limit atteint** (> 90% utilisation)
- 🔴 **Erreurs API** (> 5% échec)
- 💾 **Cache plein** (> 80% utilisation mémoire)
- 👥 **Charge utilisateur** (> seuil configuré)

## 🚀 Déploiement

### Prérequis Supplémentaires
- **Espace disque** pour le cache (recommandé: 100MB)
- **RAM** pour le cache mémoire (recommandé: 256MB)
- **Permissions** d'écriture sur le dossier de cache

### Commandes de Maintenance
```bash
# Vider le cache manuellement
python -c "from utils import CacheManager; CacheManager().clear()"

# Statistiques du cache
python -c "from utils import CacheManager; print(CacheManager().get_stats())"

# Sauvegarde des paramètres utilisateur
python -c "from utils import UserSettings; print('Backup done')"
```

## 📚 Ressources

### Documentation Technique
- **Architecture** : Patterns de design utilisés
- **API Reference** : Toutes les méthodes disponibles
- **Configuration** : Options et paramètres
- **Troubleshooting** : Solutions aux problèmes courants

### Support
- 🔧 **Debugging** : Outils et techniques
- 📖 **Guides** : Tutoriels étape par étape
- 💬 **Communauté** : Entraide et échanges
- 🆘 **Support** : Assistance technique

---

*FootStat Analyzer v2.0* - Bot Telegram d'analyse de matchs de football avec fonctionnalités avancées ✨
