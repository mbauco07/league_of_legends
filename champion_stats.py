#This script will ask for a champ or champs and will get their stats, stats per level, etc and then compare build with items included.


#import keys as ks
import deprecated_functions as dep_funcs
import special_scaling_values as ssv
import requests
import sys
import math
from prettytable import PrettyTable
from prettytable import from_csv
import pandas as pd
import numpy as np
import random
import os
import leaguepedia_parser as lp
import mwclient
import matplotlib as plt

xValues_lvls = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
BASIC_TABLE = {}
STAT_DICTIONARY = {}
NO_DECIMAL_PLACES = 0
TWO_DECIMAL_PLACES = 2
ALL_ITEMS_DFs = {}
MAIN_DIRECTORY = './statsheets'




#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#
#we need to account for champions that have a special scaling that is different then the rest of the champions (I.E. Tristanna or Cassieopia) because of this
#we must check to see if we are dealing with one of these special cases and adjust our output for it.
#this will also only output levels 1 and 18 not in between
def Basic_Stats_Output(_data, _championName):   
    basic_table = PrettyTable()
    basic_table.title = 'Basic Stats for: ' + _championName + ' at Level 1 and 18'

    basic_table.field_names=["Stat", "Level 1", "Level 18", "per level"]
    basic_table.add_row(['Health', _data['hp'], (_data['hp']+(_data['hpperlevel']*17)), _data['hpperlevel']])
    basic_table.add_row(['Mana/Resource', _data['mp'], (_data['mp']+(_data['mpperlevel']*17)), _data['mpperlevel']])

    #are we dealing with Cassiopeia?
    if _championName != 'Cassiopeia':
        basic_table.add_row(['Move Speed', _data['movespeed'], _data['movespeed'], 'N/A'])
    else: #we are dealing with Cassiopeia
        basic_table.add_row(['Move Speed***', _data['movespeed']+ssv.cass_ms_per_level , (_data['movespeed']+ssv.cass_ms_per_level)+(ssv.cass_ms_per_level*17), ssv.cass_ms_per_level])

    basic_table.add_row(['Armor', Normal_Round(_data['armor']), (Normal_Round(_data['armor']+(_data['armorperlevel']*17))), _data['armorperlevel']])
    basic_table.add_row(['Magic Resistance', round(_data['spellblock']), Normal_Round((_data['spellblock']+(_data['spellblockperlevel']*17))), _data['spellblockperlevel']])

    #are we dealing with Tristana?
    if _championName != 'Tristana':
        basic_table.add_row(['Attack Range', _data['attackrange'], _data['attackrange'], 'N/A'])
    else:
        basic_table.add_row(['Attack Range***', _data['attackrange'], _data['attackrange']+(ssv.tristanna_range_per_level*17), ssv.tristanna_range_per_level])
    
    basic_table.add_row(['HP Regeneration', round(_data['hpregen']), Normal_Round((_data['hpregen']+(_data['hpregenperlevel']*17))), _data['hpregenperlevel']])
    basic_table.add_row(['Mana/Resource Regeneration', round(_data['mpregen']), Normal_Round((_data['mpregen']+(_data['mpregenperlevel']*17))), _data['mpregenperlevel']])
    basic_table.add_row(['Critical Strike', _data['crit'], (_data['crit']+(_data['critperlevel']*17)), _data['critperlevel']])
    basic_table.add_row(['Attack Damage', round(_data['attackdamage']), round((_data['attackdamage']+(_data['attackdamageperlevel']*17))), _data['attackdamageperlevel']])
    basic_table.add_row(['Attack Speed', Round_Half_Up(_data['attackspeed'],2), Round_Half_Up(((Round_Half_Up(_data['attackspeed'],2)*((_data['attackspeedperlevel']*17)))/100) + round(_data['attackspeed'],2),2) , _data['attackspeedperlevel']])
    print(basic_table)

#this will work similliarly to Basic_Stats_Output however instead this wissssll output each level for a champion
#also at the same create a dictionary so we can create a pandas dataframe.
def Per_Level_Stats_Output(_table_name, _data, _championName):

    #HEALTH
    Create_Entry_For_Dictionary('Health', _data['hp'], _data['hpperlevel'], NO_DECIMAL_PLACES)

    #MANA   
    Create_Entry_For_Dictionary('Mana/Resource', _data['mp'], _data['mpperlevel'], NO_DECIMAL_PLACES)

    #MOVE SPEED
    #are we dealing with Cassiopeia?
    if _championName != 'Cassiopeia':
        Create_Entry_For_Dictionary('Move Speed', _data['movespeed'], 0, NO_DECIMAL_PLACES)
    else: #we are dealing with Cassiopeia
        Create_Entry_For_Dictionary('Move Speed', _data['movespeed']+ssv.cass_ms_per_level, ssv.cass_ms_per_level, NO_DECIMAL_PLACES)

    #ARMOR
    Create_Entry_For_Dictionary('Armor', _data['armor'], _data['armorperlevel'], NO_DECIMAL_PLACES)
    
    #MR
    Create_Entry_For_Dictionary('Magic Resistance', _data['spellblock'], _data['spellblockperlevel'], NO_DECIMAL_PLACES)

    #ATTACK RANGE
    #are we dealing with Tristana?
    if _championName != 'Tristana':
        Create_Entry_For_Dictionary('Attack Range', _data['attackrange'], 0, NO_DECIMAL_PLACES)
    else:
        Create_Entry_For_Dictionary('Attack Range', ssv.tristanna_range_per_level, 0, NO_DECIMAL_PLACES)

    #HP REGEN
    Create_Entry_For_Dictionary('HP Regeneration', _data['hpregen'], _data['hpregenperlevel'],NO_DECIMAL_PLACES)

    #CRIT
    Create_Entry_For_Dictionary( 'Critical Strike', _data['crit'], _data['critperlevel'],NO_DECIMAL_PLACES)

    #ATTACK DAMAGE
    Create_Entry_For_Dictionary( 'Attack Damage', _data['attackdamage'], _data['attackdamageperlevel'],NO_DECIMAL_PLACES)

    #ATTACK SPEED
    Create_Entry_For_Dictionary( 'Attack Speed', _data['attackspeed'], _data['attackspeedperlevel'],TWO_DECIMAL_PLACES)


def Create_Entry_For_Dictionary(_statName, _startingValue, _perLevelValue, rounding_type):
    if rounding_type == 0: # we are rounding to 0 decimal places:
        values = [
            Normal_Round(_startingValue+(_perLevelValue*0)),   
            Normal_Round(_startingValue+(_perLevelValue*1)),  
            Normal_Round(_startingValue+(_perLevelValue*2)),  
            Normal_Round(_startingValue+(_perLevelValue*3)),   
            Normal_Round(_startingValue+(_perLevelValue*4)),  
            Normal_Round(_startingValue+(_perLevelValue*5)),   
            Normal_Round(_startingValue+(_perLevelValue*6)),   
            Normal_Round(_startingValue+(_perLevelValue*7)),   
            Normal_Round(_startingValue+(_perLevelValue*8)),  
            Normal_Round(_startingValue+(_perLevelValue*9)),  
            Normal_Round(_startingValue+(_perLevelValue*10)),   
            Normal_Round(_startingValue+(_perLevelValue*11)),   
            Normal_Round(_startingValue+(_perLevelValue*12)),   
            Normal_Round(_startingValue+(_perLevelValue*13)),   
            Normal_Round(_startingValue+(_perLevelValue*14)),   
            Normal_Round(_startingValue+(_perLevelValue*15)),   
            Normal_Round(_startingValue+(_perLevelValue*16)),   
            Normal_Round(_startingValue+(_perLevelValue*17)),   
        ]
        
    else: #we are rounding with 2 decimal places
        values = [
            round(_startingValue+(_startingValue*(_perLevelValue*0)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*1)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*2)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*3)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*4)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*5)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*6)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*7)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*8)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*9)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*10)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*11)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*12)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*13)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*14)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*15)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*16)/100),2),   
            round(_startingValue+(_startingValue*(_perLevelValue*17)/100),2)          
        ]

    STAT_DICTIONARY[_statName] = values


#when items are added to the arguments, we must get each of the items stats and add them to the Per_Level_Table_Output so we can show the differences
def Get_Item_Stat_Modifier(_item):
    new_item_df = champ_perLvl_Stats_df.copy()
    for stat in _item:
        #remove any spaces for the stat value variable tht can occur when splitting
        stat = stat.lstrip()
        statName = stat.split(" ", 1)[1]
        statValue =  stat.split(" ", 1)[0]
        #create a copy of the df for the specific item.
        #new_df = modify_stat_of_df(Get_Stat_helper(stat), item['stats'][stat], new_df)
        new_item_df = Modify_Stat_Of_Df(statName, statValue, new_item_df)
        #create a new csv file with the item changes
    name_of_file = item['name']+'.csv'
    Save_To_File(champion, new_item_df, name_of_file)
    ALL_ITEMS_DFs[item['name']] = new_item_df


def Modify_Stat_Of_Df(_stat, _statValue, _df):
    #we need to check if the stat that we are modify exists for example Ability Haste isn't a stat that champion start with it
    if _stat not in _df.columns:
        #we add a column for that stat.
        _df[_stat] = 0


    #we need to check if the stat is modyfing or taget stat by a percent or flat.
    if '%' in _statValue: #we add the value as a percent
        _statValue  =_statValue.replace('%', '')
        _df[_stat] = _df[_stat].apply(lambda x: (x + (x*(int(_statValue)/100)),2))
    else: #we add the value flat.           
        _df[_stat] = _df[_stat].apply(lambda x: x + int(_statValue))

    return _df

#for some champion names that have a space or a special characther, they need to be removed so that champion can be correctly found
def Validate_Champ_Input(_champion):
    #check if the champion name has a space in it.
    if  ' ' in _champion:
        _champion  =_champion.replace(' ', '')
    
    if '\'' in _champion:
        x  =  _champion.split("\'", 2)
        _champion  =  x[0]+''+x[1].lower()

    return _champion

#we use this for values we round to the ones because of how python takes care of rounding on x.5.
#using round() is will always round down in these situations however we need to to round up instead
def Normal_Round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def Round_Half_Up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def Check_Response_Code(_response, _type):
    if response_champ.status_code != 200:
        raise Exception("An Error Occured for:" +_type+ ' Response Code: ' + str(_response.status_code))


def Split_Item_Stat_String(_string):
    print("1")
    #print(re.split(r'(?<=\d)\D', _string))

def Random_Color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def Save_To_File(_champion,_df, _file_name):

    #check if the champion directory already exists
    if os.path.isdir(MAIN_DIRECTORY+"/"+_champion):
        _df.to_csv(MAIN_DIRECTORY+"/"+_champion+"/"+_file_name, index=False) 
    else:
        os.makedirs(MAIN_DIRECTORY+"/"+_champion+"/")
        _df.to_csv(MAIN_DIRECTORY+"/"+_champion+"/"+_file_name, index=False) 


#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#



#------------------------------------------------------------ MAIN ------------------------------------------------------------#\

champion = Validate_Champ_Input(str(sys.argv[1]))
print("champion")
#print ("Number of arguments: " + str(len(sys.argv)))
items_list= []
response_champ = requests.get(ks.DDragon_champs+champion+'.json')
response_items = requests.get(ks.DDragon_items)
Check_Response_Code(response_champ, 'CHAMPS')
Check_Response_Code(response_items, 'ITEMS')
championData = response_champ.json()['data']
itemData = response_items.json()['data']
 #create a basic table that shows the champions level 1 stats,  level 18 stats and the per level stat
Basic_Stats_Output(championData[champion]['stats'], champion)
Per_Level_Stats_Output("inital_table", championData[champion]['stats'], champion)
for i in itemData:
    if itemData[i]['name'] in sys.argv:
        #print(itemData[i])
        items_list.append(itemData[i])
champ_perLvl_Stats_df = pd.DataFrame(data=STAT_DICTIONARY)
name_of_file = "No_Items.csv"
#champ_perLvl_Stats_df.to_csv("./statsheets/"+name_of_file+"", index=False) 

Save_To_File(champion, champ_perLvl_Stats_df.copy(),name_of_file)
with open(MAIN_DIRECTORY+"/"+champion+"/"+name_of_file, 'r') as fp:
    x = from_csv(fp)
 #this add the base champ stats df to the list of all dfs
ALL_ITEMS_DFs['No Items'] = champ_perLvl_Stats_df
 #lets use the dataframe we created and create copies that inheret stats from items so that we can compare them.

itemSoup = ""
for item in items_list:
    itemSoup = bs(item['description'], 'html.parser')
    for br in itemSoup.find_all("br"):
            br.replace_with("\n")
    itemSoup = itemSoup.stats.text.strip().split('\n')
    Get_Item_Stat_Modifier(itemSoup)
#print(lp.get_game_details(tournament_games[0]))
#get all the games where the champion submitted is PICKED not banned.   
# now we create a 

#------------------------------------------------------------ MAIN ------------------------------------------------------------#
