from attributes import Attributes
from dataclasses import dataclass
from itertools import combinations

@dataclass
class Member:
    name: str
    attr: Attributes
    level: int
    job: str
    id: int = 0

    def __str__(self):
        return f"{self.id} {self.attr} {self.name}"

# Do NOT make this one immutable, because we will (probably)
#   need to toggle the is_available
@dataclass
class Mission:
    name: str
    requirements: Attributes
    level: int
    xp_reward: int
    is_available: bool

@dataclass
class Squad:
    id: str
    members: tuple[Member]
    attr: Attributes

    def __str__(self):
        return f"{self.id} {self.attr}"

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

        self.squads: dict[str, Squad] = dict()

    def craft_squad_id(self, selection: tuple[Member]) -> str:
        if len(selection) != 4:
            raise ValueError("Squad must have four (4) members")
        return f"{selection[0].id}{selection[1].id}{selection[2].id}{selection[3].id}"

    def build_squads(self) -> None:
        squads_have_been_built = len(self.squads) > 0
        if squads_have_been_built:
            # Then don't build them again.
            return
        
        for selection in combinations(self.members, 4):
            id = self.craft_squad_id(selection)
            members = selection

            attr_as_list = [m.attr for m in selection]
            attr = sum(attr_as_list, start=self.training_attr)

            self.squads[id] = Squad(id, members, attr)

        return


# INPUT DATA
#   Hardcoded for development, because I don't want to deal with 
#   the logic of Squadron Training Attributes
training_attr = Attributes(80, 160, 40)
max_training_attr = 280

#   And also, I didn't want to deal with how to architect my whole
#   project to deal with the CSV parsing etc etc.

members = [
    Member(id=1, attr=Attributes(90,23,53), name="Cecily", level=36, job="Gladiator"),
    Member(id=2, attr=Attributes(36,24,108), name="Nanasomi", level=37, job="Archer"),
    Member(id=3, attr=Attributes(102,24,42), name="Hastaloeya", level=37, job="Marauder"),
    Member(id=4, attr=Attributes(25,18,93), name="Ceaulie", level=21, job="Archer"),
    Member(id=5, attr=Attributes(54,32,64), name="Totodi", level=28, job="Pugilist"),
    Member(id=6, attr=Attributes(53,23,90), name="Inghilswys", level=36, job="Lancer"),
    Member(id=7, attr=Attributes(20,76,54), name="Sofine", level=28, job="Scholar"),
    Member(id=8, attr=Attributes(22,90,44), name="Nunulupa Tatalupa", level=31, job="Thaumaturge"),
]

#   Yes, I copy-pasted the CSV in the python file, and then I used
#   the multi-column cursor in Visual Studio Code.

missions = [
Mission(requirements=Attributes(165,170,150),name="Military Courier", level=1, xp_reward=7500, is_available=True),
Mission(requirements=Attributes(150,255,195),name="Outskirts Patrol", level=1, xp_reward=9000, is_available=True),
Mission(requirements=Attributes(155,195,250),name="Beastmen Recon", level=5, xp_reward=10500, is_available=True),
Mission(requirements=Attributes(305,210,130),name="Supply Wagon Escort", level=10, xp_reward=12000, is_available=True),
Mission(requirements=Attributes(320,145,225),name="Pest Eradication", level=15, xp_reward=13500, is_available=False),
Mission(requirements=Attributes(265,435,125),name="Frontline Support", level=20, xp_reward=15000, is_available=False),
Mission(requirements=Attributes(270,145,425),name="Officer Escort", level=20, xp_reward=16500, is_available=True),
Mission(requirements=Attributes(280,155,435),name="Border Patrol", level=25, xp_reward=19500, is_available=True),
Mission(requirements=Attributes(440,175,300),name="Stronghold Recon", level=30, xp_reward=22500, is_available=True),
Mission(requirements=Attributes(455,315,190),name="Search and Rescue", level=35, xp_reward=25500, is_available=True),
Mission(requirements=Attributes(170,480,310),name="Allied Maneuvers", level=35, xp_reward=27000, is_available=True),
]

sq = Squadron(members, missions, training_attr, max_training_attr)

print("Squadron Members:")
print(*sq.members, sep='\n')

sq.build_squads()
print("Squads:")
print(*sq.squads.values(), sep='\n')


