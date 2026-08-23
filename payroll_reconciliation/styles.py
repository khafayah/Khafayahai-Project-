"""Hakim Group brand styling for the payroll reconciliation pack."""
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
PURPLE = "3D315D"        # deep purple - headers, titles
PINK = "DF5694"          # hot pink - accents, review highlights
GOLD = "FFC000"          # gold - input cells (the ONLY cells a user edits)
OFFWHITE = "F7F7F7"      # off-white - backgrounds
MID_PURPLE = "66609B"    # mid purple - secondary tabs
GREY = "D9D9D9"          # grey - helper / calculation cells
WHITE = "FFFFFF"
RED_TEXT = "C00000"
GREEN_TEXT = "1E7B34"

FONT_NAME = "Aptos"

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
def f_title():
    return Font(name=FONT_NAME, size=16, bold=True, color=WHITE)

def f_header():
    return Font(name=FONT_NAME, size=11, bold=True, color=WHITE)

def f_subheader():
    return Font(name=FONT_NAME, size=11, bold=True, color=PURPLE)

def f_body():
    return Font(name=FONT_NAME, size=10, color="000000")

def f_input():
    return Font(name=FONT_NAME, size=10, bold=True, color="000000")

def f_note():
    return Font(name=FONT_NAME, size=9, italic=True, color="595959")

def f_kpi_value():
    return Font(name=FONT_NAME, size=20, bold=True, color=WHITE)

def f_kpi_label():
    return Font(name=FONT_NAME, size=10, color=WHITE)

# ---------------------------------------------------------------------------
# Fills
# ---------------------------------------------------------------------------
FILL_PURPLE = PatternFill("solid", fgColor=PURPLE)
FILL_PINK = PatternFill("solid", fgColor=PINK)
FILL_GOLD = PatternFill("solid", fgColor=GOLD)
FILL_OFFWHITE = PatternFill("solid", fgColor=OFFWHITE)
FILL_MID_PURPLE = PatternFill("solid", fgColor=MID_PURPLE)
FILL_GREY = PatternFill("solid", fgColor=GREY)
FILL_WHITE = PatternFill("solid", fgColor=WHITE)
FILL_PINK_LIGHT = PatternFill("solid", fgColor="FBE1EC")

THIN = Side(style="thin", color="BFBFBF")
BORDER_THIN = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# ---------------------------------------------------------------------------
# Reusable block styling
# ---------------------------------------------------------------------------

def style_title(cell, text):
    cell.value = text
    cell.font = f_title()
    cell.fill = FILL_PURPLE
    cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)


def style_header_row(ws, row, first_col, last_col, height=22):
    ws.row_dimensions[row].height = height
    for c in range(first_col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = f_header()
        cell.fill = FILL_PURPLE
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN


def style_secondary_header_row(ws, row, first_col, last_col, height=20):
    ws.row_dimensions[row].height = height
    for c in range(first_col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = f_header()
        cell.fill = FILL_MID_PURPLE
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN


def style_input_cell(cell):
    cell.fill = FILL_GOLD
    cell.font = f_input()
    cell.border = BORDER_THIN
    cell.alignment = Alignment(horizontal="center", vertical="center")


def style_helper_cell(cell):
    cell.fill = FILL_GREY
    cell.font = Font(name=FONT_NAME, size=9, color="595959")
    cell.alignment = Alignment(horizontal="center", vertical="center")


def style_body_cell(cell, number_format=None, bold=False, align="left"):
    cell.font = Font(name=FONT_NAME, size=10, bold=bold)
    cell.alignment = Alignment(horizontal=align, vertical="center")
    cell.border = BORDER_THIN
    if number_format:
        cell.number_format = number_format


def set_tab_color(ws, secondary=False):
    ws.sheet_properties.tabColor = MID_PURPLE if secondary else PURPLE


def apply_offwhite_background(ws, max_row=200, max_col=40):
    for r in range(1, max_row + 1):
        for c in range(1, max_col + 1):
            cell = ws.cell(row=r, column=c)
            if cell.fill is None or cell.fill.fgColor.rgb in (None, "00000000"):
                cell.fill = FILL_OFFWHITE


def freeze_and_filter(ws, header_row, first_col, last_col, last_row):
    """Freeze panes below the header row and add an autofilter over the table."""
    ws.freeze_panes = ws.cell(row=header_row + 1, column=first_col).coordinate
    first_letter = get_column_letter(first_col)
    last_letter = get_column_letter(last_col)
    ws.auto_filter.ref = f"{first_letter}{header_row}:{last_letter}{last_row}"


def col_widths(ws, widths: dict):
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def review_highlight_rule(fill=FILL_PINK_LIGHT):
    """Conditional format: font used for 'Review required' status text."""
    font = Font(name=FONT_NAME, color=RED_TEXT, bold=True)
    return font


def add_status_conditional_formatting(ws, status_col_letter, first_row, last_row, first_col_letter, last_col_letter):
    """Highlight entire row pink when the status column says 'Review required'."""
    rng = f"{first_col_letter}{first_row}:{last_col_letter}{last_row}"
    formula = f'${status_col_letter}{first_row}="Review required"'
    ws.conditional_formatting.add(
        rng,
        FormulaRule(formula=[formula], fill=FILL_PINK_LIGHT, font=Font(name=FONT_NAME, color=RED_TEXT, bold=True)),
    )


def add_check_conditional_formatting(ws, check_col_letter, first_row, last_row):
    rng = f"{check_col_letter}{first_row}:{check_col_letter}{last_row}"
    ws.conditional_formatting.add(
        rng,
        CellIsRule(operator="equal", formula=['"CHECK"'], fill=FILL_PINK, font=Font(name=FONT_NAME, color=WHITE, bold=True)),
    )
