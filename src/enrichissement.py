# =========================
# IMPORTS
# =========================

# pandas pour manipuler les données
import pandas as pd

# On importe la fonction qui récupère les offres depuis l'API
# Comme enrichissement.py et api_offres.py sont dans le même dossier src,
# on peut importer directement comme ça
from api_offres import get_offres_data_multi


# =========================
# FONCTION : CHARGER LE FICHIER DES COMMUNES PROPRES
# =========================
def charger_communes_clean():
    """
    Charge le fichier nettoyé des communes.
    """

    df_communes = pd.read_csv(
        "data/processed/communes_clean.csv",
        dtype={
            "code_insee": str,
            "nom_standard": str,
            "code_postal": str
        }
    )

    return df_communes


# =========================
# FONCTION : NETTOYER LES CLÉS DE JOINTURE
# =========================
def nettoyer_cles_jointure(df_offres, df_communes):
    """
    Harmonise les formats des colonnes utilisées dans les jointures.
    """

    # -------- OFFRES --------

    # Nettoyage de la commune côté offres
    # On a vu que cette colonne contient souvent un code INSEE
    if "lieuTravail.commune" in df_offres.columns:
        df_offres["lieuTravail.commune"] = (
            df_offres["lieuTravail.commune"]
            .astype(str)                              # convertir en texte
            .str.strip()                              # enlever les espaces
            .str.replace(".0", "", regex=False)       # enlever .0 éventuel
            .replace("nan", pd.NA)                    # remplacer "nan" texte par une vraie valeur manquante
        )

    # Nettoyage du code postal côté offres
    if "lieuTravail.codePostal" in df_offres.columns:
        df_offres["lieuTravail.codePostal"] = (
            df_offres["lieuTravail.codePostal"]
            .astype(str)
            .str.strip()
            .str.replace(".0", "", regex=False)
            .replace("nan", pd.NA)
        )

        # On force le code postal sur 5 caractères si la valeur existe
        df_offres["lieuTravail.codePostal"] = df_offres["lieuTravail.codePostal"].apply(
            lambda x: x.zfill(5) if pd.notna(x) and x != "" else x
        )

    # -------- COMMUNES --------

    # Nettoyage du code INSEE dans la table communes
    df_communes["code_insee"] = (
        df_communes["code_insee"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    # Nettoyage du code postal dans la table communes
    df_communes["code_postal"] = (
        df_communes["code_postal"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )

    # Nettoyage du nom standard de la commune
    df_communes["nom_standard"] = (
        df_communes["nom_standard"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df_offres, df_communes


# =========================
# FONCTION : CORRIGER LES ARRONDISSEMENTS
# =========================
def corriger_arrondissements(df_offres):
    """
    Crée une colonne code_insee_corrige pour rattacher
    les arrondissements à leur commune principale.
    """

    # Par défaut, on reprend la commune d'origine
    df_offres["code_insee_corrige"] = df_offres["lieuTravail.commune"]

    # -------- PARIS --------
    # Les arrondissements de Paris commencent souvent par 751
    # On les rattache au code INSEE principal de Paris : 75056
    df_offres.loc[
        df_offres["lieuTravail.commune"].astype(str).str.startswith("751", na=False),
        "code_insee_corrige"
    ] = "75056"

    # -------- LYON --------
    # Les arrondissements de Lyon commencent souvent par 6938
    # On les rattache au code INSEE principal de Lyon : 69123
    df_offres.loc[
        df_offres["lieuTravail.commune"].astype(str).str.startswith("6938", na=False),
        "code_insee_corrige"
    ] = "69123"

    # -------- MARSEILLE --------
    # Les arrondissements de Marseille commencent souvent par 132
    # On les rattache au code INSEE principal de Marseille : 13055
    df_offres.loc[
        df_offres["lieuTravail.commune"].astype(str).str.startswith("132", na=False),
        "code_insee_corrige"
    ] = "13055"

    return df_offres


# =========================
# FONCTION : JOINTURE PRINCIPALE SUR CODE INSEE CORRIGÉ
# =========================
def joindre_sur_code_insee(df_offres, df_communes):
    """
    Jointure principale :
    code_insee_corrige (offres) = code_insee (communes)
    """

    # On garde seulement les colonnes utiles de la table communes
    df_communes_small = df_communes[
        [
            "code_insee",
            "nom_standard",
            "code_postal",
            "population",
            "latitude_centre",
            "longitude_centre"
        ]
    ].copy()

    # Jointure gauche : on garde toutes les offres
    df_merge = df_offres.merge(
        df_communes_small,
        left_on="code_insee_corrige",
        right_on="code_insee",
        how="left"
    )

    return df_merge


# =========================
# FONCTION : JOINTURE DE SECOURS SUR CODE POSTAL
# =========================
def completer_sur_code_postal(df_merge_insee, df_communes):
    """
    Si la jointure sur code INSEE n'a pas trouvé,
    on essaie une jointure de secours sur le code postal.
    """

    # Lignes déjà bien matchées
    df_match_ok = df_merge_insee[df_merge_insee["latitude_centre"].notna()].copy()

    # Lignes non trouvées
    df_non_match = df_merge_insee[df_merge_insee["latitude_centre"].isna()].copy()

    # Si aucune ligne non trouvée, on retourne tel quel
    if df_non_match.empty:
        return df_merge_insee

    # Pour éviter les doublons :
    # on garde une seule commune par code postal,
    # ici la plus peuplée
    df_postal = (
        df_communes
        .sort_values("population", ascending=False)
        .drop_duplicates(subset=["code_postal"])
    )

    df_postal = df_postal[
        [
            "code_postal",
            "nom_standard",
            "population",
            "latitude_centre",
            "longitude_centre"
        ]
    ].copy()

    # On enlève les anciennes colonnes issues de la première jointure
    df_non_match = df_non_match.drop(
        columns=["nom_standard", "code_postal", "population", "latitude_centre", "longitude_centre"],
        errors="ignore"
    )

    # Jointure de secours sur code postal
    df_non_match_postal = df_non_match.merge(
        df_postal,
        left_on="lieuTravail.codePostal",
        right_on="code_postal",
        how="left"
    )

    # On reconstruit le dataframe final
    df_final = pd.concat([df_match_ok, df_non_match_postal], ignore_index=True)

    return df_final


# =========================
# FONCTION : PIPELINE COMPLET
# =========================
def get_offres_enrichies():
    """
    Pipeline complet :
    1. récupérer les offres
    2. charger les communes
    3. nettoyer les clés
    4. corriger les arrondissements
    5. joindre sur code INSEE corrigé
    6. compléter sur code postal
    """

    # 1. Récupérer les offres
    df_offres = get_offres_data_multi()

    # 2. Charger la table des communes
    df_communes = charger_communes_clean()

    # 3. Nettoyer les colonnes de jointure
    df_offres, df_communes = nettoyer_cles_jointure(df_offres, df_communes)

    # 4. Corriger les arrondissements
    df_offres = corriger_arrondissements(df_offres)

    # 5. Jointure principale sur code INSEE corrigé
    df_merge = joindre_sur_code_insee(df_offres, df_communes)

    # 6. Jointure de secours sur code postal
    df_final = completer_sur_code_postal(df_merge, df_communes)

    return df_final


# =========================
# TEST LOCAL
# =========================
if __name__ == "__main__":
    # On lance le pipeline complet
    df = get_offres_enrichies()

    # On affiche quelques colonnes importantes pour vérifier
    print(
        df[
            [
                "intitule",
                "lieuTravail.commune",
                "lieuTravail.codePostal",
                "code_insee_corrige",
                "nom_standard",
                "population",
                "latitude_centre",
                "longitude_centre"
            ]
        ].head(20)
    )

    # On calcule le taux de jointure réussi
    taux_match = df["latitude_centre"].notna().mean() * 100
    print(f"\nTaux de jointure réussi : {taux_match:.2f}%")

    # Diagnostic des lignes non matchées
    df_non_match = df[df["latitude_centre"].isna()].copy()

    print("\nNombre de lignes non matchées :", len(df_non_match))

    print("\nExemples de lignes non matchées :")
    print(
        df_non_match[
            [
                "intitule",
                "lieuTravail.commune",
                "lieuTravail.codePostal",
                "code_insee_corrige"
            ]
        ].head(20)
    )
    print(
    df[[
        "lieuTravail.libelle",
        "lieuTravail.commune",
        "lieuTravail.codePostal"
    ]].drop_duplicates().head(30)
)