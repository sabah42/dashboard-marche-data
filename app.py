# =========================
# IMPORTS
# =========================

# Streamlit pour créer l'application web
import streamlit as st

# Plotly Express pour créer les graphiques
import plotly.express as px

# Pandas pour manipuler les données
import pandas as pd

# Base64 pour afficher le logo dans le header
import base64

# JSON pour lire le fichier geojson des départements
import json

# Fonction perso qui récupère les données de l'API France Travail
from src.api_offres import get_offres_data_multi

import streamlit.components.v1 as components
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    # tout ton code Streamlit ici
    st.set_page_config(
        page_title="Marché du travail de la data en France",
        layout="wide"
    )

# =========================
# CONFIGURATION DE LA PAGE
# =========================

# On définit le titre de l'onglet navigateur et on met la page en mode large
st.set_page_config(
    page_title="Marché du travail de la data en France",
    layout="wide"
)
components.html(
    """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-K4JYKF6K5H"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-K4JYKF6K5H');
    </script>
    """,
    height=0,
)

# =========================
# CSS / STYLE VISUEL
# =========================
st.markdown(
    """
    <style>
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        margin-top: 10px;
    }

    .logo-circle {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: white;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        border: 2px solid white;
    }

    .logo-circle img {
        width: 120px;
        height: 120px;
        object-fit: contain;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* Fond général bleu très clair */
[data-testid="stAppViewContainer"] {
    background-color: #eaf4ff;
}

/* On enlève le fond blanc par défaut du header Streamlit */
[data-testid="stHeader"] {
    background: transparent;
}

/* Position du petit menu en haut à droite */
[data-testid="stToolbar"] {
    right: 2rem;
}

/* Marges internes de la zone principale */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0.8rem;
    max-width: 100%;
}

/* Largeur de la sidebar */
section[data-testid="stSidebar"] {
    width: 240px !important;
}

section[data-testid="stSidebar"] > div:first-child {
    width: 240px !important;
}

/* Couleur de fond de la sidebar */
[data-testid="stSidebar"] {
    background: #243C8F;
}

/* Couleur générale du texte dans la sidebar */
[data-testid="stSidebar"] * {
    color: white;
}

/* IMPORTANT :
   On force le texte des labels des filtres en blanc,
   mais on ne force PAS la valeur affichée dans les champs,
   sinon la valeur sélectionnée devient invisible */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* Style des titres dans la sidebar */
.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #dbe7ff;
    margin-bottom: 14px;
}

.sidebar-section {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 14px;
    margin-bottom: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(255,255,255,0.25);
}

/* Bloc du header avec logo */
.logo-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    background: white;
    border-radius: 20px;
    padding: 10px 16px;
    box-shadow: 0 4px 14px rgba(29, 63, 143, 0.08);
    margin-bottom: 14px;
    width: 100%;
}

/* Taille du logo */
.logo-box img {
    height: 64px;
}

/* Texte principal du header */
.logo-text {
    font-size: 18px;
    font-weight: 700;
    color: #1d3f8f;
}

/* Sous-texte du header */
.logo-subtext {
    font-size: 13px;
    color: #5b6785;
}

/* Carte KPI */
.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 10px 14px;
    box-shadow: 0 4px 14px rgba(29, 63, 143, 0.08);
    border-left: 6px solid #1d70b8;
    text-align: left;
    margin-bottom: 8px;
    min-height: 76px;
}

/* Titre du KPI */
.kpi-title {
    font-size: 12px;
    color: #5b6785;
    margin-bottom: 6px;
    font-weight: 600;
}

/* Valeur du KPI */
.kpi-value {
    font-size: 18px;
    font-weight: 700;
    color: #1d3f8f;
}

/* Carte du tableau ancienne version */
.table-card {
    background: white;
    border-radius: 20px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(29, 63, 143, 0.08);
    margin-top: 10px;
    height: 320px;
    display: flex;
    flex-direction: column;
}

/* Nouveau bloc table HTML */
.html-table-card {
    background: white;
    border-radius: 20px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(29, 63, 143, 0.08);
    height: 320px;
    overflow: hidden;
}

.html-table-wrapper {
    max-height: 250px;
    overflow-y: auto;
    border-radius: 12px;
}

.html-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    background: white;
}

.html-table th {
    text-align: left;
    padding: 10px;
    background: #f4f7fb;
    color: #1d3f8f;
    border-bottom: 1px solid #d9e2f0;
    position: sticky;
    top: 0;
}

.html-table td {
    padding: 10px;
    border-bottom: 1px solid #eef2f7;
    color: #222;
    vertical-align: top;
}

/* Style des selectbox */
div[data-testid="stSelectbox"] > div {
    background-color: white;
    border-radius: 12px;
}

/* IMPORTANT :
   On remet le texte des valeurs de filtre en noir
   pour voir ce qu'on sélectionne */
div[data-baseweb="select"] * {
    color: black !important;
}

/* Style du dataframe */
div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 18px;
}

/* Espace horizontal entre les blocs */
div[data-testid="stHorizontalBlock"] {
    gap: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOGO SIDEBAR + HEADER
# =========================

# Chemin du logo dans ton projet
logo_path = "france_travail_logo.png"

# On lit le fichier image en binaire
with open(logo_path, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

# Logo dans la sidebar
with st.sidebar:
    st.markdown(
        f"""
        <div class="logo-container">
            <div class="logo-circle">
                <img src="data:image/png;base64,{logo_base64}" />
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Header sans logo, avec nom à droite
st.markdown(
    """
    <div class="logo-box">
        <div>
            <div class="logo-text">Marché du travail de la data en France</div>
            <div class="logo-subtext">Dashboard connecté à l'API France Travail</div>
        </div>
        <div style="font-size: 13px; color: #5b6785; white-space: nowrap; text-align: right;">
            Sabah Assas
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CHARGEMENT AUTOMATIQUE DES DONNÉES
# =========================

# Si les données ne sont pas encore dans la session
if "df_data" not in st.session_state:
    # On affiche un message de chargement
    with st.spinner("Chargement des offres en cours..."):
        try:
            # On appelle l'API et on stocke le résultat
            st.session_state.df_data = get_offres_data_multi()
        except Exception as e:
            # En cas d'erreur, on met un DataFrame vide
            st.session_state.df_data = pd.DataFrame()
            st.error(f"Erreur détaillée : {e}")

# On récupère les données depuis la session
df = st.session_state.df_data


# =========================
# CHARGEMENT DES DÉPARTEMENTS
# =========================

# On charge la table propre des départements
df_dep = pd.read_csv(
    "data/processed/departements_clean.csv",
    dtype={"code_departement": str}
)

# On charge le fichier geojson de la carte des départements
with open("data/raw/departements.geojson", "r", encoding="utf-8") as f:
    geojson_departements = json.load(f)


# =========================
# FONCTION : EXTRAIRE LE DÉPARTEMENT DEPUIS LE CODE POSTAL
# =========================

def get_departement(cp):
    """
    Cette fonction extrait le département depuis le code postal.
    Exemple :
    42000 -> 42
    75012 -> 75
    97100 -> 971
    """

    # Si le code postal est vide
    if pd.isna(cp):
        return None

    # Conversion en texte + nettoyage
    cp = str(cp).strip().replace(".0", "")

    # Si la chaîne est vide après nettoyage
    if cp == "":
        return None

    # On remet sur 5 caractères
    cp = cp.zfill(5)

    # Cas DOM / TOM : 971, 972, 973...
    if cp.startswith(("97", "98")):
        return cp[:3]

    # Cas général : on prend les 2 premiers caractères
    return cp[:2]


# =========================
# FONCTION POUR STYLISER LES GRAPHIQUES
# =========================

def apply_chart_style(fig, title, bleu_fonce):
    """
    Cette fonction applique un style commun à tous les graphiques.
    Ça évite de répéter le même code partout.
    """

    fig.update_layout(
        # Titre à l'intérieur du bloc blanc, aligné à gauche
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=16, color=bleu_fonce)
        ),

        # Fond blanc pour la carte Plotly
        paper_bgcolor="white",
        plot_bgcolor="white",

        # Marges internes
        margin=dict(l=10, r=10, t=55, b=10),

        # Taille globale du texte
        font=dict(size=11),
    )

    return fig


# =========================
# AFFICHAGE DU DASHBOARD
# =========================

# Si df existe
if df is not None:

    # Si df est vide
    if df.empty:
        st.warning("Aucune offre trouvée.")

    else:
        # =========================
        # SIDEBAR
        # =========================
        with st.sidebar:
            

            # Bloc navigation
            st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

            # Choix de la page
            page_selectionnee = st.radio(
                "Aller vers",
                ["Vue globale", "Analyse salaires", "Évolution temporelle"],
                label_visibility="collapsed"
            )

            # Bloc filtres
            st.markdown('<div class="sidebar-section">Filtres</div>', unsafe_allow_html=True)

            # Liste des métiers disponibles
            metiers = ["Tous"] + sorted(df["metier_recherche"].dropna().unique().tolist())
            metier_selectionne = st.selectbox("Métier", metiers)

            # Liste des contrats disponibles
            contrats = ["Tous"] + sorted(df["type_contrat_simple"].dropna().unique().tolist())
            contrat_selectionne = st.selectbox("Type de contrat", contrats)

            # Liste des expériences disponibles
            experiences = ["Tous"] + sorted(df["experience_simple"].dropna().unique().tolist())
            experience_selectionnee = st.selectbox("Expérience", experiences)

        # =========================
        # FILTRAGE DES DONNÉES
        # =========================

        # On fait une copie du DataFrame
        df_filtre = df.copy()

        # Création de la colonne département depuis le code postal
        if "lieuTravail.codePostal" in df_filtre.columns:
            df_filtre["departement"] = df_filtre["lieuTravail.codePostal"].apply(get_departement)
        else:
            df_filtre["departement"] = None

        # Filtre métier
        if metier_selectionne != "Tous":
            df_filtre = df_filtre[df_filtre["metier_recherche"] == metier_selectionne]

        # Filtre contrat
        if contrat_selectionne != "Tous":
            df_filtre = df_filtre[df_filtre["type_contrat_simple"] == contrat_selectionne]

        # Filtre expérience
        if experience_selectionnee != "Tous":
            df_filtre = df_filtre[df_filtre["experience_simple"] == experience_selectionnee]

        # =========================
        # KPI CALCULÉS
        # =========================

        # Nombre d'offres du jour
        if "dateCreation" in df_filtre.columns:
    # Conversion de la colonne en datetime
         df_filtre["dateCreation"] = pd.to_datetime(df_filtre["dateCreation"], errors="coerce")

    # On compare seulement la partie date
         date_du_jour = pd.Timestamp.now().date()

         nb_offres_auj = (
          df_filtre["dateCreation"].dt.date == date_du_jour
         ).sum()
        else:
         nb_offres_auj = 0
        # Nombre de départements distincts
        nb_departements = df_filtre["departement"].nunique() if "departement" in df_filtre.columns else 0

        # Nombre d'entreprises
        nb_entreprises = df_filtre["entreprise.nom"].nunique() if "entreprise.nom" in df_filtre.columns else 0

# =========================
# KPI SALAIRES
# =========================
        if "salaire_annuel_estime" in df_filtre.columns:
            salaire_brut = df_filtre["salaire_annuel_estime"]

            # garder seulement les salaires valides
            salaire_series = salaire_brut.dropna()
            salaire_series = salaire_series[(salaire_series > 0) & (salaire_series <= 150000)]

            nb_offres_avec_salaire = salaire_series.count()
            nb_offres_sans_salaire = salaire_brut.isna().sum()
        else:
            salaire_series = pd.Series(dtype=float)
            nb_offres_avec_salaire = 0
            nb_offres_sans_salaire = len(df_filtre)

        # Moyenne
        salaire_moyen = int(salaire_series.mean()) if not salaire_series.empty else None
        salaire_moyen_affiche = f"{salaire_moyen:,.0f} €".replace(",", " ") if salaire_moyen is not None else "N/D"
        # Median
        salaire_median = int(salaire_series.median()) if not salaire_series.empty else None
        salaire_median_affiche = f"{salaire_median:,.0f} €".replace(","," ") if salaire_median is not None else "N/D"
        # Minimum
        salaire_min = int(salaire_series.min()) if not salaire_series.empty else None
        salaire_min_affiche = f"{salaire_min:,.0f} €".replace(",", " ") if salaire_min is not None else "N/D"

        # Maximum
        salaire_max = int(salaire_series.max()) if not salaire_series.empty else None
        salaire_max_affiche = f"{salaire_max:,.0f} €".replace(",", " ") if salaire_max is not None else "N/D"

        # Comptages
        nb_offres_avec_salaire_affiche = f"{nb_offres_avec_salaire:,}".replace(",", " ")
        nb_offres_sans_salaire_affiche = f"{nb_offres_sans_salaire:,}".replace(",", " ")
        # =========================
        # COULEURS
        # =========================

        bleu_fonce = "#243C8F"
        bleu_moyen = "#1F8FD5"
        bleu_clair = "#4DB7E5"
        rose = "#E7A6C8"
        rouge = "#E53935"
        jaune = "#F4D03F"

        # =========================
        # PAGE 1 : VUE GLOBALE
        # =========================

        if page_selectionnee == "Vue globale":

            # Ligne de KPI
            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Nombre d'offres</div>
                    <div class="kpi-value">{len(df_filtre)}</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Offres aujourd'hui</div>
                    <div class="kpi-value">{int(nb_offres_auj)}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Départements</div>
                    <div class="kpi-value">{nb_departements}</div>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Entreprises</div>
                    <div class="kpi-value">{nb_entreprises}</div>
                </div>
                """, unsafe_allow_html=True)

            with c5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Salaire annuel moyen</div>
                    <div class="kpi-value">{salaire_moyen_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            # =========================
            # PRÉPARATION DES DONNÉES DÉPARTEMENT
            # =========================

            # On calcule le nombre d'offres par département
            df_dep_map = (
                df_filtre.groupby("departement", dropna=True)
                .agg(nb_offres=("id", "count"))
                .reset_index()
            )

            # On joint avec la table des départements pour récupérer le nom
            df_dep_map = df_dep_map.merge(
                df_dep,
                left_on="departement",
                right_on="code_departement",
                how="left"
            )

            # =========================
            # LIGNE 1 : métier | table des offres | contrat
            # =========================
            g1, g_table, g2 = st.columns(3)

            # ----- Graphique 1 : offres par métier
            with g1:
                metier_counts = df_filtre["metier_recherche"].value_counts().reset_index()
                metier_counts.columns = ["metier", "nb"]

                fig1 = px.bar(
                    metier_counts,
                    x="metier",
                    y="nb",
                    text="nb",
                    height=320
                )

                fig1.update_traces(
                    marker_color=bleu_moyen,
                    textposition="outside"
                )

                fig1.update_layout(
                    xaxis_title="Métier",
                    yaxis_title="Nombre d'offres",
                    showlegend=False
                )

                fig1 = apply_chart_style(fig1, "Offres par métier", bleu_fonce)
                st.plotly_chart(fig1, use_container_width=True, key="graph_metier")

            # ----- Bloc 2 : table des offres (version HTML pour rester dans le bloc)
            with g_table:
                colonnes_table = [
                    col for col in [
                        "intitule",
                        "lieuTravail.libelle",
                        "type_contrat_simple",
                        "experience_simple",
                        "salaire_annuel_estime"
                    ] if col in df_filtre.columns
                ]

                df_table = df_filtre[colonnes_table].head(10).copy()

                rename_map = {
                    "intitule": "Intitulé",
                    "lieuTravail.libelle": "Lieu",
                    "type_contrat_simple": "Contrat",
                    "experience_simple": "Expérience",
                    "salaire_annuel_estime": "Salaire annuel"
                }
                df_table = df_table.rename(columns=rename_map)

                if "Salaire annuel" in df_table.columns:
                    df_table["Salaire annuel"] = df_table["Salaire annuel"].apply(
                        lambda x: f"{int(x):,} €".replace(",", " ") if pd.notna(x) else ""
                    )

                table_html = df_table.to_html(index=False, classes="html-table", escape=False)

                st.markdown(
                    f"""
                    <div class="html-table-card">
                        <div style="font-size:16px;font-weight:700;color:{bleu_fonce};margin-bottom:10px;">
                            Table des offres
                        </div>
                        <div class="html-table-wrapper">
                            {table_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ----- Graphique 3 : type de contrat
            with g2:
                contrat_counts = df_filtre["type_contrat_simple"].value_counts().reset_index()
                contrat_counts.columns = ["contrat", "nb"]

                fig2 = px.pie(
                    contrat_counts,
                    names="contrat",
                    values="nb",
                    hole=0.45,
                    height=320,
                    color_discrete_sequence=[
                        bleu_fonce,
                        bleu_moyen,
                        bleu_clair,
                        rose,
                        rouge,
                        jaune
                    ]
                )

                fig2.update_traces(
                    textposition="inside",
                    textinfo="percent+label"
                )

                fig2.update_layout(
                    legend_title="Type de contrat"
                )

                fig2 = apply_chart_style(fig2, "Type de contrat", bleu_fonce)
                st.plotly_chart(fig2, use_container_width=True, key="graph_contrat")

            # =========================
            # LIGNE 2 : expérience | carte | top départements
            # =========================
            g3, g4, g5 = st.columns(3)

            # ----- Graphique 4 : expérience
            with g3:
                exp_counts = df_filtre["experience_simple"].value_counts().reset_index()
                exp_counts.columns = ["experience", "nb"]

                ordre_exp = [
                    "Débutant",
                    "Moins de 1 an",
                    "1 an",
                    "1 à 2 ans",
                    "3 à 5 ans",
                    "6 à 9 ans",
                    "10 ans et plus",
                    "Expérience exigée non précisée",
                    "Non précisé"
                ]

                exp_counts["experience"] = pd.Categorical(
                    exp_counts["experience"],
                    categories=ordre_exp,
                    ordered=True
                )

                exp_counts = exp_counts.sort_values("experience")

                fig3 = px.bar(
                    exp_counts,
                    y="experience",
                    x="nb",
                    text="nb",
                    orientation="h",
                    height=320
                )

                fig3.update_traces(
                    marker_color=bleu_clair,
                    textposition="outside"
                )

                fig3.update_layout(
                    xaxis_title="Nombre d'offres",
                    yaxis_title="Expérience",
                    showlegend=False
                )

                fig3 = apply_chart_style(fig3, "Offres par expérience", bleu_fonce)
                st.plotly_chart(fig3, use_container_width=True, key="graph_experience")

            # ----- Graphique 5 : carte choropleth par département
            with g4:
                fig_map = px.choropleth(
                    df_dep_map,
                    geojson=geojson_departements,
                    locations="departement",
                    featureidkey="properties.code",
                    color="nb_offres",
                    hover_name="nom_departement",
                    color_continuous_scale="Blues",
                    height=320
                )

                fig_map.update_geos(
                    fitbounds="locations",
                    visible=False
                )

                fig_map = apply_chart_style(fig_map, "Offres par département", bleu_fonce)
                st.plotly_chart(fig_map, use_container_width=True, key="graph_map")

            # ----- Graphique 6 : top départements
            with g5:
                # On prend les 10 départements avec le plus d'offres
                df_dep_top = (
                    df_filtre.groupby("departement", dropna=True)
                    .agg(nb=("id", "count"))
                    .reset_index()
                    .sort_values("nb", ascending=False)
                    .head(10)
                )

                # On récupère le nom du département
                df_dep_top = df_dep_top.merge(
                    df_dep,
                    left_on="departement",
                    right_on="code_departement",
                    how="left"
                )

                # On trie pour affichage horizontal propre
                df_dep_top = df_dep_top.sort_values("nb", ascending=True)

                fig_top = px.bar(
                    df_dep_top,
                    y="nom_departement",
                    x="nb",
                    orientation="h",
                    text="nb",
                    height=320
                )

                fig_top.update_traces(
                    marker_color=bleu_fonce,
                    textposition="outside"
                )

                fig_top.update_layout(
                    xaxis_title="Offres",
                    yaxis_title="Département",
                    showlegend=False
                )

                fig_top = apply_chart_style(fig_top, "Top départements", bleu_fonce)
                st.plotly_chart(fig_top, use_container_width=True, key="graph_top_departements")

        # =========================
        # PAGE 2 : ANALYSE SALAIRES
        # =========================
        elif page_selectionnee == "Analyse salaires":
            # Données salaires filtrées
            df_salaires = df_filtre[
                (df_filtre["salaire_annuel_estime"].notna()) &
                (df_filtre["salaire_annuel_estime"] > 0) &
                (df_filtre["salaire_annuel_estime"] <= 150000)
            ].copy()

            # =========================
            # KPI
            # =========================
            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Salaire annuel médian</div>
                    <div class="kpi-value">{salaire_median_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Salaire annuel min</div>
                    <div class="kpi-value">{salaire_min_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Salaire annuel max</div>
                    <div class="kpi-value">{salaire_max_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Offres avec salaire</div>
                    <div class="kpi-value">{nb_offres_avec_salaire_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Offres sans salaire</div>
                    <div class="kpi-value">{nb_offres_sans_salaire_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            # =========================
            # BLOC 1 : métier + boxplot
            # =========================
            col1, col2 = st.columns(2)

            if not df_salaires.empty:
                # Salaire médian par métier
                salaire_par_metier = df_salaires.groupby(
                    "metier_recherche",
                    as_index=False
                )["salaire_annuel_estime"].median()

                fig_salaire = px.bar(
                    salaire_par_metier,
                    x="metier_recherche",
                    y="salaire_annuel_estime",
                    text="salaire_annuel_estime",
                    height=320
                )

                fig_salaire.update_traces(
                    marker_color=bleu_moyen,
                    texttemplate="%{text:.0f}",
                    textposition="outside"
                )

                fig_salaire.update_layout(
                    xaxis_title="Métier",
                    yaxis_title="Salaire annuel médian",
                    showlegend=False
                )

                fig_salaire = apply_chart_style(
                    fig_salaire,
                    "Salaire médian par métier",
                    bleu_fonce
                )

                # Boxplot
                fig_box = px.box(
                    df_salaires,
                    y="salaire_annuel_estime",
                    points="outliers",
                    height=320
                )

                fig_box.update_traces(
                    marker_color=bleu_fonce
                )

                fig_box.update_layout(
                    xaxis_title="",
                    yaxis_title="Salaire annuel",
                    showlegend=False
                )

                fig_box.update_yaxes(range=[0, 120000])

                fig_box = apply_chart_style(
                    fig_box,
                    "Distribution des salaires annuels",
                    bleu_fonce
                )

                with col1:
                    st.plotly_chart(fig_salaire, use_container_width=True)

                with col2:
                    st.plotly_chart(fig_box, use_container_width=True)

            else:
                with col1:
                    st.info("Pas assez d'informations salaire pour afficher ce graphique.")

                with col2:
                    st.info("Pas assez d'informations salaire pour afficher la distribution des salaires.")

            # =========================
            # BLOC 2 : expérience + carte + top départements
            # =========================
            col3, col4, col5 = st.columns(3)

            with col3:
                if not df_salaires.empty:
                    salaire_par_experience = df_salaires.groupby(
                        "experience_simple",
                        as_index=False
                    )["salaire_annuel_estime"].median()

                    salaire_par_experience = salaire_par_experience.sort_values(
                        by="salaire_annuel_estime",
                        ascending=True
                    )

                    fig_exp = px.bar(
                        salaire_par_experience,
                        x="salaire_annuel_estime",
                        y="experience_simple",
                        orientation="h",
                        text="salaire_annuel_estime",
                        height=320
                    )

                    fig_exp.update_traces(
                        marker_color=bleu_clair,
                        texttemplate="%{text:.0f}",
                        textposition="outside"
                    )

                    fig_exp.update_layout(
                        xaxis_title="Salaire médian",
                        yaxis_title="Expérience",
                        showlegend=False
                    )

                    fig_exp = apply_chart_style(
                        fig_exp,
                        "Salaire médian par expérience",
                        bleu_fonce
                    )

                    st.plotly_chart(fig_exp, use_container_width=True)

                else:
                    st.info("Pas assez d'informations.")

            with col4:
                if not df_salaires.empty:
                    df_dep_salaire = (
                        df_salaires.groupby("departement", dropna=True)
                        .agg(salaire_median=("salaire_annuel_estime", "median"))
                        .reset_index()
                    )

                    df_dep_salaire = df_dep_salaire.merge(
                        df_dep,
                        left_on="departement",
                        right_on="code_departement",
                        how="left"
                    )

                    fig_map = px.choropleth(
                        df_dep_salaire,
                        geojson=geojson_departements,
                        locations="departement",
                        featureidkey="properties.code",
                        color="salaire_median",
                        hover_name="nom_departement",
                        color_continuous_scale="Blues",
                        height=320
                    )

                    fig_map.update_geos(
                        fitbounds="locations",
                        visible=False
                    )

                    fig_map = apply_chart_style(
                        fig_map,
                        "Salaire médian par département",
                        bleu_fonce
                    )

                    st.plotly_chart(fig_map, use_container_width=True, key="graph_map_salaire")

                else:
                    st.info("Pas assez d'informations.")

            with col5:
                if not df_salaires.empty:
                    df_dep_top = (
                        df_salaires.groupby("departement", dropna=True)
                        .agg(salaire_median=("salaire_annuel_estime", "median"))
                        .reset_index()
                    )

                    df_dep_top = df_dep_top.merge(
                        df_dep,
                        left_on="departement",
                        right_on="code_departement",
                        how="left"
                    )

                    df_dep_top = df_dep_top.sort_values(
                        "salaire_median",
                        ascending=False
                    ).head(10)

                    df_dep_top = df_dep_top.sort_values(
                        "salaire_median",
                        ascending=True
                    )

                    fig_dept = px.bar(
                        df_dep_top,
                        y="nom_departement",
                        x="salaire_median",
                        orientation="h",
                        text="salaire_median",
                        height=320
                    )

                    fig_dept.update_traces(
                        marker_color=bleu_fonce,
                        texttemplate="%{text:.0f}",
                        textposition="outside"
                    )

                    fig_dept.update_layout(
                        xaxis_title="Salaire médian",
                        yaxis_title="",
                        showlegend=False
                    )

                    fig_dept = apply_chart_style(
                        fig_dept,
                        "Top départements",
                        bleu_fonce
                    )

                    st.plotly_chart(fig_dept, use_container_width=True, key="graph_top_departements_salaire")

                else:
                    st.info("Pas assez d'informations.")

        # =========================
        # PAGE 3 : ÉVOLUTION TEMPORELLE
        # =========================
        elif page_selectionnee == "Évolution temporelle":
            df_marche = df_filtre.copy()

            # Sécuriser la date
            if "dateCreation" in df_marche.columns:
                df_marche["dateCreation"] = pd.to_datetime(
                    df_marche["dateCreation"],
                    errors="coerce",
                    utc=True
                )
                df_marche = df_marche[df_marche["dateCreation"].notna()].copy()

                date_ref = pd.Timestamp.now(tz="UTC").normalize()

                df_marche["date_only"] = df_marche["dateCreation"].dt.date
                df_marche["jour_semaine"] = df_marche["dateCreation"].dt.day_name()
            else:
                df_marche = pd.DataFrame()

            if not df_marche.empty:
                date_max = df_marche["dateCreation"].max().date()

                nb_total_offres_marche = len(df_marche)

                nb_7j = (
                    df_marche["dateCreation"] >= (date_ref - pd.Timedelta(days=7))
                ).sum()

                nb_30j = (
                    df_marche["dateCreation"] >= (date_ref - pd.Timedelta(days=30))
                ).sum()

                part_7j = round((nb_7j / nb_total_offres_marche) * 100, 1) if nb_total_offres_marche > 0 else 0

                date_plus_recente = date_max.strftime("%d/%m/%Y")

                part_7j_affiche = f"{part_7j}%"
                nb_7j_affiche = f"{nb_7j:,}".replace(",", " ")
                nb_30j_affiche = f"{nb_30j:,}".replace(",", " ")
                nb_total_offres_marche_affiche = f"{nb_total_offres_marche:,}".replace(",", " ")
            else:
                nb_total_offres_marche_affiche = "0"
                nb_7j_affiche = "0"
                nb_30j_affiche = "0"
                part_7j_affiche = "0%"
                date_plus_recente = "N/D"

            # =========================
            # KPI
            # =========================
            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Offres observées</div>
                    <div class="kpi-value">{nb_total_offres_marche_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Publications sur 7 jours</div>
                    <div class="kpi-value">{nb_7j_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Publications sur 30 jours</div>
                    <div class="kpi-value">{nb_30j_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Part des 7 derniers jours</div>
                    <div class="kpi-value">{part_7j_affiche}</div>
                </div>
                """, unsafe_allow_html=True)

            with c5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Dernière publication</div>
                    <div class="kpi-value">{date_plus_recente}</div>
                </div>
                """, unsafe_allow_html=True)

            if not df_marche.empty:
                st.info(
                    "Cette page analyse la dynamique des dates de publication des offres présentes dans l'extraction actuelle. "
                    "Elle décrit l'évolution observée des annonces actives, et non un historique exhaustif du marché."
                )

                # =========================
                # BLOC 1 : cumul + évolution par métier
                # =========================
                g1, g2 = st.columns(2)

                # Cumul des offres
                df_jour = (
                    df_marche.groupby("date_only")
                    .agg(nb_offres=("id", "count"))
                    .reset_index()
                    .sort_values("date_only")
                )

                df_jour["cumul_offres"] = df_jour["nb_offres"].cumsum()

                fig_cumul = px.line(
                    df_jour,
                    x="date_only",
                    y="cumul_offres",
                    markers=False,
                    height=300
                )

                fig_cumul.update_traces(
                    line_color=bleu_fonce
                )

                fig_cumul.update_layout(
                    xaxis_title="Date de publication",
                    yaxis_title="Cumul des offres",
                    showlegend=False
                )

                fig_cumul = apply_chart_style(
                    fig_cumul,
                    "Cumul des offres observées",
                    bleu_fonce
                )

                # Évolution par métier : limiter aux 5 métiers les plus publiés
                top_metiers = (
                    df_marche["metier_recherche"]
                    .value_counts()
                    .head(5)
                    .index
                )

                df_evol_metier = (
                    df_marche[df_marche["metier_recherche"].isin(top_metiers)]
                    .groupby(["date_only", "metier_recherche"])
                    .agg(nb_offres=("id", "count"))
                    .reset_index()
                    .sort_values("date_only")
                )

                fig_evol_metier = px.line(
                    df_evol_metier,
                    x="date_only",
                    y="nb_offres",
                    color="metier_recherche",
                    markers=False,
                    height=300
                )

                fig_evol_metier.update_layout(
                    xaxis_title="Date de publication",
                    yaxis_title="Nombre d'offres",
                    legend_title="Métier"
                )

                fig_evol_metier = apply_chart_style(
                    fig_evol_metier,
                    "Évolution des publications par métier",
                    bleu_fonce
                )

                with g1:
                    st.plotly_chart(fig_cumul, use_container_width=True, key="graph_cumul_offres")

                with g2:
                    st.plotly_chart(fig_evol_metier, use_container_width=True, key="graph_evol_metier")

                # =========================
                # BLOC 2 : rythme hebdo / métiers récents / villes récentes
                # =========================
                g3, g4, g5 = st.columns(3)

                # Répartition par jour de semaine
                ordre_jours = [
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"
                ]

                traduction_jours = {
                    "Monday": "Lundi",
                    "Tuesday": "Mardi",
                    "Wednesday": "Mercredi",
                    "Thursday": "Jeudi",
                    "Friday": "Vendredi",
                    "Saturday": "Samedi",
                    "Sunday": "Dimanche"
                }

                df_weekday = (
                    df_marche.groupby("jour_semaine")
                    .agg(nb_offres=("id", "count"))
                    .reset_index()
                )

                df_weekday["ordre"] = df_weekday["jour_semaine"].apply(
                    lambda x: ordre_jours.index(x) if x in ordre_jours else 99
                )
                df_weekday = df_weekday.sort_values("ordre")
                df_weekday["jour_fr"] = df_weekday["jour_semaine"].map(traduction_jours)

                fig_weekday = px.bar(
                    df_weekday,
                    x="jour_fr",
                    y="nb_offres",
                    text="nb_offres",
                    height=280
                )

                fig_weekday.update_traces(
                    marker_color=bleu_fonce,
                    textposition="outside"
                )

                fig_weekday.update_layout(
                    xaxis_title="Jour de publication",
                    yaxis_title="Nombre d'offres",
                    showlegend=False
                )

                fig_weekday = apply_chart_style(
                    fig_weekday,
                    "Rythme de publication par jour",
                    bleu_fonce
                )

                # Top métiers récents (30 derniers jours)
                df_recent_30 = df_marche[
                    df_marche["dateCreation"] >= (date_ref - pd.Timedelta(days=30))
                ].copy()

                df_metiers_recent = (
                    df_recent_30.groupby("metier_recherche")
                    .agg(nb_offres=("id", "count"))
                    .reset_index()
                    .sort_values("nb_offres", ascending=False)
                    .head(8)
                    .sort_values("nb_offres", ascending=True)
                )

                fig_metiers_recent = px.bar(
                    df_metiers_recent,
                    y="metier_recherche",
                    x="nb_offres",
                    orientation="h",
                    text="nb_offres",
                    height=280
                )

                fig_metiers_recent.update_traces(
                    marker_color=bleu_clair,
                    textposition="outside"
                )

                fig_metiers_recent.update_layout(
                    xaxis_title="Offres publiées",
                    yaxis_title="Métier",
                    showlegend=False
                )

                fig_metiers_recent = apply_chart_style(
                    fig_metiers_recent,
                    "Métiers les plus publiés (30 jours)",
                    bleu_fonce
                )

                # Top villes récentes
                if "lieuTravail.libelle" in df_recent_30.columns:
                    df_villes_recent = (
                        df_recent_30.groupby("lieuTravail.libelle")
                        .agg(nb_offres=("id", "count"))
                        .reset_index()
                        .sort_values("nb_offres", ascending=False)
                        .head(8)
                        .sort_values("nb_offres", ascending=True)
                    )
                else:
                    df_villes_recent = pd.DataFrame(columns=["lieuTravail.libelle", "nb_offres"])

                fig_villes_recent = px.bar(
                    df_villes_recent,
                    y="lieuTravail.libelle",
                    x="nb_offres",
                    orientation="h",
                    text="nb_offres",
                    height=280
                )

                fig_villes_recent.update_traces(
                    marker_color=bleu_clair,
                    textposition="outside"
                )

                fig_villes_recent.update_layout(
                    xaxis_title="Offres publiées",
                    yaxis_title="Ville",
                    showlegend=False
                )

                fig_villes_recent = apply_chart_style(
                    fig_villes_recent,
                    "Villes les plus actives (30 jours)",
                    bleu_fonce
                )

                with g3:
                    st.plotly_chart(fig_weekday, use_container_width=True, key="graph_jour_semaine")

                with g4:
                    st.plotly_chart(fig_metiers_recent, use_container_width=True, key="graph_metiers_recent")

                with g5:
                    st.plotly_chart(fig_villes_recent, use_container_width=True, key="graph_villes_recent")

            else:
                st.info("Pas assez d'informations pour analyser l'évolution du marché.")