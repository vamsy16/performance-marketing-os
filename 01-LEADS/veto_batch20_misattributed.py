"""Veto the one genuinely-new advertiser the corrected batch-20 feed surfaces.

Re-running the corrected feed shows exactly one advertiser that is not already
in the pipeline: mr_koti_00. Opening its ad by its own Library ID
(2319725685441877) shows it is an ad for Garuda Solar Energy Solutions, 3rd
Floor Amarravati Rd, Guntur, Andhra Pradesh - outside the Hyderabad/Telangana
segment this pipeline works, so it is vetoed on segment rather than rowed.

The other mis-attributed ID (1691922249204293) belongs to AB Solar Power
Systems, which is already a rowed and audited lead (leads.csv, CI score 7/100)
- the duplicate guard catches it correctly, which is the point of re-running
the feed after correcting it.

  python3 veto_batch20_misattributed.py            # dry run
  python3 veto_batch20_misattributed.py --write
"""

import io
import json
import sys

EXTRA = 'known_leads_extra.json'

VETO = ("mr_koti_00", "https://www.instagram.com/_u/mr_koti_00", "Guntur, Andhra Pradesh",
        "2026-11-15", "segment",
        "Live Meta advertiser (Library ID 2319725685441877, started 4 Sep 2026, "
        "page instagram.com/_u/mr_koti_00) but the ad sells Garuda Solar Energy "
        "Solutions, 3rd Floor Amarravati Rd, Guntur, Andhra Pradesh, +91 8886946169, "
        "with Govt subsidies for AP and Telangana. Guntur is outside the "
        "Hyderabad/Telangana segment this pipeline works. This ID was recorded as a "
        "Visiontek Solar Energy ad in batch 20 and was corrected on 2026-11-15.")


def main():
    write = '--write' in sys.argv
    raw = io.open(EXTRA, encoding='utf-8').read()
    d = json.loads(raw)
    name, site, city, checked, gate, reason = VETO
    if any(v.get('name') == name for v in d['vetted']):
        print('already vetoed:', name)
        return
    if write:
        d['vetted'].append({'name': name, 'website': site, 'city': city,
                            'checked': checked, 'gate': gate, 'reason': reason})
        # indent=2 is the file's established convention - keep it, or every
        # re-run rewrites the whole file and buries the real change
        io.open(EXTRA, 'w', encoding='utf-8', newline='').write(
            json.dumps(d, indent=2, ensure_ascii=False) + '\n')
        print('vetoed %s on %s -> known %d / vetted %d'
              % (name, gate, len(d['known']), len(d['vetted'])))
    else:
        print('dry run: would veto %s on %s' % (name, gate))


if __name__ == '__main__':
    main()
