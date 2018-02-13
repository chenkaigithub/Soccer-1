'''
Created on Dec 23, 2017

@author: drews
'''
import pandas as pd
import datetime as dt
import numpy as np

class Team:
    '''
    classdocs
    '''

    def __init__(self, name, players, formation):
        '''
        Constructor
        '''
        
        self.name = name
        df = pd.read_csv('datasets/players.csv')
        self.players = []
        for name in players:
            diff = float('inf')
            found = False
            for _,row in df.loc[df["player_name"] == name].iterrows():
                found = True
                d = compare_dates(str(dt.datetime.today()), row[1])
                if d < diff:
                    diff = d
                    self.players.insert(len(self.players), row)
            if not found:
                print("No stats for {}".format(name))
        self.players = np.array(self.players)
        self.formation = np.array(formation)
        print("There are {} players in {}".format(len(self.players),self.name))
        
    def get_form(self):
        return(self.formation.flatten())
    
    def get_players(self):
#         print(np.delete(self.players,[0,1,38]))
        cols = [[41*i,41*i + 1, 41*i + 38] for i in range(22)]
        return(np.delete(self.players,cols))
        
        
def compare_dates(dt1,dt2):
    d1 = dt.datetime.strptime(dt1[:10],'%Y-%m-%d')
    d2 = dt.datetime.strptime(dt2[:10],'%Y-%m-%d')
    return(abs((d2 - d1).days))

def main():
    pos = {"RCB": [4,3],"LCB": [6,3],"RB": [2,3],"LB": [8,3],"CB": [5,3],
           "RDCM": [4,6],"LDCM": [6,6],"LDM": [8,6],"RDM": [2,6],
           "RCM": [4,8],"LCM": [6,8],"LM": [8,6],"RM": [2,6],
           "RACM": [4,10],"LACM": [6,10],"LAM": [7,8],"RAM": [3,8],"CAM":[5,8],
           "CST": [5,11],"LST": [6,11],"RST": [4,11],"RW": [2,11],"LW": [8,11]}
#     p_ids = [182917, 696365, 41468, 299215]
    manU_names = ["Romelu Lukaku","Jesse Lingard",
             "Juan Mata","Anthony Martial","Paul Pogba",
             "Nemanja Matic","Ashley Young","Phil Jones",
             "Chris Smalling","Marcos Rojo","David De Gea"]
    
    manU_form = [pos["CST"],pos["CAM"],pos["RAM"],pos["LAM"],[7,6],[3,7],
                 pos["LB"],pos["LCB"],pos["RCB"],pos["RB"],[1,1]]
    
    manU = Team("Manchester United",manU_names,manU_form)
    
    Les_names = ["Kasper Schmeichel","Wes Morgan","Danny Simpson","Andy King",
                 "Christian Fuchs","Daniel Amartey","Vicente Iborra","Riyad Mahrez",
                 "Demarai Gray","Marc Albrighton","Jamie Vardy"]
    
    les_form = [[1,1],pos["LCB"],pos["LB"],pos["RCB"],pos["RB"],[7,6],[3,6],
                pos["LAM"],pos["CAM"],pos["RAM"],pos["CST"]]
    
    lesC = Team("Leicester City",Les_names,les_form)
    
    row = np.array(lesC.get_form())
    row = np.append(row,manU.get_form())
    row = np.append(row,lesC.get_players())
    row = np.append(row,manU.get_players())
    
#     print(row)
#     length = len(lesC.get_form())
#     length += len(manU.get_form())
#     length += len(lesC.get_players())
#     length += len(manU.get_players())
#     length -= 3*22
    print(manU.get_players())
    
if __name__ == '__main__':
    main()