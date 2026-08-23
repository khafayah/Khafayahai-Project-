"""Synthetic iTrent-style source data for the Hakim Group payroll reconciliation pack.

This mimics the six raw exports described in the brief, at the exact row/column
layout the reconciliation tool expects. It is used both to populate the
workbook "paste" tabs (so the delivered tool is a working demonstration, not an
empty shell) and to drive an independent Python reference calculation used to
validate the spreadsheet's own formulas.
"""
import random
from dataclasses import dataclass, field

random.seed(42)

PRIOR_LABEL = "June 2026"
CURRENT_LABEL = "July 2026"

PRACTICES = {
    "Riverside Dental Practice": "HG",
    "Kings Road Dental Practice": "HG",
    "Elm Park Dental Practice": "HG",
    "Oakfield Dental Practice": "HG",
    "Hakim Group Head Office": "HO2",
}

TOLERANCE_BY_GROUP = {"HG": 0.20, "HO2": 0.05}
MIN_FLAG_VALUE = 50.0

CATEGORIES = ["Practice Support", "Practice Clinical", "Practice Partner", "HGHQ", "Employee"]

# Element order fixed for both months post-alignment (K onward).
AGGREGATE_ELEMENTS = [
    "Total Gross", "Taxable Gross", "Pensionable Pay", "Hours Paid",
    "Net Pay After Rounding", "Employer NI", "Employer Pension", "Apprenticeship Levy",
]
REAL_ELEMENTS = [
    "Basic Salary", "Overtime", "Bonus", "Mileage Expenses", "Other Expenses",
    "SMP", "SSP", "Pension Deduction", "Student Loan", "Attachment of Earnings",
    "On Call Allowance", "Unsocial Hours Premium",
]
ALL_ELEMENTS = AGGREGATE_ELEMENTS + REAL_ELEMENTS

STRUCTURE_FILLER_COLS = [
    "Line Manager", "Region", "Division", "Pay Group", "Tax Code", "NI Category",
    "Pension Scheme", "Pension Status", "Address Line 1", "Address Line 2", "Town",
    "Postcode", "Email", "Phone", "Bank Name", "Account Ref", "Union Member", "Notes",
]

FIRST_NAMES = ["Amelia", "Oliver", "Isla", "George", "Freya", "Harry", "Poppy", "Jack",
               "Ivy", "Charlie", "Grace", "Leo", "Ruby", "Oscar", "Ella", "Noah",
               "Chloe", "Arthur", "Mia", "Freddie", "Layla", "Alfie", "Sophie", "Theo",
               "Evie", "Jacob", "Lily", "Max", "Zara", "Finn", "Rosie", "Sam",
               "Daisy", "Ben", "Nina", "Kai", "Tara", "Luca", "Anya", "Milo",
               "Priya", "Reuben", "Fatima", "Callum", "Sana", "Dylan", "Amara", "Ethan",
               "Nadia", "Joel", "Yasmin", "Aaron", "Leah", "Tom", "Maya", "Josh",
               "Alia", "Ravi", "Faye", "Sami"]
LAST_NAMES = ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Davies", "Evans",
              "Thomas", "Roberts", "Johnson", "Walker", "Wright", "Green", "Hall", "Wood",
              "Patel", "Khan", "Hussain", "Ahmed", "Ali", "Shah", "Begum", "Malik",
              "Clarke", "Turner", "Hughes", "Edwards", "Bennett", "Cooper", "Ward", "Foster",
              "Gray", "James", "Morris", "Murphy", "Palmer", "Reid", "Russell", "Stone",
              "Baker", "Bell", "Carter", "Dixon", "Ellis", "Fisher", "Gibson", "Hunt",
              "Irving", "Jenkins", "Kelly", "Lewis", "Mason", "Nash", "Owens", "Parker",
              "Quinn", "Rees", "Shaw", "Vaughan"]

POSITIONS = {
    "Practice Clinical": ["Dentist", "Dental Hygienist", "Dental Nurse", "Orthodontist"],
    "Practice Support": ["Practice Receptionist", "Treatment Coordinator", "Practice Administrator"],
    "Practice Partner": ["Practice Partner", "Clinical Director"],
    "HGHQ": ["Payroll Advisor", "HR Business Partner", "Finance Analyst", "IT Support Engineer"],
    "Employee": ["Regional Support Officer", "Compliance Officer"],
}


@dataclass
class Employee:
    payroll_number: str
    personal_reference: str
    practice: str
    category: str
    position_name: str
    basis_list: list
    prior_net: float = None
    current_net: float = None
    elements: dict = field(default_factory=dict)  # name -> (prior, current)
    is_starter: bool = False
    is_leaver: bool = False
    story: str = ""  # scenario tag, for human readability / QA only

    @property
    def tolerance_group(self):
        return PRACTICES[self.practice]

    @property
    def is_zero_hours_only(self):
        return len(self.basis_list) > 0 and all(b == "Zero Hours" for b in self.basis_list)


def _name(rng):
    return rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)


def _pick_practice(rng, group=None):
    pool = [p for p, g in PRACTICES.items() if group is None or g == group]
    return rng.choice(pool)


def _pick_category_and_position(rng, practice):
    if practice == "Hakim Group Head Office":
        cat = "HGHQ"
    else:
        cat = rng.choices(
            ["Practice Clinical", "Practice Support", "Practice Partner", "Employee"],
            weights=[45, 35, 10, 10],
        )[0]
    pos = rng.choice(POSITIONS[cat])
    return cat, pos


def _blank_elements(prior_net, current_net):
    """Build a plausible element breakdown around a given net figure."""
    elements = {}
    for e in ALL_ELEMENTS:
        elements[e] = (0.0, 0.0)
    return elements


def _base_elements(basic_prior, basic_current, gross_prior, gross_current,
                    net_prior, net_current, extra_current=None, extra_prior=None):
    elements = {e: (0.0, 0.0) for e in ALL_ELEMENTS}
    elements["Basic Salary"] = (basic_prior, basic_current)
    elements["Total Gross"] = (gross_prior, gross_current)
    elements["Taxable Gross"] = (round(gross_prior * 0.98, 2), round(gross_current * 0.98, 2))
    elements["Pensionable Pay"] = (round(gross_prior * 0.95, 2), round(gross_current * 0.95, 2))
    elements["Hours Paid"] = (basic_prior / 12 if basic_prior else 0, basic_current / 12 if basic_current else 0)
    elements["Net Pay After Rounding"] = (net_prior, net_current)
    elements["Employer NI"] = (round(gross_prior * 0.138, 2) if gross_prior else 0,
                                round(gross_current * 0.138, 2) if gross_current else 0)
    elements["Employer Pension"] = (round(gross_prior * 0.05, 2) if gross_prior else 0,
                                     round(gross_current * 0.05, 2) if gross_current else 0)
    elements["Apprenticeship Levy"] = (round(gross_prior * 0.005, 2) if gross_prior else 0,
                                        round(gross_current * 0.005, 2) if gross_current else 0)
    if extra_prior:
        for k, v in extra_prior.items():
            p, c = elements[k]
            elements[k] = (v, c)
    if extra_current:
        for k, v in extra_current.items():
            p, c = elements[k]
            elements[k] = (p, v)
    return elements


def build_dataset():
    rng = random.Random(42)
    employees = []
    used_payroll_numbers = set()

    def next_payroll_number():
        while True:
            n = f"P{rng.randint(10000, 99999)}"
            if n not in used_payroll_numbers:
                used_payroll_numbers.add(n)
                return n

    # ---------------------------------------------------------------
    # 1) Stable employees (~30) - movement within tolerance
    # ---------------------------------------------------------------
    for i in range(30):
        practice = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice)
        group = PRACTICES[practice]
        tol = TOLERANCE_BY_GROUP[group]
        base = rng.uniform(1400, 3200)
        move_pct = rng.uniform(-0.9, 0.9) * (tol - 0.02)  # comfortably inside tolerance
        current = round(base * (1 + move_pct), 2)
        payroll_number = next_payroll_number()
        emp = Employee(
            payroll_number=payroll_number,
            personal_reference="PR" + payroll_number[1:],
            practice=practice,
            category=cat,
            position_name=pos,
            basis_list=["Permanent"],
            prior_net=round(base, 2),
            current_net=current,
            elements=_base_elements(round(base * 1.35, 2), round(current * 1.35, 2),
                                     round(base * 1.55, 2), round(current * 1.55, 2),
                                     round(base, 2), current),
            story="stable",
        )
        employees.append(emp)

    # ---------------------------------------------------------------
    # 2) Over-tolerance, real routine causes (~10)
    # ---------------------------------------------------------------
    causes = [
        ("Basic Salary", "salary increase", 0.30, 1),
        ("Bonus", "one-off bonus", 1.0, 1),
        ("Overtime", "overtime spike", 1.2, 1),
        ("Basic Salary", "reduced hours", -0.35, 1),
        ("Mileage Expenses", "expenses claim", 5.0, 1),
        ("SSP", "sick pay", 0.6, 1),
        ("Unsocial Hours Premium", "unsocial hours premium", 2.0, 1),
        ("On Call Allowance", "on-call allowance started", 3.0, 1),
        ("Bonus", "large bonus", 1.0, 1),
        ("Basic Salary", "salary increase (material)", 0.45, 1),
    ]
    for idx, (elem, tag, factor, _) in enumerate(causes):
        practice = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice)
        base = rng.uniform(1600, 2800)
        payroll_number = next_payroll_number()
        elements = _base_elements(round(base * 1.3, 2), round(base * 1.3, 2),
                                   round(base * 1.5, 2), round(base * 1.5, 2),
                                   round(base, 2), round(base, 2))
        prior_elem_amt = round(base * 0.15, 2) if factor > 0 else round(base * 0.5, 2)
        if factor < 0:
            current_elem_amt = round(prior_elem_amt * (1 + factor), 2)
        else:
            current_elem_amt = round(prior_elem_amt + base * factor * 0.4, 2) if elem == "Basic Salary" else round(base * factor * 0.25, 2)
        elements[elem] = (prior_elem_amt, current_elem_amt)
        net_delta = round((current_elem_amt - prior_elem_amt) * 0.75, 2)
        current_net = round(base + net_delta, 2)
        elements["Total Gross"] = (round(base * 1.5, 2), round(base * 1.5 + net_delta / 0.75, 2))
        elements["Net Pay After Rounding"] = (round(base, 2), current_net)
        emp = Employee(
            payroll_number=payroll_number,
            personal_reference="PR" + payroll_number[1:],
            practice=practice, category=cat, position_name=pos,
            basis_list=["Permanent"],
            prior_net=round(base, 2), current_net=current_net,
            elements=elements, story=f"over-tolerance:{tag}",
        )
        employees.append(emp)

    # ---------------------------------------------------------------
    # 3) Starters (~4) - current month only
    # ---------------------------------------------------------------
    starter_records = []
    starter_bases = [rng.uniform(1500, 2600) for _ in range(3)] + [rng.uniform(700, 1200)]
    for i in range(4):
        practice = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice)
        base_current = starter_bases[i]
        payroll_number = next_payroll_number()
        personal_ref = "PR" + payroll_number[1:]
        elements = _base_elements(0, round(base_current * 1.3, 2),
                                   0, round(base_current * 1.5, 2), 0, round(base_current, 2))
        emp = Employee(
            payroll_number=payroll_number, personal_reference=personal_ref,
            practice=practice, category=cat, position_name=pos, basis_list=["Permanent"],
            prior_net=None, current_net=round(base_current, 2), elements=elements,
            is_starter=True, story="starter",
        )
        employees.append(emp)
        starter_records.append(emp)

    # ---------------------------------------------------------------
    # 4) Leavers (~4) - prior month only
    # ---------------------------------------------------------------
    leaver_records = []
    for i in range(4):
        practice = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice)
        base_prior = rng.uniform(1400, 2500)
        payroll_number = next_payroll_number()
        personal_ref = "PR" + payroll_number[1:]
        elements = _base_elements(round(base_prior * 1.3, 2), 0,
                                   round(base_prior * 1.5, 2), 0, round(base_prior, 2), 0)
        emp = Employee(
            payroll_number=payroll_number, personal_reference=personal_ref,
            practice=practice, category=cat, position_name=pos, basis_list=["Permanent"],
            prior_net=round(base_prior, 2), current_net=None, elements=elements,
            is_leaver=True, story="leaver",
        )
        employees.append(emp)
        leaver_records.append(emp)

    # ---------------------------------------------------------------
    # 5) Zero-hours ONLY (~4) - moved to Zero Hours tab regardless of swing
    # ---------------------------------------------------------------
    for i in range(4):
        practice = _pick_practice(rng, group="HG")
        cat, pos = "Practice Support", "Bank Dental Nurse"
        prior = rng.uniform(150, 700)
        swing = rng.uniform(-0.6, 0.9)
        current = round(prior * (1 + swing), 2)
        payroll_number = next_payroll_number()
        elements = _base_elements(round(prior, 2), current, round(prior * 1.05, 2), round(current * 1.05, 2),
                                   round(prior, 2), current)
        emp = Employee(
            payroll_number=payroll_number, personal_reference="PR" + payroll_number[1:],
            practice=practice, category=cat, position_name=pos, basis_list=["Zero Hours"],
            prior_net=round(prior, 2), current_net=current, elements=elements, story="zero-hours-only",
        )
        employees.append(emp)

    # ---------------------------------------------------------------
    # 6) Zero-hours ALONGSIDE permanent contract (~2) - stays on main list
    # ---------------------------------------------------------------
    for i in range(2):
        practice = _pick_practice(rng, group="HG")
        cat, pos = _pick_category_and_position(rng, practice)
        base = rng.uniform(1800, 2600)
        move_pct = rng.uniform(-0.05, 0.08)
        current = round(base * (1 + move_pct), 2)
        payroll_number = next_payroll_number()
        elements = _base_elements(round(base * 1.3, 2), round(current * 1.3, 2),
                                   round(base * 1.5, 2), round(current * 1.5, 2), round(base, 2), current)
        emp = Employee(
            payroll_number=payroll_number, personal_reference="PR" + payroll_number[1:],
            practice=practice, category=cat, position_name=pos,
            basis_list=["Zero Hours", "Permanent"],
            prior_net=round(base, 2), current_net=current, elements=elements,
            story="zero-hours-plus-permanent",
        )
        employees.append(emp)

    # ---------------------------------------------------------------
    # 7) Paired transfers (~2 pairs / 4 records) - same personal_reference,
    #    old payroll number "leaves", new payroll number "starts" - net pay
    #    genuinely moved between two payroll records for the same person.
    # ---------------------------------------------------------------
    for i in range(2):
        practice_old = _pick_practice(rng)
        practice_new = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice_new)
        amount = rng.uniform(1800, 2600)
        shared_personal_ref = "PRTRF" + str(1000 + i)
        old_payroll = next_payroll_number()
        new_payroll = next_payroll_number()
        elements_old = _base_elements(round(amount * 1.3, 2), 0, round(amount * 1.5, 2), 0, round(amount, 2), 0)
        elements_new = _base_elements(0, round(amount * 1.3, 2), 0, round(amount * 1.5, 2), 0, round(amount, 2))
        emp_old = Employee(
            payroll_number=old_payroll, personal_reference=shared_personal_ref,
            practice=practice_old, category=cat, position_name=pos, basis_list=["Permanent"],
            prior_net=round(amount, 2), current_net=None, elements=elements_old,
            is_leaver=True, story="paired-transfer-old",
        )
        emp_new = Employee(
            payroll_number=new_payroll, personal_reference=shared_personal_ref,
            practice=practice_new, category=cat, position_name=pos, basis_list=["Permanent"],
            prior_net=None, current_net=round(amount, 2), elements=elements_new,
            is_starter=True, story="paired-transfer-new",
        )
        employees.extend([emp_old, emp_new])
        leaver_records.append(emp_old)
        starter_records.append(emp_new)

    # ---------------------------------------------------------------
    # 8) High priority: no pay this month, no leaver record on file (genuine
    #    payroll issue - e.g. unpaid leave not processed correctly)
    # ---------------------------------------------------------------
    for i in range(2):
        practice = _pick_practice(rng)
        cat, pos = _pick_category_and_position(rng, practice)
        base = rng.uniform(1800, 2600)
        payroll_number = next_payroll_number()
        elements = _base_elements(round(base * 1.3, 2), 0, round(base * 1.5, 2), 0, round(base, 2), 0)
        emp = Employee(
            payroll_number=payroll_number, personal_reference="PR" + payroll_number[1:],
            practice=practice, category=cat, position_name=pos, basis_list=["Permanent"],
            prior_net=round(base, 2), current_net=0.0, elements=elements,
            story="no-pay-no-leaver",
        )
        employees.append(emp)

    return {
        "employees": employees,
        "starters": starter_records,
        "leavers": leaver_records,
        "period_prior": PRIOR_LABEL,
        "period_current": CURRENT_LABEL,
        "tolerance_by_group": TOLERANCE_BY_GROUP,
        "min_flag_value": MIN_FLAG_VALUE,
        "aggregate_elements": AGGREGATE_ELEMENTS,
        "real_elements": REAL_ELEMENTS,
        "all_elements": ALL_ELEMENTS,
    }


if __name__ == "__main__":
    ds = build_dataset()
    print(f"employees: {len(ds['employees'])}")
    print(f"starters: {len(ds['starters'])}  leavers: {len(ds['leavers'])}")
