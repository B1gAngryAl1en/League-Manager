# League manager project

## Description

The League Manager project is intended to provide a simple automated solution for
management of league style competitions.

## Set up a League

1. Fork the repository.
2. Open the 'Leagues' and create a copy of the League_Template folder.
3. Give the copy a suitable name.
4. (_Optional_) delete the folders for any existing leagues that are not required.
5. Open the player_list.csv file and add data for the players in the league.
6. Open the league_results.csv file and add fixtures
_(for steps 5 and 6 see the files in the test_league folder or any of the 
existing leagues for the required data formatting)_. 
7. Open the leagues_config.csv file in the top level of the Leagues folder.
8. Add a row for the new league with the league name, name of the folder data folder
(as set in step 3) and the points for wins, draws and losses. Adding a 'y' in the 
update column will cause the league to be updated by the update_league.py script.
9. Run the update_leagues.py script. This will generate output files in the
output_data folder within the league folder (see output files section below)
The readme file will also be updated with links to the summary page for each 
 league within the leagues folder.

## Workflow

1. Update the league_results.csv, ko_stage_results.csv or overall_results.csv
files for the required leagues within their individual folders.
2. Open the leagues_config.csv file and select the leagues to be updated by entering
'y' in the update column on the appropriate rows.
3. Run the update_leagues.py script.
4. The updated data can be accessed using the links in the readme.md file or by opening
the 'output_data' folder within the folder for any individual league.

## Output files

All within the 'output_data' folder within the league folder.

* league_page.md - Summary of the league results including the overall results,
knockout and league stages.
* <league_name>_all_results.csv - raw results data in tidy data format
(provided for checking what the process_results.py script has 
parsed from the fixtures.csv input file)
* <league_name>_player_data.csv - list of players, team names and notes
(provided for checking what the process_results.py script has parsed
from the player_list.csv input file)
* <league_name>_player_records.csv - individual player records for all
players in the league.
* <league_name>_standings.csv - league standings with placings 
determined by league points and then by game points.

## Additional notes

When running the update_leagues.py script error messages may be
displayed in the console. These could concern players that could
not be added (typically due to a non-unique player name) or results
that could not be added (typically due to a repeat combination of
round number and game number or an unrecognised player name). In all
cases the relevant input csv file should be updated, saved and the 
process_results.py script re-run.

Only rows from the input files (overall_results.csv, ko_stage_results.csv, 
league_results.csv) with 'y' in the 'add' column read in and processed by the
update_leagues.py script. This enables fixtures etc to be set up in advance and 
then results added as games are played.

The functions and methods of the League class (League.py file) are 
designed to be agnostic of the front end implementation. They 
could thus be used with a pure python script or a text / graphical
user interface.

---