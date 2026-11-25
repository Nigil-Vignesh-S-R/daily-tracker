# Daily Tracker
Daily Tracker is a modern desktop habit-tracking application built with **Python**, **PyQt5**, and **SQLite3**. It helps users build consistent routines by allowing them to create habits, track daily progress, maintain streaks, and write daily notes through a clean and responsive desktop interface.

Unlike web-based habit trackers, Daily Tracker stores all data locally using SQLite, making it lightweight, portable, and easy to set up—no external database server is required.

---

# Features

## Habit Management

- Create and delete habits with ease.
- Prevents duplicate habit entries.
- Input validation for reliable data.
- Instant UI updates after modifications.
- Preserves the creation date of every habit.
---

## Daily Habit Tracking

- Mark habits as completed for the current day.
- Completion history is permanently stored.
- Only today's entries are editable.
- Browse previous and upcoming months using the integrated calendar.
- Color-coded completion indicators (✓ Completed / ✗ Incomplete).
- Completion indicators are only shown from a habit's creation date onward.
---

## Progress Dashboard

- Live completion percentage.
- Progress bar with visual feedback.
- Completed habits vs total habits.
- Statistics update automatically.

---

## Streak Tracking

- Automatically calculates your current streak.
- Restores streak correctly after restarting the application.
- Encourages consistency through daily progress.

> **Consistency Beats Intensity.**

---

## Interactive Calendar

- Navigate seamlessly between months.
- Automatically synchronizes with the habit table.
- Supports months with 28, 29, 30, and 31 days.
- Review previous completion history effortlessly.

---

## Daily Notes

- Write notes for each day.
- Automatically saves your notes.
- Loads previously saved notes when reopening the application.

---

## Local SQLite Database

- Stores habits, completion records, and notes locally.
- No database installation required.
- Lightweight and portable.
- Uses relational tables with foreign key support.
- Clean separation between the user interface and database layer.

---

## Stats & Streak Analytics

- Stats page: today's completion donut, monthly completion chart, 7-day completion rate, and best performing habit.
- Streak page: longest streak, current streak, best day, best week, and per-habit streak bars.
- Charts built with Matplotlib and follow the active theme.
- Analytics are computed in background threads, so the interface stays responsive.
- Pages reload only when your data changes.

---

## Responsive User Experience

- Database operations run in background threads using **QThread**.
- Prevents the interface from freezing during database operations.
- Uses Qt's signal-slot mechanism for real-time updates.
- Smooth and responsive desktop experience.

---

## Modern Desktop Interface

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

# Tech Stack

- Python
- PyQt5
- SQLite3
- pandas
- Matplotlib
- Qt Signals & Slots
- QThread

---

# Installation

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

   ## Download (Windows)

   Get the latest build from the [Releases page](https://github.com/Nigil-Vignesh-S-R/daily-tracker/releases),
   unzip it, and run `DailyTracker.exe`. No Python needed.

---
# Screenshots
### Dark theme
<img width="1200" height="750" alt="image" src="https://github.com/user-attachments/assets/90f73e88-ed3b-46ba-8caa-071773cedf22" />

**double clicks waking**
<img width="1193" height="750" alt="image" src="https://github.com/user-attachments/assets/6fdb2fe2-d109-482a-810a-d2a190ae6a2f" />

<img width="1198" height="750" alt="image" src="https://github.com/user-attachments/assets/2c7a8c02-6f27-4abe-b9b6-219de32c6d99" />

**clicks ok/press enter**
<img width="1202" height="749" alt="image" src="https://github.com/user-attachments/assets/1b213863-1f2b-4446-8e56-c09f000cb62e" />

**cursor over dashboard**
<img width="1200" height="749" alt="image" src="https://github.com/user-attachments/assets/88e3a4e2-77ce-474e-8913-afa23684c5dc" />
<img width="1195" height="748" alt="image" src="https://github.com/user-attachments/assets/58e5d596-a804-47de-8398-d0a6744098cd" />
<img width="1198" height="753" alt="image" src="https://github.com/user-attachments/assets/f073d6d5-a04f-4b85-9df5-065473c58e86" />
<img width="1198" height="754" alt="image" src="https://github.com/user-attachments/assets/6a06de2a-def2-4b70-87f8-c79048e75090" />

### Light Theme
<img width="1197" height="751" alt="image" src="https://github.com/user-attachments/assets/03b1ebd5-a4f5-4df6-a96d-30d1bba4383a" />
<img width="1202" height="748" alt="image" src="https://github.com/user-attachments/assets/1723aba7-119d-475f-83fe-a3ffdbdc77af" />
<img width="1200" height="750" alt="image" src="https://github.com/user-attachments/assets/719bb415-e29e-4fe4-89d1-e5c336887fd0" />
<img width="1200" height="748" alt="image" src="https://github.com/user-attachments/assets/c555410a-076d-4e56-bd7c-4f4895822cb3" />

---

# Current Features

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

# Roadmap

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

# Version

**Current Version:** `v1.0.9`

### Recent Improvements

- Added the Stats page (completion donut, monthly chart, 7-day rate, best habit)
- Streak page now shows best day, best week, and per-habit streak bars
- Faster Streak page loading and fixes for chart and layout issues

---

# Objectives

This project was developed to improve productivity:

- Desktop application development with **PyQt5**
- Multithreading using **QThread**
- SQLite database design
- Qt's Signal-Slot architecture
- Responsive GUI programming
- Clean application architecture
- Object-oriented programming in Python

---

## Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future development.

**Author:** S R Nigil Vignesh
