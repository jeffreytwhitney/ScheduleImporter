import ScheduleConfigs
from ImportRecords import ImportRecordWriter
import Schedule
from ScheduleRun import ScheduleRun
from TaskScheduleLinkRecords import TaskScheduleLinkRecordWriter
from Tasks import TaskWriter


def process_schedules():
    schedule_configs = ScheduleConfigs.get_scheduleconfigs()
    schedule_run = ScheduleRun()
    task_writer = TaskWriter
    import_record_writer = ImportRecordWriter
    task_schedule_link_writer = TaskScheduleLinkRecordWriter
    for config in schedule_configs:
        try:
            with Schedule.Schedule(config) as schedule:
                _process_schedule(schedule, task_writer, import_record_writer, task_schedule_link_writer)
        except Schedule.ScheduleBadHeadersError:
            error_message = f"The headers (columns) for schedule {config.schedule_id} have change. Cannot process file."
            _write_error_to_db(schedule_run.schedule_run_id, config.schedule_id, error_message)
        except Schedule.ScheduleFileNotFoundError:
            error_message = f"Could not find file for schedule {config.schedule_id}."
            _write_error_to_db(schedule_run.schedule_run_id, config.schedule_id, error_message)
        except Exception:
            error_message = f"Schedule {config.schedule_id} failed to update."
            _write_error_to_db(schedule_run.schedule_run_id, config.schedule_id, error_message)


def _process_schedule(schedule, task_writer, import_record_writer, task_schedule_link_writer):
    for i in range(1, schedule.row_count):
        print(i)


def _write_error_to_db(runid, schedule_id, error_message: str):
    pass


def _write_log_to_db(runid, schedule_id, log_message: str):
    pass


if __name__ == '__main__':
    process_schedules()
