import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Daten laden
data = pd.read_csv('DuneMaster.csv')

# Filtern der Spieler, die mindestens einmal gewonnen haben
players_with_wins = data[data['is_winner'] == 1]['depositor'].unique()
data_players_with_wins = data[data['depositor'].isin(players_with_wins)]

# Berechnen der Anzahl an gespielten Runden für Spieler, die mindestens einmal gewonnen haben
total_rounds_played_winners = data_players_with_wins.groupby('depositor')['roundid'].count().reset_index()
total_rounds_played_winners.rename(columns={'roundid': 'total_rounds_played'}, inplace=True)

# Berechnen des kumulativen Gewinns für Spieler, die mindestens einmal gewonnen haben
cumulative_winnings_winners = data_players_with_wins[data_players_with_wins['is_winner'] == 1].groupby('depositor')['deposit_usd'].sum().reset_index()
cumulative_winnings_winners.rename(columns={'deposit_usd': 'cumulative_winnings'}, inplace=True)

# Zusammenführen der Daten für die Regression
merged_data_for_winning_regression_winners = pd.merge(total_rounds_played_winners, cumulative_winnings_winners, on='depositor')

# Regression
X_winnings_winners = merged_data_for_winning_regression_winners['cumulative_winnings']
y_rounds_played_winners = merged_data_for_winning_regression_winners['total_rounds_played']
X_winnings_winners = sm.add_constant(X_winnings_winners)  # Konstante hinzufügen
model_winnings_winners = sm.OLS(y_rounds_played_winners, X_winnings_winners).fit()

# Grafik erstellen
plt.figure(figsize=(10, 6))
sns.regplot(x='cumulative_winnings', y='total_rounds_played', data=merged_data_for_winning_regression_winners, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Regression of Total Rounds Played on Cumulative Winnings (Players with Wins)')
plt.xlabel('Cumulative Winnings (USD)')
plt.ylabel('Total Rounds Played')
plt.show()

# Zusammenfassung des Modells anzeigen
print(model_winnings_winners.summary())
