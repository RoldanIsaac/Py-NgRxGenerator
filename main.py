import os
import re

def pluralize(word):
    """
    Generate the plural form of an English noun using improved linguistic rules.
    Handles:
    - Consonant + y  -> ies
    - Words ending in s, x, z, ch, sh -> es
    - Words ending in f / fe -> ves
    - Common irregular nouns
    - Default: +s
    """

    irregulars = {
        "person": "people",
        "man": "men",
        "woman": "women",
        "child": "children",
        "tooth": "teeth",
        "foot": "feet",
        "mouse": "mice",
        "goose": "geese",
        "ox": "oxen",
    }

    # Check irregulars (case-insensitive, but preserve original casing)
    lower = word.lower()
    if lower in irregulars:
        plural = irregulars[lower]
        # Restore original casing (Capitalized or Uppercase)
        if word.istitle():
            return plural.capitalize()
        if word.isupper():
            return plural.upper()
        return plural

    # Consonant + y → ies
    if word.endswith("y") and len(word) > 1 and word[-2].lower() not in "aeiou":
        return word[:-1] + "ies"

    # Words ending in s, x, z, ch, sh → es
    if re.search(r"(s|x|z|ch|sh)$", word):
        return word + "es"

    # Words ending in f → ves (e.g., wolf → wolves)
    if word.endswith("f"):
        return word[:-1] + "ves"

    # Words ending in fe → ves (e.g., knife → knives)
    if word.endswith("fe"):
        return word[:-2] + "ves"

    # Default: add s
    return word + "s"


def capitalize(word):
    """
    Capitalize the first letter of a word, preserving the rest.
    Returns the word unchanged if empty.
    """
    return word[0].upper() + word[1:] if word else word

def camel_case_replace(text, original, replacement):
    """
    Replace occurrences of `original` inside camelCase or PascalCase identifiers.
    - Matches words containing the original term
    - Replaces only the matching substring while maintaining case formatting
    - Useful for renaming TypeScript variables such as rideCount → userCount
    """
    # Busca ocurrencias de original dentro de palabras y las reemplaza respetando mayúsculas
    pattern = re.compile(r'\b\w*' + re.escape(original) + r'\w*\b', re.IGNORECASE)

    def replacer(match):
        word = match.group(0)
        idx = word.lower().find(original.lower())
        if idx == -1:
            return word
        before = word[:idx]
        after = word[idx + len(original):]
        new_middle = capitalize(replacement)
        return before + new_middle + after

    return pattern.sub(replacer, text)

def replace_all_variants(text, original, replacement):
    """
    Replace all relevant variants of the original term:
    - Lowercase, uppercase, capitalized
    - Singular and plural forms
    - Handles full-word replacements
    - Also processes camelCase and PascalCase embedded replacements
    """
    variants = {
        original: replacement,
        original.lower(): replacement.lower(),
        original.upper(): replacement.upper(),
        capitalize(original): capitalize(replacement),

        pluralize(original): pluralize(replacement),
        pluralize(original).lower(): pluralize(replacement).lower(),
        pluralize(original).upper(): pluralize(replacement).upper(),
        capitalize(pluralize(original)): capitalize(pluralize(replacement)),
    }

    for orig, repl in sorted(variants.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(rf'\b{re.escape(orig)}\b')
        text = pattern.sub(repl, text)

    # Reemplazos dentro de identificadores camelCase o PascalCase
    text = camel_case_replace(text, original, replacement)
    text = camel_case_replace(text, pluralize(original), pluralize(replacement))

    return text

def replace_filename(filename, original, replacement):
    """
    Replace occurrences of the original term inside filenames.
    This applies case variations and plural forms, but does NOT require
    whole-word matches since filenames often combine words.
    """
    variants = [
        (original, replacement),
        (original.lower(), replacement.lower()),
        (capitalize(original), capitalize(replacement)),
        (pluralize(original), pluralize(replacement)),
        (pluralize(original).lower(), pluralize(replacement).lower()),
        (capitalize(pluralize(original)), capitalize(pluralize(replacement))),
    ]
    new_name = filename
    for orig, repl in variants:
        new_name = re.sub(rf'{re.escape(orig)}', repl, new_name, flags=re.IGNORECASE)
    return new_name

def process_folder(folder_path, original_term, replacement_term, dry_run=True):
    """
    Process all .ts files inside a folder:
    - Reads each file
    - Applies text replacements
    - Writes updated files into an output directory
    - Output folder is placed OUTSIDE the source folder to avoid recursive processing
    - If dry_run=True, changes are printed but not written
    """
    if not os.path.isdir(folder_path):
        print(f"❌ Carpeta no encontrada: {folder_path}")
        return
    
    # Mover output fuera de la carpeta procesada
    output_folder = os.path.abspath(f"{folder_path}_output_{replacement_term}")

   
    if not dry_run:
        os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        # Evitar que os.walk procese carpetas de salida
        dirs[:] = [d for d in dirs if not d.startswith("_output_")]

        for filename in files:
            if filename.endswith(".ts"):
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                updated_content = replace_all_variants(content, original_term, replacement_term)
                new_filename = replace_filename(filename, original_term, replacement_term)

                rel_path = os.path.relpath(root, folder_path)
                target_folder = os.path.join(output_folder, rel_path)
                output_path = os.path.join(target_folder, new_filename)

                if dry_run:
                    print(f"🔍 DRY RUN: {filename} → {new_filename}")
                    if content != updated_content:
                        print(f" - Cambios detectados en contenido")
                else:
                    os.makedirs(target_folder, exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"✅ {filename} → {new_filename}")

    if not dry_run:
        print(f"\n📁 All files saved in: {output_folder}")
    else:
        print(f"\n🔎 Dry-run completed — None of the files were modified.")

if __name__ == "__main__":
    print("=== NGRX Factory ===\n")
    print(" Replace")
    print(" Output: New ngrx store generated with: ")
    print(" 1. Reducer")
    print(" 2. Selectors")
    print(" 3. Models")
    print(" 4. Effects")
    print(" 5. Actions")
    print("===              ===\n")

    # folder = input("Ruta de la carpeta con archivos .ts: ").strip()
    folder = 'store'
    # original = input("Término original (singular, ej: ride): ").strip()
    original = 'ride'
    replacement = input("Name of the new entity (singular, ej: controlLoop): ").strip()

    dry_run_input = input("Dry-run (Simulation)? (s/n): ").strip().lower()
    dry_run = dry_run_input == 's'

    process_folder(folder, original, replacement, dry_run=dry_run)
