#!/usr/bin/env python3
"""
Unit tests for the threaded follow-up sequence engine.

Run:  python tests_sequence.py     (stdlib unittest, no extra dependency)
"""

import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sequence as S

LEAD = {"name": "Ksquare Energy", "city": "Hyderabad",
        "email": "info@ksquareenergy.com", "website": "https://ksquareenergy.com"}
AUDIT = {"score": {"score": 12, "issues": ["No Meta Pixel installed"]}}


def fresh_manifest():
    m = {"version": 1, "sequences": []}
    seq = S.upsert_sequence(m, LEAD, AUDIT, "Quick question", "Hi, body")
    return m, seq


class TestSubjects(unittest.TestCase):
    def test_re_subject_single_prefix(self):
        self.assertEqual(S.re_subject("Hello"), "Re: Hello")
        self.assertEqual(S.re_subject("Re: Hello"), "Re: Hello")
        self.assertEqual(S.re_subject("RE: re: Hello"), "Re: Hello")


class TestBuildSteps(unittest.TestCase):
    def test_four_steps_threaded(self):
        steps = S.build_steps(LEAD, AUDIT, "Quick question", "body")
        self.assertEqual(len(steps), 4)
        self.assertEqual(steps[0]["kind"], "initial")
        self.assertEqual(steps[3]["kind"], "breakup")
        for s in steps[1:]:
            self.assertEqual(s["subject"], "Re: Quick question")
            self.assertEqual(s["delay_after_previous_days"], 2)

    def test_bodies_personalized(self):
        steps = S.build_steps(LEAD, AUDIT, "s", "b")
        self.assertIn("Ksquare Energy", steps[1]["body"])
        self.assertIn("No Meta Pixel installed", steps[1]["body"])
        self.assertIn("Hyderabad", steps[2]["body"])


class TestSchedule(unittest.TestCase):
    def test_clock_starts_on_send_not_draft(self):
        m, seq = fresh_manifest()
        S.mark_draft(seq, 0, "draft-1", thread_id="t1", message_id="<m1>")
        # Draft created but NOT sent -> follow-up has no due date yet
        self.assertEqual(S.due_date_for(seq, 1), "")
        self.assertEqual(S.due_followups(m, today=date(2030, 1, 1)), [])

    def test_due_two_days_after_send(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>",
                    on=date(2026, 10, 18))
        self.assertEqual(S.due_date_for(seq, 1), "2026-10-20")
        self.assertEqual(S.due_followups(m, today=date(2026, 10, 19)), [])
        due = S.due_followups(m, today=date(2026, 10, 20))
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["step"], 1)
        self.assertEqual(due[0]["thread_id"], "t1")
        self.assertEqual(due[0]["in_reply_to"], "<m1>")

    def test_chain_each_step_plus_two(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>", on=date(2026, 10, 18))
        S.mark_draft(seq, 1, "draft-2", today=date(2026, 10, 20))  # on due day
        S.mark_sent(seq, 1, on=date(2026, 10, 21))  # sent a day late
        # Next due is +2 from ACTUAL send (21st), not from original plan
        self.assertEqual(S.due_date_for(seq, 2), "2026-10-23")
        self.assertEqual(S.get_step(seq, 1)["thread_id"], "t1")


class TestThreadingGuard(unittest.TestCase):
    def test_followup_draft_refused_before_send(self):
        m, seq = fresh_manifest()
        with self.assertRaises(SystemExit):
            S.mark_draft(seq, 1, "draft-x")

    def test_followup_draft_refused_in_wrong_thread(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>", on=date(2026, 10, 18))
        with self.assertRaises(SystemExit):
            S.mark_draft(seq, 1, "draft-x", thread_id="OTHER-THREAD")

    def test_followup_draft_inherits_thread(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>", on=date(2026, 10, 18))
        step = S.mark_draft(seq, 1, "draft-2", today=date(2026, 10, 20))
        self.assertEqual(step["thread_id"], "t1")
        self.assertEqual(step["status"], "draft")

    def test_no_predrafting_only_one_draft_at_a_time(self):
        # Follow-up drafts must NOT exist before their due day:
        # refused while step 0 is merely a draft...
        m, seq = fresh_manifest()
        S.mark_draft(seq, 0, "draft-1", thread_id="t1", message_id="<m1>")
        with self.assertRaises(SystemExit):
            S.mark_draft(seq, 1, "draft-2", today=date(2026, 10, 18))
        # ...and refused after sending but BEFORE the +2-day due date.
        S.mark_sent(seq, 0, on=date(2026, 10, 18))
        with self.assertRaises(SystemExit):
            S.mark_draft(seq, 1, "draft-2", today=date(2026, 10, 19))
        # On the due day it is allowed (created then, in the thread).
        step = S.mark_draft(seq, 1, "draft-2", today=date(2026, 10, 20))
        self.assertEqual(step["thread_id"], "t1")

    def test_due_action_is_create_draft(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>", on=date(2026, 10, 18))
        due = S.due_followups(m, today=date(2026, 10, 20))
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["action"], "create_draft")
        self.assertEqual(due[0]["thread_id"], "t1")


class TestColumns(unittest.TestCase):
    def test_columns_track_progress(self):
        m, seq = fresh_manifest()
        S.refresh_columns(seq)
        self.assertEqual(seq["mails_sent"], 0)
        self.assertEqual(seq["next_followup_date"], "")
        self.assertEqual(seq["thread_id"], "")

        S.mark_draft(seq, 0, "d1", thread_id="t1", message_id="<m1>")
        S.refresh_columns(seq)
        self.assertEqual(seq["thread_id"], "t1")
        self.assertEqual(seq["mails_sent"], 0)          # draft != sent
        self.assertEqual(seq["next_followup_date"], "")  # clock not started

        S.mark_sent(seq, 0, on=date(2026, 10, 18))
        self.assertEqual(seq["mails_sent"], 1)
        self.assertEqual(seq["next_followup_date"], "2026-10-20")
        self.assertEqual(seq["next_step"], 1)

        S.mark_sent(seq, 1, on=date(2026, 10, 20))
        S.mark_sent(seq, 2, on=date(2026, 10, 22))
        S.mark_sent(seq, 3, on=date(2026, 10, 24))
        self.assertEqual(seq["mails_sent"], 4)
        self.assertEqual(seq["next_followup_date"], "")  # sequence finished
        self.assertIsNone(seq["next_step"])


class TestManifestPreservesState(unittest.TestCase):
    def test_regeneration_keeps_gmail_state(self):
        m, seq = fresh_manifest()
        S.mark_sent(seq, 0, thread_id="t1", message_id="<m1>", on=date(2026, 10, 18))
        # Re-run the generator with a new body: state must survive
        seq2 = S.upsert_sequence(m, LEAD, AUDIT, "Quick question", "new body")
        step0 = S.get_step(seq2, 0)
        self.assertEqual(step0["status"], "sent")
        self.assertEqual(step0["thread_id"], "t1")
        self.assertEqual(step0["body"], "new body")
        self.assertEqual(S.due_date_for(seq2, 1), "2026-10-20")


if __name__ == "__main__":
    unittest.main(verbosity=2)
