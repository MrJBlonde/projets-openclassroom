# ============================================================
# Script de détection automatique de faux billets - ONCFM
# Auteur : Gauthier Julien
# Date : 06/2026
# ------------------------------------------------------------
# Ce script prend en entrée :
#   - un chemin vers un fichier CSV contenant les mesures de plusieurs billets
#   - ou les valeurs géométriques d'un seul billet saisies manuellement
# Il retourne pour chaque billet : True (vrai) ou False (faux)
# ============================================================

import pandas as pd
import joblib
import sys
import os
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, fbeta_score
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

# ------------------------------------------------------------
# Définition des classes du pipeline
# (nécessaires pour charger le modèle sauvegardé)
# ------------------------------------------------------------

class ColumnValidator(BaseEstimator, TransformerMixin):
    def __init__(self, expected_columns):
        self.expected_columns = expected_columns
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        missing = set(self.expected_columns) - set(X.columns)
        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")
        return X[self.expected_columns]

class EmptyRowDetector(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        fully_empty = X.isna().all(axis=1)
        if fully_empty.any():
            nb = fully_empty.sum()
            raise ValueError(f"{nb} billet(s) sans aucune mesure : impossible de prédire.")
        return X

class BestModelSelector(BaseEstimator, ClassifierMixin):
    def __init__(self, models, scoring=None, cv=5):
        self.models = models
        self.scoring = scoring
        self.cv = cv
    def fit(self, X, y):
        fbeta_faux = make_scorer(fbeta_score, beta=2, pos_label=False)
        scoring = self.scoring or fbeta_faux
        best_score = -np.inf
        best_model = None
        best_name = None
        for name, model in self.models.items():
            score = cross_val_score(model, X, y, scoring=scoring, cv=self.cv).mean()
            if score > best_score:
                best_score = score
                best_model = model
                best_name = name
        self.best_model_ = best_model.fit(X, y)
        self.best_name_ = best_name
        return self
    def predict_proba(self, X):
        return self.best_model_.predict_proba(X)
    def predict(self, X):
        return self.best_model_.predict(X)

class ThresholdClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, base_model, threshold=0.8):
        self.base_model = base_model
        self.threshold = threshold
    def fit(self, X, y):
        self.base_model.fit(X, y)
        self.classes_ = np.unique(y)
        return self
    def predict_proba(self, X):
        return self.base_model.predict_proba(X)
    def predict(self, X):
        probas = self.base_model.predict_proba(X)[:, 1]
        return np.where(probas >= self.threshold, True, False)

# ------------------------------------------------------------
# Chargement du modèle sauvegardé
# ------------------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "pipeline_final.pkl")

if not os.path.exists(MODEL_PATH):
    print(f"Erreur : le modèle '{MODEL_PATH}' est introuvable.")
    sys.exit(1)

pipeline = joblib.load(MODEL_PATH)
print("Modèle chargé avec succès.")

# ------------------------------------------------------------
# Gestion des inputs
# ------------------------------------------------------------

COLONNES = ["diagonal", "height_left", "height_right", "margin_low", "margin_up", "length"]

def charger_depuis_csv(chemin):
    """Charge les billets depuis un fichier CSV."""
    if not os.path.exists(chemin):
        print(f"Erreur : le fichier '{chemin}' est introuvable.")
        sys.exit(1)
    df = pd.read_csv(chemin, sep=None, engine="python")  # détecte automatiquement le séparateur
    return df

def charger_depuis_valeurs_manuelles():
    """Demande à l'utilisateur de saisir les 6 mesures d'un billet."""
    print("Saisie manuelle des mesures du billet :")
    valeurs = {}
    for col in COLONNES:
        valeurs[col] = float(input(f"  {col} : "))
    return pd.DataFrame([valeurs])

# ------------------------------------------------------------
# Prédiction et affichage du résultat
# ------------------------------------------------------------

def predire(df):
    """Prédit si chaque billet est vrai ou faux et affiche le résultat."""
    predictions = pipeline.predict(df)
    probas = pipeline.predict_proba(df)[:, 1]  # Probabilité d'être un vrai billet

    print("\nRésultats :")
    for i, (pred, proba) in enumerate(zip(predictions, probas)):
        statut = "Vrai billet" if pred else "Faux billet"
        print(f"  Billet {i+1} : {statut} ({pred}) — probabilité d'être vrai : {proba:.1%}")

    nb_total = len(predictions)
    nb_vrais = sum(predictions)
    nb_faux = nb_total - nb_vrais
    print(f"\n--- Récapitulatif ---")
    print(f"  Total billets analysés : {nb_total}")
    print(f"  Vrais billets          : {nb_vrais}")
    print(f"  Faux billets détectés  : {nb_faux}")

    # Export Excel avec probabilités
    df_result = df.copy()
    df_result["prediction"] = ["Vrai billet" if p else "Faux billet" for p in predictions]
    df_result["probabilite_vrai"] = (probas * 100).round(1).astype(str) + "%"
    output_path = os.path.join(os.path.dirname(__file__), "resultats_predictions.xlsx")
    df_result.to_excel(output_path, index=False)
    print(f"\n  Résultats exportés : {output_path}")

    return predictions

# ------------------------------------------------------------
# Point d'entrée du script
# ------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        chemin_csv = sys.argv[1]
        print(f"Chargement du fichier : {chemin_csv}")
        df = charger_depuis_csv(chemin_csv)
    else:
        df = charger_depuis_valeurs_manuelles()
    predire(df)
    
