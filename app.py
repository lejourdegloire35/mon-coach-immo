# -*- coding: utf-8 -*-
# app.py — Mon Coach Prêt Immo (base propre, robuste)

import streamlit as st

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(page_title="Coach Pret Immo", page_icon="🏠", layout="wide")

# -----------------------------
# Données communes
# -----------------------------
STATUTS = [
    "CDI", "CDD", "CDIC", "Intérim", "Intermittent", "Saisonnier",
    "Militaire", "Stagiaire FP", "Assistante maternelle", "Apprenti",
    "Pompier volontaire", "Élu", "Multi-contrats", "Famille d'accueil",
]

DOCS_PAR_STATUT = {
    "CDI": [
        "Contrat de travail en CDI",
        "3 derniers bulletins de salaire",
        "Dernier avis d'imposition",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "CDD": [
        "Dernier avis d'imposition",
        "Tous les contrats CDD",
        "3 derniers bulletins de salaire par employeur",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "CDIC": [
        "Dernier avis d'imposition",
        "Contrat CDIC (CDI de chantier) avec date de fin",
        "3 derniers bulletins de salaire",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Intérim": [
        "3 derniers avis d'imposition",
        "3 derniers bulletins de salaire",
        "Dernier contrat de mission",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Intermittent": [
        "3 derniers avis d'imposition",
        "Justificatifs d'activité sur 3 ans",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Saisonnier": [
        "3 derniers avis d'imposition",
        "3 derniers bulletins de salaire",
        "Dernier contrat de travail",
        "Preuve de 2 saisons sur 3 ans",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Militaire": [
        "3 derniers avis d'imposition",
        "3 derniers bulletins de salaire",
        "Dernier contrat d'engagement",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Stagiaire FP": [
        "Dernier avis d'imposition",
        "Contrat de stage (fonction publique)",
        "3 derniers bulletins de salaire",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Assistante maternelle": [
        "Dernier avis d'imposition",
        "Contrats de garde (CDI ou CDD) par employeur",
        "Agréments en cours de validité",
        "Contrats futurs (si déjà signés) — optionnel",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Apprenti": [
        "Dernier avis d'imposition de l'apprenti (ou parents si rattaché)",
        "Contrat d'apprentissage",
        "3 derniers bulletins de salaire",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Pompier volontaire": [
        "2 derniers avis d'imposition",
        "3 derniers bulletins de salaire",
        "Justificatifs d'activité (≥ 24 mois passés)",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Élu": [
        "Dernier avis d'imposition",
        "Justificatif de mandat d'élu",
        "3 derniers bulletins de salaire",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Multi-contrats": [
        "Dernier avis d'imposition",
        "3 derniers bulletins de salaire pour chaque employeur",
        "Contrats de travail (CDI/CDD) par employeur",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
    "Famille d'accueil": [
        "Dernier avis d'imposition",
        "Contrat de garde",
        "Agrément (5 ans, renouvelable)",
        "Pièce d'identité",
        "Relevés bancaires (3 mois)",
    ],
}

# -----------------------------
# Aides: petits utilitaires
# -----------------------------
def eur(x: float) -> str:
    return f"{x:,.2f} €".replace(",", " ")

# -----------------------------
# Page: Dossier client
# -----------------------------
def render_dossier_client():
    st.subheader("Dossier client — Tous statuts")

    # --------- Identité & statut ---------
    c0, c1 = st.columns(2)
    with c0:
        nom = st.text_input("Nom et prénom")
    with c1:
        statut = st.selectbox("Statut professionnel", [
            "CDI", "CDD", "CDIC", "Intérim", "Intermittent", "Saisonnier",
            "Militaire", "Stagiaire FP", "Assistante maternelle", "Apprenti",
            "Pompier volontaire", "Élu", "Multi-contrats", "Famille d'accueil"
        ], index=0)

    # --------- Revenus communs ----------
    c2, c3 = st.columns(2)
    with c2:
        salaire_fixe = st.number_input("Salaire fixe mensuel (€)", min_value=0.0, value=2500.0, step=50.0)
    with c3:
        autres_revenus = st.number_input("Autres revenus stables (€)", min_value=0.0, value=0.0, step=50.0)

    def eur(x: float) -> str:
        return f"{x:,.2f} €".replace(",", " ")

    st.divider()

    # ===== CDD / CDIC =====
    if statut in ["CDD", "CDIC"]:
        st.markdown("### Paramètres spécifiques CDD / CDIC")
        with st.expander("Revenus & contrôles", expanded=True):
            c1x, c2x = st.columns(2)
            with c1x:
                cdd_rni_12m = st.number_input("RNI (hors Pôle Emploi) — 12 mois (annuel €)", min_value=0.0, value=0.0, step=500.0)
            with c2x:
                cdd_mois_restants = st.number_input("Mois restants sur contrat", min_value=0, max_value=36, value=3, step=1)
            deductions = st.number_input("Déductions annuelles (primes exceptionnelles, HS ponctuelles) (€)", min_value=0.0, value=0.0, step=100.0)

        if cdd_rni_12m <= 0:
            st.error("⚠️ Renseigne le RNI 12 mois hors Pôle Emploi.")
            st.metric("Revenu mensuel (minimal)", eur(salaire_fixe + autres_revenus))
            return

        revenu_cdd = round((cdd_rni_12m - deductions) / 12.0, 2)
        msg = f"{statut} : RNI 12m hors Pôle Emploi / 12."
        if deductions > 0:
            msg += f" Primes/HS déduites ({deductions:.0f} €/an)."
        if cdd_mois_restants < 3:
            msg += " ⚠️ Moins de 3 mois restants sur le contrat."
        st.metric("Revenu éligible (mensuel)", eur(revenu_cdd))
        st.caption(msg)

        revenu_total = round(revenu_cdd + autres_revenus, 2)
        st.metric("Revenu total retenu (avec autres revenus)", eur(revenu_total))
        st.info("Docs : dernier avis IR + tous les contrats CDD/CDIC + 3 derniers bulletins de salaire / employeur.")
        return

    # ===== Intérim / Intermittent / Saisonnier =====
    if statut in ["Intérim", "Intermittent", "Saisonnier"]:
        st.markdown(f"### Paramètres spécifiques — {statut}")
        with st.expander("Revenus nets imposables (inclure Pôle Emploi)", expanded=True):
            cN, cN1, cN2 = st.columns(3)
            with cN:
                rni_N  = st.number_input("Année N (annuel €)",  min_value=0.0, value=0.0, step=500.0, key=f"{statut}_rniN")
            with cN1:
                rni_N1 = st.number_input("Année N-1 (annuel €)",min_value=0.0, value=0.0, step=500.0, key=f"{statut}_rniN1")
            with cN2:
                rni_N2 = st.number_input("Année N-2 (annuel €)",min_value=0.0, value=0.0, step=500.0, key=f"{statut}_rniN2")

        eligible = True
        contraintes = []

        if statut == "Intérim":
            mois_activite = st.number_input("Mois d’activité (24 derniers mois)", min_value=0, max_value=24, value=18, step=1)
            if mois_activite < 18:
                eligible = False
                contraintes.append("❌ Intérim : ≥ 18 mois d’activité sur 24.")
        if statut == "Intermittent":
            annees = st.number_input("Années d’activité justifiées", min_value=0, value=3, step=1)
            if annees < 3:
                eligible = False
                contraintes.append("❌ Intermittent : au moins 3 ans.")
        if statut == "Saisonnier":
            saisons = st.number_input("Saisons réalisées (3 dernières années)", min_value=0, value=2, step=1)
            if saisons < 2:
                eligible = False
                contraintes.append("❌ Saisonnier : ≥ 2 saisons sur 3 ans.")

        valeurs = [v for v in [rni_N, rni_N1, rni_N2] if v > 0]
        if not valeurs:
            st.error("⚠️ Renseigne au moins un revenu annuel.")
            st.metric("Revenu mensuel (minimal)", eur(salaire_fixe + autres_revenus))
            return

        revenu_mensuel = round(sum(valeurs) / len(valeurs) / 12.0, 2)

        if not eligible:
            st.warning(" / ".join(contraintes))
            st.metric("Revenu éligible (mensuel)", eur(0.0))
            st.caption(f"{statut} : conditions d’antériorité non remplies → revenu non retenu.")
            st.info({
                "Intérim": "Docs : 3 avis IR + 3 bulletins + dernier contrat de mission.",
                "Intermittent": "Docs : 3 avis IR + preuve d’activité sur 3 ans (vérifier régularité).",
                "Saisonnier": "Docs : 3 avis IR + 3 bulletins + dernier contrat + preuve d’au moins 2 saisons/3 ans.",
            }[statut])
            return

        st.metric("Revenu éligible (mensuel)", eur(revenu_mensuel))
        revenu_total = round(revenu_mensuel + autres_revenus, 2)
        st.metric("Revenu total retenu (avec autres revenus)", eur(revenu_total))
        st.info({
            "Intérim": "Docs : 3 avis IR + 3 bulletins + dernier contrat de mission. Condition : 18 mois/24.",
            "Intermittent": "Docs : 3 avis IR + activité ≥ 3 ans. Vérifier régularité.",
            "Saisonnier": "Docs : 3 avis IR + 3 bulletins + dernier contrat. Condition : ≥ 2 saisons / 3 ans.",
        }[statut])
        return

    # ===== Militaire =====
    if statut == "Militaire":
        st.markdown("### Paramètres spécifiques — Militaire")
        rni_N  = st.number_input("RNI Année N (€)",   min_value=0.0, value=0.0, step=500.0)
        rni_N1 = st.number_input("RNI Année N-1 (€)", min_value=0.0, value=0.0, step=500.0)
        rni_N2 = st.number_input("RNI Année N-2 (€)", min_value=0.0, value=0.0, step=500.0)
        revenu = round(((rni_N + rni_N1 + rni_N2) / 3.0) / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : 3 avis IR + 3 bulletins de solde + dernier contrat d’engagement.")
        return

    # ===== Stagiaire FP =====
    if statut == "Stagiaire FP":
        st.markdown("### Paramètres spécifiques — Stagiaire Fonction publique")
        rni = st.number_input("RNI annuel (€)", min_value=0.0, value=0.0, step=500.0)
        revenu = round(rni / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : dernier avis IR + contrat de stage + 3 bulletins de salaire.")
        return

    # ===== Assistante maternelle =====
    if statut == "Assistante maternelle":
        st.markdown("### Paramètres spécifiques — Assistante maternelle")
        cumul_paje = st.number_input("Cumul annuel des revenus PAJE (€)", min_value=0.0, value=0.0, step=500.0)
        revenu = round(cumul_paje / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : avis IR + contrats de garde + agréments (vérifier pérennité).")
        return

    # ===== Apprenti =====
    if statut == "Apprenti":
        st.markdown("### Paramètres spécifiques — Apprenti")
        rni = st.number_input("RNI annuel (€)", min_value=0.0, value=0.0, step=500.0)
        duree = st.number_input("Durée restante du contrat (mois)", min_value=0, value=24, step=1)
        if duree <= 0:
            st.warning("⚠️ Contrat expiré → non éligible.")
            revenu = 0.0
        else:
            revenu = round(rni / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : avis IR de l’apprenti (ou parents si rattaché) + contrat d’apprentissage.")
        return

    # ===== Pompier volontaire =====
    if statut == "Pompier volontaire":
        st.markdown("### Paramètres spécifiques — Pompier volontaire")
        rni_N  = st.number_input("RNI Année N (€)",   min_value=0.0, value=0.0, step=500.0)
        rni_N1 = st.number_input("RNI Année N-1 (€)", min_value=0.0, value=0.0, step=500.0)
        revenu = round(((rni_N + rni_N1) / 2.0) / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : 2 avis IR + 3 bulletins. Pérennité ≥ 24 mois.")
        return

    # ===== Élu =====
    if statut == "Élu":
        st.markdown("### Paramètres spécifiques — Élu")
        revenus_mandat = st.number_input("Revenus de mandat (annuel €)", min_value=0.0, value=0.0, step=500.0)
        autres = st.number_input("Autres revenus (annuel €)", min_value=0.0, value=0.0, step=500.0)
        revenu = round((revenus_mandat + autres) / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : avis IR + justificatif de mandat + 3 bulletins. Vérifier adéquation durée prêt/mandat.")
        return

    # ===== Multi-contrats =====
    if statut == "Multi-contrats":
        st.markdown("### Paramètres spécifiques — Multi-contrats")
        nb = st.number_input("Nombre d’employeurs", min_value=1, value=2, step=1)
        total = 0.0
        for i in range(nb):
            total += st.number_input(f"RNI annuel employeur {i+1} (€)", min_value=0.0, value=0.0, step=500.0, key=f"mc_{i}")
        revenu = round(total / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : avis IR + 3 bulletins + contrats par employeur. Si mix CDI/CDD → vérifier 18 mois sur 24 pour les CDD.")
        return

    # ===== Famille d’accueil =====
    if statut == "Famille d'accueil":
        st.markdown("### Paramètres spécifiques — Famille d’accueil")
        revenus_annuels = st.number_input("Revenus annuels (hors compléments pensionnaires) (€)", min_value=0.0, value=0.0, step=500.0)
        revenu = round(revenus_annuels / 12.0, 2)
        st.metric("Revenu éligible (mensuel)", eur(revenu))
        st.info("Docs : avis IR + contrat de garde + agrément (5 ans, renouvelable). Vérifier pérennité.")
        return

    # ===== CDI (à la fin) =====
    st.markdown("### Paramètres spécifiques — CDI")
    b1, b2, b3 = st.columns(3)
    with b1:
        cdi_anciennete_mois = st.number_input("Ancienneté CDI (mois)", min_value=0, value=12, step=1)
        cdi_periode_essai_terminee = st.checkbox("Période d'essai terminée ?", value=True)
    with b2:
        cdi_statut_cadre = st.checkbox("Statut cadre ?", value=False)
        cdi_salaire_brut_annuel_contrat = st.number_input("Salaire brut annuel du contrat (€)", min_value=0.0, value=30000.0, step=500.0)
    with b3:
        cdi_primes_contractuelles_annuelles = st.number_input("Primes contractuelles annuelles (€)", min_value=0.0, value=0.0, step=100.0)

    st.caption("Primes non contractuelles (annuelles) — moyenne sur 3 années (×2/3 si ancienneté < 36 mois).")
    p1, p2, p3 = st.columns(3)
    with p1:
        pnc1 = st.number_input("PNC Année N-1 (€)", min_value=0.0, value=0.0, step=100.0)
    with p2:
        pnc2 = st.number_input("PNC Année N-2 (€)", min_value=0.0, value=0.0, step=100.0)
    with p3:
        pnc3 = st.number_input("PNC Année N-3 (€)", min_value=0.0, value=0.0, step=100.0)

    st.markdown("#### Données fiscales (annuelles, avant abattement)")
    f1, f2 = st.columns(2)
    with f1:
        cdi_cni = st.number_input("Cumul net imposable (Déc N-1) — annuel (€)", min_value=0.0, value=0.0, step=500.0)
    with f2:
        cdi_rni = st.number_input("Revenu net imposable (dernier avis IRPP) — annuel (€)", min_value=0.0, value=0.0, step=500.0)
    st.caption("Si ancienneté ≥ 12 mois : retenir le **moins favorable** entre CNI N-1 et RNI IRPP, puis /12.")

    st.markdown("#### Changement de situation")
    cdi_chgt = st.checkbox("Changement de situation ? (moyenne des 3 derniers bulletins)", value=False)
    if cdi_chgt:
        s1, s2, s3 = st.columns(3)
        with s1:
            b_m1 = st.number_input("Bulletin M-1 — net à payer (€)", min_value=0.0, value=0.0, step=50.0)
        with s2:
            b_m2 = st.number_input("Bulletin M-2 — net à payer (€)", min_value=0.0, value=0.0, step=50.0)
        with s3:
            b_m3 = st.number_input("Bulletin M-3 — net à payer (€)", min_value=0.0, value=0.0, step=50.0)
        salaires_3_mois = [b_m1, b_m2, b_m3]
    else:
        salaires_3_mois = None

    st.divider()

    def pnc_mensuelles(p1, p2, p3, anciennete_mois):
        vals = [v for v in [p1, p2, p3] if v is not None]
        if not vals:
            return 0.0
        moy_ann = sum(vals) / len(vals)
        mens = moy_ann / 12.0
        coef = (2.0 / 3.0) if anciennete_mois < 36 else 1.0
        return mens * coef

    if cdi_chgt and salaires_3_mois and any(salaires_3_mois):
        moy3 = sum(salaires_3_mois) / len([x for x in salaires_3_mois if x is not None and x > 0])
        revenu_cdi = max(0.0, round(moy3, 2))
        message = "CDI (changement) : moyenne des 3 derniers bulletins retenue."
    else:
        pc_m = (cdi_primes_contractuelles_annuelles / 12.0) if cdi_primes_contractuelles_annuelles else 0.0
        pnc_m = pnc_mensuelles(pnc1, pnc2, pnc3, cdi_anciennete_mois)

        if cdi_anciennete_mois < 12:
            if not cdi_periode_essai_terminee:
                st.error("CDI < 12 mois : période d'essai non terminée → non éligible.")
                revenu_cdi = 0.0
                message = "CDI < 12 mois : période d'essai non terminée."
            else:
                coef = 0.75 if cdi_statut_cadre else 0.78
                base_m = (cdi_salaire_brut_annuel_contrat * coef) / 12.0
                revenu_cdi = max(0.0, round(base_m + pc_m + pnc_m, 2))
                message = f"CDI < 12 mois : (brut annuel×{coef})/12 + primes (contractuelles 100%/12 ; PNC moy.3a/12 ×{'2/3' if cdi_anciennete_mois < 36 else '1'})."
        else:
            candidats = [x for x in [cdi_cni, cdi_rni] if x and x > 0]
            if candidats:
                base_m = min(candidats) / 12.0
                revenu_cdi = max(0.0, round(base_m, 2))  # les primes sont déjà incluses dans ces bases fiscales
                message = "CDI ≥ 12 mois : base fiscale = min(CNI N-1 ; RNI IRPP) / 12."
            else:
                revenu_cdi = max(0.0, round(salaire_fixe + pc_m + pnc_m, 2))
                message = "CDI ≥ 12 mois (fallback) : fixe + primes (contractuelles 100%/12 ; PNC moy.3a/12 × (2/3 si <36m))."

    st.metric("Revenu éligible CDI (mensuel)", eur(revenu_cdi))
    st.caption(message)
    revenu_total = round(revenu_cdi + autres_revenus, 2)
    st.metric("Revenu total retenu (avec autres revenus)", eur(revenu_total))
    st.info("Rappel primes CDI : contractuelles = 100% ; non contractuelles = moyenne 3 ans /12, ×2/3 si ancienneté < 36 mois. "
            "Si ancienneté ≥ 12 mois et CNI/RNI fournis : retenir le moins favorable /12 (sans ajouter de primes).")
    return

# -----------------------------
# Page: Check-lists
# -----------------------------
def render_checklists():
    st.subheader("Check-lists par statut")
    statut = st.selectbox("Choisir un statut", STATUTS, index=0, key="cl_statut")
    docs = DOCS_PAR_STATUT.get(statut, [])
    if not docs:
        st.warning("Aucune check-list prédéfinie pour ce statut.")
        return
    st.write("Documents à demander :")
    for i, d in enumerate(docs, start=1):
        st.checkbox(f"{i}. {d}", key=f"doc_{statut}_{i}")
    st.caption("Astuce : capture d’écran ou copier/coller pour l’envoyer au client.")

# -----------------------------
# Page: Autres revenus (aide)
# -----------------------------
def render_autres_revenus_aide():
    st.subheader("Autres revenus (aide / pense-bête)")
    st.info("Cette page est un mémo. Elle n’affecte pas les calculs automatiquement.")
    tabs = st.tabs([
        "Retraites",
        "Allocations familiales & aides sociales",
        "Aide au logement & IJ",
        "Revenus fonciers / loc. saisonnière",
        "Autres revenus sous conditions",
        "Exclusions",
    ])

    with tabs[0]:
        st.markdown(
            "**Principe :** régime général + complémentaire. Si proche retraite, demander estimation prévisionnelle (caisse / simulateur).  \n"
            "**Justificatifs :** dernier avis IRPP ou relevé annuel de pension."
        )
    with tabs[1]:
        st.markdown(
            "**Allocations familiales / AAH / APA / Prime d’activité :** retenir si pérennes sur la durée du prêt.  \n"
            "**Justificatifs :** décompte CAF, documents organismes sociaux."
        )
    with tabs[2]:
        st.markdown(
            "**Aide au logement :** retenir uniquement si versée sur le compte du client.  \n"
            "**Indemnités journalières :** prudence (temporaire)."
        )
    with tabs[3]:
        st.markdown(
            "**Revenus fonciers :** saisir 100% (pondération gérée côté banque). Revenus attendus OK si baux/estimations (≈3.5% neuf, 4% ancien, 4.5% meublé) "
            "et DPE A–E ou travaux de performance budgétisés.  \n"
            "**Justificatifs :** 2072/2042/2031/2044, baux récents, 3 relevés bancaires.  \n"
            "**Location saisonnière :** moyenne pluriannuelle ou attestation gestionnaire si historique insuffisant."
        )
    with tabs[4]:
        st.markdown(
            "**Pensions alimentaires :** seulement si jugement + versement effectif (relevés).  \n"
            "**Invalidité cat.2 / rente AT :** si durée compatible.  \n"
            "**Obligations / coupons :** récurrents et réguliers.  \n"
            "**Dividendes :** stables sur 3 ans et déclarés, vérifier capacité de distribution (bilan).  \n"
            "**Photovoltaïque :** moyenne 2 ans (justif EDF / BIC)."
        )
    with tabs[5]:
        st.markdown(
            "**Exclus :** remboursements de frais professionnels (IK, repas), indemnités de déplacement chauffeurs.  \n"
            "Toujours saisir des revenus pérennes, réguliers et traçables."
        )

# -----------------------------
# Pages: Exports & Aide
# -----------------------------
def render_exports():
    import io
    from datetime import datetime
    st.subheader("Exports PDF")

    # Tentative d'import de fpdf2
    try:
        from fpdf import FPDF
    except Exception:
        st.error("La librairie 'fpdf2' n'est pas installée.")
        st.code("pip install fpdf2", language="bash")
        st.caption("Après installation, relance l'app : streamlit run app.py")
        return

    # --- Helpers PDF ---
    def eur(x: float) -> str:
        try:
            return f"{float(x):,.2f} €".replace(",", " ")
        except Exception:
            return f"{x} €"

    def safe(txt: str) -> str:
        """
        Nettoie tout texte pour la police core Helvetica (Latin-1) :
        - remplace les tirets longs par '-'
        - supprime les caractères hors Latin-1 pour éviter FPDFUnicodeEncodingException
        """
        if txt is None:
            txt = ""
        txt = txt.replace("—", "-").replace("–", "-")
        # supprime/ignore tout hors latin-1
        return txt.encode("latin-1", "ignore").decode("latin-1")

    mode = st.radio("Type d'export", ["Résumé 1 page", "Check-list par statut"], horizontal=True)

    if mode == "Résumé 1 page":
        st.markdown("### Contenu du résumé")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom et prénom", "")
            statut = st.selectbox("Statut professionnel", STATUTS, index=0)
        with col2:
            revenu_elig = st.number_input("Revenu éligible (mensuel, €)", min_value=0.0, value=0.0, step=50.0)
            revenu_total = st.number_input("Revenu total retenu (mensuel, €)", min_value=0.0, value=0.0, step=50.0)

        notes = st.text_area("Notes (facultatif)", placeholder="Observations, hypotheses, points de vigilance...")

        if st.button("Générer le PDF (Résumé)"):
            class PDF(FPDF):
                def header(self):
                    self.set_font("Helvetica", "B", 14)
                    self.cell(0, 10, safe("Coach Pret Immo - Resume dossier"), ln=1, align="C")
                    self.set_font("Helvetica", "", 9)
                    self.cell(0, 6, safe(datetime.now().strftime("Genere le %d/%m/%Y a %H:%M")), ln=1, align="C")
                    self.ln(2)
                    self.set_draw_color(200, 200, 200)
                    y = self.get_y()
                    self.line(10, y, 200, y)
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Helvetica", "I", 8)
                    self.cell(0, 10, safe(f"Page {self.page_no()}"), align="C")

            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Helvetica", "", 11)

            # Identité
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, safe("Identite & Statut"), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(60, 8, safe("Nom et prenom :"), border=0)
            pdf.cell(0, 8, safe(nom or "-"), ln=1)
            pdf.cell(60, 8, safe("Statut professionnel :"), border=0)
            pdf.cell(0, 8, safe(statut), ln=1)
            pdf.ln(4)

            # Chiffres
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, safe("Synthese revenus mensuels"), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(60, 8, safe("Revenu eligibile :"), border=0)
            pdf.cell(0, 8, safe(eur(revenu_elig)), ln=1)
            pdf.cell(60, 8, safe("Revenu total retenu :"), border=0)
            pdf.cell(0, 8, safe(eur(revenu_total)), ln=1)
            pdf.ln(4)

            # Notes
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, safe("Notes"), ln=1)
            pdf.set_font("Helvetica", "", 11)
            if notes.strip():
                pdf.multi_cell(0, 6, safe(notes))
            else:
                pdf.set_text_color(120, 120, 120)
                pdf.cell(0, 6, safe("(aucune)"), ln=1)
                pdf.set_text_color(0, 0, 0)

            # Export
            pdf_bytes = bytes(pdf.output(dest="S"))
            st.download_button(
                label="Télécharger le PDF (Résumé)",
                data=pdf_bytes,
                file_name=f"resume_dossier_{(nom or 'client').replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
            st.success("PDF (Résumé) généré.")

    else:
        st.markdown("### Check-list par statut")
        statut = st.selectbox("Choisir un statut", STATUTS, index=0, key="export_statut")
        docs = DOCS_PAR_STATUT.get(statut, [])

        if not docs:
            st.warning("Aucune check-list définie pour ce statut.")
            return

        st.write("Tu peux cocher (pour mémoire) ce qui est déjà récupéré :")
        cols = st.columns(2)
        checked = []
        for i, doc in enumerate(docs):
            col = cols[i % 2]
            with col:
                val = st.checkbox(doc, key=f"export_doc_{i}")
                checked.append((doc, val))

        remarque = st.text_area("Notes / remarques (facultatif)", "")

        if st.button("Générer le PDF (Check-list)"):
            class PDF(FPDF):
                def header(self):
                    self.set_font("Helvetica", "B", 14)
                    self.cell(0, 10, safe("Coach Pret Immo - Checklist documents"), ln=1, align="C")
                    self.set_font("Helvetica", "", 9)
                    self.cell(0, 6, safe(datetime.now().strftime("Genere le %d/%m/%Y a %H:%M")), ln=1, align="C")
                    self.ln(2)
                    self.set_draw_color(200, 200, 200)
                    y = self.get_y()
                    self.line(10, y, 200, y)
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Helvetica", "I", 8)
                    self.cell(0, 10, safe(f"Page {self.page_no()}"), align="C")

            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Helvetica", "", 11)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, safe(f"Statut : {statut}"), ln=1)
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 11)

            for doc, ok in checked:
                prefix = "[x] " if ok else "[ ] "
                pdf.multi_cell(0, 6, safe(prefix + doc))

            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, safe("Notes"), ln=1)
            pdf.set_font("Helvetica", "", 11)
            if remarque.strip():
                pdf.multi_cell(0, 6, safe(remarque))
            else:
                pdf.set_text_color(120, 120, 120)
                pdf.cell(0, 6, safe("(aucune)"), ln=1)
                pdf.set_text_color(0, 0, 0)

            pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
            st.download_button(
                label="Télécharger le PDF (Check-list)",
                data=pdf_bytes,
                file_name=f"checklist_{statut.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
            st.success("PDF (Check-list) généré.")

def render_aide():
    st.subheader("Aide")
    st.write("Raccourcis nano : CTRL+O (sauver), CTRL+X (quitter), CTRL+W (chercher), CTRL+K (couper ligne), CTRL+U (coller).")
    st.write("Si écran blanc : vérifier qu’il n’y a **qu’un seul** routeur et qu’aucun bloc multi-ligne n’est resté ouvert.")

# -----------------------------
# Navigation + router robuste
# -----------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Dossier client", "Check-lists", "Autres revenus (aide)", "Exports", "Aide"],
)

def _safe_render(fn):
    import traceback
    try:
        fn()
    except Exception as e:
        st.error("Une erreur est survenue dans cette page.")
        st.exception(e)
        st.code(traceback.format_exc())

if page == "Dossier client":
    _safe_render(render_dossier_client)
elif page == "Check-lists":
    _safe_render(render_checklists)
elif page == "Autres revenus (aide)":
    _safe_render(render_autres_revenus_aide)
elif page == "Exports":
    _safe_render(render_exports)
elif page == "Aide":
    _safe_render(render_aide)

