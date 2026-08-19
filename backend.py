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
            self.backfill_sort_order()
        except sqlite3.Error as e:
            print(f"Connection error: {str(e)}")
    def update_habit_order(self,ordered_habit_ids):
        try:
            for index,habit_id in enumerate(ordered_habit_ids):
                self.cursor.execute("UPDATE habits SET sort_order=? WHERE habit_id=?",(index,habit_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating habit order: {str(e)}")
            return False
    def backfill_sort_order(self):
        already_done=self.get_setting("sort_order_backfilled")
        if already_done=="1":
            return
        self.cursor.execute("""SELECT COUNT(*) FROM habits WHERE sort_order = 0""")
        if self.cursor.fetchone()[0]>0:
            self.cursor.execute("""SELECT habit_id FROM habits ORDER BY habit_id""")
            for index,(habit_id,) in enumerate(self.cursor.fetchall()):
                self.cursor.execute("""UPDATE habits SET sort_order = ? WHERE habit_id=?""",
                                    (index,habit_id))
            self.connection.commit()
        self.save_setting("sort_order_backfilled","1")
    def create_tables(self):
        self.cursor.executescript("""
                                CREATE TABLE IF NOT EXISTS habits(
                                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    habit_name TEXT NOT NULL UNIQUE,
                                    created_at DATE NOT NULL DEFAULT(DATE('now')),
                                    sort_order INTEGER NOT NULL DEFAULT 0
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
                                );
                                CREATE TABLE IF NOT EXISTS settings(
                                key TEXT PRIMARY KEY,
                                value TEXT NOT NULL
                                );""")
        self.connection.commit()
    def add_habit(self,habit_name):
        try:
            self.cursor.execute("SELECT COALESCE(MAX(sort_order),-1)+1 FROM habits")
            next_order =self.cursor.fetchone()[0]
            query="""INSERT INTO habits (habit_name,sort_order) VALUES(?,?)"""
            self.cursor.execute(query,(habit_name,next_order))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Habit:{str(e)}")
            return None
    def get_habits(self):
        query="""SELECT habit_id,habit_name,created_at from habits ORDER BY sort_order"""
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        return [
            (habit_id,habit_name,dt.date.fromisoformat(created_at))
            for habit_id,habit_name, created_at in rows
        ]
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
    def get_completed_dates(self):
        try:
            query="""SELECT DISTINCT date from daily_log
                     WHERE completed=1
                     ORDER BY date DESC"""
            self.cursor.execute(query)
            rows=self.cursor.fetchall()
            return [dt.date.fromisoformat(row[0]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error Fetching Completed Dates: {str(e)}")
            return []
    def get_setting(self,key,default=None):
        try:
            query="""SELECT value FROM settings WHERE key=?"""
            self.cursor.execute(query,(key,))
            row=self.cursor.fetchone()
            return row[0] if row else default
        except sqlite3.Error as e:
            print(f"Error fetching setting: {str(e)}")
            return default
    def save_setting(self,key,value):
        try:
            query="""INSERT INTO settings(key,value)
                     VALUES(?,?)
                     ON CONFLICT(key) DO UPDATE SET value=excluded.value"""
            self.cursor.execute(query,(key,value))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving setting: {str(e)}")
            return False
    def update_habits(self,habit_name,habit_id):
        try:
            query="""UPDATE habits SET habit_name=? where habit_id=?"""
            self.cursor.execute(query,(habit_name,habit_id))
            self.connection.commit()
        except sqlite3.Error as e:
            pass
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
if __name__ == "__main__":
    db=Database()
    db.connect()
    print(db.get_habits())