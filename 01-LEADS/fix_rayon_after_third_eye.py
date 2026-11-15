#!/usr/bin/env python3
"""Correct the Ray On Solar Systems row after the third-eye re-verification.

The third-eye pass (re-opening every recorded ad ID on its own, after the
audit) found three problems with this row:

1. Library ID 1107666674962232, the only ad evidence the row carried, does
   not open as an ad. Meta resolves the page to "MRK Associates" and answers
   "Ad isn't in the Ad Library". It was read off a search-result list and is
   misattributed.
2. Library ID 2401086164116585, which a Telugu sweep surfaced next to the
   Ray On card, resolves to "Vyaktigat Vikas", a Hindi computer-books
   advertiser, and returns ~230 unrelated ads. Also misattributed, also read
   off a search list.
3. Library ID 3529873930505195 does open as Ray On Solar Systems (page
   61571060785642, started 18 Sep 2026, "multiple versions"), so the row
   keeps its live-ad basis on exactly one verified ID.

The city field also said Hyderabad while the firm's own site says
Visakhapatnam, Andhra Pradesh.

The row is corrected, not deleted: one verified live ad is enough to keep
the lead, and the firm publishes rayonsolars@gmail.com. The misattributed
IDs are recorded so nobody re-uses them.
"""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(HERE, "leads.csv")

SNIPPET = (
    "Live Meta advertiser: 1 verified active ad on the \"Ray On Solar "
    "Systems\" page (FB page 61571060785642) - Library ID 3529873930505195, "
    "started running 18 Sep 2026, marked by Meta as \"this ad has multiple "
    "versions\", so the real creative count is higher than one. Creative: "
    "\"Cut Electricity Bills with Solar / 3kW Solar Power System Offer / Get "
    "your 3kW solar system at a special price with subsidy and long-term "
    "warranty support\", CTA Get Quote on a generic fb.me link, headline "
    "image pointing at instagram.com/ray_on_solar_systems_. The ads drive no "
    "traffic to the website. THIRD-EYE CORRECTION 2026-11-15, made after the "
    "audit: this row previously cited Library ID 1107666674962232 as its only "
    "live ad. Opening that ID on its own returns \"Ad isn't in the Ad "
    "Library\" and resolves the page to \"MRK Associates\", a different "
    "advertiser - the ID had been read off a search-result list, which is "
    "exactly the misattribution this pass exists to catch. A second ID, "
    "2401086164116585, surfaced next to the Ray On card in a Telugu sweep "
    "and resolves to \"Vyaktigat Vikas\", a Hindi computer-books "
    "advertiser; it is discarded. Both are recorded here so they are never "
    "reused. Contacts: rayonsolars@gmail.com, +91 8500976346 / +91 9703774654, "
    "published on the firm's own site. The firm's own site states it is "
    "located in Visakhapatnam, Andhra Pradesh - \"Ray On Solar Systems, "
    "located in Visakhapatnam, specializes in customized rooftop solar "
    "solutions\" - and serves homes and businesses there. The city field of "
    "this row said Hyderabad, which contradicted the snippet and the state "
    "audit; corrected on 2026-11-15 to reflect the firm's real base. The "
    "lead is retained because it advertises into Telangana and publishes a "
    "real email address, but it is an Andhra Pradesh firm and is counted "
    "outside Telangana by the state guard."
)


def main():
    with io.open(LEADS, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    hits = 0
    for r in rows:
        if r["name"] == "Ray On Solar Systems":
            r["city"] = ("Visakhapatnam, Andhra Pradesh "
                         "(advertising into Hyderabad)")
            r["snippet"] = SNIPPET
            r["phone"] = "+91 8500976346 / +91 9703774654"
            hits += 1
    if hits != 1:
        raise SystemExit("expected exactly one Ray On row, found %d" % hits)

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    with io.open(LEADS, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    print("corrected Ray On Solar Systems row")


if __name__ == "__main__":
    main()
