import sys
import leaguepedia_parser as lp


def Check_Tournaments(_tournaments):
    if len(_tournaments ) <= 0:
        sys.exit('ERROR: The inputted parameters returned no tournaments, Check the spelling!!!!')
 
def Get_Tournament_Games(_tournaments, _tournament_name):
    games = []
    for i in _tournaments:
        if i['name'] == _tournament_name:
            games = lp.get_games(i['overviewPage'])
    return games