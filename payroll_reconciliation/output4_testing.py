"""Builds the tester-facing pack: a plain-English how-to-test guide plus a
Pass/Fail checklist, for handing to someone testing the reconciliation pack
for the first time. Not one of the three core deliverables - this is the
internal UAT (user acceptance testing) companion document.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
import styles as S

# (area, test, steps, expected_result)
CHECKLIST = [
    ("1. Getting started", "Open the Reconciliation Tool file",
     "Open 'Hakim Group - Payroll Reconciliation Tool.xlsx'.",
     "The file opens and you can see tabs along the bottom, starting with Control Sheet."),
    ("1. Getting started", "Read the Control Sheet",
     "Click the Control Sheet tab. Read the monthly steps and the pink warning box.",
     "It's clear what to do each month, in plain English. The gold boxes are obviously the ones you're meant to type into."),
    ("1. Getting started", "Change the tolerance",
     "Click on the gold 'Tolerance - HG practices' box and change the number.",
     "The box lets you type a new number easily. Nothing looks broken."),

    ("2. Pasting real data", "Paste NPV Comparison",
     "Delete the example rows below the header on the 'NPV Comparison' tab (keep the header row). Paste your real export starting at that header row.",
     "Your data lines up under the right column headings (Payroll Number, Prior Net Pay, etc.)."),
    ("2. Pasting real data", "Paste Payment Breakdown - current month",
     "Same as above on the 'Payment Breakdown Current' tab.",
     "Practice lands in column D and pay elements start at column K."),
    ("2. Pasting real data", "Paste Payment Breakdown - prior month (the tricky one)",
     "Same as above on the 'Payment Breakdown Prior' tab. IMPORTANT: check whether this export has an extra column at the very start before pasting - if it does, delete that column first.",
     "Practice still lands in column D and pay elements still start at column K, same as the current month tab."),
    ("2. Pasting real data", "Paste New Starters",
     "Same idea on the 'New Starters' tab.",
     "Your starters list appears correctly, with Personal Reference in column K."),
    ("2. Pasting real data", "Paste Leavers",
     "Same idea on the 'Leavers' tab.",
     "Your leavers list appears correctly, with Personal Reference in column K."),
    ("2. Pasting real data", "Paste Structure report",
     "Same idea on the 'Structure' tab.",
     "Your structure data appears correctly, with Payroll Reference in column P and Category in column AI."),
    ("2. Pasting real data", "Everything updates by itself",
     "After pasting all six tabs, click on the Summary tab.",
     "The numbers on Summary have already changed to match your real data - you didn't have to press any buttons or type any formulas."),

    ("3. Summary tab", "Employee count looks right",
     "Look at 'Employee count (compared)' on the Summary tab.",
     "That number roughly matches how many people you'd expect to be on payroll (excluding zero hours staff)."),
    ("3. Summary tab", "Review count looks sensible",
     "Look at 'Review required count'.",
     "It's a believable number - not zero (unless genuinely nothing moved) and not everyone."),
    ("3. Summary tab", "Top 20 movements make sense",
     "Scroll to the 'Top 20 review movements by £' table.",
     "The people listed are ones you'd expect to see - the biggest pay changes. The 'Main Movement' column names something believable (e.g. Bonus, Basic Salary)."),
    ("3. Summary tab", "Totals reconciliation",
     "Look at the 'Totals reconciliation' section (Net Pay, Total Gross, Employer NI, etc).",
     "The Net Pay total is close to (or matches) what you'd expect to see on the BACS payment file."),
    ("3. Summary tab", "Headcount reconciliation",
     "Look at the 'Headcount reconciliation' section at the bottom.",
     "It says 'Reconciled'. If it says 'Check required', that's worth a note but isn't necessarily a bug - flag it anyway."),

    ("4. Exceptions tab", "Everyone you'd expect is there",
     "Click the Exceptions tab and scroll through.",
     "You recognise the payroll numbers as real people who should be compared this month."),
    ("4. Exceptions tab", "Zero hours staff are NOT here",
     "Check whether anyone on a zero-hours-only contract appears on this tab.",
     "They shouldn't be here - they should only appear on the Zero Hours tab instead."),
    ("4. Exceptions tab", "Status column makes sense",
     "Look down the Status column.",
     "Starters say 'Explained: Starter', leavers say 'Explained: Leaver', and the rest say either 'OK' or 'Review required' - nothing confusing or blank where it shouldn't be."),
    ("4. Exceptions tab", "Try typing a note",
     "Click a gold Notes cell on any row and type a short note.",
     "It lets you type normally, like any other Excel cell."),

    ("5. Zero Hours tab", "Zero-hours-only staff appear here",
     "Click the Zero Hours tab.",
     "Anyone whose ONLY contract is zero hours shows up here, with their pay comparison."),
    ("5. Zero Hours tab", "Mixed contracts do NOT appear here",
     "Check anyone who has BOTH a zero-hours contract and a permanent/fixed-term contract.",
     "They should NOT be on this tab - they should be on the Exceptions tab instead, since they have a 'real' contract too."),

    ("6. Drilldown tab", "Look up a real person",
     "Click the Drilldown tab. Type a real payroll number into the gold box.",
     "You see that person's practice, status, and every pay element compared side by side for both months."),
    ("6. Drilldown tab", "Look up a made-up number",
     "Type a payroll number that doesn't exist (e.g. P00000).",
     "It says something sensible like 'Not found' rather than showing an error or crashing."),
    ("6. Drilldown tab", "Leave it blank",
     "Delete whatever is in the gold lookup box so it's empty.",
     "Nothing breaks - the table below just goes blank or shows nothing, no red error messages."),

    ("7. Investigation List file", "Priorities look right",
     "Open 'Hakim Group - Investigation List.xlsx'. Look at the Priority column.",
     "The people marked 'High' are genuinely the big or serious ones (large amounts, or no pay with no leaver on record)."),
    ("7. Investigation List file", "Can type into the gold columns",
     "Click 'Investigated by' and 'Outcome' on a row and type something.",
     "Types normally, no issues."),
    ("7. Investigation List file", "Summary counts match",
     "Compare the counts on this file's Summary tab to the Reconciliation Tool's Summary tab.",
     "The 'review required' style numbers roughly line up between the two files."),

    ("8. SLT Pack file - GDPR check", "No names anywhere - this one really matters",
     "Open 'Hakim Group - SLT Pack.xlsx'. Look through every tab carefully.",
     "You cannot find a single employee name anywhere - only payroll numbers. If you spot a name anywhere in this file, that is a serious problem, flag it immediately."),
    ("8. SLT Pack file - GDPR check", "Charts look right",
     "Look at the donut and bar charts on the Dashboard and Expenses tabs.",
     "The charts have sensible labels and the slices/bars roughly match the numbers next to them."),
    ("8. SLT Pack file - GDPR check", "Everyone has a reason",
     "Check the All Employees tab.",
     "Every single person has something in the Reason column - not just the ones flagged for review."),

    ("9. Try to break it", "Close and reopen",
     "Close the file completely (saving if asked) and open it again.",
     "Everything still looks the same and works the same."),
    ("9. Try to break it", "Leave a tab empty",
     "Pick one of the six paste tabs and delete all the data rows (just leave the header).",
     "Nothing crashes. The Summary/Exceptions numbers just drop to reflect less data, rather than showing errors everywhere."),
    ("9. Try to break it", "A really big pay change",
     "Find or fake one person with a huge pay increase (e.g. double their pay).",
     "They show up clearly as 'Review required' with 'High' priority and a sensible reason."),
    ("9. Try to break it", "Look for red error messages",
     "Scroll through every tab in all three files looking for anything starting with a hash symbol (#) - that's what an Excel error looks like.",
     "You find none at all. If you find even one, write down exactly which cell, on which tab, in which file."),
]

INSTRUCTIONS = [
    ("What is this?",
     "We've built a tool that checks everyone's pay each month against last month, and flags anything "
     "that looks off. Before the payroll team relies on it, we need someone to try it out properly and "
     "tell us if anything looks wrong, confusing, or broken."),
    ("What does 'testing' mean?",
     "It just means: use it like you normally would, with real data, and pay close attention. If "
     "something looks weird, wrong, or doesn't make sense - that's a 'fail', and we want to know about it. "
     "If it works the way you'd expect - that's a 'pass'."),
    ("What you'll need",
     "The three files we sent you, plus a real month of the six iTrent reports (NPV Comparison, Payment "
     "Breakdown x2, New Starters, Leavers, Structure report) that you can paste in."),
    ("How to actually do it",
     "1. Open this file and go to the 'Test Checklist' tab.\n"
     "2. Go through the tests roughly in order, top to bottom - they're grouped into sections.\n"
     "3. For each row: do what the 'Steps' column says, then compare what you see to the 'Expected Result' column.\n"
     "4. Click the Result cell for that row and pick Pass or Fail from the dropdown.\n"
     "5. If it's a Fail (or even if something feels 'off' but you're not sure), write what happened in the "
     "Notes column - be as specific as you can (which tab, which cell, what you typed, what you saw).\n"
     "6. Keep going until you've done every row.\n"
     "7. Save the file and send it back."),
    ("If something breaks badly",
     "Don't panic and don't try to fix it yourself. Just write down exactly what you did right before it "
     "broke, take a screenshot if you can, and mark it as a Fail. That's exactly what this test is for."),
    ("A few things worth knowing",
     "- The gold-coloured boxes are the ONLY cells you're meant to type into. Everything else works itself out.\n"
     "- If a number looks wrong, it's still useful feedback even if you're not 100% sure - just say what you noticed.\n"
     "- There's no such thing as a silly question or a silly Fail. We'd rather hear about ten things that turn "
     "out to be fine than miss the one that matters."),
]


def build_instructions_sheet(wb):
    ws = wb.create_sheet("How To Test")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=60, max_col=8)
    S.set_tab_color(ws)
    ws.merge_cells("A1:F2")
    S.style_title(ws["A1"], "Testing the Payroll Reconciliation Pack - A Simple Guide")

    row = 4
    for heading, body in INSTRUCTIONS:
        ws[f"A{row}"] = heading
        ws[f"A{row}"].font = S.f_subheader()
        row += 1
        ws.merge_cells(f"A{row}:F{row + body.count(chr(10))}")
        cell = ws[f"A{row}"]
        cell.value = body
        cell.font = S.f_body()
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        n_lines = body.count("\n") + 1 + body.count(". ") // 6
        ws.row_dimensions[row].height = max(20, 16 * (body.count(chr(10)) + 1) + 14 * (len(body) // 90))
        row += body.count(chr(10)) + 2

    ws["A" + str(row + 1)] = "Next tab: Test Checklist ->"
    ws["A" + str(row + 1)].font = Font(name=S.FONT_NAME, size=11, bold=True, color=S.PINK)

    S.col_widths(ws, {"A": 90})
    ws.freeze_panes = "A3"
    return ws


def build_checklist_sheet(wb):
    ws = wb.create_sheet("Test Checklist")
    ws.sheet_view.showGridLines = False
    S.apply_offwhite_background(ws, max_row=8 + len(CHECKLIST), max_col=9)
    S.set_tab_color(ws)
    ws.merge_cells("A1:I1")
    S.style_title(ws["A1"], "Test Checklist - Pass or Fail Every Row")
    ws["A2"] = "Result and Notes are the only cells to type into. Pick Pass or Fail from the dropdown."
    ws["A2"].font = S.f_note()
    ws.merge_cells("A2:I2")

    header_row = 3
    headers = ["#", "Area", "Test", "Steps", "Expected Result", "Result", "Notes / What Went Wrong",
               "Tested By", "Date"]
    for i, h in enumerate(headers):
        ws.cell(row=header_row, column=1 + i, value=h)
    S.style_header_row(ws, header_row, 1, len(headers))

    data_start = header_row + 1
    dv = DataValidation(type="list", formula1='"Pass,Fail,Not tested"', allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)

    for i, (area, test, steps, expected) in enumerate(CHECKLIST):
        r = data_start + i
        ws.cell(row=r, column=1, value=i + 1)
        ws.cell(row=r, column=2, value=area)
        ws.cell(row=r, column=3, value=test)
        ws.cell(row=r, column=4, value=steps)
        ws.cell(row=r, column=5, value=expected)
        result_cell = ws.cell(row=r, column=6, value="Not tested")
        S.style_input_cell(result_cell)
        dv.add(result_cell)
        notes_cell = ws.cell(row=r, column=7)
        S.style_input_cell(notes_cell)
        notes_cell.alignment = Alignment(horizontal="left", wrap_text=True, vertical="top")
        by_cell = ws.cell(row=r, column=8)
        S.style_input_cell(by_cell)
        date_cell = ws.cell(row=r, column=9)
        S.style_input_cell(date_cell)

        for col in (1, 2, 3, 4, 5):
            cell = ws.cell(row=r, column=col)
            cell.font = S.f_body()
            cell.border = S.BORDER_THIN
            cell.alignment = Alignment(horizontal="left", wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 46

    last_row = data_start + len(CHECKLIST) - 1
    ws.conditional_formatting.add(
        f"F{data_start}:F{last_row}",
        S.CellIsRule(operator="equal", formula=['"Fail"'], fill=S.FILL_PINK,
                     font=Font(name=S.FONT_NAME, color="FFFFFF", bold=True)))
    ws.conditional_formatting.add(
        f"A{data_start}:I{last_row}",
        S.FormulaRule(formula=[f'$F{data_start}="Fail"'], fill=S.FILL_PINK_LIGHT))

    S.col_widths(ws, {"A": 4, "B": 20, "C": 30, "D": 42, "E": 40, "F": 12, "G": 40, "H": 14, "I": 12})
    S.freeze_and_filter(ws, header_row, 1, len(headers), last_row)

    summary_row = last_row + 3
    ws[f"B{summary_row}"] = "Totals"
    ws[f"B{summary_row}"].font = S.f_subheader()
    ws[f"B{summary_row+1}"] = "Passed"
    ws[f"D{summary_row+1}"] = f'=COUNTIF(F{data_start}:F{last_row},"Pass")'
    ws[f"B{summary_row+2}"] = "Failed"
    ws[f"D{summary_row+2}"] = f'=COUNTIF(F{data_start}:F{last_row},"Fail")'
    ws[f"B{summary_row+3}"] = "Not tested yet"
    ws[f"D{summary_row+3}"] = f'=COUNTIF(F{data_start}:F{last_row},"Not tested")'
    for i in range(1, 4):
        rr = summary_row + i
        ws[f"B{rr}"].font = S.f_body()
        c = ws[f"D{rr}"]
        c.font = Font(name=S.FONT_NAME, bold=True, color=S.PURPLE)
        c.number_format = "#,##0"
        c.border = S.BORDER_THIN
        c.alignment = Alignment(horizontal="center")
    ws.conditional_formatting.add(
        f"D{summary_row+2}",
        S.CellIsRule(operator="greaterThan", formula=["0"], fill=S.FILL_PINK,
                     font=Font(name=S.FONT_NAME, color="FFFFFF", bold=True)))

    return ws


def build_output4(path):
    wb = Workbook()
    wb.remove(wb.active)
    build_instructions_sheet(wb)
    build_checklist_sheet(wb)
    wb.active = 0
    wb.save(path)
    return path


if __name__ == "__main__":
    build_output4("output/Hakim Group - Testing Guide and Checklist.xlsx")
    print("Testing pack written.")
