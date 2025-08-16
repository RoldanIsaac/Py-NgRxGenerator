import os
import re

def pluralize(word):
    if word.endswith('y') and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    elif word.endswith('s'):
        return word + 'es'
    else:
        return word + 's'

def capitalize(word):
    return word[0].upper() + word[1:] if word else word

def camel_case_replace(text, original, replacement):
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
    if not os.path.isdir(folder_path):
        print(f"❌ Carpeta no encontrada: {folder_path}")
        return

    output_folder = os.path.join(folder_path, f"_output_{replacement_term}")
    if not dry_run:
        os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(folder_path):
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
        print(f"\n📁 Todos los archivos fueron guardados en: {output_folder}")
    else:
        print(f"\n🔎 Dry-run completado — No se modificó ningún archivo.")

if __name__ == "__main__":
    print("=== NGRX Factory ===\n")
    print(" Reemplazo de contenido y nombres de archivos")
    print(" Salida: Nueva entidad NGRX generada con: ")
    print(" 1. Reducer   2. Selectors    3. Models   4.Effects   5. Actions \n")
    print("===              ===\n")

    # folder = input("Ruta de la carpeta con archivos .ts: ").strip()
    folder = 'store'
    # original = input("Término original (singular, ej: ride): ").strip()
    original = 'ride'
    replacement = input("Nuevo término (singular, ej: controlLoop): ").strip()

    dry_run_input = input("¿Quieres hacer dry-run (simulación)? (s/n): ").strip().lower()
    dry_run = dry_run_input == 's'

    process_folder(folder, original, replacement, dry_run=dry_run)
