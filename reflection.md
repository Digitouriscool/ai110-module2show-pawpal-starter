# PawPal+ Project Reflection

## 1. System Design

A user should be able to add basic user and pet information. Add or edit pet care tasks, such as walks, feeding, medications, and grooming. They should be able to generate and view a daily schedule that prioritizes tasks based on time, priority, and preferences.

**a. Initial design**

My initial UML design focuses on the core backend objects needed to plan daily pet care. I included an `Owner` class to store the owner's name, available time, preferences, and pets. I included a `Pet` class to store pet details such as name, species, breed, age, and care needs.

I also included a task class to represent individual tasks like feeding, walks, and grooming. In the final code this became `Task`, which stores the description, duration, priority, frequency, preferred time, due date, and completion status. The `Scheduler` class is responsible for sorting tasks by priority, checking whether they fit within the owner's available time, detecting preferred-time conflicts, and building a daily plan.

To represent the result of the scheduling process, I included a `DailySchedule` class that stores selected scheduled items, skipped tasks, and conflict warnings.

**b. Design changes**

My design changed during implementation. I originally planned separate `CareTask` and `ScheduleItem` classes, but I simplified the model by using one `Task` class and storing scheduled items as dictionaries inside `DailySchedule`. That kept the code easier to connect to both the CLI demo and Streamlit table output.

I also added fields and methods that were not in the first UML draft, including `due_date`, `completed`, `create_next_occurrence()`, `sort_by_time()`, `filter_tasks()`, and `detect_conflicts()`. These changes happened after testing the scheduler and realizing that recurring tasks, completed tasks, and conflict warnings were important parts of the user experience.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers priority, preferred time, task duration, completion status, due date, frequency, and the owner's available minutes. It schedules incomplete tasks that are required today, sorts them by priority first, then preferred time, then duration, and skips tasks that do not fit into the remaining available time.

I decided priority and available time mattered most because a pet owner needs critical care tasks, such as feeding or medication, to appear before lower-priority tasks. Preferred time matters too, but it should not outrank urgency. Due date and completion status prevent the scheduler from showing tasks that are already done or not due yet.

**b. Tradeoffs**

One tradeoff my scheduler makes is in the conflict detection algorithm. It checks each task's preferred start time and duration to see whether two preferred time windows overlap, then returns warning messages instead of blocking the schedule or crashing the program. This is simple and readable, but it does not automatically resolve the conflict or move one task to a better time.

I asked my AI coding assistant how this algorithm could be simplified for readability or performance. A more Pythonic suggestion was to use `itertools.combinations()` to compare every pair of tasks. That version was shorter, but I decided to keep the current nested-loop version because it is easier to follow while I am still developing and debugging the scheduler. For this project, clear logic is more useful than a slightly shorter implementation.

This tradeoff is reasonable because PawPal+ is a small scheduling app. A pet owner mainly needs to know when two tasks compete for the same time, not necessarily have the app solve every conflict automatically yet.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant for several phases: brainstorming the object model, drafting the Mermaid UML, generating dataclass skeletons, filling in scheduler logic, adding tests, updating the Streamlit UI, and reviewing the final README and UML. The most effective features were automatic code editing, fast review of relationships between classes, and test-focused suggestions.

For building the scheduler, the most useful AI features were asking for small algorithm ideas and then turning those into methods one at a time. Prompts like "how should the Scheduler retrieve all tasks from the Owner's pets?" helped me keep the design clean. The answer led to `Owner.get_all_tasks()`, which gives the scheduler one clear way to access pet data without reaching too deeply into each object.

**b. Judgment and verification**

One AI suggestion I modified was the idea to introduce more separate helper classes for scheduled items and conflicts. That would have been more formal, but it also would have added complexity before the app needed it. I kept `DailySchedule` simple by storing scheduled items as dictionaries and conflict warnings as strings.

I also chose not to replace the conflict detection loop with a shorter `itertools.combinations()` version. The shorter version was valid, but the nested-loop version was easier to read and explain for this project. I verified the behavior with pytest, including a test that creates two tasks with the same preferred time and checks that the scheduler returns a conflict warning.

Using separate chat sessions or phases helped me stay organized because each conversation had a clear purpose. One phase focused on architecture and UML, another focused on implementation, another focused on algorithm improvements, and another focused on documentation. That separation made it easier to compare AI suggestions against the current goal instead of mixing design, code, and README decisions together.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding tasks to pets, recurring daily task creation, recurring weekly task creation, one-time task completion, chronological sorting by preferred time, and conflict detection. These tests were important because they cover the main behaviors a pet owner depends on: saving tasks, marking them done, generating future recurring tasks, organizing the day, and warning about overlapping task times.

**b. Confidence**

I am fairly confident in the scheduler for the project scope because the core behaviors are covered by tests and the CLI demo shows the scheduler working across multiple pets. I would rate my confidence as 4 out of 5.

If I had more time, I would test invalid preferred time formats, tasks with future due dates, owners with zero available minutes, duplicate pet names, large task lists, and schedules where several tasks have the same priority and preferred time.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the way the backend stayed modular. `Owner` manages pets, `Pet` manages tasks, `Task` handles completion and recurrence data, and `Scheduler` handles sorting, filtering, conflict detection, and schedule creation.

**b. What you would improve**

In another iteration, I would redesign time handling to use stronger time objects internally instead of relying on `HH:MM` strings. I would also add real availability windows, so an owner could say they are free from 8:00-9:00 and 17:00-18:00 instead of only giving total available minutes.

**c. Key takeaway**

The biggest lesson is that being the lead architect means I cannot just accept every AI-generated idea. The AI assistant was powerful for generating options, writing boilerplate, and spotting missing logic, but I still had to decide what belonged in the system. Good collaboration meant using AI to move faster while keeping ownership of the design boundaries, naming, tests, and tradeoffs.
