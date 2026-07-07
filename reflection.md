# PawPal+ Project Reflection

## 1. System Design

A user should be able to add basic user and pet information. Add or edit pet care tasks, such as walks, feeding, medications, and grooming. They should be able to generate and view a daily schedule that prioritizes tasks based on time, priority, and preferences.

**a. Initial design**

My initial UML design focuses on the core backend objects needed to plan daily pet care. I included an `Owner` class to store the owner's name, available time, preferences, and pets. I included a `Pet` class to store pet details such as name, species, breed, age, and care needs.

I also included a `CareTask` class to represent individual tasks like feeding, walks, and grooming. Each task stores its title, category, duration, priority, preferred time, and whether it repeats. The `Scheduler` class is responsible for sorting tasks by priority, checking whether they fit within the owner's available time, and building a daily plan.

To represent the result of the scheduling process, I included a `DailySchedule` class that stores the selected scheduled items and skipped tasks. Each scheduled task is represented by a `ScheduleItem`, which records the task, start time, end time, and explanation for why it was included.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
