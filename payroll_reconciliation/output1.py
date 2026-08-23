"""Builds Output 1: the reusable, formula-driven Reconciliation Tool."""
from openpyxl import Workbook
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

import styles as S
import raw_layout as L
import raw_writer as RW
from mock_data import REAL_ELEMENTS, ALL_ELEMENTS
from element_layout import (ELEMENT_COL, TOTAL_GROSS_COL, EMPLOYER_NI_COL,
                             EMPLOYER_PENSION_COL, APPRENTICESHIP_LEVY_COL,
                             BASIC_SALARY_COL, REAL_ELEMENT_COLS)

MAXROWS = 90                        # employee capacity for the comparison engine
HELPERS_FIRST = 2
HELPERS_LAST = HELPERS_FIRST + MAXROWS - 1   # 151

NPV_LAST = L.NPV_DATA_START - 1 + MAXROWS       # 164
PB_LAST = L.PB_DATA_START - 1 + MAXROWS         # 164
NS_LAST = L.NS_DATA_START - 1 + 60              # 73
LV_LAST = L.LV_DATA_START - 1 + 60              # 71
ST_LAST = L.ST_DATA_START - 1 + 300             # 312

CTRL = "Control Sheet"
NPV_SHEET = "NPV Comparison"
PBC_SHEET = "Payment Breakdown Current"
PBP_SHEET = "Payment Breakdown Prior"
NS_SHEET = "New Starters"
LV_SHEET = "Leavers"
ST_SHEET = "Structure"
HLP_SHEET = "_Helpers"

TOL_HG = f"'{CTRL}'!$C$5"
TOL_HO2 = f"'{CTRL}'!$C$6"
MIN_FLAG = f"'{CTRL}'!$C$7"
PRIOR_LABEL = f"'{CTRL}'!$C$8"
CURRENT_LABEL = f"'{CTRL}'!$C$9"

MATERIAL_STARTER = 1500
LARGE_MONEY = 2000
MEDIUM_MONEY = 500


def _npv_row(h_row):
    return L.NPV_DATA_START - HELPERS_FIRST + h_row


# ---------------------------------------------------------------------------
# _Helpers engine sheet
# ---------------------------------------------------------------------------

def build_helpers_sheet(wb):
    ws = wb.create_sheet(HLP_SHEET)
    ws.sheet_state = "hidden"
    headers = ["PayrollNumber", "PriorNet", "CurrentNet", "Practice", "IsZeroHoursOnly",
               "IsMainList", "IsStarter", "IsLeaver", "PersonalRef", "IsPaired",
               "ToleranceGroupPct", "Diff", "DiffPct", "OverTolerance", "Flagged",
               "Status", "NoPayNoLeaver", "IsReviewItem", "Priority",
               "BasicSalaryPrior", "BasicSalaryCurrent", "BasicSalaryPctChange"]
    for i, h in enumerate(headers):
        ws.cell(row=1, column=i + 1, value=h)
    real_start_col = 23  # W
    for i, name in enumerate(REAL_ELEMENTS):
        ws.cell(row=1, column=real_start_col + i, value=name)
    diff_end_col = real_start_col + len(REAL_ELEMENTS) - 1  # AH (34)
    max_col = diff_end_col + 1        # AI MaxAbsDiff
    driver_col = diff_end_col + 2     # AJ DriverElement
    driver_val_col = diff_end_col + 3  # AK DriverDiffValue
    rank_col = diff_end_col + 4        # AL RankKey
    ws.cell(row=1, column=max_col, value="MaxAbsDiff")
    ws.cell(row=1, column=driver_col, value="DriverElement")
    ws.cell(row=1, column=driver_val_col, value="DriverDiffValue")
    ws.cell(row=1, column=rank_col, value="RankKey")

    diff_start_letter = get_column_letter(real_start_col)
    diff_end_letter = get_column_letter(diff_end_col)
    max_letter = get_column_letter(max_col)
    driver_letter = get_column_letter(driver_col)
    driver_val_letter = get_column_letter(driver_val_col)
    rank_letter = get_column_letter(rank_col)

    for r in range(HELPERS_FIRST, HELPERS_LAST + 1):
        npv_r = _npv_row(r)
        ws[f"A{r}"] = f"=IF('{NPV_SHEET}'!D{npv_r}=\"\",\"\",'{NPV_SHEET}'!D{npv_r})"
        ws[f"B{r}"] = f"=IF('{NPV_SHEET}'!E{npv_r}=\"\",\"\",'{NPV_SHEET}'!E{npv_r})"
        ws[f"C{r}"] = f"=IF('{NPV_SHEET}'!F{npv_r}=\"\",\"\",'{NPV_SHEET}'!F{npv_r})"
        ws[f"D{r}"] = f'=IF($A{r}="","",IFERROR(INDEX({ST_SHEET}!$E${L.ST_DATA_START}:$E${ST_LAST},MATCH($A{r},{ST_SHEET}!$P${L.ST_DATA_START}:$P${ST_LAST},0)),""))'
        ws[f"E{r}"] = (f'=IF($A{r}="",0,IF(COUNTIF({ST_SHEET}!$P${L.ST_DATA_START}:$P${ST_LAST},$A{r})=0,0,'
                        f'IF(COUNTIFS({ST_SHEET}!$P${L.ST_DATA_START}:$P${ST_LAST},$A{r},{ST_SHEET}!$N${L.ST_DATA_START}:$N${ST_LAST},"<>Zero Hours")=0,1,0)))')
        ws[f"F{r}"] = f'=IF($A{r}="",0,1-E{r})'
        ws[f"G{r}"] = f'=IF($A{r}="",0,IF(COUNTIF(\'{NS_SHEET}\'!$D${L.NS_DATA_START}:$D${NS_LAST},$A{r})>0,1,0))'
        ws[f"H{r}"] = f'=IF($A{r}="",0,IF(COUNTIF(\'{LV_SHEET}\'!$D${L.LV_DATA_START}:$D${LV_LAST},$A{r})>0,1,0))'
        ws[f"I{r}"] = (f'=IF($A{r}="","",IFERROR(INDEX(\'{NS_SHEET}\'!$K${L.NS_DATA_START}:$K${NS_LAST},MATCH($A{r},\'{NS_SHEET}\'!$D${L.NS_DATA_START}:$D${NS_LAST},0)),'
                        f'IFERROR(INDEX(\'{LV_SHEET}\'!$K${L.LV_DATA_START}:$K${LV_LAST},MATCH($A{r},\'{LV_SHEET}\'!$D${L.LV_DATA_START}:$D${LV_LAST},0)),"")))')
        ws[f"J{r}"] = (f'=IF(AND(G{r}=1,I{r}<>"",COUNTIF(\'{LV_SHEET}\'!$K${L.LV_DATA_START}:$K${LV_LAST},I{r})>0),1,'
                        f'IF(AND(H{r}=1,I{r}<>"",COUNTIF(\'{NS_SHEET}\'!$K${L.NS_DATA_START}:$K${NS_LAST},I{r})>0),1,0))')
        ws[f"K{r}"] = f'=IF(ISNUMBER(SEARCH("Head Office",D{r})),{TOL_HO2},{TOL_HG})'
        ws[f"L{r}"] = f'=IF(OR($A{r}="",AND(B{r}="",C{r}="")),"",IF(B{r}="",C{r},IF(C{r}="",-B{r},C{r}-B{r})))'
        ws[f"M{r}"] = f"=IFERROR(L{r}/B{r},\"\")"
        ws[f"N{r}"] = f'=IF($A{r}="",0,IF(OR(B{r}="",C{r}="",C{r}=0,IF(ISNUMBER(M{r}),ABS(M{r})>K{r},FALSE)),1,0))'
        ws[f"O{r}"] = f'=IF(OR($A{r}="",L{r}=""),0,IF(AND(N{r}=1,ABS(L{r})>={MIN_FLAG},F{r}=1),1,0))'
        ws[f"P{r}"] = (f'=IF($A{r}="","",IF(F{r}=0,"Zero Hours",IF(J{r}=1,"Explained: Paired transfer",'
                        f'IF(AND(G{r}=1,H{r}=0,J{r}=0),"Explained: Starter",'
                        f'IF(AND(H{r}=1,G{r}=0,J{r}=0),"Explained: Leaver",'
                        f'IF(O{r}=1,"Review required","OK"))))))')
        ws[f"Q{r}"] = f'=IF(AND(F{r}=1,OR(C{r}="",C{r}=0),H{r}=0,J{r}=0),1,0)'
        ws[f"R{r}"] = (f'=IF(F{r}=0,0,IF(P{r}="Review required",1,'
                        f'IF(AND(P{r}="Explained: Starter",ISNUMBER(C{r}),C{r}>={MATERIAL_STARTER}),1,0)))')
        ws[f"S{r}"] = (f'=IF(R{r}=0,"",IF(Q{r}=1,"High",'
                        f'IF(AND(P{r}="Explained: Starter",C{r}>={MATERIAL_STARTER}),"High",'
                        f'IF(ABS(L{r})>={LARGE_MONEY},"High",IF(ABS(L{r})>={MEDIUM_MONEY},"Medium","Low")))))')
        ws[f"T{r}"] = f"=SUMIFS('{PBP_SHEET}'!${BASIC_SALARY_COL}${L.PB_DATA_START}:${BASIC_SALARY_COL}${PB_LAST},'{PBP_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},$A{r})"
        ws[f"U{r}"] = f"=SUMIFS('{PBC_SHEET}'!${BASIC_SALARY_COL}${L.PB_DATA_START}:${BASIC_SALARY_COL}${PB_LAST},'{PBC_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},$A{r})"
        ws[f"V{r}"] = f"=IFERROR((U{r}-T{r})/T{r},\"\")"

        for i, name in enumerate(REAL_ELEMENTS):
            col_letter = get_column_letter(real_start_col + i)
            src_col = ELEMENT_COL[name]
            cur = f"SUMIFS('{PBC_SHEET}'!${src_col}${L.PB_DATA_START}:${src_col}${PB_LAST},'{PBC_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},$A{r})"
            pri = f"SUMIFS('{PBP_SHEET}'!${src_col}${L.PB_DATA_START}:${src_col}${PB_LAST},'{PBP_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},$A{r})"
            ws[f"{col_letter}{r}"] = f"=({cur})-({pri})"

        elem_letters = [get_column_letter(real_start_col + i) for i in range(len(REAL_ELEMENTS))]
        # Plain (non-array) formulas throughout - nested MAX/IF chains avoid CSE
        # array-formula recalculation, which is far slower and less reliable
        # under LibreOffice headless recalculation than ordinary formulas.
        ws[f"{max_letter}{r}"] = "=MAX(" + ",".join(f"ABS({c}{r})" for c in elem_letters) + ")"
        driver_chain = '""'
        val_chain = '""'
        for c in reversed(elem_letters):
            driver_chain = f'IF(ABS({c}{r})={max_letter}{r},{c}$1,{driver_chain})'
            val_chain = f'IF(ABS({c}{r})={max_letter}{r},{c}{r},{val_chain})'
        ws[f"{driver_letter}{r}"] = f'=IF({max_letter}{r}<0.005,"",{driver_chain})'
        ws[f"{driver_val_letter}{r}"] = f'=IF({max_letter}{r}<0.005,"",{val_chain})'
        ws[f"{rank_letter}{r}"] = f'=IF(R{r}=1,ABS(L{r})-ROW()/100000000,"")'

    return {"diff_start": diff_start_letter, "diff_end": diff_end_letter,
            "max_col": max_letter, "driver_col": driver_letter,
            "driver_val_col": driver_val_letter, "rank_col": rank_letter}


# ---------------------------------------------------------------------------
# Control Sheet
# ---------------------------------------------------------------------------

def build_control_sheet(wb, dataset):
    ws = wb.create_sheet(CTRL)
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=60, max_col=10)
    S.set_tab_color(ws)
    ws.merge_cells("A1:H2")
    S.style_title(ws["A1"], "Hakim Group  |  Payroll Reconciliation Tool")

    ws["B4"] = "Monthly Control Panel"
    ws["B4"].font = S.f_subheader()

    labels = [
        ("B5", "Tolerance - HG practices (%)", "C5", 0.20, "0%"),
        ("B6", "Tolerance - HO2 practice (%)", "C6", 0.05, "0%"),
        ("B7", "Minimum £ to flag", "C7", 50, '£#,##0'),
        ("B8", "Prior period label", "C8", dataset["period_prior"], None),
        ("B9", "Current period label", "C9", dataset["period_current"], None),
    ]
    for label_cell, label_text, input_cell, value, fmt in labels:
        ws[label_cell] = label_text
        ws[label_cell].font = S.f_body()
        c = ws[input_cell]
        c.value = value
        if fmt:
            c.number_format = fmt
        S.style_input_cell(c)
    ws["B10"] = ("Rule: practices whose name contains 'Head Office' use the HO2 tolerance; "
                 "all others use the HG tolerance. Edit only the gold cells above.")
    ws["B10"].font = S.f_note()
    ws.row_dimensions[10].height = 28
    ws.merge_cells("B10:H10")
    ws["B10"].alignment = Alignment(wrap_text=True, vertical="top")

    ws["B12"] = "Monthly steps"
    ws["B12"].font = S.f_subheader()
    steps = [
        "1. Export the six iTrent reports below for the current payroll run.",
        "2. Check the prior-month Payment Breakdown export for an EXTRA leading 'Reference No' "
        "column (see warning below). Delete it if present so both months line up.",
        "3. Clear old data from each paste tab (keep the header row) and paste the new export "
        "starting at the header row shown in 'Expected report layout' below.",
        "4. Update the Prior/Current period labels above.",
        "5. Open Summary, Exceptions, Zero Hours and Drilldown - they recalculate automatically.",
        "6. Work through Exceptions top to bottom; use Drilldown to inspect any payroll number.",
        "7. Agree totals on the Summary tab to BACS and to the payroll submissions.",
    ]
    for i, s in enumerate(steps):
        r = 13 + i
        ws[f"B{r}"] = s
        ws[f"B{r}"].font = S.f_body()
        ws.merge_cells(f"B{r}:H{r}")
        ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 16

    layout_row = 13 + len(steps) + 2
    ws[f"B{layout_row}"] = "Expected report layout"
    ws[f"B{layout_row}"].font = S.f_subheader()
    header_row = layout_row + 1
    cols = ["Report", "Paste tab", "Header row", "Data starts", "Key columns"]
    for i, h in enumerate(cols):
        cell = ws.cell(row=header_row, column=2 + i, value=h)
    S.style_secondary_header_row(ws, header_row, 2, 6)
    rows = [
        ("NPV Comparison (Net Pay)", NPV_SHEET, L.NPV_HEADER_ROW, L.NPV_DATA_START, "D Payroll No, E Prior Net, F Current Net"),
        ("Payment Breakdown - current month", PBC_SHEET, L.PB_HEADER_ROW, L.PB_DATA_START, "D Practice, K.. Elements, last col Reference No"),
        ("Payment Breakdown - prior month", PBP_SHEET, L.PB_HEADER_ROW, L.PB_DATA_START, "Same as above once the extra leading column is removed"),
        ("New Starters", NS_SHEET, L.NS_HEADER_ROW, L.NS_DATA_START, "D Payroll No, K Personal Reference"),
        ("Leavers", LV_SHEET, L.LV_HEADER_ROW, L.LV_DATA_START, "D Payroll No, K Personal Reference"),
        ("Structure report", ST_SHEET, L.ST_HEADER_ROW, L.ST_DATA_START, "L Position, N Basis, P Payroll Ref (MHR), AI Category"),
    ]
    for i, row_vals in enumerate(rows):
        r = header_row + 1 + i
        for j, v in enumerate(row_vals):
            cell = ws.cell(row=r, column=2 + j, value=v)
            S.style_body_cell(cell)
    S.col_widths(ws, {"A": 3, "B": 30, "C": 24, "D": 12, "E": 12, "F": 45, "G": 10, "H": 10})

    warn_row = header_row + 1 + len(rows) + 2
    ws.merge_cells(f"B{warn_row}:H{warn_row + 3}")
    warn_cell = ws[f"B{warn_row}"]
    warn_cell.value = ("⚠ WARNING - PRIOR MONTH PAYMENT BREAKDOWN: some iTrent exports carry an extra "
                        "leading 'Reference No' column that shifts Practice, elements and everything else "
                        "one column to the right. If Practice does not land in column D and the first "
                        "pay element does not land in column K on the 'Payment Breakdown Prior' tab, "
                        "delete the extra leading column before pasting. Getting this wrong silently "
                        "misaligns the whole comparison.")
    warn_cell.font = Font(name=S.FONT_NAME, size=10, bold=True, color="FFFFFF")
    warn_cell.fill = S.FILL_PINK
    warn_cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[warn_row].height = 20
    for rr in range(warn_row, warn_row + 4):
        ws.row_dimensions[rr].height = 18

    ws.freeze_panes = "A3"
    return ws


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def build_summary_sheet(wb, helper_cols):
    ws = wb.create_sheet("Summary")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=80, max_col=12)
    S.set_tab_color(ws)
    ws.merge_cells("A1:L2")
    S.style_title(ws["A1"], "Payroll Reconciliation - Summary")

    ws["B4"] = "Key Metrics"
    ws["B4"].font = S.f_subheader()
    kpis = [
        ("Employee count (compared)", f"=COUNTIF({HLP_SHEET}!$F${HELPERS_FIRST}:$F${HELPERS_LAST},1)"),
        ("Movements over tolerance", f'=SUMPRODUCT(({HLP_SHEET}!$F${HELPERS_FIRST}:$F${HELPERS_LAST}=1)*({HLP_SHEET}!$P${HELPERS_FIRST}:$P${HELPERS_LAST}<>"OK")*({HLP_SHEET}!$P${HELPERS_FIRST}:$P${HELPERS_LAST}<>""))'),
        ("Explained starters/leavers", f'=SUMPRODUCT(({HLP_SHEET}!$F${HELPERS_FIRST}:$F${HELPERS_LAST}=1)*(LEFT({HLP_SHEET}!$P${HELPERS_FIRST}:$P${HELPERS_LAST},9)="Explained"))'),
        ("Zero hours count", f"=COUNTIF({HLP_SHEET}!$E${HELPERS_FIRST}:$E${HELPERS_LAST},1)"),
        ("Review required count", f"=COUNTIF({HLP_SHEET}!$R${HELPERS_FIRST}:$R${HELPERS_LAST},1)"),
    ]
    for i, (label, formula) in enumerate(kpis):
        r = 5 + i
        ws[f"B{r}"] = label
        ws[f"B{r}"].font = S.f_body()
        cell = ws[f"D{r}"]
        cell.value = formula
        cell.font = Font(name=S.FONT_NAME, size=12, bold=True, color=S.PURPLE)
        cell.number_format = "#,##0"
        cell.fill = S.FILL_WHITE
        cell.alignment = Alignment(horizontal="center")
        cell.border = S.BORDER_THIN

    # ---------------- Top 20 review movements by £ ----------------
    top_row = 12
    ws[f"B{top_row}"] = "Top 20 review movements by £"
    ws[f"B{top_row}"].font = S.f_subheader()
    header_row = top_row + 1
    headers = ["Rank", "Payroll Number", "Practice", "Prior Net", "Current Net", "Difference £",
               "Difference %", "Status", "Priority", "Main Movement"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=2 + i, value=h)
    S.style_header_row(ws, header_row, 2, 2 + len(headers) - 1)
    rk = helper_cols["rank_col"]
    for k in range(1, 21):
        r = header_row + k
        ws[f"B{r}"] = k
        val_cell = f"IFERROR(LARGE({HLP_SHEET}!${rk}${HELPERS_FIRST}:${rk}${HELPERS_LAST},{k}),\"\")"
        src_helper = f"IFERROR(MATCH({val_cell},{HLP_SHEET}!${rk}${HELPERS_FIRST}:${rk}${HELPERS_LAST},0)+1,\"\")"
        ws[f"J{r}"] = f"={src_helper}"  # hidden helper: absolute _Helpers row
        S.style_helper_cell(ws[f"J{r}"])
        for col_letter, hlp_col in [("C", "A"), ("D", "D")]:
            pass
        ws[f"C{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$A${HELPERS_FIRST}:$A${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"D{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$D${HELPERS_FIRST}:$D${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"E{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$B${HELPERS_FIRST}:$B${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"F{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$C${HELPERS_FIRST}:$C${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"G{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$L${HELPERS_FIRST}:$L${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"H{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$M${HELPERS_FIRST}:$M${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"I{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$P${HELPERS_FIRST}:$P${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"K{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!$S${HELPERS_FIRST}:$S${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        ws[f"L{r}"] = f'=IF($J{r}="","",INDEX({HLP_SHEET}!${helper_cols["driver_col"]}${HELPERS_FIRST}:${helper_cols["driver_col"]}${HELPERS_LAST},$J{r}-{HELPERS_FIRST}+1))'
        for col in ["C", "D", "E", "F", "G", "H", "I", "K", "L"]:
            cell = ws[f"{col}{r}"]
            S.style_body_cell(cell, number_format=('#,##0.00' if col in ("E", "F", "G") else ('0.0%' if col == "H" else None)))
    S.add_status_conditional_formatting(ws, "I", header_row + 1, header_row + 20, "B", "L")

    # ---------------- Totals reconciliation ----------------
    tot_row = header_row + 23
    ws[f"B{tot_row}"] = "Totals reconciliation"
    ws[f"B{tot_row}"].font = S.f_subheader()
    thr = tot_row + 1
    for i, h in enumerate(["Figure", "Prior", "Current", "Difference"]):
        ws.cell(row=thr, column=2 + i, value=h)
    S.style_header_row(ws, thr, 2, 5)
    npv_rng_e = f"'{NPV_SHEET}'!$E${L.NPV_DATA_START}:$E${NPV_LAST}"
    npv_rng_f = f"'{NPV_SHEET}'!$F${L.NPV_DATA_START}:$F${NPV_LAST}"
    figs = [
        ("Net Pay", npv_rng_e, npv_rng_f),
        ("Total Gross", f"'{PBP_SHEET}'!${TOTAL_GROSS_COL}${L.PB_DATA_START}:${TOTAL_GROSS_COL}${PB_LAST}",
         f"'{PBC_SHEET}'!${TOTAL_GROSS_COL}${L.PB_DATA_START}:${TOTAL_GROSS_COL}${PB_LAST}"),
        ("Employer NI", f"'{PBP_SHEET}'!${EMPLOYER_NI_COL}${L.PB_DATA_START}:${EMPLOYER_NI_COL}${PB_LAST}",
         f"'{PBC_SHEET}'!${EMPLOYER_NI_COL}${L.PB_DATA_START}:${EMPLOYER_NI_COL}${PB_LAST}"),
        ("Employer Pension", f"'{PBP_SHEET}'!${EMPLOYER_PENSION_COL}${L.PB_DATA_START}:${EMPLOYER_PENSION_COL}${PB_LAST}",
         f"'{PBC_SHEET}'!${EMPLOYER_PENSION_COL}${L.PB_DATA_START}:${EMPLOYER_PENSION_COL}${PB_LAST}"),
        ("Apprenticeship Levy", f"'{PBP_SHEET}'!${APPRENTICESHIP_LEVY_COL}${L.PB_DATA_START}:${APPRENTICESHIP_LEVY_COL}${PB_LAST}",
         f"'{PBC_SHEET}'!${APPRENTICESHIP_LEVY_COL}${L.PB_DATA_START}:${APPRENTICESHIP_LEVY_COL}${PB_LAST}"),
    ]
    for i, (label, prior_rng, current_rng) in enumerate(figs):
        r = thr + 1 + i
        ws[f"B{r}"] = label
        ws[f"B{r}"].font = S.f_body()
        ws[f"C{r}"] = f"=SUM({prior_rng})"
        ws[f"D{r}"] = f"=SUM({current_rng})"
        ws[f"E{r}"] = f"=D{r}-C{r}"
        for col in ("C", "D", "E"):
            S.style_body_cell(ws[f"{col}{r}"], number_format='£#,##0.00')
    note_row = thr + 1 + len(figs) + 1
    ws.merge_cells(f"B{note_row}:E{note_row}")
    ws[f"B{note_row}"] = "Note: agree Net Pay above to BACS. Agree Total Gross / Employer NI / Employer Pension / Apprenticeship Levy to the payroll submissions (FPS/EPS)."
    ws[f"B{note_row}"].font = S.f_note()
    ws[f"B{note_row}"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[note_row].height = 28

    # ---------------- Headcount reconciliation ----------------
    hc_row = note_row + 3
    ws[f"B{hc_row}"] = "Headcount reconciliation"
    ws[f"B{hc_row}"].font = S.f_subheader()
    ws[f"B{hc_row+1}"] = "Prior records"
    ws[f"D{hc_row+1}"] = f"=COUNT('{NPV_SHEET}'!$E${L.NPV_DATA_START}:$E${NPV_LAST})"
    ws[f"B{hc_row+2}"] = "+ Starters"
    ws[f"D{hc_row+2}"] = f"=COUNTA('{NS_SHEET}'!$D${L.NS_DATA_START}:$D${NS_LAST})"
    ws[f"B{hc_row+3}"] = "- Leavers"
    ws[f"D{hc_row+3}"] = f"=COUNTA('{LV_SHEET}'!$D${L.LV_DATA_START}:$D${LV_LAST})"
    ws[f"B{hc_row+4}"] = "Expected current records (Prior + Starters - Leavers)"
    ws[f"D{hc_row+4}"] = f"=D{hc_row+1}+D{hc_row+2}-D{hc_row+3}"
    ws[f"B{hc_row+5}"] = "Actual current records"
    ws[f"D{hc_row+5}"] = f"=COUNT('{NPV_SHEET}'!$F${L.NPV_DATA_START}:$F${NPV_LAST})"
    ws[f"B{hc_row+6}"] = "Check"
    ws[f"D{hc_row+6}"] = f'=IF(D{hc_row+4}=D{hc_row+5},"Reconciled","Check required")'
    for i in range(1, 7):
        r = hc_row + i
        ws[f"B{r}"].font = S.f_body()
        cell = ws[f"D{r}"]
        cell.font = Font(name=S.FONT_NAME, bold=(i in (4, 6)))
        cell.number_format = "#,##0"
        cell.border = S.BORDER_THIN
        cell.alignment = Alignment(horizontal="center")
    ws.conditional_formatting.add(
        f"D{hc_row+6}",
        S.FormulaRule(formula=[f'D{hc_row+6}="Check required"'], fill=S.FILL_PINK,
                      font=Font(name=S.FONT_NAME, color="FFFFFF", bold=True)))

    S.col_widths(ws, {"A": 3, "B": 24, "C": 15, "D": 15, "E": 15, "F": 12, "G": 12, "H": 12,
                       "I": 22, "J": 8, "K": 12, "L": 24})
    ws.column_dimensions["J"].hidden = True
    ws.freeze_panes = "A3"
    return ws


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

def build_exceptions_sheet(wb, helper_cols):
    ws = wb.create_sheet("Exceptions")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=6 + MAXROWS, max_col=15)
    S.set_tab_color(ws)
    ws.merge_cells("A1:M1")
    S.style_title(ws["A1"], "Exceptions - Net Pay Movements")
    ws["A2"] = ("Zero-hours-only staff are excluded here - see the Zero Hours tab. "
                "Gold 'Notes' cells are the only cells to type into.")
    ws["A2"].font = S.f_note()
    ws.merge_cells("A2:M2")

    header_row = 3
    headers = ["Payroll Number", "Practice", "Prior Net", "Current Net", "Difference £",
               "Difference %", "Starter?", "Leaver?", "Status", "Basic Salary % Change",
               "Main Movement (Element)", "Main Movement (£)", "Notes"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))
    ws.cell(row=header_row, column=len(headers) + 2, value="Helper: rank pointer")
    S.style_helper_cell(ws.cell(row=header_row, column=len(headers) + 2))

    data_start = header_row + 1
    helper_col_idx = len(headers) + 2  # column O
    helper_letter = get_column_letter(helper_col_idx)

    for k in range(1, MAXROWS + 1):
        r = data_start + k - 1
        formula = (f'IFERROR(SMALL(IF({HLP_SHEET}!$F${HELPERS_FIRST}:$F${HELPERS_LAST}=1,'
                   f'ROW({HLP_SHEET}!$F${HELPERS_FIRST}:$F${HELPERS_LAST})),ROWS($A${data_start}:A{r})),"")')
        ws[f"{helper_letter}{r}"] = ArrayFormula(f"{helper_letter}{r}", f"={formula}")
        S.style_helper_cell(ws[f"{helper_letter}{r}"])
        idx = f'${helper_letter}{r}-{HELPERS_FIRST}+1'
        ws[f"A{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$A${HELPERS_FIRST}:$A${HELPERS_LAST},{idx}))'
        ws[f"B{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$D${HELPERS_FIRST}:$D${HELPERS_LAST},{idx}))'
        ws[f"C{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$B${HELPERS_FIRST}:$B${HELPERS_LAST},{idx}))'
        ws[f"D{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$C${HELPERS_FIRST}:$C${HELPERS_LAST},{idx}))'
        ws[f"E{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$L${HELPERS_FIRST}:$L${HELPERS_LAST},{idx}))'
        ws[f"F{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$M${HELPERS_FIRST}:$M${HELPERS_LAST},{idx}))'
        ws[f"G{r}"] = f'=IF(${helper_letter}{r}="","",IF(INDEX({HLP_SHEET}!$G${HELPERS_FIRST}:$G${HELPERS_LAST},{idx})=1,"Starter",""))'
        ws[f"H{r}"] = f'=IF(${helper_letter}{r}="","",IF(INDEX({HLP_SHEET}!$H${HELPERS_FIRST}:$H${HELPERS_LAST},{idx})=1,"Leaver",""))'
        ws[f"I{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$P${HELPERS_FIRST}:$P${HELPERS_LAST},{idx}))'
        ws[f"J{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$V${HELPERS_FIRST}:$V${HELPERS_LAST},{idx}))'
        ws[f"K{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!${helper_cols["driver_col"]}${HELPERS_FIRST}:${helper_cols["driver_col"]}${HELPERS_LAST},{idx}))'
        ws[f"L{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!${helper_cols["driver_val_col"]}${HELPERS_FIRST}:${helper_cols["driver_val_col"]}${HELPERS_LAST},{idx}))'

        for col, fmt in [("C", '#,##0.00'), ("D", '#,##0.00'), ("E", '#,##0.00'),
                          ("F", '0.0%'), ("J", '0.0%'), ("L", '#,##0.00')]:
            ws[f"{col}{r}"].number_format = fmt
        for col in "ABCDEFGHIJKL":
            cell = ws[f"{col}{r}"]
            cell.font = S.f_body()
            cell.alignment = Alignment(horizontal="center" if col not in ("A", "B") else "left")
            cell.border = S.BORDER_THIN
        m_cell = ws[f"M{r}"]
        S.style_input_cell(m_cell)
        m_cell.alignment = Alignment(horizontal="left")

    last_row = data_start + MAXROWS - 1
    S.add_status_conditional_formatting(ws, "I", data_start, last_row, "A", "M")
    S.col_widths(ws, {"A": 14, "B": 24, "C": 12, "D": 12, "E": 12, "F": 11, "G": 9, "H": 9,
                       "I": 20, "J": 12, "K": 20, "L": 13, "M": 26})
    ws.column_dimensions[helper_letter].hidden = True
    S.freeze_and_filter(ws, header_row, 1, len(headers) + 1, last_row)
    return ws


# ---------------------------------------------------------------------------
# Zero Hours
# ---------------------------------------------------------------------------

def build_zero_hours_sheet(wb):
    ws = wb.create_sheet("Zero Hours")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=6 + MAXROWS, max_col=10)
    S.set_tab_color(ws)
    ws.merge_cells("A1:G1")
    S.style_title(ws["A1"], "Zero Hours Contracts - Net Pay Movements")
    ws["A2"] = "Staff whose ONLY contract basis on the Structure report is Zero Hours. Listed for visibility only."
    ws["A2"].font = S.f_note()
    ws.merge_cells("A2:G2")

    header_row = 3
    headers = ["Payroll Number", "Practice", "Prior Net", "Current Net", "Difference £", "Difference %"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))
    helper_col_idx = len(headers) + 2
    helper_letter = get_column_letter(helper_col_idx)
    ws.cell(row=header_row, column=helper_col_idx, value="Helper: rank pointer")
    S.style_helper_cell(ws.cell(row=header_row, column=helper_col_idx))

    data_start = header_row + 1
    for k in range(1, MAXROWS + 1):
        r = data_start + k - 1
        formula = (f'IFERROR(SMALL(IF({HLP_SHEET}!$E${HELPERS_FIRST}:$E${HELPERS_LAST}=1,'
                   f'ROW({HLP_SHEET}!$E${HELPERS_FIRST}:$E${HELPERS_LAST})),ROWS($A${data_start}:A{r})),"")')
        ws[f"{helper_letter}{r}"] = ArrayFormula(f"{helper_letter}{r}", f"={formula}")
        S.style_helper_cell(ws[f"{helper_letter}{r}"])
        idx = f'${helper_letter}{r}-{HELPERS_FIRST}+1'
        ws[f"A{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$A${HELPERS_FIRST}:$A${HELPERS_LAST},{idx}))'
        ws[f"B{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$D${HELPERS_FIRST}:$D${HELPERS_LAST},{idx}))'
        ws[f"C{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$B${HELPERS_FIRST}:$B${HELPERS_LAST},{idx}))'
        ws[f"D{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$C${HELPERS_FIRST}:$C${HELPERS_LAST},{idx}))'
        ws[f"E{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$L${HELPERS_FIRST}:$L${HELPERS_LAST},{idx}))'
        ws[f"F{r}"] = f'=IF(${helper_letter}{r}="","",INDEX({HLP_SHEET}!$M${HELPERS_FIRST}:$M${HELPERS_LAST},{idx}))'
        for col, fmt in [("C", '#,##0.00'), ("D", '#,##0.00'), ("E", '#,##0.00'), ("F", '0.0%')]:
            ws[f"{col}{r}"].number_format = fmt
        for col in "ABCDEF":
            cell = ws[f"{col}{r}"]
            cell.font = S.f_body()
            cell.alignment = Alignment(horizontal="center" if col not in ("A", "B") else "left")
            cell.border = S.BORDER_THIN

    last_row = data_start + MAXROWS - 1
    S.col_widths(ws, {"A": 14, "B": 24, "C": 12, "D": 12, "E": 12, "F": 11})
    ws.column_dimensions[helper_letter].hidden = True
    S.freeze_and_filter(ws, header_row, 1, len(headers), last_row)
    return ws


# ---------------------------------------------------------------------------
# Drilldown
# ---------------------------------------------------------------------------

def build_drilldown_sheet(wb):
    ws = wb.create_sheet("Drilldown")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=40, max_col=8)
    S.set_tab_color(ws)
    ws.merge_cells("A1:F1")
    S.style_title(ws["A1"], "Drilldown - Inspect a Payroll Number")

    ws["A3"] = "Enter Payroll Number:"
    ws["A3"].font = S.f_body()
    lookup_cell = ws["C3"]
    S.style_input_cell(lookup_cell)
    lookup_ref = "$C$3"

    def hlp_lookup(col):
        return f'IFERROR(INDEX({HLP_SHEET}!${col}${HELPERS_FIRST}:${col}${HELPERS_LAST},MATCH({lookup_ref},{HLP_SHEET}!$A${HELPERS_FIRST}:$A${HELPERS_LAST},0)),"Not found")'

    info = [
        ("Practice", hlp_lookup("D")),
        ("Status", hlp_lookup("P")),
        ("Starter?", f'IF(N({hlp_lookup("G")})=1,"Yes","No")'),
        ("Leaver?", f'IF(N({hlp_lookup("H")})=1,"Yes","No")'),
        ("Zero Hours contract?", f'IF(N({hlp_lookup("E")})=1,"Yes","No")'),
        ("Prior Net", hlp_lookup("B")),
        ("Current Net", hlp_lookup("C")),
        ("Difference £", hlp_lookup("L")),
        ("Difference %", hlp_lookup("M")),
    ]
    for i, (label, formula) in enumerate(info):
        r = 5 + i
        ws[f"A{r}"] = label
        ws[f"A{r}"].font = S.f_body()
        cell = ws[f"C{r}"]
        cell.value = f"={formula}"
        cell.font = Font(name=S.FONT_NAME, bold=True)
        cell.border = S.BORDER_THIN
        if label in ("Prior Net", "Current Net", "Difference £"):
            cell.number_format = '#,##0.00'
        elif label == "Difference %":
            cell.number_format = '0.0%'

    tol_lookup_row = 5 + len(info) + 1
    ws[f"A{tol_lookup_row}"] = "Tolerance applied"
    ws[f"A{tol_lookup_row}"].font = S.f_body()
    ws[f"C{tol_lookup_row}"] = f'=IF(ISNUMBER(SEARCH("Head Office",C5)),{TOL_HO2},{TOL_HG})'
    ws[f"C{tol_lookup_row}"].number_format = "0%"
    ws[f"C{tol_lookup_row}"].border = S.BORDER_THIN

    table_row = tol_lookup_row + 2
    ws[f"A{table_row}"] = "All pay elements - both months compared"
    ws[f"A{table_row}"].font = S.f_subheader()
    header_row = table_row + 1
    headers = ["Element", "Prior", "Current", "Difference", "Difference %", "CHECK"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))

    data_start = header_row + 1
    for i, name in enumerate(ALL_ELEMENTS):
        r = data_start + i
        col_letter = ELEMENT_COL[name]
        ws[f"A{r}"] = name
        ws[f"A{r}"].font = S.f_body()
        prior_f = f"SUMIFS('{PBP_SHEET}'!${col_letter}${L.PB_DATA_START}:${col_letter}${PB_LAST},'{PBP_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},{lookup_ref})"
        current_f = f"SUMIFS('{PBC_SHEET}'!${col_letter}${L.PB_DATA_START}:${col_letter}${PB_LAST},'{PBC_SHEET}'!${L.PB_REFNO_LETTER}${L.PB_DATA_START}:${L.PB_REFNO_LETTER}${PB_LAST},{lookup_ref})"
        ws[f"B{r}"] = f"=IF({lookup_ref}=\"\",\"\",{prior_f})"
        ws[f"C{r}"] = f"=IF({lookup_ref}=\"\",\"\",{current_f})"
        ws[f"D{r}"] = f'=IF({lookup_ref}="","",C{r}-B{r})'
        ws[f"E{r}"] = f'=IFERROR(D{r}/B{r},"")'
        ws[f"F{r}"] = (f'=IF({lookup_ref}="","",IF(AND(ABS(D{r})>={MIN_FLAG},'
                        f'OR(B{r}=0,IF(ISNUMBER(E{r}),ABS(E{r})>$C${tol_lookup_row},FALSE))),"CHECK",""))')
        for col, fmt in [("B", '#,##0.00'), ("C", '#,##0.00'), ("D", '#,##0.00'), ("E", '0.0%')]:
            ws[f"{col}{r}"].number_format = fmt
        for col in "ABCDEF":
            cell = ws[f"{col}{r}"]
            cell.font = S.f_body()
            cell.border = S.BORDER_THIN
            cell.alignment = Alignment(horizontal="center" if col != "A" else "left")

    last_row = data_start + len(ALL_ELEMENTS) - 1
    S.add_check_conditional_formatting(ws, "F", data_start, last_row)
    S.col_widths(ws, {"A": 26, "B": 13, "C": 13, "D": 13, "E": 12, "F": 10})
    ws.freeze_panes = f"A{data_start}"
    return ws


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def build_output1(dataset, path):
    wb = Workbook()
    wb.remove(wb.active)

    build_control_sheet(wb, dataset)
    helper_cols = build_helpers_sheet(wb)
    build_summary_sheet(wb, helper_cols)
    build_exceptions_sheet(wb, helper_cols)
    build_zero_hours_sheet(wb)
    build_drilldown_sheet(wb)

    ws_npv = wb.create_sheet(NPV_SHEET)
    RW.write_npv_comparison(ws_npv, dataset)
    ws_pbc = wb.create_sheet(PBC_SHEET)
    RW.write_payment_breakdown(ws_pbc, dataset, "current")
    ws_pbp = wb.create_sheet(PBP_SHEET)
    RW.write_payment_breakdown(ws_pbp, dataset, "prior")
    ws_ns = wb.create_sheet(NS_SHEET)
    RW.write_new_starters(ws_ns, dataset)
    ws_lv = wb.create_sheet(LV_SHEET)
    RW.write_leavers(ws_lv, dataset)
    ws_st = wb.create_sheet(ST_SHEET)
    RW.write_structure(ws_st, dataset)

    wb.active = 0
    wb.save(path)
    return path


if __name__ == "__main__":
    from mock_data import build_dataset
    ds = build_dataset()
    build_output1(ds, "output/Hakim Group - Payroll Reconciliation Tool.xlsx")
    print("Output 1 written.")
