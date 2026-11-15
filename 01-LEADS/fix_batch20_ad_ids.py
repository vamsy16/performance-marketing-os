"""Third-eye corrections for batch 20, 2026-11-15.

Run after the batch-20 commit (04f7058). Re-reading every ad by its own
Library ID showed two of the five IDs recorded for batch 20 belong to other
advertisers, and that Visiontek's ad count was badly undercounted.

  RECORDED                                     ACTUAL
  ----------------------------------------------------------------------
  Meissa Reeve 1691922249204293                AB Solar Power Systems
  Meissa Reeve (no second ID)                  1641050694153685
  Visiontek 2319725685441877 (4 Sep 2026)      mr_koti_00 / Garuda Solar
  Visiontek "4 live ads"                       11 distinct live creatives

Both leads remain valid - the companies, contacts and live-ad status all
checked out - but the evidence attached to them was partly wrong, and a PDF
built on it would have carried someone else's ad IDs.

  python3 fix_batch20_ad_ids.py            # dry run
  python3 fix_batch20_ad_ids.py --write
"""

import csv
import io
import sys

LEADS = 'leads.csv'

MEISSA_OLD = 'Live Meta advertiser: 1 active ad on the "Meissa Reeve" page (Library ID 1691922249204293, started running 14 Nov 2026)'
MEISSA_NEW = ('Live Meta advertiser: 1 active ad on the "Meissa Reeve" page (Library ID 1641050694153685, '
              'started running 14 Nov 2026, ~18 hrs active)')

VISIONTEK_OLD = ('4 active ads on the "Visionteknewenergy" page - Library ID 1133037052650969 '
                 '(12 Nov 2026, 2 ads use this creative), 1138341982459373 (12 Nov 2026, 2 ads use '
                 'this creative), 1449750756945639 (12 Nov 2026, 2 ads use this creative) and '
                 '2319725685441877 (4 Sep 2026) - "Still paying high electricity bills? Switch to '
                 'Visiontek Solar and turn sunlight into savings.')
VISIONTEK_NEW = ('11 distinct live Meta creatives on the "Visionteknewenergy" page, all verified '
                 'active on 2026-11-15 and all started 12 Nov 2026 except one on 6 Nov 2026, with '
                 'Meta grouping each ("2 ads use this creative and text") so the real ad count is '
                 'higher than the number of distinct IDs - "Still paying high electricity bills? '
                 'Switch to Visiontek Solar and turn sunlight into savings.')


def fix(rows):
    changed = []
    for r in rows:
        name, snip = r[0], r[5]
        if name == 'Meissa Reeve':
            assert MEISSA_OLD in snip, 'Meissa snippet no longer carries the wrong ID'
            r[5] = snip.replace(MEISSA_OLD, MEISSA_NEW)
            changed.append(name)
        elif name == 'Visiontek Solar Energy':
            assert VISIONTEK_OLD in snip, 'Visiontek snippet no longer carries the wrong IDs'
            r[5] = snip.replace(VISIONTEK_OLD, VISIONTEK_NEW)
            changed.append(name)
    return changed


def main():
    write = '--write' in sys.argv
    raw = open(LEADS, 'rb').read()
    assert raw.endswith(b'\r\n'), 'leads.csv must end with CRLF'
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8'))))
    header, body = rows[0], rows[1:]
    changed = fix(body)
    print('corrected snippets:', changed or 'NONE')
    if write and changed:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(body)
        open(LEADS, 'w', encoding='utf-8', newline='').write(buf.getvalue())
        assert open(LEADS, 'rb').read().endswith(b'\r\n')
        print('written: %d rows' % len(body))
    elif not changed:
        print('nothing to do - already corrected')


if __name__ == '__main__':
    main()
