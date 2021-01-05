# league_of_legends
This is where all my current running/working on LoL Scripts will be, some examples of the return values from my scripts can be found in the statsheets and pb folders as either csvs or .txt filess (which are complied as json objects):

1: champion_stats.py V1, args (Champion Name, "list of items seperated by commas") -> ["Sett", "Black Cleaver", "Trinity Force"]
  This scripts purpose is to compared a champions based stats when adding in an items modifiers to the champions stats. I get the champion and item information from Riot Games' Data Dragon. Once all the necessary information is collected the stats are tabulated for the respective champion and seperate .csv files are created holding the information per level per each item and also the champions bases stats without item modification. One issue I ran into is that for champions that have special scaling tied to their passive (i.e. Tristana Range increase per level and Cassieopia movement speed per level increase) I needed to created special cases for those champion and the scaling values tied to them. 

2: pick_ban_stats.py V2, args (Country Where tournament is being held, Tournament Name) -> ["Korea, KeSPA Cup 2020] or ["China, Demacia Cup 2020]
  This scripts will return a JSON object that holds the picks and bans statistics for an entire tournament. The stats are broken down per champion with each champion broken down into each possible position in a pick and ban scenario (i.e. Blue Ban 1, Red Pick 5, etc...). Versiona 2 still has the champion breakdowns, but not it also includes breakdowns for the individual teams at the tournament as well as if there are any matches that create exceptions, the user will be notified that those matches where skipped and also the leaguepedia index for the match.

3: player_pick_ban_stats.py V1, args  (Country Where tournament is being held, Tournament Name) -> ["Korea, KeSPA Cup 2020] or ["China, Demacia Cup 2020]
  This script works similiarly to pick_ban_stats.py however instead of gathering champions and team pick ban information, it gathers then players pick stats which includes total picks per game and total wins per champ also. There is also the exception checker that makes sure that if the game for some reason does not have any pick ban data on leaguepedia is will added to the exceptions list with a vod of the match and the leaguepedia match index.
  
  
  
