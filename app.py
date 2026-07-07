import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

        frequency = st.selectbox("Frequency", ["daily", "today", "once"])
        preferred_time = st.text_input("Preferred time", value="08:00")
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
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
                "preferred_time": task.preferred_time,
                "completed": task.completed,
            }
            for pet, task in all_pet_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses the Owner object stored in st.session_state.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    schedule = scheduler.build_schedule(owner)
    st.text(schedule.format_plan())
