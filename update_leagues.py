import pandas as pd

from league_class import League
from datetime import datetime

league_config_df = pd.read_csv('Leagues/leagues_config.csv')

for league_idx, league_name in enumerate(league_config_df['league_name'].to_list()):
    if str(league_config_df.loc[league_idx]['update']).lower() == 'y':
        print(f'Updating {league_name}')
        data_folder = league_config_df.loc[league_idx]['data_folder']

        # set up league instance
        league = League(name=league_name,
                        win_pts=league_config_df.loc[league_idx]['win_pts'],
                        draw_pts=league_config_df.loc[league_idx]['draw_pts'],
                        loss_pts=league_config_df.loc[league_idx]['loss_pts'])

        # get player list and add players
        players_df = pd.read_csv(f'Leagues/{data_folder}/player_list.csv')
        for player_idx, player_name in enumerate(players_df['player_name'].to_list()):
            if player_name != "":
                name = player_name
                team = players_df.loc[player_idx]['player_team_name']
                note = players_df.loc[player_idx]['player_note']
                if not league.add_player(name=name, team=team, note=note):
                    print(f"error: player {player_name} not added")

        # get game results and add them
        results_data_df = pd.read_csv(f'Leagues/{data_folder}/league_results.csv')
        for (result_idx, rnd) in enumerate(results_data_df['round'].to_list()):
            if str(results_data_df.loc[result_idx]['add']).lower() == 'y':
                game = results_data_df.loc[result_idx]['game']
                player_a = results_data_df.loc[result_idx]['player_a']
                player_b = results_data_df.loc[result_idx]['player_b']
                player_a_score = results_data_df.loc[result_idx]['player_a_sc']
                player_b_score = results_data_df.loc[result_idx]['player_b_sc']
                return_msg = league.add_result(rnd=rnd, game=game,
                                               pl_a=player_a, sc_a=player_a_score,
                                               pl_b=player_b, sc_b=player_b_score)
                if return_msg != 'result added':
                    print(f"Error: round: {rnd}, game: {game}, - {return_msg}")

        # get dataframes from the league instance
        player_data_df = league.get_all_player_data()
        standings_df = league.get_standings()
        all_results_df = league.get_all_result_data()
        player_records_df = league.get_all_player_records()

        # export files
        filename = league_name.replace(" ", "-")
        player_data_df.to_csv(f'Leagues/{data_folder}/output_data/{filename}_player_data.csv', index=False)
        standings_df.to_csv(f'Leagues/{data_folder}/output_data/{filename}_standings.csv', index=False)
        all_results_df.to_csv(f'Leagues/{data_folder}/output_data/{filename}_all_results.csv', index=False)
        player_records_df.to_csv(f'Leagues/{data_folder}/output_data/{filename}_player_records.csv', index=False)

        # update league page
        overall_results_df = pd.read_csv(f'Leagues/{data_folder}/overall_results.csv')
        ko_stage_results_df = pd.read_csv(f'Leagues/{data_folder}/ko_stage_results.csv')

        with open(f'Leagues/{data_folder}/output_data/league_page.md', 'w') as file:

            file.write(f'# {league_name}\n\n')
            file.write(f'last updated {datetime.now().strftime("%A %d %B %H:%M")}\n\n')
            file.write('---\n')

            if 'y' in overall_results_df['add'].to_list() or 'Y' in overall_results_df['add'].to_list():
                file.write('## Overall Results \n\n')
                for overall_idx, placing in enumerate(overall_results_df['placing'].to_list()):
                    if str(overall_results_df.loc[overall_idx]['add']).lower() == 'y':
                        file.write(f'{placing} - {overall_results_df.loc[overall_idx]["player_name"]}\n\n')
                file.write('---\n\n')

            if 'y' in ko_stage_results_df['add'].to_list() or 'Y' in overall_results_df['add'].to_list():
                file.write('## Knockout Stage Results \n\n')
                for ko_idx, ko_game in enumerate(ko_stage_results_df['game'].to_list()):
                    if str(ko_stage_results_df.loc[ko_idx]['add']).lower() == 'y':
                        ko_pa = ko_stage_results_df.loc[ko_idx]['player_a']
                        ko_pa_sc = ko_stage_results_df.loc[ko_idx]['player_a_score']
                        ko_pb = ko_stage_results_df.loc[ko_idx]['player_b']
                        ko_pb_sc = ko_stage_results_df.loc[ko_idx]['player_b_score']
                        if pd.notnull(ko_stage_results_df.loc[ko_idx]['game_note']):
                            game_note = ko_stage_results_df.loc[ko_idx]['game_note']
                        else:
                            game_note = ''
                        file.write(f'{ko_game}: {ko_pa} ({ko_pa_sc}) vs. {ko_pb} ({ko_pb_sc}) {game_note}\n\n')
                file.write('---\n\n')

            file.write('## League Standings\n\n')
            file.write(f'[Fixtures and results](/Leagues/{data_folder}/league_results.csv)\n\n')
            file.write('|Pos|Player|played|league pts|game pts|\n')
            file.write('|:---:|:---:|:---:|:---:|:---:|\n')

            pos_ls = standings_df['pos'].to_list()
            player_ls = standings_df['player'].to_list()
            played_ls = standings_df['played'].to_list()
            league_pts_ls = standings_df['league points'].to_list()
            game_pts_ls = standings_df['game points'].to_list()

            for pos_idx, pos in enumerate(pos_ls):
                file.write(f'|{pos}|{player_ls[pos_idx]}|{played_ls[pos_idx]}|'
                           f'{league_pts_ls[pos_idx]}|{game_pts_ls[pos_idx]}|\n')
            file.write('\n')
            file.write(f'[Full standings]'
                       f'(/Leagues/{data_folder}/output_data/{filename}_standings.csv)\n\n')
            file.write(f'[Player performance records]'
                       f'(/Leagues/{data_folder}/output_data/{filename}_player_records.csv)\n\n')
            file.write(f'[Player list and data]'
                       f'(/Leagues/{data_folder}/output_data/{filename}_player_data.csv)\n\n')
            file.write(f'[Raw results data]'
                       f'(/Leagues/{data_folder}/output_data/{filename}_all_results.csv)\n\n')
            file.write('---\n\n')
            file.write('powered by [League Manager](/league_manager_project.md)')
        print(f"Update of {league_name} complete")

with open(f'readme.md', 'w') as file:
    file.write('# Current leagues:\n\n')
    for lge_idx, league_name in enumerate(league_config_df['league_name'].to_list()):
        file.write(f'[{league_name}]'
                   f'(/Leagues/{league_config_df.loc[lge_idx]["data_folder"]}/output_data/league_page.md)\n\n')

    file.write('---\n\n')
    file.write('# League Manager Project\n\n')
    file.write('The league manager project is intended to provide a simple automated solution for '
               'management of league style competitions. \n\n')
    file.write('More information on the project can be found [here](/league_manager_project.md)\n\n')
    file.write('---')
