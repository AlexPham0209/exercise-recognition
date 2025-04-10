import requests, zipfile, io, os, pickle
import numpy as np
import tensorflow as tf
from keras import layers, models

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATA_PATH = os.path.join("dataset", "uci_har")

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
y_train = tf.one_hot(np.loadtxt(os.path.join(train_path, "y_train.txt")) - 1, depth=6)

x_test = extract_features(os.path.join(test_path, "Inertial Signals"))
y_test = tf.one_hot(np.loadtxt(os.path.join(test_path, "y_test.txt")) - 1, depth=6)

print("\nTraining Set:")
print(f"x_train: {x_train.shape}")
print(f"y_train: {y_train.shape}\n")

print("Test Set:")
print(f"x_test: {x_test.shape}")
print(f"y_test: {y_test.shape}\n")

print(f"TensorFlow version: {tf.__version__}\n")

# Make model folder
if not os.path.isdir("model"):
    os.mkdir("model")

model = models.Sequential([
    layers.Input((x_train.shape[1], x_train.shape[2])),
    layers.LSTM(64),
    layers.Dropout(rate=0.2),
    layers.Dense(128, activation="relu"),
    layers.Dense(6, activation="softmax")
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))



