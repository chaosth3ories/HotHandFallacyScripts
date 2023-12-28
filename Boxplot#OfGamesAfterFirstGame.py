import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Laden des Datensatzes
dune_data = pd.read_csv('DuneMaster.csv')

# Konvertierung von block_time in datetime
dune_data['block_time'] = pd.to_datetime(dune_data['block_time'])

# Ermittle das erste Spiel jedes Spielers
first_games_status = dune_data.sort_values(by='block_time').groupby('depositor').first().reset_index()

# Erstelle ein Dictionary, das jeden Spieler seinem ersten Spielstatus (gewonnen/verloren) zuordnet
player_first_game_status = dict(zip(first_games_status['depositor'], first_games_status['is_winner']))

# Erstelle eine Kopie von later_games, um SettingWithCopyWarning zu vermeiden
later_games = dune_data[~dune_data.index.isin(first_games_status.index)].copy()
later_games['first_game_status'] = later_games['depositor'].map(player_first_game_status)

# Trenne die Daten in zwei Gruppen: Spieler, die ihr erstes Spiel gewonnen haben, und diejenigen, die verloren haben
later_games_winners = later_games[later_games['first_game_status'] == 1]
later_games_losers = later_games[later_games['first_game_status'] == 0]

# Zähle die Anzahl der Spiele, die jeder Spieler nach seinem ersten Spiel gespielt hat und konvertiere in Listen
games_played_after_first_win = later_games_winners.groupby('depositor').size().tolist()
games_played_after_first_loss = later_games_losers.groupby('depositor').size().tolist()

# Überprüfe, ob die Listen nicht leer sind
if games_played_after_first_win and games_played_after_first_loss:
    # Erstelle zwei Boxplots
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=[games_played_after_first_win, games_played_after_first_loss], 
                showfliers=False)  # Ausschluss von Ausreißern
    plt.xticks([0, 1], ['Spiele Nach Erstem Gewinn', 'Spiele Nach Erster Niederlage'])
    plt.ylabel('Anzahl der Gespielten Spiele')
    plt.title('Vergleich der Anzahl der Gespielten Spiele nach dem Ersten Spiel')
    plt.show()
else:
    print("Eine der Listen ist leer.")
