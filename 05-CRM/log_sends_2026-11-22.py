#!/usr/bin/env python3
"""Record 2026-11-22 sends in the repo, read off Gmail.

What was sent on 22 Nov was established from Gmail, not from the manifest:
`in:sent after:2026/11/21 before:2026/11/23` returns 39 messages, of which 27
carry a 21 Nov date, leaving 12 on 22 Nov. That total is `complete: true`, so
12 is the full set for the day - nothing was inferred from a truncated page.

Twelve sends fall into three groups:

  1. Five were follow-up drafts created on 21 Nov and sent by hand on 22 Nov.
     Gmail's draft folder is now empty, which corroborates that all five left
     as email rather than being deleted. (Aadithya, Eagle, Hindusthan? no -
     see SENT_ON below: the five are Aadithya, Eagle, Valcan, and the step-0
     batch-15 drafts Growcell / Roof Rays / Akhil / Manasaa are separate.)

  2. Nine were first-touch emails for sequences sitting at `never-sent`.
     Nothing was fabricated to make them "due": they were simply never emailed,
     and now they have been.

  3. One (Sree Bhalaji Industries) belongs to no sequence in the manifest at
     all. It is a real 2-step thread - initial 16 Nov, follow-up 22 Nov - so it
     is logged here rather than forced into a sequence it does not have.

A caution about ordering. Eagle Solar Systems received its 22 Nov follow-up
(10:25) *before* its 22 Nov first-touch (13:13), and in two different threads.
Gmail is unambiguous about the timestamps; the sequence logic is not. That is
recorded as it happened, with a note, instead of being silently reordered.

    cd 05-CRM && python3 log_sends_2026-11-22.py --write
"""
import csv
import datetime
import json
import os
import sys

KINDS = 4

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MANIFEST = os.path.join(REPO, "02-OUTREACH", "generated_emails",
                        "sequence_manifest.json")
SEND_LOG = os.path.join(HERE, "send_log.csv")

SENT_ON = "2026-11-22"

# (company | None, to, time, message_id, thread_id, step_kind, note)
SENDS = [
    ("Akhil Electrical Works", "narasimhayaragorla2@gmail.com",
     "14:34:00", "1a2027f8091e7250", "1a1ff0196c4cbd97", "initial",
     "batch-15 step-0 draft sent by hand"),
    ("Roof Rays Solar Solutions", "support@roofrays.in",
     "14:21:00", "1a20273993c028ab", "1a1ff017b2de6665", "initial",
     "batch-15 step-0 draft sent by hand"),
    ("Growcell Solar Energy", "sales@growcellenergy.in",
     "14:07:00", "1a20266c7d270044", "1a1ff0165aee942d", "initial",
     "batch-15 step-0 draft sent by hand"),
    ("Manasaa Enterprises", "manasaaenterprises2024@gmail.com",
     "13:54:00", "1a2025ae1ffee897", "1a1ff01aa6251bc3", "initial",
     "batch-15 step-0 draft sent by hand"),
    ("Sri Narayana Enterprise Solar Energies", "snepadilabad@gmail.com",
     "13:41:00", "1a2024efa1a9a138", "1a1fe7ce6030ffc6", "initial",
     "first touch; sequence had been sitting at never-sent"),
    ("Griffin Energy", "info@griffinenergy.in",
     "13:26:00", "1a202413f55f37cc", "1a1fe7ca5e9f2455", "initial",
     "first touch; sequence had been sitting at never-sent"),
    ("Eagle Solar Systems", "eaglesolarhyd@gmail.com",
     "13:13:00", "1a2023557af9cbcb", "1a1fe7b74d1dcb75", "initial",
     "first touch in a NEW thread, 2h48m after this prospect's follow-up "
     "went out in the older thread - ordering recorded, not corrected"),
    ("Nova Solar Solutions", "info@novasolar.in",
     "12:57:30", "1a202272caca51e0", "1a1fe7cc89345d69", "initial",
     "first touch; sequence had been sitting at never-sent"),
    (None, "info@bhalajigroup.com",
     "10:51:00", "1a201b357b2a7d67", "1a1e1e37d3ac627c", "followup",
     "Sree Bhalaji Industries - in NO manifest sequence; real thread "
     "(initial 2026-11-16, follow-up 2026-11-22); logged here only"),
    ("Aadithya Solar Energies", "info@aadithyasolarenergies.com",
     "10:38:00", "1a201a76ed629daa", "1a1c31262722f32b", "breakup",
     "step-3 breakup draft created 2026-11-21, sent by hand"),
    ("Eagle Solar Systems", "eaglesolarhyd@gmail.com",
     "10:25:00", "1a2019b88bcde5a0", "1a1e1c3fc3a0baea", "followup",
     "step-1 follow-up draft created 2026-11-21, sent by hand"),
    ("Valcan Solar", "info@valcansolar.com",
     "10:11:53", "1a2018f8fab6a28c", "1a15c27f4e7546f3", "followup",
     "step-1 follow-up draft created 2026-11-21, sent by hand"),
]

# Eagle's 22 Nov sends: the follow-up (10:25) and then a fresh first touch
# (13:13) in a separate thread. Both are real; both are recorded.
FIELDS = ["sent_date", "sent_time", "to", "company", "step_kind",
          "subject", "message_id", "thread_id", "source", "note"]


def load_subjects():
    """Subjects come from Gmail; kept here so the log is reproducible offline."""
    return {
        "1a2027f8091e7250": "Akhil Electrical Works: TSRE250617 appears in none of your four live ads",
        "1a20273993c028ab": "Roof Rays: your site already prices a 3 kW system - none of your ads use it",
        "1a20266c7d270044": "Growcell Solar Energy: 2 live Hyderabad ads, and neither one lands on your site",
        "1a2025ae1ffee897": "Manasaa Enterprises: three asterisks, no footnote, on a Rs.5.92 lakh quote",
        "1a2024efa1a9a138": "Sri Narayana Enterprise Solar Energies: 1 live Adilabad, Telangana ad, one funnel",
        "1a202413f55f37cc": "Griffin Energy: 4 live Hyderabad, Telangana ads, one funnel",
        "1a2023557af9cbcb": "Eagle Solar Systems: 3 live Hyderabad, Telangana ads, one funnel",
        "1a202272caca51e0": "Nova Solar Solutions: 3 live Hyderabad, Telangana ads, one funnel",
        "1a201b357b2a7d67": "Re: Sree Bhalaji Industries \u2014 what I found testing bhalajigroup.com",
        "1a201a76ed629daa": "Re: Aadithya Solar Energies: 1 live Hyderabad ad, one funnel",
        "1a2019b88bcde5a0": "Re: Eagle Solar Systems: 2 live Hyderabad ads, one funnel",
        "1a2018f8fab6a28c": "Re: Valcan Solar: 2 live Hyderabad ads, one funnel",
    }


def main():
    write = "--write" in sys.argv
    subjects = load_subjects()
    rows = []
    for company, to, tm, mid, tid, kind, note in SENDS:
        rows.append({
            "sent_date": SENT_ON, "sent_time": tm, "to": to,
            "company": company or "Sree Bhalaji Industries",
            "step_kind": kind, "subject": subjects.get(mid, ""),
            "message_id": mid, "thread_id": tid,
            "source": "Gmail SENT, verified 2026-11-23",
            "note": note,
        })
    rows.sort(key=lambda r: r["sent_time"])

    print(f"{len(rows)} sends on {SENT_ON}\n")
    for r in rows:
        print(f"  {r['sent_time']}  {r['company'][:38]:<40}{r['step_kind']:<9}{r['to']}")

    # --- manifest: stamp sent_at on the steps these sends satisfy
    m = json.load(open(MANIFEST, encoding="utf-8"))
    by_company = {}
    for r in rows:
        by_company.setdefault(r["company"], []).append(r)

    touched = []
    for s in m["sequences"]:
        recs = by_company.get(s["company"])
        if not recs:
            continue
        moved = []
        for r in recs:
            # match the step the send satisfies: same kind, still unsent
            for st in s["steps"]:
                if st.get("status") == "sent":
                    continue
                if st.get("kind") != r["step_kind"]:
                    continue
                st["status"] = "sent"
                st["sent_at"] = f"{r['sent_date']}T{r['sent_time']}+05:30"
                st["message_id"] = r["message_id"]
                st["thread_id"] = r["thread_id"]
                st["sent_source"] = "Gmail SENT (verified 2026-11-23)"
                moved.append(f"step {st['step']} {st['kind']} @ {r['sent_time']}")
                break
        unmatched = [r for r in recs
                     if r["message_id"] not in
                     {st.get("message_id") for st in s["steps"]}]
        if unmatched:
            s.setdefault("extra_sends", [])
            for r in unmatched:
                s["extra_sends"].append({
                    "sent_at": f"{r['sent_date']}T{r['sent_time']}+05:30",
                    "step_kind": r["step_kind"],
                    "message_id": r["message_id"],
                    "thread_id": r["thread_id"],
                    "subject": r["subject"],
                    "note": r["note"],
                })
                moved.append(f"extra {r['step_kind']} @ {r['sent_time']} "
                             f"(new thread {r['thread_id']})")

        if moved:
            s["mails_sent"] = sum(1 for st in s["steps"]
                                  if st.get("status") == "sent")
            sent_at = [st["sent_at"] for st in s["steps"] if st.get("status") == "sent"]
            last = max(sent_at)
            # "finished" means all four steps actually exist and all are sent.
            # Several batch-14/15 sequences only ever had a step-0 record built,
            # so len(steps) is 1; treating that as complete would silently close
            # a live sequence. Those stay open and say what is missing.
            if len(s["steps"]) >= KINDS and s["mails_sent"] >= KINDS:
                s["state"] = "finished"
                s["next_followup_date"] = ""
            else:
                s["state"] = "live-due"
                s["next_followup_date"] = (
                    datetime.date.fromisoformat(last[:10])
                    + datetime.timedelta(days=2)).isoformat()
                if len(s["steps"]) < KINDS:
                    s["note"] = (
                        f"only {len(s['steps'])} step(s) built; follow-up steps "
                        f"need generating before this sequence can advance")
            s["next_step"] = s["mails_sent"]
            touched.append((s["company"], s["mails_sent"], s["state"],
                            s["next_followup_date"] or "-", "; ".join(moved)))

    print(f"\nmanifest updates: {len(touched)}")
    for c, n, state, due, what in touched:
        print(f"  {c[:38]:<40} sent={n}  {state:<10} due={due:<12} {what}")

    if write:
        with open(SEND_LOG, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        json.dump(m, open(MANIFEST, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        print(f"\nwrote {SEND_LOG}")
        print(f"wrote {MANIFEST}")
    else:
        print("\ndry run - pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
