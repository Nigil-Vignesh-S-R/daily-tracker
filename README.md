# 📖 Daily Tracker

**Author:** S R Nigil Vignesh

Daily Tracker is a modern desktop habit-tracking application built with **Python**, **PyQt5**, and **SQLite3**. It helps users build consistent routines by allowing them to create habits, track daily progress, maintain streaks, and write daily notes through a clean and responsive desktop interface.

Unlike web-based habit trackers, Daily Tracker stores all data locally using SQLite, making it lightweight, portable, and easy to set up—no external database server is required.

---

# ✨ Features

## 📝 Habit Management

- Create and delete habits with ease.
- Prevents duplicate habit entries.
- Input validation for reliable data.
- Instant UI updates after modifications.
- Preserves the creation date of every habit.
---

## ✅ Daily Habit Tracking

- Mark habits as completed for the current day.
- Completion history is permanently stored.
- Only today's entries are editable.
- Browse previous and upcoming months using the integrated calendar.
- Color-coded completion indicators (✓ Completed / ✗ Incomplete).
- Completion indicators are only shown from a habit's creation date onward.
---

## 📊 Progress Dashboard

- Live completion percentage.
- Progress bar with visual feedback.
- Completed habits vs total habits.
- Statistics update automatically.

---

## 🔥 Streak Tracking

- Automatically calculates your current streak.
- Restores streak correctly after restarting the application.
- Encourages consistency through daily progress.

> **Consistency Beats Intensity.**

---

## 📅 Interactive Calendar

- Navigate seamlessly between months.
- Automatically synchronizes with the habit table.
- Supports months with 28, 29, 30, and 31 days.
- Review previous completion history effortlessly.

---

## 📒 Daily Notes

- Write notes for each day.
- Automatically saves your notes.
- Loads previously saved notes when reopening the application.

---

## 💾 Local SQLite Database

- Stores habits, completion records, and notes locally.
- No database installation required.
- Lightweight and portable.
- Uses relational tables with foreign key support.
- Clean separation between the user interface and database layer.

---

## ⚡ Responsive User Experience

- Database operations run in background threads using **QThread**.
- Prevents the interface from freezing during database operations.
- Uses Qt's signal-slot mechanism for real-time updates.
- Smooth and responsive desktop experience.

---

## 🎨 Modern Desktop Interface

- Modern dark & light themes.
- Custom SVG icons.
- Interactive calendar.
- Progress dashboard.
- Statistics panel.
- Dedicated streak widget.
- Responsive tables with synchronized scrolling.
- Highlights the current day for improved usability.
- Color-coded habit completion indicators.

---

# 🛠️ Tech Stack

- Python
- PyQt5
- SQLite3
- Qt Signals & Slots
- QThread

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Nigil-Vignesh-S-R/daily-tracker.git

cd daily-tracker
```

---

## 2. Install the required packages

```bash
pip install -r requirements.txt
```

---

## 3. Run the application

```bash
python dailytracker_ui.py
```

---

# 📷 Screenshots

<img width="1200" height="762" alt="image" src="https://github.com/user-attachments/assets/c33e753a-c876-4cce-a732-081ff5ef1081" />
**double clicks waking**
<img width="1198" height="772" alt="image" src="https://github.com/user-attachments/assets/be145955-5fef-4776-9d07-ebb99098cc07" />
<img width="1198" height="768" alt="image" src="https://github.com/user-attachments/assets/1bc4a6e1-1a0f-4e7f-acfa-5e3dd5e123ac" />

**clicks ok/press enter**
<img width="1200" height="761" alt="image" src="https://github.com/user-attachments/assets/f52b0566-e133-4e0c-b80a-aed3bceb7bb6" />
**cursor over dashboard**
<img width="1208" height="766" alt="image" src="https://github.com/user-attachments/assets/e7ae2558-5540-45c7-b507-af68eb578a0d" />


<img width="1195" height="769" alt="image" src="https://github.com/user-attachments/assets/3dac1024-97cb-497c-9d99-f6ef399ead2b" />

**Under Construction**
<img width="1199" height="767" alt="image" src="https://github.com/user-attachments/assets/949b97e8-2670-4188-8a04-de964ee77ae5" />
<img width="1197" height="766" alt="image" src="https://github.com/user-attachments/assets/85e72eb9-f55b-4b74-ba81-7ae33891e184" />
<img width="1199" height="771" alt="image" src="https://github.com/user-attachments/assets/900523a4-2eed-4337-bfa6-0381a9e80526" />

---

# 📈 Current Features

- ✅ Habit Management
- ✅ Daily Habit Tracking
- ✅ Progress Dashboard
- ✅ Current Streak
- ✅ Calendar Navigation
- ✅ Daily Notes
- ✅ Responsive UI using QThread
- ✅ SQLite Database
- ✅ Modern Dark & Light Theme

---

# 🚀 Roadmap

### Completed

- [x] Habit Management
- [x] Daily Tracking
- [x] Calendar Navigation
- [x] Progress Dashboard
- [x] Current Streak
- [x] Daily Notes
- [x] Responsive Database Operations
- [x] Theme switching
- [x] Bottom status bar
- [x] Drag-and-drop habit reordering
- [x] Renaming/Updating habit names 
### Planned

- [ ] Persistent notes until completed
- [ ] Monthly Analytics
- [ ] Completion Graphs (Matplotlib)
- [ ] Longest Streak Statistics
- [ ] Habit-wise Analytics
- [ ] CSV Export
- [ ] Settings Page
---

# 📌 Version

**Current Version:** `v1.0.6`

### Recent Improvements

- Migrated from MySQL to SQLite3.
- Simplified project setup.
- Improved startup performance.
- Fixed streak restoration after application restart.
- Improved calendar synchronization.
- Correctly handles months with 28, 29, 30 and 31 days.
- Added calendar navigation support.
- Redesigned habit completion indicators (✓ / ✗).
- Prevented completion indicators before a habit's creation date.
- General UI and UX improvements.
- Enabled Theme Toggling
- Enabled Drag and Drop of Habits in the habits list(not the table)
- Enabled Renaming of habits in the habit list(not the table)
- Added animated navigation using QStackedWidget, QPropertyAnimation, and QRect.
- Added dedicated navigation sections for Stats, Streak, and Settings.
- Added temporary "Coming Soon" views for sections currently under development.
- Improved dashboard layout and user experience.

---

# 🎯 Objectives

This project was developed to improve productivity:

- Desktop application development with **PyQt5**
- Multithreading using **QThread**
- SQLite database design
- Qt's Signal-Slot architecture
- Responsive GUI programming
- Clean application architecture
- Object-oriented programming in Python

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future development.
