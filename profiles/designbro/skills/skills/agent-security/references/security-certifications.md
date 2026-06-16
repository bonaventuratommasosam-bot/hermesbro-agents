# Security Certifications & Audits — Cost & Accessibility Guide

## Certified Audits (formal, recognized)

### SOC 2 Type II
- **What it certifies:** Security, availability, processing integrity, confidentiality, privacy
- **Who recognizes it:** US enterprise, SaaS buyers, investors
- **Cost:** $5,000–30,000 (startup tier)
- **Timeline:** 3–6 months (2–3 with automation)
- **Automation platforms:** Vanta, Drata, Secureframe — cut time/cost significantly
- **When to get it:** When you have paying enterprise customers who require it

### ISO 27001
- **What it certifies:** Information Security Management System (ISMS)
- **Who recognizes it:** EU enterprise, governments, international partners
- **Cost:** $10,000–50,000
- **Timeline:** 6–12 months
- **When to get it:** When operating in EU markets or targeting enterprise

### ISO 42001
- **What it certifies:** AI governance and management
- **Who recognizes it:** International, growing adoption
- **When to get it:** Relevant for AI products specifically — newer standard

## Penetration Testing / Security Audits (technical, recognized in industry)

- **Schellman** — independent auditor, SOC 2 + ISO + pentest
- **Coalfire** — compliance + pentest for cloud/SaaS
- **Qualysec** — manual VAPT, detailed reports
- **Cure53** — highly respected in EU, web/JS/CSS audits
- **HackerOne** — bug bounty + on-demand pentest
- Cost: $3,000–15,000 for full web app pentest

## Budget-Friendly Options

### Bug Bounty (pay per finding)
- **HackerOne** or **Bugcrowd** — pool from $150–2,000
- Pay only for vulnerabilities actually found
- Recognized in the industry as legitimate security practice
- Good for: startups post-launch, before SOC 2 investment

### OWASP ASVS Self-Assessment (free)
- Application Security Verification Standard
- 200+ security controls checklist
- Self-attestation — not externally certified but industry-recognized framework
- Good for: early-stage, internal security posture documentation

### Security Policy + Responsible Disclosure (free)
- Publish `/.well-known/security.txt` with contact info
- Publish a security policy page
- Shows professionalism to users/partners

### OpenSSF Scorecard (free, automated)
- If code is on GitHub, analyzes supply chain security automatically
- Generates public score — verifiable by anyone
- Good for: open-source projects

## Micro-Budget Reality Check

For a startup with <€50/month budget:
1. **Do the audit yourself** (or with AI agent) — fix the actual vulnerabilities
2. **Add security.txt** + responsible disclosure policy
3. **Run OWASP ASVS self-assessment**
4. **Open bug bounty** with small pool when you have users
5. **SOC 2** only when enterprise customers demand it and revenue justifies it

The "certification" that matters most early on is clean code + proper headers + security policy — not a paid certificate.
