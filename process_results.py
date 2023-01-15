import pandas as pd

from League import League
from datetime import datetime

# set the league name
league_name = "test league"

# set league points by result type
league_pts = {'win': 3,
              'draw': 1,
              'loss': 0}

# set up league instance
league = League(name=league_name,
                win_pts=league_pts['win'], draw_pts=league_pts['draw'], loss_pts=league_pts['loss'])

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

# generate an update readme file
player_ls = standings_df['player'].to_list()
played_ls = standings_df['played'].to_list()
league_points_ls = standings_df['league points'].to_list()
game_pts_ls = standings_df['game points'].to_list()

with open('input_data/readme_content.md', 'r') as file:
    readme_content = file.read()

with open('readme.md', 'w') as file:
    file.write(f'# {league_name} current standings\n')
    file.write('|Player|played|league pts|game pts|\n')
    file.write('|:---:|:---:|:---:|:---:|\n')

    for idx, player in enumerate(player_ls):
        file.write(f'|{player}|{played_ls[idx]}|{league_points_ls[idx]}|{game_pts_ls[idx]}|\n')

    file.write(f'\nlast updated {datetime.now().strftime("%A %d %B %H:%M")}\n')

    file.write(readme_content)
