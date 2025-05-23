from dataclasses import dataclass

import DB


@dataclass
class TaskScheduleLinkRecord:
    task_id: int
    linked_table_name_id: int
    machine_name: str
    site_id: int


class TaskScheduleLinkRecordWriter:
    def __init__(self):
        self._records = []

    def add_task_schedule_link_record(self, task_id: int, linked_table_name_id: int, machine_name: str, site_id: int):
        self._records.append(TaskScheduleLinkRecord(task_id, linked_table_name_id, machine_name, site_id))

    def write_records_to_database(self):
        for record in self._records:
            DB.execute_sql_statement(
                "INSERT INTO tblTaskScheduleData (TaskID, LinkedTableNameID, MachineName, SiteID) VALUES ('{task_id}', '{linked_table_name_id}', '{machine_name}', {site_id})".format(
                    task_id=record.task_id,
                    linked_table_name_id=record.linked_table_name_id,
                    machine_name=record.machine_name,
                    site_id=record.site_id
                )
            )
