##############################################   GLOBALS/IMPORTS   ############################################## 
from lol_dto.classes import game
import requests
import sys
import pandas as pd
import numpy as np
import leaguepedia_parser as lp
import matplotlib as plt
import json
import os
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

def Check_Tournaments(_tournaments):
    if len(_tournaments ) <= 0:
        sys.exit('ERROR: The inputted parameters returned no tournaments, Check the spelling!!!!')
 

def Get_Picks_And_Bans(_game, _blue_team, _red_team):
    pbPosition = 0
    for champ in _game:
        #print(champ['championName'] + " is Ban: " + str(champ['isBan'])  + ' Side: ' + champ['team'] + " POS: " + str(pbPosition))
        #Does the data entry for the champion entry without team information
        if champ["championName"] not in pb_json['overall'].keys():
            Add_Champion_Information_No_Team(True, champ)
        else:
            Add_Champion_Information_No_Team(False, champ)
        pb_json['overall'][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       

        #before we add a champion to a team we need to know which team to add to
        if "Blue" in Get_Draft_Position_String(pbPosition):
            #add to the side on blue side
            #data entry for the team entry BLUE TEAM
            if _blue_team not in pb_json['teams'].keys():
                Add_Champion_Information_With_Team(True, champ, _blue_team)
            else:
                Add_Champion_Information_With_Team(False, champ, _blue_team)
            pb_json['teams'][_blue_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       
        else:
            #data entry for the team entry RED TEAM
            if _red_team not in pb_json['teams'].keys():
                Add_Champion_Information_With_Team(True, champ, _red_team)
            else:
                Add_Champion_Information_With_Team(False, champ, _red_team)
            pb_json['teams'][_red_team][champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1       
        pbPosition += 1


def Add_Champion_Information_No_Team(_first_time: bool, _champion):
    if _first_time:
            pb_json['overall'][_champion["championName"]] = {
                'ChampionID' : _champion["championId"],
                    'Picks' : 0,
                    'Bans' : 0,
                    'Details' :{
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
                        'Red Pick 3' : 0,
                        'Red Ban 4' : 0,
                        'Blue Ban 4' : 0,
                        'Red Ban 5' : 0,
                        'Blue Ban 5' : 0,
                        'Red Pick 4' : 0,
                        'Blue Pick 4' : 0,
                        'Blue Pick 5' : 0,
                        'Red Pick 5' : 0                    
                    }
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
                        'Details' :{
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
                            'Red Pick 3' : 0,
                            'Red Ban 4' : 0,
                            'Blue Ban 4' : 0,
                            'Red Ban 5' : 0,
                            'Blue Ban 5' : 0,
                            'Red Pick 4' : 0,
                            'Blue Pick 4' : 0,
                            'Blue Pick 5' : 0,
                            'Red Pick 5' : 0                        }
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
                        'Details' :{
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
                            'Red Pick 3' : 0,
                            'Red Ban 4' : 0,
                            'Blue Ban 4' : 0,
                            'Red Ban 5' : 0,
                            'Blue Ban 5' : 0,
                            'Red Pick 4' : 0,
                            'Blue Pick 4' : 0,
                            'Blue Pick 5' : 0,
                            'Red Pick 5' : 0
                        }
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
tournament_name = sys.argv[1].split(",")[1].strip()
tournament_games = []
#print(region)
#print(tournament_name)
#print(champion_name)
#print(lp.get_regions())
tournaments = lp.get_tournaments(region, 2020) 
#print(tournaments)
Check_Tournaments(tournaments)
for i in tournaments:
    if i['name'] == tournament_name:
        tournament_games = lp.get_games(i['overviewPage'])
for i in tqdm (range(len(tournament_games)), desc="In Progress"):
    #some tournament sometimes do a blind pick first match in a series and therefore there is no pick ban for this, however every subsequent games does there fore we need to skip this games 
    #but also tell the user why we skipped
    if lp.get_game_details(tournament_games[i])['picksBans'] is not None:
        Get_Picks_And_Bans(lp.get_game_details(tournament_games[i])['picksBans'], tournament_games[i]['teams']['BLUE']['name'],tournament_games[i]['teams']['RED']['name'])
    else:
        pb_json['exceptions'][tournament_games[i]['sources']['leaguepedia']['scoreboardIdWiki']] = 'No Pick Ban found for this match, Match VOD: ' + tournament_games[i]['vod']

with open(FILE_PATH+tournament_name+"_PickBan.json", "w") as outfile:  
    json.dump(pb_json, outfile) 
##############################################   MAIN   ############################################## 
