# A file to experiment with stuff in the Python language

import csv
import logging

input_filename = "Squadron_semicolons.csv"

rows_squadron = []
rows_members = []
rows_missions = []

# Separate the rows by data type (squadron, member, mission)
#
# Code based on: https://docs.python.org/3/library/csv.html#csv.DictReader
with open(input_filename, newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read())
    csvfile.seek(0)
    datareader = csv.DictReader(csvfile, dialect=dialect)
    for row in datareader:
        datatype = row['Data Type'].lower()
        print(datatype)
        if datatype == 'squadron':
            rows_squadron.append(row)
        elif datatype == 'member':
            rows_members.append(row)
        elif datatype == 'mission':
            rows_missions.append(row)
        else:
            datatype_as_seen_in_input = row['Data Type']
            logging.warning(
                f"In input file, data type {datatype_as_seen_in_input} is "
                "not recognized, and the corresponding row has been ignored."
                )

print("Squadron Rows")
print(*rows_squadron, sep='\n')
print()
print("Members Rows")
print(*rows_members, sep='\n')
print()
print("Missions Rows")
print(*rows_missions, sep='\n')
print()

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


