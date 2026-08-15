# Étude de marché — Export international

## Objectif

Identifier les pays les plus prometteurs pour exporter un produit, à partir de données économiques et sociales de 126 pays.

## Démarche

Standardisation des données puis réduction de dimension par ACP (8 composantes retenues, 84,1% de variance expliquée). Regroupement des pays par classification ascendante hiérarchique, validé par K-means (concordance ARI = 0,634). Score composite pondéré selon des critères business (pouvoir d'achat, dépendance aux importations, sensibilité au bio) pour prioriser les cibles au sein du meilleur cluster.

## Compétences

Réduction de dimension (ACP) · Classification non supervisée (CAH, K-means) · Validation de clustering (silhouette, ARI) · Construction d'un score métier pondéré

**Résultat clé** : 8 pays prioritaires confirmés par score composite, issus à 100% du cluster le mieux noté

**Stack** : Python, Pandas, Scikit-learn, Scipy
