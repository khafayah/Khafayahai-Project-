"""Column-letter lookups for Payment Breakdown pay elements, derived once
from the fixed ALL_ELEMENTS order so every formula-building module agrees."""
from mock_data import ALL_ELEMENTS, AGGREGATE_ELEMENTS, REAL_ELEMENTS
import raw_layout as L

ELEMENT_COL = {name: L.pb_element_col_letter(i) for i, name in enumerate(ALL_ELEMENTS)}

TOTAL_GROSS_COL = ELEMENT_COL["Total Gross"]
EMPLOYER_NI_COL = ELEMENT_COL["Employer NI"]
EMPLOYER_PENSION_COL = ELEMENT_COL["Employer Pension"]
APPRENTICESHIP_LEVY_COL = ELEMENT_COL["Apprenticeship Levy"]
BASIC_SALARY_COL = ELEMENT_COL["Basic Salary"]

REAL_ELEMENT_COLS = [ELEMENT_COL[name] for name in REAL_ELEMENTS]
