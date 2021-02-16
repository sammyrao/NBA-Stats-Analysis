import os.path
from custom_headers import custom_headers
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats
from datetime import date

# To display all rows and columns of data frames
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Global variables to be accessed by 'analyze_stats.py'
# Take the starting date of the current season and today's date to retrieve the latest stats
# 'date_from and 'date_to' should be in the format 'mm/dd/yyyy'
date_from = '12/22/2020'
date_to = date.today()
date_to = date_to.strftime('%m/%d/%y')
current_season = '2020-21'

# Function to retrieve the teams
# Needed for reference while analyzing the teams' stats
def retvieve_teams():

    # No need to download the teams data if it already exists
    if os.path.exists('data/teams/teams.csv'):

        print('Teams CSV file already exitst!')

        teams_CSV_df = pd.read_csv('data/teams/teams.csv')

        print(teams_CSV_df)

    else:

        print('Retrieving the teams . . .')   

        # Retrieve the teams
        teams_df = pd.DataFrame(teams.get_teams())

        print('Number of teams retrieved: {}'.format(len(teams_df)))
        
        # Rename the columns
        teams_df = teams_df.rename(columns = {'id'            :   'ID', 
                                            'full_name'     :   'FULL NAME',
                                            'abbreviation'  :   'ABBREVIATION',
                                            'nickname'      :   'NICKNAME',
                                            'city'          :   'CITY',
                                            'state'         :   'STATE',
                                            'year_founded'  :   'YEAR FOUNDED'})

        print(teams_df)

        # Save the data as CSV
        teams_df.to_csv('data/teams/teams.csv', index = True)

        print("CSV Saved!")

# Function to retrieve the stats of all teams
def retrieve_all_teams_stats(date_from, date_to, season, save_location):

    print('Retrieving stats for the ' + season + ' season . . .')

    teams_stats = []

    # Loop through the teams and retrieve their stats
    for team in teams.get_teams():

        team_id = team['id']
        team_name = team['full_name']

        print('     Retrieving stats for the ' + team_name + ' . . .')
  
        # The stats from the 'Traditional' section
        general_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = team_id, per_mode_detailed = 'PerGame', season_type_all_star = 'Regular Season', date_from_nullable = date_from, date_to_nullable = date_to, season = season, headers = custom_headers, timeout = 120)
        general_team_dict = general_team_info.get_normalized_dict()
        general_team_dashboard = general_team_dict['OverallTeamDashboard'][0]

        games_played = general_team_dashboard['GP']
        points = general_team_dashboard['PTS']
        wins = general_team_dashboard['W']
        losses = general_team_dashboard['L']
        win_percentage = general_team_dashboard['W_PCT']
        field_goal_percentage = general_team_dashboard['FG_PCT']
        three_point_percentage = general_team_dashboard['FG3_PCT']
        free_throw_percentage = general_team_dashboard['FT_PCT']
        offensive_rebounds = general_team_dashboard['OREB']
        defensive_rebounds = general_team_dashboard['DREB']
        rebounds = general_team_dashboard['REB']
        assists = general_team_dashboard['AST']
        turnovers = general_team_dashboard['TOV']
        plus_minus = general_team_dashboard['PLUS_MINUS']

        # The stats from the 'Advanced' section
        advanced_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = team_id, measure_type_detailed_defense = 'Advanced', season_type_all_star = 'Regular Season', date_from_nullable = date_from, date_to_nullable = date_to, season = season, headers = custom_headers, timeout = 120)
        advanced_team_dict = advanced_team_info.get_normalized_dict()
        advanced_team_dashboard = advanced_team_dict['OverallTeamDashboard'][0]

        offensive_rating = advanced_team_dashboard['OFF_RATING']
        defensive_rating = advanced_team_dashboard['DEF_RATING']
        net_rating = advanced_team_dashboard['NET_RATING']
        assist_percentage = advanced_team_dashboard['AST_PCT']
        assist_to_turnover_ratio = advanced_team_dashboard['AST_TO']
        assist_ratio = advanced_team_dashboard['AST_RATIO']
        offensive_rebound_percentage = advanced_team_dashboard['OREB_PCT']
        defensive_rebound_percentage = advanced_team_dashboard['DREB_PCT']
        rebound_percentage = advanced_team_dashboard['REB_PCT']
        turnover_percentage = advanced_team_dashboard['TM_TOV_PCT']
        effective_field_goal_percentage = advanced_team_dashboard['EFG_PCT']
        true_shooting_percentage = advanced_team_dashboard['TS_PCT']
        player_impact_estimate = advanced_team_dashboard['PIE']
        
        # Temporary dictionary to hold the stats
        # Put the percentage columns as percentages values
        teams_stats_temp = {'ID'            :   team_id,
                            'NAME'          :   team_name,
                            'GP'            :   games_played,
                            'PTS'           :   points,
                            'W'             :   wins,
                            'L'             :   losses,
                            'WIN%'          :   win_percentage * 100, 
                            'FG%'           :   field_goal_percentage * 100,
                            '3P%'           :   three_point_percentage * 100,
                            'FT%'           :   free_throw_percentage * 100,   
                            'OREB'          :   offensive_rebounds,
                            'DREB'          :   defensive_rebounds,
                            'REB'           :   rebounds,
                            'AST'           :   assists,
                            'TOV'           :   turnovers,
                            '+/-'           :   plus_minus,
                            'OFF RATING'    :   offensive_rating,
                            'DEF RATING'    :   defensive_rating,
                            'NET RATING'    :   net_rating,
                            'AST%'          :   assist_percentage * 100,
                            'AST/TO'        :   assist_to_turnover_ratio,
                            'AST RATIO'     :   assist_ratio,
                            'OREB%'         :   offensive_rebound_percentage * 100,
                            'DREB%'         :   defensive_rebound_percentage * 100,
                            'REB%'          :   rebound_percentage * 100,
                            'TOV%'          :   turnover_percentage * 100,
                            'EFG%'          :   effective_field_goal_percentage * 100,
                            'TS%'           :   true_shooting_percentage * 100,
                            'PIE'           :   player_impact_estimate * 100}

        teams_stats.append(teams_stats_temp)         

    teams_stats_df = pd.DataFrame.from_dict(teams_stats)

    print('Number of records retrieved: {}'.format(len(teams_stats_df)))

    # Sort by the team names
    teams_stats_df_sorted = teams_stats_df.sort_values('NAME', ascending = True)

    print(teams_stats_df_sorted.to_string(index = False))

    # Save the data as CSV
    teams_stats_df_sorted.to_csv('data/' + save_location + 'teams_stats_' + season + '.csv', index = False)

    print('CSV Saved for the ' + season + ' season!')

# Function to retrieve the stats of a specific team
def retrieve_specific_team_stats(team_id, team_name, date_from, date_to, season):

    print('Retrieving stats for the ' + team_name + ' . . .')

    team_stats = [] 

    # The stats from the 'Traditional' section
    general_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = team_id, per_mode_detailed = 'PerGame', season_type_all_star = 'Regular Season', date_from_nullable = date_from, date_to_nullable = date_to, season = season, headers = custom_headers, timeout = 120)
    general_team_dict = general_team_info.get_normalized_dict()
    general_team_dashboard = general_team_dict['OverallTeamDashboard'][0]

    field_goal_percentage = general_team_dashboard['FG_PCT']
    three_point_percentage = general_team_dashboard['FG3_PCT']
    free_throw_percentage = general_team_dashboard['FT_PCT']

    # The stats from the 'Advanced' section
    advanced_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = team_id, measure_type_detailed_defense = 'Advanced', season_type_all_star = 'Regular Season', date_from_nullable = date_from, date_to_nullable = date_to, season = season, headers = custom_headers, timeout = 120)
    advanced_team_dict = advanced_team_info.get_normalized_dict()
    advanced_team_dashboard = advanced_team_dict['OverallTeamDashboard'][0]

    assist_percentage = advanced_team_dashboard['AST_PCT']
    offensive_rebound_percentage = advanced_team_dashboard['OREB_PCT']
    defensive_rebound_percentage = advanced_team_dashboard['DREB_PCT']
    rebound_percentage = advanced_team_dashboard['REB_PCT']
    turnover_percentage = advanced_team_dashboard['TM_TOV_PCT']
    effective_field_goal_percentage = advanced_team_dashboard['EFG_PCT']
    true_shooting_percentage = advanced_team_dashboard['TS_PCT']
        
    # Dictionary to hold the stats
    # Put the percentage columns as percentages values
    team_stats_dict = {'ID'     :   team_id,
                       'NAME'   :   team_name,
                       'FG%'    :   field_goal_percentage * 100,
                       '3P%'    :   three_point_percentage * 100,
                       'FT%'    :   free_throw_percentage * 100,   
                       'AST%'   :   assist_percentage * 100,
                       'OREB%'  :   offensive_rebound_percentage * 100,
                       'DREB%'  :   defensive_rebound_percentage * 100,
                       'REB%'   :   rebound_percentage * 100,
                       'TOV%'   :   turnover_percentage * 100,
                       'EFG%'   :   effective_field_goal_percentage * 100,
                       'TS%'    :   true_shooting_percentage * 100} 

    team_stats.append(team_stats_dict)  

    team_stats_df = pd.DataFrame.from_dict(team_stats)    

    print('Done!')

    return(team_stats_df)      

if __name__ == '__main__':

    # Retrieve the teams
    retvieve_teams()

    # Retrieve the teams' stats for the current season
    retrieve_all_teams_stats(date_from, date_to, current_season, 'current_season_teams_stats/')

    # The past seasons data needed to calculate the correlation and formulate the grading
    past_seasons = ['2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

    # Loop through the past seasons and retrieve the teams' stats
    for season in past_seasons:

        # No need to download the season data if it already exists
        if os.path.exists('data/past_seasons_teams_stats/teams_stats_' + season + '.csv'):

            print('Season CSV file already exitst!')

            teams_stats_CSV_df = pd.read_csv('data/past_seasons_teams_stats/teams_stats_' + season + '.csv')

            print(teams_stats_CSV_df.to_string(index = False))

        else:

            # Passing the season is enough to retrieve the teams' stats for past seasons
            # 'date_from' and 'date_to' not necessary
            retrieve_all_teams_stats('', '', season, 'past_seasons_teams_stats/')               