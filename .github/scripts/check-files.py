#!/usr/bin/env python3
# =============================================================================
# check-files.py : contrôle des fichiers du dépôt selon docs/conventions.md.
#
# Lancé par .github/workflows/check-files.yml, mais aussi en local :
#     python3 .github/scripts/check-files.py names
#     python3 .github/scripts/check-files.py headers
#     python3 .github/scripts/check-files.py readmes
#
# Chaque contrôle lit la liste des fichiers suivis par Git (`git ls-files`) :
# un fichier ignoré (par exemple dans private/) n'est jamais contrôlé.
#
# Les erreurs sont écrites au format "::error file=…::message" : GitHub les
# affiche en rouge dans la PR, à côté du fichier concerné.
# =============================================================================

import re
import subprocess
import sys
import unicodedata

# -----------------------------------------------------------------------------
# Section 2 des conventions : noms de fichiers et de dossiers
# -----------------------------------------------------------------------------

# kebab-case en minuscules, sans accents : "risk-register.md",
# "2026-11-18-pricing-review", "check-pr.yml".
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)*$")

# Noms imposés par un outil (tableau « Exceptions » de la section 2).
FIXED_NAMES = {"README.md", "LICENSE", "CLAUDE.md", "AGENTS.md", "SKILL.md"}

# Dossiers dont le contenu suit le format de son outil.
TOOL_DIRS = (".github/", ".claude/")


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, text=True, check=True
    ).stdout
    return [f for f in out.split("\0") if f]


def error(path, message):
    print(f"::error file={path}::{message}")


def check_names(files):
    errors = 0
    for path in files:
        if path.startswith(TOOL_DIRS):
            continue
        for part in path.split("/"):
            # Fichiers de configuration cachés : .gitignore, .gitkeep…
            if part.startswith("."):
                continue
            if part in FIXED_NAMES:
                continue
            if not KEBAB.match(part):
                error(
                    path,
                    f"« {part} » n'est pas en kebab-case anglais "
                    "(minuscules, tirets, sans accents ni espaces). "
                    "Voir docs/conventions.md, section 2.",
                )
                errors += 1
                break
    return errors


# -----------------------------------------------------------------------------
# Section 3 des conventions : en-tête YAML des documents de référence
# -----------------------------------------------------------------------------

HEADER_FIELDS = ["titre", "statut", "mis-a-jour"]
STATUSES = {"brouillon", "valide", "obsolete"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def needs_header(path):
    # Documents de docs/, sauf les README.md.
    return (
        path.startswith("docs/")
        and path.endswith(".md")
        and not path.endswith("README.md")
    )


def check_header(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    if not lines or lines[0] != "---":
        return ["l'en-tête YAML est absent : la 1re ligne doit être « --- »"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ["l'en-tête YAML n'est pas fermé par une ligne « --- »"]

    fields = []
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        if not sep:
            return [f"ligne d'en-tête illisible : « {line} »"]
        fields.append((key.strip(), value.strip()))

    keys = [k for k, _ in fields]
    if keys != HEADER_FIELDS:
        return [
            f"champs attendus, dans cet ordre : {', '.join(HEADER_FIELDS)} "
            f"(trouvés : {', '.join(keys) or 'aucun'})"
        ]

    values = dict(fields)
    problems = []
    if not values["titre"]:
        problems.append("le champ « titre » est vide")
    if values["statut"] not in STATUSES:
        problems.append(
            f"statut « {values['statut']} » inconnu "
            f"(autorisés : {', '.join(sorted(STATUSES))})"
        )
    if not DATE.match(values["mis-a-jour"]):
        problems.append(
            f"date « {values['mis-a-jour']} » invalide (format AAAA-MM-JJ)"
        )
    return problems


def check_headers(files):
    errors = 0
    for path in filter(needs_header, files):
        for problem in check_header(path):
            error(path, f"{problem}. Voir docs/conventions.md, section 3.")
            errors += 1
    return errors


# -----------------------------------------------------------------------------
# Section 4 des conventions : émojis dans les titres des README.md
# -----------------------------------------------------------------------------


def count_emojis(text):
    # Un émoji est un « symbole autre » (catégorie Unicode So).
    # Les caractères invisibles qui les accompagnent (variante U+FE0F,
    # liaison U+200D) ne sont pas des symboles : ils ne sont pas comptés.
    # Un émoji composé avec U+200D (ex. 👨‍💻) compte pour un seul.
    count = 0
    previous = ""
    for char in text:
        if unicodedata.category(char) == "So" and previous != "‍":
            count += 1
        previous = char
    return count


def check_readme(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    problems = []
    in_code = False
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r"^(#{1,2}) (.*)$", line)
        if not match:
            continue
        title = match.group(2).strip()
        first = title[:1]
        if not first or unicodedata.category(first) != "So":
            problems.append((number, f"le titre « {line} » doit commencer par un émoji"))
        elif count_emojis(title) > 1:
            problems.append((number, f"le titre « {line} » contient plus d'un émoji"))
    return problems


def check_readmes(files):
    errors = 0
    for path in files:
        if path.split("/")[-1] != "README.md" or path.startswith(TOOL_DIRS):
            continue
        for number, problem in check_readme(path):
            print(
                f"::error file={path},line={number}::{problem}. "
                "Voir docs/conventions.md, section 4."
            )
            errors += 1
    return errors


# -----------------------------------------------------------------------------

CHECKS = {"names": check_names, "headers": check_headers, "readmes": check_readmes}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in CHECKS:
        print(f"usage : {sys.argv[0]} {'|'.join(CHECKS)}")
        return 2
    errors = CHECKS[sys.argv[1]](tracked_files())
    if errors:
        print(f"{errors} problème(s) trouvé(s).")
        return 1
    print("Aucun problème.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
