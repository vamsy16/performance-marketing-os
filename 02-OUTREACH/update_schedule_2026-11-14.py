#!/usr/bin/env python3
"""Append the 2026-11-14 send log to the pending-schedule document.

The schedule file is a running log: one section per send date, plus a header
and a "Manifest state" footer that describe the CURRENT position. This script
regenerates only the new section, the header and the footer from the manifest,
so no Message-ID or draft ID is typed by hand.

Run from the repo root:
    python3 02-OUTREACH/update_schedule_2026-11-14.py
"""
import datetime
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "02-OUTREACH"))
import sequence  # noqa: E402

SCHEDULE = os.path.join(ROOT, "02-OUTREACH", "generated_emails",
                        "pending_schedule_2026-11-08.md")
SENT_ON = "2026-11-14"
TODAY = "2026-11-15"

# The same 31 rows record_sent_2026-11-14.py wrote, in send order (IST).
ORDER = [
    ("14:06", "Milestone Solarcom Private Limited", "milestonesolarcomsales@gmail.com"),
    ("13:38", "Surya Renewable Energies", "info@suryarenewable.com"),
    ("13:27", "Nature Power Solar", "info@naturepowersolar.com"),
    ("13:12", "SunWorks Energy Private Limited", "gosolar@sunworks.in"),
    ("12:50", "Zenith Energy Services Private Limited", "zenith@zenithenergy.com"),
    ("12:36", "Four Solar", "contact@foursolar.com"),
    ("12:24", "Origian Power", "origian.ei@gmail.com"),
    ("12:11", "Green Carbon Hub", "info@greencarbonhub.com"),
    ("11:58", "Sri Balaji Solar Energies", "sbse4444@gmail.com"),
    ("11:46", "Arcedo Systems", "info@arcedo.net"),
    ("11:33", "Bhanu PV Solar", "info@bhanupvsolar.in"),
    ("11:21", "Freyr Energy", "info@freyrenergy.com"),
    ("11:07", "Dakshin Solar Power Systems", "dakshinsolar@gmail.com"),
    ("10:54", "Arkahub", "care@arkahub.in"),
    ("10:41", "Krisol Solar", "sales@krisolsolar.com"),
    ("10:26", "Hydromo", "info@hydromo.in"),
    ("10:15", "3S Solutions", "praveen@3ssol.in"),
    ("10:03", "Lotus Industries", "lotusindustries95@gmail.com"),
    ("09:51", "MrSolar", "info@mrsolar.in"),
    ("09:38", "Rayzon Solar", "contact@rayzonenergies.com"),
    ("09:24", "VajraSimha Industries", "info@vajrasimhaindustries.com"),
    ("09:11", "Sunova Green Energy", "sunovagreenenergy@gmail.com"),
    ("08:57", "Lumisun Solar", "service.info@lumisunsolar.com"),
    ("08:49", "SolarSquare Energy", "welisten@solarsquare.in"),
    ("08:33", "PMP Solar Power", "sreepooji27@gmail.com"),
    ("08:21", "Wisda Energy", "connect@wisda.in"),
    ("08:08", "Vanguard Energy", "info@vanguardenergysystems.com"),
    ("07:50", "SunX Solar and Renewable Solutions", "nitish@sunxsolarsolutions.in"),
    ("07:33", "Aadithya Solar Energies", "info@aadithyasolarenergies.com"),
    ("07:21", "Varna Solar Pvt. Ltd.", "info@varnasolar.com"),
    ("07:09", "The Arka Solar Power", "info@arkasolarpower.com"),
]


def sent_step(seq):
    """The step this sequence sent on 2026-11-14, or None."""
    for st in seq["steps"]:
        if st.get("sent_at") == SENT_ON:
            return st
    return None


def all_steps_sent(seq):
    return bool(seq["steps"]) and all(
        st["status"] == "sent" for st in seq["steps"])


def closed_sequences(manifest):
    """Ran to completion: every step sent AND more than one step existed.

    A sequence with only a step-0 email is NOT closed - it simply has no
    follow-up steps behind it, which is a different thing.
    """
    return [s["company"] for s in manifest["sequences"]
            if len(s["steps"]) > 1 and all_steps_sent(s)]


def build_section(manifest):
    lines = []
    lines.append("## Sent %s by the owner (reconciled into the manifest)\n" % SENT_ON)
    lines.append(
        "All **31** outstanding drafts went out on %s, 07:09-14:06 IST: the 9 first\n"
        "contacts drafted on 2026-11-10 (Four Solar, Origian Power, Green Carbon Hub,\n"
        "Sri Balaji, Zenith, SunWorks, Nature Power, Surya Renewable, Milestone) plus\n"
        "the 22 due follow-ups. Every one was reconciled with its real Gmail\n"
        "Message-ID through `sequence.py mark_sent`, so each follow-up clock now runs\n"
        "from the true send date.\n" % SENT_ON)
    lines.append("| Time (IST) | Company | Step | To | Gmail Message-ID | Draft ID sent |")
    lines.append("|---|---|---|---|---|---|")
    for tm, company, to in ORDER:
        seq = sequence.find_sequence(manifest, company)
        st = sent_step(seq)
        if st is None:
            raise SystemExit("no %s send recorded for %s" % (SENT_ON, company))
        lines.append("| %s | %s | %s | %s | `%s` | %s |"
                     % (tm, company, st["step"], to, st["message_id"],
                        "`%s`" % st["draft_id"] if st.get("draft_id") else "—"))
    lines.append("")

    kinds = {}
    for _tm, company, _to in ORDER:
        seq = sequence.find_sequence(manifest, company)
        st = sent_step(seq)
        kinds[st["kind"]] = kinds.get(st["kind"], 0) + 1
    lines.append("By kind: **%d initial · %d followup · %d breakup.**\n"
                 % (kinds.get("initial", 0), kinds.get("followup", 0),
                    kinds.get("breakup", 0)))

    closed = [c for _tm, c, _to in ORDER if c in set(closed_sequences(manifest))]
    lines.append(
        "The %d step-3 emails were **breakups** — the final follow-up in those\n"
        "sequences. Those sequences are now **closed**: %s.\n"
        % (kinds.get("breakup", 0), ", ".join(sorted(closed))))

    nxt = datetime.date.fromisoformat(SENT_ON) + datetime.timedelta(days=2)
    lines.append(
        "Every sequence that still has an unsent follow-up is now due **%s**\n"
        "(previous send + 2 days). The 9 first contacts each start a fresh clock.\n"
        % nxt.isoformat())

    step0_only = [c for _tm, c, _to in ORDER
                  if len(sequence.find_sequence(manifest, c)["steps"]) == 1]
    if step0_only:
        lines.append(
            "\n**Worth knowing:** %d of the first contacts sent that day — %s —\n"
            "have **only a step-0 email in the manifest, no follow-up steps**, so\n"
            "nothing is scheduled behind them. Same for the three batch-18 drafts.\n"
            "See the note at the end of this file.\n"
            % (len(step0_only), ", ".join(sorted(step0_only))))
    lines.append("")
    return "\n".join(lines)


def build_footer(manifest):
    tally = {}
    for seq in manifest["sequences"]:
        for st in seq["steps"]:
            tally[st["status"]] = tally.get(st["status"], 0) + 1
    total = sum(tally.values())
    closed = closed_sequences(manifest)
    step0_only = [s["company"] for s in manifest["sequences"]
                  if len(s["steps"]) == 1]
    due = sequence.due_followups(manifest, datetime.date.fromisoformat(TODAY))

    out = []
    out.append("## Manifest state (as of %s)\n" % TODAY)
    out.append("%d sequences / %d steps — **%d sent · %d draft · %d pending.**\n"
               % (len(manifest["sequences"]), total, tally.get("sent", 0),
                  tally.get("draft", 0), tally.get("pending", 0)))
    out.append("The %d live drafts are the three batch-18 first contacts (KehanSri,\n"
               "Hysun, V1 Solar — created %s, still unsent) plus Valcan Solar's\n"
               "step-1, parked in trash by owner decision.\n"
               % (tally.get("draft", 0), "2026-11-15"))
    out.append("%d sequences are closed (no further step).\n" % len(closed))
    out.append("### Still due as of %s — %d\n" % (TODAY, len(due)))
    out.append("| Company | Step | Kind | Due | Action | Draft |")
    out.append("|---|---|---|---|---|---|")
    for d in due:
        out.append("| %s | %s | %s | %s | %s | %s |"
                   % (d["company"], d["step"], d["kind"], d["due_date"],
                      d["action"], "`%s`" % d["draft_id"] if d["draft_id"] else "—"))
    out.append("")
    out.append("### Sequences with a first contact but no follow-up steps — %d\n"
               % len(step0_only))
    out.append("These leads were emailed once and nothing is scheduled behind them,\n"
               "because no follow-up steps were ever built for their sequences:\n")
    out.append(", ".join("%s" % c for c in sorted(step0_only)) + ".\n")
    out.append("`sequence.py upsert_sequence()` can add steps 1-3 to any of them\n"
               "without touching the sent state — say the word and I will build them.\n")
    return "\n".join(out)


def main():
    manifest = sequence.load_manifest()
    text = io.open(SCHEDULE, encoding="utf-8").read()

    if "## Sent %s by the owner" % SENT_ON in text:
        print("section for %s already present - not duplicating" % SENT_ON)
        return 0

    # 1. refresh the header paragraph that describes the live-draft count
    old_hdr = ("Gmail holds **27 live drafts** — the follow-ups that fell due "
               "2026-11-09 and 2026-11-10,\nall drafted on 2026-11-10 as "
               "threaded `Re:` replies (see \"Drafts created 2026-11-10\" "
               "below).\nValcan Solar's step-1 draft `r-4135467498809954457` "
               "is in **trash** and **parked by owner\ndecision — ignore "
               "it**.\nGmail's scheduled send is UI-only, so pick a time on "
               "each draft.")
    new_hdr = ("Running log of every send, newest section first below. The "
               "current position is in\n\"Manifest state\" at the end.\n\n"
               "Gmail holds **4 live drafts** as of %s: the three batch-18 "
               "first contacts (KehanSri,\nHysun, V1 Solar) created 2026-11-15 "
               "and still unsent, plus Valcan Solar's step-1\n"
               "`r-4135467498809954457`, which is in **trash** and **parked "
               "by owner decision —\nignore it**. Gmail's scheduled send is "
               "UI-only, so pick a time on each draft." % TODAY)
    if old_hdr not in text:
        print("WARNING: header paragraph not found verbatim; leaving it alone")
    else:
        text = text.replace(old_hdr, new_hdr, 1)

    # 2. drop the old footer and rebuild it, then append the new section
    marker = "## Manifest state"
    idx = text.index(marker)
    text = text[:idx].rstrip("\n") + "\n\n"
    text += build_section(manifest)
    text += build_footer(manifest)

    io.open(SCHEDULE, "w", encoding="utf-8", newline="\n").write(text)
    print("updated %s" % os.path.relpath(SCHEDULE, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
