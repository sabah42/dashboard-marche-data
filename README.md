# Analyse du marché de la data en France (API France Travail)
## Table des matières

- [Description du projet](#description-du-projet)
- [Objectifs du projet](#objectifs-du-projet)
* [Données et source](#données-et-source)
- [Contenu du projet](#contenu-du-projet)
- [Structure du projet](#structure-du-projet)
- [Étapes principales](#étapes-principales)
- [Description du tableau de bord](#Description-du-tableau-de-bord)
- [Principaux insights](#principaux-insights)
- [Compétences utilisées](#compétences-utilisées)
- [Résultats](#résultats)

---

## Description du projet

Ce projet propose une analyse du marché de l’emploi dans le domaine de la data en France à partir des données de l’API France Travail.

L’objectif est de comprendre :

- la demande en métiers data,
- la répartition géographique des offres,
- les niveaux de salaire,
- les exigences en expérience et type de contrat.

> Ce projet s’inscrit dans une logique d’aide à la décision pour les candidats et les acteurs du marché de la data.

---

## Objectifs du projet

### Objectifs analytiques

- Analyser la demande des métiers data en France 
- Étudier la répartition des offres par métier
- Comprendre les niveaux de salaire selon le métier et l’expérience
- Identifier les zones géographiques les plus dynamiques
- Analyser les types de contrats proposés

### Objectifs personnels

- Travailler avec une API réelle (France Travail)
- Automatiser la collecte de données
- Construire un dashboard interactif avec Streamlit
- Transformer des données brutes en insights métier
  
---

## Données et source

Source principale : API France Travail (offres d’emploi)

Données utilisées

- Intitulé du poste
- Type de contrat
- Expérience requise
- Salaire (libellé brut)
- Localisation
- Entreprise
- Dates de publication
  
### Remarque

Les données sont récupérées en temps réel via l’API.

Certaines informations (notamment les salaires) peuvent être absentes ou hétérogènes.
 
---

## Contenu du projet

Le projet comprend :

- la récupération des données via API (Python)
- le nettoyage et la transformation des données
- l’extraction et normalisation des salaires
- la création de variables analytiques (contrat, expérience)
- la création d’un dashboard interactif (Streamlit)
  
---

## Structure du projet
dashboard-marche-data/
│

├── data/                 # Données (optionnel si stockage local)

│
├── src/                  # Code source

│   └── api_offres.py     # Récupération et traitement des données API

│
├── .streamlit/           # Configuration Streamlit

│
├── app.py                # Application principale Streamlit

├── requirements.txt      # Dépendances

├── .gitignore            # Fichiers ignorés (dont .env)

├── README.md             # Documentation du projet

---

## Étapes principales

1. Connexion à l’API France Travail (OAuth2)
2. Récupération des offres d’emploi (Python)
3. Nettoyage et transformation des données
4. Normalisation des salaires (annuel / mensuel)
5. Création de variables analytiques
6. Construction du dashboard Streamlit
7. Déploiement en ligne

---

## Description du tableau de bord

### Page 1 – Vue globale

- Nombre d’offres
- Nombre d’entreprises
- Nombre de départements
- Salaire moyen

Objectif : avoir une vision générale du marché.

---

### Page 2 – Analyse des salaires

- Salaire médian, min, max
- Distribution des salaires
- Salaire par métier
- Salaire par expérience
- Salaire par département

Objectif : comprendre les différences de rémunération.

---

### Page 3 – Évolution temporelle

- Nombre d’offres sur 7 et 30 jours
- Évolution des publications
- Rythme de publication par jour
- Métiers les plus publiés

Objectif : analyser la dynamique du marché.

---

## Principaux insights

- Le métier de Data Analyst est le plus demandé
- Les contrats CDI dominent largement le marché
- Une forte concentration des offres en Île-de-France
- Les salaires varient fortement selon :
   - le métier
   - l’expérience
   - la localisation
- Une grande partie des offres ne mentionne pas de salaire

---

## Compétences utilisées

- Python (requests, pandas)
- API REST (authentification OAuth2)
- Data cleaning & feature engineering
- Streamlit (dashboard interactif)
- Git / GitHub (versioning)
- Déploiement cloud (Streamlit Cloud)
  
---

## Résultats
Dashboard interactif en ligne
Données actualisées automatiquement via API
Analyse complète du marché de la data en France

👉 Lien du projet : https://dashboard-marche-data.streamlit.app/

---

## Auteur

Sabah ASSAS
