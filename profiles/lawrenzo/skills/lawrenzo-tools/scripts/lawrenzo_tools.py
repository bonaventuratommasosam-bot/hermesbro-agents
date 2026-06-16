#!/usr/bin/env python3
"""
LAWrenzo Legal Tools — Contract generation, compliance, GDPR, document analysis.
Deploy: {{HERMES_HOME}}/profiles/lawrenzo/skills/lawrenzo-tools/scripts/lawrenzo_tools.py
"""

import sys, json, argparse
from datetime import datetime

from legal_config import legal_context, load

# ═══════════════════════════════════════════
# TOOL 1: CONTRACT GENERATOR
# ═══════════════════════════════════════════
def generate_contract(contract_type: str, parties: dict, terms: dict) -> dict:
    """Generate a draft contract based on type and parameters."""
    
    templates = {
        "nda": {
            "title": "ACCORDO DI RISERVATEZZA (NDA)",
            "clauses": [
                {"id": "1", "title": "Oggetto", "text": f"Le Parti si impegnano a mantenere riservate tutte le informazioni scambiate nell'ambito di {terms.get('purpose', '[oggetto della collaborazione]')}."},
                {"id": "2", "title": "Definizione di Informazioni Riservate", "text": "Costituiscono Informazioni Riservate: dati tecnici, commerciali, finanziari, know-how, strategie, elenchi clienti e qualsiasi altra informazione non pubblica."},
                {"id": "3", "title": "Durata", "text": f"L'obbligo di riservatezza permane per {terms.get('duration', '5')} anni dalla data di sottoscrizione."},
                {"id": "4", "title": "Esclusioni", "text": "Non sono considerate riservate le informazioni: (a) già pubbliche; (b) sviluppate indipendentemente; (c) ricevute legittimamente da terzi."},
                {"id": "5", "title": "Penale", "text": f"In caso di violazione, la Parte inadempiente corrisponderà una penale di €{terms.get('penalty', '10.000')}."},
                {"id": "6", "title": "Foro Competente", "text": f"Foro di {terms.get('jurisdiction', '[città]')}."},
            ]
        },
        "partnership": {
            "title": "ACCORDO DI PARTNERSHIP",
            "clauses": [
                {"id": "1", "title": "Oggetto e Scopo", "text": f"Le Parti costituiscono una partnership per {terms.get('purpose', '[scopo della partnership]')}."},
                {"id": "2", "title": "Obblighi delle Parti", "text": f"{parties.get('party_a', 'Parte A')} si impegna a: {terms.get('obligations_a', '[obblighi Parte A]')}. {parties.get('party_b', 'Parte B')} si impegna a: {terms.get('obligations_b', '[obblighi Parte B]')}."},
                {"id": "3", "title": "Ripartizione Ricavi", "text": f"I ricavi saranno ripartiti: {terms.get('revenue_split', '50% - 50%')}."},
                {"id": "4", "title": "Durata e Recesso", "text": f"Durata: {terms.get('duration', '12')} mesi. Recesso con preavviso di {terms.get('notice', '30')} giorni."},
                {"id": "5", "title": "Riservatezza", "text": "Le Parti si impegnano a non divulgare informazioni confidenziali relative alla partnership."},
                {"id": "6", "title": "Foro Competente", "text": f"Foro di {terms.get('jurisdiction', '[città]')}."},
            ]
        },
        "fornitura": {
            "title": "CONTRATTO DI FORNITURA",
            "clauses": [
                {"id": "1", "title": "Oggetto", "text": f"Il Fornitore si impegna a fornire a {parties.get('client', '[Cliente]')} i seguenti beni/servizi: {terms.get('goods', '[descrizione]')}."},
                {"id": "2", "title": "Prezzo e Pagamento", "text": f"Corrispettivo: €{terms.get('price', '[importo]')}. Pagamento: {terms.get('payment_terms', '30 giorni data fattura')}."},
                {"id": "3", "title": "Consegna", "text": f"Termini di consegna: {terms.get('delivery', '[termini]')}. Luogo: {terms.get('place', '[luogo]')}."},
                {"id": "4", "title": "Garanzia", "text": f"Garanzia di {terms.get('warranty', '12')} mesi dalla consegna."},
                {"id": "5", "title": "Penali", "text": f"Ritardo consegna: penale di €{terms.get('delay_penalty', '100')}/giorno."},
                {"id": "6", "title": "Risoluzione", "text": "In caso di inadempimento grave, la Parte adempiente può risolvere il contratto con preavviso scritto di 15 giorni."},
                {"id": "7", "title": "Foro Competente", "text": f"Foro di {terms.get('jurisdiction', '[città]')}."},
            ]
        },
        "consulenza": {
            "title": "CONTRATTO DI CONSULENZA",
            "clauses": [
                {"id": "1", "title": "Incarico", "text": f"Il Consulente svolgerà attività di {terms.get('service', '[tipo consulenza]')} per {parties.get('client', '[Cliente]')}."},
                {"id": "2", "title": "Compenso", "text": f"Compenso: €{terms.get('fee', '[importo]')} ({terms.get('billing', 'a corpo')})."},
                {"id": "3", "title": "Durata", "text": f"Durata: {terms.get('duration', '6')} mesi, dal {terms.get('start_date', '[data inizio]')}."},
                {"id": "4", "title": "Autonomia", "text": "Il Consulente opera in piena autonomia, senza vincolo di subordinazione."},
                {"id": "5", "title": "Riservatezza", "text": "Il Consulente è tenuto alla massima riservatezza sulle informazioni del Cliente."},
                {"id": "6", "title": "Recesso", "text": f"Recesso con preavviso di {terms.get('notice', '30')} giorni."},
            ]
        },
    }
    
    if contract_type not in templates:
        return {"error": f"Contract type '{contract_type}' not available. Available: {list(templates.keys())}"}
    
    template = templates[contract_type]
    return {
        "tool": "generate_contract",
        "timestamp": datetime.now().isoformat(),
        "contract_type": contract_type,
        "title": template["title"],
        "parties": parties,
        "clauses": template["clauses"],
        "full_text": format_contract(template, parties, terms),
        "warnings": check_contract_risks(contract_type, terms),
        "next_steps": [
            "1. Compilare i placeholder [] con i dati reali",
            "2. Far revisionare a un legale prima della firma",
            "3. Verificare foro competente e legge applicabile",
            "4. Firmare digitalmente o in originale"
        ]
    }


def format_contract(template: dict, parties: dict, terms: dict) -> str:
    lines = [template["title"], "=" * len(template["title"]), ""]
    lines.append(f"Tra: {parties.get('party_a', 'Parte A')}")
    if parties.get('party_b'):
        lines.append(f"E: {parties.get('party_b', 'Parte B')}")
    lines.append("")
    for clause in template["clauses"]:
        lines.append(f"{clause['id']}. {clause['title']}")
        lines.append(f"   {clause['text']}")
        lines.append("")
    lines.append(f"Data: {terms.get('date', datetime.now().strftime('%d/%m/%Y'))}")
    lines.append(f"Firma {parties.get('party_a', 'Parte A')}: ________________")
    if parties.get('party_b'):
        lines.append(f"Firma {parties.get('party_b', 'Parte B')}: ________________")
    return "\n".join(lines)


def check_contract_risks(contract_type: str, terms: dict) -> list[str]:
    risks = []
    if contract_type == "nda":
        if not terms.get('penalty'):
            risks.append("⚠️ NDA senza penale specificata — difficile da far valere in giudizio")
        if not terms.get('jurisdiction'):
            risks.append("⚠️ Foro competente non specificato — in caso di disputa, incertezza")
    elif contract_type in ("partnership", "fornitura", "consulenza"):
        if not terms.get('jurisdiction'):
            risks.append("⚠️ Foro competente non specificato")
    return risks


# ═══════════════════════════════════════════
# TOOL 2: GDPR COMPLIANCE CHECK
# ═══════════════════════════════════════════
def gdpr_check(business_type: str, data_collected: list[str]) -> dict:
    """Assess GDPR compliance requirements based on business type and data collected."""
    
    requirements = []
    risk_level = "LOW"
    
    for data_type in data_collected:
        dt = data_type.lower()
        if any(w in dt for w in ["email", "nome", "telefono"]):
            requirements.append({"req": "Informativa privacy", "priority": "OBBLIGATORIO", "detail": "Deve indicare: titolare, finalità, base giuridica, diritti, tempi conservazione"})
        if any(w in dt for w in ["pagamento", "carta", "iban", "bancari"]):
            requirements.append({"req": "Nomina responsabile pagamenti", "priority": "OBBLIGATORIO", "detail": "Il processore di pagamento deve essere nominato responsabile ex art. 28"})
            risk_level = "MEDIUM"
        if any(w in dt for w in ["sanitari", "medici", "salute"]):
            requirements.append({"req": "Base giuridica rafforzata", "priority": "CRITICAL", "detail": "Dati particolari ex art. 9 — serve consenso esplicito o base giuridica specifica"})
            risk_level = "HIGH"
        if any(w in dt for w in ["cookies", "tracciamento", "ip"]):
            requirements.append({"req": "Cookie policy + consenso", "priority": "OBBLIGATORIO", "detail": "Banner cookie con consenso granulare, cookie tecnici esclusi"})
    
    # Business-type specific
    if "ecommerce" in business_type.lower() or "e-commerce" in business_type.lower():
        requirements.append({"req": "Termini e condizioni di vendita", "priority": "OBBLIGATORIO", "detail": "Diritto di recesso 14 giorni, garanzia legale 2 anni, informazioni precontrattuali"})
    if "saas" in business_type.lower():
        requirements.append({"req": "DPA (Data Processing Agreement)", "priority": "OBBLIGATORIO", "detail": "Accordo trattamento dati con ciascun cliente business"})
    
    return {
        "tool": "gdpr_check",
        "timestamp": datetime.now().isoformat(),
        "business_type": business_type,
        "data_collected": data_collected,
        "overall_risk": risk_level,
        "requirements": requirements,
        "mandatory_documents": [
            "Informativa privacy (art. 13-14 GDPR)",
            "Registri trattamento (art. 30) — se >250 dipendenti o trattamento rischioso",
            "Nomine responsabili (art. 28) — per ogni fornitore che tratta dati",
            "Cookie policy — se si usano cookie non tecnici",
        ],
        "deadlines": {
            "data_breach_notification": "72 ore dall'evento",
            "dsar_response": "30 giorni (prorogabili)",
            "privacy_review": "Almeno annuale"
        },
        "fine_risk": {
            "LOW": "Fino a €10M o 2% fatturato",
            "MEDIUM": "Fino a €10M o 2% fatturato",
            "HIGH": "Fino a €20M o 4% fatturato"
        }.get(risk_level, "N/A")
    }


# ═══════════════════════════════════════════
# TOOL 3: TERMS ANALYZER
# ═══════════════════════════════════════════
def analyze_terms(terms_text: str, jurisdiction: str = "IT") -> dict:
    """Analyze terms of service / contract for risks and compliance."""
    
    flags = []
    text_lower = terms_text.lower()
    
    checks = [
        ("auto-rinnovo", "Rinnovo automatico", "Verificare durata e preavviso per disdetta. In Italia il tacito rinnovo è valido ma deve essere esplicito."),
        ("penale", "Clausola penale", "Verificare proporzionalità. Penali manifestamente eccessive possono essere ridotte dal giudice (art. 1382 c.c.)."),
        ("foro", "Foro competente", "Verificare che non sia eccessivamente oneroso per una delle parti (es. foro estero per consumatore italiano)."),
        ("riservatezza", "Riservatezza / Confidentiality", "Verificare durata e ambito. Obblighi perpetui possono essere nulli."),
        ("limitazione", "Limitazione responsabilità", "In Italia non è possibile limitare la responsabilità per dolo o colpa grave."),
        ("dati personali", "Trattamento dati personali", "Deve esserci riferimento alla normativa privacy applicabile (GDPR)."),
        ("legge applicabile", "Legge applicabile", f"Verificare compatibilità con {jurisdiction}."),
        ("arbitrato", "Clausola arbitrale", "Verificare che non sia vessatoria (doppia sottoscrizione ex art. 1341 c.c.)."),
        ("esclusiva", "Esclusiva", "Verificare durata e compenso. Clausole di esclusiva senza corrispettivo possono essere abusive."),
    ]
    
    for keyword, title, advice in checks:
        if keyword in text_lower:
            flags.append({"flag": title, "severity": "HIGH" if keyword in ["foro", "penale", "limitazione"] else "MEDIUM", "advice": advice})
    
    return {
        "tool": "analyze_terms",
        "timestamp": datetime.now().isoformat(),
        "jurisdiction": jurisdiction,
        "flags_found": len(flags),
        "flags": flags,
        "overall_risk": "HIGH" if any(f["severity"] == "HIGH" for f in flags) else ("MEDIUM" if flags else "LOW"),
        "recommendation": "Revisione legale consigliata" if len(flags) > 3 else "Contratto relativamente standard" if flags else "Nessuna criticità evidente",
        "clausole_vessatorie_1341": [
            "Limitazioni di responsabilità",
            "Facoltà di recedere senza giusta causa",
            "Decadenza da termini",
            "Restrizioni alla libertà contrattuale",
            "Clausola compromissoria / arbitrato"
        ]
    }


# ═══════════════════════════════════════════
# TOOL 4: REGULATORY WATCH
# ═══════════════════════════════════════════
def regulatory_watch(sector: str, jurisdiction: str = "IT") -> dict:
    """Alert on relevant regulations for a given sector."""
    
    sector_alerts = {
        "crypto": [
            {"regulation": "MiCA (Markets in Crypto-Assets)", "status": "In vigore da giugno 2024", "impact": "HIGH", "action": "Registrazione presso CONSOB o autorità nazionale competente"},
            {"regulation": "Quadro RT / Dichiarazione crypto", "status": "Attivo", "impact": "HIGH", "action": "Monitoraggio plusvalenze >€2.000 e obbligo Quadro RT"},
            {"regulation": "Travel Rule (FATF)", "status": "In vigore", "impact": "MEDIUM", "action": "KYC/AML su transazioni >€1.000"},
        ],
        "food": [
            {"regulation": "Reg. CE 852/2004 (HACCP)", "status": "In vigore", "impact": "HIGH", "action": "Piano HACCP aggiornato e formazione personale"},
            {"regulation": "Reg. UE 1169/2011 (Etichettatura)", "status": "In vigore", "impact": "MEDIUM", "action": "Verifica informazioni obbligatorie su menu e prodotti"},
            {"regulation": "D.lgs 231/2001 (Sicurezza alimentare)", "status": "In vigore", "impact": "MEDIUM", "action": "Nomina responsabile e audit periodici"},
        ],
        "saas": [
            {"regulation": "GDPR (Reg. UE 2016/679)", "status": "In vigore", "impact": "HIGH", "action": "DPA con clienti, registro trattamenti, nomina DPO se necessario"},
            {"regulation": "AI Act (Reg. UE 2024/1689)", "status": "Entrata in vigore progressiva 2025-2027", "impact": "HIGH", "action": "Classificare i sistemi AI per livello di rischio; obblighi rafforzati per high-risk"},
            {"regulation": "DORA (Digital Operational Resilience Act)", "status": "In vigore da gennaio 2025", "impact": "MEDIUM", "action": "Se fornitore ICT a banche/assicurazioni: compliance DORA"},
        ],
        "ecommerce": [
            {"regulation": "D.lgs 70/2003 (E-commerce)", "status": "In vigore", "impact": "HIGH", "action": "Informativa precontrattuale, diritto recesso 14gg, garanzia 2 anni"},
            {"regulation": "Omnibus Directive (UE 2019/2161)", "status": "In vigore", "impact": "MEDIUM", "action": "Trasparenza su sconti e recensioni verificate"},
            {"regulation": "P2B Regulation (UE 2019/1150)", "status": "In vigore", "impact": "LOW", "action": "Solo se marketplace: trasparenza ranking e condizioni"},
        ],
    }
    
    alerts = sector_alerts.get(sector.lower(), [
        {"regulation": "Nessuna alert specifica", "status": "N/A", "impact": "LOW", "action": "Nessuna azione immediata"}
    ])
    
    return {
        "tool": "regulatory_watch",
        "timestamp": datetime.now().isoformat(),
        "sector": sector,
        "jurisdiction": jurisdiction,
        "alerts": alerts,
        "disclaimer": "Questa non è consulenza legale. Verificare sempre con un professionista abilitato.",
        "monitoring_advice": [
            f"Monitorare Gazzetta Ufficiale UE mensilmente per {sector}",
            f"Iscriversi a newsletter regolatorie di settore",
            "Impostare Google Alert per keywords rilevanti"
        ]
    }


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="LAWrenzo Legal Tools")
    parser.add_argument("tool", help="Tool: generate_contract, gdpr_check, analyze_terms, regulatory_watch")
    parser.add_argument("--contract_type", choices=["nda", "partnership", "fornitura", "consulenza"])
    parser.add_argument("--party_a", help="Parte A")
    parser.add_argument("--party_b", help="Parte B")
    parser.add_argument("--purpose", help="Scopo/oggetto")
    parser.add_argument("--duration", help="Durata")
    parser.add_argument("--jurisdiction", default="IT")
    parser.add_argument("--business_type", help="Tipo business per GDPR check")
    parser.add_argument("--data_collected", help="Dati raccolti (comma-separated)")
    parser.add_argument("--terms_text", help="Testo termini da analizzare")
    parser.add_argument("--sector", help="Settore per regulatory watch")
    parser.add_argument("--json_input", help="JSON input completo")
    
    args = parser.parse_args()
    
    # Merge JSON input if provided
    if args.json_input:
        ji = json.loads(args.json_input)
        for k, v in ji.items():
            if not getattr(args, k, None):
                setattr(args, k, v)
    
    ctx = legal_context(load())

    if args.tool == "generate_contract":
        result = generate_contract(
            args.contract_type or "nda",
            {
                "party_a": args.party_a or ctx["client"],
                "party_b": args.party_b or "",
            },
            {
                "purpose": args.purpose or "",
                "duration": args.duration or "5",
                "jurisdiction": ctx["foro"],
            },
        )
    elif args.tool == "gdpr_check":
        data = [d.strip() for d in (args.data_collected or "").split(",") if d.strip()]
        result = gdpr_check(args.business_type or ctx["sector"], data)
    elif args.tool == "analyze_terms":
        result = analyze_terms(args.terms_text or "", args.jurisdiction or ctx["country"])
    elif args.tool == "regulatory_watch":
        result = regulatory_watch(args.sector or ctx["sector"], args.jurisdiction or ctx["country"])
    else:
        result = {
            "error": f"Unknown tool: {args.tool}",
            "available": ["generate_contract", "gdpr_check", "analyze_terms", "regulatory_watch"],
        }

    result["disclaimer"] = ctx["disclaimer"]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
