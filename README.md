# league_of_legends
This is where all my current running/working on LoL Scripts will be, some examples of currently completed scripts:

1: champion_stats.py, args (Champion Name, "list of items seperated by commas") -> ["Sett", "Black Cleaver", "Trinity Force"]
  This scripts purpose is to compared a champions based stats when adding in an items modifiers to the champions stats. I get the champion and item information from Riot Games' Data Dragon. Once all the necessary information is collected the stats are tabulated for the respective champion and seperate .csv files are created holding the information per level per each item and also the champions bases stats without item modification. One issue I ran into is that for champions that have special scaling tied to their passive (i.e. Tristana Range increase per level and Cassieopia movement speed per level increase) I needed to created special cases for those champion and the scaling values tied to them. 

