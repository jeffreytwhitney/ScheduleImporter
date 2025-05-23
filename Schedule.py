import os

import xlwings

from ScheduleConfigs import ScheduleConfig


class ScheduleFileNotFoundError(Exception):
    pass

class ScheduleBadHeadersError(Exception):
    pass


class Schedule:
    _schedule_config: ScheduleConfig
    _excel_application: xlwings.App
    _workbook: xlwings.Book
    _sheet: xlwings.Sheet
    _partnumber_cell: xlwings.Range
    _completion_date_cell: xlwings.Range
    _used_range: xlwings.Range
    _valid_part_delimiters = []
    _machine_name: str

    def __init__(self, schedule_config: ScheduleConfig):
        self._schedule_config = schedule_config
        self._load_schedule()

    def __exit__(self):
        self._workbook.close()
        self._excel_application.quit()

    def _load_schedule(self):
        filepath = self._schedule_config.file_path
        sheetname = self._schedule_config.sheet_name
        partnumber_address = self._schedule_config.starting_cell_address
        completion_offset = self._schedule_config.completion_date_cell_offset

        if not os.path.isfile(filepath):
            raise ScheduleFileNotFoundError(self._schedule_config.file_path)

        xlapp = xlwings.App(visible=False)
        xlbook = xlwings.Book(filepath)
        xlsheet = xlbook.sheets[sheetname]
        xlpartRange = xlsheet.range(partnumber_address)
        xlcompletionRange = xlpartRange.offset(0, completion_offset)
        self._excel_application = xlapp
        self._workbook = xlbook
        self._sheet = xlsheet
        self._partnumber_cell = xlpartRange
        self._completion_date_cell = xlcompletionRange
        self._used_range = xlsheet.used_range
        if self.is_part_number_delimiter and self.is_completion_date_delimiter:
            machine_offset_left = int(self._schedule_config.machine_name_offset_left)
            machine_offset_up = int(self._schedule_config.machine_name_offset_up)
            machine_name_cell = self._partnumber_cell.offset(machine_offset_up, machine_offset_left)
            self._machine_name = machine_name_cell.value
        else:
            raise ScheduleBadHeadersError(self._schedule_config.file_path)


    @property
    def partnumber_value(self):
        return self._partnumber_cell.value

    @property
    def completion_date_value(self):
        return self._completion_date_cell.value

    @property
    def row_count(self):
        return self._used_range.rows.count

    @property
    def partnumber_cell(self):
        return self._partnumber_cell

    @property
    def completion_date_cell(self):
        return self._completion_date_cell

    @property
    def is_part_number_delimiter(self) -> bool:
        return self.partnumber_value in self._valid_part_delimiters

    @property
    def is_completion_date_delimiter(self) -> bool:
        return self.completion_date_value == self._schedule_config.completion_date_delimiter

    def offset(self):
        self._partnumber_cell = self._partnumber_cell.offset(1, 0)
        self._completion_date_cell = self._completion_date_cell.offset(1, 0)

        if self.is_part_number_delimiter and self.is_completion_date_delimiter:
            machine_offset_left = int(self._schedule_config.machine_name_offset_left)
            machine_offset_up = int(self._schedule_config.machine_name_offset_up)
            machine_name_cell = self._partnumber_cell.offset(machine_offset_up, machine_offset_left)
            self._machine_name = machine_name_cell.value
