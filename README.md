# NBA Stats Analysis

A simple experimental program made in Python 3.7.2 that can be used to get an alternative overall look at the various stats available to compare two NBA teams head-to-head.

## Working Principle

The official NBA website offers a wide range of statistical data for each team going back all the way to the 1996-97 season. While the stats are impressive and can be used to gain an in-depth view of the performance of the teams, they can also be quite intimidating and a bit difficult to understand and put into a measurable overall value when attempting to perform a head-to-head comparison of two teams. It is not always easy to say which team has the better standing in terms of the statistical data.
It is this problem, coupled with the fact that I am a diehard NBA basketball fan who wanted his own simple measurement, that prompted me to play with the numbers hoping to obtain a single measurement value that might give me a hint as to the performance of any NBA team. Of course, one can always look at the *Net Rating* value of the teams. But I wanted my own.  
Starting with the thought that each of the statistical values contributes to and is responsible for a win or a loss to a certain extent,  I began by retrieving the stats going back from the 2010-11 season onwards  and looking at the relationship between the different numbers.  As there is quite a large amount of data available, I decided to narrow down my focus arbitrarily to only eleven of the stat values thtat are expressed as percentages and experiment with them.
The stat values considered are:

    * Win Percentage
    * Field Goal Percentage
    * Three Point Field Goal Percentage
    * Free Throw Percentage
    * Assist Percentage
    * Offensive Rebound Percentage
    * Defensive Rebound Percentage
    * Rebound Percentage
    * Turnover Percentage
    * Effective Field Goal Percentage
    * True Shooting Percentage

I then proceeded to determine the correlation of the ten columns with the Win Percentage column so as to see the extent of their effect on winning which gave me a varying array of values I used to make my grading scale (Have a look at '*data\correlation_and_grading_scales\grading_scales.xlsx*').

## Usage

1. Install the required Python modules listed in '*requrements.txt*'.
2. Retrieve the stats with '*retrieve_stats.py*'.
3. Calculate the correlation with '*perform_correlation.py*'.
4. Open '*analyze_stats.py*', input any two teams and run the analysis.
