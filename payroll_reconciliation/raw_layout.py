"""Exact row/column layout for the six iTrent raw exports, per the brief.

Header row = the row directly above the first data row in every report,
matching the explicit NPV Comparison spec ("headers row 14, data from row 15")
extended consistently to the other five reports.
"""
from openpyxl.utils import get_column_letter, column_index_from_string
from mock_data import ALL_ELEMENTS, STRUCTURE_FILLER_COLS

# ---------------------------------------------------------------------------
# 1) NPV Comparison (Net Pay)
# ---------------------------------------------------------------------------
NPV_HEADER_ROW = 14
NPV_DATA_START = 15
NPV_COLUMNS = {
    "A": "Payroll Area", "B": "Surname", "C": "Forename",
    "D": "Payroll Number", "E": "Prior Net Pay", "F": "Current Net Pay",
    "G": "Difference", "H": "Difference %", "I": "Payment Date", "J": "Frequency",
}

# ---------------------------------------------------------------------------
# 2/3) Payment Breakdown (current + prior share this layout once aligned)
# ---------------------------------------------------------------------------
PB_HEADER_ROW = 14
PB_DATA_START = 15
PB_ELEMENT_START_COL = 11  # K
PB_ELEMENT_COUNT = len(ALL_ELEMENTS)
PB_ELEMENT_END_COL = PB_ELEMENT_START_COL + PB_ELEMENT_COUNT - 1  # AD
PB_REFNO_COL = PB_ELEMENT_END_COL + 1  # AE
PB_PREFIX_COLUMNS = {
    "A": "Row", "B": "Surname", "C": "Forename", "D": "Practice",
    "E": "Department", "F": "Cost Centre", "G": "Payment Date",
    "H": "Frequency", "I": "Tax Code", "J": "NI Category",
}
PB_PRACTICE_COL = "D"

def pb_element_col_letter(i):
    """1-indexed position within ALL_ELEMENTS -> column letter."""
    return get_column_letter(PB_ELEMENT_START_COL + i)

PB_REFNO_LETTER = get_column_letter(PB_REFNO_COL)

# ---------------------------------------------------------------------------
# 4) New Starters
# ---------------------------------------------------------------------------
NS_HEADER_ROW = 13
NS_DATA_START = 14
NS_COLUMNS = {
    "A": "Row", "B": "Title", "C": "Surname", "D": "Payroll Number",
    "E": "Practice", "F": "Position Name", "G": "Start Date",
    "H": "Category", "I": "Basis", "J": "Department", "K": "Personal Reference",
}

# ---------------------------------------------------------------------------
# 5) Leavers
# ---------------------------------------------------------------------------
LV_HEADER_ROW = 11
LV_DATA_START = 12
LV_COLUMNS = {
    "A": "Row", "B": "Title", "C": "Surname", "D": "Payroll Number",
    "E": "Practice", "F": "Position Name", "G": "Leave Date",
    "H": "Category", "I": "Basis", "J": "Department", "K": "Personal Reference",
}

# ---------------------------------------------------------------------------
# 6) Structure report
# ---------------------------------------------------------------------------
ST_HEADER_ROW = 12
ST_DATA_START = 13
ST_PREFIX_COLUMNS = {
    "A": "Structure ID", "B": "Title", "C": "First Name", "D": "Last Name",
    "E": "Practice", "F": "Department", "G": "Cost Centre", "H": "Start Date",
    "I": "End Date", "J": "Employment Status", "K": "Contracted Hours",
    "L": "Position Name", "M": "Grade", "N": "Basis", "O": "FTE",
    "P": "Payroll Reference",
}
# Q..AH = 18 filler columns, then AI = Category
ST_FILLER_START_COL = column_index_from_string("Q")  # 17
ST_CATEGORY_COL = "AI"
ST_POSITION_COL = "L"
ST_BASIS_COL = "N"
ST_PAYROLL_REF_COL = "P"
