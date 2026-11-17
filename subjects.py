"""Subject catalog management."""
from config import SUBJECTS_FILE
from storage import read_records, write_records, append_record
from interface import ask, message, print_table

FIELDS = ["subject_code", "subject_name", "units"]

def get_subjects():
    """Load all subjects from subjects.txt."""
    return read_records(SUBJECTS_FILE, FIELDS)

def show_subjects(records=None):
    """Display the subject catalog."""
    records = get_subjects() if records is None else records
    print_table(["Code", "Subject name", "Units"],
                [[r["subject_code"], r["subject_name"], r["units"]] for r in records])

def add_subject():
    """Add a subject after checking that its subject code is unique."""
    records = get_subjects()
    code = ask("Subject code: ").upper()
    if any(r["subject_code"].upper() == code for r in records):
        message("Subject code already exists.", "error")
        return
    name = ask("Subject name: ")
    units = ask("Units (number): ")
    try:
        if int(units) <= 0:
            raise ValueError
    except ValueError:
        message("Units must be a positive whole number.", "error")
        return
    if append_record(SUBJECTS_FILE, FIELDS,
                     {"subject_code": code, "subject_name": name, "units": units}):
        message("Subject saved.", "success")

def search_subject():
    """Search subjects by code or subject name."""
    keyword = ask("Search subject: ").lower()
    matches = [r for r in get_subjects()
               if keyword in r["subject_code"].lower() or keyword in r["subject_name"].lower()]
    show_subjects(matches)
