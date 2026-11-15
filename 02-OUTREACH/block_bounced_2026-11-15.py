#!/usr/bin/env python3
"""Block the two sequences whose step-0 email hard-bounced on 2026-11-11.

Owner decision 2026-11-15: mark them bounced and stop their follow-up
clocks, rather than leaving step 1 reading as overdue forever. The
addresses still need correcting before either sequence can resume.

Run from the repo root:
    python3 02-OUTREACH/block_bounced_2026-11-15.py            # dry run
    python3 02-OUTREACH/block_bounced_2026-11-15.py --write    # apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "02-OUTREACH"))
import sequence  # noqa: E402

ON = "2026-11-15"

# Reasons quote Gmail's own bounce notice, read on 2026-11-15.
BLOCKED = {
    "Hindusthan Solar Energy Enterprise":
        "info@hindusthansolarenergy.com hard-bounced 2026-11-11 - Gmail "
        "\"Delivery Status Notification (Failure)\": the recipient server "
        "did not accept our requests. Delayed 11-08/09/10, then failed, so "
        "the step-0 email sent 2026-11-08 never landed. A corrected address "
        "is needed before this sequence can resume.",
    "Kypas Solar Power Pvt Ltd":
        "Info@kypassolar.in hard-bounced 2026-11-11 - Gmail \"Delivery "
        "Status Notification (Failure)\": the recipient server did not "
        "accept our requests. Delayed 11-08/09/10, then failed, so the "
        "step-0 email sent 2026-11-08 never landed. A corrected address is "
        "needed before this sequence can resume.",
}


def main():
    write = "--write" in sys.argv
    manifest = sequence.load_manifest()
    print("=" * 78)
    print("BLOCKING SEQUENCES WHOSE STEP-0 EMAIL HARD-BOUNCED 2026-11-11")
    print("=" * 78)
    for company, reason in BLOCKED.items():
        seq = sequence.find_sequence(manifest, company)
        before = (seq.get("blocked"), seq.get("next_step"),
                  seq.get("next_followup_date"), seq.get("mails_sent"))
        print("\n%s" % company)
        print("   to=%s" % seq["to"])
        print("   before: blocked=%s next_step=%s next_followup=%s "
              "mails_sent=%s" % before)
        if before[0]:
            print("   already blocked - leaving as is")
            continue
        sequence.mark_blocked(seq, reason, ON)
        print("   after:  blocked=%s next_step=%s next_followup=%s "
              "mails_sent=%s"
              % (seq["blocked"], seq["next_step"],
                 seq["next_followup_date"] or "-", seq["mails_sent"]))
        print("   due dates now: %s"
              % [s["due_date"] or "-" for s in seq["steps"]])

    # Recompute everything so no stale column survives.
    for seq in manifest["sequences"]:
        sequence.refresh_due_dates(seq)

    due = sequence.due_followups(manifest, sequence.date(2026, 11, 15))
    print("\n" + "-" * 78)
    print("follow-ups due as of 2026-11-15: %d" % len(due))
    for d in due:
        print("   %-40s step %s due %s" % (d["company"][:40], d["step"],
                                           d["due_date"]))
    blocked = [s["company"] for s in manifest["sequences"] if s.get("blocked")]
    print("blocked sequences: %d -> %s" % (len(blocked), ", ".join(blocked)))

    if not write:
        print("\nDRY RUN - nothing written. Re-run with --write to apply.")
        return 0
    sequence.save_manifest(manifest)
    path = sequence.MANIFEST_FILE
    with io.open(path, "a", encoding="utf-8") as f:
        f.write("\n")
    print("\nwritten to %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
