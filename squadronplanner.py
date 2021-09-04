from attributes import Attributes
from dataclasses import dataclass

@dataclass
class Member:
    name: str
    attr: Attributes
    level: int
    job: str

@dataclass
class Mission:
    name: str
    requirements: Attributes
    level: int
    xp_reward: int

class Squadron:
    def __init__(
            self, 
            members: list[Member],
            missions: list[Mission],
            training_attr: Attributes,
            max_training_attr: int,
            remaining_daily_courses: int=3
        ):
        self.members = members
        self.missions = missions
        self.training_attr = training_attr
        self.max_training_attr = max_training_attr
        self.remaining_daily_courses = remaining_daily_courses
