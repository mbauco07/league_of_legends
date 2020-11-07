#This script will ask for a champ or champs and will get their stats, stats per level, etc and then compare build with items included.
import keys
import requests
import sys
from prettytable import PrettyTable

#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#
def output_basic_stats(_data, _championName):   
    x = PrettyTable()
    x.field_names=["Stat", "Level 1", "Level 18", "per level"]
    x.add_row(['Health', _data['hp'], (_data['hp']+(_data['hpperlevel']*17)), _data['hpperlevel']])
    x.add_row(['Mana/Resource', _data['mp'], (_data['mp']+(_data['mpperlevel']*17)), _data['mpperlevel']])
    x.add_row(['Move Speed', _data['movespeed'], _data['movespeed'], 'N/A'])
    x.add_row(['Armor', _data['armor'], (_data['armor']+(_data['armorperlevel']*17)), _data['armorperlevel']])
    x.add_row(['Magic Resistance', _data['spellblock'], (_data['spellblock']+(_data['spellblockperlevel']*17)), _data['spellblockperlevel']])
    x.add_row(['Attack Range', _data['attackrange'], _data['attackrange'], 'N/A'])
    x.add_row(['HP Regeneration', _data['hpregen'], (_data['hpregen']+(_data['hpregenperlevel']*17)), _data['hpregenperlevel']])
    x.add_row(['Resource Regeneration', _data['mpregen'], (_data['mpregen']+(_data['mpregenperlevel']*17)), _data['mpregenperlevel']])
    x.add_row(['Critical Strike', _data['crit'], (_data['crit']+(_data['critperlevel']*17)), _data['critperlevel']])
    x.add_row(['Attack Damage', _data['attackdamage'], (_data['attackdamage']+(_data['attackdamageperlevel']*17)), _data['attackdamageperlevel']])
    x.add_row(['Attack Speed', _data['attackspeed'], (_data['attackspeed']+(_data['attackspeedperlevel']*17)), _data['attackspeedperlevel']])
    print(x)

#------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------#



#------------------------------------------------------------ MAIN ------------------------------------------------------------#
champion = str(sys.argv[1])
#print(champion)

response = requests.get(keys.DDragon+champion+'.json')

#do we have a good request?
if response.status_code == 200:
    print('Success!')
#if we do not get a 200 code, raise an error and stop the program
else:
    raise Exception("An Error Occured: "+ champion + " was not found")


championData = response.json()['data']
championData_stats = response.json()['data'][champion]['stats']

print(championData_stats)
    
#create a basic table that shows the champions level 1 stats,  level 18 stats and the per level stat
output_basic_stats(championData_stats, champion)
#------------------------------------------------------------ MAIN ------------------------------------------------------------#
