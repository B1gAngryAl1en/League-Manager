import pandas as pd

from League import League

league_name = "test_league"

# set up league, pass win_pts, draw_pts  and loss_pts args to override defaults (3,1,0)
league = League(name=league_name)

# set up players, list of lists [name, team_name, note]
players = [['player_a_name', 'player_a_team_name', 'player_a_note'],
           ['player_b_name', 'player_b_team_name', 'player_b_note'],
           ['player_c_name', 'player_c_team_name', 'player_c_note'],
           ['player_d_name', 'player_d_team_name', 'player_d_note']]

for player in players:
    if not league.add_player(name=player[0], faction=player[1], note=player[2]):
        print(f"error: player {player} not added")

# get game results
results_data_df = pd.read_csv('input_data/fixtures.csv')

for (idx, row) in results_data_df.iterrows():
    if row.loc['played'] == 'y':
        rnd = row.loc['round']
        game = row.loc['game']
        player_a = row.loc['player_a']
        player_b = row.loc['player_b']
        player_a_score = row.loc['player_a_sc']
        player_b_score = row.loc['player_b_sc']
        result = league.add_result(rnd=rnd, game=game,
                                   pl_a=player_a, sc_a=player_a_score,
                                   pl_b=player_b, sc_b=player_b_score)
        if result != 'result added':
            print(f"Error: round: {rnd+1}, game: {game}, - {result}")

# export player data
league.get_all_player_data().to_csv(filename+"_player_data.csv", index=False)

# export standings
standings = league.get_standings()
standings.to_csv(filename+"_standings.csv", index=False)

# export all results
league.get_all_result_data().to_csv(filename+"_all_results.csv", index=False)

# export player records
league.get_all_player_records().to_csv(filename+"_records.csv", index=False)

player_ls = standings['player'].to_list()
points_ls = standings['league points'].to_list()

for idx, player in enumerate(player_ls):
    print(f"{player} - {points_ls[idx]}")
