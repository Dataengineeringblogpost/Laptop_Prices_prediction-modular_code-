import pandas as pd



"""
Objective :- 
"""

def del_rows_count(df,col_name): 
    values = df[col_name].value_counts().values
    index = df[col_name].value_counts().index
    for itr in range(len(df[col_name].value_counts().values)):

        if values[itr]<5:
            indexAge = df[ (df[col_name] == index[itr])].index
            df.drop(indexAge, inplace=True)
