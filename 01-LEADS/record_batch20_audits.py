"""Record the batch-20 full-audit results in leads.csv, 2026-11-15.

Both leads now have a Ksquare-shaped full audit built from page text read live
on 2026-11-15. Scores come from calculate_audit_score() over measured values
only - every field the sandbox could not measure is null and is neither
penalised nor counted as a win.

  Meissa Reeve        23/100, 11 issues, 7 wins
  Visiontek           10/100,  8 issues, 9 wins

Visiontek's 10 is its own arithmetic (no contact form on the homepage +8, no
visible testimonials +2) and is not copied from any other report.

  python3 record_batch20_audits.py            # dry run
  python3 record_batch20_audits.py --write
"""

import csv
import io
import json
import sys

LEADS = 'leads.csv'

RESULTS = {
    'Meissa Reeve': ('audit_Meissa_Reeve.json', 'audited'),
    'Visiontek Solar Energy': ('audit_Visiontek_Solar_Energy.json', 'audited'),
}


def main():
    write = '--write' in sys.argv
    raw = open(LEADS, 'rb').read()
    assert raw.endswith(b'\r\n'), 'leads.csv must end with CRLF'
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8'))))
    header, body = rows[0], rows[1:]
    i_score = header.index('audit_score')
    i_issues = header.index('audit_issues_count')
    i_status = header.index('status')

    changed = []
    for r in body:
        want = RESULTS.get(r[0])
        if not want:
            continue
        fname, status = want
        d = json.load(open('audit_results/' + fname, encoding='utf-8'))
        sc = d['score']['score']
        n = d['score']['issue_count']
        assert sc is not None, '%s has no score - refusing to record one' % r[0]
        assert n, '%s has no issue count' % r[0]
        if (r[i_score], r[i_issues], r[i_status]) == (str(sc), str(n), status):
            print('  already recorded:', r[0])
            continue
        r[i_score], r[i_issues], r[i_status] = str(sc), str(n), status
        changed.append((r[0], sc, n))

    if write and changed:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(body)
        open(LEADS, 'w', encoding='utf-8', newline='').write(buf.getvalue())
        assert open(LEADS, 'rb').read().endswith(b'\r\n')
        print('written: %d rows' % len(body))
    for c, s, n in changed:
        print('  %s -> %s/100, %d issues, audited' % (c, s, n))
    if not changed:
        print('  nothing to change')


if __name__ == '__main__':
    main()
