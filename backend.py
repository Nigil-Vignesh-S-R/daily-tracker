import sqlite3
import os
import datetime as dt
def resource_path(relative_path):
    import sys
    base_path=getattr(sys,"_MEIPASS",os.path.abspath("."))
    return os.path.join(base_path,relative_path)
class Database:
    def __init__(self,db_path=None):
        if db_path is None:
            if getattr(__import__("sys"),'frozen',False):
                base_dir=os.path.join(os.environ["LOCALAPPDATA"],"DailyTracker")
            else:
                base_dir=os.path.dirname(os.path.abspath(__file__))
            os.makedirs(base_dir,exist_ok=True)
            db_path=os.path.join(base_dir,"dailytracker.db")
        self.db_path=db_path
        self.connection=None
        self.cursor=None
    def connect(self):
        try:
            self.connection=sqlite3.connect(self.db_path,check_same_thread=False)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor=self.connection.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Connection error: {str(e)}")
    def create_tables(self):
        self.cursor.executescript("""
                                CREATE TABLE IF NOT EXISTS habits(
                                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    habit_name TEXT NOT NULL UNIQUE,
                                    created_at DATE NOT NULL DEFAULT(DATE('now'))
                                );
                                CREATE TABLE IF NOT EXISTS notes(
                                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date DATE NOT NULL DEFAULT(DATE('now')),
                                    note TEXT NOT NULL,
                                    UNIQUE(date)
                                );
                                CREATE TABLE IF NOT EXISTS daily_log(
                                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date DATE NOT NULL DEFAULT(DATE('now')),
                                    habit_id INTEGER NOT NULL,
                                    completed INTEGER NOT NULL,

                                    UNIQUE (habit_id,date),
                                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
                                );""")
        self.connection.commit()
    def add_habit(self,habit_name):
        try:
            query="""INSERT INTO habits (habit_name) VALUES(?)"""
            self.cursor.execute(query,(habit_name,))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Habit:{str(e)}")
            return None
    def get_habits(self):
        query="""SELECT habit_id,habit_name from habits ORDER BY habit_id"""
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        return rows
    def delete_habit(self,habit_id):
        try:
            query="""DELETE FROM habits WHERE habit_id =(?)"""
            self.cursor.execute(query,(habit_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting Habit:{str(e)}")
            return False
    def save_note(self,note_text,note_date=None):
        if note_date is None:
            note_date=dt.date.today()
        try:
            query="""INSERT INTO notes (note,date)
                    VALUES (?,?)
                    ON CONFLICT(date) DO UPDATE SET note = excluded.note"""
            self.cursor.execute(query,(note_text,note_date))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error Saving Note: {str(e)}")
            return False
    def get_note(self,note_date=None):
        if note_date is None:
            note_date=dt.date.today()
        try:
            query="""SELECT note FROM notes WHERE date = ?"""
            self.cursor.execute(query,(note_date,))
            row=self.cursor.fetchone()
            return row[0] if row else ""
        except sqlite3.Error as e:
            print(f"Error Fetching Note: {str(e)}")
            return ""
    def mark_completed(self,habit_id,completed,log_date=None):
        if log_date is None :
            log_date=dt.date.today()
        try:
            query="""INSERT INTO daily_log(habit_id,date,completed)
                     VALUES (?,?,?)
                     ON CONFLICT(habit_id,date) DO UPDATE SET completed= excluded.completed"""
            self.cursor.execute(query,(habit_id,log_date,int(completed)))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"error makring completion: {str(e)}")
            return False
    def get_month_completion(self,year,month):
        try:
            query="""SELECT habit_id,date,completed FROM daily_log
                     WHERE strftime('%Y',date)=? and strftime('%m',date)=?"""
            self.cursor.execute(query,(f"{year:04d}",f"{month:02d}"))
            rows=self.cursor.fetchall()
            return[
                (habit_id,dt.date.fromisoformat(log_date),bool(completed))
                for habit_id,log_date,completed in rows
            ]
        except sqlite3.Error as e:
            print(f"Error Fetching Completions: {str(e)}")
            return[]
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()