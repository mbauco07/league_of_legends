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