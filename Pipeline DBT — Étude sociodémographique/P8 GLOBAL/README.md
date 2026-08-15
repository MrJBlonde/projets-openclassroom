# Projet 8 — Analyse sociodémographique des étudiants Data OC

> **Contexte :** Tu es data analyst junior chez OpenClassrooms. Ta mission est d'analyser l'évolution du profil sociodémographique des étudiants inscrits aux parcours Data sur 4 ans, en utilisant DBT + Snowflake.

---

## 🗺️ Vision globale du pipeline

```
Tes fichiers CSV (données brutes)
        ↓
   [1. SNOWFLAKE]
   Tu charges tes données dans le cloud
   → comme "mettre tes fichiers sur une base de données partagée"
        ↓
   [2. DBT — Staging]
   Tu nettoies les données brutes
   → renommer les colonnes, supprimer les doublons, gérer les valeurs manquantes
   → anonymiser pour le RGPD
        ↓
   [3. DBT — Marts]
   Tu agrèges pour créer des indicateurs
   → % femmes/hommes par année, répartition par région, tranche d'âge...
   → tu intègres aussi les données INSEE ici
        ↓
   [4. EXPORT]
   Tu exportes le fichier .csv final propre
        ↓
   [5. SLIDES]
   Tu présentes les résultats à la direction (~15 slides)
```

---

## 📁 Structure du projet DBT

```
mon_projet_dbt/
│
├── models/
│   ├── staging/
│   │   ├── stg_etudiants.sql            ← nettoyage des données brutes étudiants
│   │   └── stg_insee.sql                ← nettoyage des données publiques INSEE
│   │
│   └── marts/
│       ├── mart_demographie.sql         ← indicateurs finaux (âge, genre, région)
│       └── mart_comparaison_insee.sql   ← comparaison étudiants vs population FR
│
├── sources.yml                          ← "voici où sont mes données brutes dans Snowflake"
├── schema.yml                           ← documentation des colonnes + tests qualité
└── dbt_project.yml                      ← configuration générale du projet
```

**Règle simple à retenir :**
- Chaque fichier `.sql` = **une transformation**
- Chaque fichier `.yml` = **documentation + tests**
- C'est tout ce qu'est DBT.

---

## 🧱 Les 3 concepts clés de DBT

### 1. Les modèles
Des fichiers `.sql` qui définissent une transformation.  
DBT les exécute **dans le bon ordre automatiquement** en lisant les dépendances entre eux.

```sql
-- Exemple : models/staging/stg_etudiants.sql
SELECT
    id_etudiant,
    LOWER(genre)        AS genre,
    annee_inscription   AS annee,
    region
FROM {{ source('openclassrooms', 'etudiants_raw') }}
WHERE id_etudiant IS NOT NULL
```

### 2. Les sources
Tu déclares **où sont tes données brutes** dans Snowflake.  
Ça évite les erreurs de référence et rend le projet reproductible.

```yaml
# sources.yml
sources:
  - name: openclassrooms
    database: ma_base
    schema: raw
    tables:
      - name: etudiants_raw
        description: "Données brutes des étudiants inscrits aux parcours Data"
```

### 3. Les tests
Tu définis des **règles de qualité** sur tes colonnes.  
DBT vérifie qu'elles sont respectées avant que tu présentes tes résultats.

```yaml
# schema.yml
models:
  - name: stg_etudiants
    columns:
      - name: id_etudiant
        tests:
          - not_null      # aucun identifiant ne peut être vide
          - unique        # pas de doublon
      - name: genre
        tests:
          - accepted_values:
              values: ['homme', 'femme', 'non_renseigne']
```

---

## 📅 Plan de travail Mardi → Vendredi

| Jour | Objectif | Ce que tu fais concrètement |
|------|----------|-----------------------------|
| **Mardi** | Setup + compréhension des données | Installer DBT, créer le compte Snowflake, charger les CSV, explorer les données |
| **Mercredi** | Construire les modèles DBT | Écrire `stg_etudiants.sql`, `mart_demographie.sql`, intégrer les données INSEE |
| **Jeudi** | Qualité + RGPD + export | Écrire les tests dans `schema.yml`, vérifier la conformité, exporter le `.csv` final |
| **Vendredi matin** | Slides + finalisation | Construire la présentation 15 slides, relecture globale |

---

## 🔒 RGPD — Ce que tu dois vérifier

Le RGPD impose de **minimiser les données personnelles**. Dans ce projet, ça veut dire :

- ❌ Ne pas garder les noms, prénoms, emails dans les tables finales
- ✅ Travailler avec des identifiants anonymisés (`id_etudiant`)
- ✅ Utiliser des **tranches d'âge** plutôt que les dates de naissance exactes
- ✅ Documenter **pourquoi** chaque colonne sensible est conservée ou supprimée

---

## 📊 Indicateurs à analyser

Ces indicateurs répondent à l'objectif : *illustrer le profil sociodémographique et mesurer son évolution sur 4 ans.*

| Dimension | Indicateur | Comparaison INSEE possible ? |
|-----------|-----------|-------------------------------|
| Genre | % hommes / femmes par année | ✅ Oui — population active française |
| Âge | Répartition par tranche d'âge | ✅ Oui — population en formation continue |
| Région | Top régions représentées | ✅ Oui — population par région |
| Évolution | Tendance sur 4 ans pour chaque indicateur | — |

---

## 🗂️ Livrables attendus

| # | Fichier | Nom example |
|---|---------|-------------|
| 1 | Données consolidées | `Nom_Prenom_1_fichier_012026.csv` |
| 2 | Workflow DBT complet | Dossier zippé avec tous les `.sql` et `.yml` |
| 3 | Support de présentation | `Nom_Prenom_3_slides_012026.pptx` |

---

## 🔗 Ressources utiles

- [Documentation officielle DBT](https://docs.getdbt.com)
- [Quickstart DBT + Snowflake](https://docs.getdbt.com/quickstarts/snowflake)
- [Données publiques INSEE](https://www.insee.fr/fr/statistiques)
- [Règlement RGPD — CNIL](https://www.cnil.fr/fr/rgpd-de-quoi-parle-t-on)
