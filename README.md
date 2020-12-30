# league_of_legends
This is where all my current running/working on LoL Scripts will be, some examples of currently completed scripts:

1: champion_stats.py V1, args (Champion Name, "list of items seperated by commas") -> ["Sett", "Black Cleaver", "Trinity Force"]
  This scripts purpose is to compared a champions based stats when adding in an items modifiers to the champions stats. I get the champion and item information from Riot Games' Data Dragon. Once all the necessary information is collected the stats are tabulated for the respective champion and seperate .csv files are created holding the information per level per each item and also the champions bases stats without item modification. One issue I ran into is that for champions that have special scaling tied to their passive (i.e. Tristana Range increase per level and Cassieopia movement speed per level increase) I needed to created special cases for those champion and the scaling values tied to them. 

2: pick_ban_stats.py V1, args (Country Where tournament is being held, Tournament Name) -> ["Korea, KeSPA Cup 2020]
  This scripts will return a JSON object that holds the picks and bans statistics for an entire tournament. The stats are broken down per champion with each champion broken down into each possible position in a pick and ban scenario (i.e. Blue Ban 1, Red Pick 5, etc...). An example out for a champion breakdown is:
    {"Aatrox":
      {"ChampionName": "Aatrox", 
        "Picks": 12,
        "Bans": 9, 
          "Details": 
          {"Blue Ban 1": 3,
          "Red Ban 1": 2,
          "Blue Ban 2": 1,
          "Red Ban 2": 0,
          "Blue Ban 3": 0,
          "Red Ban 3": 0,
          "Blue Pick 1": 3, 
          "Red Pick 1": 0,
          "Red Pick 2": 1, 
          "Blue Pick 2": 0,
          "Blue Pick 3": 2, 
          "Red Ban 4": 1,
          "Blue Ban 4": 0, 
          "Red Ban 5": 1, "Blue Ban 5": 1, 
          "Red Pick 4": 1, 
          "Blue Pick 4": 1, 
          "Blue Pick 5": 3, 
          "Red Pick 5": 1
         }
       }
