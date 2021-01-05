import sys
import leaguepedia_parser as lp
import json
import global_functions as gf
from tqdm import tqdm 

import sys
import leaguepedia_parser as lp
import json
from tqdm import tqdm 

FILE_PATH_TO_WRITE = 'pb_files/'
FILE_TO_READ = 'pb_files/regions_to_query.txt'
Pick_Ban_Positions_Strings = {
        'Blue Ban 1' : 0,
        'Red Ban 1' : 0,
        'Blue Ban 2' : 0,
        'Red Ban 2' : 0,
        'Blue Ban 3' : 0,
        'Red Ban 3' : 0,
        'Blue Pick 1' : 0,
        'Blue Pick 1' : 0,
        'Red Pick 1' : 0,
        'Red Pick 2' : 0,
        'Blue Pick 2' : 0,
        'Blue Pick 3' : 0,
        'Red Ban 4' : 0,
        'Blue Ban 4' : 0,
        'Red Ban 5' : 0,
        'Blue Ban 5' : 0,
        'Red Pick 4' : 0,
        'Blue Pick 4' : 0,
        'Blue Pick 5' : 0,
        'Red Pick 5' : 0
    }
pb_json_players = {
    'players': {},
    'exceptions': {}
}##############################################   FUNCTIONS   ############################################## 

def Get_Player_Data(game ,_winning_side):

    #do a loop for the blue and red side team
    for i in game['BLUE']['players']:
        #print(i['uniqueIdentifiers']['leaguepedia'])
        #print(i['uniqueIdentifiers']['leaguepedia']['name'])
        player_name = Get_Player_Name(i)
        if player_name not in pb_json_players['players'].keys():
            pb_json_players['players'][player_name] = {
                    'role': i['role'],
                    'champions': {}
            }
        if i['championName'] not in pb_json_players['players'][player_name]['champions'].keys():
            pb_json_players['players'][player_name]['champions'][i['championName']] = {
                    'championId' : i['championId'],
                    'picks' : 0,
                    'wins' : 0
            }
        pb_json_players['players'][player_name]['champions'][i['championName']]['picks'] += 1
        if _winning_side == 'BLUE':
            pb_json_players['players'][player_name]['champions'][i['championName']]['wins'] += 1



    for i in game['RED']['players']:
        player_name = Get_Player_Name(i)
       # print(i['uniqueIdentifiers']['leaguepedia'])
        if player_name not in pb_json_players['players'].keys():
            pb_json_players['players'][player_name] = {
                    'role': i['role'],
                    'champions': {}
                }
        if i['championName'] not in pb_json_players['players'][player_name]['champions'].keys():
            pb_json_players['players'][player_name]['champions'][i['championName']] = {
                    'championId' : i['championId'],
                    'picks' : 0,
                    'wins' : 0
            }
        pb_json_players['players'][player_name]['champions'][i['championName']]['picks'] += 1
        if _winning_side == 'RED':
            pb_json_players['players'][player_name]['champions'][i['championName']]['wins'] += 1

#Sometimes the information for a player only includes his in game name,
#however whenn this is the case the key that holds the value is not called 'name' it is 'gameName'
#therefore we need to check to see if we need to use 'name' or 'gameName' or the key
#this is only an issue with Chinese players as of now
def Get_Player_Name(player_info):

    if 'name' not in player_info['uniqueIdentifiers']['leaguepedia'].keys():
        return player_info['uniqueIdentifiers']['leaguepedia']['gameName']
    return player_info['uniqueIdentifiers']['leaguepedia']['name']
##############################################   FUNCTIONS   ############################################## 

################################################   MAIN   ################################################ 
region = sys.argv[1].split(",")[0].strip()
tournament_name = sys.argv[1].split(",")[1].strip()
tournament_games = []
tournaments = lp.get_tournaments(region, 2020) 
gf.Check_Tournaments(tournaments)
tournament_games = gf.Get_Tournament_Games(tournaments, tournament_name)

print(lp.get_game_details(tournament_games[0])['winner'])

#for i in tqdm (range(len(tournament_games)), desc="In Progress"):
for i in tqdm (range(len(tournament_games))):
    teams = lp.get_game_details(tournament_games[i])['teams']
    winning_side = lp.get_game_details(tournament_games[i])['winner']
    if lp.get_game_details(tournament_games[i])['picksBans'] is not None:
        Get_Player_Data(teams, winning_side)
    else:
        pb_json_players['exceptions'][tournament_games[i]['sources']['leaguepedia']['scoreboardIdWiki']] = 'No Pick Ban found for this match, Match VOD: ' + tournament_games[i]['vod']

with open(FILE_PATH_TO_WRITE+tournament_name+"_Player_Picks.json", "w") as outfile:  
    json.dump(pb_json_players, outfile) 

print(pb_json_players)
################################################   MAIN   ################################################ 
