#!/usr/bin/env python3
"""
Known-leads registry — the duplicate guard for every discovery run.

Every sweep (discover_leads.py, batch builders, manual Meta/Google probes) must
check a candidate against this registry BEFORE auditing or drafting. It answers
one question: "have we already touched this business?"

Sources merged, in order (later sources only add, never replace):
  1. 01-LEADS/leads.csv                     name | city | website | email
  2. 02-OUTREACH/generated_emails/sequence_manifest.json
                                             company | website | email per sequence
  3. 01-LEADS/audit_results/**/*.json       company | website
  4. 01-LEADS/ads_only_results/*.json       company | website
  5. 01-LEADS/batches/*.md                 advertiser names read out of every
                                             past discovery log, so a business
                                             found but never promoted to a CSV
                                             row is still recognised
  6. 01-LEADS/known_leads_extra.json        manual aliases / hard blocks /
                                             recently-vetted rejections

Matching is deliberately conservative, and reports three outcomes:
  "known"  — same business. Always skipped. Fired by a shared registrable
             domain, an identical normalised name, an identical significant
             token set, or two or more shared significant tokens.
  "review" — one distinctive brand word in common but nothing corroborating
             it. Common South Indian trading names collide this way ("Shree
             Adithya Solar" vs "Adithya Solar Tech" are different businesses).
             discover_leads.py skips these too and names them, so a human can
             promote or clear them instead of the sweep silently dropping them.
  None     — genuinely new.

A single generic word in common ("solar", "energy", "power") is NEVER enough.

Usage:
    from known_leads import KnownLeads
    known = KnownLeads()                      # auto-discovers the repo root
    known.verdict(name="Shree Adithya Solar")  # -> ("review", "vetted:live-ads", "Adithya Solar Tech")
    known.is_known(name="SolarSquare Energy")  # -> True

    # CLI, handy before any manual sweep:
    python known_leads.py "Solar Power Experts" amplisolar.in megasolarindia.com
    python known_leads.py --show-vetted        # list the vetoed candidates
"""

import csv
import datetime
import difflib
import json
import os
import re
import sys
from glob import glob

# ---------------------------------------------------------------------------
# normalisation helpers
# ---------------------------------------------------------------------------

# Legal / structural noise that must never decide a match on its own.
LEGAL_TOKENS = {
    "pvt", "private", "ltd", "limited", "llp", "inc", "co", "company",
    "corporation", "corp", "enterprise", "enterprises", "industries",
    "solutions", "solution", "systems", "system", "services", "service",
    "technologies", "technology", "tech", "group", "and", "the", "of",
    "india", "indian", "hyderabad", "telangana", "secunderabad", "new",
}

# Market-generic words. Sharing one of these is not a match.
GENERIC_TOKENS = LEGAL_TOKENS | {
    "solar", "energy", "energies", "power", "renewable", "renewables",
    "green", "sun", "surya", "rooftop", "panel", "panels", "infra",
    "electrical", "electric", "epc", "clean", "smart", "bright", "shree",
    "sri", "mega", "super", "prime", "best", "top", "one", "first",
}

# A token this long counts as a brand word when it is not generic.
DISTINCTIVE_MIN_LEN = 6

# Shortest token that can identify a business on its own, provided no other
# entry in the registry uses it ("kypas", "orbit", "four").
IDENTIFYING_MIN_LEN = 4

# Two tokens at least this similar count as the same trading name, so "Adithya"
# and "Aadithya" both weigh against a single shared token.
# Words that turn up in the name of almost every Indian solar company. They
# can support a match alongside a real brand word, but they can never identify
# a business on their own: "Surya Shakti Solar Energy" and "Shakti On Roof"
# share only "shakti", and they are different companies.
NON_IDENTIFYING = {
    "solar", "power", "energy", "green", "sun", "sunlight", "renewable",
    "renewables", "tech", "technologies", "solutions", "systems", "services",
    "service", "enterprises", "industries", "india", "indian", "new", "mega",
    "shakti", "surya", "the", "and", "pvt", "ltd",
    "limited", "company", "co", "hyderabad", "telangana",
}

TOKEN_SIMILARITY = 0.85


def norm_name(value):
    """'Four Solar Energy Systems Pvt. Ltd.' -> 'four solar energy systems'"""
    if not value:
        return ""
    v = value.lower().replace("&", " and ")
    v = re.sub(r"[^a-z0-9\s]", " ", v)
    return " ".join(t for t in v.split() if t not in LEGAL_TOKENS)


def name_tokens(value):
    """Significant tokens of a name, generics removed."""
    raw = norm_name(value)
    return {t for t in raw.split() if t and t not in GENERIC_TOKENS}


def norm_domain(value):
    """'https://www.ArkaSolar.in/hyderabad' -> 'arkasolar.in' (registrable host)"""
    if not value:
        return ""
    v = str(value).strip().lower()
    v = re.sub(r"^[a-z]+://", "", v)
    v = v.split("/")[0].split("?")[0].split("#")[0]
    v = v.split("@")[-1]
    if v.startswith("www."):
        v = v[4:]
    if not v or "." not in v:
        return ""
    labels = [p for p in v.split(".") if p]
    if len(labels) <= 2:
        return ".".join(labels)
    # fold two-label public suffixes: co.in, com.in, net.in, org.in, gov.in ...
    if labels[-2] in {"co", "com", "net", "org", "gov", "ac", "edu"} and labels[-1] in {
        "in", "uk", "au", "za", "br", "nz", "jp", "za"
    }:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def norm_email(value):
    """'Info@ValcanSolar.com ' -> 'valcansolar.com' (domain half only)."""
    if not value or "@" not in str(value):
        return ""
    return norm_domain(str(value).strip().split("@")[-1])


def repo_root():
    """Walk up from this file until we find the repo root (the dir holding 01-LEADS/)."""
    here = os.path.dirname(os.path.abspath(__file__))
    # This file lives in 01-LEADS/, so its own directory is never the root.
    if os.path.basename(here) == "01-LEADS":
        here = os.path.dirname(here)
    for _ in range(6):
        if os.path.isfile(os.path.join(here, "01-LEADS", "leads.csv")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

class KnownLeads(object):
    """Everything the pipeline has already touched, indexed for fast lookup."""

    DEFAULT_VETO_DAYS = 45

    def __init__(self, root=None, extra_path=None, quiet=True, today=None):
        self.root = root or repo_root()
        self.quiet = quiet
        self.veto_days = self.DEFAULT_VETO_DAYS
        self.today = today or datetime.date.today()
        self.entries = []          # list of dicts: name, domain, email_domain, source
        self.vetted = []           # checked-and-rejected, with an expiry
        self._by_domain = {}
        self._by_name = {}
        self._load_csv()
        self._load_manifest()
        self._load_audit_jsons()
        self._load_batch_logs()
        self._load_extra(extra_path)
        self._index()

    # -- loading ------------------------------------------------------------

    def _log(self, msg):
        if not self.quiet:
            print(msg)

    def _path(self, *parts):
        return os.path.join(self.root, *parts)

    def _add(self, name, website, email, source, city=""):
        domain = norm_domain(website)
        email_domain = norm_email(email)
        clean = (name or "").strip()
        if not clean and not domain:
            return
        entry = {"name": clean, "domain": domain, "email_domain": email_domain,
                 "city": (city or "").strip(), "source": source}
        self.entries.append(entry)
        if domain:
            self._by_domain.setdefault(domain, entry)
        if clean:
            self._by_name.setdefault(norm_name(clean), entry)

    @staticmethod
    def _parse_date(value):
        try:
            return datetime.date.fromisoformat(str(value).strip()[:10])
        except Exception:
            return None

    def _load_csv(self):
        path = self._path("01-LEADS", "leads.csv")
        if not os.path.isfile(path):
            self._log("  [known] no leads.csv at %s" % path)
            return
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                name = (row.get("name") or "").strip()
                if not name:
                    continue
                self._add(name, row.get("website"), row.get("email"),
                          "leads.csv", row.get("city"))
        self._log("  [known] leads.csv -> %d rows" % len(self.entries))

    def _load_manifest(self):
        path = self._path("02-OUTREACH", "generated_emails", "sequence_manifest.json")
        if not os.path.isfile(path):
            return
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:                                # pragma: no cover
            self._log("  [known] manifest unreadable: %s" % exc)
            return
        before = len(self.entries)
        for seq in data.get("sequences", []) or []:
            if not isinstance(seq, dict):
                continue
            email = seq.get("to") or ""
            for step in seq.get("steps", []) or []:
                if isinstance(step, dict) and step.get("to"):
                    email = email or step.get("to")
            self._add(seq.get("company"), seq.get("website"), email,
                      "sequence_manifest", seq.get("city"))
        self._log("  [known] sequence_manifest -> +%d" % (len(self.entries) - before))

    # Batch-log parsing -------------------------------------------------------
    # Prose fragments that get **bolded** in the logs but are not companies.
    EMPHASIS = {
        "none found", "none public", "no website", "not confirmed", "no email",
        "new", "live", "active", "known", "unknown", "review", "duplicate",
        "blocked", "failed", "pass", "skip", "excluded", "no ads", "no phone",
        "none", "same", "different", "unconfirmed", "rejected", "gate",
        "confirmed", "not yet run", "not hyderabad", "not claimed",
        "no new local epc", "hiring", "zero", "split", "own pages",
        "three destinations", "page resolved", "ad card did not render",
        "owner to create and send", "no web presence found",
    }
    # Single words that are never a business name on their own.
    NOISE_WORDS = {
        "zero", "split", "hiring", "run", "none", "only", "yet", "me", "fb",
        "instagram", "whatsapp", "page", "bescom", "bengaluru", "guntur",
        "meerut", "mumbai-hq", "wrapper", "found", "link", "form", "chat",
        "ads", "website", "presence", "owner", "resolved", "attached",
    }

    @classmethod
    def _is_companyish(cls, name):
        name = name.strip().strip("`*# ").rstrip(".").strip()
        words = name.split()
        if not 1 <= len(words) <= 6:
            return False
        if name.lower() in cls.EMPHASIS:
            return False
        if len(name) < 4 or len(name) > 60:
            return False
        for w in words:
            if w.lower() in cls.NOISE_WORDS:
                return False
            if not re.match(r"^[A-Za-z][A-Za-z&.\'-]*$", w):
                return False
        return any(c.isalpha() for c in name)

    @staticmethod
    def _cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def _bold(self, text):
        return [m.group(1).strip() for m in re.finditer(r"\*\*(.+?)\*\*", text)]

    def _names_from_row(self, line):
        """Advertiser names out of one batch-log table row.

        Reads only the leading cells. Later cells carry the emphasis prose
        ("**No website found**", "**Unverifiable**"), which is exactly the
        noise that must not become a registry key.
        """
        cells = self._cells(line)
        if not cells:
            return []
        if re.match(r"^\d+$", cells[0]):
            cells = cells[:2]          # | 4 | **Lead** | evidence | ...
        else:
            cells = cells[:1]          # | **Candidate** | why not rowed | ...
        found = []
        for cell in cells:
            found.extend(self._bold(cell))
            for paren in re.finditer(r"\(([^()]*advertiser[^()]*)\)", cell, re.I):
                for part in re.split(r"[,+/]", paren.group(1)):
                    part = part.strip().strip("`*# ").strip()
                    if part and self._is_companyish(part):
                        found.append(part)
        return [n for n in found if self._is_companyish(n)]

    def _names_from_excluded(self, line):
        """Bold company names inside an 'Excluded because/as ...' sentence."""
        found = [m.group(1).strip()
                 for m in re.finditer(r"\*\*(.+?)\*\*", line)]
        return [n for n in found if self._is_companyish(n)]

    def _load_batch_logs(self):
        pattern = self._path("01-LEADS", "batches", "*.md")
        before = len(self.entries)
        for path in sorted(glob(pattern)):
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except Exception:
                continue
            source = "batch_log:" + os.path.splitext(os.path.basename(path))[0]
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("|"):
                    for name in self._names_from_row(stripped):
                        self._add(name, "", "", source)
                elif re.match(r"excluded\b", stripped, re.I):
                    for name in self._names_from_excluded(stripped):
                        self._add(name, "", "", source)
        self._log("  [known] batch logs -> +%d" % (len(self.entries) - before))

    def _load_audit_jsons(self):
        patterns = [
            self._path("01-LEADS", "audit_results", "*", "*.json"),
            self._path("01-LEADS", "audit_results", "*.json"),
            self._path("01-LEADS", "ads_only_results", "*.json"),
        ]
        before = len(self.entries)
        seen = set()
        for pattern in patterns:
            for path in sorted(glob(pattern)):
                if path in seen:
                    continue
                seen.add(path)
                try:
                    with open(path, encoding="utf-8") as fh:
                        data = json.load(fh)
                except Exception:
                    continue
                if not isinstance(data, dict):
                    continue
                website = data.get("website") or ""
                if isinstance(website, dict):
                    website = website.get("url", "")
                discovery = data.get("discovery") or {}
                if not website and isinstance(discovery, dict):
                    website = discovery.get("destination", "")
                self._add(data.get("company") or data.get("name"), website,
                          data.get("email"), "audit_json")
        self._log("  [known] audit JSONs -> +%d" % (len(self.entries) - before))

    def _load_extra(self, extra_path):
        path = extra_path or self._path("01-LEADS", "known_leads_extra.json")
        if not os.path.isfile(path):
            return
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:                                # pragma: no cover
            self._log("  [known] extra file unreadable: %s" % exc)
            return
        self.veto_days = int(data.get("veto_days", self.DEFAULT_VETO_DAYS))
        before = len(self.entries)
        for item in data.get("known", []) or []:
            if isinstance(item, str):
                self._add(item, "", "", "known_leads_extra")
            elif isinstance(item, dict):
                self._add(item.get("name"), item.get("website"),
                          item.get("email"), "known_leads_extra",
                          item.get("city"))
        self._log("  [known] known_leads_extra -> +%d" % (len(self.entries) - before))

        for item in data.get("vetted", []) or []:
            if not isinstance(item, dict):
                continue
            checked = self._parse_date(item.get("checked"))
            if checked is None:
                self._log("  [known] vetted entry without a date skipped: %r"
                          % item.get("name"))
                continue
            self.vetted.append({
                "name": (item.get("name") or "").strip(),
                "domain": norm_domain(item.get("website")),
                "checked": checked,
                "reason": item.get("reason", ""),
                "gate": item.get("gate", ""),
                "veto_days": int(item.get("veto_days", self.veto_days)),
            })
        self._log("  [known] vetted rejections -> %d" % len(self.vetted))

    def veto_until(self, entry):
        return entry["checked"] + datetime.timedelta(days=entry["veto_days"])

    def active_vetoes(self):
        """Vetted rejections whose cooling-off window has not yet elapsed."""
        return [v for v in self.vetted if self.veto_until(v) >= self.today]

    def expired_vetoes(self):
        return [v for v in self.vetted if self.veto_until(v) < self.today]

    def _index(self):
        """Build the token-frequency index used to judge lone shared words."""
        # token -> set of DISTINCT normalised names carrying it, so the same
        # business appearing in leads.csv, the manifest and an audit JSON
        # still counts once
        names_by_token = {}
        for entry in list(self.entries) + list(self.vetted):
            key = norm_name(entry.get("name", ""))
            if not key:
                continue
            for tok in name_tokens(entry.get("name", "")):
                names_by_token.setdefault(tok, set()).add(key)
        self._token_counts = names_by_token

        # exact normalised full-name index for vetted entries, so a rejected
        # business is still recognised when its name reduces to one token
        self._by_vetted_name = {}
        for entry in self.vetted:
            key = norm_name(entry.get("name", ""))
            if key:
                self._by_vetted_name.setdefault(key, entry)

    def _name_contained(self, norm_a, norm_b):
        """Verdict strength when one normalised name wholly contains the other.

        Catches "four solar" vs "four solar energy systems" - the same business
        under a longer or shorter trading name. Needs two words on the shorter
        side so a lone generic word can never trigger it.

        Returns "known" when the shared part carries a real brand word, and
        "review" when it only carries generic ones. That second case matters:
        "adithya solar tech" normalises to "adithya solar" (tech is generic), so
        it looks like a prefix of "adithya solar works" - but those are
        different businesses, so it must be flagged, never auto-cleared.
        """
        if not norm_a or not norm_b:
            return None
        if len(norm_a.split()) < 2 or len(norm_b.split()) < 2:
            return None
        for a, b in ((norm_a, norm_b), (norm_b, norm_a)):
            # whole-word containment, and the same test with spaces removed so
            # "Kehan Sri Solar" still matches "KehanSri Technologies & Service"
            if (" " + a + " ") not in (" " + b + " ") and \
                    a.replace(" ", "") not in b.replace(" ", ""):
                continue
            strength, _ = self._name_hit(
                {t for t in a.split() if t not in GENERIC_TOKENS},
                {t for t in b.split() if t not in GENERIC_TOKENS})
            return strength
        return None

    def token_freq(self, token):
        """How many distinct businesses carry this token, or one spelled like it."""
        if not token:
            return 0
        counts = getattr(self, "_token_counts", None) or {}
        names = set(counts.get(token, set()))
        for other, other_names in counts.items():
            if other == token:
                continue
            if difflib.SequenceMatcher(None, token, other).ratio() >= TOKEN_SIMILARITY:
                names |= other_names
        return len(names)

    # -- matching -----------------------------------------------------------

    def _name_hit(self, tokens_a, tokens_b):
        """(verdict, weight) for two significant-token sets.

        "known"  -> two or more significant tokens in common
        "review" -> exactly one shared token, and that trading name is common
                    enough in the registry that it cannot identify a business
        """
        if not tokens_a or not tokens_b:
            return None, 0
        shared = tokens_a & tokens_b
        if len(shared) >= 2:
            return "known", len(shared)
        for tok in shared:
            if tok in NON_IDENTIFYING:
                continue          # too common to identify a business alone
            freq = self.token_freq(tok)
            # A brand word nobody else in the registry uses identifies the
            # business; a trading name several businesses share does not.
            if freq == 1 and len(tok) >= IDENTIFYING_MIN_LEN:
                return "known", 1
            if freq >= 2 and len(tok) >= DISTINCTIVE_MIN_LEN:
                return "review", 1
        return None, 0

    def verdict(self, name="", website="", email=""):
        """Return (verdict, source, matched_name).

        verdict is "known" (same business, always skip), "review" (one
        distinctive brand word in common - skip but name it), or None (new).
        """
        domain = norm_domain(website) or norm_domain(email) or norm_email(email)
        tokens = name_tokens(name)
        norm = norm_name(name)

        hit, strength = self._lookup(domain, norm, tokens, self.entries)
        if hit:
            return strength, hit["source"], hit["name"] or name or domain

        if norm:
            entry = self._by_vetted_name.get(norm)
            if entry and self.veto_until(entry) >= self.today:
                return "known", self._veto_label(entry), entry["name"] or name

        for entry in self.active_vetoes():
            if domain and entry["domain"] and entry["domain"] == domain:
                return "known", self._veto_label(entry), entry["name"] or name
            contained = self._name_contained(norm, norm_name(entry["name"]))
            if contained == "known":
                return "known", self._veto_label(entry), entry["name"] or name
            strength, _ = self._name_hit(tokens, name_tokens(entry["name"]))
            if strength:
                return strength, self._veto_label(entry), entry["name"] or name
        return None, None, None

    def match(self, name="", website="", email=""):
        """Back-compatible 2-tuple: (source, matched_name) when known-or-review."""
        verdict, source, matched = self.verdict(name, website, email)
        if verdict:
            return source, matched
        return None, None

    @staticmethod
    def _veto_label(entry):
        return "vetted:%s" % (entry["gate"] or "rejected")

    def _lookup(self, domain, norm, tokens, entries):
        """(entry, strength). Domain and exact-name hits are always "known"."""
        if domain:
            hit = self._by_domain.get(domain)
            if hit:
                return hit, "known"
        if norm:
            hit = self._by_name.get(norm)
            if hit:
                return hit, "known"
        best = None
        for entry in entries:
            if not entry["name"]:
                continue
            strength = self._name_contained(norm, norm_name(entry["name"]))
            if strength == "known":
                return entry, "known"
            if strength == "review" and best is None:
                best = entry
                continue
            strength, _ = self._name_hit(tokens, name_tokens(entry["name"]))
            if strength == "known":
                return entry, "known"
            if strength == "review" and best is None:
                best = entry
        if best is not None:
            return best, "review"
        return None, None

    def is_known(self, name="", website="", email=""):
        return self.match(name, website, email)[0] is not None

    def why(self, name="", website="", email=""):
        """Same as match() — kept as a readable alias."""
        return self.match(name, website, email)

    # -- reporting ----------------------------------------------------------

    def summary(self):
        by_source = {}
        for entry in self.entries:
            by_source[entry["source"]] = by_source.get(entry["source"], 0) + 1
        return {
            "total": len(self.entries),
            "by_source": by_source,
            "unique_domains": len({e["domain"] for e in self.entries if e["domain"]}),
            "unique_names": len({e["name"] for e in self.entries if e["name"]}),
            "vetted_active": len(self.active_vetoes()),
            "vetted_expired": len(self.expired_vetoes()),
        }

    def __len__(self):
        return len(self.entries)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    show_vetted = "--show-vetted" in argv
    if show_vetted:
        argv = [a for a in argv if a != "--show-vetted"]
    if not argv and not show_vetted:
        known = KnownLeads(quiet=False)
        print(json.dumps(known.summary(), indent=2))
        print("\nUsage: python known_leads.py [--show-vetted] <name-or-domain> [more ...]")
        return 0

    known = KnownLeads(quiet=True)
    print("Registry: %s" % json.dumps(known.summary()))
    print("-" * 60)
    if show_vetted:
        print("Active vetoes (re-check after expiry):")
        for v in known.active_vetoes():
            print("  %-38s %-14s until %s  (%s)"
                  % (v["name"] or v["domain"], v["gate"], known.veto_until(v), v["reason"]))
        if known.expired_vetoes():
            print("Expired vetoes (eligible again):")
            for v in known.expired_vetoes():
                print("  %-38s %-14s expired %s"
                      % (v["name"] or v["domain"], v["gate"], known.veto_until(v)))
        print("-" * 60)
    for probe in argv:
        looks_like_domain = "." in probe and " " not in probe
        if looks_like_domain:
            verdict, source, matched = known.verdict(name="", website=probe)
        else:
            verdict, source, matched = known.verdict(name=probe, website="")
        if verdict == "known":
            print("KNOWN   %-38s <- %s (%s)" % (probe, matched, source))
        elif verdict == "review":
            print("REVIEW  %-38s ~ %s (%s)" % (probe, matched, source))
        else:
            print("NEW     %-38s" % probe)
    return 0


if __name__ == "__main__":
    sys.exit(main())
