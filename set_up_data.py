'''
Created on Dec 1, 2017

@author: drews
'''
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# df = pd.read_csv('match_team_players.csv')
df = pd.read_csv('datasets\match_players-11.csv')

# drop matches and players id
df = df.drop(['date','match_api_id','home_team_api_id','away_team_api_id'],1)

cols = []
for i in range(1,12):
    cols.append('home_player_' + str(i))
    cols.append('away_player_' + str(i))
# 
df = df.drop(cols,1)

# don't use team attributes

# make goals as the labels
d = {'home_team_goal': df['home_team_goal'],'away_team_goal':df['away_team_goal']}
outputs = pd.DataFrame(data=d)
inputs = df.drop(['home_team_goal','away_team_goal'],1)

scaler = MinMaxScaler(feature_range=(-5,5))
scaler.fit(inputs)

train_x = scaler.transform(inputs)

train_outputs = []
for index,row in outputs.iterrows():
    if row[0] > row[1]:
        train_outputs.append([1,0,0])
    elif row[1] > row[0]:
        train_outputs.append([0,1,0])
    else:
        train_outputs.append([0,0,1])

split_size = int(len(train_outputs)*0.8)
print("split size: {}".format(split_size))

train_x, val_x = pd.DataFrame(inputs[:split_size]), pd.DataFrame(inputs[split_size:])
train_y, val_y = pd.DataFrame(train_outputs[:split_size]), pd.DataFrame(train_outputs[split_size:])

# write to csv
train_x.to_csv('p_train_inputs.csv',index=False)
train_y.to_csv('p_train_outputs.csv',index=False)
print("Wrote trains to csv")

val_x.to_csv('p_test_inputs.csv',index=False)
val_y.to_csv('p_test_outputs.csv',index=False)
print("Wrote tests to csv")
