"""Builds Output 2: the Investigation List pack.

Populated from the same reconciliation engine as Output 1 (via
reference_calc.py, run against the same source data) so the two packs agree
by construction. Each month this file is regenerated as a snapshot alongside
Output 1; its own Summary tab totals are formula-driven off its own
Investigation List tab so they stay correct if rows are added or reordered.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import styles as S

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def _sorted_review_items(result):
    items = list(result["review_items"])
    items.sort(key=lambda r: (PRIORITY_ORDER.get(r["priority"], 9), -abs(r["diff"])))
    return items


def build_investigation_list_sheet(wb, result):
    ws = wb.create_sheet("Investigation List")
    ws.sheet_view.showGridLines = False
    items = _sorted_review_items(result)
    S.apply_offwhite_background(ws, max_row=8 + max(len(items), 1), max_col=15)
    S.set_tab_color(ws)
    ws.merge_cells("A1:M1")
    S.style_title(ws["A1"], "Investigation List")
    ws["A2"] = "Sorted by priority then £ movement. Gold columns are the only cells to type into."
    ws["A2"].font = S.f_note()
    ws.merge_cells("A2:M2")

    header_row = 3
    headers = ["Priority", "Payroll Number", "Practice", "Status", "Difference £",
               "Difference %", "Cause (Element)", "Element Prior £", "Element Current £",
               "Element Diff £", "Investigated by", "Outcome"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))

    data_start = header_row + 1
    for i, item in enumerate(items):
        r = data_start + i
        cause = item["cause"] or {}
        values = [
            item["priority"], item["payroll_number"], item["practice"], item["status"],
            item["diff"], item["diff_pct"], cause.get("element", "Unmatched - review manually"),
            cause.get("prior"), cause.get("current"), cause.get("diff"),
        ]
        for j, v in enumerate(values):
            cell = ws.cell(row=r, column=1 + j, value=v)
            cell.font = S.f_body()
            cell.border = S.BORDER_THIN
            cell.alignment = Alignment(horizontal="left" if j in (1, 2, 3, 6) else "center")
        for col_idx, fmt in [(5, '#,##0.00'), (6, '0.0%'), (8, '#,##0.00'), (9, '#,##0.00'), (10, '#,##0.00')]:
            ws.cell(row=r, column=col_idx).number_format = fmt
        inv_cell = ws.cell(row=r, column=11)
        out_cell = ws.cell(row=r, column=12)
        S.style_input_cell(inv_cell)
        S.style_input_cell(out_cell)

    last_row = data_start + len(items) - 1 if items else data_start
    S.add_status_conditional_formatting(ws, "A", data_start, last_row, "A", "L")
    ws.conditional_formatting.add(
        f"A{data_start}:A{last_row}",
        S.CellIsRule(operator="equal", formula=['"High"'], fill=S.FILL_PINK,
                     font=Font(name=S.FONT_NAME, color="FFFFFF", bold=True)))
    S.col_widths(ws, {"A": 10, "B": 14, "C": 24, "D": 22, "E": 12, "F": 11, "G": 22,
                       "H": 14, "I": 14, "J": 13, "K": 20, "L": 20})
    S.freeze_and_filter(ws, header_row, 1, len(headers), last_row)
    return ws, len(items)


def build_summary_sheet(wb, result, n_items):
    ws = wb.create_sheet("Summary")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=40, max_col=10)
    S.set_tab_color(ws)
    ws.merge_cells("A1:F1")
    S.style_title(ws["A1"], "Investigation List - Summary")

    last_row = 3 + n_items if n_items else 4
    kpis = [
        ("Total review items", f'=COUNTA(\'Investigation List\'!$B$4:$B${last_row})'),
        ("High priority", f'=COUNTIF(\'Investigation List\'!$A$4:$A${last_row},"High")'),
        ("Medium priority", f'=COUNTIF(\'Investigation List\'!$A$4:$A${last_row},"Medium")'),
        ("Low priority", f'=COUNTIF(\'Investigation List\'!$A$4:$A${last_row},"Low")'),
        ("Zero hours (visibility only)", f"=COUNTA('Zero Hours'!$A$4:$A${4 + result['summary']['zero_hours_count']})"),
    ]
    ws["B4"] = "Key Metrics"
    ws["B4"].font = S.f_subheader()
    for i, (label, formula) in enumerate(kpis):
        r = 5 + i
        ws[f"B{r}"] = label
        ws[f"B{r}"].font = S.f_body()
        cell = ws[f"D{r}"]
        cell.value = formula
        cell.font = Font(name=S.FONT_NAME, size=12, bold=True, color=S.PURPLE)
        cell.number_format = "#,##0"
        cell.border = S.BORDER_THIN
        cell.alignment = Alignment(horizontal="center")

    cause_row = 11
    ws[f"B{cause_row}"] = "Breakdown by cause"
    ws[f"B{cause_row}"].font = S.f_subheader()
    header_row = cause_row + 1
    ws.cell(row=header_row, column=2, value="Cause (Element)")
    ws.cell(row=header_row, column=4, value="Count")
    S.style_header_row(ws, header_row, 2, 4)

    causes = sorted({(i["cause"]["element"] if i["cause"] else "Unmatched - review manually")
                      for i in result["review_items"]})
    if not causes:
        causes = ["Unmatched - review manually"]
    for i, cause in enumerate(causes):
        r = header_row + 1 + i
        ws[f"B{r}"] = cause
        ws[f"B{r}"].font = S.f_body()
        ws[f"D{r}"] = f'=COUNTIF(\'Investigation List\'!$G$4:$G${last_row},B{r})'
        ws[f"D{r}"].number_format = "#,##0"
        ws[f"D{r}"].border = S.BORDER_THIN
        ws[f"D{r}"].alignment = Alignment(horizontal="center")

    S.col_widths(ws, {"A": 3, "B": 26, "C": 6, "D": 12})
    ws.freeze_panes = "A3"
    return ws


def build_zero_hours_sheet(wb, result):
    ws = wb.create_sheet("Zero Hours")
    ws.sheet_view.showGridLines = False
    rows = result["zero_hours_rows"]
    S.apply_offwhite_background(ws, max_row=8 + max(len(rows), 1), max_col=8)
    S.set_tab_color(ws)
    ws.merge_cells("A1:F1")
    S.style_title(ws["A1"], "Zero Hours Contracts")
    ws["A2"] = "Listed for visibility only - not part of the investigation count."
    ws["A2"].font = S.f_note()
    ws.merge_cells("A2:F2")

    header_row = 3
    headers = ["Payroll Number", "Practice", "Prior Net", "Current Net", "Difference £", "Difference %"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))
    data_start = header_row + 1
    for i, row in enumerate(rows):
        r = data_start + i
        vals = [row["payroll_number"], row["practice"], row["prior_net"], row["current_net"],
                row["diff"], row["diff_pct"]]
        for j, v in enumerate(vals):
            cell = ws.cell(row=r, column=1 + j, value=v)
            cell.font = S.f_body()
            cell.border = S.BORDER_THIN
            cell.alignment = Alignment(horizontal="left" if j < 2 else "center")
        for col_idx, fmt in [(3, '#,##0.00'), (4, '#,##0.00'), (5, '#,##0.00'), (6, '0.0%')]:
            ws.cell(row=r, column=col_idx).number_format = fmt
    last_row = data_start + len(rows) - 1 if rows else data_start
    S.col_widths(ws, {"A": 14, "B": 24, "C": 12, "D": 12, "E": 12, "F": 11})
    S.freeze_and_filter(ws, header_row, 1, len(headers), last_row)
    return ws


def build_output2(result, path):
    wb = Workbook()
    wb.remove(wb.active)
    inv_ws, n_items = build_investigation_list_sheet(wb, result)
    build_summary_sheet(wb, result, n_items)
    build_zero_hours_sheet(wb, result)
    order = ["Summary", "Investigation List", "Zero Hours"]
    wb._sheets = [wb[name] for name in order]
    wb.active = 0
    wb.save(path)
    return path


if __name__ == "__main__":
    from mock_data import build_dataset
    from reference_calc import compute_reconciliation
    ds = build_dataset()
    result = compute_reconciliation(ds)
    build_output2(result, "output/Hakim Group - Investigation List.xlsx")
    print("Output 2 written.")
