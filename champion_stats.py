#This script will ask for a champ or champs and will get their stats, stats per level, etc and then compare build with items included.
import keys as ks
import special_scaling_values as ssv
import requests
import sys
import math
from prettytable import PrettyTable
import pandas as pd
#because Python does not have a built in Switch statement we will be using a dictionary instead to implement this.

BASIC_TABLE = {}
STAT_DICTIONARY = {}
NO_DECIMAL_PLACES = 0
TWO_DECIMAL_PLACES = 2
#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#
#we need to account for champions that have a special scaling that is different then the rest of the champions (I.E. Tristanna or Cassieopia) because of this
#we must check to see if we are dealing with one of these special cases and adjust our output for it.
#this will also only output levels 1 and 18 not in between
def Basic_Stats_Output(_data, _championName):   
    basic_table = PrettyTable()
    basic_table.title = 'Stats for: ' + _championName + ' at Level 1 and 18'

    basic_table.field_names=["Stat", "Level 1", "Level 18", "per level"]
    basic_table.add_row(['Health', _data['hp'], (_data['hp']+(_data['hpperlevel']*17)), _data['hpperlevel']])
    basic_table.add_row(['Mana/Resource', _data['mp'], (_data['mp']+(_data['mpperlevel']*17)), _data['mpperlevel']])

    #are we dealing with Cassiopeia?
    if _championName != 'Cassiopeia':
        basic_table.add_row(['Move Speed', _data['movespeed'], _data['movespeed'], 'N/A'])
    else: #we are dealing with Cassiopeia
        basic_table.add_row(['Move Speed***', _data['movespeed']+ssv.cass_ms_per_level , (_data['movespeed']+ssv.cass_ms_per_level)+(ssv.cass_ms_per_level*17), ssv.cass_ms_per_level])

    basic_table.add_row(['Armor', normal_round(_data['armor']), (normal_round(_data['armor']+(_data['armorperlevel']*17))), _data['armorperlevel']])
    basic_table.add_row(['Magic Resistance', round(_data['spellblock']), normal_round((_data['spellblock']+(_data['spellblockperlevel']*17))), _data['spellblockperlevel']])

    #are we dealing with Tristana?
    if _championName != 'Tristana':
        basic_table.add_row(['Attack Range', _data['attackrange'], _data['attackrange'], 'N/A'])
    else:
        basic_table.add_row(['Attack Range***', _data['attackrange'], _data['attackrange']+(ssv.tristanna_range_per_level*17), ssv.tristanna_range_per_level])
    
    basic_table.add_row(['HP Regeneration', round(_data['hpregen']), normal_round((_data['hpregen']+(_data['hpregenperlevel']*17))), _data['hpregenperlevel']])
    basic_table.add_row(['Mana/Resource Regeneration', round(_data['mpregen']), normal_round((_data['mpregen']+(_data['mpregenperlevel']*17))), _data['mpregenperlevel']])
    basic_table.add_row(['Critical Strike', _data['crit'], (_data['crit']+(_data['critperlevel']*17)), _data['critperlevel']])
    basic_table.add_row(['Attack Damage', round(_data['attackdamage']), round((_data['attackdamage']+(_data['attackdamageperlevel']*17))), _data['attackdamageperlevel']])
    basic_table.add_row(['Attack Speed', round(_data['attackspeed'],2), round(((round(_data['attackspeed'],2)*((_data['attackspeedperlevel']*17)))/100) + round(_data['attackspeed'],2),2) , _data['attackspeedperlevel']])
    print(basic_table)

#this will work similliarly to Basic_Stats_Output however instead this will output each level for a champion
#also at the same create a dictionary so we can create a pandas dataframe.
def Per_Level_Stats_output(_table_name, _data, _championName):
    _table_name = PrettyTable()
    _table_name.title = 'Stats for: ' + _championName + ' at each level'
    Per_Level_Table_Helper_no_Dec(_table_name, 'Level' , 1, 1)
    #HEALTH
    Per_Level_Table_Helper_no_Dec(_table_name, 'Health', _data['hp'], _data['hpperlevel'])
    create_entry_for_dictionary('Health', _data['hp'], _data['hpperlevel'], NO_DECIMAL_PLACES)

    #MANA   
    Per_Level_Table_Helper_no_Dec(_table_name, 'Mana/Resource', _data['mp'], _data['mpperlevel'])
    create_entry_for_dictionary('Mana/Resource', _data['mp'], _data['mpperlevel'], NO_DECIMAL_PLACES)

    #MOVE SPEED
    #are we dealing with Cassiopeia?
    if _championName != 'Cassiopeia':
        Per_Level_Table_Helper_no_Dec(_table_name, 'Move Speed', _data['movespeed'], 0)
        create_entry_for_dictionary('Move Speed', _data['movespeed'], 0, NO_DECIMAL_PLACES)
    else: #we are dealing with Cassiopeia
        Per_Level_Table_Helper_no_Dec(_table_name, 'Move Speed', _data['movespeed']+ssv.cass_ms_per_level, ssv.cass_ms_per_level)
        create_entry_for_dictionary('Move Speed', _data['movespeed']+ssv.cass_ms_per_level, ssv.cass_ms_per_level, NO_DECIMAL_PLACES)

    #ARMOR
    Per_Level_Table_Helper_no_Dec(_table_name, 'Armor', _data['armor'], _data['armorperlevel'])
    
    #MR
    Per_Level_Table_Helper_no_Dec(_table_name, 'Magic Resistance', _data['spellblock'], _data['spellblockperlevel'])

    #ATTACK RANGE
    #are we dealing with Tristana?
    if _championName != 'Tristana':
        Per_Level_Table_Helper_no_Dec(_table_name, 'Attack Range', _data['attackrange'], 0)
        create_entry_for_dictionary('Attack Range', _data['attackrange'], 0, NO_DECIMAL_PLACES)
    else:
        Per_Level_Table_Helper_no_Dec(_table_name, 'Attack Range', _data['attackrange'], ssv.tristanna_range_per_level)
        create_entry_for_dictionary('Attack Range', ssv.tristanna_range_per_level, 0, NO_DECIMAL_PLACES)

    #HP REGEN
    Per_Level_Table_Helper_no_Dec(_table_name, 'HP Regeneration', _data['hpregen'], _data['hpregenperlevel'])
    create_entry_for_dictionary('HP Regeneration', _data['hpregen'], _data['hpregenperlevel'],NO_DECIMAL_PLACES)

    #CRIT
    Per_Level_Table_Helper_no_Dec(_table_name, 'Critical Strike', _data['crit'], _data['critperlevel'])
    create_entry_for_dictionary( 'Critical Strike', _data['crit'], _data['critperlevel'],NO_DECIMAL_PLACES)

    #ATTACK DAMAGE
    Per_Level_Table_Helper_no_Dec(_table_name, 'Attack Damage', _data['attackdamage'], _data['attackdamageperlevel'])
    create_entry_for_dictionary( 'Attack Damage', _data['attackdamage'], _data['attackdamageperlevel'],NO_DECIMAL_PLACES)

    #ATTACK SPEED
    Per_Level_Table_Helper_2_Dec_Attack_Speed(_table_name, 'Attack Speed', round(_data['attackspeed'],2), _data['attackspeedperlevel'])
    create_entry_for_dictionary( 'Attack Speed', round(_data['attackspeed'],2), _data['attackspeedperlevel'],TWO_DECIMAL_PLACES)
   
    print(_table_name)



def Per_Level_Table_Helper_no_Dec(_table,_statName, _startingValue, _perLevelValue):
    _table.add_column(
        _statName, [ 
        normal_round(_startingValue+(_perLevelValue*0)),   
        normal_round(_startingValue+(_perLevelValue*1)),  
        normal_round(_startingValue+(_perLevelValue*2)),  
        normal_round(_startingValue+(_perLevelValue*3)),   
        normal_round(_startingValue+(_perLevelValue*4)),  
        normal_round(_startingValue+(_perLevelValue*5)),   
        normal_round(_startingValue+(_perLevelValue*6)),   
        normal_round(_startingValue+(_perLevelValue*7)),   
        normal_round(_startingValue+(_perLevelValue*8)),  
        normal_round(_startingValue+(_perLevelValue*9)),  
        normal_round(_startingValue+(_perLevelValue*10)),   
        normal_round(_startingValue+(_perLevelValue*11)),   
        normal_round(_startingValue+(_perLevelValue*12)),   
        normal_round(_startingValue+(_perLevelValue*13)),   
        normal_round(_startingValue+(_perLevelValue*14)),   
        normal_round(_startingValue+(_perLevelValue*15)),   
        normal_round(_startingValue+(_perLevelValue*16)),   
        normal_round(_startingValue+(_perLevelValue*17)),   
    ])    

def Per_Level_Table_Helper_2_Dec_Attack_Speed(_table,_statName, _startingValue, _perLevelValue):
    _table.add_column(
        _statName, [ 
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
    ])  

def create_entry_for_dictionary(_statName, _startingValue, _perLevelValue, rounding_type):
    if rounding_type == 0: # we are rounding to 0 decimal places:
        values = [
            normal_round(_startingValue+(_perLevelValue*0)),   
            normal_round(_startingValue+(_perLevelValue*1)),  
            normal_round(_startingValue+(_perLevelValue*2)),  
            normal_round(_startingValue+(_perLevelValue*3)),   
            normal_round(_startingValue+(_perLevelValue*4)),  
            normal_round(_startingValue+(_perLevelValue*5)),   
            normal_round(_startingValue+(_perLevelValue*6)),   
            normal_round(_startingValue+(_perLevelValue*7)),   
            normal_round(_startingValue+(_perLevelValue*8)),  
            normal_round(_startingValue+(_perLevelValue*9)),  
            normal_round(_startingValue+(_perLevelValue*10)),   
            normal_round(_startingValue+(_perLevelValue*11)),   
            normal_round(_startingValue+(_perLevelValue*12)),   
            normal_round(_startingValue+(_perLevelValue*13)),   
            normal_round(_startingValue+(_perLevelValue*14)),   
            normal_round(_startingValue+(_perLevelValue*15)),   
            normal_round(_startingValue+(_perLevelValue*16)),   
            normal_round(_startingValue+(_perLevelValue*17)),   
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

def Get_Stat_helper(_item_stat_name):
    return  {
    'FlatPhysicalDamageMod' : 'Attack Damage',
    'FlatMagicDamageMod': 'Magic Damage',
    'PercentPhysicalDamageMod' : 'Attack Damage_P',
    'FlatMovementSpeedMod' : 'Move Speed',
    'PercentMovementSpeedMod': 'Move Speed_P',
    'FlatHPPoolMod' : "Health",
    'PercentHPPoolMod' : "Health_P",
    'FlatMPPoolMod' : 'Mana/Resource',
    'PercentMPPoolMod' : 'Mana/Resource_P',
    'FlatArmorMod' : 'Armor',
    'FlatSpellBlockMod' : 'Magic Resistance',
    'FlatCritChanceMod' : 'Critical Strike_P', #even though it says FlatCrit, crit chance is inherentely a percent chance so it will be calculated as such
    'PercentAttackSpeedMod' :'Attack Speed_P'
    #will add cooldown reduction once it is changed to ABILITY HASTE
}.get(_item_stat_name, "ERROR") 

#when items are added to the arguments, we must get each of the items stats and add them to the Per_Level_Table_Output so we can show the differences
def Get_Item_Stat_modifier(items):
    for item in items:
        print(item['name'])
        for stat in item['stats']:          
            print(Get_Stat_helper(stat) + ' +' + str(item['stats'][stat]))
        #print(item['name'])
        #print(item['description'])
        #print(item['gold']['total'])
        print('------------------------------')

#for some champion names that have a space or a special characther, they need to be removed so that champion can be correctly found
def validate_champInput(_champion):
    #check if the champion name has a space in it.
    if  ' ' in _champion:
        _champion  =_champion.replace(' ', '')
    
    if '\'' in _champion:
        x  =  _champion.split("\'", 2)
        _champion  =  x[0]+''+x[1].lower()

    return _champion

#we use this for values we round to the ones because of how python takes care of rounding on x.5.
#using round() is will always round down in these situations however we need to to round up instead
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def check_response_code(_response, _type):
    if response_champ.status_code != 200:
        raise Exception("An Error Occured for:" +_type+ ' Response Code: ' + str(_response.status_code))

#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#



#------------------------------------------------------------ MAIN ------------------------------------------------------------#
champion = validate_champInput(str(sys.argv[1]))
#print(champion)
#print ("Number of arguments: " + str(len(sys.argv)))
items = []


response_champ = requests.get(ks.DDragon_champs+champion+'.json')
response_items = requests.get(ks.DDragon_items)

check_response_code(response_champ, 'CHAMPS')
check_response_code(response_items, 'ITEMS')

championData = response_champ.json()['data']
itemData = response_items.json()['data']
#print(championData[champion]['stats'] )




#print(championData[champion]['spells'])
#create a basic table that shows the champions level 1 stats,  level 18 stats and the per level stat
Basic_Stats_Output(championData[champion]['stats'], champion)
Per_Level_Stats_output("inital_table", championData[champion]['stats'], champion)

for i in itemData:
     if itemData[i]['name'] in sys.argv:
        #print(itemData[i])
        items.append(itemData[i])

Get_Item_Stat_modifier(items)
#print(STAT_DICTIONARY)

df = pd.DataFrame(data=STAT_DICTIONARY)
print(df)
#------------------------------------------------------------ MAIN ------------------------------------------------------------#
