import os
import pickle
import keras
from keras import layers, models, callbacks
import matplotlib.pyplot as plt

# Saves model's history
with open(os.path.join('results', "train_history"), 'rb') as f:
    history = pickle.load(f)

# Plot model's accuracy and loss over epochs
plt.subplot(1, 2, 1)
plt.plot(history['accuracy'])
plt.plot(history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')

plt.tight_layout()
plt.show()

