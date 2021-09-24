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
1. Clear the terminal window
1. Run the script
1. Check how many 2-courses training programs meet the threshold
1. If there are none...
    1. Reduce the threshold by 1
    1. Clear the terminal window
    1. Run the script
1. In the results, even if no training program has _more_ doable missions,
    stay on the lookout for _different_ missions that may have been made avaialble.
1. Repeat the steps starting at "Update `threshold_nb_doable_missions_1_courses`",
    but this time for `2_courses`

The next steps were written using the data from `Squadron-2021-09-24.csv`,
and the code at the commit `COMMIT HASH HERE`. 
(Look for commit message "README EXAMPLE #1")
> Yes, I know about tags in Git. 
> No, I don't want to take the time right now to learn how they work.
> Yes, I know it's probably super-simple, but you know what won't be simple?
> Checking out every alternatives to git tags, and then getting sucked into
> learning how releases work on Github, because of course that's how it's
> gonna go 😑






