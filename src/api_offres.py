import os
import re
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = st.secrets.get("CLIENT_ID", os.getenv("CLIENT_ID"))
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", os.getenv("CLIENT_SECRET"))

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("CLIENT_ID ou CLIENT_SECRET manquant")


def simplifier_contrat(type_contrat, intitule=None):
    type_txt = str(type_contrat).lower().strip() if pd.notna(type_contrat) else ""
    titre_txt = str(intitule).lower().strip() if pd.notna(intitule) else ""

    # normalisation
    for old, new in [("é", "e"), ("è", "e"), ("ê", "e")]:
        type_txt = type_txt.replace(old, new)
        titre_txt = titre_txt.replace(old, new)

    # -------- 1. ALTERNANCE (très large) --------
    if any(mot in titre_txt for mot in [
        "alternance",
        "alternant",
        "alternante",
        "alternant(e)",
        "apprenti",
        "apprentie",
        "apprenti(e)",
        "apprentissage"
    ]):
        return "Alternance"

    # -------- 2. STAGE (titre uniquement) --------
    if any(mot in titre_txt for mot in [
        "stage",
        "stagiaire"
    ]):
        return "Stage"

    # -------- 3. typeContratLibelle --------
    if "profession liberale" in type_txt or "freelance" in type_txt or "independant" in type_txt:
        return "Freelance"

    if "interim" in type_txt:
        return "Intérim"

    if "cdi" in type_txt:
        return "CDI"

    if "cdd" in type_txt:
        return "CDD"

    # fallback (rare)
    if "alternance" in type_txt or "apprentissage" in type_txt:
        return "Alternance"

    if "stage" in type_txt:
        return "Stage"

    return "Autre"


def simplifier_experience(experience_libelle, experience_exige=None):
    import re

    texte = str(experience_libelle).lower().strip() if pd.notna(experience_libelle) else ""

    # normalisation
    texte = texte.replace("(", "").replace(")", "")
    texte = texte.replace("an(s)", "ans")
    texte = texte.replace("année", "an").replace("années", "ans")
    texte = " ".join(texte.split())

    # rien de précisé
    if texte == "":
        if str(experience_exige).lower() == "oui":
            return "Expérience exigée non précisée"
        return "Non précisé"

    # débutant
    if (
        "débutant" in texte
        or "debutant" in texte
        or "débutant accepté" in texte
        or "debutant accepte" in texte
        or "sans expérience" in texte
        or "sans experience" in texte
        or texte in ["0 an", "0 ans", "0 mois"]
    ):
        return "Débutant"

    # cas "expérience exigée" sans précision
    if "expérience exigée" in texte or "experience exigee" in texte:
        return "Expérience exigée non précisée"

    # 1) gérer les mois
    match_mois = re.search(r"(\d+)\s*mois", texte)
    if match_mois:
        nb_mois = int(match_mois.group(1))

        if nb_mois == 0:
            return "Débutant"
        elif nb_mois < 12:
            return "Moins de 1 an"
        elif nb_mois == 12:
            return "1 an"
        elif nb_mois <= 24:
            return "1 à 2 ans"
        elif nb_mois <= 59:
            return "3 à 5 ans"
        elif nb_mois <= 119:
            return "6 à 9 ans"
        else:
            return "10 ans et plus"

    # 2) gérer les années
    match_ans = re.search(r"(\d+)\s*an", texte)
    if match_ans:
        nb_ans = int(match_ans.group(1))

        if nb_ans == 0:
            return "Débutant"
        elif nb_ans == 1:
            return "1 an"
        elif nb_ans == 2:
            return "1 à 2 ans"
        elif 3 <= nb_ans <= 5:
            return "3 à 5 ans"
        elif 6 <= nb_ans <= 9:
            return "6 à 9 ans"
        else:
            return "10 ans et plus"

    # si on ne comprend pas, mais expérience exigée = oui
    if str(experience_exige).lower() == "oui":
        return "Expérience exigée non précisée"

    return "Non précisé"


def extraire_salaire_annuel(salaire_text):
    if pd.isna(salaire_text):
        return None

    texte = str(salaire_text).lower().strip()
    texte = texte.replace("\xa0", " ").replace(",", ".")

    # ignorer les salaires horaires
    if "horaire" in texte or "heure" in texte:
        return None

    # détecter le nombre de mois (gère aussi 12.0 mois)
    nb_mois = 12
    match_mois = re.search(r"sur\s+(\d+(?:\.\d+)?)\s+mois", texte)
    if match_mois:
        nb_mois = int(float(match_mois.group(1)))
    else:
        match_mois_simple = re.search(r"(\d+(?:\.\d+)?)\s+mois", texte)
        if match_mois_simple and ("mensuel" in texte or "mensuelle" in texte):
            nb_mois = int(float(match_mois_simple.group(1)))

    # enlever les mentions "sur 12.0 mois", "12.0 mois", etc.
    texte_sans_mois = re.sub(r"sur\s+\d+(?:\.\d+)?\s+mois", "", texte)
    texte_sans_mois = re.sub(r"\d+(?:\.\d+)?\s+mois", "", texte_sans_mois)

    # extraire les montants
    nombres_bruts = re.findall(r"\d[\d\s]*\.?\d*", texte_sans_mois)

    valeurs = []
    for n in nombres_bruts:
        n = n.strip().replace(" ", "")
        if n:
            try:
                valeurs.append(float(n))
            except:
                pass

    if not valeurs:
        return None

    # moyenne si fourchette
    if len(valeurs) >= 2:
        base_valeur = sum(valeurs[:2]) / 2
    else:
        base_valeur = valeurs[0]

    # si annuel
    if "annuel" in texte or "annuelle" in texte:
        return round(base_valeur, 2)

    # si mensuel
    if "mensuel" in texte or "mensuelle" in texte:
        return round(base_valeur * nb_mois, 2)

    return None


def extraire_salaire_mensuel(salaire_text):
    if pd.isna(salaire_text):
        return None

    texte = str(salaire_text).lower().strip()
    texte = texte.replace("\xa0", " ").replace(",", ".")

    # ignorer les salaires horaires
    if "horaire" in texte or "heure" in texte:
        return None

    # détecter le nombre de mois (gère aussi 12.0 mois)
    nb_mois = 12
    match_mois = re.search(r"sur\s+(\d+(?:\.\d+)?)\s+mois", texte)
    if match_mois:
        nb_mois = int(float(match_mois.group(1)))
    else:
        match_mois_simple = re.search(r"(\d+(?:\.\d+)?)\s+mois", texte)
        if match_mois_simple and ("mensuel" in texte or "mensuelle" in texte):
            nb_mois = int(float(match_mois_simple.group(1)))

    # enlever les mentions "sur 12.0 mois", "12.0 mois", etc.
    texte_sans_mois = re.sub(r"sur\s+\d+(?:\.\d+)?\s+mois", "", texte)
    texte_sans_mois = re.sub(r"\d+(?:\.\d+)?\s+mois", "", texte_sans_mois)

    # extraire les montants
    nombres_bruts = re.findall(r"\d[\d\s]*\.?\d*", texte_sans_mois)

    valeurs = []
    for n in nombres_bruts:
        n = n.strip().replace(" ", "")
        if n:
            try:
                valeurs.append(float(n))
            except:
                pass

    if not valeurs:
        return None

    # moyenne si fourchette
    if len(valeurs) >= 2:
        base_valeur = sum(valeurs[:2]) / 2
    else:
        base_valeur = valeurs[0]

    # si mensuel
    if "mensuel" in texte or "mensuelle" in texte:
        return round(base_valeur, 2)

    # si annuel
    if "annuel" in texte or "annuelle" in texte:
        return round(base_valeur / nb_mois, 2)

    return None


def get_access_token():
    token_url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"

    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    response = requests.post(token_url, data=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Erreur token : {response.text}")

    token_data = response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise Exception("Token introuvable")

    return access_token


def get_offres_data(mots_cles="data analyst", nb_pages=1):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    search_url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    all_offres = []

    for i in range(nb_pages):
        start = i * 100
        end = start + 99

        params = {
            "motsCles": mots_cles,
            "range": f"{start}-{end}"
        }

        response = requests.get(search_url, headers=headers, params=params, timeout=30)

        if response.status_code not in [200, 206]:
            raise Exception(
                f"Erreur API offres pour '{mots_cles}' | status={response.status_code} | réponse={response.text}"
            )

        data = response.json()
        offres = data.get("resultats", [])

        # s'il n'y a plus de résultats, on arrête la boucle
        if not offres:
            break

        all_offres.extend(offres)

        # si l'API renvoie moins de 100 offres, inutile de continuer
        if len(offres) < 100:
            break

    if not all_offres:
        return pd.DataFrame()

    df = pd.json_normalize(all_offres)

    colonnes_utiles = [
        "id",
        "intitule",
        "description",
        "dateCreation",
        "dateActualisation",
        "romeCode",
        "romeLibelle",
        "typeContratLibelle",
        "experienceLibelle",
        "lieuTravail.libelle",
        "lieuTravail.commune",
        "lieuTravail.codePostal",
        "salaire.libelle",
        "salaire.commentaire",
        "entreprise.nom",
        "secteurActiviteLibelle"
    ]

    colonnes_existantes = [col for col in colonnes_utiles if col in df.columns]
    df = df[colonnes_existantes].copy()

    df["metier_recherche"] = mots_cles

    if "typeContratLibelle" in df.columns:
        df["type_contrat_simple"] = df.apply(
            lambda row: simplifier_contrat(
                row.get("typeContratLibelle"),
                row.get("intitule")
            ),
            axis=1
        )
    else:
        df["type_contrat_simple"] = "Non précisé"

    df["experience_simple"] = (
        df["experienceLibelle"].apply(simplifier_experience)
        if "experienceLibelle" in df.columns else "Non précisé"
    )

    df["salaire_annuel_estime"] = (
        df["salaire.libelle"].apply(extraire_salaire_annuel)
        if "salaire.libelle" in df.columns else None
    )

    df["salaire_mensuel_estime"] = (
        df["salaire.libelle"].apply(extraire_salaire_mensuel)
        if "salaire.libelle" in df.columns else None
    )

    return df


def get_offres_data_multi():
    metiers = [
        "data analyst",
        "data scientist",
        "data engineer",
        "machine learning engineer",
        "ingenieur ia",
        "power bi",
        "cloud engineer"
    ]

    all_df = []

    for metier in metiers:
        try:
            df = get_offres_data(mots_cles=metier, nb_pages=2)

            if not df.empty:
                all_df.append(df)

        except Exception as e:
            print(f"Erreur pour le métier '{metier}' : {e}")
            continue

    if all_df:
        df_final = pd.concat(all_df, ignore_index=True)

        if "id" in df_final.columns:
            df_final = df_final.drop_duplicates(subset="id")

        return df_final

    return pd.DataFrame()