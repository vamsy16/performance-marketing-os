#!/usr/bin/env python3
"""Fill in the Gmail draft identifiers for the two batch-20 step-0 drafts.

The sequences were appended as `pending` step-0 steps by
build_batch20_outreach.py; this script promotes each to `draft`, records the
draft/message/thread ids plus the creation date exactly as the batch-17 and
batch-18 sequences are recorded, and stamps the same ids onto the reviewable
.txt copies in 02-OUTREACH/generated_emails/.

Run from the repo root:
    python3 02-OUTREACH/finalize_batch20_drafts.py

The ids below were read back with gmail.get_draft after creation: recipient,
subject, body length and PDF attachment all verified, and the attachment was
downloaded and compared byte-for-byte with the file in the workspace.
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
READ_ON = "2026-11-15"


def slug(name):
    return "".join(c if c.isalnum() else "_" for c in name)[:48].strip("_")


# Verified against Gmail on 2026-11-15 (draft created 06:04 -0600 / 12:05 UTC).
DRAFTS = {
    "Meissa Reeve": {
        "draft_id": "r-373894025108968495",
        "message_id": "1a1df1889ec81e2d",
        "thread_id": "1a1df1889ec81e2d",
        "attachment": "audit_Meissa_Reeve.pdf",
        "attachment_bytes": 27788,
    },
    "Visiontek Solar Energy": {
        "draft_id": "r-121616867487234761",
        "message_id": "1a1df18c74328897",
        "thread_id": "1a1df18c74328897",
        "attachment": "audit_Visiontek_Solar_Energy.pdf",
        "attachment_bytes": 31109,
    },
}


def stamp_txt(name, d):
    path = os.path.join(OUTDIR, "batch20_email_%s.txt" % slug(name))
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
        "Attachment: %s (%d bytes, verified byte-identical to the workspace "
        "copy)\n"
        % (READ_ON, CREATED, d["draft_id"], d["attachment"],
           d["attachment_bytes"]), 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    print("  ok stamped %s" % os.path.basename(path))


def main():
    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    seqs = man["sequences"]
    by_name = {s["company"]: s for s in seqs}

    changed = 0
    for name, d in DRAFTS.items():
        seq = by_name.get(name)
        if seq is None:
            print("  ! no sequence for %r" % name)
            continue
        step = seq["steps"][0]
        if step["status"] != "pending":
            print("  ! %s step-0 status is %r, expected 'pending'"
                  % (name, step["status"]))
            continue
        if step["step"] != 0:
            print("  ! %s first step is %r, expected 0" % (name, step["step"]))
            continue
        step["status"] = "draft"
        step["draft_id"] = d["draft_id"]
        step["message_id"] = d["message_id"]
        step["thread_id"] = d["thread_id"]
        step["draft_created_at"] = CREATED
        changed += 1
        print("  ok %s -> %s" % (name, d["draft_id"]))
        stamp_txt(name, d)

    if changed:
        with io.open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(man, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("manifest: %d sequences, %d step-0 drafts recorded"
              % (len(seqs), changed))
    else:
        print("nothing to change")

    # Re-derive the due dates so next_step / next_followup_date are consistent
    # with a step-0 that now exists as a draft but has not been sent.
    from sequence import refresh_columns
    for name in DRAFTS:
        seq = by_name.get(name)
        if seq:
            refresh_columns(seq)
    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
