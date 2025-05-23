from dataclasses import dataclass
from datetime import datetime

import DB


@dataclass
class ImportRecord:
    task_name: str
    due_date: datetime
    site_id: int


class ImportRecordWriter:
    def __init__(self):
        self._records = []

    def add_import_record(self, task_name: str, due_date: datetime, site_id: int):
        existing_records = [record for record in self._records if record.task_name == task_name]
        if not existing_records:
            self._records.append(ImportRecord(task_name, due_date, site_id))
        else:
            existing_due_date = existing_records[0].due_date
            if due_date < existing_due_date:
                existing_records[0].due_date = due_date

    def write_records_to_database(self):
        for record in self._records:
            DB.execute_sql_statement(
                "INSERT INTO tblImport (TaskName, DueDate, SiteID) VALUES ('{task_name}', '{due_date}', {site_id})".format(
                    task_name=record.task_name,
                    due_date=record.due_date,
                    site_id=record.site_id
                )
            )
