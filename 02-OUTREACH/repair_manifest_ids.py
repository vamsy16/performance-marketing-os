#!/usr/bin/env python3
"""Repair the sequence manifest so follow-up dues are trustworthy.

Three defects, all in data written earlier this session rather than in the
sequence engine:

  1. THREAD ID STORED AS MESSAGE ID. Several step records carry the Gmail
     thread id in `message_id`. A follow-up needs the previous email's real
     Message-ID for In-Reply-To/References; passing a thread id makes a draft
     that does not thread.

  2. MISSING MESSAGE ID. The first-touch sends of 21/22 Nov logged `sent_at`
     but no `message_id`, so nothing downstream could thread to them.

  3. A SEND DOUBLE-APPLIED. `log_sends_2026-11-22.py` was not idempotent: it
     re-matched a send to the next step of the same kind, so Valcan and Eagle
     each showed one message id against two steps, and Eagle's `extra_sends`
     gained a duplicate. (Eagle's extra entry is legitimate - a second first
     touch in a new thread - but it was written twice.)

Every id below was read from Gmail during this session, either from a SENT
listing or from the draft that was later sent. Nothing is invented, and a
company+step that is not listed is left alone.

    cd 02-OUTREACH && python3 repair_manifest_ids.py           # dry run
    cd 02-OUTREACH && python3 repair_manifest_ids.py --write
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "generated_emails", "sequence_manifest.json")

# (company, step) -> (message_id, thread_id) as read from Gmail.
FIX = {
    # --- thread id was sitting in message_id
    ("3S Solutions", 0): ("1a1676254bbd9ba9", "1a166b32ae127c61"),
    ("Bhanu PV Solar", 0): ("1a1679cec83508ee", "1a166d20de09bd9f"),
    ("Dakshin Solar Power Systems", 0): ("1a16754997ab24ff", "1a166b20e9febcaf"),
    ("Freyr Energy", 0): ("1a167834b01f51f0", "1a166d20b4fc0c5d"),
    ("Hydromo", 0): ("1a1676c673b3089a", "1a166b3641cd2487"),
    ("Krisol Solar", 0): ("1a1673ea09a1cb54", "1a166b0f94c4086c"),
    ("Lotus Industries", 0): ("1a1b9f23234fd4b8", "1a1b96e50a8f2457"),
    ("Lumisun Solar", 0): ("1a1b9d7a481e9334", "1a1b96e59632d7c1"),
    ("PMP Solar Power", 0): ("1a16748b275d4983", "1a166b1353d6dd55"),
    ("VajraSimha Industries", 0): ("1a1677762a283ec5", "1a166d20a867560a"),
    ("Vanguard Energy", 0): ("1a16791f19b305d0", "1a166d20c6b73541"),
    ("Varna Solar Pvt. Ltd.", 0): ("1a1b9e560b904f8f", "1a1b96e5281d2907"),
    ("Aadithya Solar Energies", 0): ("1a1c3f20264d7da3", "1a1c31262722f32b"),
    ("Eagle Solar Systems", 0): ("1a1e44920320500d", "1a1e1c3fc3a0baea"),
    # --- sent but no message id recorded
    ("Four Solar", 1): ("1a1fcec3053e3446", "1a1c5ad3cec9972d"),
    ("Green Carbon Hub", 2): ("1a1fd014052a6806", "1a1c5ad3e5cea499"),
    ("Origian Power", 1): ("1a1fcf72d3787e8f", "1a1c5ad3dbe4f48b"),
    ("Sri Balaji Solar Energies", 1): ("1a1fda9b4ea9fdf2", "1a1fca2e3f161d3e"),
    ("Kakatiya Energies", 1): ("1a1fd9a248534774", "1a1fd14db01575b1"),
    ("Visiontek", 1): ("1a1fd8b7f53a61bf", "1a1fd14f51c3e422"),
    ("Laxmi Narayana Solar", 0): ("1a1fd5db66596508", "1a1fc79deabd85f3"),
    ("Envious Energy Private Limited", 0): ("1a1fdbdd982564d5", "1a1fca2c7a12f81e"),
    ("Hindusthan Solar Energy Enterprise", 0): ("1a1ba0aea736f565", "1a1b96e4e23fedab"),
    ("Kypas Solar Power Pvt Ltd", 0): ("1a1b9ffef3225525", "1a1b96e4fc02c231"),
    # --- step 3 breakup sent 22 Nov (was a draft on 21 Nov)
    ("Aadithya Solar Energies", 3): ("1a201a76ed629daa", "1a1c31262722f32b"),
}

# A message id may only be marked sent against one step per sequence.
KEEP_FIRST = {"Valcan Solar": "1a2018f8fab6a28c",
              "Eagle Solar Systems": "1a2019b88bcde5a0"}


def main():
    write = "--write" in sys.argv
    m = json.load(open(MANIFEST, encoding="utf-8"))
    log = []

    # --- sent_at must be a bare YYYY-MM-DD. sequence.py runs
    # date.fromisoformat() on it, so a full timestamp crashes `due` outright.
    healed = 0
    for s in m["sequences"]:
        for st in s["steps"]:
            v = st.get("sent_at") or ""
            if len(v) > 10 and "T" in v:
                st["sent_at"] = v[:10]
                st.setdefault("sent_at_time", v[11:])
                healed += 1
    if healed:
        log.append(f"normalised {healed} sent_at timestamp(s) -> date")

    for s in m["sequences"]:
        for st in s["steps"]:
            key = (s["company"], st["step"])
            if key not in FIX:
                continue
            mid, tid = FIX[key]
            if st.get("status") != "sent" and not st.get("sent_at"):
                continue  # do not attach an id to a step that did not send
            if st.get("message_id") != mid:
                log.append(f"{s['company'][:32]:<34} step {st['step']} "
                           f"message_id {st.get('message_id') or '(none)'} -> {mid}")
                st["message_id"] = mid
            if st.get("thread_id") != tid:
                st["thread_id"] = tid
            s["thread_id"] = tid

    # --- one message id, one step
    for s in m["sequences"]:
        dup = KEEP_FIRST.get(s["company"])
        if not dup:
            continue
        seen = False
        for st in sorted(s["steps"], key=lambda x: x["step"]):
            if st.get("message_id") == dup and st.get("status") == "sent":
                if seen:
                    log.append(f"{s['company'][:32]:<34} step {st['step']} "
                               f"cleared duplicate send ({dup})")
                    st["status"] = "pending"
                    st["sent_at"] = ""
                    st["message_id"] = ""
                seen = True

    # --- de-duplicate extra_sends, keep the richer record
    for s in m["sequences"]:
        ex = s.get("extra_sends") or []
        best = {}
        for e in ex:
            k = e.get("message_id")
            cur = best.get(k)
            if cur is None or (len(e) > len(cur)):
                best[k] = e
        if len(best) != len(ex):
            log.append(f"{s['company'][:32]:<34} extra_sends {len(ex)} -> {len(best)}")
            s["extra_sends"] = list(best.values())

    # --- recompute mails_sent / next_step from the steps themselves
    for s in m["sequences"]:
        n = sum(1 for st in s["steps"] if st.get("status") == "sent")
        if s.get("mails_sent") != n:
            log.append(f"{s['company'][:32]:<34} mails_sent "
                       f"{s.get('mails_sent')} -> {n}")
            s["mails_sent"] = n
        if s.get("next_step") is None:
            s["next_step"] = n

    print(f"{len(log)} correction(s):")
    for line in log:
        print("  ", line)

    if write:
        json.dump(m, open(MANIFEST, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        print("\nmanifest written")
    else:
        print("\ndry run - pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
