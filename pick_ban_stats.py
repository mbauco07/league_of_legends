# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:29:57 2021

@author: Marco Bauco
@about: Will create a json object and save it to a file that holds all information pertanining to a leagues and its teams pick bans data.
"""
##############################################   GLOBALS/IMPORTS   ############################################## 
import sys
import leaguepedia_parser as lp
import json
import global_functions as gf
from tqdm import tqdm 

FILE_PATH = 'pb_files/'
pb_json = {
    'teams': {},
    'overall': {},
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


def Get_Picks_And_Bans(_game, _blue_team, _red_team, win_side_colour):
    pbPosition = 0
    for champ in _game:
        #print(champ['championName'] + " is Ban: " + str(champ['isBan'])  + ' Side: ' + champ['team'] + " POS: " + str(pbPosition))
      
        if champ["championName"] not in pb_json['overall'].keys():
            Add_Champion_Information_No_Team(True, champ)
        else:
<<<<<<< Updated upstream
            Add_Champion_Information_No_Team(False, champ)  #Does the data entry for the champion entry without team information
        pb_json['overall'][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       

=======
            Add_Champion_Information_No_Team(False, champ)
        #we also to make sure that we don;t have redudant empty space we will only add pertinant information
        if Get_Draft_Position_String(pbPosition) in pb_json['overall'][champ["championName"]]['Details'].keys():
            pb_json['overall'][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       
        else:
            pb_json['overall'][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] = 1     
       #also add a win if necessary     
        if champ['team'] == win_side_colour:
            pb_json['overall'][champ["championName"]]['Wins'] += 1
>>>>>>> Stashed changes
        #before we add a champion to a team we need to know which team to add to
        if "Blue" in Get_Draft_Position_String(pbPosition):
            #add to the side on blue side
            #data entry for the team entry BLUE TEAM
            if _blue_team not in pb_json['teams'].keys():
                Add_Champion_Information_With_Team(True, champ, _blue_team)
            else:
                Add_Champion_Information_With_Team(False, champ, _blue_team)
            #we also to make sure that we don;t have redudant empty space we will only add pertinant information
            if Get_Draft_Position_String(pbPosition) in pb_json['teams'][_blue_team][champ["championName"]]['Details'].keys():
                pb_json['teams'][_blue_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       
            else:
                  pb_json['teams'][_blue_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] = 1      
            if champ['team'] == win_side_colour:
               pb_json['teams'][_blue_team][champ["championName"]]['Wins'] += 1
        else:
            #data entry for the team entry RED TEAM
            if _red_team not in pb_json['teams'].keys():
                Add_Champion_Information_With_Team(True, champ, _red_team)
            else:
                Add_Champion_Information_With_Team(False, champ, _red_team)
            if Get_Draft_Position_String(pbPosition) in pb_json['teams'][_red_team][champ["championName"]]['Details'].keys():
                pb_json['teams'][_red_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       
            else:
                  pb_json['teams'][_red_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] = 1    
            if champ['team'] == win_side_colour:
               pb_json['teams'][_red_team][champ["championName"]]['Wins'] += 1
        pbPosition += 1


def Add_Champion_Information_No_Team(_first_time: bool, _champion):
    if _first_time:
            pb_json['overall'][_champion["championName"]] = {
                'ChampionID' : _champion["championId"],
                    'Picks' : 0,
                    'Bans' : 0,
                    'Details' :{},
                    'Wins' : 0
                }
            if _champion['isBan']:
                   pb_json['overall'][_champion["championName"]]['Bans'] += 1
            if not _champion['isBan']:
                   pb_json['overall'][_champion["championName"]]['Picks'] += 1
    else:
            if _champion['isBan']:
                   pb_json['overall'][_champion["championName"]]['Bans'] += 1
            if not _champion['isBan']:
                   pb_json['overall'][_champion["championName"]]['Picks'] += 1


def Add_Champion_Information_With_Team(_first_time: bool, _champion, _team):
    if _first_time:
            pb_json['teams'][_team] = {
                _champion["championName"]: {
                    'ChampionID' : _champion["championId"],
                        'Picks' : 0,
                        'Bans' : 0,
                        'Details' :{},
                        'Wins' : 0
                    }
            }
            if _champion['isBan']:
                   pb_json['teams'][_team][_champion["championName"]]['Bans'] += 1
            if not _champion['isBan']:
                   pb_json['teams'][_team][_champion["championName"]]['Picks'] += 1

    elif _champion['championName'] not in pb_json['teams'][_team].keys():
            pb_json['teams'][_team][_champion['championName']] = {
                    'ChampionID' : _champion["championId"],
                        'Picks' : 0,
                        'Bans' : 0,
                        'Details' :{},
                        'Wins' : 0
                    }
            if _champion['isBan']:
                pb_json['teams'][_team][_champion['championName']]['Bans'] += 1
            if not _champion['isBan']:
                pb_json['teams'][_team][_champion['championName']]['Picks'] += 1

    else:
        if _champion['isBan']:
            pb_json['teams'][_team][_champion["championName"]]['Bans'] += 1
        if not _champion['isBan']:
            pb_json['teams'][_team][_champion["championName"]]['Picks'] += 1                                

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
tournament_name = sys.argv[2]
tournament_games = []
<<<<<<< Updated upstream
tournaments = lp.get_tournaments(region, 2021) 
gf.Check_Tournaments(tournaments)
tournament_games = gf.Get_Tournament_Games(tournaments, tournament_name)


=======
#print(region)
#print(tournament_name)
#print(champion_name)
#print(lp.get_regions())
tournaments = lp.get_tournaments(region, 2021) 
Check_Tournaments(tournaments)
for i in tournaments:
    if i['name'] == tournament_name:
        tournament_games = lp.get_games(i['overviewPage'])
>>>>>>> Stashed changes
for i in tqdm (range(len(tournament_games)), desc="In Progress"):
    #some tournament sometimes do a blind pick first match in a series and therefore there is no pick ban for this, however every subsequent games does there fore we need to skip this games 
    #but also tell the user why we skipped
    if lp.get_game_details(tournament_games[i])['picksBans'] is not None:
        Get_Picks_And_Bans(lp.get_game_details(tournament_games[i])['picksBans'], tournament_games[i]['teams']['BLUE']['name'],tournament_games[i]['teams']['RED']['name'], tournament_games[i]['winner'])
    else:
        pb_json['exceptions'][tournament_games[i]['sources']['leaguepedia']['scoreboardIdWiki']] = 'No Pick Ban found for this match, Match VOD: ' + tournament_games[i]['vod']

with open(FILE_PATH+tournament_name+"_PickBan.json", "w") as outfile:  
    json.dump(pb_json, outfile) 
##############################################   MAIN   ############################################## 
