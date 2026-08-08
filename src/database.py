import sqlite3
import os


class EchoDatabase:

    def __init__(self, db_path="database/echo.db"):

        os.makedirs("database", exist_ok=True)

        self.conn = sqlite3.connect(db_path)

        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera_id TEXT,

            frame INTEGER,

            timestamp TEXT,

            timestamp_seconds REAL,

            track_id INTEGER,

            class TEXT,

            confidence REAL,

            crop_path TEXT,

            x1 INTEGER,
            y1 INTEGER,
            x2 INTEGER,
            y2 INTEGER

        )
        """)

        self.conn.commit()

    def insert_detection(
        self,
        camera_id,
        frame,
        timestamp,
        timestamp_seconds,
        track_id,
        class_name,
        confidence,
        crop_path,
        x1,
        y1,
        x2,
        y2
    ):

        self.cursor.execute("""
        INSERT INTO detections(

            camera_id,
            frame,
            timestamp,
            timestamp_seconds,
            track_id,
            class,
            confidence,
            crop_path,
            x1,
            y1,
            x2,
            y2

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            camera_id,
            frame,
            timestamp,
            timestamp_seconds,
            track_id,
            class_name,
            confidence,
            crop_path,
            x1,
            y1,
            x2,
            y2

        ))

        self.conn.commit()

    def close(self):

        self.conn.close()