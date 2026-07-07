from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


PRIORITY_WEIGHTS = {
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    preferred_time: str = ""
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def __post_init__(self):
        """Normalize and validate task fields after initialization."""
        self.priority = self.priority.lower()
        self.frequency = self.frequency.lower()
        if isinstance(self.due_date, str):
            self.due_date = date.fromisoformat(self.due_date)
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than 0 minutes.")
        if self.priority not in PRIORITY_WEIGHTS:
            raise ValueError("Priority must be one of: high, medium, low.")

    @property
    def title(self):
        """Return the task description as a title alias."""
        return self.description

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.completed = False

    def get_priority_score(self):
        """Return the numeric score for this task's priority."""
        return PRIORITY_WEIGHTS[self.priority]

    def is_required_today(self):
        """Return whether this task should be scheduled today."""
        return (
            not self.completed
            and self.frequency in {"daily", "today", "once", "weekly"}
            and self.due_date <= date.today()
        )

    def create_next_occurrence(self):
        """Create the next due task for daily or weekly recurring tasks.

        Daily tasks are copied with a due date of tomorrow. Weekly tasks are
        copied with a due date one week from today. Non-recurring tasks return
        None so callers can skip adding a follow-up task.
        """
        if self.frequency == "daily":
            next_due_date = date.today() + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = date.today() + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            preferred_time=self.preferred_time,
            due_date=next_due_date,
        )

    def describe(self):
        """Return a readable summary of this task."""
        status = "done" if self.completed else "pending"
        return (
            f"{self.description} ({self.duration_minutes} min, "
            f"{self.priority} priority, {self.frequency}, due {self.due_date}, {status})"
        )


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    @property
    def care_needs(self):
        """Return this pet's tasks as care needs."""
        return self.tasks

    def add_task(self, task):
        """Add a task to this pet."""
        if not isinstance(task, Task):
            raise TypeError("Pet.add_task expects a Task object.")
        self.tasks.append(task)

    def add_care_need(self, task):
        """Add a care task using the care-needs alias."""
        self.add_task(task)

    def remove_task(self, description):
        """Remove and return a task by description."""
        for task in self.tasks:
            if task.description == description:
                self.tasks.remove(task)
                return task
        raise ValueError(f"No task found for {self.name}: {description}")

    def get_tasks(self):
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def get_pending_tasks(self):
        """Return this pet's incomplete tasks."""
        return [task for task in self.tasks if not task.completed]

    def get_profile(self):
        """Return a readable pet profile."""
        breed_text = f", {self.breed}" if self.breed else ""
        return f"{self.name} is a {self.age}-year-old {self.species}{breed_text}."


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner."""
        if not isinstance(pet, Pet):
            raise TypeError("Owner.add_pet expects a Pet object.")
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove and return a pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                return pet
        raise ValueError(f"No pet found named {pet_name}.")

    def get_pet(self, pet_name):
        """Return a pet by name, or None if it is not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed=False):
        """Return all tasks across this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                if include_completed or not task.completed:
                    all_tasks.append((pet, task))
        return all_tasks

    def update_preferences(self, preferences):
        """Replace the owner's preference list."""
        self.preferences = list(preferences)

    def set_available_time(self, minutes):
        """Set the owner's available care time in minutes."""
        if minutes < 0:
            raise ValueError("Available minutes cannot be negative.")
        self.available_minutes = minutes


@dataclass
class Scheduler:
    start_time: str = "08:00"
    priority_weights: dict = field(default_factory=lambda: dict(PRIORITY_WEIGHTS))

    def get_tasks_from_owner(self, owner):
        """Retrieve pending tasks from all pets owned by an owner."""
        return owner.get_all_tasks()

    def sort_tasks(self, pet_tasks):
        """Sort pet-task pairs by priority, preferred time, and duration."""
        return sorted(
            pet_tasks,
            key=lambda pet_task: (
                -self.priority_weights[pet_task[1].priority],
                pet_task[1].preferred_time or "99:99",
                pet_task[1].duration_minutes,
            ),
        )

    def sort_by_time(self, pet_tasks):
        """Return pet-task pairs sorted by the task's preferred HH:MM time.

        Because preferred times use zero-padded HH:MM strings, a normal string
        comparison sorts them in chronological order. Tasks without a preferred
        time are placed last.
        """
        return sorted(pet_tasks, key=lambda pet_task: pet_task[1].preferred_time or "99:99")

    def filter_tasks(self, pet_tasks, completed=None, pet_name=None):
        """Return pet-task pairs matching optional status and pet filters.

        The completed argument can be True or False. The pet_name argument is
        matched case-insensitively. If a filter is omitted, that filter is not
        applied.
        """
        filtered_tasks = pet_tasks

        if completed is not None:
            filtered_tasks = [
                (pet, task)
                for pet, task in filtered_tasks
                if task.completed == completed
            ]

        if pet_name is not None:
            filtered_tasks = [
                (pet, task)
                for pet, task in filtered_tasks
                if pet.name.lower() == pet_name.lower()
            ]

        return filtered_tasks

    def _preferred_time_window(self, task):
        """Return a task's preferred start/end datetimes for conflict checks.

        The start comes from preferred_time and the end is calculated by adding
        duration_minutes. Tasks with no preferred_time return None.
        """
        if not task.preferred_time:
            return None

        start = datetime.strptime(task.preferred_time, "%H:%M")
        end = start + timedelta(minutes=task.duration_minutes)
        return start, end

    def detect_conflicts(self, pet_tasks):
        """Return warnings for tasks whose preferred time windows overlap.

        This method is intentionally lightweight: it reports conflicts between
        required tasks but does not raise an error or reschedule anything.
        """
        warnings = []
        timed_tasks = []

        for pet, task in pet_tasks:
            if not task.is_required_today():
                continue
            time_window = self._preferred_time_window(task)
            if time_window is not None:
                timed_tasks.append((pet, task, *time_window))

        for index, first in enumerate(timed_tasks):
            first_pet, first_task, first_start, first_end = first
            for second in timed_tasks[index + 1:]:
                second_pet, second_task, second_start, second_end = second
                if first_start < second_end and second_start < first_end:
                    warnings.append(
                        "Warning: "
                        f"{first_pet.name}'s {first_task.description} "
                        f"({first_start.strftime('%H:%M')}-{first_end.strftime('%H:%M')}) "
                        "conflicts with "
                        f"{second_pet.name}'s {second_task.description} "
                        f"({second_start.strftime('%H:%M')}-{second_end.strftime('%H:%M')})."
                    )

        return warnings

    def fits_available_time(self, task, remaining_minutes):
        """Return whether a task fits in the remaining available time."""
        return task.duration_minutes <= remaining_minutes

    def build_schedule(self, owner, pet=None, tasks=None):
        """Build a daily schedule for an owner or a specific pet task list."""
        if pet is not None and tasks is not None:
            pet_tasks = [(pet, task) for task in tasks if not task.completed]
        else:
            pet_tasks = self.get_tasks_from_owner(owner)

        schedule = []
        skipped_tasks = []
        conflict_warnings = self.detect_conflicts(pet_tasks)
        remaining_minutes = owner.available_minutes
        current_time = datetime.strptime(self.start_time, "%H:%M")

        for pet_item, task in self.sort_tasks(pet_tasks):
            if task.is_required_today() and self.fits_available_time(task, remaining_minutes):
                start = current_time.strftime("%H:%M")
                current_time += timedelta(minutes=task.duration_minutes)
                end = current_time.strftime("%H:%M")
                schedule.append(
                    {
                        "pet": pet_item.name,
                        "task": task,
                        "start_time": start,
                        "end_time": end,
                        "reason": self.explain_choice(task),
                    }
                )
                remaining_minutes -= task.duration_minutes
            else:
                skipped_tasks.append((pet_item, task))

        return DailySchedule(
            date=date.today().isoformat(),
            owner=owner,
            scheduled_items=schedule,
            skipped_tasks=skipped_tasks,
            conflict_warnings=conflict_warnings,
        )

    def explain_choice(self, task):
        """Explain why a task was selected for the schedule."""
        return (
            f"Selected because it is {task.priority} priority and takes "
            f"{task.duration_minutes} minutes."
        )

    def complete_task(self, owner, pet_name, task_description):
        """Mark a task complete and add its next recurring occurrence if needed.

        Daily and weekly tasks create a new incomplete Task with the next due
        date. One-time tasks are only marked complete.
        """
        pet = owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"No pet found named {pet_name}.")
        for task in pet.tasks:
            if task.description == task_description:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return task
        raise ValueError(f"No task found for {pet_name}: {task_description}")


@dataclass
class DailySchedule:
    date: str
    owner: Owner
    scheduled_items: list = field(default_factory=list)
    skipped_tasks: list = field(default_factory=list)
    conflict_warnings: list = field(default_factory=list)

    def add_item(self, item):
        """Add an item to the daily schedule."""
        self.scheduled_items.append(item)

    def add_skipped_task(self, pet_task):
        """Add a pet-task pair to the skipped task list."""
        self.skipped_tasks.append(pet_task)

    def total_scheduled_minutes(self):
        """Return the total minutes scheduled for the day."""
        return sum(item["task"].duration_minutes for item in self.scheduled_items)

    def format_plan(self):
        """Return the daily schedule as terminal-friendly text."""
        lines = [f"Daily plan for {self.owner.name} on {self.date}:"]

        if not self.scheduled_items:
            lines.append("  No tasks scheduled.")

        for item in self.scheduled_items:
            task = item["task"]
            lines.append(
                f"  {item['start_time']}-{item['end_time']} | "
                f"{item['pet']}: {task.description} "
                f"({task.duration_minutes} min, {task.priority})"
            )

        if self.skipped_tasks:
            lines.append("Skipped tasks:")
            for pet, task in self.skipped_tasks:
                lines.append(f"  {pet.name}: {task.description}")

        if self.conflict_warnings:
            lines.append("Warnings:")
            for warning in self.conflict_warnings:
                lines.append(f"  {warning}")

        return "\n".join(lines)


CareTask = Task
