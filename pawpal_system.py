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

    def __post_init__(self):
        """Normalize and validate task fields after initialization."""
        self.priority = self.priority.lower()
        self.frequency = self.frequency.lower()
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
        return not self.completed and self.frequency in {"daily", "today", "once"}

    def describe(self):
        """Return a readable summary of this task."""
        status = "done" if self.completed else "pending"
        return (
            f"{self.description} ({self.duration_minutes} min, "
            f"{self.priority} priority, {self.frequency}, {status})"
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
        )

    def explain_choice(self, task):
        """Explain why a task was selected for the schedule."""
        return (
            f"Selected because it is {task.priority} priority and takes "
            f"{task.duration_minutes} minutes."
        )

    def complete_task(self, owner, pet_name, task_description):
        """Mark one task complete by owner, pet name, and task description."""
        pet = owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"No pet found named {pet_name}.")
        for task in pet.tasks:
            if task.description == task_description:
                task.mark_complete()
                return task
        raise ValueError(f"No task found for {pet_name}: {task_description}")


@dataclass
class DailySchedule:
    date: str
    owner: Owner
    scheduled_items: list = field(default_factory=list)
    skipped_tasks: list = field(default_factory=list)

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

        return "\n".join(lines)


CareTask = Task
