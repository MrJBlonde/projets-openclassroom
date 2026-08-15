# Bottleneck — Pipeline augmenté par l'IA

## Objectif

Améliorer une analyse de ventes existante grâce à l'IA, de façon critique et documentée : détecter automatiquement les erreurs de données, mieux estimer les ventes manquantes, et recommander un prix optimal — plutôt que de refaire l'analyse à la main.

## Les 6 axes d'amélioration

1. **Validation automatique des données** *(Pandera)* — fiabiliser les données à l'entrée sans vérification manuelle répétée
2. **Détection d'anomalies multivariées** *(Isolation Forest)* — repérer des erreurs invisibles pour un simple Z-score, en croisant plusieurs variables à la fois
3. **Explicabilité des anomalies** *(SHAP)* — transformer une alerte en explication compréhensible pour une équipe non-technique
4. **Segmentation automatique des produits** *(K-Means)* — fiabiliser et automatiser une segmentation faite manuellement
5. **Estimation des ventes manquantes** *(kNN)* — remplacer une moyenne globale par une estimation basée sur les produits les plus proches
6. **Recommandation de prix** *(Régression log-log)* — quantifier l'élasticité prix/ventes pour orienter une décision de pricing

**Résultat clé** : manque à gagner réestimé à 20 538€ (-27% vs calcul initial par simple moyenne)

**Stack** : Python, Pandas, Scikit-learn, SHAP, Pandera, Plotly
