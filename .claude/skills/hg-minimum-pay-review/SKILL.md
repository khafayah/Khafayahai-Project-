---
name: hg-minimum-pay-review
description: Run this when Khafayah types "national minimum wage" (or NMW, NLW, minimum wage review). Work out the cost of a National Minimum Wage / National Living Wage rise for Hakim Group, plus the pay compression (pay gap) impact on Managers and DOs, and produce a backup workbook and HG one-pagers. Use when Khafayah asks about minimum wage, NLW, NMW, Budget pay rates, uplift costs, pay compression or pay gaps for Hakim Group.
---

# Hakim Group minimum pay review (NMW/NLW cost and pay gaps)

## How to start
When Khafayah types "national minimum wage" (or similar):
1. Fetch the Notion skill "National Minimum Wage Review: Cost and Pay Gaps (Hakim Group)" (under Hakim Group Payroll) if Notion is connected. It holds the master prompt. Follow it together with this file.
2. Confirm the new rates on GOV.UK and show them in a table with links.
3. Ask for the data (latest payroll report, or the populated HG template) and the month it is from. Ask for AGE at the start date only. Never ask for, accept or store dates of birth (GDPR). If a file contains dates of birth, stop, tell Khafayah, and ask her to replace them with ages.
4. Ask what has changed: pension rate, job titles for Managers and DOs, who the reports are for.
5. Run sections 2 to 7 below.

Khafayah is Head of Payroll at Hakim Group. Write to her as her assistant and truth-check partner. Use the HG-friendly voice: plain English, short sentences, no contractions, no em dashes, English spelling. Ask before assuming anything that is missing.

## 1. Confirm the rates (never from memory or news alone)
- Use GOV.UK as the source: the Budget document (HM Treasury) or the HMRC / GOV.UK minimum wage rates page. News sites can be wrong (in 2026 the news said £13.20; the Budget document said £13.21).
- Confirm: start date (1 April), rates for 21 and over, 18 to 20, 16 to 17, apprentices, accommodation offset.
- Confirm employer NI rate and secondary threshold, and pension qualifying earnings limits, for the tax year.
- Hakim Group employer pension: 3% of qualifying earnings (confirmed October 2026). Re-confirm each year.
- Report the sources with links.

## 2. Check the data before calculating
Expected columns (same order as the HG template Data sheet):
A Payroll Ref | B Category | C Job type | D Basis | E Work location | F Pay basis (Annual/Hourly) | G Occupancy start date | H FTE | I FTE salary | J Pro-rated salary | K Contract hours a week | L Weeks worked | M Hourly rate | N Date of birth in Khafayah's own copy; ages only when shared with Claude
Checks (report each one):
- Column layout. Payroll exports often have an extra row-number column; a shifted column breaks every formula.
- Row count, duplicate refs (people with two posts), blank ages, text errors (#N/A), ages under 16 or over 75.
- Hourly rate should equal FTE salary / (FT hours x FT weeks). Hourly rates are stored as floats (12.709999), so always round to 2 decimal places before comparing.
- For hourly-paid staff the pro-rated column is NOT yearly pay. Use hourly rate x contract hours x weeks worked.
- The HG template works out age from date of birth in column O. Before sharing, Khafayah copies column O and pastes values over column N, so only ages remain (the template accepts ages in column N). Otherwise she works out ages in her own file with =DATEDIF(DOB,DATE(yyyy,4,1),"Y") and sends ages only. If she sees 127, the formula is pointing at the hourly rate column; tell her to click the date of birth cell when building the formula.
- With ages only, the 'below current minimum' check uses age minus 1 (lowest possible current age) to avoid false alarms.

## 3. Calculation rules
- New minimum by age on the start date. Apprentice rate only if job type is Apprentice AND (under 19 OR started within the last 12 months). Under 16: not entitled.
- Uplift needed if ROUND(hourly rate,2) < new minimum. New rate = new minimum.
- Salaried: new yearly pay = pro-rated salary x new rate / current rate. Hourly paid: new rate x contract hours x weeks worked.
- Anyone not needing a rise must show zero change (avoid rounding noise).
- Company NI = rate x MAX(0, pay - threshold). Pension = rate x pay between the lower and upper limits.
- Cost is a full 12 months from the start date; monthly = yearly / 12.
- Flags: below current minimum now, apprentice moves to age rate later, turns 21 (age 20) or 18 (age 17) in the year, zero hours not costed, age missing, under 16.

## 4. Pay gaps (pay compression)
- Groups: Managers = Practice Manager + PP - Practice Manager. DOs = Dispensing Optician + PP - Dispensing Optician. Team = Optical Assistant. Ask whether supervisors or seniors are coded under "Other".
- Gap = hourly pay minus adult minimum (today and new). Report median pay, median gap, within £1, on the minimum, gap bands, and median lead over Optical Assistants.
- Options (extra cost on top of the minimum rise, incl NI and pension):
  1. Lift protected roles to new minimum + £1.
  2. Same pence rise as the minimum for every protected role paid above today's minimum.
  3. Same % rise as the minimum for every protected role.
- Suggest Option 1 as the lowest-cost fix plus a pay structure review. Flag Managers paid the minimum (possible job title errors).

## 5. Verify
- Cross-check totals with an independent calculation (for example pandas) and reconcile to the penny or explain rounding.
- Recalculate the workbook (LibreOffice headless) and check for zero formula errors.
- Re-read every number in the one-pagers against the workbook.

## 6. Outputs
1. Backup workbook (or the populated HG template): Summary, Pay Gaps, Data, Rates. Live formulas. Rates on one sheet.
2. Management one-pager (use the hg-one-pager skill): side-by-side Today | From [date] | Extra cost table, who is affected, costs still to come, checks done, decisions, "How we worked this out" (data source, period, method).
3. Pay gaps one-pager with an HG pink/navy chart, the three options, suggested next steps.
4. HG-voice cover email in a code block.

## 7. Data protection
Never ask for dates of birth. Never commit staff data (refs, pay, ages) to git or any external service. Keep files in the session scratchpad and send them to Khafayah. Remind her to password-protect the workbook. One-pagers carry no personal data.

## Template
The reusable workbook is HG_Minimum_Pay_and_Pay_Gaps_Template.xlsx (Data sheet columns A to N are inputs, O to AM are locked formulas; Rates sheet holds all rates and the pay gap group mapping in columns E to G). 2026 baseline for testing: October 2026 report, 3,033 jobs, 1,062 need a rise, £722,354.52 a year.
