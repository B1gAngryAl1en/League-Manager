# League manager project

## Description

This project is intended to provide a simple automated solution for
management of league style competitions.

## Set up

1. Fork the repository.
2. _(optional)_ create a local branch for the league you want to run.
This may be useful for running multiple seasons of the same league,
multiple brackets in the same competition etc.
3. Add the name of the league on line 7 of the  process_results.py 
script and save the file.
4. Set the options for readme file generation on lines 10 to 15. Options
are listed below (all content files are in the readme_content folder).
   - Update_readme - set if readme file will be regenerated or not.
   - add_overall_results - add content of the overall_results.md file 
   (update manually before running script).
   - add_ko_stage - add content of the ko_stage_results.md file (update
   manually before running script).
   - add_league_stage - add auto generated league summary table and links
   to output .csv files.
   - add_league_manager_info - add content pf the league_manager_notes.md 
   file.
6. _(optional)_ adjust the league_pts dictionary in the 
process_results.py file (lines 18 to 20) to set the league points for
each type of result (by default win = 3 pts, draw = 1 pt, loss = 0 
pts).
7. Open the player_list.csv file in the input_data folder, add the 
data for players in the league and save it.

## Workflow

1. Open the fixtures.csv file in the input data folder.
2. Add fixtures and scores as required (player names must match those
in the player_list.csv file and the 'played' column must be populated
with 'y' for the result to be read).
Adjust readme file generation options (see set up).
3. Save the file.
4. Run the process_results.py script. 

This will generate updated csv files (see below) in the output_data 
folder and an updated readme.md file with summary league stats and 
links to the csv files with detailed output.

Have a look at the branches of this repository for some worked 
examples.

## Output files

* league_name_all_results.csv - raw results data in tidy data format
(provided for checking what the process_results.py script has 
parsed from the fixtures.csv input file)
* league_name_player_data.csv - list of players, team names and notes
(provided for checking what the process_results.py script has parsed
from the player_list.csv input file)
* league_name_player_records.csv - individual player records for all
players in the league.
* league_name_standings.csv - league standings with placings 
determined by league points and then by game points.

## Additional notes

When running the process_results.py script error messages may be
displayed in the console. These could concern players that could
not be added (typically due to a non-unique player name) or results
that could not be added (typically due to a repeat combination of
round number and game number or an unrecognised player name). In all
cases the relevant input csv file should be updated, saved and the 
process_results.py script re-run.

Only rows from the fixtures.csv file with the 'played' column 
populated with 'y' will be read in by the process_result.py script. 
This enables fixtures to be set up in advance and the scores added as
games are played.

The functions and methods of the League class (League.py file) are 
designed to be agnostic of the front end implementation. They 
could thus be used with a pure python script or a text / graphical
user interface.

---