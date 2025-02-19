import os
import gettext
from typing import Optional

# Set up the translations directory
LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')

def setup_translations(language: str = 'pt_BR') -> gettext.NullTranslations:
    """
    Set up translations for the given language.
    
    Args:
        language (str): Language code (e.g., 'pt_BR', 'en_US')
        
    Returns:
        gettext.NullTranslations: Translation object
    """
    try:
        translation = gettext.translation(
            'messages',
            localedir=LOCALE_DIR,
            languages=[language],
            fallback=True
        )
        return translation
    except FileNotFoundError:
        return gettext.NullTranslations()

# Global translation function
_ = gettext.gettext  # Initialize with default gettext

def set_language(language: str) -> None:
    """
    Set the application language.
    
    Args:
        language (str): Language code (e.g., 'pt_BR', 'en_US')
    """
    global _
    translation = setup_translations(language)
    translation.install()
    _ = translation.gettext 