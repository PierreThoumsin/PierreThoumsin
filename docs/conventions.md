---
titre: Conventions du projet POSSAD-Off
statut: valide
mis-a-jour: 2026-11-26
---

# Conventions du projet POSSAD-Off

Ce document est la **source unique** des règles du projet.
`CLAUDE.md` (Claude Code) et `AGENTS.md` (Codex) se contentent d'y renvoyer : aucune règle n'est recopiée ailleurs.

Les mots **DOIT**, **NE DOIT PAS** et **PEUT** ont leur sens habituel : obligation, interdiction, faculté.

---

## 1. Langue

- Le **contenu** des documents, des messages de commit et des échanges DOIT être en **français**.
- Les **noms** de fichiers, de dossiers et de branches DOIVENT être en **anglais** (voir section 2).
- Exception : les **titres de section** des descriptions de Pull Request sont en **anglais** (`## OBJECT:`, `## SUMMARY:`…), leur contenu reste en français (voir section 5).

## 2. Noms de fichiers et de dossiers

### Règle générale

Un nom de fichier ou de dossier DOIT être :

- en **anglais** ;
- en **minuscules** ;
- en **kebab-case** : mots séparés par des tirets `-` ;
- **sans accents, espaces ni caractères spéciaux**.

| ✅ Correct | ❌ Incorrect | Problème |
|---|---|---|
| `decision-register.md` | `registre-decisions.md` | nom en français |
| `risk-register.md` | `Risk_Register.md` | majuscules et underscore |
| `company-profile.md` | `company profile.md` | espace |
| `ceo-summary.md` | `synthèse-ceo.md` | accent et français |

### Exceptions

| Fichier | Raison |
|---|---|
| `README.md`, `CLAUDE.md`, `AGENTS.md` | noms imposés par GitHub, Claude Code et Codex |
| `SKILL.md`, `.github/…` et autres fichiers d'outils | format imposé par l'outil |
| contenu de `private/` | données personnelles, jamais versionnées |

### Éléments numérotés ou datés

| Élément | Format | Exemple |
|---|---|---|
| Décision du dirigeant | `DEC-NNN` (dans le registre) | `DEC-007` |
| Dossier de travail | `AAAA-MM-JJ-sujet-court/` | `2026-11-18-pricing-review/` |

## 3. En-tête YAML

### Documents concernés

L'en-tête est **obligatoire uniquement sur les documents de référence** :

- les documents de `docs/` (méthode, conventions, modèle de fonctionnement) ;
- les registres et fiches de la mémoire de l'entreprise (profil, chiffres clés, registres de décisions et de risques).

Il NE DOIT PAS être ajouté :

- aux `README.md` ;
- aux fichiers d'outils (`CLAUDE.md`, `AGENTS.md`, `.claude/**`) ;
- aux notes et livrables des dossiers de travail.

### Format

Trois champs, dans cet ordre :

```yaml
---
titre: Registre des décisions
statut: brouillon
mis-a-jour: 2026-11-18
---
```

| Champ | Valeurs autorisées |
|---|---|
| `titre` | titre du document, en français |
| `statut` | `brouillon` · `valide` · `obsolete` |
| `mis-a-jour` | date de la dernière modification significative, au format `AAAA-MM-JJ` |

L'auteur, l'historique et les versions ne sont **pas** dans l'en-tête : Git les conserve.
Il n'y a donc **pas de journal des modifications** dans les documents.

## 4. Fichiers README.md

### Rôle

Un `README.md` est la **porte d'entrée d'un dossier**. Il explique en peu de lignes :

1. à quoi sert le dossier ;
2. ce qu'il contient ;
3. les règles propres à ce dossier, s'il y en a.

Le `README.md` racine présente le projet dans son ensemble et explique comment démarrer.
Chaque dossier principal DOIT avoir son `README.md` (5 à 30 lignes suffisent hors racine).

### Émojis : obligatoires

Les `README.md` DOIVENT utiliser des émojis **pertinents** pour structurer et dynamiser la lecture :

- le **titre principal** (`#`) DOIT commencer par un émoji ;
- chaque **titre de section** (`##`) DOIT commencer par un émoji ;
- **un seul émoji par titre**, choisi pour son sens, pas pour décorer ;
- dans le corps du texte, les émojis PEUVENT servir de repères dans les listes et tableaux (statuts, avertissements) ;
- les émojis NE DOIVENT PAS apparaître dans les blocs de code ni dans les noms de fichiers.

Pour que les mêmes émojis aient toujours le même sens d'un README à l'autre :

| Émoji | Usage |
|---|---|
| 🎯 | objectif, raison d'être |
| 🧭 | principe, règle fondatrice |
| 📂 | structure, contenu du dossier |
| 🚀 | démarrage, mise en route |
| 🤖 | agents IA |
| 📏 | conventions, règles |
| 🗺️ | feuille de route |
| 📌 | état actuel |
| 🔒 | données sensibles, confidentialité |
| ⚠️ | avertissement |
| ✅ / ❌ | correct / incorrect, fait / non fait |
| 🚧 | en construction |

### Exemple de README de dossier

```markdown
# 🏢 company

## 🎯 Rôle
Mémoire durable de l'entreprise, lue par tous les agents avant d'agir.

## 📂 Contenu
| Fichier | Contenu |
|---|---|
| `company-profile.md` | identité, activité, juridiction |
| `decision-register.md` | décisions prises par le dirigeant |

## 📏 Règles
Seul le dirigeant valide une modification de ces fichiers.
```

## 5. Branches et Pull Requests

Le modèle est volontairement simple : **pas de branche `develop`**, et une seule règle de nommage,
quel que soit l'outil utilisé (humain, Claude Code, Codex).

### Nom des branches

```text
type/court-resume-en-anglais
```

- `type` : un des types autorisés de la section 6 (`feat`, `fix`, `docs`, `agent`, `refactor`, `chore`, `ci`, `test`, `revert`) ;
- `court-resume-en-anglais` : quelques mots en anglais, en minuscules et en kebab-case.

| ✅ Correct | ❌ Incorrect | Problème |
|---|---|---|
| `docs/add-project-conventions` | `codex/add-conventions` | préfixe d'outil interdit |
| `feat/add-agent-registry` | `feature/agent-registry` | type non autorisé |
| `agent/define-cfo-scope` | `agent/définir-le-cfo` | français et accent |
| `fix/broken-register-link` | `fix/Broken_Link` | majuscules et underscore |

Aucun préfixe propre à un outil (`codex/`…) n'est toléré, **sauf `claude/`** : les sessions Claude dans le cloud
créent elles-mêmes leur branche sous ce préfixe et ne peuvent pas le changer. Un humain ou un agent en local
DOIT utiliser un type de la liste.
La seule branche permanente est `main`, version de référence toujours propre.

### Cycle de vie

- une branche = **un seul sujet**, de courte durée ;
- elle part de `main` et revient dans `main` par une Pull Request ;
- **la fusion est décidée et effectuée par le dirigeant**, jamais par un agent ;
- la fusion se fait **uniquement en « Squash and merge »** : tous les commits de la PR deviennent un seul commit dans `main` ;
- le message de ce commit est le **titre et la description de la PR** (réglage du dépôt : *Default commit message → Pull request title and description*) ;
- la branche est supprimée après la fusion.

### Titre des Pull Requests

Avec la fusion en squash, le titre de la PR **devient le titre du commit** dans `main`.
Il suit donc exactement le format des commits (section 6) :

```text
type(portée): description en français
```

- `type` : le même que celui de la branche (sauf branche `claude/`, qui prend le type adapté) ;
- `(portée)` : facultative ;
- description à l'infinitif, sans point final, **72 caractères maximum** pour le titre entier.

| Branche | Titre de la Pull Request |
|---|---|
| `docs/add-project-conventions` | `docs: établir les conventions du projet` |
| `feat/add-agent-registry` | `feat: ajouter le registre des agents` |
| `agent/define-cfo-scope` | `agent(cfo): préciser le périmètre trésorerie` |

### Description des Pull Requests

La description de la PR **devient le corps du commit** dans `main`. Elle DOIT suivre cette structure :
titres de section en anglais, en majuscules, précédés de `##` et suivis de deux-points ; contenu en français.

<!-- ci:pr-sections : tableau lu par la CI, garder ce format de ligne -->

| Section | Statut | Contenu |
|---|---|---|
| `## OBJECT:` | obligatoire | l'objet de la PR, comme l'objet d'un email : pourquoi ce changement |
| `## SUMMARY:` | obligatoire | ce qui a été ajouté, modifié ou supprimé, une ligne par changement |
| `## TODO:` | facultative | actions restantes, prochaines étapes |
| `## FIXME:` | facultative | problèmes connus, points fragiles à reprendre |
| `## NOTE:` | facultative | choix techniques, précisions utiles |
| `## QUESTION:` | facultative | points ouverts, demandes de validation |

<!-- /ci:pr-sections -->

Aucun autre titre `##` n'est autorisé (les sous-titres `###` sont libres).
Le modèle `.github/pull_request_template.md` préremplit cette structure : ses consignes en commentaires HTML
(`<!-- … -->`) DOIVENT être effacées avant la fusion, sinon elles sont copiées dans le commit.

Exemple :

```markdown
## OBJECT:
Vérifier automatiquement le format des Pull Requests avant leur fusion.

## SUMMARY:
- `.github/workflows/check-pr.yml` : création du workflow de contrôle.

## TODO:
- Rendre ce contrôle obligatoire dans un ruleset de `main`.
```

### Contrôle automatique

Le workflow `.github/workflows/check-pr.yml` vérifie sur chaque PR le nom de la branche, le titre et la description.
Un contrôle rouge signale une règle non respectée : la PR DOIT être corrigée avant la fusion.

La liste des types (section 6) et celle des sections de description (ci-dessus) sont **lues directement dans ce
document**, tel qu'il est sur `main`. Une nouvelle règle ne s'applique donc qu'une fois sa PR fusionnée.
Le même workflow vérifie que le modèle `.github/pull_request_template.md` reste cohérent avec ces listes.

## 6. Commits

### Format du titre

```text
type(portée): description en français
```

- `type` : obligatoire, choisi dans la liste ci-dessous ;
- `(portée)` : facultative, le dossier ou le sujet concerné (`agents`, `company`, `docs`, `templates`, `config`…) ;
- `description` : en français, à l'infinitif, sans point final, **72 caractères maximum** pour le titre entier.

### Types autorisés

<!-- ci:types : tableau lu par la CI, garder ce format de ligne -->

| Type | Usage |
|---|---|
| `feat` | nouvelle fonctionnalité, nouveau workflow, nouvelle commande |
| `fix` | correction d'une erreur |
| `docs` | documentation (README, conventions, guides) |
| `agent` | création ou modification d'une fiche agent |
| `refactor` | réorganisation sans changement de comportement (renommage, déplacement) |
| `chore` | maintenance technique (configuration, dépendances, `.gitignore`) |
| `ci` | intégration continue (workflows GitHub Actions) |
| `test` | ajout ou correction de tests |
| `revert` | annulation d'un changement précédent |

<!-- /ci:types -->

### Exemples

| ✅ Correct | ❌ Incorrect | Problème |
|---|---|---|
| `docs(conventions): définir la règle des émojis` | `update` | aucune information |
| `agent(cfo): préciser le périmètre trésorerie` | `Agent CFO modifié.` | pas de type, point final |
| `fix: corriger le lien vers le registre` | `fix: Fixed broken link` | description en anglais |
| `chore: ignorer le dossier private` | `chore: Ignorer private.` | majuscule et point final |

### Corps et pied du message

- Le **corps** est facultatif. Il explique le *pourquoi*, séparé du titre par une ligne vide.
- Le **pied** peut contenir des mentions de co-auteur (`Co-Authored-By: …`).
- Le titre décrit **l'ensemble** des changements du commit, pas seulement le premier fichier touché.
  Si un commit mélange deux sujets, il DOIT être découpé.
- Les émojis sont autorisés dans les messages de commit.
- Avec la fusion en squash, seuls le titre et la description de la PR arrivent dans `main` (section 5) :
  les commits de branche servent au suivi du travail en cours.

### Signature obligatoire

Tout commit DOIT être **signé** et apparaître comme **Verified** sur GitHub avant d'être fusionné dans `main`.

Mise en place sur un poste (une seule fois), avec une clé SSH :

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Ajouter ensuite la même clé publique sur GitHub comme **clé de signature** :
*Settings → SSH and GPG keys → New SSH key → Key type : Signing Key*.

Vérification : badge **Verified** à côté du commit sur GitHub.

Le commit de squash créé par GitHub lors de la fusion est signé par GitHub et apparaît donc comme **Verified**.
La règle s'applique quand même aux commits de branche, qui restent visibles dans la PR.

Si un commit ne peut pas être signé ou n'apparaît pas comme vérifié, l'agent DOIT le signaler au dirigeant
au lieu de le présenter comme conforme.

## 7. Données sensibles

- Tout le contenu du dossier `private/` est **ignoré par Git** (`.gitignore`), **sauf** les `README.md` et `.gitkeep`
  qui décrivent sa structure. Ces fichiers NE DOIVENT contenir **aucune donnée sensible**.
- Pièces d'identité, relevés bancaires, contrats non publics, données personnelles de salariés ou de clients :
  **uniquement dans `private/`**, jamais dans un commit.
- Un agent qui rencontre une donnée sensible hors de `private/` DOIT le signaler avant tout commit.

## 8. Faire évoluer ces conventions

- Toute modification de ce document est proposée au dirigeant, puis appliquée par un commit
  `docs(conventions): …` après son accord.
- Une règle n'existe que si elle est écrite ici. Une règle écrite ailleurs n'est pas applicable.
- Le workflow `.github/workflows/check-pr.yml` applique une partie des sections 5 et 6 :
  - les **listes** (types autorisés, sections de description) sont lues dans ce document, entre les marqueurs
    `<!-- ci:… -->` : il suffit de modifier les tableaux, sans toucher au workflow. Les marqueurs et le format
    des lignes (`` | `valeur` | … ``) NE DOIVENT PAS être modifiés ;
  - les **formats** (kebab-case, `type(portée): description`, 72 caractères) sont écrits dans le workflow :
    toute modification de ces formats DOIT y être reportée dans la même Pull Request.
