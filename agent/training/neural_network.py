import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential, Input
from keras.layers import Dense, Normalization
from keras.optimizers import SGD

othello_games = pd.read_csv('agent/training/training_data.csv', delimiter=";")

attributes = othello_games.drop(labels='current_player_won', axis=1)
target = othello_games['current_player_won']

(training_attributes, test_attributes,
training_target, test_target) = train_test_split(
    attributes, target,
    test_size = .2
)

normalizator = Normalization()
normalizator.adapt(training_attributes.to_numpy())

test_othello_net = Sequential()
test_othello_net.add(Input(shape=(64,)))
test_othello_net.add(normalizator)
test_othello_net.add(Dense(16, activation='sigmoid'))
test_othello_net.add(Dense(1))

test_othello_net.compile(optimizer=SGD(learning_rate=0.01), loss='mean_squared_error')
test_othello_net.fit(training_attributes, training_target, batch_size=100, epochs=50)

test_othello_net.evaluate(test_attributes, test_target)



def check_dataset_status(dataset):
    dataset.isna().any()