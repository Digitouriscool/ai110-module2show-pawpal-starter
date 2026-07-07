# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app and Python scheduling system that helps pet owners plan daily care tasks across multiple pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

The app combines an object-oriented Python backend with a Streamlit interface and a CLI demo.

## Features

- Add and manage multiple pets for one owner.
- Add pet care tasks with duration, priority, frequency, preferred time, and completion status.
- Generate today's schedule from all pets owned by the user.
- Sort tasks by priority, preferred time, and duration.
- Sort task lists chronologically by preferred time.
- Filter tasks by completion status or pet name.
- Skip tasks that do not fit within the owner's available care time.
- Detect preferred-time conflicts and show warning messages.
- Create the next occurrence for completed daily and weekly recurring tasks.
- Exclude completed tasks from today's schedule while still allowing them to appear in full task views.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run The CLI Demo

```bash
python main.py
```

### Run The Streamlit App

```bash
streamlit run app.py
```

## 🖥️ Sample Output

Terminal output from running `python main.py`:

```
Tasks Sorted by Preferred Time
==============================
07:30 | Luna: Refresh water bowl (done)
08:00 | Mochi: Morning walk (pending)
09:00 | Mochi: Breakfast (pending)
09:00 | Luna: Give medication (pending)
17:00 | Mochi: Brush coat (pending)
18:00 | Luna: Clean litter box (pending)
19:00 | Mochi: Wash bedding (pending)

Pending Tasks
=============
Mochi: Brush coat
Mochi: Morning walk
Mochi: Breakfast
Mochi: Wash bedding
Luna: Clean litter box
Luna: Give medication

Luna's Tasks
============
Luna: Clean litter box (pending)
Luna: Give medication (pending)
Luna: Refresh water bowl (done)

Today's Schedule
================
Daily plan for Jordan on 2026-07-06:
  08:00-08:30 | Mochi: Morning walk (30 min, high)
  08:30-08:40 | Mochi: Breakfast (10 min, high)
  08:40-08:50 | Luna: Give medication (10 min, high)
  08:50-09:10 | Luna: Clean litter box (20 min, medium)
Skipped tasks:
  Mochi: Wash bedding
  Mochi: Brush coat
Warnings:
  Warning: Mochi's Breakfast (09:00-09:10) conflicts with Luna's Give medication (09:00-09:10).

Recurring Tasks Created After Completion
========================================
Mochi: Morning walk next due on 2026-07-07
Mochi: Wash bedding next due on 2026-07-13
```

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The tests cover task completion, adding tasks to pets, recurring daily and weekly task creation, one-time task completion, chronological sorting by preferred time, and conflict detection for duplicate preferred times.

Successful test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/digito/Documents/codepath/ai110/week4/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 7 items

tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.02s ===============================
```

Confidence Level: 4/5 stars

## 📐 Smarter Scheduling

PawPal+ includes several small scheduling algorithms that make the daily plan more useful than a manual task list.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority-based scheduling | `Scheduler.sort_tasks()`, `Scheduler.build_schedule()` | Builds the daily plan by sorting pending tasks by priority, preferred time, and duration. |
| Sorting by preferred time | `Scheduler.sort_by_time()` | Sorts pet-task pairs by each task's `preferred_time` in `HH:MM` format. Tasks without a preferred time are placed last. |
| Filtering by status or pet | `Scheduler.filter_tasks()` | Filters tasks by completion status, pet name, or both. This supports views such as "pending tasks" or "Luna's tasks." |
| Available-time filtering | `Scheduler.fits_available_time()`, `Scheduler.build_schedule()` | Skips tasks that do not fit inside the owner's remaining available minutes. |
| Conflict detection | `Scheduler._preferred_time_window()`, `Scheduler.detect_conflicts()` | Checks whether required tasks have overlapping preferred time windows and returns warning messages instead of crashing. |
| Recurring tasks | `Task.create_next_occurrence()`, `Scheduler.complete_task()` | When a daily or weekly task is completed, a new incomplete task is created with the next due date. Daily tasks use tomorrow; weekly tasks use one week from today. |
| Due-date checks | `Task.is_required_today()` | Only schedules incomplete tasks whose due date is today or earlier. |

## Demo Walkthrough

The Streamlit UI lets a pet owner set their available care time, add pets, add tasks for a selected pet, view all current tasks, and generate today's schedule. Pet and task data are stored in `st.session_state`, so button clicks do not erase the current owner, pets, or tasks during the browser session.

Example workflow:

1. Enter the owner's name and available care time for the day.
2. Add a pet with name, species, age, and optional breed.
3. Add a task for that pet with a duration, priority, frequency, and preferred time.
4. Repeat for additional pets and tasks.
5. Click **Generate schedule** to build today's plan from all pets.

The scheduler behavior shown in the app and CLI demo includes priority-based ordering, chronological sorting by preferred time, filtering pending tasks, skipping tasks when the owner runs out of available minutes, conflict warnings for overlapping preferred times, and daily or weekly recurrence creation after task completion.

Sample CLI output from `python main.py`:

```text
Tasks Sorted by Preferred Time
==============================
07:30 | Luna: Refresh water bowl (done)
08:00 | Mochi: Morning walk (pending)
09:00 | Mochi: Breakfast (pending)
09:00 | Luna: Give medication (pending)
17:00 | Mochi: Brush coat (pending)
18:00 | Luna: Clean litter box (pending)
19:00 | Mochi: Wash bedding (pending)

Pending Tasks
=============
Mochi: Brush coat
Mochi: Morning walk
Mochi: Breakfast
Mochi: Wash bedding
Luna: Clean litter box
Luna: Give medication

Luna's Tasks
============
Luna: Clean litter box (pending)
Luna: Give medication (pending)
Luna: Refresh water bowl (done)

Today's Schedule
================
Daily plan for Jordan on 2026-07-06:
  08:00-08:30 | Mochi: Morning walk (30 min, high)
  08:30-08:40 | Mochi: Breakfast (10 min, high)
  08:40-08:50 | Luna: Give medication (10 min, high)
  08:50-09:10 | Luna: Clean litter box (20 min, medium)
Skipped tasks:
  Mochi: Wash bedding
  Mochi: Brush coat
Warnings:
  Warning: Mochi's Breakfast (09:00-09:10) conflicts with Luna's Give medication (09:00-09:10).

Recurring Tasks Created After Completion
========================================
Mochi: Morning walk next due on 2026-07-07
Mochi: Wash bedding next due on 2026-07-13
```
