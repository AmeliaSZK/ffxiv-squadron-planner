from attributes import Attributes
from dataclasses import dataclass, field
from itertools import combinations, islice
from operator import attrgetter
from typing import Optional
from enum import Enum, unique

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

    def __str__(self):
        return f"Lv. {self.level:2}    {self.name} "

@dataclass
class Squad:
    id: str
    members: tuple[Member]
    attr: Attributes = field(init=False)
    aggregate: int = field(init=False)

    def __post_init__(self):
        attr_as_list = [member.attr for member in self.members]
        self.attr = sum(attr_as_list, start=Attributes())
        self.aggregate = self.attr.aggregate()

    def __str__(self):
        return f"{self.id} {self.attr} (aggr={self.aggregate})"

@unique
class Course(Enum):
    PHY = 1
    MEN = 2
    TAC = 3
    PHY_MEN = 4
    PHY_TAC = 5
    MEN_TAC = 6


@dataclass
class TrainingProgram:
    """All calculations assume that individuals training attributes
    must always be a multiple of 20.
    """
    courses: tuple[Course]
    initial_attr: Attributes
    max_aggregate: int
    is_redundant: bool = field(init=False)
    attr: Attributes = field(init=False)

    def __post_init__(self):
        self.is_redundant, self.attr = self.calculate_program()

    def calculate_one_course(
        self, 
        base_attr: Attributes, 
        course: Course
    ) -> Attributes:
        # Base data:
        if course == Course.PHY:
            intended_delta = Attributes(40, 0, 0)
        elif course == Course.MEN:
            intended_delta = Attributes(0, 40, 0)
        elif course == Course.TAC:
            intended_delta = Attributes(0, 0, 40)
        elif course == Course.PHY_MEN:
            intended_delta = Attributes(20, 20, 0)
        elif course == Course.PHY_TAC:
            intended_delta = Attributes(20, 0, 20)
        elif course == Course.MEN_TAC:
            intended_delta = Attributes(0, 20, 20)
        # "delta" means "change in..."
        # so "intended_delta" means "intended change to base attributes"

        # When we can apply the intended delta
        # Best case scenario, but very rare
        if base_attr.has_room_for_delta(intended_delta, self.max_aggregate):
            return base_attr + intended_delta

        # When we start at max_aggregate
        # Most common scenario
        if course == Course.PHY:
            balanced_delta = Attributes(40, -20, -20)
        elif course == Course.MEN:
            balanced_delta = Attributes(-20, 40, -20)
        elif course == Course.TAC:
            balanced_delta = Attributes(-20, -20, 40)
        elif course == Course.PHY_MEN:
            balanced_delta = Attributes(20, 20, -40)
        elif course == Course.PHY_TAC:
            balanced_delta = Attributes(20, -40, 20)
        elif course == Course.MEN_TAC:
            balanced_delta = Attributes(-40, 20, 20)
        
        if base_attr.has_room_for_delta(balanced_delta, self.max_aggregate):
            return base_attr + balanced_delta
        
        # If the function has still not returned, 
        #   then one attribute will either go negative,
        #   or break the max after the delta.
        # Since we assume all individual attributes are multiples of 20,
        #   we have these solutions:
        #   A) Reduce the delta.              Eg: ( 40/  0/  0) -> ( 20/  0/ 0)
        #   B) Reduce the balancing.          Eg: (-40/ 20/ 20) -> (-20/ 20/20)
        #   C) Balance on a single attribute. Eg: ( 40/-20/-20) -> ( 40/-40/ 0)
        #   D) (next section)
        # Because of the "multiples of 20" rule, not all of these solution can
        #   be used on all courses.
        # Because the goal of training courses is to *increase* the stats, 
        #   we will prioritize the solution with the biggest increases.
        #
        # NB.: This Python script attempts to emulate the in-game rules,
        #   and none of our rules & assumptions have been tested yet.

        reduced_delta = None
        reduced_balancing_delta = None
        reduced_delta_1 = None
        reduced_delta_2 = None
        rebalanced_1_delta = None
        rebalanced_2_delta = None
        if course == Course.PHY:
            reduced_delta = Attributes(20, 0, 0)
            rebalanced_1_delta = Attributes(40, -40,   0)
            rebalanced_2_delta = Attributes(40,   0, -40)
        elif course == Course.MEN:
            reduced_delta = Attributes(0, 20, 0)
            rebalanced_1_delta = Attributes(-40, 40,   0)
            rebalanced_2_delta = Attributes(  0, 40, -40)
        elif course == Course.TAC:
            reduced_delta = Attributes(0, 0, 20)
            rebalanced_1_delta = Attributes(-40,   0, 40)
            rebalanced_2_delta = Attributes(  0, -40, 40)
        elif course == Course.PHY_MEN:
            reduced_balancing_delta = Attributes(20, 20, -20) 
            reduced_delta_1 = Attributes(20, 0, 0) 
            reduced_delta_2 = Attributes(0, 20, 0) 
            rebalanced_1_delta = Attributes(20, 0, -20) 
            rebalanced_2_delta = Attributes(0, 20, -20) 
        elif course == Course.PHY_TAC:
            reduced_balancing_delta = Attributes(20, -20, 20) 
            reduced_delta_1 = Attributes(20, 0, 0) 
            reduced_delta_2 = Attributes(0, 0, 20) 
            rebalanced_1_delta = Attributes(20, -20, 0) 
            rebalanced_2_delta = Attributes(0, -20, 20) 
        elif course == Course.MEN_TAC:
            reduced_balancing_delta = Attributes(-20, 20, 20) 
            reduced_delta_1 = Attributes(0, 20, 0) 
            reduced_delta_2 = Attributes(0, 0, 20) 
            rebalanced_1_delta = Attributes(-20, 20, 0) 
            rebalanced_2_delta = Attributes(-20, 0, 20) 
        
        # The order of this list is important, because that's where
        #   the priorities are defined.
        all_deltas = [
            reduced_delta, 
            reduced_balancing_delta, 
            reduced_delta_1,
            reduced_delta_2,
            rebalanced_1_delta, 
            rebalanced_2_delta]
        
        for delta in all_deltas:
            if delta is not None and base_attr.has_room_for_delta(delta, self.max_aggregate):
                return base_attr + delta


        # If all attempts have failed, then the course cannot improve anything,
        #   so we return what we started with.
        return base_attr

    def calculate_program(self) -> tuple[bool, Attributes]:
        is_redundant = False
        attr = self.initial_attr

        for course in self.courses:
            new_attr = self.calculate_one_course(attr, course)

            course_was_useless = new_attr == attr
            if course_was_useless:
                is_redundant = True            
            attr = new_attr
        return is_redundant, attr




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

        self.squads: list[Squad] = list()
        self.squads_by_asc_aggr: list[Squad] = list()
        self.squads_by_des_aggr: list[Squad] = list()
        self.squads_by_asc_phy: list[Squad] = list()
        self.squads_by_des_phy: list[Squad] = list()
        self.squads_by_asc_men: list[Squad] = list()
        self.squads_by_des_men: list[Squad] = list()
        self.squads_by_asc_tac: list[Squad] = list()
        self.squads_by_des_tac: list[Squad] = list()

    def craft_squad_id(self, selection: tuple[Member]) -> str:
        if len(selection) != 4:
            raise ValueError("Squad must have four (4) members")
        return f"{selection[0].id}{selection[1].id}{selection[2].id}{selection[3].id}"

    def build_squads(self) -> None:
        squads_have_been_built = len(self.squads) > 0
        if squads_have_been_built:
            # Then don't build them again.
            return
        
        # Build squads, "sorted" by member ID
        for selection in combinations(self.members, 4):
            id = self.craft_squad_id(selection)
            members = selection
            self.squads.append(Squad(id, members))
        
        # Build the different sortings of the squads.
        #   We are storing them all in memory, because
        #   squads are at most 4 members, and there can
        #   be at most 8 members in the squadron.
        #   
        #   There are only 70 ways to choose 4 items
        #   from a set of 8. (https://www.wolframalpha.com/input/?i=8+choose+4)
        #
        #   We believe that a list of 70 items is negligible.
        #
        #   Also, we are assuming that Python will only create 70 Squad objects,
        #   and that all the lists will only contain pointers to these same
        #   70 objects. That might be wrong.
        self.squads_by_asc_aggr = sorted(self.squads, key=attrgetter('aggregate'))
        self.squads_by_des_aggr = sorted(self.squads, key=attrgetter('aggregate'), reverse=True)
        self.squads_by_asc_phy  = sorted(self.squads, key=attrgetter('attr.phy', 'aggregate'))
        self.squads_by_des_phy  = sorted(self.squads, key=attrgetter('attr.phy', 'aggregate'), reverse=True)
        self.squads_by_asc_men  = sorted(self.squads, key=attrgetter('attr.men', 'aggregate'))
        self.squads_by_des_men  = sorted(self.squads, key=attrgetter('attr.men', 'aggregate'), reverse=True)
        self.squads_by_asc_tac  = sorted(self.squads, key=attrgetter('attr.tac', 'aggregate'))
        self.squads_by_des_tac  = sorted(self.squads, key=attrgetter('attr.tac', 'aggregate'), reverse=True)


        return

    def list_doable_missions(self, training_attr: Attributes):
        return
    
    def iter_qualifying_squads_for_mission(
        self, 
        mission: Mission, 
        training_attr: Attributes,
        squads_list: list[Squad] = None
    ):
        """Default value for `squads_list` is `self.squads`"""
        if squads_list is None:
            squads_list = self.squads

        for squad in squads_list:
            attr = squad.attr + training_attr
            if attr.clears(mission.requirements):
                yield squad
            else:
                continue
    
    def find_lowest_qualifying_squad(
        self, 
        mission: Mission, 
        training_attr: Attributes
    ) -> Optional[Squad]:
        """Find the squad with the lowest aggregate attributes that qualifies
        for the specified mission.
        
        If there are no qualifying squads, returns None."""
        lowest_as_iter = islice(
            self.iter_qualifying_squads_for_mission(
                mission, 
                training_attr, 
                self.squads_by_asc_aggr),
            1)
        lowest_as_list = list(lowest_as_iter)
        if len(lowest_as_list) == 0:
            lowest = None
        else:
            lowest = lowest_as_list[0]
        return lowest


    def iter_available_missions(self):
        return filter(lambda mi: mi.is_available, self.missions)


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
    Member(id=4, attr=Attributes(54,32,64), name="Totodi", level=28, job="Pugilist"),
    Member(id=5, attr=Attributes(53,23,90), name="Inghilswys", level=36, job="Lancer"),
    Member(id=6, attr=Attributes(20,76,54), name="Sofine", level=28, job="Scholar"),
    Member(id=7, attr=Attributes(22,90,44), name="Nunulupa Tatalupa", level=31, job="Thaumaturge"),
    Member(id=8, attr=Attributes(22,106,28), name="Awayuki", level=31, job="Conjurer"),
]

#   Yes, I copy-pasted the CSV in the python file, and then I used
#   the multi-column cursor in Visual Studio Code.

missions = [
Mission(requirements=Attributes(165,170,150),name="Military Courier", level=1, xp_reward=7500, is_available=True),
Mission(requirements=Attributes(150,255,195),name="Outskirts Patrol", level=1, xp_reward=9000, is_available=True),
Mission(requirements=Attributes(155,195,250),name="Beastmen Recon", level=5, xp_reward=10500, is_available=True),
Mission(requirements=Attributes(305,210,130),name="Supply Wagon Escort", level=10, xp_reward=12000, is_available=False),
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
print(*sq.squads, sep='\n')
print()
# print("Squads by aggregate:")
# print(*sq.squads_by_asc_aggr, sep='\n')
# print()
# print("Squads by aggregate descending:")
# print(*sq.squads_by_des_aggr, sep='\n')
# print()
# print("Squads by Physical:")
# print(*sq.squads_by_asc_phy, sep='\n')
# print()
# print("Squads by Physical descending:")
# print(*sq.squads_by_des_phy, sep='\n')
# print()
# print("Squads by Mental:")
# print(*sq.squads_by_asc_men, sep='\n')
# print()
# print("Squads by Mental descending:")
# print(*sq.squads_by_des_men, sep='\n')
# print()
# print("Squads by Tactical:")
# print(*sq.squads_by_asc_tac, sep='\n')
# print()
# print("Squads by Tactical descending:")
# print(*sq.squads_by_des_tac, sep='\n')
# print()

# print("Available Missions")
# print(*sq.iter_available_missions(), sep='\n')

print("Nb of qualifying squad for each available mission")
for mission in sq.iter_available_missions():
    nb = len(list(sq.iter_qualifying_squads_for_mission(mission, sq.training_attr)))
    print(f"{nb}\t{mission}")

print("Lowest qualifying squad for each available mission")
for mission in sq.iter_available_missions():
    squad = sq.find_lowest_qualifying_squad(mission, sq.training_attr)
    print(f"{squad}\t{mission}")

# Tests for training courses:
print()
print("Training courses")
print(training_attr)
print(max_training_attr)

prog1 = TrainingProgram((Course.PHY,), training_attr, max_training_attr)
print(prog1)

print()
print(f"Initial\t{training_attr}")
for course in list(Course):
    new_attr = prog1.calculate_one_course(training_attr, course)
    delta = new_attr - training_attr
    print(f"{course.name:7}\t{new_attr}    {delta}")