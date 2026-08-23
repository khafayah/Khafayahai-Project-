# Hakim Group Payroll Reconciliation Pack

Python/openpyxl build for three monthly Excel deliverables, generated from six
iTrent exports (NPV Comparison, Payment Breakdown x2, New Starters, Leavers,
Structure report).

## Outputs

1. **Hakim Group - Payroll Reconciliation Tool.xlsx** - reusable, formula-driven.
   Paste new monthly exports into the six raw tabs and Control Sheet /
   Summary / Exceptions / Zero Hours / Drilldown recalculate automatically.
   All comparison logic lives in the hidden `_Helpers` engine sheet.
2. **Hakim Group - Investigation List.xlsx** - prioritised review list with
   gold "Investigated by" / "Outcome" columns for the team working the queue.
3. **Hakim Group - SLT Pack.xlsx** - GDPR-safe leadership pack (payroll
   numbers only, no employee names): dashboard, full employee list with a
   reason for every person, and an expenses breakdown.

Hakim Group branding throughout: deep purple `#3D315D` headers/titles, hot
pink `#DF5694` accents/review highlighting, gold `#FFC000` input cells, grey
helper cells, mid purple `#66609B` secondary tabs, Aptos font.

## Files

- `mock_data.py` - synthetic but realistic iTrent-style source data (60
  employees) covering every scenario the logic must handle: stable pay,
  tolerance breaches with a real cause, starters, leavers, zero-hours-only
  staff, zero-hours-plus-permanent staff, paired payroll-record transfers,
  and a no-pay/no-leaver case.
- `reference_calc.py` - an independent, pure-Python re-implementation of the
  reconciliation logic (tolerance, pairing, zero-hours grouping, driver
  detection, priority). Ground truth used to validate the workbook formulas.
- `raw_layout.py` / `element_layout.py` - exact row/column layout constants
  for the six raw reports, per the brief.
- `raw_writer.py` - populates the six paste tabs.
- `styles.py` - Hakim brand styling helpers.
- `output1.py`, `output2.py`, `output3.py` - build each deliverable.
- `validate.py` - builds all three workbooks, recalculates each with
  LibreOffice, asserts zero formula errors, and cross-checks the workbooks'
  own computed KPIs against `reference_calc.py`.

## Regenerating

```
python3 validate.py
```

Requires `openpyxl` and LibreOffice (`soffice` with the Calc component -
`apt-get install libreoffice-calc`) on PATH.

## Known limits (documented on the Control Sheet)

- The comparison engine supports up to 90 employees per run (headroom over
  the current ~60; raise `MAXROWS` in `output1.py` and rebuild if the
  practice roster grows beyond this).
- Tolerance group is inferred from the practice name: any practice whose
  name contains "Head Office" uses the HO2 tolerance; all others use the HG
  tolerance.
- A starter's first payment is also raised as a review item (not just
  "Explained") when it is at or above the material-value threshold
  (£1,500), so unusually large first payments still get a look.
