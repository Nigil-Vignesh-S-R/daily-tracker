import os
from dotenv import load_dotenv
import mysql.connector as myc
from mysql.connector import Error
import datetime as dt
load_dotenv()
class Database:
    def __init__(self):
        self.host=os.getenv("DB_HOST")
        self.user=os.getenv("DB_USER")
        self.password=os.getenv("DB_PASSWORD")
        self.database=os.getenv("DB_NAME")
        self.port=int(os.getenv("DB_PORT"))
        self.connection=None
        self.cursor=None
    def connect(self):
        try:
            #print("before connect")
            self.connection=myc.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                use_pure=True
            )
            #print("after connect")
            if self.connection.is_connected():
            #    print("Connected")
                self.cursor=self.connection.cursor()
            #    print("connected to mysql")
        except Error as e:
            print(f"Connection Error{e}")
            raise
    def add_habit(self,habit_name):
        try:
            query="INSERT INTO habits (habit_name) VALUES(%s)"
            self.cursor.execute(query,(habit_name,))
            self.connection.commit()
            #print("habit added Succesfully")
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding habit: {e}")
            return None
    def get_habits(self):
        query="SELECT habit_id,habit_name from habits ORDER BY habit_id"
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        return rows
    def update_habit(self):
        pass
    def delete_habit(self,habit_id):
        try:
            query="DELETE FROM habits where habit_id=%s"
            self.cursor.execute(query,(habit_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting habit: {str(e)}")
            return False
    def save_note(self,note_text,note_date=None):
        if note_date is None:
            note_date=dt.date.today()
        try:
            query="""INSERT INTO notes (date,note)
                  VALUES(%s,%s)
                  ON DUPLICATE KEY UPDATE note=(%s)"""
            self.cursor.execute(query,(note_date,note_text,note_text))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error saving Note:{str(e)}")
            return False
    def get_note(self,note_date=None):
        if note_date is None:
            note_date=dt.date.today()
        try:
            query="SELECT note FROM notes WHERE date=(%s)"
            self.cursor.execute(query,(note_date,))
            row=self.cursor.fetchone()
            return row[0] if row else ""
        except Error as e:
            print(f"Error in Fetching notes: {str(e)}")
            return ""
    def mark_completed(self,habit_id,completed,log_date=None):
        if log_date is None:
            log_date=dt.date.today()
        try:
            query="""INSERT INTO daily_log(habit_id,date,completed)
                     VALUES(%s,%s,%s)
                     ON DUPLICATE KEY UPDATE completed=%s"""
            self.cursor.execute(query,(habit_id,log_date,completed,completed))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error marking completion {str(e)}")
            return False
    def get_month_completion(self,year,month):
        try:
            query="""SELECT habit_id,date,completed from daily_log
                     WHERE YEAR(date)=%s and MONTH(date)=%s"""
            self.cursor.execute(query,(year,month))
            rows=self.cursor.fetchall()
            return  rows
        except Error as e:
            print(f"Error Fetching Completions: {str(e)}")
            return[]
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
           #print("connection Closed.")
if __name__=="__main__":
    db=Database()
    db.connect()
    #new_id=db.add_habit("test habit")
    #print(f"habit id: {new_id}")
    #print(db.get_habits())
    db.close_connection()