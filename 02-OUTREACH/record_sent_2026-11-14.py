#!/usr/bin/env python3
"""Record the 31 emails the owner sent on 2026-11-14 into the manifest.

Every message is matched to its sequence by Gmail thread_id and to the exact
step by the body's opening text, then written through sequence.py's own
mark_sent() so the derived columns (mails_sent, next_step,
next_followup_date, per-step due_date) are recomputed by the canonical code
rather than by hand.

Run from the repo root:
    python3 02-OUTREACH/record_sent_2026-11-14.py            # dry run
    python3 02-OUTREACH/record_sent_2026-11-14.py --write    # apply
"""
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "02-OUTREACH"))
import sequence  # noqa: E402  (the canonical manifest engine)

SENT_ON = "2026-11-14"

# (time IST, company, to, message_id, thread_id, body opening) - read from
# Gmail with `in:sent newer_than:2d older_than:1d`.
SENT = [
    ("14:06", "Milestone Solarcom Private Limited",
     "milestonesolarcomsales@gmail.com", "1a1d932fcc0fd49e",
     "1a1c50f925f30304",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what "
     "Milestone Solar is doing right now."),
    ("13:38", "Surya Renewable Energies", "info@suryarenewable.com",
     "1a1d9195a688b855", "1a1c50f92c8f4ee8",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what Surya "
     "Renewable Energies is doing right now."),
    ("13:27", "Nature Power Solar", "info@naturepowersolar.com",
     "1a1d90f498667554", "1a1c50f9358e5419",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what "
     "Nature Power Solar is doing right now."),
    ("13:12", "SunWorks Energy Private Limited", "gosolar@sunworks.in",
     "1a1d9018ca2c9d65", "1a1c50f93d9989f5",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what "
     "SunWorks Energy is doing right now."),
    ("12:50", "Zenith Energy Services Private Limited",
     "zenith@zenithenergy.com", "1a1d8ed68844061e", "1a1c50f94fa693c8",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what "
     "Zenith Energy is doing right now."),
    ("12:36", "Four Solar", "contact@foursolar.com", "1a1d8e097a74289e",
     "1a1c5ad3cec9972d",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what Four "
     "Solar is doing right now."),
    ("12:24", "Origian Power", "origian.ei@gmail.com", "1a1d8d59b5fee349",
     "1a1c5ad3dbe4f48b",
     "Hi, I spend my week reading the public ad-transparency records for the "
     "Telangana solar market, and I put together a short report on what "
     "Origian Power is doing right now."),
    ("12:11", "Green Carbon Hub", "info@greencarbonhub.com",
     "1a1d8c9b468278df", "1a1c5ad3e5cea499",
     "Hi, I specialise in helping solar companies in Hyderabad get more "
     "installation enquiries, and I put together a full audit of what Green "
     "Carbon Hub is doing right now"),
    ("11:58", "Sri Balaji Solar Energies", "sbse4444@gmail.com",
     "1a1d8bdcc0789b0e", "1a1c5ad438ab5bdd",
     "Hi, I specialise in helping solar companies in Hyderabad get more "
     "installation enquiries, and I put together a full audit of what Sri "
     "Balaji Solar Energies is doing right now"),
    ("11:46", "Arcedo Systems", "info@arcedo.net", "1a1d8b2d0331a57d",
     "1a163e5661ececcb",
     "Hi, I have reached out a couple of times about the ad report for Arcedo "
     "Systems with no response, so I will assume the timing is not right and "
     "close the loop."),
    ("11:33", "Bhanu PV Solar", "info@bhanupvsolar.in", "1a1d8a6eadecede8",
     "1a166d20de09bd9f",
     "Hi, I have reached out a couple of times about the ad report for Bhanu "
     "PV Solar with no response, so I will assume the timing is not right and "
     "close the loop."),
    ("11:21", "Freyr Energy", "info@freyrenergy.com", "1a1d89bec8e50d72",
     "1a166d20b4fc0c5d",
     "Hi, I have reached out a couple of times about the ad report for Freyr "
     "Energy with no response, so I will assume the timing is not right and "
     "close the loop."),
    ("11:07", "Dakshin Solar Power Systems", "dakshinsolar@gmail.com",
     "1a1d88f1c60023bc", "1a166b20e9febcaf",
     "Hi, I have reached out a couple of times about the ad report for "
     "Dakshin Solar Power Systems with no response, so I will assume the "
     "timing is not right and close the loop."),
    ("10:54", "Arkahub", "care@arkahub.in", "1a1d88335ccf495c",
     "1a163e590a0600f9",
     "Hi, I have reached out a couple of times about the ad report for Arkahub "
     "with no response, so I will assume the timing is not right and close "
     "the loop."),
    ("10:41", "Krisol Solar", "sales@krisolsolar.com", "1a1d8774fae6bc96",
     "1a166b0f94c4086c",
     "Hi, I have reached out a couple of times about the ad report for Krisol "
     "Solar with no response, so I will assume the timing is not right and "
     "close the loop."),
    ("10:26", "Hydromo", "info@hydromo.in", "1a1d8699303039cb",
     "1a166b3641cd2487",
     "Hi, I have reached out a couple of times about the ad report for Hydromo "
     "with no response, so I will assume the timing is not right and close "
     "the loop."),
    ("10:15", "3S Solutions", "praveen@3ssol.in", "1a1d85f805713103",
     "1a166b32ae127c61",
     "Hi, I have reached out a couple of times about the ad report for 3S "
     "Solutions with no response, so I will assume the timing is not right "
     "and close the loop."),
    ("10:03", "Lotus Industries", "lotusindustries95@gmail.com",
     "1a1d85485d0909df", "1a1b96e50a8f2457",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("09:51", "MrSolar", "info@mrsolar.in", "1a1d84986f4a991b",
     "1a163e53b42765d9",
     "Hi, I have reached out a couple of times about the ad report for MrSolar "
     "with no response, so I will assume the timing is not right and close "
     "the loop."),
    ("09:38", "Rayzon Solar", "contact@rayzonenergies.com",
     "1a1d83da12243680", "1a16c5b42b8b0477",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("09:24", "VajraSimha Industries", "info@vajrasimhaindustries.com",
     "1a1d830ce163f093", "1a166d20a867560a",
     "Hi, I have reached out a couple of times about the ad report for "
     "VajraSimha Industries with no response, so I will assume the timing is "
     "not right and close the loop."),
    ("09:11", "Sunova Green Energy", "sunovagreenenergy@gmail.com",
     "1a1d824e8739562a", "1a16c5ada8854291",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("08:57", "Lumisun Solar", "service.info@lumisunsolar.com",
     "1a1d818170fae2e2", "1a1b96e59632d7c1",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("08:49", "SolarSquare Energy", "welisten@solarsquare.in",
     "1a1d810c5d506557", "1a16c5b20d3ee424",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("08:33", "PMP Solar Power", "sreepooji27@gmail.com", "1a1d8021ff931cd9",
     "1a166b1353d6dd55",
     "Hi, I have reached out a couple of times about the ad report for PMP "
     "Solar Power with no response, so I will assume the timing is not right "
     "and close the loop."),
    ("08:21", "Wisda Energy", "connect@wisda.in", "1a1d7f7230633008",
     "1a16c5afd49e13ca",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("08:08", "Vanguard Energy", "info@vanguardenergysystems.com",
     "1a1d7eb3af92208d", "1a166d20c6b73541",
     "Hi, I have reached out a couple of times about the ad report for "
     "Vanguard Energy with no response, so I will assume the timing is not "
     "right and close the loop."),
    ("07:50", "SunX Solar and Renewable Solutions",
     "nitish@sunxsolarsolutions.in", "1a1d7dac1c49c777",
     "1a1c312cd345bd63",
     "Hi, Following up on the live-ad report I sent for SunX Solar and "
     "Renewable Solutions. The Diwali ad is still live"),
    ("07:33", "Aadithya Solar Energies", "info@aadithyasolarenergies.com",
     "1a1d7cb31d919575", "1a1c31262722f32b",
     "Hi, Following up on the live-ad report I sent for Aadithya Solar "
     "Energies. The ad is still live"),
    ("07:21", "Varna Solar Pvt. Ltd.", "info@varnasolar.com",
     "1a1d7c033a1a1daf", "1a1b96e5281d2907",
     "Hi, One thing I keep seeing in the Hyderabad solar market: the "
     "installers who are winning right now are not the ones with the biggest "
     "ad budget"),
    ("07:09", "The Arka Solar Power", "info@arkasolarpower.com",
     "1a1d7b5c18eb50c0", "1a1c3126393dd49f",
     "Hi, Following up on the live-ad report I sent for The Arka Solar Power. "
     "The ad is still live"),
]

_ENT = {"&#39;": "'", "&amp;": "&", "&quot;": '"',
        "&lt;": "<", "&gt;": ">", "&#x27;": "'"}


def _norm(text):
    text = re.sub(r"<[^>]+>", " ", text)
    for k, v in _ENT.items():
        text = text.replace(k, v)
    return re.sub(r"\s+", " ", text).strip()


def main():
    write = "--write" in sys.argv
    manifest = sequence.load_manifest()
    by_thread = {}
    for seq in manifest["sequences"]:
        by_thread.setdefault(seq["thread_id"], []).append(seq)

    print("=" * 96)
    print("RECORDING SENDS OF %s - %d messages" % (SENT_ON, len(SENT)))
    print("=" * 96)
    applied, problems = 0, []
    for tm, company, to, mid, tid, opening in SENT:
        cands = by_thread.get(tid, [])
        if len(cands) != 1:
            problems.append((company, "thread matched %d sequences" % len(cands)))
            continue
        seq = cands[0]
        if seq["company"] != company:
            problems.append((company, "thread maps to %r" % seq["company"]))
            continue
        needle = _norm(opening)
        hits = [st for st in seq["steps"]
                if _norm(st["body"]).startswith(needle[:90])]
        if len(hits) != 1:
            problems.append((company, "opening matched %d steps" % len(hits)))
            continue
        step = hits[0]
        before = (step["status"], seq.get("mails_sent"),
                  seq.get("next_step"), seq.get("next_followup_date"))
        sequence.mark_sent(seq, step["step"], tid, mid, SENT_ON)
        applied += 1
        print("  %s  %-38s step %s (%-8s) %-7s -> sent   "
              "next_step %-4s next_followup %s"
              % (tm, company[:38], step["step"], step["kind"], before[0],
                 seq["next_step"], seq["next_followup_date"] or "-"))

    # Recompute every sequence so nothing is left stale.
    for seq in manifest["sequences"]:
        sequence.refresh_due_dates(seq)

    print("-" * 96)
    print("applied %d / %d" % (applied, len(SENT)))
    for p in problems:
        print("  PROBLEM:", p)

    tally = {}
    for seq in manifest["sequences"]:
        for st in seq["steps"]:
            tally[st["status"]] = tally.get(st["status"], 0) + 1
    print("manifest: %d sequences, steps %s"
          % (len(manifest["sequences"]), tally))
    due = sequence.due_followups(manifest, datetime.date(2026, 11, 15))
    print("follow-ups due as of 2026-11-15: %d" % len(due))

    if problems:
        print("\nNOT WRITTEN - resolve the problems above first.")
        return 1
    if not write:
        print("\nDRY RUN - nothing written. Re-run with --write to apply.")
        return 0
    sequence.save_manifest(manifest)
    # sequence.save_manifest() writes no trailing newline; the committed file
    # has always ended with one, so keep the repo convention.
    path = sequence.MANIFEST_FILE
    with io.open(path, "a", encoding="utf-8") as f:
        f.write("\n")
    print("\nwritten to %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
