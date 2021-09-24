# ffxiv-squadron-planner
To help plan training courses and squad selection for daily squadron missions in Final Fantasy XIV


# Data Update Process

Quick notes of what I do when I want to know what courses and mission
I should take for today's mission.

1. Write the in-game data in Excel
    1. Check if mission requirements changed. (Do they change weekly?)
    1. Update the Squadron Attributes from training courses
    1. Update squadron members attributes & levels 
    (keeping track of levels has no use beyond soothing my feelings.)
    1. Update which missions are not available anymore
1. Export the Excel to CSV
1. Reboot to Linux (It was a good idea at the time, lolsob)
1. Manually transfer the data from the CSV to the Python script
    1. Update the squadron attributes
    1. Update members attributes and levels
    1. Update missions
1. Check the highest possible mission with 0 courses
    1. Comment-out the code that prints results for 2 and 3 courses
    1. Run the script
    1. Check what can be done with 0 courses
    1. Count how many mission can be done with 0 and 1 course
    1. Update `threshold_nb_doable_missions_1_courses` with the higher
        number found in the previous step
    1. Uncomment the code that prints results for 2 courses.
        (but leave commented the code for 3 courses)





