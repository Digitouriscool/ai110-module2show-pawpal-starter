from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    owner = Owner(name="Jordan", available_minutes=75)

    dog = Pet(name="Mochi", species="dog", breed="Corgi", age=4)
    cat = Pet(name="Luna", species="cat", breed="Tabby", age=6)

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
            description="Brush coat",
            duration_minutes=15,
            frequency="daily",
            priority="low",
            preferred_time="17:00",
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
            description="Clean litter box",
            duration_minutes=20,
            frequency="daily",
            priority="medium",
            preferred_time="18:00",
        )
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(start_time="08:00")
    schedule = scheduler.build_schedule(owner)

    print("Today's Schedule")
    print("================")
    print(schedule.format_plan())


if __name__ == "__main__":
    main()
