"""
Configuration avancée pour FootStat Analyzer v2.0
Contient les paramètres avancés pour le cache, la pagination, et les fonctionnalités
"""
import os
from typing import Dict, Any

class AdvancedConfig:
    """Configuration avancée du bot"""
    
    # === CACHE CONFIGURATION ===
    CACHE_SETTINGS = {
        'root_dirs': {
            'football_api': 'cache/football_api',
            'user_data': 'cache/user_data',
            'temp': 'cache/temp'
        },
        'ttl_settings': {
            'team_data': 3600,      # 1 heure
            'match_data': 1800,     # 30 minutes
            'league_data': 7200,     # 2 heures
            'user_settings': 86400, # 24 heures
            'analysis_results': 300  # 5 minutes
        },
        'memory_settings': {
            'max_entries': 1000,
            'cleanup_interval': 300,  # 5 minutes
            'auto_cleanup': True
        }
    }
    
    # === PAGINATION CONFIGURATION ===
    PAGINATION_SETTINGS = {
        'default_items_per_page': 3,
        'max_items_per_page': 10,
        'navigation_buttons': {
            'prev_text': '◀️ Précédent',
            'next_text': 'Suivant ▶️',
            'page_info_format': '📄 Page {current}/{total}',
            'show_page_info': True,
            'show_item_range': True
        }
    }
    
    # === LEAGUE CONFIGURATION ===
    LEAGUE_SETTINGS = {
        'supported_leagues': ['PL', 'PD', 'SA', 'BL1', 'FL1', 'PPL', 'CL', 'EL'],
        'default_league': 'PL',
        'league_display_format': '{code} - {name} ({country})',
        'season_format': {
            'start_month': 8,  # Août
            'year_offset': 0   # Année courante
        }
    }
    
    # === USER INTERFACE CONFIGURATION ===
    UI_SETTINGS = {
        'buttons_per_row': 2,
        'max_message_length': 4096,
        'markdown_mode': 'Markdown',
        'emoji_enabled': True,
        'progress_indicators': True,
        'confirmation_dialogs': True
    }
    
    # === POUR RIOR CONFIGURATION ===
    ERROR_HANDLING = {
        'max_retries': 3,
        'retry_delay': 5,  # secondes
        'fallback_messages': True,
        'detailed_logging': True,
        'user_friendly_errors': True,
        'error_codes': {
            'API_UNAVAILABLE': 'Service temporairement indisponible',
            'INVALID_TEAM': 'Équipe non trouvée',
            'RATE_LIMIT': 'Limite de requêtes atteinte',
            'NETWORK_ERROR': 'Problème de connexion',
            'PARSE_ERROR': 'Erreur de traitement des données',
            'CACHE_ERROR': 'Problème de cache',
            'UNKNOWN_ERROR': 'Erreur inconnue'
        }
    }
    
    # === PERFORMANCE CONFIGURATION ===
    PERFORMANCE_SETTINGS = {
        'api_timeout': 10,  # secondes
        'cache_timeout': 5,  # secondes
        'max_concurrent_requests': 5,
        'rate_limiting': {
            'requests_per_minute': 50,
            'burst_limit': 10
        }
    }
    
    # === DEBUGGING CONFIGURATION ===
    DEBUG_SETTINGS = {
        'enable_debug_logs': os.getenv('DEBUG_LOGS', 'false').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'save_api_responses': False,
        'performance_metrics': True,
        'cache_statistics': True
    }
    
    @classmethod
    def get_cache_dir(cls, cache_type: str) -> str:
        """Retourne le dossier de cache pour un type donné"""
        return cls.CACHE_SETTINGS['root_dirs'].get(cache_type, 'cache/default')
    
    @classmethod
    def get_cache_ttl(cls, data_type: str) -> int:
        """Retourne le TTL pour un type de données"""
        return cls.CACHE_SETTINGS['ttl_settings'].get(data_type, 300)
    
    @classmethod
    def get_error_message(cls, error_code: str) -> str:
        """Retourne le message d'erreur pour un code donné"""
        return cls.ERROR_HANDLING['error_codes'].get(error_code, 'Erreur inconnue')
    
    @classmethod
    def is_debug_enabled(cls) -> bool:
        """Vérifie si le debug est activé"""
        return cls.DEBUG_SETTINGS['enable_debug_logs']
    
    @classmethod
    def get_pagination_config(cls) -> Dict[str, Any]:
        """Retourne la configuration de pagination"""
        return cls.PAGINATION_SETTINGS.copy()
    
    @classmethod
    def get_ui_config(cls) -> Dict[str, Any]:
        """Retourne la configuration de l'interface utilisateur"""
        return cls.UI_SETTINGS.copy()
    
    @classmethod
    def validate_league(cls, league_code: str) -> bool:
        """Valider un code de ligue"""
        return league_code.upper() in cls.LEAGUE_SETTINGS['supported_leagues']
    
    @classmethod
    def get_performance_config(cls) -> Dict[str, Any]:
        """Retourne la configuration de performance"""
        return cls.PERFORMANCE_SETTINGS.copy()

class DatabaseConfig:
    """Configuration pour une future base de données"""
    
    DB_SETTINGS = {
        'provider': 'sqlite',  # sqlite, postgresql, mysql
        'connection_string': 'footstat.db',
        'tables': {
            'users': 'user_settings',
            'matches': 'match_history',
            'cache': 'cache_metadata',
            'statistics': 'performance_stats'
        },
        'backup_settings': {
            'enabled': True,
            'interval': 'daily',
            'retention_days': 30
        }
    }

class SecurityConfig:
    """Configuration de sécurité"""
    
    SECURITY_SETTINGS = {
        'rate_limiting': {
            'per_user': 10,      # requêtes par minute par utilisateur
            'global': 100,       # requêtes par minute globales
            'burst_factor': 2    # facteur d'éclatement
        },
        'data_validation': {
            'max_team_name_length': 100,
            'max_match_count': 20,
            'input_sanitization': True
        },
        'api_security': {
            'key_rotation': False,
            'request_signing': 'auto',
            'encryption': False
        }
    }
    
    @classmethod
    def get_rate_limits(cls) -> Dict[str, int]:
        """Retourne les limites de taux"""
        return cls.SECURITY_SETTINGS['rate_limiting']

class IntegrationConfig:
    """Configuration pour les intégrations tierces"""
    
    INTEGRATION_SETTINGS = {
        'external_apis': {
            'football_data': {
                'base_url': 'https://api.football-data.org/v4',
                'timeout': 10,
                'retry_count': 3,
                'caching': True
            },
            'openai': {
                'model': 'gpt-3.5-turbo',
                'max_tokens': 500,
                'temperature': 0.7,
                'timeout': 30
            }
        },
        'webhooks': {
            'enabled': False,
            'endpoint': '/webhook',
            'secret_token': None,
            'verify_signature': True
        }
    }

# Configuration exportée par défaut
def get_advanced_config() -> Dict[str, Any]:
    """Retourne toute la configuration avancée"""
    return {
        'cache': AdvancedConfig.CACHE_SETTINGS,
        'pagination': AdvancedConfig.PAGINATION_SETTINGS,
        'league': AdvancedConfig.LEAGUE_SETTINGS,
        'ui': AdvancedConfig.UI_SETTINGS,
        'error': AdvancedConfig.ERROR_HANDLING,
        'performance': AdvancedConfig.PERFORMANCE_SETTINGS,
        'debug': AdvancedConfig.DEBUG_SETTINGS,
        'database': DatabaseConfig.DB_SETTINGS,
        'security': SecurityConfig.SECURITY_SETTINGS,
        'integration': IntegrationConfig.INTEGRATION_SETTINGS
    }

# Validation de la configuration
def validate_config() -> list[str]:
    """Valide la configuration et retourne les erreurs"""
    errors = []
    
    # Vérification des chemins de cache
    for dir_type, dir_path in AdvancedConfig.CACHE_SETTINGS['root_dirs'].items():
        if not dir_path or len(dir_path) < 3:
            errors.append(f"Chemin de cache invalide pour {dir_type}: {dir_path}")
    
    # Vérification des TTL
    for data_type, ttl in AdvancedConfig.CACHE_SETTINGS['ttl_settings'].items():
        if not isinstance(ttl, int) or ttl < 0:
            errors.append(f"TTL invalide pour {data_type}: {ttl}")
    
    # Vérification des ligues
    if not AdvancedConfig.LEAGUE_SETTINGS['supported_leagues']:
        errors.append("Aucune ligue supportée configurée")
    
    return errors

if __name__ == '__main__':
    # Print la configuration complète
    import json
    import sys
    import os
    
    # Configurer l'encodage pour Windows
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    config = get_advanced_config()
    print("Configuration avancée FootStat Analyzer v2.0:")
    print("=" * 50)
    
    for section_name, section_config in config.items():
        print(f"\n📋 {section_name.upper()}:")
        print(json.dumps(section_config, indent=2, ensure_ascii=False))
    
    # Valider la configuration
    errors = validate_config()
    print(f"\n{'=' * 50}")
    if errors:
        print(f"❌ Erreurs de configuration trouvées:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ Configuration valide")
