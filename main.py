from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    owner = Owner(name="Jordan", available_minutes=75)

    dog = Pet(name="Mochi", species="dog", breed="Corgi", age=4)
    cat = Pet(name="Luna", species="cat", breed="Tabby", age=6)

    dog.add_task(
        Task(
            description="Brush coat",
            duration_minutes=15,
            frequency="daily",
            priority="low",
            preferred_time="17:00",
        )
    )
    dog.add_task(
        Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            priority="high",
            preferred_time="08:00",
        )
    )
    dog.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            frequency="daily",
            priority="high",
            preferred_time="09:00",
        )
    )
    dog.add_task(
        Task(
            description="Wash bedding",
            duration_minutes=25,
            frequency="weekly",
            priority="medium",
            preferred_time="19:00",
        )
    )
    cat.add_task(
        Task(
            description="Clean litter box",
            duration_minutes=20,
            frequency="daily",
            priority="medium",
            preferred_time="18:00",
        )
    )
    cat.add_task(
        Task(
            description="Give medication",
            duration_minutes=10,
            frequency="daily",
            priority="high",
            preferred_time="09:00",
        )
    )
    cat.add_task(
        Task(
            description="Refresh water bowl",
            duration_minutes=5,
            frequency="daily",
            priority="medium",
            preferred_time="07:30",
            completed=True,
        )
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(start_time="08:00")
    all_tasks = owner.get_all_tasks(include_completed=True)
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    pending_tasks = scheduler.filter_tasks(all_tasks, completed=False)
    luna_tasks = scheduler.filter_tasks(all_tasks, pet_name="Luna")
    schedule = scheduler.build_schedule(owner)

    print("Tasks Sorted by Preferred Time")
    print("==============================")
    for pet, task in sorted_by_time:
        status = "done" if task.completed else "pending"
        print(f"{task.preferred_time} | {pet.name}: {task.description} ({status})")

    print()
    print("Pending Tasks")
    print("=============")
    for pet, task in pending_tasks:
        print(f"{pet.name}: {task.description}")

    print()
    print("Luna's Tasks")
    print("============")
    for pet, task in luna_tasks:
        status = "done" if task.completed else "pending"
        print(f"{pet.name}: {task.description} ({status})")

    print()
    print("Today's Schedule")
    print("================")
    print(schedule.format_plan())

    scheduler.complete_task(owner, "Mochi", "Morning walk")
    scheduler.complete_task(owner, "Mochi", "Wash bedding")
    recurring_tasks = [
        task
        for task in dog.tasks
        if not task.completed and task.description in {"Morning walk", "Wash bedding"}
    ]

    print()
    print("Recurring Tasks Created After Completion")
    print("========================================")
    for task in recurring_tasks:
        print(f"{dog.name}: {task.description} next due on {task.due_date}")


if __name__ == "__main__":
    main()
