import os.path
import pandas as pd
import glob

# To display all rows and columns of data frames
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Function to combine the CSV files from the past seasons
def combine_CSV_files():

    # No need to combine the CSV data if it already exists
    if os.path.exists('data/combined_teams_stats/combined_teams_stats_2010-2020.csv'):

        print('Combined CSV file already exitst!')

        combined_CSV_file_df = pd.read_csv('data/combined_teams_stats/combined_teams_stats_2010-2020.csv')

        print(combined_CSV_file_df.to_string(index = False))

    else:          

        print('Reading the CSV files . . .')

        extension = 'csv'

        # Go through all the CSV files in the folder
        CSV_files = [i for i in glob.glob('data/past_seasons_teams_stats/*.{}'.format(extension))]

        print('Combining the CSV files . . .')

        # Combine all the CSV files 
        combined_CSV_file_df = pd.concat([pd.read_csv(file) for file in CSV_files])

        print(combined_CSV_file_df.to_string(index = False))

        # Save the data as CSV
        combined_CSV_file_df.to_csv('data/combined_teams_stats/combined_teams_stats_2010-2020.csv', index = False)

        print('CSV Saved!')

# Function to perform the correlation calculation
def perform_correlation_calculation():

    # No need to perform the correlation calculation if the correlation CSV already exists
    if os.path.exists('data/correlation_and_grading_scales/correlation.csv'):

        print('Correlation CSV file already exitst!')

        correlation_CSV_df = pd.read_csv('data/correlation_and_grading_scales/correlation.csv')

        print(correlation_CSV_df.to_string(index = False))

    else:    

        print('Reading the combined teams stats file . . .')

        # The percentage columns
        percentage_columns = ['WIN%', 'FG%', '3P%', 'FT%', 'AST%', 'OREB%', 'DREB%', 'REB%', 'TOV%', 'EFG%', 'TS%']
        
        # The rows and columns to drop from the correlation matrix
        # To be left with only the correlation to the win percentage
        indexes_to_drop = ['FG%', '3P%', 'FT%', 'AST%', 'OREB%', 'DREB%', 'REB%', 'TOV%', 'EFG%', 'TS%']
        columns_to_trop = ['WIN%']

        # Read the combined CSV file from the past seasons 
        teams_stats_df = pd.read_csv('data/combined_teams_stats/combined_teams_stats_2010-2020.csv', usecols = percentage_columns)
        
        print('Performing correlation calculation . . .')

        # Calculate the correlation
        correlation = teams_stats_df.corr(method = 'spearman')

        # Leave only the correlation to the win percentage
        correlation = correlation.drop(index = indexes_to_drop, columns = columns_to_trop)

        print(correlation)

        # Save the data as CSV
        correlation.to_csv('data/correlation_and_grading_scales/correlation.csv', index = True)
        
        print('CSV Saved!')

if __name__ == '__main__':

    # Combine the CSV files from the past seasons 
    combine_CSV_files()

    # Perform the correlation calculation
    perform_correlation_calculation()    