
"""Simple pipe-delimited TXT file storage helpers."""
import csv
from config import DATA_DIR


def ensure_data_files():
    """Create the data folder and required TXT files if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in ("users.txt", "students.txt", "subjects.txt", "grades.txt"):
        path = DATA_DIR / filename

        if not path.exists():
            path.touch()


def read_records(path, fields):
    """Read a TXT database and return its rows as dictionaries."""
    records = []

    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(
                file,
                fieldnames=fields,
                delimiter="|"
            )

            for row in reader:
                if row and all(row.get(field) is not None for field in fields):
                    records.append(row)

    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    except OSError as error:
        print(f"\n[FILE ERROR] Could not read {path.name}: {error}")

    return records


def write_records(path, fields, records):
    """Replace a TXT database with the supplied list of dictionaries."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fields,
                delimiter="|",
                lineterminator="\n",
                extrasaction="ignore"
            )

            for record in records:
                writer.writerow({
                    field: str(record.get(field, ""))
                    for field in fields
                })

        return True

    except OSError as error:
        print(f"\n[FILE ERROR] Could not write {path.name}: {error}")
        return False


def append_record(path, fields, record):
    """Append one record to a TXT database."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fields,
                delimiter="|",
                lineterminator="\n",
                extrasaction="ignore"
            )

            writer.writerow({
                field: str(record.get(field, ""))
                for field in fields
            })

        return True

    except OSError as error:
        print(f"\n[FILE ERROR] Could not append to {path.name}: {error}")
        return False
