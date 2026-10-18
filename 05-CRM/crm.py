#!/usr/bin/env python3
"""
Free CRM — Track leads, clients, and deals for your solar agency.
Runs entirely on your computer. No internet needed. No fees.

Usage:
  python crm.py                    # Interactive menu
  python crm.py add                # Add a lead manually
  python crm.py import FILE.csv    # Import from CSV
  python crm.py list               # List all leads
  python crm.py pipeline           # Sales pipeline view
  python crm.py stats              # Your numbers
  python crm.py followup           # Who needs follow-up today?
"""

import csv
import io
import os
import sys
import json
from datetime import datetime, timedelta

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_FILE = os.path.join(os.path.dirname(__file__), "crm_data.json")

STATUSES = [
    "new", "contacted", "replied", "meeting_booked",
    "proposal_sent", "negotiating", "client", "lost"
]

SERVICES = [
    "seo", "social", "google_ads", "meta_ads",
    "website", "full_package", "audit"
]


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"leads": [], "next_id": 1}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_lead(data, name, city="", phone="", email="", website="", source="manual", notes=""):
    lead = {
        "id": data["next_id"],
        "name": name,
        "city": city,
        "phone": phone,
        "email": email,
        "website": website,
        "source": source,
        "status": "new",
        "service_interest": "",
        "deal_value": 0,
        "notes": notes,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_contact": "",
        "next_followup": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
    }
    data["leads"].append(lead)
    data["next_id"] += 1
    return lead


def import_csv(data, filepath):
    imported = 0
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_names = {l["name"].lower() for l in data["leads"]}

        for row in reader:
            name = (row.get("name") or "").strip()
            if not name or name.lower() in existing_names:
                continue

            add_lead(
                data,
                name=name,
                city=row.get("city", ""),
                phone=row.get("phone", ""),
                email=row.get("email", ""),
                website=row.get("website", ""),
                source=row.get("source", "import"),
                notes=row.get("notes", ""),
            )
            imported += 1

    return imported


def list_leads(data, status_filter=None):
    leads = data["leads"]
    if status_filter:
        leads = [l for l in leads if l["status"] == status_filter]

    if not leads:
        print("No leads found.")
        return

    print(f"\n{'ID':<4} {'Name':<30} {'City':<12} {'Status':<16} {'Last Contact':<12}")
    print("-" * 80)
    for l in leads:
        print(f"{l['id']:<4} {l['name'][:28]:<30} {l['city'][:10]:<12} "
              f"{l['status']:<16} {l['last_contact'] or 'never':<12}")


def show_pipeline(data):
    print("\n" + "=" * 60)
    print("SALES PIPELINE")
    print("=" * 60)

    for status in STATUSES:
        leads = [l for l in data["leads"] if l["status"] == status]
        if leads:
            print(f"\n[{status.upper()}] ({len(leads)})")
            for l in leads:
                value = f"₹{l['deal_value']:,}" if l["deal_value"] else ""
                print(f"  #{l['id']} {l['name'][:35]:<37} {value}")


def show_stats(data):
    leads = data["leads"]
    total = len(leads)

    print("\n" + "=" * 60)
    print("YOUR NUMBERS")
    print("=" * 60)
    print(f"Total leads: {total}")

    for status in STATUSES:
        count = sum(1 for l in leads if l["status"] == status)
        if count:
            print(f"  {status}: {count}")

    clients = [l for l in leads if l["status"] == "client"]
    monthly_recurring = sum(l["deal_value"] for l in clients if "retainer" in l.get("notes", "").lower() or l["deal_value"] > 0)
    print(f"\nActive clients: {len(clients)}")
    print(f"Pipeline value: ₹{sum(l['deal_value'] for l in leads):,}")

    if total:
        conversion = len(clients) / total * 100
        print(f"Lead→Client conversion: {conversion:.1f}%")


def show_followups(data):
    today = datetime.now().strftime("%Y-%m-%d")
    week_out = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    print(f"\n{'=' * 60}")
    print(f"FOLLOW-UPS DUE (as of {today})")
    print(f"{'=' * 60}")

    due = [l for l in data["leads"]
           if l["next_followup"] and l["next_followup"] <= week_out
           and l["status"] not in ("client", "lost")]

    if not due:
        print("No follow-ups due. Enjoy the free time!")
        return

    for l in sorted(due, key=lambda x: x["next_followup"]):
        overdue = "⚠️ OVERDUE" if l["next_followup"] < today else ""
        print(f"\n#{l['id']} {l['name']} ({l['city']})")
        print(f"   Status: {l['status']} | Due: {l['next_followup']} {overdue}")
        print(f"   Contact: {l['email'] or l['phone'] or 'no contact info'}")


def update_status(data):
    lead_id = input("Lead ID: ").strip()
    lead = next((l for l in data["leads"] if str(l["id"]) == lead_id), None)
    if not lead:
        print("Lead not found.")
        return

    print(f"Current status: {lead['status']}")
    print("New status options:", ", ".join(STATUSES))
    new_status = input("New status: ").strip().lower()
    if new_status not in STATUSES:
        print("Invalid status.")
        return

    lead["status"] = new_status
    lead["last_contact"] = datetime.now().strftime("%Y-%m-%d")
    lead["next_followup"] = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    if new_status == "client":
        value = input("Deal value (₹, monthly retainer): ").strip()
        if value.isdigit():
            lead["deal_value"] = int(value)

    print(f"Updated #{lead['id']} → {new_status}")


def interactive_menu():
    data = load_data()

    while True:
        print("\n" + "=" * 50)
        print("SOLAR AGENCY CRM — Free Forever")
        print("=" * 50)
        print("1. Add lead")
        print("2. List all leads")
        print("3. Sales pipeline")
        print("4. My stats")
        print("5. Today's follow-ups")
        print("6. Update lead status")
        print("7. Import from CSV")
        print("8. Search leads")
        print("0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            if name:
                city = input("City: ").strip()
                phone = input("Phone: ").strip()
                email = input("Email: ").strip()
                website = input("Website: ").strip()
                lead = add_lead(data, name, city, phone, email, website)
                save_data(data)
                print(f"Added #{lead['id']}: {name}")

        elif choice == "2":
            list_leads(data)

        elif choice == "3":
            show_pipeline(data)

        elif choice == "4":
            show_stats(data)

        elif choice == "5":
            show_followups(data)

        elif choice == "6":
            update_status(data)
            save_data(data)

        elif choice == "7":
            filepath = input("CSV path: ").strip()
            count = import_csv(data, filepath)
            save_data(data)
            print(f"Imported {count} leads.")

        elif choice == "8":
            query = input("Search: ").strip().lower()
            results = [l for l in data["leads"]
                       if query in l["name"].lower()
                       or query in l["city"].lower()
                       or query in l.get("email", "").lower()]
            for l in results:
                print(f"#{l['id']} {l['name']} ({l['city']}) — {l['status']}")

        elif choice == "0":
            save_data(data)
            print("Saved. Bye!")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = load_data()
        cmd = sys.argv[1]

        if cmd == "add" and len(sys.argv) > 2:
            add_lead(data, sys.argv[2])
            save_data(data)
            print("Added.")

        elif cmd == "import" and len(sys.argv) > 2:
            count = import_csv(data, sys.argv[2])
            save_data(data)
            print(f"Imported {count} leads.")

        elif cmd == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            list_leads(data, status)

        elif cmd == "pipeline":
            show_pipeline(data)

        elif cmd == "stats":
            show_stats(data)

        elif cmd == "followup":
            show_followups(data)

        else:
            print(__doc__)
    else:
        interactive_menu()
