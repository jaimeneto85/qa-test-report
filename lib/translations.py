import os
import gettext
from typing import Optional

# Set up the translations directory
LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')

_translation = gettext.NullTranslations()

def setup_translations(language: str = 'pt_BR') -> gettext.NullTranslations:
    """
    Set up translations for the given language.
    
    Args:
        language (str): Language code (e.g., 'pt_BR', 'en_US')
        
    Returns:
        gettext.NullTranslations: Translation object
    """
    global _translation
    try:
        translation = gettext.translation(
            'messages',
            localedir=LOCALE_DIR,
            languages=[language],
            fallback=True
        )
        _translation = translation
    except FileNotFoundError:
        _translation = gettext.NullTranslations()

def set_language(language: str) -> None:
    """
    Set the application language.
    
    Args:
        language (str): Language code (e.g., 'pt_BR', 'en_US')
    """
    setup_translations(language)
    _translation.install()

def _(message: str) -> str:
    """
    Translation function.
    
    Args:
        message (str): The message to translate.
        
    Returns:
        str: Translated message.
    """
    return _translation.gettext(message)