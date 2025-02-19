#!/usr/bin/env python3
import os
import subprocess

def compile_translations():
    """Compile all translation files in the locale directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')
    
    for lang in ['pt_BR', 'en_US']:
        po_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            print(f"Compiling translations for {lang}...")
            try:
                subprocess.run(['msgfmt', po_file, '-o', mo_file], check=True)
                print(f"Successfully compiled {lang} translations")
            except subprocess.CalledProcessError as e:
                print(f"Error compiling {lang} translations: {e}")
            except FileNotFoundError:
                print("Error: msgfmt not found. Please install gettext.")
        else:
            print(f"Warning: Translation file not found for {lang}")

if __name__ == '__main__':
    compile_translations() 