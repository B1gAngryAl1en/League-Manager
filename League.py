import pandas as pd


class League:

    def __init__(self, name: str, win_pts: int = 3, draw_pts: int = 1, loss_pts: int = 0) -> None:
        self.name = name
        self.league_points_dict = {'win': win_pts,
                                   'draw': draw_pts,
                                   'loss': loss_pts}

        self.result_col_lbl = ['round', 'game', 'player', 'pts for', 'pts against', 'delta', 'result']
        self.results_data_df = pd.DataFrame(columns=self.result_col_lbl)
        self.player_col_lbl = ['name', 'faction', 'notes']
        self.player_data_df = pd.DataFrame(columns=self.player_col_lbl)
        self.add_player(name='none', faction='', note='null player for bye result etc')

    def load_league_data(self) -> bool:
        data_loaded = False
        filename = self.name.lower().replace(" ", "")
        try:
            self.results_data_df = pd.read_csv(filename + "_results.csv")
        except:
            pass
        else:
            self.player_data_df = pd.read_csv(filename + "_players.csv")
            data_loaded = True

        return data_loaded

    def save_league_data(self) -> bool:
        data_saved = False
        filename = self.name.lower().replace(" ", "")
        try:
            self.results_data_df.to_csv(filename + "_results.csv", index=False)
        except:
            pass
        else:
            self.player_data_df.to_csv(filename + "_players.csv", index=False)
            data_saved = True

        return data_saved

    def get_num_players(self) -> int:
        num_players = len(self.player_data_df['name'].to_list())

        return num_players

    def add_player(self, name: str, faction: str, note: str) -> bool:
        player_added = False
        name = name.lower()

        player_data = [[name, faction, note]]
        if not self.player_check(name):
            new_player_df = pd.DataFrame(data=player_data, columns=self.player_col_lbl)
            self.player_data_df = pd.concat(objs=[self.player_data_df, new_player_df], ignore_index=True)
            player_added = True

        return player_added

    def update_player(self, name: str, faction: str, note: str) -> bool:
        player_updated = False
        name = name.lower()

        if self.player_check(name):
            player_updated = True
            self.player_data_df.loc[self.player_data_df['name'] == name, ['faction', 'notes']] = [faction, note]
        return player_updated

    def list_players(self) -> list:
        return self.player_data_df['name'].to_list()

    def get_all_player_data(self) -> pd.DataFrame:

        return self.player_data_df

    def add_result(self, rnd: int, game: int,
                   pl_a: str, sc_a: int,
                   pl_b: str, sc_b: int) -> str:

        player_a_result = ""
        player_b_result = ""

        if self.check_for_result(rnd=rnd, game=game):
            result_added = "result already exists"

        else:
            if not self.player_check(pl_a) or not self.player_check(pl_b):
                result_added = "player not recognised"
            else:
                if sc_a > sc_b:
                    player_a_result = "win"
                    player_b_result = "loss"
                elif sc_a < sc_b:
                    player_a_result = "loss"
                    player_b_result = "win"
                elif sc_a == sc_b:
                    player_a_result = "draw"
                    player_b_result = "draw"

                result_data = [[rnd, game,
                                pl_a, sc_a, sc_b, sc_a - sc_b, player_a_result],
                               [rnd, game,
                                pl_b, sc_b, sc_a, sc_b - sc_a, player_b_result]]
                new_result_df = pd.DataFrame(data=result_data, columns=self.result_col_lbl)
                self.results_data_df = pd.concat(objs=[self.results_data_df, new_result_df])
                result_added = "result added"

        return result_added

    def check_for_result(self, rnd: int, game: int) -> bool:
        return_val = False
        mask = (self.results_data_df['round'] == rnd) & (self.results_data_df['game'] == game)
        if any(mask):
            return_val = True
        return return_val

    def get_result_data(self, rnd: int, game: int) -> pd.DataFrame:
        output_df = pd.DataFrame()
        mask = (self.results_data_df['round'] == rnd) & (self.results_data_df['game'] == game)
        if any(mask):
            output_df = self.results_data_df[mask]

        return output_df

    def get_all_result_data(self) -> pd.DataFrame:

        return self.results_data_df

    def player_check(self, name: str) -> bool:
        return_val = False
        if name.lower() in self.player_data_df['name'].to_list():
            return_val = True
        return return_val

    def get_num_results(self) -> int:
        num_results = len(self.results_data_df['round'].to_list())

        return num_results

    def delete_result(self, rnd: int, game: int) -> bool:
        result_deleted = False
        if not self.check_for_result(rnd=rnd, game=game):
            mask = (self.results_data_df['round'] == rnd) & (self.results_data_df['game'] == game)
            mask = ~mask
            self.results_data_df = self.results_data_df[mask]
            result_deleted = True

        return result_deleted

    def get_standings(self) -> pd.DataFrame:
        standings_df = self.results_data_df.copy()
        standings_df.sort_values(by=['round'], inplace=True)
        standings_df['league pts'] = standings_df['result'].map(self.league_points_dict)

        standings_df_group = standings_df.groupby('player')

        player_ls = []
        league_pts_ls = []
        game_pts_ls = []
        played_ls = []
        wins_ls = []
        draws_ls = []
        losses_ls = []
        record_ls = []

        for player, frame in standings_df_group:
            if player != 'none':
                player_ls.append(player)
                league_pts_ls.append(frame['league pts'].sum())
                game_pts_ls.append(frame['pts for'].sum())
                played_ls.append(len(frame['result'].to_list()))
                wins_ls.append(frame.loc[frame['result'] == 'win']['player'].count())
                draws_ls.append(frame.loc[frame['result'] == 'draw']['player'].count())
                losses_ls.append(frame.loc[frame['result'] == 'loss']['player'].count())
                record_ls.append("")
                for result in frame['result'].to_list():
                    if result == 'win':
                        record_ls[-1] += 'W '
                    if result == 'draw':
                        record_ls[-1] += 'D '
                    if result == 'loss':
                        record_ls[-1] += 'L '

        standings_df = pd.DataFrame(data=zip(player_ls,
                                             league_pts_ls,
                                             game_pts_ls,
                                             played_ls,
                                             wins_ls,
                                             draws_ls,
                                             losses_ls,
                                             record_ls),
                                    columns=['player',
                                             'league points',
                                             'game points',
                                             'played',
                                             'wins',
                                             'draws',
                                             'losses',
                                             'record'])

        standings_df.sort_values(by=['league points', 'game points'],
                                 ascending=False, inplace=True, ignore_index=True)

        positions_ls = []
        players = len(player_ls)
        for pos in range(1, players+1):
            positions_ls.append(pos)

        standings_df['pos'] = positions_ls
        pos_col = standings_df.pop('pos')
        standings_df.insert(1, pos_col.name, pos_col)

        return standings_df

    def get_player_record(self, player_name) -> pd.DataFrame:
        records_df = self.results_data_df.copy()

        records_df_group = records_df.groupby('player')

        player_record_df = records_df_group.get_group(player_name).copy()
        player_record_df.sort_values(by='round', inplace=True, ignore_index=True)

        player_record_df['league pts'] = player_record_df['result'].map(self.league_points_dict)

        player_record_df['cumulative league pts'] = player_record_df['league pts'].cumsum()
        player_record_df['cumulative game pts'] = player_record_df['pts for'].cumsum()
        player_record_df['cumulative game pts delta'] = player_record_df['delta'].cumsum()

        round_ls = player_record_df['round'].to_list()
        game_ls = player_record_df['game'].to_list()
        oppo_ls = []

        for idx, rnd in enumerate(round_ls):
            game = game_ls[idx]
            oppo = self.results_data_df.loc[
                (self.results_data_df['round'] == rnd) &
                (self.results_data_df['game'] == game) &
                (self.results_data_df['player'] != player_name)]['player'].to_list()[0]
            oppo_ls.append(oppo)

        player_record_df['opponent'] = oppo_ls
        player_record_df.rename(columns={'pts for': 'game pts',
                                         'delta': 'game pts delta'}, inplace=True)
        player_record_df.drop(columns=['pts against', 'game'], inplace=True)
        player_record_cols = ['player',
                              'round',
                              'opponent',
                              'result',
                              'league pts',
                              'game pts',
                              'game pts delta',
                              'cumulative league pts',
                              'cumulative game pts',
                              'cumulative game pts delta']

        player_record_df = player_record_df.reindex(columns=player_record_cols)

        blank_row_df = pd.DataFrame(data=[['']*len(player_record_cols)], columns=player_record_cols)
        player_record_df = pd.concat(objs=[player_record_df, blank_row_df])

        return player_record_df


        ## add function to get all player records
