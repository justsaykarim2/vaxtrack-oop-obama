"""
VaxTrack - A privacy-respecting Vaccination Tracker
PROG211 Object-Oriented Programming 1 - Individual Assignment

Domain : Health (Vaccination Tracker)
Concepts:
  Task 1 - Two classes (Vaccine, Recipient) + a manager class (VaccinationTracker)
  Task 2 - ONE data structure: dictionary (records stored by unique ID as key)
           Tuples are also used for fixed, read-only data (bonus).
  Task 3 - Instance methods, class methods (@classmethod), static methods
DPG    : Open-source, inclusive, privacy-respecting (no names / no sensitive
         data - only anonymous IDs and age groups), modular and reusable.

Run:  python vaxtrack.py          (interactive menu)
      python vaxtrack.py --demo   (automatic demonstration)
"""

import sys
from datetime import date, timedelta


# ----------------------------------------------------------------------
# TASK 2 - Simple functions to ADD and DISPLAY records in the dictionary
# ----------------------------------------------------------------------
def add_record(store, key, record):
    """Add a record to a dictionary store. Returns False if key exists."""
    if key in store:
        return False
    store[key] = record
    return True


def display_records(store, title):
    """Loop through a dictionary store and display every record."""
    print(f"\n=== {title} ({len(store)}) ===")
    if not store:
        print("  (no records yet)")
        return
    for record in store.values():
        record.display_info()


# ----------------------------------------------------------------------
# TASK 1 - CLASS 1: Vaccine
# ----------------------------------------------------------------------
class Vaccine:
    """A vaccine and its dosing schedule."""

    def __init__(self, code, name, doses_required, dose_intervals_days=()):
        self.code = code.upper()
        self.name = name
        self.doses_required = doses_required
        # Tuple: the schedule is fixed and must not be changed after creation.
        # Needs (doses_required - 1) gaps, e.g. 3 doses -> (28, 28)
        self.dose_intervals_days = tuple(dose_intervals_days)

    # Instance method
    def required_gap_days(self, doses_received):
        """Minimum days needed since the last dose before the next one."""
        if doses_received == 0 or doses_received >= self.doses_required:
            return 0
        return self.dose_intervals_days[doses_received - 1]

    # Instance method
    def display_info(self):
        gaps = ", ".join(str(d) for d in self.dose_intervals_days) or "n/a"
        print(f"  [{self.code}] {self.name} | doses: {self.doses_required} "
              f"| gaps (days): {gaps}")


# ----------------------------------------------------------------------
# TASK 1 - CLASS 2: Recipient (anonymous - DPG privacy principle)
# ----------------------------------------------------------------------
class Recipient:
    """An anonymous vaccine recipient. No name, address or exact age stored."""

    # Class attribute shared by all recipients
    _total_registered = 0
    # Tuple of tuples: fixed age-group boundaries (min_age, max_age, label)
    AGE_GROUPS = ((0, 4, "0-4"), (5, 17, "5-17"), (18, 59, "18-59"),
                  (60, 120, "60+"))

    def __init__(self, recipient_id, age_group):
        self.recipient_id = recipient_id
        self.age_group = age_group
        # vaccine code -> {"count": int, "last_date": date}
        self.doses = {}
        Recipient._total_registered += 1

    # ---- Class methods -------------------------------------------------
    @classmethod
    def register(cls, age):
        """Alternative constructor: build a Recipient from an age.
        The exact age is used once to find the age group, then discarded."""
        if not cls.is_valid_age(age):
            raise ValueError("Age must be a whole number between 0 and 120.")
        new_id = f"R-{cls._total_registered + 1:04d}"
        return cls(new_id, cls.age_to_group(age))

    @classmethod
    def total_registered(cls):
        return cls._total_registered

    # ---- Static methods (do not need the object or class) -------------
    @staticmethod
    def is_valid_age(age):
        return isinstance(age, int) and 0 <= age <= 120

    @staticmethod
    def age_to_group(age):
        for low, high, label in Recipient.AGE_GROUPS:
            if low <= age <= high:
                return label
        return "unknown"

    # ---- Instance methods ----------------------------------------------
    def update_record(self, vaccine, dose_date):
        """Record one dose of `vaccine` given on `dose_date`.
        Interaction between objects: uses the Vaccine's schedule rules.
        Returns (success, message)."""
        entry = self.doses.get(vaccine.code, {"count": 0, "last_date": None})

        if entry["count"] >= vaccine.doses_required:
            return False, f"{self.recipient_id} already completed {vaccine.name}."

        gap = vaccine.required_gap_days(entry["count"])
        if entry["last_date"] is not None:
            earliest = entry["last_date"] + timedelta(days=gap)
            if dose_date < earliest:
                return False, (f"Too early. Next {vaccine.name} dose is allowed "
                               f"from {earliest.isoformat()}.")

        entry["count"] += 1
        entry["last_date"] = dose_date
        self.doses[vaccine.code] = entry
        return True, (f"Dose {entry['count']}/{vaccine.doses_required} of "
                      f"{vaccine.name} recorded for {self.recipient_id}.")

    def is_fully_vaccinated(self, vaccine):
        entry = self.doses.get(vaccine.code)
        return bool(entry) and entry["count"] >= vaccine.doses_required

    def display_info(self):
        print(f"  {self.recipient_id} | age group: {self.age_group}")
        if not self.doses:
            print("      no doses recorded")
        for code, entry in self.doses.items():
            print(f"      {code}: {entry['count']} dose(s), "
                  f"last on {entry['last_date'].isoformat()}")


# ----------------------------------------------------------------------
# Manager class: holds the dictionaries and coordinates the objects
# ----------------------------------------------------------------------
class VaccinationTracker:
    """Modular, reusable manager. Uses dictionaries keyed by unique ID/code."""

    def __init__(self):
        self.vaccines = {}     # code -> Vaccine
        self.recipients = {}   # recipient_id -> Recipient

    def add_vaccine(self, vaccine):
        return add_record(self.vaccines, vaccine.code, vaccine)

    def add_recipient(self, recipient):
        return add_record(self.recipients, recipient.recipient_id, recipient)

    def record_dose(self, recipient_id, vaccine_code, dose_date=None):
        recipient = self.recipients.get(recipient_id.upper())
        vaccine = self.vaccines.get(vaccine_code.upper())
        if recipient is None:
            return False, "Recipient ID not found."
        if vaccine is None:
            return False, "Vaccine code not found."
        return recipient.update_record(vaccine, dose_date or date.today())

    def coverage_report(self, vaccine_code):
        vaccine = self.vaccines.get(vaccine_code.upper())
        if vaccine is None:
            print("Vaccine code not found.")
            return
        total = len(self.recipients)
        started = full = 0
        for recipient in self.recipients.values():
            if vaccine.code in recipient.doses:
                started += 1
            if recipient.is_fully_vaccinated(vaccine):
                full += 1
        pct = (full / total * 100) if total else 0.0
        print(f"\n=== Coverage: {vaccine.name} ===")
        print(f"  Registered: {total} | Started: {started} | "
              f"Fully vaccinated: {full} ({pct:.1f}%)")

    def display_vaccines(self):
        display_records(self.vaccines, "Vaccines")

    def display_recipients(self):
        display_records(self.recipients, "Recipients")


# ----------------------------------------------------------------------
# Program setup, demo and interactive menu
# ----------------------------------------------------------------------
def load_default_vaccines(tracker):
    tracker.add_vaccine(Vaccine("COV", "COVID-19", 2, (28,)))
    tracker.add_vaccine(Vaccine("MR", "Measles-Rubella", 2, (180,)))
    tracker.add_vaccine(Vaccine("OPV", "Oral Polio", 3, (28, 28)))
    tracker.add_vaccine(Vaccine("YF", "Yellow Fever", 1))


def demo():
    print("VaxTrack DEMO - object creation and interaction")
    tracker = VaccinationTracker()
    load_default_vaccines(tracker)
    tracker.display_vaccines()

    # Object creation using the class method
    for age in (2, 10, 34, 67):
        tracker.add_recipient(Recipient.register(age))

    print("\n-- Recording doses (fixed dates for a repeatable demo) --")
    steps = (
        ("R-0001", "OPV", date(2026, 9, 1)),
        ("R-0001", "OPV", date(2026, 9, 10)),   # too early -> rejected
        ("R-0001", "OPV", date(2026, 9, 29)),   # allowed
        ("R-0003", "COV", date(2026, 9, 5)),
        ("R-0003", "COV", date(2026, 10, 3)),   # completes the course
        ("R-0003", "COV", date(2026, 10, 20)),  # already complete
        ("R-0004", "YF", date(2026, 9, 12)),
        ("R-0099", "YF", date(2026, 9, 12)),    # unknown ID
    )
    for rid, code, when in steps:
        ok, msg = tracker.record_dose(rid, code, when)
        print(f"  {'OK  ' if ok else 'FAIL'} {msg}")

    tracker.display_recipients()
    tracker.coverage_report("COV")
    tracker.coverage_report("YF")
    print(f"\nTotal recipients registered (class method): "
          f"{Recipient.total_registered()}")


def ask_date(prompt):
    """Ask for a date; blank means today."""
    text = input(prompt).strip()
    if not text:
        return date.today()
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def menu():
    tracker = VaccinationTracker()
    load_default_vaccines(tracker)
    options = (
        "1. Register recipient",
        "2. Record a dose",
        "3. View all recipients",
        "4. View vaccines",
        "5. Coverage report",
        "0. Exit",
    )
    while True:
        print("\n--- VaxTrack (no personal data stored) ---")
        for line in options:
            print(line)
        choice = input("Choose: ").strip()

        if choice == "1":
            try:
                age = int(input("Age (used only to find age group): "))
                recipient = Recipient.register(age)
                tracker.add_recipient(recipient)
                print(f"Registered anonymous ID: {recipient.recipient_id} "
                      f"(age group {recipient.age_group})")
            except ValueError as err:
                print(f"Invalid input: {err}")
        elif choice == "2":
            rid = input("Recipient ID (e.g. R-0001): ").strip()
            code = input("Vaccine code (COV, MR, OPV, YF): ").strip()
            when = ask_date("Date YYYY-MM-DD (blank = today): ")
            if when is None:
                print("Invalid date format.")
            else:
                print(tracker.record_dose(rid, code, when)[1])
        elif choice == "3":
            tracker.display_recipients()
        elif choice == "4":
            tracker.display_vaccines()
        elif choice == "5":
            tracker.coverage_report(input("Vaccine code: ").strip())
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        menu()