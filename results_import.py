import pandas as pd

from League import League

# set the game results file name
game_results_file = "test_league_game_results.csv"

league_name = "test_league"

filename = league_name.replace(" ", "").lower()

# set up league, pass win_pts, draw_pts  and loss_pts args to override defaults (3,1,0)
league = League(name=league_name)

# set up players, list of lists [name, faction, note]
players = [['player_a_name', 'player_a_team_name', 'player_a_note'],
           ['player_b_name', 'player_b_team_name', 'player_b_note'],
           ['player_c_name', 'player_c_team_name', 'player_c_note'],
           ['player_d_name', 'player_d_team_name', 'player_d_note']]

for player in players:
    if not league.add_player(name=player[0], faction=player[1], note=player[2]):
        print(f"error: player {player} not added")

league.get_all_player_data().to_csv(filename+"_player_data.csv", index=False)

results_data_df = pd.read_csv(game_results_file)

league.add_result(rnd=1, game=1, pl_a=, pl_b=, sc_a=, sc_b=)



print(results_data_df.head())

