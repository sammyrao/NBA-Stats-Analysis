import pandas as pd
import numpy as np
import retrieve_stats

# To display all rows and columns of data frames
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Function to prepare the stats for head-to-head analysis
def prepare_teams_stats(team_a_stats_df, team_b_stats_df):

    print('Reading the grading scales . . .')

    # Read the grading scales CSV file
    grading_scales_CSV_df = pd.read_csv('data/correlation_and_grading_scales/grading_scales.csv')

    print('Grading scales:')
    print(grading_scales_CSV_df.to_string(index = False))

    team_a_name = team_a_stats_df['NAME']
    team_b_name = team_b_stats_df['NAME']

    # Drop the columns not relevant for grading
    team_a_stats_df = team_a_stats_df.drop(['ID', 'NAME'], axis = 1)
    team_b_stats_df = team_b_stats_df.drop(['ID', 'NAME'], axis = 1)

    print(team_a_name.to_string(index = False) + ' stats:')
    print(team_a_stats_df.to_string(index = False))
    print(team_b_name.to_string(index = False) + ' stats:')
    print(team_b_stats_df.to_string(index = False))

    analyze_teams_stats(team_a_name, team_a_stats_df, grading_scales_CSV_df)
    analyze_teams_stats(team_b_name, team_b_stats_df, grading_scales_CSV_df)

# Function to analyze two teams' stats head-to-head
def analyze_teams_stats(team_name, team_stats_df, grading_scales_CSV_df):

    graded_team_stats = []

    # Loop through the columns and perform the grading
    for column in grading_scales_CSV_df:

        column_grade = (team_stats_df[column] * grading_scales_CSV_df[column]) / 100

        graded_team_stats.append(column_grade)

    overall_team_stats_grade = sum(graded_team_stats)

    graded_team_stats_df = pd.DataFrame(graded_team_stats)

    graded_team_stats_df = np.transpose(graded_team_stats_df)

    print('\n' + team_name.to_string(index = False) + ' graded stats:')
    print(graded_team_stats_df.to_string(index = False))
    print(team_name.to_string(index = False) + ' overall stats grade: {}'.format(overall_team_stats_grade.to_string(index = False)) + '%') 

if __name__ == '__main__':

    # Read the teams CSV file
    teams_CSV_df = pd.read_csv('data/teams/teams.csv')

    # Get the teams' ID's and names by the indexes from 'teams.csv'
    team_a_id = teams_CSV_df['ID'][2]
    team_a_name = teams_CSV_df['FULL NAME'][2]
    team_b_id = teams_CSV_df['ID'][13]
    team_b_name = teams_CSV_df['FULL NAME'][13] 

    # Retrieve the teams' stats
    team_a_stats_df = retrieve_stats.retrieve_specific_team_stats(team_a_id, team_a_name, retrieve_stats.date_from, retrieve_stats.date_to, retrieve_stats.current_season)
    team_b_stats_df = retrieve_stats.retrieve_specific_team_stats(team_b_id, team_b_name, retrieve_stats.date_from, retrieve_stats.date_to, retrieve_stats.current_season)

    # Prepare the data and perform the stats analysis
    prepare_teams_stats(team_a_stats_df, team_b_stats_df)   