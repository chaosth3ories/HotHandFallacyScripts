import pandas as pd

# Laden der Daten aus der hochgeladenen Datei
data = pd.read_csv('DuneMaster.csv')

# Schritt 1 & 2: Berechnung des durchschnittlichen Einsatzes vor dem ersten Gewinn und Identifizierung von Spielern, die ihren Einsatz nach einem Gewinn erhöht haben

# Filtern der Gewinner
winners = data[data['is_winner'] == 1]

# Gruppieren nach Einzahler, um den ersten Gewinn zu finden
first_wins = winners.groupby('depositor').first().reset_index()

# Zusammenführen, um alle Zeilen vor dem ersten Gewinn für jeden Gewinner zu erhalten
merged_data = pd.merge(data, first_wins[['depositor', 'block_number']], on='depositor', how='left', suffixes=('', '_first_win'))
before_first_win = merged_data[merged_data['block_number'] < merged_data['block_number_first_win']]

# Berechnung des durchschnittlichen Einsatzes vor dem ersten Gewinn
avg_deposit_before_win = before_first_win.groupby('depositor')['deposit_eth'].mean().reset_index()
avg_deposit_before_win.rename(columns={'deposit_eth': 'avg_deposit_before_win'}, inplace=True)

# Zusammenführen des durchschnittlichen Einsatzes mit den Hauptdaten
data_with_avg = pd.merge(data, avg_deposit_before_win, on='depositor', how='left')

# Ermittlung des Einsatzes in der ersten Runde nach dem Gewinn
data_with_avg['next_round_deposit'] = data_with_avg.groupby('depositor')['deposit_eth'].shift(-1)

# Identifizierung von Spielern, die ihren Einsatz nach einem Gewinn erhöht haben
data_with_avg['increased_bet_after_win'] = (data_with_avg['deposit_eth'] == data_with_avg['next_round_deposit']) & \
                                           (data_with_avg['next_round_deposit'] > data_with_avg['avg_deposit_before_win']) & \
                                           (data_with_avg['is_winner'] == 1)

# Schritt 3: Hinzufügen einer Spalte, um diese Spieler zu markieren
data_with_avg['increased_bet_mark'] = data_with_avg['increased_bet_after_win'].apply(lambda x: 1 if x else 0)

# Schritt 4: Berechnung der Gesamtanzahl dieser Spieler
unique_increased_bet_players = data_with_avg[data_with_avg['increased_bet_after_win']]['depositor'].nunique()

# Schritt 5: Berechnung des durchschnittlichen Einsatzes in ETH, des durchschnittlichen Gewinns/Verlusts und der durchschnittlich gespielten Runden für diese Spieler
selected_players_data = data_with_avg[data_with_avg['increased_bet_after_win']]

# Durchschnittlicher Einsatz in ETH
average_deposit = selected_players_data['deposit_eth'].mean()

# Durchschnittlicher Gewinn/Verlust (Gewinnbetrag ist die Gesamteinzahlung anderer Spieler in der Runde, Verlust ist der eigene Einsatz)
selected_players_data['win_loss_amount'] = selected_players_data.apply(
    lambda row: -row['deposit_eth'] if row['is_winner'] == 0 else (selected_players_data[selected_players_data['roundid'] == row['roundid']]['deposit_eth'].sum() - row['deposit_eth']),
    axis=1
)
average_win_loss = selected_players_data['win_loss_amount'].mean()

# Durchschnittlich gespielte Runden
average_rounds_played = selected_players_data.groupby('depositor')['roundid'].nunique().mean()

# Ergebnisse
unique_increased_bet_players, average_deposit, average_win_loss, average_rounds_played
