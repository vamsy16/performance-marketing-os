#!/usr/bin/env python3
"""Fill in the Gmail draft identifiers for the three batch-18 step-0 drafts.

The sequences were appended as `pending` step-0 steps by
build_batch18_outreach.py; this script promotes each to `draft`, records the
draft/message/thread ids plus the creation date exactly as the batch-17
sequences are recorded, and stamps the same ids onto the reviewable .txt
copies in 02-OUTREACH/generated_emails/.

Run from the repo root:
    python3 02-OUTREACH/finalize_batch18_drafts.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "02-OUTREACH", "generated_emails",
                        "sequence_manifest.json")
OUTDIR = os.path.join(ROOT, "02-OUTREACH", "generated_emails")
CREATED = "2026-11-15"
READ_ON = "2026-11-14"

# Slug used by build_batch18_outreach.write_txt_files().
def slug(name):
    return "".join(c if c.isalnum() else "_" for c in name)[:48].strip("_")

# Draft ids returned by gmail.create_draft, verified with gmail.get_draft:
# recipient, subject and PDF attachment all read back.
DRAFTS = {
    "KehanSri Technologies & Service Pvt Ltd": {
        "draft_id": "r6289258085426613897",
        "message_id": "1a1de774e78e3b40",
        "thread_id": "1a1de774e78e3b40",
        "attachment": "audit_KehanSri_Technologies_Service_Pvt_Ltd.pdf",
    },
    "Hysun Solar Pvt. Ltd.": {
        "draft_id": "r-1445496077411248187",
        "message_id": "1a1de77a6317b6b5",
        "thread_id": "1a1de77a6317b6b5",
        "attachment": "audit_Hysun_Solar_Pvt_Ltd_.pdf",
    },
    "V1 Solar Solutions": {
        "draft_id": "r2242087638525005418",
        "message_id": "1a1de77a5c88d096",
        "thread_id": "1a1de77a5c88d096",
        "attachment": "audit_V1_Solar_Solutions.pdf",
    },
}


def stamp_txt(name, draft_id):
    """Add the draft-created / draft-id lines to the reviewable .txt copy."""
    path = os.path.join(OUTDIR, "batch18_email_%s.txt" % slug(name))
    if not os.path.exists(path):
        print("  ! missing %s" % path)
        return
    text = io.open(path, encoding="utf-8").read()
    if "Draft ID:" in text:
        print("  = %s already stamped" % os.path.basename(path))
        return
    text = text.replace(
        "Read on: %s\n" % READ_ON,
        "Read on: %s\nDraft created: %s\n"
        "Draft ID: %s (status draft, nothing sent)\n"
        % (READ_ON, CREATED, draft_id), 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    print("  ok stamped %s" % os.path.basename(path))


def main():
    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    seqs = man["sequences"]
    by_name = {s["company"]: s for s in seqs}
    for name, d in DRAFTS.items():
        seq = by_name.get(name)
        if seq is None:
            print("  ! no sequence for %r" % name)
            continue
        step = seq["steps"][0]
        if step["status"] != "pending":
            print("  ! %s step-0 status is %r, expected 'pending'"
                  % (name, step["status"]))
        step["status"] = "draft"
        step["draft_id"] = d["draft_id"]
        step["message_id"] = d["message_id"]
        step["thread_id"] = d["thread_id"]
        step["draft_created_at"] = CREATED
        step["sent_at"] = ""
        step["due_date"] = ""
        seq["thread_id"] = d["thread_id"]
        seq["mails_sent"] = 0
        seq["next_followup_date"] = ""
        seq["next_step"] = 1
        print("  ok %-40s %s (attached %s)"
              % (name, d["draft_id"], d["attachment"]))
        stamp_txt(name, d["draft_id"])
    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Re-read and report the totals the manifest is judged by.
    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    seqs = man["sequences"]
    tally = {"sent": 0, "draft": 0, "pending": 0}
    for s in seqs:
        for st in s["steps"]:
            tally[st["status"]] += 1
    print("\nmanifest: %d sequences, steps %s" % (len(seqs), tally))
    for name in DRAFTS:
        s = by_name[name]
        print("  %-40s %s  mails_sent=%s next_step=%s"
              % (name, s["steps"][0]["status"], s["mails_sent"],
                 s["next_step"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
