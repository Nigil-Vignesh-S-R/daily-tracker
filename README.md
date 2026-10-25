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

## 📈 Stats & Streak Analytics

- Stats page: today's completion donut, monthly completion chart, 7-day completion rate, and best performing habit.
- Streak page: longest streak, current streak, best day, best week, and per-habit streak bars.
- Charts built with Matplotlib and follow the active theme.
- Analytics are computed in background threads, so the interface stays responsive.
- Pages reload only when your data changes.

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
- pandas
- Matplotlib
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

<img width="1197" height="766" alt="image" src="https://github.com/user-attachments/assets/ca797f4e-f70f-462e-aecf-518d692ba944" />

**double clicks waking**
<img width="1199" height="764" alt="image" src="https://github.com/user-attachments/assets/2887b5c7-dfc9-41a1-8894-54a50b6ec1bd" />
<img width="1193" height="757" alt="image" src="https://github.com/user-attachments/assets/bbdcf4e4-9a68-4905-be11-773203039b60" />

**clicks ok/press enter**
<img width="1201" height="764" alt="image" src="https://github.com/user-attachments/assets/aac00956-d035-472a-a39d-c16393965f21" />

**cursor over dashboard**
<img width="1198" height="766" alt="image" src="https://github.com/user-attachments/assets/e4377858-8314-4994-a385-e7f8daa3166c" />

<img width="1198" height="770" alt="image" src="https://github.com/user-attachments/assets/eb0cfb23-f3ad-4241-b3e5-9e7befc5b5f3" />

<img width="1194" height="767" alt="image" src="https://github.com/user-attachments/assets/dcac283a-e0e3-46e2-b40e-6bd0bb3c9941" />

<img width="1208" height="776" alt="image" src="https://github.com/user-attachments/assets/45cd31e2-b4b3-4b62-bf45-a6f4330b135f" />

<img width="1202" height="766" alt="image" src="https://github.com/user-attachments/assets/2f1d825a-e3ba-444c-a9c4-e2097af0164e" />

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
- ✅ Stats Page
- ✅ Streak Analytics

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
- [x] Settings Page
- [x] Longest Streak Statistics
- [x] Habit-wise Analytics
- [x] CSV Export
- [x] Monthly Analytics
- [x] Completion Graphs (Matplotlib)

---

# 📌 Version

**Current Version:** `v1.0.9`

### Recent Improvements

- Added the Stats page (completion donut, monthly chart, 7-day rate, best habit)
- Streak page now shows best day, best week, and per-habit streak bars
- Faster Streak page loading and fixes for chart and layout issues

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
