# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Terminal output from running `python main.py`:

```
Today's Schedule
================
Daily plan for Jordan on 2026-07-06:
  08:00-08:30 | Mochi: Morning walk (30 min, high)
  08:30-08:40 | Luna: Give medication (10 min, high)
  08:40-09:00 | Luna: Clean litter box (20 min, medium)
  09:00-09:15 | Mochi: Brush coat (15 min, low)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
