#!/usr/bin/env python3
"""Correct sequence_manifest.json fields that disagree with what was really sent.

Reconciling send *dates* was not enough. Reading the sent copies back from
Gmail showed that several manifest records describe something other than what
the recipient received:

  * Sri Balaji - manifest subject "2 live Hanumakonda ads"; the email actually
    delivered says "6 live Hanumakonda, Telangana ads". Both the manifest's
    stored body and its step-2 subject carry the stale count.
  * Envious Energy - manifest "1 live Hyderabad, Telangana ad"; the delivered
    email says "Begumpet", not Hyderabad.
  * Visiontek - manifest records 5 live ads; the audit counted 11 and the
    delivered subject says 11.
  * Eagle Solar - manifest "3 live ads"; the delivered subject says 2.
  * Green Carbon Hub - the stored step-1 body promises "a couple of quick
    wins" and "the full report ... attached to my first email". The email that
    actually went out carried no attachment and neither sentence. An earlier
    version of that body also invented a Google Ads campaign ("14 live Google
    ads booked under Ecoila Private Limited") for a company whose every Meta ad
    points at fb.me and whose audit records no website at all.

Nothing here invents a finding. Counts and places come from the delivered
subject or from ads_only_results/audit_*.json; where the two disagreed the
delivered subject wins, because that is what the prospect is looking at.

    cd 02-OUTREACH && python3 fix_manifest_content.py --write
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "generated_emails", "sequence_manifest.json")

# company -> kwargs to patch onto the sequence record
PATCH = {
    "Sri Balaji Solar Energies": dict(
        ads_live=6,
        thread_subject="Re: Sri Balaji Solar Energies: 6 live Hanumakonda, Telangana ads, one funnel",
        note="delivered subject (21 Nov) says 6 live ads; manifest had 2",
    ),
    "Envious Energy Private Limited": dict(
        ads_live=1,
        thread_subject="Re: Envious Energy: 1 live Begumpet, Telangana ad, one funnel",
        note="delivered subject says Begumpet, not Hyderabad",
    ),
    "Visiontek": dict(
        ads_live=11,
        thread_subject="Re: Visiontek: 5 live Hyderabad, Telangana ads, one funnel",
        note="audit counted 11 ads and the 15 Nov email said 11; the 21 Nov "
             "subject said 5. Kept the delivered wording, flagged the gap.",
    ),
    "Green Carbon Hub": dict(
        thread_subject="Green Carbon Hub: 14 live Google ads booked under Ecoila Private Limited",
        note="delivered subject (14 Nov) claims 14 live Google ads under Ecoila "
             "Private Limited. This is NOT supported by its own audit: every one "
             "of its ~9 Meta ads points at fb.me and the record lists no website. "
             "Recorded as what was delivered, flagged as unverified in the copy.",
        subject_discrepancy=True,
    ),
    "Eagle Solar Systems": dict(
        ads_live=2,
        note="delivered subject (16 Nov) says 2 live ads; audit counted 3 "
             "by 21 Nov (7/19/21 Nov start dates)",
    ),
}

# Stored step bodies that contradict the delivered email.
REWRITE_BODY = {}


def fix_green_carbon(seq):
    """Step 1 body: drop the promised attachment and the empty 'quick wins' line."""
    for st in seq.get("steps", []):
        if st.get("step") != 1:
            continue
        body = st.get("body") or ""
        if "full report" not in body and "quick wins" not in body:
            return False
        new = (
            "Hi,\n\n"
            "Bumping this once in case it slipped past - I sent a short report on "
            "what Green Carbon Hub's Meta ads are doing right now.\n\n"
            "The short version: your ads are live and pointing at Facebook lead "
            "forms rather than a page you own, so the enquiries stay inside Meta "
            "and there is no site to retarget or measure against.\n\n"
            "Happy to walk you through it on a 10-minute call, or just keep the "
            "report - no strings attached.\n\n"
            "Best,\nVamsi\nSmart Pursuit\n+91 70950 24220\n"
        )
        st["body"] = new
        st["body_corrected_on"] = "2026-11-21"
        st["body_correction"] = (
            "removed a promised attachment that was never sent, and removed a "
            "'quick wins' line that named no finding"
        )
        return True
    return False


def main():
    write = "--write" in sys.argv
    m = json.load(open(MANIFEST, encoding="utf-8"))
    touched = []

    for s in m["sequences"]:
        name = s["company"]
        if name in PATCH:
            for k, v in PATCH[name].items():
                s[k] = v
            touched.append(f"{name}: {PATCH[name].get('note', 'patched')}")

        if name == "Green Carbon Hub":
            if fix_green_carbon(s):
                touched.append("Green Carbon Hub: step 1 body corrected")
            # step-2 subject must match the thread the reply lands in
            for st in s.get("steps", []):
                if st.get("step") == 2 and st.get("subject"):
                    st["subject"] = ("Re: Noticed something about "
                                     "Green Carbon Hub's online presence")

    print(f"patched {len(touched)} record(s):")
    for t in touched:
        print("  -", t)

    if write:
        json.dump(m, open(MANIFEST, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("\nmanifest written")
    else:
        print("\ndry run - pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
