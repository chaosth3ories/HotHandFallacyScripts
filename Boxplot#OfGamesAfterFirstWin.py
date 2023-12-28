import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Laden der Daten
df = pd.read_csv('DuneMaster.csv')

# Sortieren der Daten nach Spieler und Runden, um das erste Spiel jedes Spielers zu identifizieren
df_sorted = df.sort_values(by=['depositor', 'roundid'])

# Ermittlung des ersten Spiels und ob es gewonnen wurde
df_sorted['first_game'] = df_sorted.groupby('depositor')['roundid'].rank(method='first') == 1
df_sorted['first_game_win'] = df_sorted['first_game'] & df_sorted['is_winner']

# Zuordnung der Information, ob das erste Spiel gewonnen wurde, zu allen Spielen des Spielers
df_sorted['first_game_win'] = df_sorted.groupby('depositor')['first_game_win'].transform('max')

# Filtern der Daten auf die Zeilen nach dem ersten Spiel
df_post_first_game = df_sorted[df_sorted['first_game'] == False]

# Gruppieren der Daten nach Spieler und erstem Gewinn, um die Spiele zu zählen
games_played_post_first_win = df_post_first_game.groupby('depositor').agg({
    'first_game_win': 'max',  # Maximalwert, um zu prüfen, ob der erste Gewinn erfolgte
    'roundid': 'count'        # Zählen der gespielten Spiele
}).reset_index()

# Einstellen der Figurgröße
plt.figure(figsize=(10, 6))

# Boxplot für die Anzahl der gespielten Spiele nach dem ersten Gewinn
sns.boxplot(x='first_game_win', y='roundid', data=games_played_post_first_win)
plt.xlabel('Erstes Spiel Gewonnen', fontsize=12)
plt.ylabel('Anzahl der Spiele nach dem ersten Gewinn', fontsize=12)
plt.title('Spiele nach dem ersten Gewinn', fontsize=14)
plt.ylim(0, games_played_post_first_win['roundid'].quantile(0.75) + 1.5 * (games_played_post_first_win['roundid'].quantile(0.75) - games_played_post_first_win['roundid'].quantile(0.25)))  # Begrenzung auf 1.5*IQR über dem 75% Quantil

# Zeigt den Boxplot an
plt.show()

