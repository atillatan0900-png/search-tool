"""Multi-language support for search tool"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LanguageManager:
    """Multi-language support"""
    
    SUPPORTED_LANGUAGES = {
        'tr': 'Türkçe',
        'en': 'English',
        'de': 'Deutsch',
        'fr': 'Français',
        'es': 'Español',
    }
    
    TRANSLATIONS = {
        'en': {
            'app_name': 'DDGS Advanced File Search',
            'welcome': 'Welcome to DDGS Advanced File Search',
            'search': 'Search',
            'results': 'Results',
            'invalid_input': 'Invalid input',
            'error': 'Error',
            'success': 'Success',
            'loading': 'Loading...',
            'no_results': 'No results found',
            'search_prompt': 'What would you like to search for?',
            'file_types': 'File Types',
            'export_options': 'Export Options',
            'link_check': 'Check Links',
            'statistics': 'Statistics',
            'active': 'Active',
            'broken': 'Broken',
            'timeout': 'Timeout',
            'total_links': 'Total Links',
            'total_searches': 'Total Searches',
            'favorites': 'Favorites',
            'settings': 'Settings',
            'exit': 'Exit',
        },
        'tr': {
            'app_name': 'DDGS Gelişmiş Dosya Arama',
            'welcome': 'DDGS Gelişmiş Dosya Arama\'ya hoş geldiniz',
            'search': 'Ara',
            'results': 'Sonuçlar',
            'invalid_input': 'Geçersiz giriş',
            'error': 'Hata',
            'success': 'Başarılı',
            'loading': 'Yükleniyor...',
            'no_results': 'Sonuç bulunamadı',
            'search_prompt': 'Ne aramak istersiniz?',
            'file_types': 'Dosya Türleri',
            'export_options': 'Dışa Aktarma Seçenekleri',
            'link_check': 'Linkleri Kontrol Et',
            'statistics': 'İstatistikler',
            'active': 'Aktif',
            'broken': 'Bozuk',
            'timeout': 'Zaman Aşımı',
            'total_links': 'Toplam Linkler',
            'total_searches': 'Toplam Aramalar',
            'favorites': 'Favoriler',
            'settings': 'Ayarlar',
            'exit': 'Çıkış',
        },
        'de': {
            'app_name': 'DDGS Erweiterte Dateisuche',
            'welcome': 'Willkommen bei DDGS Erweiterte Dateisuche',
            'search': 'Suche',
            'results': 'Ergebnisse',
            'invalid_input': 'Ungültige Eingabe',
            'error': 'Fehler',
            'success': 'Erfolg',
            'loading': 'Wird geladen...',
            'no_results': 'Keine Ergebnisse gefunden',
            'search_prompt': 'Was möchten Sie suchen?',
            'file_types': 'Dateitypen',
            'export_options': 'Exportoptionen',
            'link_check': 'Links überprüfen',
            'statistics': 'Statistik',
            'active': 'Aktiv',
            'broken': 'Defekt',
            'timeout': 'Zeitüberschreitung',
            'total_links': 'Gesamtlinks',
            'total_searches': 'Gesamtsuchvorgänge',
            'favorites': 'Favoriten',
            'settings': 'Einstellungen',
            'exit': 'Beenden',
        },
        'fr': {
            'app_name': 'Recherche de fichiers avancée DDGS',
            'welcome': 'Bienvenue dans la recherche de fichiers avancée DDGS',
            'search': 'Rechercher',
            'results': 'Résultats',
            'invalid_input': 'Entrée invalide',
            'error': 'Erreur',
            'success': 'Succès',
            'loading': 'Chargement...',
            'no_results': 'Aucun résultat trouvé',
            'search_prompt': 'Que souhaitez-vous chercher?',
            'file_types': 'Types de fichiers',
            'export_options': 'Options d\'exportation',
            'link_check': 'Vérifier les liens',
            'statistics': 'Statistiques',
            'active': 'Actif',
            'broken': 'Cassé',
            'timeout': 'Délai d\'attente',
            'total_links': 'Liens totaux',
            'total_searches': 'Recherches totales',
            'favorites': 'Favoris',
            'settings': 'Paramètres',
            'exit': 'Quitter',
        },
        'es': {
            'app_name': 'Búsqueda avanzada de archivos DDGS',
            'welcome': 'Bienvenido a la búsqueda avanzada de archivos DDGS',
            'search': 'Buscar',
            'results': 'Resultados',
            'invalid_input': 'Entrada inválida',
            'error': 'Error',
            'success': 'Éxito',
            'loading': 'Cargando...',
            'no_results': 'No se encontraron resultados',
            'search_prompt': '¿Qué te gustaría buscar?',
            'file_types': 'Tipos de archivo',
            'export_options': 'Opciones de exportación',
            'link_check': 'Verificar enlaces',
            'statistics': 'Estadísticas',
            'active': 'Activo',
            'broken': 'Roto',
            'timeout': 'Tiempo de espera',
            'total_links': 'Enlaces totales',
            'total_searches': 'Búsquedas totales',
            'favorites': 'Favoritos',
            'settings': 'Configuración',
            'exit': 'Salir',
        }
    }
    
    def __init__(self, language: str = 'en'):
        self.current_language = language if language in self.SUPPORTED_LANGUAGES else 'en'
        logger.info(f"Language set to: {self.SUPPORTED_LANGUAGES[self.current_language]}")
    
    def set_language(self, language: str) -> bool:
        """Set current language"""
        if language not in self.SUPPORTED_LANGUAGES:
            logger.warning(f"Unsupported language: {language}")
            return False
        self.current_language = language
        logger.info(f"Language changed to: {self.SUPPORTED_LANGUAGES[language]}")
        return True
    
    def get(self, key: str, default: str = '') -> str:
        """Get translated string"""
        translations = self.TRANSLATIONS.get(self.current_language, {})
        return translations.get(key, default)
    
    def get_all_strings(self) -> Dict[str, str]:
        """Get all translations for current language"""
        return self.TRANSLATIONS.get(self.current_language, {})
    
    def get_language_name(self) -> str:
        """Get current language name"""
        return self.SUPPORTED_LANGUAGES.get(self.current_language, 'Unknown')
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()

# Global language instance
language_manager = LanguageManager()
