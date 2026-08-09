import sys
from datetime import timedelta
from PyQt5.QtWidgets import (QApplication,QWidget,QHBoxLayout,QFrame,
                             QVBoxLayout,QLabel,QListWidget,QPushButton,
                             QLineEdit,QCalendarWidget,QGridLayout,QToolButton,
                             QProgressBar,QTextEdit,QTableWidget,QHeaderView,
                             QTableWidgetItem,QCheckBox,QListWidgetItem)
from PyQt5.QtGui import QIcon,QTextCharFormat,QColor
from PyQt5.QtCore import Qt,QSize,QDate,QEvent,QTimer,QTime
from workers import(DBConnectWorker,addHabitWorker,getHabitWorker,
                    deleteHabitWorker,saveNoteWorker,getNoteWorker,
                    markCompleteWorker,getCompletionsWorker,getCompleteDaysWorker,)
from themes import get_dark_stylesheet,get_light_stylesheet
from backend import Database
class DailyTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Tracker")
        self.resize(1500, 900)
        self.setWindowIcon(QIcon("./python/dailytracker/tracker.png"))
        self.db=Database()
        self.month_completions:set={}
        self.db_ready=False
        self.is_dark_theme=True
        self.initUI()
        self.clock_timer=QTimer(self)
        self.clock_timer.timeout.connect(self.updateClock)
        self.clock_timer.start(1000)
        self.updateClock()
        self.styleCalendarHeader()
        self.dimAdjacentMonths()
        self.DBThread=DBConnectWorker(self.db)
        self.DBThread.connected.connect(self.on_db_connected)
        self.DBThread.start()
        self.DBThread.finished.connect(self.DBThread.deleteLater) 
        QApplication.instance().installEventFilter(self)
    def updateClock(self):
        now=QDate.currentDate()
        current_time=QTime.currentTime().toString("hh:mm AP")
        self.clock_label.setText(current_time)
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
        self.note_thread.finished.connect(self.loadStreak)
        self.note_thread.start()
    def habitFetched(self,success,error,habitlist):
        if success:
            self.habit_list.clear()
            self.habits=habitlist
            for habit_id,habit,created_at in habitlist:
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
            self.habits.append((habit_id,habit_name,QDate.currentDate().toPyDate()))
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
        habit_id_to_row={habit_id:row for row,(habit_id,_,_)in enumerate(self.habits)}
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
        if self.is_dark_theme:
            weekDay_Format.setForeground(QColor("#FBB03B"))
        else:
            weekDay_Format.setForeground(QColor("#A66A00"))
        for day in[Qt.Monday,Qt.Tuesday,Qt.Wednesday,Qt.Thursday,Qt.Friday]:
            self.calendar.setWeekdayTextFormat(day,weekDay_Format)
    def dimAdjacentMonths(self):
        current_month=self.calendar.monthShown()
        current_year=self.calendar.yearShown()
        dim_format=QTextCharFormat()
        dim_format.setForeground(QColor("#4A4A4A"))
        normal_format=QTextCharFormat()
        if self.is_dark_theme:
            normal_format.setForeground(QColor("#FBB03B"))
        else:
            normal_format.setForeground(QColor("#A66A00"))
        first_of_month=QDate(current_year,current_month,1)
        grid_start=first_of_month.addDays(-(first_of_month.dayOfWeek()-1))
        for i in range(42):
            date=grid_start.addDays(i)
            if date.month()!=current_month:
                self.calendar.setDateTextFormat(date,dim_format)
            else:
                self.calendar.setDateTextFormat(date,normal_format)
    def initUI(self):
        vbox=QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)
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
        #building layouts and adding to respective frames
        self.buildLeftLayout()
        self.buildCentralLayout()
        self.buildRightLayout()
        self.buildBottombar()

        vbox.addLayout(self.hbox,1)
        vbox.addWidget(self.bottom_bar)
        self.setLayout(vbox)
        #styling
        self.setObjectnames()
        self.applyStyles()
        self.refreshIcon()
        self.updateStats()
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
        self.notes_box.setPlaceholderText("What's on your mind today...")
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
        self.prev_btn=self.calendar.findChild(QToolButton,"qt_calendar_prevmonth")
        self.next_btn=self.calendar.findChild(QToolButton,"qt_calendar_nextmonth")
        self.prev_btn.setIcon(QIcon("./python/dailytracker/left_chevron.svg"))
        self.next_btn.setIcon(QIcon("./python/dailytracker/right_chevron.svg"))
        self.prev_btn.setIconSize(QSize(18,18))
        self.next_btn.setIconSize(QSize(18,18))
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
        if self.is_dark_theme:
            self.stats_icon=self.seticon("./python/dailytracker/bar.svg",35)
        else:
            self.stats_icon=self.seticon("./python/dailytracker/barL.svg",35)
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
        self.keep_label=QLabel("""        Consistency Beats Intensity""")
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
    def applyStyles(self):
        if self.is_dark_theme:
            self.applyDarkTheme()
        else:
            self.applyLightTheme()
    def applyLightTheme(self):
        #light theme styling
        self.setStyleSheet(get_light_stylesheet())
    def applyDarkTheme(self):
        # dark theme styling
        self.setStyleSheet(get_dark_stylesheet())
    def seticon(self,path:str,size:int):
        label=QLabel()
        label.setPixmap(QIcon(path).pixmap(size,size))
        return label 
    def update_icon(self,label:QLabel,path:str,size:int):
        label.setPixmap(QIcon(path).pixmap(size,size))
    def refreshIcon(self):
        suffix="" if self.is_dark_theme else "L"
        self.update_icon(self.habit_icon,f"./python/dailytracker/habit{suffix}.svg",28)
        self.update_icon(self.task_icon,f"./python/dailytracker/tasks{suffix}.svg",35)
        self.update_icon(self.note_icon,f"./python/dailytracker/notebook-pen-icon{suffix}.svg",28)
        self.update_icon(self.calendar_icon,f"./python/dailytracker/cal icon{suffix}.svg",35)
        self.prev_btn.setIcon(QIcon(f"./python/dailytracker/left_chevron{suffix}.svg"))
        self.next_btn.setIcon(QIcon(f"./python/dailytracker/right_chevron{suffix}.svg"))
        self.update_icon(self.stats_icon,f"./python/dailytracker/bar{suffix}.svg",35)  
    def set_btn_icon(self,button:QPushButton,path:str,size=22):
        button.setIcon(QIcon(path))
        button.setIconSize(QSize(size,size))
    def loadStreak(self):
        self.streak_thread=getCompleteDaysWorker(self.db)
        self.streak_thread.fetched.connect(self.streakFetched)
        self.streak_thread.finished.connect(self.streak_thread.deleteLater)
        self.streak_thread.start()
    def streakFetched(self,success,error,dates):
        if not success:
            print(f"Error Loading Streak: {error}")
            self.completed_dates=[]
        else: 
            self.completed_dates=dates
        streak=self.calculateStreak(self.completed_dates)
        self.streak_value.setText(f"{streak} Days")
        self.streak_days.setText(f"{streak}")
        self.db_ready=True
    def updateTable(self):
        self.styleCalendarHeader()
        self.dimAdjacentMonths()
        if not self.db_ready:
            return
        year=self.calendar.yearShown()
        month=self.calendar.monthShown()
        self.buildHabitTable(year,month)
        self.loadDisplayedCompletions(year,month)
    def loadDisplayedCompletions(self,year,month):
        self.display_completion_thread=getCompletionsWorker(self.db,year,month)
        self.display_completion_thread.fetched.connect(self.displayCompletions)
        self.display_completion_thread.finished.connect(
            self.display_completion_thread.deleteLater
        )
        self.display_completion_thread.start()
    def displayCompletions(self,success,error,rows):
        if not success:
            print(f"Error loading displayed Completions : {error}")
            return
        habit_id_to_row={habit_id:row for row,(habit_id,_,_) in enumerate(self.habits)}
        for habit_id,log_date,completed in rows:
            if habit_id not in habit_id_to_row: continue
            row=habit_id_to_row[habit_id]
            col=log_date.day-1
            container=self.task_table.cellWidget(row,col)
            if container:
                chk_box=container.findChild(QCheckBox)
                if chk_box and completed:
                    chk_box.blockSignals(True)
                    chk_box.setChecked(True)
                    chk_box.blockSignals(False)
    def buildHabitTable(self,year=None,month=None):
        if year is None or month is None:
            date=QDate.currentDate()
            year=date.year()
            month=date.month()
        date=QDate(year,month,1)
        days=date.daysInMonth()
        real_today=QDate.currentDate()
        self.habit_table.setColumnCount(1)
        self.habit_table.setRowCount(len(self.habits))
        self.habit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header=["Habits"]
        self.habit_table.setHorizontalHeaderLabels(header)
        for row,(habit_id,habit,_) in enumerate(self.habits):
            item=QTableWidgetItem(habit)
            item.setData(Qt.UserRole,habit_id)
            self.habit_table.setItem(row,0,item)
        self.task_table.setColumnCount(days)
        self.task_table.setRowCount(len(self.habits))
        headers=[str(i) for i in range(1,days+1)]
        self.task_table.setHorizontalHeaderLabels(headers)
        today=QDate.currentDate().day()-1
        today_qdate=QDate().currentDate()
        for row,(habit_id,habit_name,created_at) in enumerate(self.habits):
            for col in range(days):
                chk_box=QCheckBox()
                chk_box.setFixedSize(22,22)
                col_date=QDate(date.year(),date.month(),col+1).toPyDate()
                if col_date<created_at:
                    chk_box.setEnabled(False)
                    chk_box.setProperty("before_creation",True)
                elif col_date== today_qdate:
                    chk_box.setCursor(Qt.PointingHandCursor)
                    chk_box.stateChanged.connect(
                        lambda state,hid=habit_id,d=col_date:self.onHabitToggled(hid,d,state)
                    )
                else:
                    chk_box.setEnabled(False)
                    if col_date > today_qdate:
                        chk_box.setProperty("future",True)
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
                    containter.setStyleSheet("""background-color:rgba(59,130,246,30);""")
                self.task_table.setCellWidget(row,col,containter)
        for col in range(days):
            self.task_table.setColumnWidth(col,32)
        header=self.task_table.horizontalHeader()
        for i in range(days):
            header.setSectionResizeMode(i,QHeaderView.Fixed)
        for row in range(len(self.habits)):
            self.habit_table.setRowHeight(row,32)
            self.task_table.setRowHeight(row,32)
        if len(self.habits) > 0 and year == real_today.year() and month==real_today.month():
            self.task_table.scrollTo(self.task_table.model().index(0,real_today.day()-1)
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
        for _,habit_name,_ in self.habits:
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
        self.mark_thread.finished.connect(self.loadStreak)
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
    def calculateStreak(self,completed_dates):
        if not completed_dates:
            return 0
        completed_set=set(completed_dates)
        today=QDate.currentDate().toPyDate()
        day = today if today in completed_set else today-timedelta(days=1)
        streak=0
        while day in completed_set:
            streak+=1
            day=day - timedelta(days=1)
        return streak 
    def buildBottombar(self):
        self.bottom_bar = QFrame()
        self.bottom_bar.setObjectName("bottomBar")
        self.bottom_bar.setFixedHeight(36)
        bar_layout=QHBoxLayout()
        bar_layout.setContentsMargins(15,0,15,0)
        self.bottom_icon=self.seticon("./python/dailytracker/calendar.svg",35)
        self.app_label=QLabel("    Daily Tracker  •  Stay Consistent, Achieve Greatness!")
        self.app_label.setObjectName("bottomBarText")
        self.theme_btn=QPushButton()
        self.theme_btn.setObjectName("themeToggleBtn")
        self.theme_btn.setFixedSize(40,40)
        self.set_btn_icon(self.theme_btn,"./python/dailytracker/sun.svg",18)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggleTheme)

        self.clock_label=QLabel()
        self.clock_label.setObjectName("bottomBarText")
        bar_layout.addWidget(self.bottom_icon)
        bar_layout.addWidget(self.app_label)
        bar_layout.addStretch()
        bar_layout.addWidget(self.theme_btn)
        bar_layout.addWidget(self.clock_label)
        self.bottom_bar.setLayout(bar_layout)
    def toggleTheme(self):
        self.is_dark_theme=not self.is_dark_theme
        if self.is_dark_theme:
            self.set_btn_icon(self.theme_btn,"./python/dailytracker/sun.svg")
        else:
            self.set_btn_icon(self.theme_btn,"./python/dailytracker/moon.svg")
        self.applyStyles()
        self.dimAdjacentMonths()
        self.refreshIcon()
        self.styleCalendarHeader()
if __name__ == "__main__":
    app=QApplication(sys.argv)
    window = DailyTracker()
    window.show()
    sys.exit(app.exec_()) 