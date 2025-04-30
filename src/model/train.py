import requests, zipfile, io, os, pickle
import numpy as np
import tensorflow as tf
import keras
from keras import layers, models, callbacks
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from dataset.load_custom_dataset import *

EPOCHS = 500
HISTORY_PATH = os.path.join("results")

# Making model folder
if not os.path.isdir("models"):
    print("Making save data folder")
    os.mkdir("models")

callback = callbacks.ModelCheckpoint(
    filepath=os.path.join("models", "350kb.keras"),
    monitor="val_loss",
    mode="min",
    save_best_only=True,
    verbose=1
)

# Making the model
model = models.Sequential([
    layers.Input((x_train.shape[1], x_train.shape[2])),
    layers.Conv1D(32, kernel_size=3),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling1D(),

    layers.Conv1D(64, kernel_size=3),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling1D(),

    layers.Conv1D(128, kernel_size=3),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling1D(),

    layers.Flatten(),

    layers.Dense(32),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.Dropout(rate=0.5),

    layers.Dense(label, activation="softmax")
])

model.summary()

# Training the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=EPOCHS, batch_size=64, validation_data=(x_test, y_test), callbacks=callback)

loss, acc = model.evaluate(x_test, y_test, verbose=1)
print(f"Loss: {loss : .4f}\nAccuracy: {acc * 100 : .2f}%")

# Saves model's history
with open(os.path.join(HISTORY_PATH, "train_history"), 'wb') as f:
    pickle.dump(history.history, f)

# Plot model's accuracy and loss over epochs
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')

plt.tight_layout()
plt.show()

