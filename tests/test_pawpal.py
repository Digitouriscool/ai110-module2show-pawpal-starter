import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


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
