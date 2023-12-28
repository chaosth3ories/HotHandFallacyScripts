import pandas as pd

# Re-read the dataset
dune_data = pd.read_csv('DuneMaster.csv')

# Convert block_time to datetime
dune_data['block_time'] = pd.to_datetime(dune_data['block_time'])

# Identify the first game played by each player
first_games = dune_data.sort_values('block_time').groupby('depositor').first().reset_index()

# Assign a flag for the first game result
first_games['first_game_result'] = first_games['is_winner']

# Merge the first game result back into the main dataframe
dune_data = dune_data.merge(first_games[['depositor', 'first_game_result']], on='depositor')

# Filter out the first game for each player to analyze their subsequent games
subsequent_games = dune_data[dune_data['block_time'] > dune_data.groupby('depositor')['block_time'].transform('min')]

# Group these subsequent games based on whether the player won or lost their first game
games_after_first_win = subsequent_games[subsequent_games['first_game_result'] == 1]
games_after_first_loss = subsequent_games[subsequent_games['first_game_result'] == 0]

# Calculate the desired statistics for number of games played after the first game
games_played_stats_win = games_after_first_win.groupby('depositor').size().describe()
games_played_stats_loss = games_after_first_loss.groupby('depositor').size().describe()

# Calculate the desired statistics for average bet size after the first game
avg_bets_stats_win = games_after_first_win.groupby('depositor')['deposit_usd'].mean().describe()
avg_bets_stats_loss = games_after_first_loss.groupby('depositor')['deposit_usd'].mean().describe()

# Combine the statistics into a single DataFrame for display
stats_summary = pd.DataFrame({
    'Games After First Win': games_played_stats_win,
    'Games After First Loss': games_played_stats_loss,
    'Avg Bets After First Win': avg_bets_stats_win,
    'Avg Bets After First Loss': avg_bets_stats_loss
})

# Transpose the DataFrame for better readability
stats_summary = stats_summary.T

# Display the summary statistics table
stats_summary
