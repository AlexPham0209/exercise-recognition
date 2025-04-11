import requests, zipfile, io, os, pickle
import numpy as np
import tensorflow as tf
from keras import layers, models, callbacks
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATA_PATH = os.path.join("dataset", "uci_har")
EPOCHS = 50

# Extracting features from the dataset
def extract_features(path): 
    res = []
    for name in os.listdir(path):
        feature = np.loadtxt(os.path.join(path, name))
        res.append(feature)
    
    return np.stack(res, axis=-1)
        
# Check if the UCI Har dataset exists
if not os.path.isdir(DATA_PATH):
    # Download Human Activity Recognition dataset 
    print("Downloading dataset...")
    r = requests.get(URL, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(DATA_PATH)

    # Extract downloaded dataset
    print("Extract UCI HAR Dataset...")
    with zipfile.ZipFile(os.path.join(DATA_PATH, "UCI HAR Dataset.zip"), 'rb') as zip_ref:
        zip_ref.extractall(DATA_PATH)

# Loading UCI Har Dataset
print("Loading UCI Har Dataset...")
train_path = os.path.join(DATA_PATH, "UCI HAR Dataset", "train")
test_path = os.path.join(DATA_PATH, "UCI HAR Dataset", "test")

x_train = extract_features(os.path.join(train_path, "Inertial Signals"))
y_train = np.loadtxt(os.path.join(train_path, "y_train.txt")) - 1

x_test = extract_features(os.path.join(test_path, "Inertial Signals"))
y_test = np.loadtxt(os.path.join(test_path, "y_test.txt")) - 1
x_test, x_valid, y_test, y_valid = train_test_split(x_test, y_test, test_size=0.5, shuffle=True)

# Making model folder
if not os.path.isdir("model_data"):
    print("Making save data folder")
    os.mkdir("model_data")

callback = callbacks.ModelCheckpoint(
    filepath=os.path.join("model_data", "best.keras"),
    monitor="val_accuracy",
    mode="max",
    save_best_only=True
)

# Making the model
model = models.Sequential([
    layers.Input((x_train.shape[1], x_train.shape[2])),
    layers.Conv1D(128, kernel_size=3, activation="relu", padding="causal"),
    layers.Conv1D(64, kernel_size=3, activation="relu", padding="causal"),
    layers.MaxPooling1D(),
    layers.Conv1D(32, kernel_size=2, activation="relu", padding="causal"),
    layers.Conv1D(16, kernel_size=2, activation="relu", padding="causal"),
    layers.MaxPooling1D(),
    layers.Dropout(rate=0.5),

    layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
    layers.Bidirectional(layers.LSTM(64, return_sequences=False)),
    layers.Dropout(rate=0.5),
    layers.Dense(128, activation="relu"),
    layers.Dense(6, activation="softmax")
])

model.summary()

# Training the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=EPOCHS, batch_size=32, validation_data=(x_valid, y_valid), callbacks=callback)

# Evaluating model accuracy on test set
model.evaluate(x_test, y_test, verbose=1)

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

