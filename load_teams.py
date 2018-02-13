'''
Created on Nov 28, 2017

@author: drews
'''
'''
The following are counts of 
21233
267
20966
473
20493
394
20099
263
19836
203
19633
126
19507
240
19267
126
19141
105
19036
'''
import pandas as pd
import datetime as dt
from bokeh.layouts import row


matches = pd.read_csv('matches.csv')

h_teams = pd.read_csv('teams.csv')
a_teams = pd.read_csv('teams.csv')

cols = matches.columns.tolist()
for i in range(0,len(h_teams.columns)):
    cols.insert(i+len(matches.columns),'home_'+h_teams.columns[i])
    cols.insert(i+len(matches.columns) + 22,'away_'+h_teams.columns[i])

def compare_dates(dt1,dt2):
    d1 = dt.datetime.strptime(dt1[:10],'%Y-%m-%d')
    d2 = dt.datetime.strptime(dt2[:10],'%Y-%m-%d')
    return(abs((d2 - d1).days))

match_teams = pd.DataFrame(columns=cols)
h_teams.columns = cols[72:94]
a_teams.columns = cols[94:]
h_team_matches = pd.DataFrame(columns = cols[72:94])
a_team_matches = pd.DataFrame(columns = cols[94:])
h_team_matches['home_match_api_id'] = pd.Series()
a_team_matches['away_match_api_id'] = pd.Series()
i = len(match_teams)
for index,row in matches.iterrows():
    i = i + 1
    foundH = False
    foundA = False
    diff = float('inf')
    if i % 500 == 0:
        print('match: ' + str(i))
    for tmp,t in h_teams.loc[h_teams['home_team_api_id'] == row[2]].iterrows():
        d = compare_dates(t[1], row[0])
        if d < diff:
            diff = d
            h_t = t
            foundH = True
      
    diff = float('inf')
    for tmp,t in a_teams.loc[a_teams['away_team_api_id'] == row[3]].iterrows():
        d = compare_dates(t[1], row[0])
        if d < diff:
            diff = d
            a_t = t
            foundA = True
    if not foundH or not foundA:
        continue
    h_t['home_match_api_id'] = row[1]
    a_t['away_match_api_id'] = row[1]
    h_team_matches.loc[len(h_team_matches)] = h_t
    a_team_matches.loc[len(a_team_matches)] = a_t

h_team_matches = h_team_matches.drop('home_team_api_id',1)
a_team_matches = a_team_matches.drop('away_team_api_id',1)
h_team_matches = h_team_matches.drop('home_date',1)
a_team_matches = a_team_matches.drop('away_date',1)

match_teams = matches.merge(h_team_matches,left_on='match_api_id',right_on='home_match_api_id')
match_teams = match_teams.merge(a_team_matches,left_on='match_api_id',right_on='away_match_api_id')
match_teams = match_teams.drop('home_match_api_id',1)
match_teams = match_teams.drop('away_match_api_id',1)

# Writing to csv
match_teams.to_csv('match_teams.csv',index=False)
print('wrote to csv')
print(match_teams.shape)
