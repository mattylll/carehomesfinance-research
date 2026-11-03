"""Reproduce national activity comparisons from the seven supplied aggregate rows.
Python 3 standard library only. Run from any working directory.
"""
from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parent
with (ROOT / 'lending-activity.csv').open(newline='', encoding='utf-8') as f:
    source = list(csv.DictReader(f))
data = {r['Period']: r for r in source}
pairs = [('2023', '2025'), ('H1 2025', 'H1 2026'), ('Jan to Aug 2025', 'Jan to Aug 2026')]
metrics = ['Charges', 'Financing events', 'Borrowing companies']
comparisons = []
for before, after in pairs:
    for metric in metrics:
        a, b = int(data[before][metric]), int(data[after][metric])
        comparisons.append(dict(baseline=before, comparison=after, metric=metric,
                                baseline_count=a, comparison_count=b, change=b-a,
                                percentage_change=round((b/a-1)*100, 6)))
ratios = []
for r in source:
    charges, events = int(r['Charges']), int(r['Financing events'])
    ratios.append(dict(period=r['Period'], charges=charges, financing_events=events,
                      charges_per_event=round(charges/events, 6)))
for name, rows in [('comparisons.csv', comparisons), ('filing-intensity.csv', ratios)]:
    with (ROOT/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
findings = {'source_rows': len(source), 'comparisons': comparisons, 'filing_intensity': ratios,
            'source_report': 'https://carehomesfinance.co.uk/reports/care-home-finance-2026/',
            'limitations': ['Aggregate recalculation only; original matching and deduplication cannot be independently reproduced from this extract.',
                            'Financing events approximate facilities; no loan amounts, pricing, leverage or borrower demand are observed.',
                            'Annual, H1 and January-August windows overlap and must not be added.']}
(ROOT/'findings.json').write_text(json.dumps(findings,indent=2)+'\n',encoding='utf-8')
print(f'Reproduced {len(comparisons)} comparisons and {len(ratios)} filing-intensity ratios from {len(source)} source rows.')
