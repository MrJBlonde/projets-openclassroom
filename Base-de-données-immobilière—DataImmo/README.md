# Base de données immobilière — DataImmo

## Objectif

Concevoir une base de données relationnelle à partir des données publiques DVF (demandes de valeurs foncières) pour analyser les ventes immobilières du premier semestre 2020 via des requêtes SQL.

## Démarche

Modélisation relationnelle normalisée (3NF) avec séparation claire des entités (vente, bien, commune, département, région) reliées par clés primaires et étrangères, appuyée sur un dictionnaire de données. Création de la base sous SQLite, avec vérification systématique de l'intégrité des relations après import. Rédaction de 12 requêtes répondant à des besoins métier variés : agrégations, jointures multiples, calculs de proportions, classements par fenêtrage (DENSE_RANK), comparaisons de prix au m².

## Compétences

Modélisation relationnelle (3NF) · Conception de schéma avec clés primaires/étrangères · SQL avancé (jointures multiples, sous-requêtes, fonctions de fenêtrage) · Contrôle d'intégrité des données

**Résultat clé** : 12 requêtes métier livrées, dont un classement par fenêtrage des 3 communes les plus chères par département

**Stack** : SQL, SQLite, DBeaver
