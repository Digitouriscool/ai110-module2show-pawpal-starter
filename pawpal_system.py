from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    preferences: list = field(default_factory=list)
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        pass

    def update_preferences(self, preferences):
        pass

    def set_available_time(self, minutes):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    care_needs: list = field(default_factory=list)

    def add_care_need(self, need):
        pass

    def get_profile(self):
        pass


@dataclass
class CareTask:
    title: str
    category: str
    duration_minutes: int
    priority: str
    preferred_time: str = ""
    recurring: bool = False

    def get_priority_score(self):
        pass

    def is_required_today(self):
        pass

    def describe(self):
        pass


@dataclass
class Scheduler:
    start_time: str = "08:00"
    priority_weights: dict = field(
        default_factory=lambda: {
            "high": 3,
            "medium": 2,
            "low": 1,
        }
    )

    def build_schedule(self, owner, pet, tasks):
        pass

    def sort_tasks(self, tasks):
        pass

    def fits_available_time(self, task, remaining_minutes):
        pass

    def explain_choice(self, task):
        pass


@dataclass
class DailySchedule:
    date: str
    pet: Pet
    owner: Owner
    scheduled_items: list = field(default_factory=list)
    skipped_tasks: list = field(default_factory=list)

    def add_item(self, item):
        pass

    def add_skipped_task(self, task):
        pass

    def total_scheduled_minutes(self):
        pass

    def format_plan(self):
        pass


@dataclass
class ScheduleItem:
    task: CareTask
    start_time: str
    end_time: str
    reason: str = ""

    def format_item(self):
        pass

    def overlaps_with(self, other):
        pass
