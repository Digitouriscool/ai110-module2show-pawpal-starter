import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task(description="Morning walk", duration_minutes=30)

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Give breakfast", duration_minutes=10)

    starting_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == starting_count + 1


def test_completing_daily_task_creates_next_occurrence():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Morning walk", duration_minutes=30, frequency="daily")
    pet.add_task(task)
    owner.add_pet(pet)

    Scheduler().complete_task(owner, "Mochi", "Morning walk")

    next_task = pet.tasks[1]
    assert task.completed is True
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_completing_weekly_task_creates_next_occurrence():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Trim nails", duration_minutes=20, frequency="weekly")
    pet.add_task(task)
    owner.add_pet(pet)

    Scheduler().complete_task(owner, "Mochi", "Trim nails")

    next_task = pet.tasks[1]
    assert task.completed is True
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(weeks=1)


def test_completing_once_task_does_not_create_next_occurrence():
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="cat")
    task = Task(description="Vet appointment", duration_minutes=60, frequency="once")
    pet.add_task(task)
    owner.add_pet(pet)

    Scheduler().complete_task(owner, "Luna", "Vet appointment")

    assert task.completed is True
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_tasks_in_chronological_order():
    pet = Pet(name="Mochi", species="dog")
    morning_walk = Task(
        description="Morning walk",
        duration_minutes=30,
        preferred_time="08:00",
    )
    dinner = Task(
        description="Dinner",
        duration_minutes=10,
        preferred_time="18:00",
    )
    medication = Task(
        description="Medication",
        duration_minutes=5,
        preferred_time="12:00",
    )

    sorted_tasks = Scheduler().sort_by_time(
        [
            (pet, dinner),
            (pet, morning_walk),
            (pet, medication),
        ]
    )

    assert [task.description for _pet, task in sorted_tasks] == [
        "Morning walk",
        "Medication",
        "Dinner",
    ]


def test_scheduler_warns_when_preferred_times_conflict():
    owner = Owner(name="Jordan", available_minutes=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    dog.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            priority="high",
            preferred_time="09:00",
        )
    )
    cat.add_task(
        Task(
            description="Give medication",
            duration_minutes=10,
            priority="high",
            preferred_time="09:00",
        )
    )
    owner.add_pet(dog)
    owner.add_pet(cat)

    schedule = Scheduler().build_schedule(owner)

    assert len(schedule.conflict_warnings) == 1
    assert "conflicts with" in schedule.conflict_warnings[0]
    assert "Breakfast" in schedule.conflict_warnings[0]
    assert "Give medication" in schedule.conflict_warnings[0]
