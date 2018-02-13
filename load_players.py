'''
Created on Nov 28, 2017

@author: drews
'''

# import datadotworld as dw
import pandas as pd
import datetime as dt
import os

# if pathlib.Path('match_teams.csv').is_file():
#     match_teams = pd.read_csv('match_teams.csv')
# else: 
match_teams = pd.read_csv('datasets\match_players-7.csv')

# dataset = dw.load_dataset('data-society/european-soccer-data')
# player_cols = dataset.dataframes['player_attributes'].columns

# player_cols = player_cols.delete(5)
# player_cols = player_cols.delete(5)

def compare_dates(dt1,dt2):
    d1 = dt.datetime.strptime(dt1[:10],'%Y-%m-%d')
    d2 = dt.datetime.strptime(dt2[:10],'%Y-%m-%d')
    return(abs((d2 - d1).days))

h_players = pd.read_csv('players.csv').drop('player_name',1)
a_players = pd.read_csv('players.csv').drop('player_name',1)
player_cols = a_players.columns
player_cols.insert(len(player_cols),'height')
player_cols.insert(len(player_cols),'weight')

for player_num in range(1,12):
    print('')
    print('player: ' + str(player_num))
    print(match_teams.shape)
    cols = match_teams.columns.tolist()
    
    
    a_cols = ['away_' + s + '_' + str(player_num) for s in player_cols]
    h_cols = ['home_' + s + '_' + str(player_num) for s in player_cols]

    f1 = len(match_teams.columns)
    f2 = len(match_teams.columns) + len(player_cols)
    
    h_players.columns = h_cols
    a_players.columns = a_cols
    h_player_matches = pd.DataFrame(columns = h_cols)
    a_player_matches = pd.DataFrame(columns = a_cols)

    h_player_matches['home_match_api_id'] = pd.Series() # create new column
    a_player_matches['away_match_api_id'] = pd.Series()

    i = 0
    start = dt.datetime.now()
    avg = 0
    length = len(match_teams)
    for index,row in match_teams.iterrows():
        i += 1
        foundH = False
        foundA = False
        diff = float('inf')
        if i % 500 == 0:
            print('match: ' + str(i))
            if i % 3000 == 0:
                end = dt.datetime.now()
                # rate of matches per time taken 
                rate = (i-1) / (end-start).total_seconds()
                est_time_left = ((length - i + 1) / rate) + 40*(player_num - 1)
                print('Estimated time left for player ' + str(player_num) + ':')
                print('secs: ' + str(est_time_left))
        for tmp,t in h_players.loc[h_players['home_player_api_id_' + str(player_num)] == row[49 + player_num]].iterrows():
            d = compare_dates(t[1], row[0])
            if d < diff:
                diff = d
                h_p = t
                foundH = True
                
        diff = float('inf')
        for tmp,t in a_players.loc[a_players['away_player_api_id_' + str(player_num)] == row[60 + player_num]].iterrows():
            d = compare_dates(t[1], row[0])
            if d < diff:
                diff = d
                a_p = t
                foundA = True
        
        if not (foundH and foundA):
            continue
        
        h_p['home_match_api_id'] = row[1]
        a_p['away_match_api_id'] = row[1]

        h_player_matches.loc[len(h_player_matches)] = h_p
        a_player_matches.loc[len(a_player_matches)] = a_p

    h_player_matches = h_player_matches.drop('home_player_api_id_' + str(player_num),1)
    a_player_matches = a_player_matches.drop('away_player_api_id_' + str(player_num),1)
    h_player_matches = h_player_matches.drop('home_date_' + str(player_num),1)
    a_player_matches = a_player_matches.drop('away_date_' + str(player_num),1)
    
    match_teams = match_teams.merge(h_player_matches,left_on='match_api_id',right_on='home_match_api_id')
    match_teams = match_teams.merge(a_player_matches,left_on='match_api_id',right_on='away_match_api_id')
    match_teams = match_teams.drop('home_match_api_id',1)
    match_teams = match_teams.drop('away_match_api_id',1)
    directory = 'datasets'
    file = os.path.join('datasets','match_players-' + str(player_num) + '.csv')
    if not os.path.exists(directory):
        os.makedirs(directory)
    match_teams.to_csv(file,index=False)
    print('wrote to ' + file)
    print(match_teams.shape)
    print('')