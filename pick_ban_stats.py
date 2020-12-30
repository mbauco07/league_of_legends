##############################################   GLOBALS/IMPORTS   ############################################## 
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
pb_json = {}
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

def Check_Tournaments(tournamets):
    if len(tournaments) <= 0:
        sys.exit('ERROR: The inputted parameters returned no tournaments, Check the spelling!!!!')
 

def Get_Picks_And_Bans(_game):
    pbPosition = 0
    for champ in _game:
        #print(champ['championName'] + " is Ban: " + str(champ['isBan'])  + ' Side: ' + champ['team'] + " POS: " + str(pbPosition))
        if champ["championName"] not in pb_json.keys():
            pb_json[champ["championName"]] = {
                'ChampionName' : champ["championName"],
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
            if champ['isBan']:
                  pb_json[champ["championName"]]['Bans'] += 1
            if not champ['isBan']:
                  pb_json[champ["championName"]]['Picks'] += 1
        else:
            if champ['isBan']:
                  pb_json[champ["championName"]]['Bans'] += 1
            if not champ['isBan']:
                  pb_json[champ["championName"]]['Picks'] += 1
                                
        pb_json[champ["championName"]]['Details'][Get_Draft_Position_String(pbPosition)] += 1        
        pbPosition += 1
    print("----------------------------------------------")

def Get_Draft_Position_String(_i):
    switcher = {
        0: 'Blue Ban 1',
        1: 'Red Ban 1',
        2: 'Blue Ban 2',
        3: 'Red Ban 2',
        4: 'Blue Ban 3',
        5: 'Red Ban 3',
        6: 'Blue Pick 1',
        7: 'Blue Pick 1', 
        8: 'Red Pick 1' ,
        9: 'Red Pick 2' ,
        10: 'Blue Pick 2' ,
        11: 'Blue Pick 3' ,
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
##############################################   FUNCTIONS   ############################################## 


##############################################   MAIN   ############################################## 
region = sys.argv[1].split(",")[0].strip()
tournament_name = sys.argv[1].split(",")[1].strip()
champion_name = sys.argv[1].split(",")[2].strip()
tournament_games = []
#print(region)
#print(tournament_name)
#print(champion_name)
#print(lp.get_regions())
tournaments = lp.get_tournaments(region, 2021) 
#print(tournaments)
Check_Tournaments(tournaments)
for i in tournaments:
    if i['name'] == tournament_name:
        tournament_games = lp.get_games(i['overviewPage'])

for game in tqdm (range(len(tournament_games)), desc="In Progress"):
    Get_Picks_And_Bans(lp.get_game_details(tournament_games[game])['picksBans'])


with open(FILE_PATH+tournament_name+"_PickBan.json", "w") as outfile:  
    json.dump(pb_json, outfile) 
##############################################   MAIN   ############################################## 
