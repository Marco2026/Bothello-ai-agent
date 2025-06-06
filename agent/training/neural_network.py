import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential, Input
from keras.layers import Dense, Normalization
from keras.optimizers import SGD

class OthelloNet:

    def __init__(self):
        (self.training_attributes, 
         self.test_attributes, 
         self.training_target, 
         self.test_target) = self.prepare_data()
        self.model = self.build_model()        

    def prepare_data(self):
        othello_games = pd.read_csv('agent/training/training_data.csv', delimiter=";")

        attributes = othello_games.drop(labels='current_player_won', axis=1)
        target = othello_games['current_player_won']

        (training_attributes, test_attributes,
        training_target, test_target) = train_test_split(
            attributes, target,
            test_size = .2
        )

        return (training_attributes, test_attributes, training_target, test_target)

    def build_model(self):
        normalizator = Normalization()
        normalizator.adapt(self.training_attributes.to_numpy())

        model = Sequential()
        model.add(Input(shape=(64,)))
        model.add(normalizator)
        model.add(Dense(16, activation='tanh'))
        model.add(Dense(5))

        model.compile(optimizer=SGD(learning_rate=0.01), loss='mean_squared_error')
        return model

    def train_model(self):
        history = self.model.fit(self.training_attributes, self.training_target, batch_size=256, epochs=100)
        return history.history

    def evaluate_model(self):
        resultado = self.model.evaluate(self.test_attributes, self.test_target)
        return resultado
    
    def predict(self, state):
        if isinstance(state, pd.DataFrame):
            state_np = state.to_numpy()
        else:
            state_np = state

        prediction = self.model.predict(state_np)
        return prediction

    def check_dataset_status(dataset):
        dataset.isna().any()