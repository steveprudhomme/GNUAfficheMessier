# GNU Affiche Messier
**Version : 00.00.01**

**GNU Affiche Messier** est un script Python permettant de générer automatiquement une **affiche astronomique grand format (PDF 24 × 36 pouces)** regroupant les **110 objets du catalogue Messier**, à partir d’un répertoire d’images astrophotographiques (Seestar S50 ou équipement équivalent).

Le projet vise à produire une affiche :
- esthétique,
- scientifiquement cohérente,
- entièrement automatisée,
- prête pour l’impression,

tout en servant d’**outil de suivi de progression** pour les observateurs et astrophotographes amateurs.

---

## Table des matières

- Fonctionnalités  
- Philosophie générale  
- Principe de fonctionnement  
- Structure des données attendue  
- Prérequis  
- Installation  
- Utilisation  
- Détection des objets Messier  
- Table d’équivalence NGC → Messier  
- Mise en page de l’affiche  
- Statistiques et mode diagnostic  
- Impression grand format  
- Limitations connues  
- Évolutions possibles  
- Licence  
- Crédits  

---

## Fonctionnalités

- Analyse récursive d’un répertoire d’images JPEG
- Détection automatique des objets Messier :
  - par **nomenclature Messier (Mxx)**,
  - par **correspondance NGC → Messier**
- Exclusion automatique :
  - des images `_sub` ou `-sub`,
  - des vignettes (`*_thn.jpg`)
- Sélection automatique de la **meilleure image par objet** (selon la taille du fichier)
- Génération d’une **affiche PDF 24 × 36 pouces** :
  - fond noir,
  - grille 11 × 10 (M001 à M110),
  - titre et auteur en blanc,
  - nom complet de chaque objet en français,
  - cases noires pour les objets non imagés
- Affichage de **statistiques détaillées** dans la console :
  - nombre total d’images analysées,
  - nombre d’objets Messier détectés,
  - nombre d’objets récupérés par correspondance NGC,
  - liste synthétique des objets Messier manquants

---

## Philosophie générale

GNU Affiche Messier repose sur les principes suivants :

- **Un objet Messier correspond à une case**
- **Une image finale constitue une preuve d’observation**
- **L’absence d’image est une information en soi**
- **Automatisation maximale, intervention humaine minimale**
- **Aucune dépendance à un service externe**
- **Utilisation de formats ouverts et pérennes (PDF)**

L’affiche générée peut servir à la fois :
- d’outil de suivi personnel,
- de support pédagogique pour un club d’astronomie,
- de matériel de diffusion scientifique (exposition, conférence, activité éducative).

---

## Principe de fonctionnement

1. Le script parcourt récursivement le répertoire racine spécifié.
2. Il identifie les fichiers JPEG admissibles.
3. Il tente d’identifier l’objet céleste :
   - d’abord par la présence d’un identifiant Messier (`Mxx`),
   - à défaut, par un **mécanisme de repli** utilisant la nomenclature NGC.
4. Pour chaque objet Messier :
   - une seule image est retenue (la plus volumineuse).
5. Une grille normalisée est générée dans un document PDF grand format.
6. Les objets non trouvés apparaissent sous forme de cases noires.

---

## Structure des données attendue

Le script est volontairement **tolérant** et ne requiert aucune structure de répertoires rigide.

Exemples de noms de fichiers ou de chemins compatibles :

```
M 31/Stacked_Andromeda.jpg
NGC_224_Final.jpg
Messier-42.jpg
Astro/Orion/NGC1976_stack.jpeg
```

Aucune convention stricte n’est imposée, tant que les identifiants sont présents.

---

## Prérequis

- Python **3.9 ou plus récent**
- Systèmes d’exploitation testés :
  - Windows 10 / 11
- Bibliothèques Python requises :
  - `pillow`
  - `reportlab`

---

## Installation

```bash
pip install pillow reportlab
```

---

## Utilisation

1. Modifier les variables de configuration au début du script :
   ```python
   ROOT_DIR = r"F:\MyWorks"
   OUTPUT_PDF = r"Affiche_Objets_Messier_24x36.pdf"
   ```

2. Exécuter le script :
   ```bash
   python GNUAfficheMessier.py
   ```

3. Le fichier PDF est généré dans le répertoire spécifié.

---

## Détection des objets Messier

La détection s’effectue selon l’ordre suivant :

1. **Identification directe Messier**
   - Exemples : `M1`, `M001`, `Messier 42`
2. **Correspondance NGC → Messier**
   - Exemple : `NGC 224` → `M31`
   - Exemple : `NGC 1976` → `M42`

Ce mécanisme permet d’identifier des objets Messier même lorsque la nomenclature Messier n’est pas utilisée dans les fichiers.

---

## Table d’équivalence NGC → Messier

Le projet intègre une **table interne d’équivalence NGC → Messier** couvrant les objets Messier disposant d’un identifiant NGC reconnu.

Cette table peut être :
- enrichie manuellement,
- remplacée ultérieurement par une lecture à partir d’un fichier externe (CSV ou tableur).

---

## Mise en page de l’affiche

- Format : **24 × 36 pouces (ARCH D)**
- Orientation : portrait
- Grille : **11 colonnes × 10 rangées**
- Ordre de lecture : M001 → M110
- Fond : noir intégral
- Texte : blanc
- Typographie : Helvetica (police standard PDF)

---

## Statistiques et mode diagnostic

Lors de l’exécution, le script affiche :

- le nombre total d’images JPEG analysées,
- le nombre d’objets Messier détectés,
- le nombre d’objets identifiés par correspondance NGC,
- la liste synthétique des objets Messier manquants.

Ces informations facilitent :
- le diagnostic,
- l’évaluation de la couverture du catalogue Messier,
- la planification des observations futures.

---

## Impression grand format

Recommandations pour l’impression :

- Ouvrir le fichier PDF dans **Adobe Acrobat**
- Échelle : **100 % (taille réelle)**
- Désactiver tout ajustement automatique à la page
- Format papier : **24 × 36 pouces (ARCH D)**

---

## Limitations connues

- Absence de prise en charge des catalogues IC et Sharpless
- Une seule image par objet Messier
- Aucune métadonnée d’observation affichée sur l’affiche
- Typographie limitée aux polices PDF standards

---

## Évolutions possibles

- Exportation CSV des objets Messier manquants
- Ajout de la prise en charge des catalogues IC et Sharpless
- Génération de formats A0 et A1
- Lecture de la table d’équivalence depuis un tableur
- Génération d’affiches annuelles ou thématiques

---

## Licence

Projet distribué sous licence **GNU GPL version 3**.

---

## Crédits

**Auteur**  
Steve Prud’Homme  

Projet inspiré par :
- le catalogue Messier,
- la pratique de l’astronomie amateur,
- les besoins pédagogiques des clubs d’astronomie.

---
