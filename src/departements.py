# =========================
# IMPORTS
# =========================

# pandas sert à lire, nettoyer et sauvegarder les données
import pandas as pd


# =========================
# FONCTION : CHARGER LE FICHIER BRUT
# =========================
def charger_departements():
    """
    Cette fonction charge le fichier brut des départements
    depuis le dossier data/raw.
    """

    # On lit le fichier CSV brut
    # IMPORTANT :
    # on force code_departement en texte
    # pour garder les zéros éventuels au début
    df = pd.read_csv(
        "data/raw/departements-france.csv",
        dtype={"code_departement": str},
        low_memory=False
    )

    # On garde seulement les colonnes utiles pour le projet
    df = df[
        [
            "code_departement",
            "nom_departement",
            "code_region",
            "nom_region"
        ]
    ].copy()

    # On retourne le dataframe
    return df


# =========================
# FONCTION : NETTOYER LES DONNÉES
# =========================
def nettoyer_departements(df):
    """
    Cette fonction nettoie les données des départements.
    """

    # On enlève les lignes où le code département est vide
    df = df[df["code_departement"].notna()].copy()

    # On transforme le code département en texte
    df["code_departement"] = df["code_departement"].astype(str)

    # On enlève les espaces inutiles
    df["code_departement"] = df["code_departement"].str.strip()

    # On transforme le nom du département en texte
    df["nom_departement"] = df["nom_departement"].astype(str)

    # On enlève les espaces inutiles
    df["nom_departement"] = df["nom_departement"].str.strip()

    # On transforme le code région en texte
    df["code_region"] = df["code_region"].astype(str)

    # On enlève les espaces inutiles
    df["code_region"] = df["code_region"].str.strip()

    # On transforme le nom de région en texte
    df["nom_region"] = df["nom_region"].astype(str)

    # On enlève les espaces inutiles
    df["nom_region"] = df["nom_region"].str.strip()

    # On supprime les doublons éventuels
    # Ici on garde une seule ligne par département
    df = df.drop_duplicates(subset=["code_departement"]).copy()

    # On retourne le dataframe propre
    return df


# =========================
# FONCTION : SAUVEGARDER LE FICHIER PROPRE
# =========================
def sauvegarder_departements(df):
    """
    Cette fonction sauvegarde le fichier nettoyé
    dans le dossier data/processed.
    """

    # On enregistre le CSV nettoyé
    df.to_csv("data/processed/departements_clean.csv", index=False)


# =========================
# FONCTION : PIPELINE COMPLET
# =========================
def process_departements():
    """
    Cette fonction fait tout :
    1. charger
    2. nettoyer
    3. sauvegarder
    """

    # Charger les données brutes
    df = charger_departements()

    # Nettoyer les données
    df = nettoyer_departements(df)

    # Sauvegarder les données nettoyées
    sauvegarder_departements(df)

    # Retourner le résultat final
    return df


# =========================
# TEST LOCAL
# =========================
if __name__ == "__main__":
    # On lance tout le pipeline
    df = process_departements()

    # On affiche les 5 premières lignes
    print(df.head())

    # On affiche les types de colonnes
    print("\nTypes des colonnes :")
    print(df.dtypes)