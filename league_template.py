import pandas as pd

from League import League

# set the league name and points for each result
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

# round 1 games, list of lists [game, player a, player a score, player b, player b score]
rnd_1 = [[1, 'player_a_name', 100, 'none', 0],
         [2, 'player_c_name', 100, 'player_d_name', 0]]

# round 2 games
rnd_2 = [[1, 'player_a_name', 100, 'player_c_name', 0],
         [2, 'player_b_name', 100, 'player_d_name', 0]]

# round 3 games
rnd_3 = [[1, 'player_a_name', 100, 'player_d_name', 0],
         [2, 'player_b_name', 100, 'player_c_name', 0]]

# add more rounds as required

# list of game rounds to add to results
rounds = [rnd_1, rnd_2, rnd_3]

# add results to the League instance
for rnd, game_round in enumerate(rounds):
    for game in game_round:
        result = league.add_result(rnd=rnd+1, game=game[0],
                                   pl_a=game[1], sc_a=game[2],
                                   pl_b=game[3], sc_b=game[4])
        if result != 'result added':
            print(f"error: round: {rnd+1}, game: {game}, - {result}")

# export standings
league.get_standings().to_csv(filename+"_standings.csv", index=False)

# export all results
league.get_all_result_data().to_csv(filename+"_all_results.csv", index=False)

# get player records, combine into a single dataframe and export
# move this to a function in League
df_init = False
records_df = pd.DataFrame
for player in league.list_players():
    if player != 'none':
        if not df_init:
            records_df = league.get_player_record(player)
            df_init = True
        else:
            records_df = pd.concat(objs=[records_df, league.get_player_record(player)])

# export player records
records_df.to_csv(filename+"_records.csv", index=False)

