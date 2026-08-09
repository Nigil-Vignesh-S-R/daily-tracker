from PyQt5.QtCore import QThread,pyqtSignal
from backend import Database
class DBConnectWorker(QThread):
    connected=pyqtSignal(bool,str)
    def __init__(self,db:Database):
        super().__init__()
        self.db=db
    def run(self):
        try:
            self.db.connect()
            self.connected.emit(True,"")
        except Exception as e:
            self.connected.emit(False,str(e))
class addHabitWorker(QThread):
    completed=pyqtSignal(bool,str,int,str)
    def __init__(self,db:Database,habit_name):
        super().__init__()
        self.db=db
        self.habitName=habit_name
    def run(self):
        try:
            new_id=self.db.add_habit(self.habitName)
            if new_id:
                self.completed.emit(True,"",new_id,self.habitName)
            else:
                self.completed.emit(False,"Failed to add Habit",0,self.habitName)
        except Exception as e:
            self.completed.emit(False,str(e),0,self.habitName)
class getHabitWorker(QThread):
    fetched=pyqtSignal(bool,str,list)
    def __init__(self,db:Database):
        super().__init__()
        self.db=db
    def run(self):
        try:
            habits=self.db.get_habits()
            self.fetched.emit(True,"",habits)
        except Exception as e:
            self.fetched.emit(False,str(e),[])
class deleteHabitWorker(QThread):
    deleted=pyqtSignal(bool,str,int)
    def __init__(self,db:Database,habit_id):
        super().__init__()
        self.db=db
        self.habitID=habit_id
    def run(self):
        try:
            success=self.db.delete_habit(self.habitID)
            if success:
                self.deleted.emit(True,"",self.habitID)
            else:
                self.deleted.emit(False,"Failed to delete habit",self.habitID)
        except Exception as e:
            self.deleted.emit(False,str(e),self.habitID)
class saveNoteWorker(QThread):
    completed=pyqtSignal(bool,str)
    def __init__(self,db:Database,notes_text):
        super().__init__()
        self.db=db
        self.notes_text=notes_text
    def run(self):
        try:
            success=self.db.save_note(self.notes_text)
            if success:
                self.completed.emit(True,"")
            else:
                self.completed.emit(False,"Failed to save note")
        except Exception as e:
            self.completed.emit(False,str(e))
class getNoteWorker(QThread):
    fetched=pyqtSignal(bool,str,str)
    def __init__(self,db:Database):
        super().__init__()
        self.db=db
    def run(self):
        try:
            note_text=self.db.get_note()
            self.fetched.emit(True,"",note_text)
        except Exception as e:
            self.fetched.emit(False,str(e),"")
class markCompleteWorker(QThread):
    completed=pyqtSignal(bool,str)
    def __init__(self,db:Database,habit_id,log_date,is_completed):
        super().__init__()
        self.db=db
        self.habitID=habit_id
        self.logDate=log_date
        self.isCompleted=is_completed
    def run(self):
        try:
            success=self.db.mark_completed(self.habitID,self.isCompleted,self.logDate)
            if success:
                self.completed.emit(True,"")
            else:
                self.completed.emit(False,"Failed to Save Completion")
        except Exception as e :
            self.completed.emit(False,str(e))
class getCompletionsWorker(QThread):
    fetched=pyqtSignal(bool,str,list)
    def __init__(self,db:Database,year,month):
        super().__init__()
        self.db=db
        self.year=year
        self.month=month
    def run(self):
        try:
            rows=self.db.get_month_completion(self.year,self.month)
            self.fetched.emit(True,"",rows)
        except Exception as e:
            self.fetched.emit(False,str(e),[])
class getCompleteDaysWorker(QThread):
    fetched=pyqtSignal(bool,str, list)
    def __init__(self,db:Database):
        super().__init__()
        self.db=db
    def run(self):
        try:
            dates=self.db.get_completed_dates()
            self.fetched.emit(True,"",dates)
        except Exception as e:
            self.fetched.emit(False,str(e),[])