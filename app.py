from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def pet_task_rows(pet_tasks):
    return [
        {
            "Pet": pet.name,
            "Task": task.description,
            "Duration": f"{task.duration_minutes} min",
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Preferred time": task.preferred_time or "Any time",
            "Due date": task.due_date.isoformat(),
            "Status": "Done" if task.completed else "Pending",
        }
        for pet, task in pet_tasks
    ]


def schedule_rows(schedule):
    return [
        {
            "Time": f"{item['start_time']}-{item['end_time']}",
            "Pet": item["pet"],
            "Task": item["task"].description,
            "Priority": item["task"].priority,
            "Duration": f"{item['task'].duration_minutes} min",
            "Why selected": item["reason"],
        }
        for item in schedule.scheduled_items
    ]


def skipped_task_rows(skipped_tasks):
    return [
        {
            "Pet": pet.name,
            "Task": task.description,
            "Duration": f"{task.duration_minutes} min",
            "Priority": task.priority,
            "Reason": "Completed, not due today, or does not fit available time",
        }
        for pet, task in skipped_tasks
    ]


st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planner that stores pets and tasks in your current
session and uses the scheduler from `pawpal_system.py` to build today's plan.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)
    st.session_state.owner.add_pet(Pet(name="Mochi", species="dog"))

owner = st.session_state.owner
scheduler = Scheduler()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available care time today (minutes)",
    min_value=1,
    max_value=480,
    value=max(owner.available_minutes, 1),
)

owner.name = owner_name
owner.set_available_time(int(available_minutes))

st.markdown("### Pets")
with st.form("add_pet_form"):
    pet_col1, pet_col2, pet_col3 = st.columns(3)
    with pet_col1:
        new_pet_name = st.text_input("Pet name", value="Mochi")
    with pet_col2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    with pet_col3:
        new_pet_age = st.number_input("Age", min_value=0, max_value=40, value=1)

    new_pet_breed = st.text_input("Breed", value="")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if owner.get_pet(new_pet_name):
        st.warning(f"{new_pet_name} is already in your pet list.")
    else:
        owner.add_pet(
            Pet(
                name=new_pet_name,
                species=new_pet_species,
                breed=new_pet_breed,
                age=int(new_pet_age),
            )
        )
        st.success(f"Added {new_pet_name}.")

if owner.pets:
    st.table(
        [
            {
                "name": pet.name,
                "species": pet.species,
                "breed": pet.breed,
                "age": pet.age,
                "tasks": len(pet.tasks),
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Tasks are stored in Streamlit session state through your Owner object.")

pet_names = [pet.name for pet in owner.pets]

if pet_names:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Pet", pet_names)
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input(
                "Duration (minutes)",
                min_value=1,
                max_value=240,
                value=20,
            )
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        frequency = st.selectbox("Frequency", ["daily", "weekly", "today", "once"])
        preferred_time_value = st.time_input("Preferred time", value=time(8, 0))
        preferred_time = preferred_time_value.strftime("%H:%M")
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        selected_pet = owner.get_pet(selected_pet_name)
        selected_pet.add_task(
            Task(
                description=task_title,
                duration_minutes=int(duration),
                frequency=frequency,
                priority=priority,
                preferred_time=preferred_time,
            )
        )
        st.success(f"Added {task_title} for {selected_pet.name}.")

all_pet_tasks = owner.get_all_tasks(include_completed=True)

if all_pet_tasks:
    st.write("Current tasks")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        status_filter = st.selectbox("Status", ["Pending", "All", "Completed"])
    with filter_col2:
        pet_filter = st.selectbox("Pet filter", ["All pets", *pet_names])
    with filter_col3:
        sort_mode = st.selectbox(
            "Sort tasks by",
            ["Scheduler priority", "Preferred time"],
        )

    completed_filter = {"Pending": False, "Completed": True}.get(status_filter)
    pet_name_filter = None if pet_filter == "All pets" else pet_filter
    visible_pet_tasks = scheduler.filter_tasks(
        all_pet_tasks,
        completed=completed_filter,
        pet_name=pet_name_filter,
    )

    if sort_mode == "Preferred time":
        visible_pet_tasks = scheduler.sort_by_time(visible_pet_tasks)
    else:
        visible_pet_tasks = scheduler.sort_tasks(visible_pet_tasks)

    if visible_pet_tasks:
        st.success(f"Showing {len(visible_pet_tasks)} task(s), sorted by {sort_mode.lower()}.")
        st.table(pet_task_rows(visible_pet_tasks))
    else:
        st.info("No tasks match the selected filters.")

    conflict_warnings = scheduler.detect_conflicts(owner.get_all_tasks())
    if conflict_warnings:
        st.warning(
            "Some required tasks have overlapping preferred times. Consider changing one preferred time before relying on today's plan."
        )
        for warning in conflict_warnings:
            st.warning(warning)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses the Owner object stored in st.session_state.")

if st.button("Generate schedule"):
    schedule = scheduler.build_schedule(owner)
    if schedule.conflict_warnings:
        st.warning(
            "Schedule conflict detected. The plan can still be generated, but these tasks compete for the same preferred time."
        )
        for warning in schedule.conflict_warnings:
            st.warning(warning)

    if schedule.scheduled_items:
        st.success(
            f"Scheduled {len(schedule.scheduled_items)} task(s) for {schedule.total_scheduled_minutes()} minutes."
        )
        st.table(schedule_rows(schedule))
    else:
        st.info("No tasks were scheduled. Add pending tasks due today or increase available care time.")

    if schedule.skipped_tasks:
        st.warning("Some tasks were skipped.")
        st.table(skipped_task_rows(schedule.skipped_tasks))
