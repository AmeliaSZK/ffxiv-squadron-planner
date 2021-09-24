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
and the code at the commit `2895757`. 
(Look for commit message "README EXAMPLE #1")
> Yes, I know about tags in Git. 
> No, I don't want to take the time right now to learn how they work.
> Yes, I know it's probably super-simple, but you know what won't be simple?
> Checking out every alternatives to git tags, and then getting sucked into
> learning how releases work on Github, because of course that's how it's
> gonna go 😑

So, doing all the above steps with the data from `Squadron-2021-09-24.csv`
taught us that...
* We can do the level 40 mission, the best one, without training.
* We can unlock the level 30 missions with these training programs:
    * PHY_MEN, PHY, PHY
    * PHY, PHY_MEN, PHY
    * PHY, PHY, PHY_MEN

By default, the script prints in its output the least experienced squad
for each mission you can do _with no training_. To get these squads for
any training program...

1. Update `train_prog`
1. If you want squads for multiple programs...
    1. Copy-paste the 4 lines of code
    1. Change the value of the new `train_prog`
    1. Don't bother renaming that variable, because then you'll have to
        rename it in multiple places.
    1. Resist (or not) the temptation to put these 4 lines of code into
        a function, because now you're starting to see in their full glory
        all the architectural flaws in this not-really-finished Python script.
        (I should have done this in Excel from the start... 😑)
1. Clear the terminal
1. Run the script


Finally, when you have your squad compositions...

1. Make sure to note in a (paper) notebook, or in a file that can be
retrieved from Windows, **for each squad**...
    1. The squad composition
    1. The training program (meaning, all the courses to take)
    1. The mission to do after the training
1. Commit the changes to the script. This step is meant to grab the changes
    to the code that you made, and that you forgot that you made by the
    time you're done looking for results that you like.
1. Push the git repo to Github, so that you can access the current code
    from the Github website, without having to reboot into Linux
1. Reboot to Windows.



