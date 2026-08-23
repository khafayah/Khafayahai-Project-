"""Independent Python re-implementation of the reconciliation logic.

This is deliberately written without reference to the Excel formulas so it can
serve as ground truth: after the workbooks are built and recalculated with
LibreOffice, the cached formula results are compared against these numbers.

Business rules (mirrors the brief):
 - Tolerance is per practice group (HG practices 20%, HO2 5%).
 - Zero-hours-ONLY staff (every Structure row for that person has
   Basis == "Zero Hours") are moved to a separate tab entirely.
 - Starters/leavers are kept on the main list, marked Explained, and matched
   by payroll reference.
 - Two payroll records for the same person (shared personal_reference) where
   one leaves and one starts in the same period are paired and marked
   "Explained: Paired transfer" rather than counted as a leaver + a starter.
 - Everyone else whose net pay differs by more than BOTH the tolerance % and
   the minimum £ to flag is "Review required"; the biggest real (non
   aggregate) pay element movement is named as the likely cause.
 - Priority: High = no pay this month with no leaver record, or a starter's
   first payment above the material threshold, or any absolute movement over
   the large-money threshold. Medium = mid-value movements. Low = the rest.
"""

MATERIAL_STARTER_VALUE = 1500.0
LARGE_MONEY = 2000.0
MEDIUM_MONEY = 500.0


def _pct(diff, prior_net):
    if not prior_net:
        return None
    return diff / prior_net


def _biggest_driver(elements, real_elements):
    """Return (element_name, prior, current, abs_diff) for the largest mover
    among real (non-aggregate) elements, or None if there is no movement."""
    best = None
    for name in real_elements:
        prior, current = elements.get(name, (0.0, 0.0))
        diff = round((current or 0.0) - (prior or 0.0), 2)
        if best is None or abs(diff) > abs(best[3]):
            best = (name, prior, current, diff)
    if best is None or abs(best[3]) < 0.005:
        return None
    return best


def compute_reconciliation(dataset):
    employees = dataset["employees"]
    tolerance_by_group = dataset["tolerance_by_group"]
    min_flag = dataset["min_flag_value"]
    real_elements = dataset["real_elements"]

    starter_refs = {e.personal_reference for e in dataset["starters"]}
    leaver_refs = {e.personal_reference for e in dataset["leavers"]}
    paired_refs = starter_refs & leaver_refs  # same person, two payroll records

    main_rows = []
    zero_hours_rows = []

    for emp in employees:
        prior_net = emp.prior_net
        current_net = emp.current_net
        diff = round((current_net or 0.0) - (prior_net or 0.0), 2)
        diff_pct = _pct(diff, prior_net)
        tolerance = tolerance_by_group[emp.tolerance_group]

        if emp.is_zero_hours_only:
            zero_hours_rows.append({
                "payroll_number": emp.payroll_number,
                "practice": emp.practice,
                "prior_net": prior_net, "current_net": current_net,
                "diff": diff, "diff_pct": diff_pct,
            })
            continue

        is_paired = emp.personal_reference in paired_refs
        status = "OK"
        if is_paired:
            status = "Explained: Paired transfer"
        elif emp.is_starter:
            status = "Explained: Starter"
        elif emp.is_leaver:
            status = "Explained: Leaver"

        over_tolerance = (prior_net in (None, 0)) or (current_net in (None, 0)) or \
            (diff_pct is not None and abs(diff_pct) > tolerance)
        flagged = over_tolerance and abs(diff) >= min_flag

        is_review_item = False
        priority = None
        cause = None

        if status == "OK" and flagged:
            status = "Review required"
            is_review_item = True
        elif status == "Explained: Starter" and (current_net or 0) >= MATERIAL_STARTER_VALUE:
            is_review_item = True  # material first payment - verify even though explained
        elif status == "OK" and not flagged:
            status = "OK"

        # High priority: no pay this month with no leaver record on file
        no_pay_no_leaver = (current_net in (None, 0)) and status not in (
            "Explained: Leaver", "Explained: Paired transfer")
        if no_pay_no_leaver and status == "OK":
            status = "Review required"
            is_review_item = True

        if is_review_item:
            driver = _biggest_driver(emp.elements, real_elements)
            if driver:
                cause = {"element": driver[0], "prior": driver[1], "current": driver[2], "diff": driver[3]}
            if no_pay_no_leaver:
                priority = "High"
            elif status == "Explained: Starter" and (current_net or 0) >= MATERIAL_STARTER_VALUE:
                priority = "High"
            elif abs(diff) >= LARGE_MONEY:
                priority = "High"
            elif abs(diff) >= MEDIUM_MONEY:
                priority = "Medium"
            else:
                priority = "Low"

        basic_prior, basic_current = emp.elements.get("Basic Salary", (0.0, 0.0))
        basic_pct_change = _pct(round((basic_current or 0) - (basic_prior or 0), 2), basic_prior)

        main_rows.append({
            "payroll_number": emp.payroll_number,
            "personal_reference": emp.personal_reference,
            "practice": emp.practice,
            "tolerance_group": emp.tolerance_group,
            "category": emp.category,
            "position_name": emp.position_name,
            "prior_net": prior_net, "current_net": current_net,
            "diff": diff, "diff_pct": diff_pct,
            "is_starter": emp.is_starter, "is_leaver": emp.is_leaver,
            "status": status, "is_review_item": is_review_item,
            "priority": priority, "cause": cause,
            "basic_pct_change": basic_pct_change,
            "story": emp.story,
        })

    review_items = [r for r in main_rows if r["is_review_item"]]
    explained = [r for r in main_rows if r["status"].startswith("Explained")]
    movements_over_tolerance = [
        r for r in main_rows
        if r["status"] != "OK"
    ]

    summary = {
        "employee_count": len(main_rows),
        "movements_over_tolerance": len(movements_over_tolerance),
        "explained_starters_leavers": len(explained),
        "zero_hours_count": len(zero_hours_rows),
        "review_count": len(review_items),
        "prior_records": sum(1 for e in employees if e.prior_net is not None),
        "current_records": sum(1 for e in employees if e.current_net is not None),
        "starters_count": len(dataset["starters"]),
        "leavers_count": len(dataset["leavers"]),
        "total_net_prior": round(sum((e.prior_net or 0.0) for e in employees), 2),
        "total_net_current": round(sum((e.current_net or 0.0) for e in employees), 2),
        "total_gross_prior": round(sum(e.elements.get("Total Gross", (0, 0))[0] for e in employees), 2),
        "total_gross_current": round(sum(e.elements.get("Total Gross", (0, 0))[1] for e in employees), 2),
        "employer_ni_prior": round(sum(e.elements.get("Employer NI", (0, 0))[0] for e in employees), 2),
        "employer_ni_current": round(sum(e.elements.get("Employer NI", (0, 0))[1] for e in employees), 2),
        "employer_pension_prior": round(sum(e.elements.get("Employer Pension", (0, 0))[0] for e in employees), 2),
        "employer_pension_current": round(sum(e.elements.get("Employer Pension", (0, 0))[1] for e in employees), 2),
        "apprenticeship_levy_prior": round(sum(e.elements.get("Apprenticeship Levy", (0, 0))[0] for e in employees), 2),
        "apprenticeship_levy_current": round(sum(e.elements.get("Apprenticeship Levy", (0, 0))[1] for e in employees), 2),
    }
    summary["headcount_check"] = (
        summary["prior_records"] + summary["starters_count"] - summary["leavers_count"]
        == summary["current_records"]
    )

    top20 = sorted(review_items, key=lambda r: abs(r["diff"]), reverse=True)[:20]

    return {
        "main_rows": main_rows,
        "zero_hours_rows": zero_hours_rows,
        "review_items": review_items,
        "top20": top20,
        "summary": summary,
    }


if __name__ == "__main__":
    from mock_data import build_dataset
    ds = build_dataset()
    result = compute_reconciliation(ds)
    import json
    s = result["summary"]
    for k, v in s.items():
        print(f"{k}: {v}")
    print("\nStatus breakdown:")
    from collections import Counter
    print(Counter(r["status"] for r in result["main_rows"]))
    print("\nPriority breakdown (review items):")
    print(Counter(r["priority"] for r in result["review_items"]))
    print("\nCause breakdown (review items):")
    print(Counter(r["cause"]["element"] if r["cause"] else None for r in result["review_items"]))
