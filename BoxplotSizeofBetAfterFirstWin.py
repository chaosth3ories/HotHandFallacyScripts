import pandas as pd
import matplotlib.pyplot as plt

# Daten einlesen
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
winners_stats = winners_data.groupby('depositor')['deposit_usd'].agg(['mean', 'min', 'max', 'median']).mean()
losers_stats = losers_data.groupby('depositor')['deposit_usd'].agg(['mean', 'min', 'max', 'median']).mean()

# Daten für Boxplots vorbereiten
boxplot_data = pd.DataFrame({
    "Gruppe": ["Gewinner", "Verlierer"],
    "Median": [winners_stats['median'], losers_stats['median']],
    "25th Percentile": [winners_stats['min'], losers_stats['min']],
    "75th Percentile": [winners_stats['max'], losers_stats['max']]
})

# Maximale Y-Achsen-Skala basierend auf den maximalen Werten der beiden Gruppen festlegen
max_scale = max(boxplot_data['75th Percentile'])

# Erstellen von Boxplots
plt.figure(figsize=(12, 6))

# Boxplot für Gewinner
plt.subplot(1, 2, 1)
plt.boxplot([boxplot_data['Median'][0], boxplot_data['25th Percentile'][0], boxplot_data['75th Percentile'][0]])
plt.title('Gewinner')
plt.xticks([1], ['USD Beträge'])
plt.ylabel('USD')
plt.ylim(0, max_scale)  # Gleiche Skala für beide Boxplots

# Boxplot für Verlierer
plt.subplot(1, 2, 2)
plt.boxplot([boxplot_data['Median'][1], boxplot_data['25th Percentile'][1], boxplot_data['75th Percentile'][1]])
plt.title('Verlierer')
plt.xticks([1], ['USD Beträge'])
plt.ylim(0, max_scale)  # Gleiche Skala für beide Boxplots

plt.tight_layout()
plt.show()
