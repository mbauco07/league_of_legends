# -*- coding: utf-8 -*-

#Created on Mon Mar  1 13:29:57 2021

#@author: Marco Bauco
#about: Will create a json object and save it to a file that holds all information pertanining to a leagues and its teams pick bans data.
#
##############################################   GLOBALS/IMPORTS   ############################################## 
import sys
import leaguepedia_parser as lp
import json
import global_functions as gf
from tqdm import tqdm 

FILE_PATH = 'pb_files/'
data_json = {
    'general': {},
    'exceptions': {}
}
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
##############################################   GLOBALS/IMPORTS   ############################################## 



##############################################   FUNCTIONS   ############################################## 


def Get_Draft_Position_String(_i):
    switcher = {
        0: 'Blue Ban 1',
        1: 'Red Ban 1',
        2: 'Blue Ban 2',
        3: 'Red Ban 2',
        4: 'Blue Ban 3',
        5: 'Red Ban 3',
        6: 'Blue Pick 1',
        7: 'Red Pick 1', 
        8: 'Red Pick 2' ,
        9: 'Blue Pick 2' ,
        10: 'Blue Pick 3' ,
        11: 'Red Pick 3' ,
        12: 'Red Ban 4' ,
        13: 'Blue Ban 4' ,
        14: 'Red Ban 5',
        15: 'Blue Ban 5', 
        16: 'Red Pick 4' ,
        17: 'Blue Pick 4',
        18: 'Blue Pick 5' ,
        19: 'Red Pick 5' 
    }
    return switcher.get(_i) 

def Verify_Team_Name(_name):
    if not _name:
        return "all"
    else:
        return _name
##############################################   FUNCTIONS   ############################################## 


##############################################   MAIN   ############################################## 
region = sys.argv[1].split(",")[0].strip()
tournament_name = sys.argv[1].split(",")[1].strip()
tournament_games = []
tournaments = lp.get_tournaments(region, 2021) 
gf.Check_Tournaments(tournaments)
tournament_games = gf.Get_Tournament_Games(tournaments, tournament_name)

#print(region)
#print(tournament_name)
#print(champion_name)
#print(lp.get_regions())
#tournaments = lp.get_tournaments(region, 2021) 
#print(tournaments)
gf.Check_Tournaments(tournaments)
for i in tournaments:
    if i.name == tournament_name:
        tournament_games = lp.get_games(i.overviewPage)
#print(tournament_games)
games = []
for i in tqdm (range(len(tournament_games)), desc="In Progress"):
    #some tournament sometimes do a blind pick first match in a series and therefore there is no pick ban for this, however every subsequent games does there fore we need to skip this games 
    #but also tell the user why we skipped
    #print("--")
    game = lp.get_game_details(tournament_games[i])
    #print("PICK AND BANS: " + str(game.picksBans))
    #print("GAME WINNER: " + str(game.winner))
    #print(game.teams)
    pb_order = game.picksBans
    side_win = game.winner   
    teams = game.teams
    pb_json = gf.Generate_Pick_Ban_Data(pb_order, side_win, teams)
    #if lp.get_game_details(tournament_games[i].picksBans) is not None:
    #    Get_Picks_And_Bans(lp.get_game_details(tournament_games[i].picksBans), tournament_games[i]['teams']['BLUE']['name'],tournament_games[i]['teams']['RED']['name'], tournament_games[i]['winner'])
    #else:
     #   pb_json['exceptions'][tournament_games[i]['sources']['leaguepedia']['scoreboardIdWiki']] = 'No Pick Ban found for this match, Match VOD: ' + tournament_games[i]['vod']

with open(FILE_PATH+tournament_name+"_PickBan.json", "w") as outfile:  
    json.dump(pb_json, outfile) 
##############################################   MAIN   ############################################## 
