import pandas as pd
import numpy as np
import keras
from keras.models import Model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report
import matplotlib.pyplot as plt


class FBM():
    def __init__(self, features, output):
        self.model = None
        self.features = features
        self.model = self.create_model()
        checkpoint = ModelCheckpoint(output, monitor='val_accuracy', verbose=1,save_best_only=True,mode='max',period=2) 
        self.callbacks_list = [checkpoint]

    def create_model(self):
        input = Input(shape=(self.features,))
        x = Dense(20, activation='relu')(input)
        x = Dense(10, activation='relu')(x)
        out = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=[input], outputs=[out])
        model.summary()
        model.compile(optimizer='RMSprop',
                      loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def predict(self, x, file):
        self.model.load_weights(file)
        return self.model.predict(x)

    def train(self, x, y):
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=33)
        history = self.model.fit(x_train, y_train, batch_size=100, epochs=100, validation_data=(x_test, y_test), callbacks=self.callbacks_list)
        y_pred = self.model.predict(x_test)
        print(classification_report(y_test, y_pred.round()))
        history_dict = history.history
        loss_values = history_dict['loss']
        val_loss_values = history_dict['val_loss']
        epochs = range(1, len(loss_values)+1)
        plt.plot(epochs, loss_values, 'bo', label='Training loss')
        plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
