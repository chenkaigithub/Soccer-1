'''
Created on Dec 20, 2017

@author: drews
'''

'''
need:
foot,height,weight
'''

from loading.Team import Team
import tensorflow as tf
import pandas as pd
import numpy as np

matches = pd.read_csv('datasets/p_train_inputs.csv').as_matrix()
goals = pd.read_csv('datasets/p_train_outputs.csv').as_matrix()

def get_prob(input,home_name='home',away_name='away'):
    loaded_graph = tf.Graph()
     
    with tf.Session(graph=loaded_graph) as sess:    
        latest_ckpt = tf.train.latest_checkpoint('./models')
#         latest_ckpt = "./models/model_10-run-3.ckpt"
         
        #First let's load meta graph and restore weights
        saver = tf.train.import_meta_graph(latest_ckpt + '.meta')
        saver.restore(sess,latest_ckpt)
         
        x = loaded_graph.get_tensor_by_name("x:0")
         
        results = loaded_graph.get_tensor_by_name("y_clipped:0")
#         for i in range(10):
        x_in = input.reshape(1,880)
        pred = sess.run(tf.argmax(results,1), feed_dict={x: x_in})
        
        res = sess.run(results, feed_dict={x: x_in})[0]
        print("predict {} win: {:.3f}%".format(home_name,100*float(res[0])))
        print("predict {} win: {:.3f}%".format(away_name,100*float(res[1])))
        print("predict draw win: {:.3f}%".format(100*float(res[2])))
#         print(goals[i])
#         print(sess.run(tf.argmax(goals[i],0)))
        print()
        
pos = {"RCB": [4,3],"LCB": [6,3],"RB": [2,3],"LB": [8,3],"CB": [5,3],
           "RDCM": [4,6],"LDCM": [6,6],"LDM": [8,6],"RDM": [2,6],"CDM": [5,6],
           "RCM": [4,8],"LCM": [6,8],"LM": [8,6],"RM": [2,6],"GOL": [1,1],
           "RACM": [4,10],"LACM": [6,10],"LAM": [7,8],"RAM": [3,8],"CAM":[5,8],
           "CST": [5,11],"LST": [6,11],"RST": [4,11],"RW": [2,11],"LW": [8,11]}
#     p_ids = [182917, 696365, 41468, 299215]
manU_names = ["Anthony Martial",
              "Jesse Lingard","Juan Mata","Paul Pogba",
         "Nemanja Matic","Ander Herrera","Luke Shaw","Phil Jones",
         "Marcos Rojo","Victor Nilsson Lindeloef","David De Gea"]

manU_form = [pos["CST"],pos["LAM"],pos["RAM"],pos["CAM"],pos["LDM"],pos["RDM"],
             pos["LB"],pos["RCB"],pos["LCB"],pos["RB"],[1,1]]

manU = Team("Manchester United",manU_names,manU_form)

Les_names = ["Kasper Schmeichel","Wes Morgan","Danny Simpson","Andy King",
             "Christian Fuchs","Daniel Amartey","Vicente Iborra","Riyad Mahrez",
             "Demarai Gray","Marc Albrighton","Jamie Vardy"]

les_form = [[1,1],pos["LCB"],pos["LB"],pos["RCB"],pos["RB"],[7,6],[3,6],
            pos["LAM"],pos["CAM"],pos["RAM"],pos["CST"]]

lesC = Team("Leicester City",Les_names,les_form)

south_names = ["Shane Long","Sofiane Boufal","Nathan Redmond","Mario Lemina",
               "Oriol Romeu","Pierre-Emil Hoejbjerg","Matt Targett","Wesley Hoedt",
               "Maya Yoshida","Virgil van Dijk","Fraser Forster"]

south_form = [pos["CST"],pos["LAM"],pos["RAM"],pos["LDM"],pos["CDM"],pos["RDM"],
              pos["LB"],pos["LCB"],pos["RCB"],pos["RB"],pos["GOL"]]

south = Team("Southampton",south_names,south_form)

eve_names = ["Baye Oumar Niasse","Nikola Vlasic","Wayne Rooney","Yannick Bolasie",
             "Tom Davies","Morgan Schneiderlin","Mason Holgate","Michael Keane",
             "Ashley Williams","Cuco Martina","Jordan Pickford"]

eve_form = [pos["CST"],pos["LAM"],pos["CAM"],pos["RAM"],pos["LDM"],pos["RDM"],
             pos["LB"],pos["RCB"],pos["LCB"],pos["RB"],[1,1]]

eve = Team("Everton",eve_names,eve_form)
row = np.array([])
row = np.append(row,manU.get_form())
row = np.append(row,eve.get_form())
row = np.append(row,manU.get_players())
row = np.append(row,eve.get_players())

get_prob(row,manU.name,eve.name)