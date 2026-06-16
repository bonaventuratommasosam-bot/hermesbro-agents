#!/usr/bin/env python3
"""
HermesBots Outbound Email Sender
Sends cold emails via local Postfix with rate limiting and tracking.
"""

import csv
import subprocess
import time
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# ── Config ──
TEMPLATES_DIR = Path("/root/hermes-landing/outbound/templates")
LEADS_FILE = Path("/root/hermes-landing/outbound/leads.csv")
SENT_LOG = Path("/root/hermes-landing/outbound/sent.json")
FROM_EMAIL = "HermesBro@hermesbro.cloud"
FROM_NAME = "HermesBro | HermesBots"
DEMO_LINK = "https://hermesbro.cloud/#contatti"
BATCH_SIZE = 20  # emails per run
DELAY_SECONDS = 30  # delay between emails (avoid spam flags)

TEMPLATE_MAP = {
    "ristorazione": "ristoranti.md",
    "ristoranti": "ristoranti.md",
    "studi-legali": "studi-legali.md",
    "legale": "studi-legali.md",
    "avvocati": "studi-legali.md",
    "e-commerce": "e-commerce.md",
    "ecommerce": "e-commerce.md",
    "startup": "startup.md",
    "tech": "startup.md",
    "pmi": "pmi-generica.md",
    "pmi-generica": "pmi-generica.md",
}


def load_sent():
    """Load list of already-sent emails."""
    if SENT_LOG.exists():
        return json.loads(SENT_LOG.read_text())
    return {"sent": [], "last_run": None}


def save_sent(data):
    """Save sent log."""
    SENT_LOG.write_text(json.dumps(data, indent=2))


def load_template(sector):
    """Load email template for sector."""
    template_file = TEMPLATE_MAP.get(sector.lower().strip())
    if not template_file:
        template_file = "pmi-generica.md"  # fallback

    path = TEMPLATES_DIR / template_file
    if not path.exists():
        print(f"Template not found: {path}")
        return None

    content = path.read_text()

    # Extract subject and body from markdown
    lines = content.strip().split("\n")
    subject = ""
    body_lines = []
    in_body = False

    for line in lines:
        if line.startswith("**Oggetto:**"):
            subject = line.replace("**Oggetto:**", "").strip()
        elif line.startswith("#"):
            continue  # skip headers
        elif subject and not in_body and line.strip() == "":
            in_body = True
            continue
        elif in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    return subject, body


def send_email(to_email, to_name, subject, body):
    """Send email via local Postfix."""
    # Sanitize
    to_email = to_email.strip().lower()
    to_name = (to_name or "").strip()

    # Personalize
    subject = subject.replace("{nome}", to_name)
    body = body.replace("{nome}", to_name)
    body = body.replace("{link}", DEMO_LINK)

    # Build RFC 822 message
    msg = f"""From: {FROM_NAME} <{FROM_EMAIL}>
To: {to_email}
Subject: {subject}
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit

{body}
"""

    try:
        proc = subprocess.run(
            ["/usr/sbin/sendmail", "-t", "-oi"],
            input=msg.encode("utf-8"),
            capture_output=True,
            timeout=30,
        )
        if proc.returncode == 0:
            return True
        else:
            print(f"  sendmail error: {proc.stderr.decode()}")
            return False
    except Exception as e:
        print(f"  Exception: {e}")
        return False


def load_leads():
    """Load leads from CSV."""
    if not LEADS_FILE.exists():
        print(f"Leads file not found: {LEADS_FILE}")
        print("Create it with columns: name,email,sector,company")
        return []

    leads = []
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def create_sample_leads():
    """Create a sample leads CSV for testing."""
    LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)

    sample = [
        {"name": "Mario Rossi", "email": "mario@ristorante-bella.it", "sector": "ristorazione", "company": "Ristorante Bella"},
        {"name": "Laura Bianchi", "email": "laura@studio-legale-bianchi.it", "sector": "studi-legali", "company": "Studio Legale Bianchi"},
        {"name": "Giuseppe Verdi", "email": "giuseppe@shopverdi.it", "sector": "e-commerce", "company": "ShopVerdi"},
    ]

    with open(LEADS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email", "sector", "company"])
        writer.writeheader()
        writer.writerows(sample)

    print(f"Sample leads created at {LEADS_FILE}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
        create_sample_leads()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        dry_run = True
        print("DRY RUN MODE - no emails will be sent\n")
    else:
        dry_run = False

    leads = load_leads()
    if not leads:
        print("No leads found. Run with --create-sample to create a sample CSV.")
        return

    sent_data = load_sent()
    sent_emails = set(sent_data["sent"])

    # Filter out already-sent
    pending = [l for l in leads if l["email"] not in sent_emails]
    print(f"Total leads: {len(leads)}, Already sent: {len(sent_emails)}, Pending: {len(pending)}")

    if not pending:
        print("All leads have been contacted.")
        return

    # Take batch
    batch = pending[:BATCH_SIZE]
    print(f"Sending batch of {len(batch)} emails...\n")

    sent_count = 0
    for i, lead in enumerate(batch):
        email = lead["email"].strip()
        name = lead.get("name", "").strip()
        sector = lead.get("sector", "pmi").strip()
        company = lead.get("company", "").strip()

        template = load_template(sector)
        if not template:
            print(f"  [{i+1}] SKIP {email} - no template for sector '{sector}'")
            continue

        subject, body = template

        # Add company name if available
        if company:
            body = body.replace("la vostra azienda", company)
            body = body.replace("la vostra attivita", company)

        if dry_run:
            print(f"  [{i+1}] DRY RUN: Would send to {email} ({sector})")
            print(f"         Subject: {subject}")
            print()
        else:
            print(f"  [{i+1}] Sending to {email} ({sector})...", end=" ")
            success = send_email(email, name, subject, body)
            if success:
                print("OK")
                sent_data["sent"].append(email)
                sent_count += 1
            else:
                print("FAILED")

            if i < len(batch) - 1:
                time.sleep(DELAY_SECONDS)

    if not dry_run:
        sent_data["last_run"] = datetime.now().isoformat()
        save_sent(sent_data)
        print(f"\nDone. Sent {sent_count}/{len(batch)} emails.")
        print(f"Total sent so far: {len(sent_data['sent'])}")


if __name__ == "__main__":
    main()
