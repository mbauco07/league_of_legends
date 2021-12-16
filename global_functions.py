import sys
import leaguepedia_parser as lp

data_json = {
    'general': {},
    'exceptions': {}
}

def Check_Tournaments(_tournaments):
    if len(_tournaments ) <= 0:
        sys.exit('ERROR: The inputted parameters returned no tournaments, Check the spelling!!!!')
 
def Get_Tournament_Games(_tournaments, _tournament_name):
    games = []
    for i in _tournaments:
        if i.name == _tournament_name:
            games = lp.get_games(i.overviewPage)
            break
    return games

#GENERATES BASIC PICK AND BAN DATA NO TEAMS SPECIFICS
def Generate_Pick_Ban_Data(_pb_order, _winning_side, _teams):
    #PB number
    i = 0
    for champ in _pb_order:
       didChampWin = True if (_winning_side.lower()) in Get_Draft_Position_String(i).lower() and ("Pick") in Get_Draft_Position_String(i) else False
       #print(Get_Draft_Position_String(i) +": "+ str(champ.championId) + ": " + champ.championName + " Is Ban?->" + str(champ.isBan) + " did the win?-> " + str(didChampWin)) 
       if champ.championName not in data_json['general'].keys():
                Add_Champion_Data_To_JSON(True, champ.championName, champ.isBan, didChampWin)
       else:
             Add_Champion_Data_To_JSON(False, champ.championName, champ.isBan, didChampWin) #Does the data entry for the champion entry without team information       
       i=i+1
    return data_json

def Add_Champion_Data_To_JSON(_first_time, _champion, _isBan, _won):
    if _first_time:
            data_json['general'][_champion] = {
                    'Picks' : 0,
                    'Bans' : 0,
                    'Wins' : 0
                }
            if _isBan:
                       data_json['general'][_champion]['Bans'] += 1
            if not _isBan:
                   data_json['general'][_champion]['Picks'] += 1
    else:
            if _isBan:
                   data_json['general'][_champion]['Bans'] += 1
            if not _isBan:
                   data_json['general'][_champion]['Picks'] += 1
    if _won:
            data_json['general'][_champion]['Wins'] += 1


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