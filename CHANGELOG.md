# Changelog  
Tous les changements notables apportés à ce projet sont consignés dans ce fichier.

Le format est inspiré des bonnes pratiques de journal de modifications, adapté à un projet scientifique et pédagogique.

---

## [00.00.01] — 2025-12-29

### Ajouté
- Script principal permettant la génération automatique d’une affiche astronomique du catalogue Messier.
- Prise en charge de l’analyse récursive d’un répertoire d’images JPEG.
- Détection des objets Messier par :
  - nomenclature Messier directe (Mxx),
  - mécanisme de repli par correspondance NGC → Messier.
- Table interne d’équivalence NGC → Messier couvrant l’ensemble des objets Messier connus.
- Génération d’un document PDF grand format **24 × 36 pouces (ARCH D)**.
- Mise en page normalisée :
  - fond noir intégral,
  - grille de 11 colonnes × 10 rangées (M001 à M110),
  - titre et auteur en blanc,
  - libellé complet en français pour chaque objet.
- Affichage de statistiques détaillées en sortie console :
  - nombre total d’images analysées,
  - nombre d’objets Messier détectés,
  - nombre d’objets identifiés via la nomenclature NGC,
  - liste synthétique des objets Messier manquants.
- Gestion automatique des objets non imagés par affichage de cases noires.
- Documentation complète du projet (README.md).

### Exclu
- Les images de travail ou intermédiaires (`_sub`, `-sub`).
- Les vignettes (`*_thn.jpg`).

### Limitations connues
- Une seule image retenue par objet Messier.
- Absence de prise en charge des catalogues IC et Sharpless.
- Absence d’affichage des métadonnées d’observation (date, instrument, durée).
- Typographie limitée aux polices PDF standards.

---

