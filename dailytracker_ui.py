import sys
from datetime import timedelta
from PyQt5.QtWidgets import (QApplication,QWidget,QHBoxLayout,QFrame,
                             QVBoxLayout,QLabel,QListWidget,QPushButton,
                             QLineEdit,QCalendarWidget,QGridLayout,QToolButton,
                             QProgressBar,QTextEdit,QTableWidget,QHeaderView,
                             QTableWidgetItem,QCheckBox,QListWidgetItem)
from PyQt5.QtGui import QIcon,QTextCharFormat,QColor
from PyQt5.QtCore import Qt,QSize,QDate,QThread,pyqtSignal,QEvent,QTimer
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
class DailyTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Tracker")
        self.resize(1500, 900)
        self.setWindowIcon(QIcon("./python/dailytracker/tracker.png"))
        self.db=Database()
        self.month_completions:set={}
        self.initUI()
        self.styleCalendarHeader()
        self.dimAdjacentMonths()
        self.DBThread=DBConnectWorker(self.db)
        self.DBThread.connected.connect(self.on_db_connected)
        self.DBThread.start()
        self.DBThread.finished.connect(self.DBThread.deleteLater) 
        QApplication.instance().installEventFilter(self)
    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            clicked_Widget=QApplication.widgetAt(event.globalPos())
            if clicked_Widget is not None and self.habit_list.isAncestorOf(clicked_Widget):
                self.habit_list.clearSelection()
                self.habit_list.setCurrentItem(None)
            elif (clicked_Widget is self.delete_habit or 
            self.delete_habit.isAncestorOf(clicked_Widget)):
                pass 
            elif clicked_Widget is not self.habit_list:
                self.habit_list.clearSelection()
                self.habit_list.setCurrentItem(None)
        return super().eventFilter(object,event)
    def on_db_connected(self,success,error):
        if success:
            #print("DB Ready")
            self.habits_thread=getHabitWorker(self.db)
            self.habits_thread.fetched.connect(self.habitFetched)
            self.habits_thread.finished.connect(self.habits_thread.deleteLater)
            self.habits_thread.start()
        else:
            print(f"DB Failed Error: {error}")
    def loadNote(self):
        self.note_thread=getNoteWorker(self.db)
        self.note_thread.fetched.connect(self.noteFetched)
        self.note_thread.finished.connect(self.note_thread.deleteLater)
        self.note_thread.start()
    def habitFetched(self,success,error,habitlist):
        if success:
            self.habit_list.clear()
            self.habits=habitlist
            for habit_id,habit in habitlist:
                item=QListWidgetItem(f"● {habit}")
                item.setData(Qt.UserRole,habit_id)
                self.habit_list.addItem(item)
            self.buildHabitTable()
            self.loadCompletions()
        else:
            print(f"Error couldn't Load Habits:{error}")
    def habitAdded(self,success,error,habit_id,habit_name):
        self.add_habit.setEnabled(True)
        if success:
            item=QListWidgetItem(f"● {habit_name}")
            item.setData(Qt.UserRole,habit_id)
            self.habit_list.addItem(item)
            self.habits.append((habit_id,habit_name))
            self.buildHabitTable()
            self.loadCompletions()
            self.habit_name.clear()
        else:
            self.habit_error.setText(f"Error: {error}")
            self.habit_error.setVisible(True)
    def habitDeleted(self,success,error,habit_id):
        self.delete_habit.setEnabled(True)
        if success:
            row=self.habit_list.row(self.habit_list.currentItem())
            self.habit_list.takeItem(row)
            self.habit_list.clearSelection()
            self.habit_list.setCurrentItem(None)
            self.habits=[h for h in self.habits if h[0]!= habit_id]
            self.buildHabitTable()
            self.loadCompletions()
        else:
            self.habit_error.setText(f"Error: {error}")
            self.habit_error.setVisible(True)
    def noteSaved(self,success,error):
        self.save_btn.setEnabled(True)
        if not success:
            print(f"Error saving note: {error}")
    def completionsFetched(self,success,error,rows):
        if not success:
            print(f"Error loading Completions:{error}")
            return
        habit_id_to_row={habit_id:row for row,(habit_id,_)in enumerate(self.habits)}
        self.month_completions:set={}
        for habit_id,log_date,completed in rows:
            if habit_id not in habit_id_to_row:
                continue
            row=habit_id_to_row[habit_id]
            col=log_date.day-1
            container=self.task_table.cellWidget(row,col)
            if container:
                chk_box=container.findChild(QCheckBox)
                if chk_box and completed:
                    chk_box.blockSignals(True)
                    chk_box.setChecked(True)
                    chk_box.blockSignals(False)
            if completed:
                self.month_completions.setdefault(log_date,set()).add(habit_id)
            self.updateStats()
    def styleCalendarHeader(self):
        weekDay_Format=QTextCharFormat()
        weekDay_Format.setForeground(QColor("#D29104"))
        for day in[Qt.Monday,Qt.Tuesday,Qt.Wednesday,Qt.Thursday,Qt.Friday]:
            self.calendar.setWeekdayTextFormat(day,weekDay_Format)
    def dimAdjacentMonths(self):
        current_month=self.calendar.monthShown()
        current_year=self.calendar.yearShown()
        dim_format=QTextCharFormat()
        dim_format.setForeground(QColor("#4A4A4A"))
        normal_format=QTextCharFormat()
        normal_format.setForeground(QColor("#D29104"))
        first_of_month=QDate(current_year,current_month,1)
        grid_start=first_of_month.addDays(-(first_of_month.dayOfWeek()-1))
        for i in range(42):
            date=grid_start.addDays(i)
            if date.month()!=current_month:
                self.calendar.setDateTextFormat(date,dim_format)
            else:
                self.calendar.setDateTextFormat(date,normal_format)
    def initUI(self):
        #main hbox for 3 frames
        self.hbox=QHBoxLayout()
        #creating frames
        self.left_frame=QFrame()
        self.central_frame=QFrame()
        self.right_frame=QFrame()
        #adding frames to hbox
        self.hbox.addWidget(self.left_frame,1)
        self.hbox.addWidget(self.central_frame,3)
        self.hbox.addWidget(self.right_frame,1)
        self.hbox.setSpacing(20)
        self.hbox.setContentsMargins(20,20,20,20)
        self.setLayout(self.hbox)
        #building layouts and adding to respective frames
        self.buildLeftLayout()
        self.buildCentralLayout()
        self.buildRightLayout()
        #styling
        self.setObjectnames()
        self.addStyles()
    def buildLeftLayout(self):
        self.left_layout=QVBoxLayout()
        #habit header
        self.habit_header = QHBoxLayout()
        self.habit_header.setSpacing(8)
        self.habit_icon=self.seticon("./python/dailytracker/habit.svg",28)
        self.habit_label=QLabel("Habits List")
        self.habit_header.addWidget(self.habit_icon)
        self.habit_header.addWidget(self.habit_label)
        self.habit_header.addStretch()
        #the habit list
        self.habit_list=QListWidget()
        self.add_habit=QPushButton("Add Habit")
        self.set_btn_icon(self.add_habit,"./python/dailytracker/add.svg")
        self.add_habit.clicked.connect(self.addHabit)
        self.habit_name=QLineEdit()
        self.habit_name.setPlaceholderText("Enter a habit: ")
        self.habit_name.returnPressed.connect(self.addHabit)
        self.habit_error=QLabel("")
        self.habit_error.setObjectName("errorLabel")
        self.habit_error.setVisible(False)
        self.delete_habit=QPushButton("Delete Habit")
        self.set_btn_icon(self.delete_habit,"./python/dailytracker/del.svg")
        self.delete_habit.clicked.connect(self.deleteHabit)
        self.add_habit.setCursor(Qt.PointingHandCursor)
        self.delete_habit.setCursor(Qt.PointingHandCursor)
        #the left layout
        self.left_layout.addLayout(self.habit_header)
        self.left_layout.addWidget(self.habit_list)
        self.left_layout.addWidget(self.habit_name)
        self.left_layout.addWidget(self.habit_error)
        self.left_layout.addWidget(self.add_habit)
        self.left_layout.addWidget(self.delete_habit)
        self.left_frame.setLayout(self.left_layout)
    def buildCentralLayout(self):
        self.central_layout=QVBoxLayout()
        #3 frames
        self.header_frame=QFrame()
        self.task_frame=QFrame()
        self.notes_frame=QFrame()
        #header frame HBox
        self.header_layout=QHBoxLayout()
        self.today_label=QLabel("Today")
        self.date_label=QLabel(QDate.currentDate().toString("dddd, d MMMM yyyy"))
        self.date_icon=self.seticon("./python/dailytracker/calendar.svg",60)
        #left header and left text
        self.left_header=QHBoxLayout()
        self.left_text=QVBoxLayout()
        self.left_text.addWidget(self.today_label)
        self.left_text.addWidget(self.date_label)
        self.left_header.addWidget(self.date_icon)
        self.left_header.addLayout(self.left_text)
        #right header and progress bar
        self.right_header=QVBoxLayout()
        self.right_header.setAlignment(Qt.AlignRight)
        self.progress_layout=QHBoxLayout()
        self.progress_layout.setAlignment(Qt.AlignRight)
        self.finished_label=QLabel("")
        self.progress_bar=QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedWidth(220)
        self.progress_bar.setFixedHeight(12)
        self.percent_label=QLabel("")
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.percent_label)
        self.right_header.addWidget(self.finished_label)
        self.right_header.addLayout(self.progress_layout)
        #adding right and left header to header layout 
        self.header_layout.addLayout(self.left_header)
        self.header_layout.addStretch()
        self.header_layout.addLayout(self.right_header)
        #task layout
        self.task_layout=QVBoxLayout()
        self.task_header=QHBoxLayout()
        self.task_header.addSpacing(8)
        self.task_icon=self.seticon("./python/dailytracker/tasks.svg",35)
        self.task_label=QLabel("Progression of Habits")
        self.task_header.addWidget(self.task_icon)
        self.task_header.addWidget(self.task_label)
        self.task_header.addStretch()
        self.task_layout.addLayout(self.task_header)
        #the habit table
        self.table_layout=QHBoxLayout()
        self.habit_table=QTableWidget()
        self.habit_table.setMinimumWidth(180)
        self.habit_table.setMaximumWidth(180)
        self.habit_table.setFocusPolicy(Qt.NoFocus)
        self.habit_table.verticalHeader().setVisible(False)
        self.habit_table.horizontalHeader().setStretchLastSection(True)
        self.habit_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.habit_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.habits=[]     
        self.habit_table.setColumnWidth(0,180)
        self.habit_table.setSelectionMode(QTableWidget.NoSelection)
        self.habit_table.setSelectionBehavior(QTableWidget.SelectItems)
        #task_table
        self.task_table=QTableWidget()             
        self.task_table.verticalHeader().setVisible(False)      
        self.task_table.setEditTriggers(QTableWidget.NoEditTriggers)
        #syncronised scrolling
        self.task_table.verticalScrollBar().valueChanged.connect(
            self.habit_table.verticalScrollBar().setValue
        )
        self.habit_table.verticalScrollBar().valueChanged.connect(
            self.task_table.verticalScrollBar().setValue
        ) 
        self.table_layout.setSpacing(0)
        self.table_layout.setContentsMargins(0,0,0,0)
        self.table_layout.addWidget(self.habit_table)
        self.table_layout.addWidget(self.task_table)
        self.task_layout.addLayout(self.table_layout,1)
        #notes layout
        self.notes_layout=QVBoxLayout()
        self.notes_layout.setContentsMargins(15,15,15,15)
        self.note_hbox=QHBoxLayout()
        self.note_icon=self.seticon("./python/dailytracker/notebook-pen-icon.svg",28)
        self.notes_header=QLabel("Today's Notes")
        self.note_hbox.setSpacing(8)
        self.note_hbox.addWidget(self.note_icon)
        self.note_hbox.addWidget(self.notes_header)
        self.note_hbox.addStretch()
        self.notes_layout.addLayout(self.note_hbox)
        self.notes_box=QTextEdit()
        self.notes_box.setPlaceholderText("Write Today's Notes...")
        self.notes_layout.addWidget(self.notes_box)
        self.save_btn=QPushButton(" Save Changes")
        self.set_btn_icon(self.save_btn,"./python/dailytracker/save.svg")
        self.save_btn.setFixedWidth(225)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.notes_layout.addWidget(self.save_btn,alignment=Qt.AlignRight)
        self.save_btn.clicked.connect(self.saveNote)
        #setting layouts to frame
        self.header_frame.setLayout(self.header_layout)
        self.task_frame.setLayout(self.task_layout)
        self.notes_frame.setLayout(self.notes_layout)
        #adding the layout to centralframe
        self.central_layout.addWidget(self.header_frame,1)
        self.central_layout.addWidget(self.task_frame,3)
        self.central_layout.addWidget(self.notes_frame,2)
        self.central_frame.setLayout(self.central_layout)
    def buildRightLayout(self):
        self.right_layout=QVBoxLayout()
        #calendar frame
        self.calendar_frame=QFrame()
        self.calendar_layout=QVBoxLayout()
        self.calendar_header=QHBoxLayout()
        self.calendar_header.setSpacing(8)
        self.calendar_icon=self.seticon("./python/dailytracker/cal icon.svg",35)
        self.calendar_label=QLabel("Calendar")
        self.calendar_header.addWidget(self.calendar_icon)
        self.calendar_header.addWidget(self.calendar_label)
        self.calendar_header.addStretch()
        self.calendar=QCalendarWidget()
        self.calendar.currentPageChanged.connect(self.updateTable)
        prev_btn=self.calendar.findChild(QToolButton,"qt_calendar_prevmonth")
        next_btn=self.calendar.findChild(QToolButton,"qt_calendar_nextmonth")
        prev_btn.setIcon(QIcon("./python/dailytracker/left_chevron.svg"))
        next_btn.setIcon(QIcon("./python/dailytracker/right_chevron.svg"))
        prev_btn.setIconSize(QSize(18,18))
        next_btn.setIconSize(QSize(18,18))
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
        self.calendar.setMaximumHeight(260)
        self.calendar_layout.addLayout(self.calendar_header)
        self.calendar_layout.addWidget(self.calendar)
        self.calendar_frame.setLayout(self.calendar_layout)
        #stats frame
        self.stats_frame=QFrame() 
        self.statvbox=QVBoxLayout() 
        self.stats_header=QHBoxLayout()
        self.stats_header.addSpacing(8)
        self.stats_icon=self.seticon("./python/dailytracker/bar.svg",35)
        self.stats_label=QLabel("Stats")
        self.stats_header.addWidget(self.stats_icon)
        self.stats_header.addWidget(self.stats_label)
        self.stats_header.addStretch()
        self.stats_layout=QGridLayout()
        self.completion_label=QLabel("Completion Rate")
        self.completion_value=QLabel("")
        self.completion_value.setAlignment(Qt.AlignRight)
        self.completed_label=QLabel("Completed Today")
        self.completed_value=QLabel("")
        self.completed_value.setAlignment(Qt.AlignRight)
        self.total_label=QLabel("Total Habits")
        self.total_value=QLabel("")
        self.total_value.setAlignment(Qt.AlignRight)
        self.streak_label=QLabel("Current Streak")
        self.streak_value=QLabel("")
        self.streak_value.setAlignment(Qt.AlignRight)
        self.stats_layout.addWidget(self.completion_label,0,0)
        self.stats_layout.addWidget(self.completion_value,0,1)
        self.stats_layout.addWidget(self.completed_label,1,0)
        self.stats_layout.addWidget(self.completed_value,1,1)
        self.stats_layout.addWidget(self.total_label,2,0)
        self.stats_layout.addWidget(self.total_value,2,1)
        self.stats_layout.addWidget(self.streak_label,3,0)
        self.stats_layout.addWidget(self.streak_value,3,1)
        self.stats_layout.setVerticalSpacing(12)
        self.stats_layout.setHorizontalSpacing(25)
        self.stats_layout.setColumnStretch(0,3)
        self.stats_layout.setColumnStretch(1,1)
        self.statvbox.addLayout(self.stats_header)
        self.statvbox.addLayout(self.stats_layout)
        self.stats_frame.setLayout(self.statvbox)
        #streak frame.
        self.streak_frame=QFrame()
        self.streak_layout=QVBoxLayout()
        self.streak_header=QLabel("🔥 Current Streak")
        self.days_layout=QHBoxLayout()
        self.days_layout.addStretch()
        self.days_label=QLabel("days")
        self.streak_days=QLabel("")
        self.days_layout.addWidget(self.streak_days)
        self.days_layout.addWidget(self.days_label)
        self.days_layout.addStretch()
        self.keep_label=QLabel("""        Be Yourself,Belive Yourself
(note: streak resets itself every month)""")
        self.streak_layout.addWidget(self.streak_header)
        self.streak_layout.addLayout(self.days_layout)
        self.streak_layout.addWidget(self.keep_label)
        self.streak_frame.setLayout(self.streak_layout)
        #the right layout
        self.right_layout.addWidget(self.calendar_frame)
        self.right_layout.addWidget(self.stats_frame)
        self.right_layout.addWidget(self.streak_frame)
        self.right_layout.addStretch()
        self.right_frame.setLayout(self.right_layout)
    def setObjectnames(self):
        #setting object names for styling
        self.central_frame.setObjectName("centerFrame")
        self.add_habit.setObjectName("add_habit")
        self.delete_habit.setObjectName("delete_habit")
        self.calendar_label.setObjectName("calendar_label")
        self.habit_label.setObjectName("habit_label")
        for i in [self.completion_label,self.completed_label,
                  self.total_label,self.streak_label]:
            i.setObjectName("statName")
        for i in [self.completed_value,
                  self.total_value]:
            i.setObjectName("statValue")
        for i in[self.habit_label,self.calendar_label,self.stats_label]:
            i.setObjectName("sideHeaders")
        for i in [self.streak_frame,self.stats_frame,self.calendar_frame,
                  self.header_frame,self.task_frame,self.notes_frame]:
            i.setObjectName("inner_frames")
        self.completion_value.setObjectName("progress")
        self.streak_value.setObjectName("streak")
        self.streak_days.setObjectName("streakDays")
        self.days_label.setObjectName("daysLabel")
        self.keep_label.setObjectName("keepLabel")
        self.percent_label.setObjectName("percentLabel")
        self.finished_label.setObjectName("finishedLabel")
        self.date_label.setObjectName("dateLabel")
        self.today_label.setObjectName("todayLabel")
        self.save_btn.setObjectName("saveBtn")
        self.notes_header.setObjectName("notesHeader")
    def addStyles(self):
        #styling
        self.setStyleSheet("""
                           QWidget{
                           background-color:#121212;
                           font-family:Segoe UI;
                           }
                           QFrame{
                           background-color:#1E1E1E;
                           border-radius:15px;
                           }
                           QFrame#inner_frames{
                           background-color:#252525;
                           border-radius:10px;
                           padding-top:15px;
                           padding-bottom:15px;
                           }
                           QFrame#centerFrame{
                           border:2px solid #3B82F6;
                           }
                           QLabel{
                           background:transparent;
                           color:#D29104;
                           font-size:24px;
                           }
                           QLabel#sideHeaders{
                           min-height:50px;
                           }
                           QLabel#statName{
                           color:#C5C5C5;
                           font-size:18px;
                           font-weight:500;
                           }
                           QLabel#statValue{
                           color:#B8B8B8;
                           font-size:20px;
                           font-weight:500;
                           }
                           QLabel#progress{
                           color:#3B82F6;
                           font-weight:500;
                           font-size:20px;
                           }
                           QLabel#streak{
                           color:hsl(43,95%,42%);
                           font-weight:500;
                           font-size:20px;
                           }
                           QLabel#streakDays{
                           color:hsl(36,100%,55%);
                           font-size:50px;
                           font-weight:400;
                           font-style:italic;
                           }
                           QLabel#daysLabel{
                           color:#E5E5E5;
                           font-size:22px;
                           padding-top:18px;
                           }
                           QLabel#keepLabel{
                           color:#C5C5C5;
                           font-size:18px;
                           padding-left:30px;
                           }
                           QLabel#percentLabel{
                           color:#3B82F6;
                           font-size:24px;
                           font-weight:450;
                           }
                           QLabel#finishedLabel{
                           color:#3B82F6;
                           font-size:24px;
                           font-weight:450;
                           }
                           QLabel#dateLabel{
                           color:#C5C5C5;
                           font-size:20px;
                           }
                           QLabel#todayLabel{
                           color:hsl(41,96%,41%);
                           font-size:34px;
                           font-weight:460;
                           }
                           QLabel#notesHeader{
                           color:#D29104;
                           font-size:24px;
                           font-weight:500;
                           }
                           QLabel#errorLabel{
                           color:#EF4444;
                           font-size:14px;
                           }
                           QTextEdit{
                           background-color:#1E1E1E;
                           color:#E5E5E5;
                           border:none;
                           border-radius:10px;
                           padding:10px;
                           selection-background-color:#3B82F6;
                           font-size:18px;
                           }
                           QTextEdit::focus{
                           border:2px solid #3B82F6;
                           }
                           QListWidget{
                           background-color:#252525;
                           color:hsl(41,92%,42%);
                           border:none;
                           border-radius:10px;
                           font-size:18px;
                           padding:10px;
                           }
                           QListWidget::item{
                           padding:10px;
                           min-height:25px;
                           }
                           QListWidget::item:selected{
                           background-color:#3B82F6;
                           color:white;
                           border-radius:6px;
                           }
                           QProgressBar{
                           border:none;
                           border-radius:6px;
                           background:#363636;
                           height:12px;
                           }
                           QProgressBar::chunk{
                           background:#3B82F6;
                           border-radius:6px;
                           }
                           QLineEdit{
                           background-color:#252525;
                           color:hsl(42,96%,41%);
                           font-size:18px;
                           min-height:25px;
                           border:none;
                           border-radius:10px;
                           padding:8px;
                           }
                           QLineEdit:focus{
                           border:2px solid #3B82F6;
                           }
                           QCalendarWidget QWidget{
                           background-color:#252525;
                           }
                           QCalendarWidget QToolButton{
                           background-color:#252525;
                           color:hsl(41,96%,41%);
                           border-radius:6px;
                           border:none;
                           padding:4px;
                           font-size:20px;
                           font-weight:600;
                           }
                           QCalendarWidget QToolButton:hover{
                           background-color:#333333;
                           }
                           QCalendarWidget QToolButton:pressed{
                           background-color:#404040;
                           }
                           QCalendarWidget QMenu{
                           background-color:#252525;
                           color:hsl(42,96%,42%)
                           }
                           QCalendarWidget QAbstractItemView{
                           selection-background-color:#3B82F6;
                           selection-color:white;
                           }
                           QCalendarWidget QTableView{
                           background-color:#252525;
                           alternate-background-color:#252525;
                           }
                           QCalendarWidget QHeaderView{
                           background-color:#252525;
                           }
                           QCalendarWidget QTableView QHeaderView::section{
                           background-color:#252525;
                           color:hsl(41,96%,42%);
                           padding:6px;
                           border:none;
                           }
                           QPushButton{
                           border:none;
                           border-radius:10px;
                           padding:8px;
                           font-size:15px;
                           min-height:40px;
                           }
                           QPushButton#saveBtn{
                           background-color:#16A34A;
                           color:white;
                           font-size:18px;
                           font-weight:450;
                           }
                           QPushButton#saveBtn:hover{
                           background-color:#22C55E;
                           }
                           QPushButton#saveBtn:pressed{
                           background-color:#15803D;
                           }
                           QPushButton#add_habit{
                           background-color:#3B82F6;
                           color:white;
                           }
                           QPushButton#delete_habit{
                           background-color:#B91C1C;
                           color:white;
                           }
                           QPushButton#add_habit:hover{
                           background-color:#60A5FA;
                           }
                           QPushButton#add_habit:pressed{
                           background-color:#2563EB;
                           }
                           QPushButton#delete_habit:hover{
                           background-color:#DC2626;
                           }
                           QPushButton#delete_habit:pressed{
                           background-color:#991B1B;
                           }
                           QTableWidget{
                           background-color:#1E1E1E;
                           color:#E5E5E5;
                           border:none;
                           border-radius:10px;
                           gridline-color:#2F2F2F;
                           font-size:16px;
                           selection-background-color:transparent;
                           outline:none;
                           }
                           QHeaderView::section{
                           background-color:#252525;
                           color:#D29104;
                           border:1px solid #1E1E1E;
                           padding:8px;
                           font-size:16px;
                           font-weight:450;
                           }
                           QTableWidget::item:selected{
                           background-color:#3B82F6;
                           }
                           QScrollBar:horizontal{
                           background:rgb(0,0,0);
                           height:12px;
                           border:none;
                           border-radius:6px;
                           }
                           QScrollBar::handle:horizontal{
                           background:#3B82F6;
                           border-radius:6px;
                           min-width:12px;
                           }
                           QScrollBar::handle:horizontal:hover{
                           background:#60A5FA;
                           }
                           QScrollBar::add-line:horizontal,
                           QScrollBar::sub-line:horizontal{
                           width:0px;
                           }
                           QScrollBar::add-page:horizontal,
                           QScrollBar::sub-page:horizontal{
                           background:none;
                           }
                           QScrollBar:vertical{
                           background:rgb(0,0,0);
                           width:12px;
                           border:none;
                           border-radius:6px;
                           }
                           QScrollBar::handle:vertical{
                           background:#3B82F6;
                           border-radius:6px;
                           min-height:12px;
                           }
                           QScrollBar::handle:vertical:hover{
                           background:#60A5FA;
                           }
                           QScrollBar::add-line:vertical,
                           QScrollBar::sub-line:vertical{
                           height:0px;
                           }
                           QScrollBar::add-page:vertical,
                           QScrollBar::sub-page:vertical{
                           background:transparent;
                           }
                           QCheckBox{
                           background:transparent;
                           }
                           QCheckBox::indicator{
                           width:18px;
                           height:18px;
                           border:2px solid #505050;
                           border-radius:4px;
                           background-color:#1E1E1E;
                           }
                           QCheckBox::indicator:hover{
                           border:2px solid #3B82F6;
                           background-color:#2B2B2B;
                           }
                           QCheckBox::indicator:pressed{
                           background-color:#353535;
                           }
                           QCheckBox::indicator:checked{
                           background-color:#3B82F6;
                           border:2px solid #3B82F6;
                           image:url("./python/dailytracker/check.svg");
                           }
                           QCheckBox::indicator:checked:hover{
                           background-color:#60A5FA;
                           border:2px solid #60A5FA;
                           }
                           """
                           )
    def seticon(self,path:str,size:int):
        label=QLabel()
        label.setPixmap(QIcon(path).pixmap(size,size))
        return label     
    def set_btn_icon(self,button:QPushButton,path:str,size=22):
        button.setIcon(QIcon(path))
        button.setIconSize(QSize(size,size))
    def updateTable(self):
        self.styleCalendarHeader()
        self.dimAdjacentMonths()
    def buildHabitTable(self):
        date=QDate.currentDate()
        days=date.daysInMonth()
        self.habit_table.setColumnCount(1)
        self.habit_table.setRowCount(len(self.habits))
        self.habit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header=["Habits"]
        self.habit_table.setHorizontalHeaderLabels(header)
        for row,(habit_id,habit) in enumerate(self.habits):
            item=QTableWidgetItem(habit)
            item.setData(Qt.UserRole,habit_id)
            self.habit_table.setItem(row,0,item)
        self.task_table.setColumnCount(days)
        self.task_table.setRowCount(len(self.habits))
        headers=[str(i) for i in range(1,days+1)]
        self.task_table.setHorizontalHeaderLabels(headers)
        today=QDate.currentDate().day()-1
        today_qdate=QDate().currentDate()
        for row,(habit_id,habit_name) in enumerate(self.habits):
            for col in range(days):
                chk_box=QCheckBox()
                chk_box.setFixedSize(22,22)
                col_date=QDate(date.year(),date.month(),col+1).toPyDate()
                if col_date== today_qdate:
                    chk_box.setCursor(Qt.PointingHandCursor)
                    chk_box.stateChanged.connect(
                        lambda state,hid=habit_id,d=col_date:self.onHabitToggled(hid,d,state)
                    )
                else:
                    chk_box.setEnabled(False)
                containter=QWidget()
                #containter.setFixedSize(32,32)
                layout=QHBoxLayout((containter))
                layout.setContentsMargins(0,0,0,0)
                layout.setSpacing(0)
                #layout.setAlignment(Qt.AlignCenter)
                layout.addStretch()
                layout.addWidget(chk_box)
                layout.addStretch()
                if col_date==today_qdate:
                    containter.setStyleSheet("""background-color:rgba(59,130,246,40);""")
                self.task_table.setCellWidget(row,col,containter)
        for col in range(days):
            self.task_table.setColumnWidth(col,32)
        header=self.task_table.horizontalHeader()
        for i in range(days):
            header.setSectionResizeMode(i,QHeaderView.Fixed)
        for row in range(len(self.habits)):
            self.habit_table.setRowHeight(row,32)
            self.task_table.setRowHeight(row,32)
        if len(self.habits) > 0:
            self.task_table.scrollTo(self.task_table.model().index(0,today)
                                 , QTableWidget.PositionAtCenter )
        self.task_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
    def loadCompletions(self):
        today=QDate.currentDate()
        self.completions_thread=getCompletionsWorker(self.db,today.year(),today.month())
        self.completions_thread.fetched.connect(self.completionsFetched)
        self.completions_thread.finished.connect(self.completions_thread.deleteLater)
        self.completions_thread.finished.connect(self.loadNote)
        self.completions_thread.start()
    def addHabit(self):
        habit=self.habit_name.text().strip()
        if not habit:
            self.habit_error.setText("Habit Name should not be empty")
            self.habit_error.setVisible(True)
            return
        elif len(habit)>50:
            self.habit_error.setText("Habit name should not exceed 50 characters")
            self.habit_error.setVisible(True)
            return
        for _,habit_name in self.habits:
            if habit_name.lower()==habit.lower():
                self.habit_error.setText(f"{habit} already exists")
                self.habit_error.setVisible(True)
                return
        self.habit_error.setVisible(False)
        self.add_habit.setEnabled(False)
        self.add_habit_thread=addHabitWorker(self.db,habit)
        self.add_habit_thread.completed.connect(self.habitAdded)
        self.add_habit_thread.finished.connect(self.add_habit_thread.deleteLater)
        self.add_habit_thread.start()
    def deleteHabit(self):
        current_item=self.habit_list.currentItem()
        if current_item is None:
            self.habit_error.setText("Select a habit to delete")
            self.habit_error.setVisible(True)
            return
        self.habit_error.setVisible(False)
        self.delete_habit.setEnabled(False)
        habitID=current_item.data(Qt.UserRole)
        self.delete_habit_thread=deleteHabitWorker(self.db,habitID)
        self.delete_habit_thread.deleted.connect(self.habitDeleted)
        self.delete_habit_thread.finished.connect(self.delete_habit_thread.deleteLater)
        self.delete_habit_thread.start()
    def saveNote(self):
        note_text=self.notes_box.toPlainText().strip()
        self.save_btn.setEnabled(False)
        self.save_note_thread=saveNoteWorker(self.db,note_text)
        self.save_note_thread.completed.connect(self.noteSaved)
        self.save_note_thread.finished.connect(self.save_note_thread.deleteLater)
        self.save_note_thread.start()
    def noteFetched(self,success,error,notes_text):
        if success:
            self.notes_box.setPlainText(notes_text)
        else: print(f"Error loading note {error}")
    def onHabitToggled(self,habit_id,date,state):
        chk_box:QCheckBox=self.sender()
        h_scroll=self.task_table.horizontalScrollBar().value()
        v_scroll=self.task_table.verticalScrollBar().value()
        chk_box.setEnabled(False)
        def restore_scroll():
            self.task_table.horizontalScrollBar().setValue(h_scroll)
            self.task_table.verticalScrollBar().setValue(v_scroll)
        QTimer.singleShot(0,restore_scroll)
        completed=(state==Qt.Checked)
        self.mark_thread=markCompleteWorker(self.db,habit_id,date,completed)
        self.mark_thread.completed.connect(
            lambda success,error,t=self.mark_thread,hid=habit_id,d=date,c=completed:
              self.habitMarked(chk_box,t,success,error,h_scroll,v_scroll,hid,d,c)
            )
        self.mark_thread.finished.connect(self.mark_thread.deleteLater)
        self.mark_thread.start()
        if not hasattr(self,"mark_threads"):
            self.mark_threads=[]
        self.mark_threads.append(self.mark_thread)
    def habitMarked(self,chk_box:QCheckBox,thread,success,error,h_scroll,v_scroll,
                    habit_id,date,completed):
        chk_box.setEnabled(True)
        if not success:
            print(f"Error saving completion: {error}")
        else:
            day_set=self.month_completions.setdefault(date,set())
            if completed:
                day_set.add(habit_id)
            else:
                day_set.discard(habit_id)
            self.updateStats()
        self.mark_threads.remove(thread)
        def restore_scroll():
            self.task_table.horizontalScrollBar().setValue(h_scroll)
            self.task_table.verticalScrollBar().setValue(v_scroll)
        QTimer.singleShot(0,restore_scroll)
    def updateStats(self):
        total=len(self.habits)
        today=QDate.currentDate().toPyDate()
        completed_today=len(self.month_completions.get(today,set()))
        percent=int(round(completed_today*100/total)) if total else 0
        self.finished_label.setText(f"{completed_today}/{total} Completed")
        self.progress_bar.setValue(percent)
        self.percent_label.setText(f"{percent}%") 
        self.completion_value.setText(f"{percent}%")
        self.completed_value.setText(f"{completed_today}")
        self.total_value.setText(f"{total}")
        streak=self.calculateStreak()
        self.streak_value.setText(f"{streak} Days")
        self.streak_days.setText(f"{streak}")
    def calculateStreak(self):
        if not self.habits:
            return 0
        streak=0
        day=QDate.currentDate().toPyDate()
        while True:
            if self.month_completions.get(day,set()):
                streak+=1
                day=day - timedelta(days=1)
                if day.day>QDate.currentDate().day():
                    break
            else: break
        return streak 
if __name__ == "__main__":
    app=QApplication(sys.argv)
    window = DailyTracker()
    window.show()
    sys.exit(app.exec_()) 