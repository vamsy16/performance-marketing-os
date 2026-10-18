#!/usr/bin/env python3
"""
Email Sequence Engine — threaded follow-ups, +2 days after the previous email.

Turns the one-shot emails from audit_outreach.py into a tracked sequence:

  Step 0  initial audit email          -> Gmail DRAFT (agent creates it)
  Step 1  follow-up 1                  -> draft pre-created IN STEP 0's THREAD;
                                          SEND due 2 days after step 0 is SENT
  Step 2  follow-up 2                  -> same thread; due +2d after step 1 SENT
  Step 3  breakup email                -> same thread; due +2d after step 2 SENT

Threading rules (enforced here, not left to chance):
  * Every follow-up subject is "Re: <original subject>".
  * A follow-up draft may only be created once the previous step exists in
    Gmail with a recorded thread_id + Message-ID (as a draft or sent) —
    the follow-up is created inside that exact thread (thread_id +
    In-Reply-To + References), NEVER as a new standalone mail.
  * A follow-up's SEND due date is computed from the previous step's SENT
    date (+ FOLLOWUP_DELAY_DAYS), never from the draft-creation date. A
    draft sitting unsent for a week does not start the clock.

State lives in generated_emails/sequence_manifest.json and survives
re-runs of audit_outreach.py (draft/sent state is never clobbered).

Usage:
  python sequence.py build                # (re)build manifest from emails
  python sequence.py status               # show every sequence + state
  python sequence.py due                  # follow-ups due today (ready to draft)
  python sequence.py mark-draft --company "Ksquare Energy" --step 0 \
      --draft-id r-123 --thread-id 18abc --message-id "<...@mail.gmail.com>"
  python sequence.py mark-sent  --company "Ksquare Energy" --step 0 \
      --thread-id 18abc --message-id "<...@mail.gmail.com>" [--date 2026-10-18]
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAILS_DIR = os.path.join(BASE_DIR, "generated_emails")
MANIFEST_FILE = os.path.join(EMAILS_DIR, "sequence_manifest.json")

# Your details — override with env vars SP_NAME / SP_AGENCY / SP_PHONE
YOUR_NAME = os.environ.get("SP_NAME", "Vamsi")
YOUR_AGENCY = os.environ.get("SP_AGENCY", "Smart Pursuit")
YOUR_PHONE = os.environ.get("SP_PHONE", "+91 70950 24220")
YOUR_SIGNATURE = f"{YOUR_NAME}\n{YOUR_AGENCY}\n{YOUR_PHONE}"

# Days between one email being SENT and the next follow-up becoming due.
FOLLOWUP_DELAY_DAYS = int(os.environ.get("SP_FOLLOWUP_DELAY_DAYS", "2"))

MAX_STEP = 3  # 0 = initial, 1..3 = follow-ups (3 = breakup). Never more.


# ---------------------------------------------------------------------------
# Follow-up bodies (personalized from the lead + audit)
# ---------------------------------------------------------------------------

def re_subject(subject):
    """Thread subject: exactly one 'Re: ' prefix."""
    s = (subject or "").strip()
    while s.lower().startswith("re:"):
        s = s[3:].strip()
    return f"Re: {s}"


def followup_body(step, lead, audit):
    """Body for follow-up `step` (1..3). Each adds new value, per templates."""
    name = lead.get("name", "there")
    city = lead.get("city", "")
    issues = (audit.get("score", {}) or {}).get("issues", []) or []
    top_issue = issues[0] if issues else "a couple of quick wins on your website"

    if step == 1:
        return f"""Hi,

Just bumping this up your inbox — I ran a quick audit of {name}'s online presence and the biggest thing I found was: {top_issue}

I've attached the full report to my first email. Happy to walk you through it on a 10-minute call if useful — or just keep the report, no strings attached.

Best,
{YOUR_SIGNATURE}
"""
    if step == 2:
        return f"""Hi,

One more thing about the {city} solar market: searches for rooftop solar in {city} keep growing, but very few local installers are set up to actually capture that demand — most are missing basic tracking, so they can't even tell which enquiries come from where.

That's a fixable gap, and it's exactly what I help solar companies with.

If lead flow ever becomes a priority, I'd love to help {name}.

Best,
{YOUR_SIGNATURE}
"""
    # step 3 — breakup
    return f"""Hi,

I've reached out a couple of times about helping {name} get more leads through Google — no response, so I'll assume the timing isn't right and close the loop.

If that changes (or you ever want a second opinion on your marketing), my door is open.

Wishing you a strong quarter.

Best,
{YOUR_SIGNATURE}
"""


def build_steps(lead, audit, initial_subject, initial_body):
    """The full 4-step sequence for one lead (bodies + subjects, no state)."""
    steps = [{
        "step": 0, "kind": "initial",
        "subject": initial_subject, "body": initial_body,
        "delay_after_previous_days": 0,
    }]
    for n in range(1, MAX_STEP + 1):
        steps.append({
            "step": n,
            "kind": "breakup" if n == MAX_STEP else "followup",
            "subject": re_subject(initial_subject),
            "body": followup_body(n, lead, audit),
            "delay_after_previous_days": FOLLOWUP_DELAY_DAYS,
        })
    return steps


# ---------------------------------------------------------------------------
# Manifest (state) handling
# ---------------------------------------------------------------------------

def _blank_state():
    return {"status": "pending", "draft_id": "", "message_id": "",
            "thread_id": "", "draft_created_at": "", "sent_at": "",
            "due_date": ""}


def load_manifest(path=MANIFEST_FILE):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "followup_delay_days": FOLLOWUP_DELAY_DAYS,
            "sequences": []}


def save_manifest(manifest, path=MANIFEST_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    manifest["followup_delay_days"] = FOLLOWUP_DELAY_DAYS
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return path


def upsert_sequence(manifest, lead, audit, initial_subject, initial_body):
    """Add/refresh a lead's sequence. Existing Gmail state is preserved:
    re-running the generator updates bodies/subjects but never wipes
    draft_id / thread_id / sent_at already recorded."""
    company = lead.get("name", "")
    fresh_steps = build_steps(lead, audit, initial_subject, initial_body)

    seq = next((s for s in manifest["sequences"]
                if s["company"].lower() == company.lower()), None)
    if seq is None:
        seq = {"company": company, "to": lead.get("email", ""),
               "city": lead.get("city", ""), "website": lead.get("website", ""),
               "thread_subject": initial_subject, "steps": []}
        manifest["sequences"].append(seq)

    seq["to"] = lead.get("email", "") or seq.get("to", "")
    old = {s["step"]: s for s in seq.get("steps", [])}
    merged = []
    for fs in fresh_steps:
        prev = old.get(fs["step"], {})
        state = _blank_state()
        for k in state:
            if prev.get(k):
                state[k] = prev[k]
        merged.append({**fs, **state})
    seq["steps"] = merged
    return seq


def find_sequence(manifest, company):
    seq = next((s for s in manifest["sequences"]
                if company.lower() in s["company"].lower()), None)
    if seq is None:
        raise SystemExit(f"No sequence found for '{company}'")
    return seq


def get_step(seq, step_no):
    step = next((s for s in seq["steps"] if s["step"] == step_no), None)
    if step is None:
        raise SystemExit(f"{seq['company']}: no step {step_no}")
    return step


def due_date_for(seq, step_no):
    """Due date of a follow-up = previous step's SENT date + delay.
    Returns '' while the previous step is unsent (clock hasn't started)."""
    if step_no == 0:
        return ""
    prev = get_step(seq, step_no - 1)
    if not prev.get("sent_at"):
        return ""
    sent = date.fromisoformat(prev["sent_at"])
    return (sent + timedelta(days=FOLLOWUP_DELAY_DAYS)).isoformat()


def refresh_due_dates(seq):
    for s in seq["steps"]:
        s["due_date"] = due_date_for(seq, s["step"])
    return seq


def mark_draft(seq, step_no, draft_id, thread_id="", message_id="",
               on=None):
    """Record that a Gmail draft exists for a step.

    Follow-ups (step >= 1) are REFUSED unless the previous step is SENT
    with a recorded thread_id + message_id — that is what guarantees the
    follow-up lands in the same thread instead of as a new mail."""
    step = get_step(seq, step_no)
    if step_no >= 1:
        prev = get_step(seq, step_no - 1)
        if prev.get("status") not in ("draft", "sent") \
                or not prev.get("thread_id") or not prev.get("message_id"):
            raise SystemExit(
                f"REFUSED: step {step_no} for {seq['company']} cannot be "
                f"drafted yet — step {step_no - 1} has no recorded Gmail "
                "draft/sent message with thread_id/message_id. Follow-ups "
                "must be created inside the original thread, never as a "
                "new mail.")
        if thread_id and thread_id != prev["thread_id"]:
            raise SystemExit(
                f"REFUSED: follow-up thread_id {thread_id} does not match "
                f"the original thread {prev['thread_id']}.")
        thread_id = prev["thread_id"]
    step["draft_id"] = draft_id
    step["thread_id"] = thread_id or step.get("thread_id", "")
    step["message_id"] = message_id or step.get("message_id", "")
    step["draft_created_at"] = (on or date.today()).isoformat() \
        if not isinstance(on, str) else on
    step["status"] = "draft"
    refresh_due_dates(seq)
    return step


def mark_sent(seq, step_no, thread_id="", message_id="", on=None):
    """Record that a step was SENT (from Gmail). Starts the +2-day clock
    for the next follow-up."""
    step = get_step(seq, step_no)
    sent_on = on if isinstance(on, str) else (on or date.today()).isoformat()
    step["status"] = "sent"
    step["sent_at"] = sent_on
    if thread_id:
        step["thread_id"] = thread_id
    if message_id:
        step["message_id"] = message_id
    if step_no >= 1:
        prev = get_step(seq, step_no - 1)
        step["thread_id"] = prev.get("thread_id", step["thread_id"])
    refresh_due_dates(seq)
    return step


def due_followups(manifest, today=None):
    """Follow-ups due to SEND today: previous step was sent >= delay days
    ago. `action` is 'send_draft' when the threaded draft already exists
    (the normal case — drafts are pre-created), else 'create_draft'."""
    today = today or date.today()
    due = []
    for seq in manifest["sequences"]:
        refresh_due_dates(seq)
        for s in seq["steps"]:
            if s["step"] == 0 or s["status"] == "sent":
                continue
            if s.get("due_date") and date.fromisoformat(s["due_date"]) <= today:
                due.append({"company": seq["company"], "to": seq.get("to", ""),
                            "step": s["step"], "kind": s["kind"],
                            "subject": s["subject"],
                            "due_date": s["due_date"],
                            "action": "send_draft" if s["status"] == "draft"
                                      else "create_draft",
                            "draft_id": s.get("draft_id", ""),
                            "thread_id": get_step(seq, s["step"] - 1)["thread_id"],
                            "in_reply_to": get_step(seq, s["step"] - 1)["message_id"]})
    return due


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _find(manifest, company):
    seq = find_sequence(manifest, company)
    refresh_due_dates(seq)
    return seq


def main():
    p = argparse.ArgumentParser(description="Threaded follow-up sequence engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show all sequences and their state")
    sub.add_parser("due", help="List follow-ups due today")

    d = sub.add_parser("mark-draft", help="Record a Gmail draft for a step")
    d.add_argument("--company", required=True)
    d.add_argument("--step", type=int, required=True)
    d.add_argument("--draft-id", required=True)
    d.add_argument("--thread-id", default="")
    d.add_argument("--message-id", default="")

    s = sub.add_parser("mark-sent", help="Record that a step was sent")
    s.add_argument("--company", required=True)
    s.add_argument("--step", type=int, required=True)
    s.add_argument("--thread-id", default="")
    s.add_argument("--message-id", default="")
    s.add_argument("--date", default="", help="Sent date YYYY-MM-DD (default today)")

    args = p.parse_args()
    manifest = load_manifest()

    if args.cmd == "status":
        if not manifest["sequences"]:
            print("No sequences yet. Run: python audit_outreach.py --export")
            return
        for seq in manifest["sequences"]:
            refresh_due_dates(seq)
            print(f"\n{seq['company']}  <{seq.get('to') or 'NO EMAIL'}>")
            for s in seq["steps"]:
                extra = ""
                if s["step"] and s.get("due_date"):
                    extra = f" due {s['due_date']}"
                if s.get("sent_at"):
                    extra += f" sent {s['sent_at']}"
                thread = f" thread {s['thread_id'][:12]}…" if s.get("thread_id") else ""
                print(f"  step {s['step']} ({s['kind']:8}) {s['status']:8}"
                      f"{extra}{thread}")
        save_manifest(manifest)

    elif args.cmd == "due":
        due = due_followups(manifest)
        save_manifest(manifest)
        if not due:
            print("No follow-ups due today.")
        for d_ in due:
            print(f"DUE {d_['due_date']}  {d_['company']}  step {d_['step']} "
                  f"({d_['kind']})  action={d_['action']}  "
                  f"draft={d_['draft_id'] or '-'}  thread={d_['thread_id']}  "
                  f"in_reply_to={d_['in_reply_to']}")

    elif args.cmd == "mark-draft":
        seq = _find(manifest, args.company)
        step = mark_draft(seq, args.step, args.draft_id,
                          args.thread_id, args.message_id)
        save_manifest(manifest)
        print(f"Recorded draft for {seq['company']} step {args.step}: "
              f"{step['draft_id']} (thread {step['thread_id'] or '—'})")

    elif args.cmd == "mark-sent":
        seq = _find(manifest, args.company)
        mark_sent(seq, args.step, args.thread_id, args.message_id,
                  args.date or None)
        save_manifest(manifest)
        nxt = due_date_for(seq, args.step + 1) if args.step < MAX_STEP else ""
        print(f"Marked {seq['company']} step {args.step} as sent."
              + (f" Next follow-up due: {nxt}" if nxt else ""))


if __name__ == "__main__":
    main()
