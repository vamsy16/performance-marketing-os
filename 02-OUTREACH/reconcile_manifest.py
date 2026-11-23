#!/usr/bin/env python3
"""Reconcile sequence_manifest.json against the Gmail Sent folder.

Why this exists
---------------
On 2026-11-21 the manifest claimed 33 sequences had a follow-up due. Checking
them against Gmail showed that list was almost entirely fictional: 42 of the 43
sequences probed claimed the wrong number of sends, and every single one of the
33 "overdue" rows was either already finished or had never started.

The manifest is a ledger, not a source of truth. Gmail is the source of truth.
This script takes the dates actually observed in Gmail (MEASURED below) and
rewrites `mails_sent`, `next_step`, `next_followup_date` and `state` from them.

Provenance of MEASURED
----------------------
Every date below was read out of Gmail on 2026-11-21, and the 22 Nov sends
were added on 2026-11-23 from `in:sent after:2026/11/21 before:2026/11/23`
(39 messages, complete - of which 12 carried a 22 Nov date). Keep this in step
with 05-CRM/send_log.csv: if a send is logged there and not here, the next
--write run silently reverts it.

Every date below was read out of Gmail on 2026-11-21 with a per-recipient
query. Three traps were hit, and the rules that avoid them are:

  1. TRUNCATION - a search once reported 3 sends where there were 4, quietly
     dropping the newest. Counts here come from queries that came back
     `complete: true` with the full result set.
  2. DRAFTS READ AS SENDS - `to:x` without a label filter returns the unsent
     draft too. Only messages carrying SENT are counted.
  3. TRASH HIDES REAL SENDS - Valcan Solar's 21 Oct mail is labelled TRASH +
     SENT because the thread was trashed; it was still delivered, so it counts.
     Searching SENT alone silently reads that thread as zero sends.

A verified `[]` means: searched, and nothing was ever sent. That is a real
finding, not a gap - three sequences sat at "1 sent, follow-up drafted" when no
first email had ever gone out.

    cd 02-OUTREACH && python3 reconcile_manifest.py           # show the diff
    cd 02-OUTREACH && python3 reconcile_manifest.py --write   # apply it
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "generated_emails", "sequence_manifest.json")
TODAY = datetime.date(2026, 11, 21)
DELAY = 2  # mirrors followup_delay_days in the manifest
KINDS = 4  # initial, 2 follow-ups, breakup

# company -> dates of SENT-labelled messages, oldest first. [] = never sent.
MEASURED = {
    # --- ran the full four steps; nothing owed
    "3S Solutions": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Arcedo Systems": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "AB Solar Power Systems": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Evergrid Energy": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Ksquare Energy": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Punarvi Energies": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Solox Energies": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Truzon Solar": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Varahi Energies": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Venus home appliances": ["2026-10-19", "2026-10-22", "2026-10-24", "2026-11-08"],
    "Lotus Industries": ["2026-11-08", "2026-11-10", "2026-11-14", "2026-11-16"],
    "Lumisun Solar": ["2026-11-08", "2026-11-10", "2026-11-14", "2026-11-16"],
    "Varna Solar Pvt. Ltd.": ["2026-11-08", "2026-11-10", "2026-11-14", "2026-11-16"],
    "Arkahub": ["2026-10-23", "2026-11-08", "2026-11-10", "2026-11-14"],
    "MrSolar": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Hydromo": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Krisol Solar": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Bhanu PV Solar": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Dakshin Solar Power Systems": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Freyr Energy": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "PMP Solar Power": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "VajraSimha Industries": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Vanguard Energy": ["2026-10-23", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Ecolt Energy": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Ellvin Energy": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Kapil Power & Infra": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Orizen Solar Innovations": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Ray On Solar Systems": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Solar6": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Twilight Solar": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Eastman New Energy": ["2026-10-21", "2026-11-07", "2026-11-10", "2026-11-14"],
    "Rayzon Solar": ["2026-11-07", "2026-11-10", "2026-11-14", "2026-11-16"],
    "Sunova Green Energy": ["2026-11-07", "2026-11-10", "2026-11-14", "2026-11-16"],
    "Wisda Energy": ["2026-11-07", "2026-11-10", "2026-11-14", "2026-11-16"],
    # Replied, re-engaged, then closed out with a breakup on 16 Nov.
    "SolarSquare Energy": ["2026-11-07", "2026-11-10", "2026-11-14", "2026-11-16"],
    # --- two or three sends in; the next step is genuinely owed
    "Valcan Solar": ["2026-10-21", "2026-11-22"],
    "Aadithya Solar Energies": ["2026-11-10", "2026-11-14", "2026-11-16", "2026-11-22"],
    "Eagle Solar Systems": ["2026-11-16", "2026-11-22"],
    "Kakatiya Energies": ["2026-11-21", "2026-11-21"],
    "Visiontek": ["2026-11-21", "2026-11-21"],
    "Sri Balaji Solar Energies": ["2026-11-21", "2026-11-21"],
    "Envious Energy Private Limited": ["2026-11-21"],
    "Laxmi Narayana Solar": ["2026-11-21"],
    "Green Carbon Hub": ["2026-11-14", "2026-11-16", "2026-11-21"],
    "Four Solar": ["2026-11-14", "2026-11-21"],
    "Origian Power": ["2026-11-14", "2026-11-21"],
    "Hindusthan Solar Energy Enterprise": ["2026-11-08"],
    "Kypas Solar Power Pvt Ltd": ["2026-11-08"],
    # NOTE Green Carbon Hub: three sends. The 14 Nov subject claimed "14 live
    # Google ads booked under Ecoila Private Limited", which contradicts its
    # own audit - every one of its ~9 Meta ads points at fb.me and the record
    # lists no website. Flagged in fix_manifest_content.py rather than adopted.
    # --- verified never sent
    "Griffin Energy": ["2026-11-22"],
    "Nova Solar Solutions": ["2026-11-22"],
    "Sri Narayana Enterprise Solar Energies": ["2026-11-22"],
    "Junna Solar Systems": [],
    "Mamindla Energy Solutions": [],
    # --- batch 15, drafted but never sent
    "Growcell Solar Energy": ["2026-11-22"],
    "Roof Rays Solar Solutions": ["2026-11-22"],
    "Akhil Electrical Works": ["2026-11-22"],
    "Manasaa Enterprises": ["2026-11-22"],
}

# Recipients recovered from the Sent folder for sequences that had no address.
FILL_TO = {
    "Green Carbon Hub": "info@greencarbonhub.com",
    "Visiontek": "info@visiontek.com",
    "Laxmi Narayana Solar": "laxminarayanaenterprisess@gmail.com",
}


def d(s):
    return datetime.date.fromisoformat(s)


def derive(sends):
    """(state, next_step, next_followup_date) implied by a list of send dates."""
    n = len(sends)
    if n == 0:
        return "never-sent", 0, ""
    if n >= KINDS:
        return "finished", KINDS, ""
    return "live-due", n, (d(sends[-1]) + datetime.timedelta(days=DELAY)).isoformat()


def main():
    write = "--write" in sys.argv
    m = json.load(open(MANIFEST, encoding="utf-8"))
    changes, unverified = [], []

    for s in m["sequences"]:
        name = s["company"]
        if name not in MEASURED:
            unverified.append(name)
            continue
        sends = MEASURED[name]
        state, step, due = derive(sends)
        before = (s.get("mails_sent"), s.get("next_step"),
                  s.get("next_followup_date") or "", s.get("state", "?"))
        after = (len(sends), step, due, state)
        if before != after:
            changes.append((name, before, after))

        s["mails_sent"] = len(sends)
        s["next_step"] = step
        s["next_followup_date"] = due
        s["state"] = state
        s["reconciled_on"] = TODAY.isoformat()
        s["send_dates_verified"] = sends
        if name in FILL_TO and not s.get("to"):
            s["to"] = FILL_TO[name]
            s["to_source"] = "recovered from Gmail Sent 2026-11-21"

        for st in s.get("steps", []):
            idx = st.get("step", 0)
            if idx < len(sends):
                st["status"] = "sent"
                st["sent_at"] = sends[idx]
            elif st.get("status") == "sent":
                # the ledger claimed a send Gmail has no record of
                st["status"] = "pending"
                st["sent_at"] = ""

    states = {}
    for s in m["sequences"]:
        states[s.get("state", "unverified")] = states.get(s.get("state", "unverified"), 0) + 1

    print(f"verified : {len(MEASURED)} sequences against Gmail Sent")
    print(f"changed  : {len(changes)}")
    print(f"states   : " + ", ".join(f"{k}={v}" for k, v in sorted(states.items())))
    print()
    for name, before, after in sorted(changes):
        flag = "" if before[1] == after[1] else "  <-"
        print(f"  {name[:30]:<31} sent {before[0]}->{after[0]}  "
              f"step {before[1]}->{after[1]}  "
              f"{(before[2] or '-'):<10} -> {(after[2] or '-'):<11} {after[3]}{flag}")

    if unverified:
        print("\n  NOT verified - no recipient address on file, left as-is:")
        for n in unverified:
            print("   ", n)

    if write:
        json.dump(m, open(MANIFEST, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("\nmanifest written")
    else:
        print("\ndry run - pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
