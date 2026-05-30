"""
AI Agent for Questionnaire Generation
Generates questions grounded in verified digital maturity frameworks.
Each question is tagged with its source framework and maps to a specific maturity criterion.
"""
import json
import logging
import os
from knowledge.frameworks import get_frameworks_for_sector, format_frameworks_for_prompt
from knowledge.regulations import format_regulations_for_prompt
from knowledge.sector_benchmarks import format_benchmark_for_prompt
from services.llm_client import call_llm as call_groq, extract_json, TaskType

logger = logging.getLogger(__name__)


class QuestionnaireAgent:
    def __init__(self):
        # Use a fast model for questionnaire generation — quality is sufficient
        # and speed matters more here (user waits on the setup page)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def generate(self, sector: str, country: str,
                       company_size: str | None, language: str,
                       num_questions: int) -> dict:

        # Step 1: Select relevant frameworks for this company profile
        frameworks = get_frameworks_for_sector(sector, max_frameworks=3)
        framework_context = format_frameworks_for_prompt(frameworks)
        framework_names = [fw["name"] for fw in frameworks]

        # Step 2: Build regulatory and benchmark context
        regulations_context = format_regulations_for_prompt(sector, country)
        benchmark_context = format_benchmark_for_prompt(sector, country)

        # Step 3: Build axis distribution
        distribution = self._get_axis_distribution(num_questions)

        # Step 4: Build grounded prompt with all knowledge bases
        system_prompt = self._build_system_prompt(framework_context, regulations_context, benchmark_context)
        user_prompt = self._build_user_prompt(
            sector, country, company_size, language,
            distribution, framework_names
        )

        # Step 5: Call Mistral asynchronously (non-blocking, 120s timeout)
        raw = await call_groq(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            model=self.model,
            task=TaskType.QUESTIONNAIRE,
        )
        data = extract_json(raw)

        # Step 6: Detect and fix any remaining generic options in one batched call
        data = await self._fix_generic_options(data)

        result = self._normalize(data, sector, country, framework_names)
        result = self._ensure_all_axes(result, sector)

        # Step 7: Second fix pass — _normalize may have assigned _LAST_RESORT_OPTIONS
        # to questions whose raw options failed format validation (not a list of 5).
        result = await self._fix_generic_options(result)
        return result

    def _build_system_prompt(self, framework_context: str,
                             regulations_context: str = "",
                             benchmark_context: str = "") -> str:
        return f"""Tu es un agent expert en benchmarking de maturité digitale.
Tu génères des questionnaires d'évaluation professionnels fondés sur des frameworks reconnus internationalement, \
en tenant compte des réglementations applicables et des benchmarks sectoriels.

KNOWLEDGE BASE — FRAMEWORKS DE RÉFÉRENCE :
{framework_context}
{regulations_context}
{benchmark_context}

RÈGLES STRICTES :
1. Chaque question DOIT être dérivée d'un critère spécifique des frameworks ci-dessus.
2. Inclure des questions couvrant les obligations réglementaires identifiées (RGPD, DORA, NIS2, HDS, etc.).
3. Chaque question doit indiquer son framework source (source_framework).
4. Chaque question doit avoir EXACTEMENT 5 options de réponse CONTEXTUALISÉES et SPÉCIFIQUES au sujet évalué.
   Les options décrivent des pratiques concrètes, des outils, des états organisationnels précis — PAS des labels génériques.

   ✅ BON EXEMPLE pour "Dans quelle mesure utilisez-vous l'analyse de données pour piloter vos décisions marketing ?" :
   - "Aucun outil analytique, décisions basées sur l'intuition ou l'expérience"
   - "Google Analytics de base, lecture ponctuelle sans processus d'analyse"
   - "Tableaux de bord actifs, KPIs définis mais rarement actionnés"
   - "A/B testing régulier, segmentation clients, reporting hebdomadaire automatisé"
   - "Modèles prédictifs en production, personnalisation temps réel, data science marketing"

   ❌ MAUVAIS EXEMPLE (interdit — ces formulations génériques ne sont PAS acceptées) :
   - "Inexistant"
   - "Quelques initiatives isolées, non formalisées"
   - "Approche en cours de structuration"
   - "Pratiques définies et déployées en grande partie"
   - "Maîtrise complète, mesurée et en amélioration continue"

5. Chaque option doit :
   - Nommer des outils, méthodes, pratiques ou états organisationnels concrets
   - Décrire la fréquence, l'automatisation, le niveau d'équipe impliquée si pertinent
   - Être compréhensible sans relire la question
   - Former une progression logique et continue du niveau 1 (rien) au niveau 5 (excellence)
6. Les questions doivent être mesurables, objectives et non ambiguës.
7. Adapter la formulation au secteur, au pays et aux enjeux réglementaires identifiés.
8. Réponds UNIQUEMENT en JSON valide selon le format demandé.
"""

    def _build_user_prompt(self, sector: str, country: str,
                           company_size: str | None, language: str,
                           distribution: dict, framework_names: list) -> str:
        size_info = f"\n- Taille de l'entreprise : {company_size}" if company_size else ""
        frameworks_used = ", ".join(framework_names)

        dist_lines = "\n".join([
            f"- Axe BUSINESS (Stratégie digitale, Culture, Innovation, Expérience client) : {distribution['BUSINESS']} questions",
            f"- Axe PROCESS (Processus métier, Gestion de projet, Gouvernance, Agilité) : {distribution['PROCESS']} questions",
            f"- Axe INFORMATION_SYSTEM (SI, Données, Cybersécurité, Architecture technique) : {distribution['INFORMATION_SYSTEM']} questions",
            f"- Axe CANAUX_DISTRIBUTION (Canaux digitaux, Mobile, Web, Distribution omnicanal) : {distribution['CANAUX_DISTRIBUTION']} questions",
            f"- Axe MARKETING_COMMUNICATION (Marketing digital, CRM, Communication, Acquisition client) : {distribution['MARKETING_COMMUNICATION']} questions",
            f"- Axe RH_CULTURE_DIGITALE (Compétences numériques, Formation, Culture digitale, RH) : {distribution['RH_CULTURE_DIGITALE']} questions",
            f"- Axe OFFRES_DIGITALES (Offres numériques, Produits digitaux, Open Banking, Services en ligne) : {distribution['OFFRES_DIGITALES']} questions",
            f"- Axe MODELE_OPERATIONNEL_INNOVATION (Automatisation des processus, Gouvernance transformation digitale, Innovation) : {distribution['MODELE_OPERATIONNEL_INNOVATION']} questions",
            f"- Axe IT_DATA (Socle IT, Cloud, Cybersécurité avancée, Gouvernance de la donnée, Analytics) : {distribution['IT_DATA']} questions",
        ])

        return f"""Génère un questionnaire d'évaluation de maturité digitale pour :
- Secteur : {sector}
- Pays : {country}{size_info}
- Langue de rédaction : {language}
- Frameworks à utiliser : {frameworks_used}

DISTRIBUTION DES QUESTIONS (OBLIGATOIRE — tu DOIS générer exactement ces 9 axes) :
{dist_lines}

Pour chaque question :
- text : formulation claire en {language}, réponse sur échelle 1-5
- axis : BUSINESS | PROCESS | INFORMATION_SYSTEM | CANAUX_DISTRIBUTION | MARKETING_COMMUNICATION | RH_CULTURE_DIGITALE | OFFRES_DIGITALES | MODELE_OPERATIONNEL_INNOVATION | IT_DATA
- sub_axis : sous-domaine précis (ex: "Stratégie digitale", "Cybersécurité", "Canaux mobiles", "Marketing automation")
- weight : importance stratégique de 1 à 5 (5 = critique)
- display_order : numéro séquentiel
- source_framework : nom court du framework source (ex: "Gartner DMM", "McKinsey DQ", "ISO 27001", "CMMI", "COBIT 2019", "MIT CISR", "WEF DTI")
- options : tableau de 5 phrases courtes décrivant chaque niveau de maturité spécifique à CETTE question

FORMAT JSON REQUIS :
{{
  "title": "Évaluation de maturité digitale — {sector} — {country}",
  "description": "Questionnaire fondé sur {frameworks_used}. Évalue la maturité digitale selon les standards internationaux.",
  "frameworks_used": ["{frameworks_used}"],
  "questions": [
    {{
      "text": "...",
      "axis": "BUSINESS",
      "sub_axis": "...",
      "weight": 4,
      "display_order": 1,
      "source_framework": "...",
      "options": [
        "Aucune stratégie digitale formalisée, décisions au cas par cas",
        "Vision digitale esquissée mais non documentée ni partagée",
        "Feuille de route digitale existante, revue annuelle, alignement partiel",
        "Stratégie digitale formalisée, revue trimestrielle, KPIs suivis par la direction",
        "Stratégie digitale intégrée au plan d'entreprise, pilotage OKR, révision continue"
      ]
    }}
  ]
}}
"""

    def _is_generic_options(self, options: list) -> bool:
        """Returns True if options look like the generic fallback — not contextual."""
        if not isinstance(options, list) or len(options) != 5:
            return True
        generic_keywords = [
            "inexistant", "aucune pratique", "quelques initiatives", "non formalisées",
            "en cours de structuration", "approche en cours", "pratiques définies",
            "amélioration continue", "maîtrise complète",
            "aucun dispositif ou outil en place",
            "premiers essais isolés, sans processus établi",
            "pratiques partiellement formalisées",
            "pratiques établies, mesurées",
            "excellence opérationnelle, pilotage continu par la donnée",
        ]
        # Even 1 match on a verbatim LAST_RESORT pattern means it's the fallback
        last_resort_exact = [kw for kw in generic_keywords if len(kw) > 20]
        for opt in options:
            if any(kw in opt.lower() for kw in last_resort_exact):
                return True
        matches = sum(
            1 for opt in options
            if any(kw in opt.lower() for kw in generic_keywords)
        )
        return matches >= 2

    async def _fix_generic_options(self, data: dict) -> dict:
        """Regenerate generic options in batches of 5 with per-question fallback."""
        questions = data.get("questions", [])
        to_fix = [
            (i, q) for i, q in enumerate(questions)
            if self._is_generic_options(q.get("options", []))
        ]
        if not to_fix:
            return data

        logger.info("Regenerating contextual options for %d/%d questions", len(to_fix), len(questions))

        BATCH_SIZE = 5
        for batch_start in range(0, len(to_fix), BATCH_SIZE):
            batch = to_fix[batch_start:batch_start + BATCH_SIZE]
            await self._regenerate_batch(questions, batch)

        return data

    async def _regenerate_batch(self, questions: list, batch: list) -> None:
        """Regenerate options for a batch of up to 5 questions. Falls back per-question on failure."""
        questions_text = "\n".join(
            f"{rank+1}. [{q.get('axis','')}/{q.get('sub_axis','')}] {q.get('text','')}"
            for rank, (_, q) in enumerate(batch)
        )
        prompt = f"""Tu es expert en maturité digitale. Pour chaque question ci-dessous, génère 5 options de réponse \
CONTEXTUALISÉES décrivant les 5 niveaux de maturité du sujet évalué.

RÈGLES STRICTES :
- Chaque option DOIT nommer des outils, méthodes ou états organisationnels concrets et spécifiques à la question
- Option 1 : rien en place, état initial
- Option 2 : tentatives isolées, sans processus standardisé
- Option 3 : début de formalisation, usage partiel
- Option 4 : pratiques établies, mesurées, équipes formées
- Option 5 : excellence, automatisation avancée
- INTERDIT : "Inexistant", "Quelques initiatives", "Approche en cours", "Pratiques définies", "Amélioration continue" seuls

QUESTIONS ({len(batch)}) :
{questions_text}

JSON UNIQUEMENT — {len(batch)} tableaux dans le même ordre :
{{
  "options_by_question": [
    ["option1 spécifique", "option2 spécifique", "option3 spécifique", "option4 spécifique", "option5 spécifique"]
  ]
}}"""

        try:
            raw = await call_groq(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                model=self.model,
                task=TaskType.QUESTIONNAIRE,
            )
            result = extract_json(raw)
            options_list = result.get("options_by_question", [])
            fixed = 0
            for rank, (orig_idx, _) in enumerate(batch):
                if rank < len(options_list) and isinstance(options_list[rank], list) and len(options_list[rank]) == 5:
                    questions[orig_idx]["options"] = options_list[rank]
                    fixed += 1
                else:
                    await self._regenerate_single(questions, orig_idx, batch[rank][1])
            logger.info("Batch fix: %d/%d options regenerated", fixed, len(batch))
        except Exception as exc:
            logger.warning("Batch regeneration failed (%s) — retrying individually", exc)
            for orig_idx, q in batch:
                await self._regenerate_single(questions, orig_idx, q)

    async def _regenerate_single(self, questions: list, orig_idx: int, q: dict) -> None:
        """Last-resort single-question option regeneration."""
        prompt = f"""Génère 5 options de réponse CONTEXTUALISÉES pour cette question d'évaluation de maturité digitale.

Question : {q.get('text', '')}
Axe : {q.get('axis', '')} / {q.get('sub_axis', '')}

Chaque option doit décrire concrètement un niveau de maturité (outils, pratiques, état d'organisation).
Option 1 = rien en place. Option 5 = excellence opérationnelle.
INTERDIT : formulations génériques comme "Inexistant", "Quelques initiatives", "En cours".

JSON UNIQUEMENT : {{"options": ["opt1", "opt2", "opt3", "opt4", "opt5"]}}"""

        try:
            raw = await call_groq(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                model=self.model,
                task=TaskType.QUESTIONNAIRE,
            )
            result = extract_json(raw)
            opts = result.get("options", [])
            if isinstance(opts, list) and len(opts) == 5:
                questions[orig_idx]["options"] = opts
            else:
                logger.warning("Single regen returned wrong format for q[%d], using last resort", orig_idx)
                questions[orig_idx]["options"] = self._LAST_RESORT_OPTIONS
        except Exception as exc:
            logger.warning("Single regen failed for q[%d]: %s", orig_idx, exc)
            questions[orig_idx]["options"] = self._LAST_RESORT_OPTIONS

    # Fallback questions per axis — used when the LLM generates < 3 questions for an axis
    _AXIS_DEFAULTS: dict[str, list[dict]] = {
        "BUSINESS": [
            {"text": "Votre stratégie de transformation digitale est-elle formalisée, partagée et pilotée par des KPIs ?",
             "sub_axis": "Stratégie digitale", "weight": 5, "source_framework": "Gartner DMM",
             "options": ["Aucune stratégie digitale, décisions au cas par cas",
                         "Vision esquissée mais non documentée ni partagée",
                         "Feuille de route existante, revue annuelle, alignement partiel",
                         "Stratégie formalisée, revue trimestrielle, KPIs suivis par la direction",
                         "Stratégie digitale intégrée au plan d'entreprise, pilotage OKR, révision continue"]},
            {"text": "L'expérience client digitale est-elle mesurée et améliorée en continu ?",
             "sub_axis": "Expérience client", "weight": 4, "source_framework": "McKinsey DQ",
             "options": ["Aucune mesure de l'expérience client digitale",
                         "Enquêtes ponctuelles sans processus d'amélioration",
                         "NPS mesuré annuellement, actions correctives ad hoc",
                         "NPS/CSAT trimestriels, roadmap UX priorisée par la data",
                         "Customer journey mapping continu, A/B testing systématique, amélioration hebdo"]},
            {"text": "Votre modèle d'affaires intègre-t-il des sources de revenus digitales ?",
             "sub_axis": "Modèle d'affaires digital", "weight": 4, "source_framework": "MIT CISR",
             "options": ["Aucun revenu digital, 100% modèle traditionnel",
                         "<5% revenus digitaux, expériences isolées",
                         "10-20% revenus digitaux, offres en cours de digitalisation",
                         ">30% revenus digitaux, plateforme ou marketplace en opération",
                         ">50% revenus digitaux, écosystème partenaires, monétisation données"]},
        ],
        "PROCESS": [
            {"text": "Dans quelle mesure vos processus opérationnels sont-ils automatisés et dématérialisés ?",
             "sub_axis": "Automatisation", "weight": 4, "source_framework": "CMMI",
             "options": ["Processus 100% manuels et papier",
                         "Quelques outils bureautiques, pas d'automatisation structurée",
                         "Workflows partiels, signature électronique déployée",
                         "Processus critiques automatisés, RPA opérationnel sur les tâches répétitives",
                         "Automatisation end-to-end, IA intégrée aux processus, 0 ressaisie"]},
            {"text": "Une gouvernance de la transformation digitale (comité, budget dédié, roadmap) est-elle en place ?",
             "sub_axis": "Gouvernance", "weight": 4, "source_framework": "COBIT 2019",
             "options": ["Aucune gouvernance formelle de la transformation digitale",
                         "Initiatives isolées sans pilotage transversal",
                         "Comité ad hoc, budget non dédié, reporting irrégulier",
                         "Comité trimestriel, budget digital identifié, KPIs de transformation suivis",
                         "Gouvernance intégrée au CA, budget >2% CA, OKRs digitaux revus mensuellement"]},
            {"text": "Vos équipes travaillent-elles en mode agile et utilisent-elles des méthodes de gestion de projet modernes ?",
             "sub_axis": "Agilité", "weight": 3, "source_framework": "SAFe",
             "options": ["Méthodes classiques en cascade, aucune agilité",
                         "Quelques équipes tentent Scrum sans cadre formel",
                         "Scrum déployé sur 2-3 équipes, sprints de 2 semaines",
                         "Agilité généralisée, PI Planning trimestriel, DevOps partiel",
                         "SAFe ou LeSS à l'échelle, déploiement continu CI/CD, feedback loops <1 semaine"]},
        ],
        "INFORMATION_SYSTEM": [
            {"text": "Dans quelle mesure votre infrastructure SI s'appuie-t-elle sur le cloud ?",
             "sub_axis": "Cloud", "weight": 5, "source_framework": "Gartner DMM",
             "options": ["Infrastructure 100% on-premise, aucun cloud",
                         "1-2 applications SaaS isolées (email, stockage)",
                         "Cloud hybride partiel, migration en cours pour les applications non critiques",
                         "Cloud-first pour les nouveaux projets, IaaS/PaaS pour les apps critiques",
                         "Multi-cloud géré, FinOps actif, >80% workloads dans le cloud"]},
            {"text": "La cybersécurité est-elle gérée activement avec des politiques et des outils dédiés ?",
             "sub_axis": "Cybersécurité", "weight": 5, "source_framework": "ISO 27001",
             "options": ["Aucune politique de sécurité formalisée",
                         "Antivirus basique, pas de politique BYOD ni de formation",
                         "Politique de mots de passe, sauvegardes régulières, formation annuelle",
                         "MFA déployé, SIEM en place, tests de pénétration annuels, PSSI formalisée",
                         "SOC 24/7, certification ISO 27001, threat intelligence, réponse incidents <1h"]},
            {"text": "Vos systèmes d'information sont-ils intégrés et exposent-ils des APIs à des partenaires ?",
             "sub_axis": "Architecture & APIs", "weight": 4, "source_framework": "TOGAF",
             "options": ["Systèmes en silos, aucune intégration ni API",
                         "Intégrations point-à-point fragiles, fichiers CSV/Excel en échange",
                         "ESB ou middleware en place, quelques APIs internes documentées",
                         "API Management déployé, APIs exposées à des partenaires, documentation OpenAPI",
                         "Architecture microservices, API marketplace, événements temps réel, 100+ partenaires intégrés"]},
        ],
        "CANAUX_DISTRIBUTION": [
            {"text": "Quels canaux digitaux utilisez-vous pour distribuer vos produits/services ?",
             "sub_axis": "Canaux digitaux", "weight": 4, "source_framework": "McKinsey DQ",
             "options": ["Distribution 100% physique, aucun canal digital",
                         "Site web vitrine sans transaction, présence sociale basique",
                         "E-commerce ou portail client fonctionnel, taux conversion <2%",
                         "App mobile + web + partenaires digitaux, taux conversion >3%, analytics actif",
                         "Omnicanal complet, parcours unifié, personnalisation temps réel, 50%+ ventes digitales"]},
            {"text": "Vos canaux digitaux et physiques sont-ils intégrés (omnicanalité) ?",
             "sub_axis": "Omnicanalité", "weight": 4, "source_framework": "Gartner DMM",
             "options": ["Canaux totalement cloisonnés, historique client non partagé",
                         "Partage manuel d'informations entre canaux, incohérences fréquentes",
                         "CRM partagé, historique visible mais parcours non unifiés",
                         "Panier/profil unifié web-mobile-magasin, continuité de service assurée",
                         "Orchestration omnicanale temps réel, IA de recommandation, NPS omnicanal >70"]},
            {"text": "Analysez-vous les données de vos canaux digitaux pour optimiser la conversion et l'expérience ?",
             "sub_axis": "Analytics canaux", "weight": 3, "source_framework": "WEF DTI",
             "options": ["Aucune analyse des canaux digitaux",
                         "Google Analytics installé, lecture mensuelle sans action",
                         "KPIs définis (taux rebond, conversion), rapports hebdomadaires",
                         "A/B testing régulier, heatmaps, entonnoirs de conversion optimisés",
                         "Analytics prédictif, attribution multi-touch, personnalisation individuelle"]},
        ],
        "MARKETING_COMMUNICATION": [
            {"text": "Disposez-vous d'une stratégie de marketing digital formalisée avec des objectifs mesurables ?",
             "sub_axis": "Stratégie marketing digital", "weight": 4, "source_framework": "Gartner DMM",
             "options": ["Aucune stratégie marketing digital",
                         "Présence sur les réseaux sociaux sans plan ni objectifs",
                         "Plan marketing annuel, budget dédié, KPIs définis mais peu suivis",
                         "Stratégie SEO/SEA/social active, reporting mensuel, ROI mesuré",
                         "Marketing automation, lead scoring, attribution multi-canal, optimisation continue"]},
            {"text": "Analysez-vous les données clients pour personnaliser vos communications et offres ?",
             "sub_axis": "Personnalisation & CRM", "weight": 4, "source_framework": "McKinsey DQ",
             "options": ["Aucune personnalisation, communications génériques à tous",
                         "Segmentation basique par produit ou zone géographique",
                         "Segmentation comportementale, emails ciblés, CRM actif",
                         "Personnalisation dynamique basée sur l'historique, recommandations automatiques",
                         "IA de personnalisation temps réel, next-best-action, hyper-personnalisation 1-to-1"]},
            {"text": "Mesurez-vous le retour sur investissement (ROI) de vos actions marketing digitales ?",
             "sub_axis": "ROI marketing", "weight": 3, "source_framework": "WEF DTI",
             "options": ["Aucune mesure du ROI marketing digital",
                         "Suivi des dépenses sans lien avec les résultats",
                         "ROI calculé ponctuellement par campagne, outils basiques",
                         "Tableau de bord marketing ROI mensuel, attribution last-click",
                         "Attribution multi-touch, LTV client, marketing mix modeling, ROI >400%"]},
        ],
        "RH_CULTURE_DIGITALE": [
            {"text": "Vos collaborateurs bénéficient-ils de formations régulières aux outils et usages digitaux ?",
             "sub_axis": "Formation digitale", "weight": 4, "source_framework": "WEF DTI",
             "options": ["Aucune formation digitale organisée",
                         "Formations ponctuelles à la demande, sans plan structuré",
                         "Plan de formation annuel, e-learning disponible, 50% collaborateurs formés",
                         "Parcours de formation certifiant, 80%+ collaborateurs formés, digital champions désignés",
                         "Learning organization, upskilling continu, académie digitale interne, compétences mesurées"]},
            {"text": "La direction impulse-t-elle et porte-t-elle la transformation digitale ?",
             "sub_axis": "Leadership digital", "weight": 4, "source_framework": "McKinsey DQ",
             "options": ["La direction est absente ou réfractaire à la transformation digitale",
                         "Intérêt déclaré mais sans engagement budgétaire ni décisions concrètes",
                         "Un sponsor C-level identifié, quelques investissements digitaux validés",
                         "CDO ou équivalent nommé, transformation dans les priorités du COMEX",
                         "Toute la direction est digital-native, culture de l'innovation ancrée dans le modèle de gouvernance"]},
            {"text": "Disposez-vous de profils et compétences digitaux en interne (data, UX, tech, agile) ?",
             "sub_axis": "Compétences digitales", "weight": 3, "source_framework": "CMMI",
             "options": ["Aucun profil digital dédié en interne",
                         "1-2 profils tech isolés, recours systématique à l'externe",
                         "Équipe digitale de 3-5 personnes, compétences couvrant les besoins basiques",
                         "Squad pluridisciplinaire (UX, data, dev, agile), >10 profils digitaux",
                         "Centre d'excellence digital, 20%+ de l'effectif avec compétences avancées, talent brand forte"]},
        ],
        "OFFRES_DIGITALES": [
            {"text": "Proposez-vous des services ou produits nativement digitaux (sans équivalent physique) ?",
             "sub_axis": "Offres nativement digitales", "weight": 5, "source_framework": "MIT CISR",
             "options": ["100% offres physiques ou traditionnelles, aucune offre digitale native",
                         "Quelques offres dématérialisées (PDF, email) mais sans valeur ajoutée digitale",
                         "1-2 offres digitales en production, adoption client <20%",
                         "Catalogue digital complet, adoption >40%, revenus récurrents (SaaS/abonnement)",
                         "Plateforme digitale leader, API marketplace, >60% revenus digitaux, effet réseau"]},
            {"text": "Vos offres s'appuient-elles sur la data et l'IA pour créer de la valeur client ?",
             "sub_axis": "Offres data-driven & IA", "weight": 4, "source_framework": "Gartner DMM",
             "options": ["Offres sans composante data ou IA",
                         "Données collectées mais non exploitées dans les offres",
                         "Recommandations basiques, scoring manuel, insights ponctuels",
                         "IA intégrée dans 1-2 offres clés, personnalisation automatique, feedback loops",
                         "IA centrale dans toutes les offres, apprentissage continu, différenciation concurrentielle"]},
            {"text": "Votre organisation expose-t-elle des APIs permettant à des partenaires de créer des offres complémentaires ?",
             "sub_axis": "Open platform & APIs", "weight": 3, "source_framework": "WEF DTI",
             "options": ["Aucune API exposée, écosystème fermé",
                         "APIs internes uniquement, pas d'ouverture partenaires",
                         "Quelques APIs partenaires en production, documentation basique",
                         "API Management mature, portail développeurs actif, 10+ partenaires intégrés",
                         "Marketplace d'APIs, modèle économique plateforme, 50+ partenaires, revenu API >10%"]},
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            {"text": "Vos processus métier clés sont-ils automatisés de bout en bout (0 ressaisie manuelle) ?",
             "sub_axis": "Automatisation des processus", "weight": 4, "source_framework": "CMMI",
             "options": ["Aucune automatisation, 100% manuel",
                         "Quelques scripts isolés, sans flux bout-en-bout",
                         "Automatisation partielle, ressaisies encore fréquentes",
                         "Pipeline end-to-end pour les processus critiques, alertes configurées",
                         "0 ressaisie, orchestration complète (n8n/Power Automate), KPIs temps réel"]},
            {"text": "Une gouvernance digitale (comité de pilotage, PRA, conformité réglementaire) est-elle formalisée ?",
             "sub_axis": "Gouvernance & conformité", "weight": 4, "source_framework": "COBIT 2019",
             "options": ["Aucun cadre de gouvernance digitale",
                         "Responsabilités informelles, pas de comité dédié",
                         "Comité existant mais réuni irrégulièrement, PRA non testé",
                         "Comité trimestriel, PRA documenté et testé annuellement, budget digital défini",
                         "Gouvernance intégrée au CA, budget digital >2% CA, conformité RGPD/APDP certifiée"]},
            {"text": "Des initiatives d'innovation digitale (IoT, IA sectorielle, R&D partenariats) sont-elles engagées ?",
             "sub_axis": "Innovation digitale", "weight": 3, "source_framework": "WEF DTI",
             "options": ["Aucune initiative d'innovation digitale",
                         "Veille technologique informelle, pas de pilotes",
                         "1-2 pilotes IoT ou IA en cours, sans feuille de route",
                         "Programme d'innovation structuré, partenariats R&D actifs, 3+ pilotes en production",
                         "Innovation systémique, brevets déposés, lab dédié, écosystème partenaires étendu"]},
        ],
        "IT_DATA": [
            {"text": "L'infrastructure IT est-elle fiable, redondante et disponible en permanence (alimentation, connectivité) ?",
             "sub_axis": "Socle IT & infrastructure", "weight": 5, "source_framework": "ISO 27001",
             "options": ["Infrastructure sans redondance, pannes fréquentes",
                         "UPS basique, une seule connexion internet, pas de monitoring",
                         "Redondance partielle (backup électrique), monitoring manuel",
                         "Double alimentation + double connexion FAI, monitoring automatisé (UptimeRobot), SLA 99.5%",
                         "Infrastructure N+1 complète, bascule <30s, SLA 99.9%, PRA testé trimestriellement"]},
            {"text": "Des outils d'analyse de données et d'aide à la décision (dashboards, ML, lac de données) sont-ils déployés ?",
             "sub_axis": "Data & Analytics", "weight": 4, "source_framework": "Gartner DMM",
             "options": ["Aucun outil analytique, décisions basées sur l'intuition",
                         "Export Excel manuel, analyse ponctuelle",
                         "Tableaux de bord basiques, données peu actualisées, silos persistants",
                         "Lac de données opérationnel, dashboards temps réel, KPIs actionnés hebdo",
                         "ML prédictif en production, analytics géospatial/comportemental, data-driven decisions"]},
            {"text": "Une gouvernance des données (qualité, sécurité, valorisation, conformité RGPD/APDP) est-elle définie ?",
             "sub_axis": "Gouvernance des données", "weight": 4, "source_framework": "COBIT 2019",
             "options": ["Aucune politique de données, stockage anarchique",
                         "Règles informelles, pas de responsable données désigné",
                         "Politique de confidentialité publiée, DPO nommé mais sans processus formels",
                         "Registre des traitements tenu, classification données sensibles, audits annuels",
                         "Data mesh, data catalog, conformité RGPD certifiée, monétisation données active"]},
        ],
    }

    def _ensure_all_axes(self, data: dict, sector: str) -> dict:
        """Ensure every axis has exactly 3 questions. Top up with defaults if the LLM under-generates."""
        questions = data.get("questions", [])
        counts: dict[str, int] = {}
        for q in questions:
            counts[q["axis"]] = counts.get(q["axis"], 0) + 1

        order = len(questions)
        for axis, defaults in self._AXIS_DEFAULTS.items():
            needed = max(0, 3 - counts.get(axis, 0))
            for q in defaults[:needed]:
                order += 1
                questions.append({
                    "text": q["text"],
                    "axis": axis,
                    "sub_axis": q["sub_axis"],
                    "weight": q["weight"],
                    "display_order": order,
                    "source_framework": q["source_framework"],
                    "options": q["options"],
                })
        data["questions"] = questions
        return data

    def _get_axis_distribution(self, total: int) -> dict:
        axes = [
            "BUSINESS", "PROCESS", "INFORMATION_SYSTEM",
            "CANAUX_DISTRIBUTION", "MARKETING_COMMUNICATION",
            "RH_CULTURE_DIGITALE", "OFFRES_DIGITALES",
            "MODELE_OPERATIONNEL_INNOVATION", "IT_DATA",
        ]
        base = total // len(axes)
        remainder = total % len(axes)
        distribution = {axis: base for axis in axes}
        for i in range(remainder):
            distribution[axes[i]] += 1
        return distribution

    _LAST_RESORT_OPTIONS = [
        "Aucun dispositif ou outil en place",
        "Premiers essais isolés, sans processus établi",
        "Pratiques partiellement formalisées, adoption en cours",
        "Pratiques établies, mesurées, déployées à grande échelle",
        "Excellence opérationnelle, pilotage continu par la donnée",
    ]

    def _normalize(self, data: dict, sector: str, country: str, framework_names: list) -> dict:
        questions = []
        for i, q in enumerate(data.get("questions", []), start=1):
            raw_options = q.get("options", [])
            if isinstance(raw_options, list) and len(raw_options) == 5:
                options = raw_options
            else:
                options = self._LAST_RESORT_OPTIONS
            questions.append({
                "text": q.get("text", ""),
                "axis": q.get("axis", "BUSINESS").upper(),
                "sub_axis": q.get("sub_axis", "Général"),
                "weight": max(1, min(5, int(q.get("weight", 3)))),
                "display_order": q.get("display_order", i),
                "source_framework": q.get("source_framework", framework_names[0] if framework_names else ""),
                "options": options
            })

        return {
            "title": data.get("title", f"Questionnaire {sector} — {country}"),
            "description": data.get("description", ""),
            "sector": sector,
            "country": country,
            "frameworks_used": data.get("frameworks_used", framework_names),
            "questions": questions
        }
