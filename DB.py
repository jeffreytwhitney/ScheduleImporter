from typing import List, Dict, Any

import pymssql


class DatabaseConnection:
    DB_SERVER = 'rms-corplfsql1.cretexinc.com'
    DB_USER = 'MPMUser'
    DB_PASSWORD = 'W5c~VYg3u^k*ULtehRzD?x'
    DB_NAME = 'LF_RMS_COMMS_MPM'

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymssql.connect(
            server=self.DB_SERVER,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
            as_dict=True
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def fetch_records(self, sql: str) -> List[Dict[str, Any]]:
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute_statement(self, sql: str) -> None:
        self.cursor.execute(sql)
        self.conn.commit()


def get_sql_recordset(sql: str) -> List[Dict[str, Any]]:
    with DatabaseConnection() as db:
        return db.fetch_records(sql)


def execute_sql_statement(sql: str) -> None:
    with DatabaseConnection() as db:
        db.execute_statement(sql)
