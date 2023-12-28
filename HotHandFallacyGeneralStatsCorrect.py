import pandas as pd

# Lade die bereitgestellte Datei
data = pd.read_csv('DuneMaster.csv')

# Identifiziere das erste Spiel jedes Spielers
first_games = data.sort_values(by=['depositor', 'roundid']).groupby('depositor').first().reset_index()

# Gruppierung der Spieler in Gewinner und Verlierer ihres ersten Spiels
winners_first_game = first_games[first_games['is_winner'] == 1]
losers_first_game = first_games[first_games['is_winner'] == 0]

# Filtere Spiele, die nach dem ersten Spiel stattfanden
data_with_first_game_info = data.merge(first_games[['depositor', 'roundid']], on='depositor', suffixes=('', '_first_game'))
data_after_first_game = data_with_first_game_info[data_with_first_game_info['roundid'] > data_with_first_game_info['roundid_first_game']]

# Trenne die Daten in Gewinner und Verlierer des ersten Spiels
winners_data = data_after_first_game[data_after_first_game['depositor'].isin(winners_first_game['depositor'])]
losers_data = data_after_first_game[data_after_first_game['depositor'].isin(losers_first_game['depositor'])]

# Berechnung der erforderlichen Statistiken für beide Gruppen
winners_stats = {
    "Games Played": winners_data.groupby('depositor').size().agg(['mean', 'min', 'max', 'median']),
    "Deposit Stats (USD)": winners_data.groupby('depositor')['deposit_usd'].agg(['mean', 'min', 'max', 'median']).mean()
}

winners_stats_quartiles = {
    "Games Played 25th": winners_data.groupby('depositor').size().quantile(0.25),
    "Games Played 75th": winners_data.groupby('depositor').size().quantile(0.75),
    "Deposit Stats (USD) 25th": winners_data.groupby('depositor')['deposit_usd'].quantile(0.25).mean(),
    "Deposit Stats (USD) 75th": winners_data.groupby('depositor')['deposit_usd'].quantile(0.75).mean()
}

losers_stats = {
    "Games Played": losers_data.groupby('depositor').size().agg(['mean', 'min', 'max', 'median']),
    "Deposit Stats (USD)": losers_data.groupby('depositor')['deposit_usd'].agg(['mean', 'min', 'max', 'median']).mean()
}

losers_stats_quartiles = {
    "Games Played 25th": losers_data.groupby('depositor').size().quantile(0.25),
    "Games Played 75th": losers_data.groupby('depositor').size().quantile(0.75),
    "Deposit Stats (USD) 25th": losers_data.groupby('depositor')['deposit_usd'].quantile(0.25).mean(),
    "Deposit Stats (USD) 75th": losers_data.groupby('depositor')['deposit_usd'].quantile(0.75).mean()
}

# Erstellung der finalen Tabelle mit Quartilen
final_summary_table = pd.DataFrame({
    # Gewinner-Statistiken
    "Gewinner - Spiele (Durchschnitt)": [winners_stats['Games Played']['mean']],
    "Gewinner - Spiele (Minimum)": [winners_stats['Games Played']['min']],
    "Gewinner - Spiele (Maximum)": [winners_stats['Games Played']['max']],
    "Gewinner - Spiele (Median)": [winners_stats['Games Played']['median']],
    "Gewinner - Spiele (25. Quartil)": [winners_stats_quartiles['Games Played 25th']],
    "Gewinner - Spiele (75. Quartil)": [winners_stats_quartiles['Games Played 75th']],
    "Gewinner - Einsatz (USD) (Durchschnitt)": [winners_stats['Deposit Stats (USD)']['mean']],
    "Gewinner - Einsatz (USD) (Minimum)": [winners_stats['Deposit Stats (USD)']['min']],
    "Gewinner - Einsatz (USD) (Maximum)": [winners_stats['Deposit Stats (USD)']['max']],
    "Gewinner - Einsatz (USD) (Median)": [winners_stats['Deposit Stats (USD)']['median']],
    "Gewinner - Einsatz (USD) (25. Quartil)": [winners_stats_quartiles['Deposit Stats (USD) 25th']],
    "Gewinner - Einsatz (USD) (75. Quartil)": [winners_stats_quartiles['Deposit Stats (USD) 75th']],
    # Verlierer-Statistiken
    "Verlierer - Spiele (Durchschnitt)": [losers_stats['Games Played']['mean']],
    "Verlierer - Spiele (Minimum)": [losers_stats['Games Played']['min']],
    "Verlierer - Spiele (Maximum)": [losers_stats['Games Played']['max']],
    "Verlierer - Spiele (Median)": [losers_stats['Games Played']['median']],
    "Verlierer - Spiele (25. Quartil)": [losers_stats_quartiles['Games Played 25th']],
    "Verlierer - Spiele (75. Quartil)": [losers_stats_quartiles['Games Played 75th']],
    "Verlierer - Einsatz (USD) (Durchschnitt)": [losers_stats['Deposit Stats (USD)']['mean']],
    "Verlierer - Einsatz (USD) (Minimum)": [losers_stats['Deposit Stats (USD)']['min']],
    "Verlierer - Einsatz (USD) (Maximum)": [losers_stats['Deposit Stats (USD)']['max']],
    "Verlierer - Einsatz (USD) (Median)": [losers_stats['Deposit Stats (USD)']['median']],
    "Verlierer - Einsatz (USD) (25. Quartil)": [losers_stats_quartiles['Deposit Stats (USD) 25th']],
    "Verlierer - Einsatz (USD) (75. Quartil)": [losers_stats_quartiles['Deposit Stats (USD) 75th']]
})

