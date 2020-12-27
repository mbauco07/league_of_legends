

def Check_Tournaments(tournamets):
    if len(tournaments) <= 0:
        sys.exit('ERROR: The inputted parameters returned no tournaments, Check the spelling!!!!')
 


 
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

URL = tournament_games[0]['sources']['leaguepedia']['matchHistoryUrl']
page = requests.get(URL)
html_soup = bs(page.text, 'html.parser')
#get the div that hold the player informations
team_containers = html_soup.find_all('div', class_ = 'section-wrapper-content-wrapper')
print(type(team_containers))
print(len(team_containers))