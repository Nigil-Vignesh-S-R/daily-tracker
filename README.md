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

<img width="1497" height="951" alt="image" src="https://github.com/user-attachments/assets/0f3abb6f-9d05-448b-b82b-80f855d9d9d8" />

<img width="1497" height="956" alt="image" src="https://github.com/user-attachments/assets/ca59d690-545d-44a7-8d4b-13ed8af6aac6" />



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

### Planned

- [ ] Drag-and-drop habit reordering
- [ ] Persistent notes until completed
- [ ] Monthly Analytics
- [ ] Completion Graphs (Matplotlib)
- [ ] Longest Streak Statistics
- [ ] Habit-wise Analytics
- [ ] CSV Export
- [ ] Settings Page
---

# 📌 Version

**Current Version:** `v1.0.3`

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
