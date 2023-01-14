import pandas as pd

from League import League

# set the league name
league_name = "test league"

# set up league instance
league = League(name=league_name, win_pts=3, draw_pts=1, loss_pts=0)

# get player list and add players
players_df = pd.read_csv('input_data/player_list.csv')

for (idx, player) in players_df.iterrows():
    if player.loc['player name'] != "":
        name = player.loc['player name']
        team = player.loc['player team name']
        note = player.loc['player note']
        if not league.add_player(name=name, faction=team, note=note):
            print(f"error: player {player} not added")

# get game results and add them
results_data_df = pd.read_csv('input_data/fixtures.csv')

for (idx, result) in results_data_df.iterrows():
    if result.loc['played'] == 'y':
        rnd = result.loc['round']
        game = result.loc['game']
        player_a = result.loc['player_a']
        player_b = result.loc['player_b']
        player_a_score = result.loc['player_a_sc']
        player_b_score = result.loc['player_b_sc']
        return_msg = league.add_result(rnd=rnd, game=game,
                                       pl_a=player_a, sc_a=player_a_score,
                                       pl_b=player_b, sc_b=player_b_score)
        if return_msg != 'result added':
            print(f"Error: round: {rnd+1}, game: {result}, - {result}")

# get dataframes from the league instance
player_data_df = league.get_all_player_data()
standings_df = league.get_standings()
all_results_df = league.get_all_result_data()
player_records_df = league.get_all_player_records()

# export csv files
filename = league_name.replace(" ", "-")
player_data_df.to_csv(f'output_data/{filename}_player_data.csv', index=False)
standings_df.to_csv(f'output_data/{filename}_standings.csv', index=False)
all_results_df.to_csv(f'output_data/{filename}_all_results.csv', index=False)
player_records_df.to_csv(f'output_data/{filename}_player_records.csv', index=False)

# generate a readme file
player_ls = standings_df['player'].to_list()
points_ls = standings_df['league points'].to_list()

for idx, player in enumerate(player_ls):
    print(f"{player} - {points_ls[idx]}")
