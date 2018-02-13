'''
Created on Dec 15, 2017

@author: drews
'''
# "OneDrive\Documents\Hobart 17-18\workspace\soccer\src\loading"

import tensorflow as tf
import pandas as pd
import numpy as np

train_x = pd.read_csv('datasets/p_train_inputs.csv').as_matrix()
train_y = pd.read_csv('datasets/p_train_outputs.csv').as_matrix()

val_x = pd.read_csv('datasets/p_test_inputs.csv').as_matrix()
val_y = pd.read_csv('datasets/p_test_outputs.csv').as_matrix()

def next_batch(batch_size,indices):

    batch_x = []
    batch_y = []
    for i in range(batch_size):
        index = np.random.choice(len(train_x))
        while index in indices:
            index = np.random.choice(len(train_x))
        indices.append(index)
        batch_x.append(train_x[index])
        batch_y.append(train_y[index])
    return(batch_x,batch_y,indices)

# hidden = {600,585,550,450,350,300}

x = tf.placeholder(tf.float32, shape=[None, 880], name='x')
y = tf.placeholder(tf.float32, shape=[None, 3], name='y')

batch_size = 50
alpha = .5
epochs_list = [8,9,10]
node_list = [[880,576,384,256,170,60,20,3],
             [880,576,432,324,288,192,64,3],
             [880,576,384,576,384,170,60,3]]
rates = [.01,.02,.05,.1,.15,.2,.25,.5]
rate = .2
best = 0
a = 0
nodes = node_list[2]
num_epoch = 7
# nodes= n
best_list = pd.DataFrame(columns=['accuracy','nodes','run'])
# filename = 'best_list_epochs.csv'
num_trials = 10
count = 0
# for nodes in node_list:
# for rate in rates:
#     count += 1
for opt in range(4,7):
    avg_acc = 0
    print("Using optimizer {}".format(opt))
    for run in range(num_trials):
        print()
        print("trial {} for optimizer {}".format(run + 1,opt))
        W = {}
        b = {}
        for i in range(1,len(nodes)):
            W[i-1] = tf.Variable(tf.random_normal([nodes[i-1], nodes[i]], stddev=0.03),name='W'+str(i))
            b[i-1] = tf.Variable(tf.random_normal([nodes[i]], stddev=0.01),name='b'+str(i))
            
        in_layer = x
        for i in range(len(nodes)-2):
            layer = tf.add(tf.matmul(in_layer, W[i]), b[i])
            layer = tf.nn.leaky_relu(layer,float(alpha))
            in_layer = layer
         
        # now calculate the hidden layer output - in this case, let's use a softmax activated
        # output layer
        y_ = tf.add(tf.matmul(in_layer, W[len(nodes)-2]), b[len(nodes)-2])
         
        y_clipped = tf.clip_by_value(y_, 1e-10, 0.9999999,name="y_clipped")
         
    #     cross_entropy = -tf.reduce_mean(tf.reduce_sum(y * tf.log(y_clipped) + (1 - y) * tf.log(1 - y_clipped), axis=1))
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_clipped,labels=y))
         
        # add an optimiser
        if opt == 0:
            optimiser = tf.train.GradientDescentOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 1:
            optimiser = tf.train.AdamOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 2:
            optimiser = tf.train.AdadeltaOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 3:
            optimiser = tf.train.AdagradOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 4:
            optimiser = tf.train.AdagradDAOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 5:
            optimiser = tf.train.MomentumOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 6:
            optimiser = tf.train.ProximalAdagradOptimizer(learning_rate=rate).minimize(cross_entropy)
        elif opt == 7:
            optimiser = tf.train.ProximalGradientDescentOptimizer(learning_rate=rate).minimize(cross_entropy)
                    
        saver = tf.train.Saver(max_to_keep=9)
         
        # finally setup the initialisation operator
        init_op = tf.global_variables_initializer()
         
    #     saver = tf.train.Saver()
         
        # start the session
        with tf.Session() as sess:
            # define an accuracy assessment operation
            correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
             
            # initialise the variables
            sess.run(init_op)
            total_batch = int(len(train_y) / batch_size)
            for epoch in range(num_epoch):
                avg_cost = 0
                indexes = []
                for i in range(total_batch):
                    batch_x, batch_y,indexes = next_batch(batch_size,indexes)
                    _, c = sess.run([optimiser, cross_entropy], 
                                 feed_dict={x: batch_x, y: batch_y})
                    avg_cost += c / total_batch
                print("Epoch:", (epoch + 1), "cost =", "{:.3f}".format(avg_cost))
            trial = sess.run(accuracy, feed_dict={x: val_x, y: val_y})
            print(trial)
            avg_acc += float(trial) / num_trials
            if run + 1 == num_trials:
                save_file = "./models/model_optimizer-{}.ckpt".format(opt)
                print("saved file at '{}'".format(save_file))
                saver.save(sess, save_file)
    # best_list.loc[len(best_list)] = [avg_acc,num_epoch,'avg']
    print("avg for optimizer {}: {}".format(opt,avg_acc))
# best_list.to_csv(filename,index=False)