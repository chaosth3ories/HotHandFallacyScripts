import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Laden des Datensatzes
dune_data = pd.read_csv('DuneMaster.csv')

# Konvertierung von block_time in datetime
dune_data['block_time'] = pd.to_datetime(dune_data['block_time'])

# Ermittle das erste Spiel jedes Spielers
first_games = dune_data.sort_values('block_time').groupby('depositor').first().reset_index()
first_games['first_game_result'] = first_games['is_winner']

# Füge die Information über das erste Spiel zu den Hauptdaten hinzu
dune_data = dune_data.merge(first_games[['depositor', 'block_time', 'first_game_result']], 
                             on='depositor', 
                             suffixes=('', '_first_game'))

# Filtere die Daten für Spiele nach dem ersten Spiel jedes Spielers
later_games = dune_data[dune_data['block_time'] > dune_data['block_time_first_game']].copy()

# Teile die Spiele in zwei Gruppen basierend auf dem Ergebnis des ersten Spiels
later_games['is_first_game_winner'] = later_games['depositor'].map(
    first_games.set_index('depositor')['is_winner']
)

# Berechne die durchschnittlichen Einzahlungen in USD für die beiden Gruppen
avg_deposit_after_first_win = later_games[later_games['is_first_game_winner'] == 1]['deposit_usd']
avg_deposit_after_first_loss = later_games[later_games['is_first_game_winner'] == 0]['deposit_usd']

# Erstelle die Boxplots
plt.figure(figsize=(12, 6))
sns.boxplot(data=[avg_deposit_after_first_win, avg_deposit_after_first_loss], showfliers=False)
plt.xticks([0, 1], ['Nach Erstem Gewinn', 'Nach Erster Niederlage'])
plt.ylabel('Durchschnittliche Einzahlung in USD')
plt.title('Durchschnittliche Einzahlungen in USD nach dem ersten Spiel: Gewinner vs. Verlierer')
plt.tight_layout()
plt.show()
