import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

def comparator(stringsin):
    # read in MajesticMillion and NoTracking lists as sets
    with open('majmill_list.txt', 'r') as f:
        majmill = set(f.read().splitlines())
    with open('notrack_list.txt', 'r') as f:
        notrack = set(f.read().splitlines())

    for string in stringsin:
        majmill = 1 if string in majmill else 0
        notrack = 1 if string in notrack else 0
        sql.setComparator(string, majmill, notrack)
    # create output table as a DataFrame
    # outtable = pd.DataFrame({'Address': stringsin,
    #                          'MajesticMillion': [1 if s in majmill else 0 for s in stringsin],
    #                          'NoTracking': [1 if s in notrack else 0 for s in stringsin]})

    # print output table
    # print(outtable)
    # return outtable
    return 0
    
stringsin = sys.argv[1:]
comparator(*stringsin)


