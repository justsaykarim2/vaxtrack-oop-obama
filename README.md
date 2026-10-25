# VaxTrack – Vaccination Tracker

**Module:** PROG211 Object-Oriented Programming 1 – Individual Assignment
**Domain:** Health (Vaccination Tracker)
**Language:** Python 3.8+ (standard library only – nothing to install)

VaxTrack helps a clinic or community health team track which anonymous
recipients have received which vaccine doses, enforces the minimum gap between
doses, and reports vaccination coverage.

## How to run

```bash
python Vaxtracker.py --demo   # automatic demonstration
python Vaxtracker.py          # interactive menu
```

## OOP concepts used

| Assignment task | Where in `Vaxtracker.py` |
|---|---|
| **Task 1 – Classes, attributes, objects** | `Vaccine` and `Recipient` (plus manager class `VaccinationTracker`). Each has attributes and methods such as `update_record()` and `display_info()`. Objects interact: `Recipient.update_record()` uses the `Vaccine` schedule. |
| **Task 2 – One data structure** | **Dictionary** only: `recipients` (ID → `Recipient`) and `vaccines` (code → `Vaccine`). Functions `add_record()` and `display_records()` add and display records. |
| **Task 2 – Tuples (bonus)** | `Vaccine.dose_intervals_days` and `Recipient.AGE_GROUPS` are tuples because they are fixed, read-only data. |
| **Task 3 – Instance methods** | `update_record()`, `is_fully_vaccinated()`, `display_info()`, `required_gap_days()` |
| **Task 3 – Class methods** | `Recipient.register()` (alternative constructor) and `Recipient.total_registered()` |
| **Static methods** | `Recipient.is_valid_age()` and `Recipient.age_to_group()` |

## How VaxTrack meets Digital Public Goods (DPG) standards

1. **Open-source** – Published on GitHub under the MIT Licence; anyone can use,
   study, modify and share it.
2. **Inclusive and accessible design** – Plain-text, menu-driven interface with
   clear messages and input validation. It needs only Python and runs on low-spec
   machines with no internet connection, which suits clinics with limited
   infrastructure. Code is simple and commented so it can be translated or adapted.
3. **Privacy-respecting** – No names, addresses, phone numbers or national IDs
   are collected. Recipients get an anonymous ID (e.g. `R-0001`). The exact age is
   used once to select an age group and is **never stored**.
4. **Modular and reusable** – Each class has a single responsibility. New
   vaccines are added with one line (`Vaccine("HPV", "HPV", 2, (180,))`), and the
   classes can be imported into other health projects.

## Example usage (sample input / output)

Command: `python Vaxtracker.py --demo`

```text
VaxTrack DEMO - object creation and interaction

=== Vaccines (4) ===
  [COV] COVID-19 | doses: 2 | gaps (days): 28
  [MR] Measles-Rubella | doses: 2 | gaps (days): 180
  [OPV] Oral Polio | doses: 3 | gaps (days): 28, 28
  [YF] Yellow Fever | doses: 1 | gaps (days): n/a

-- Recording doses (fixed dates for a repeatable demo) --
  OK   Dose 1/3 of Oral Polio recorded for R-0001.
  FAIL Too early. Next Oral Polio dose is allowed from 2026-09-29.
  OK   Dose 2/3 of Oral Polio recorded for R-0001.
  OK   Dose 1/2 of COVID-19 recorded for R-0003.
  OK   Dose 2/2 of COVID-19 recorded for R-0003.
  FAIL R-0003 already completed COVID-19.
  OK   Dose 1/1 of Yellow Fever recorded for R-0004.
  FAIL Recipient ID not found.

=== Recipients (4) ===
  R-0001 | age group: 0-4
      OPV: 2 dose(s), last on 2026-09-29
  R-0002 | age group: 5-17
      no doses recorded
  R-0003 | age group: 18-59
      COV: 2 dose(s), last on 2026-10-03
  R-0004 | age group: 60+
      YF: 1 dose(s), last on 2026-09-12

=== Coverage: COVID-19 ===
  Registered: 4 | Started: 1 | Fully vaccinated: 1 (25.0%)

=== Coverage: Yellow Fever ===
  Registered: 4 | Started: 1 | Fully vaccinated: 1 (25.0%)

Total recipients registered (class method): 4
```

Interactive session (menu option 1 then 2):

```text
Choose: 1
Age (used only to find age group): 25
Registered anonymous ID: R-0001 (age group 18-59)
Choose: 2
Recipient ID (e.g. R-0001): R-0001
Vaccine code (COV, MR, OPV, YF): cov
Date YYYY-MM-DD (blank = today): 2026-10-01
Dose 1/2 of COVID-19 recorded for R-0001.
```

## Files

- `Vaxtracker.py` – source code
- `README.md` – this document
- `LICENSE` – MIT Licence

## Author

Abdul Karim Obama Jalloh – Student ID: 905006394 – PROG211, Semester 03 (Sept 2026 – Feb 2027)
