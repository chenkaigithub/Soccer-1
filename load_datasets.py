'''
Created on Nov 28, 2017

@author: drews
'''

import datadotworld as dw

dataset = dw.load_dataset('data-society/european-soccer-data')

matches = dataset.dataframes['match']

# drop unneeded columns
# keep players, xy coords of players, date, id, goals, home/away team ids
matches = matches.drop(matches.columns[[range(77,115)]],1)
matches = matches.drop(matches.columns[[range(0,5)]],1)
matches = matches.dropna(0,'any')

matches.to_csv('matches.csv',index=False)
print('wrote matches.csv')

teams =  dataset.dataframes['team_attributes']
teams = teams.drop(teams.columns[[0,1,6]],1)

# change string values to integer values
teams['buildupplayspeedclass'] = teams['buildupplayspeedclass'].replace(['Fast','Balanced','Slow'],[3,2,1])
teams['buildupplaydribblingclass'] = teams['buildupplaydribblingclass'].replace(['Lots','Normal','Little'],[3,2,1])
teams['buildupplaypassingclass'] = teams['buildupplaypassingclass'].replace(['Long','Mixed','Short'],[3,2,1])
teams['buildupplaypositioningclass'] = teams['buildupplaypositioningclass'].replace(['Free Form','Organised'],[-1,1])
teams['chancecreationpassingclass'] = teams['chancecreationpassingclass'].replace(['Risky','Normal','Safe'],[3,2,1])
teams['chancecreationcrossingclass'] = teams['chancecreationcrossingclass'].replace(['Lots','Normal','Little'],[3,2,1])
teams['chancecreationshootingclass'] = teams['chancecreationshootingclass'].replace(['Lots','Normal','Little'],[3,2,1])
teams['chancecreationpositioningclass'] = teams['chancecreationpositioningclass'].replace(['Free Form','Organised'],[-1,1])
teams['defencepressureclass'] = teams['defencepressureclass'].replace(['High','Medium','Deep'],[3,2,1])
teams['defenceaggressionclass'] = teams['defenceaggressionclass'].replace(['Press','Double','Contain'],[3,2,1])
teams['defenceteamwidthclass'] = teams['defenceteamwidthclass'].replace(['Wide','Normal','Narrow'],[3,2,1])
teams['defencedefenderlineclass'] = teams['defencedefenderlineclass'].replace(['Offside Trap','Cover'],[-1,1])

teams.to_csv('teams.csv',index=False)
print('wrote teams.csv')

players = dataset.dataframes['player_attributes']

players = players.drop(players.columns[[0,1,7,8]],1)
players = players.dropna(0,'any')

# change string values to integer values
players['preferred_foot'] = players['preferred_foot'].replace(['right','left'],[1,-1])

player_stats =  dataset.dataframes['player']

player_stats = player_stats.drop(['id','player_fifa_api_id','birthday'],1)
player_stats = player_stats.dropna(0,'any')

players = players.merge(player_stats,left_on='player_api_id',right_on='player_api_id')

players.to_csv('players.csv',index=False)
print('wrote players.csv')

player_names = player_stats.drop(['height','weight'],1)

player_names.to_csv('player_names.csv',index=False)
print('wrote player_names.csv')
