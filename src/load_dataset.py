# Loading UCI Har Dataset
import os

import numpy as np
from src.download_dataset import DATA_PATH
from sklearn.model_selection import train_test_split

# Extracting features from the dataset
def extract_features(path): 
    res = []
    for name in os.listdir(path):
        feature = np.loadtxt(os.path.join(path, name))
        res.append(feature)
    
    return np.stack(res, axis=-1)

print("Loading UCI Har Dataset...")
train_path = os.path.join(DATA_PATH, "UCI HAR Dataset", "train")
test_path = os.path.join(DATA_PATH, "UCI HAR Dataset", "test")

x_train = extract_features(os.path.join(train_path, "Inertial Signals"))
y_train = np.loadtxt(os.path.join(train_path, "y_train.txt")) - 1

x_test = extract_features(os.path.join(test_path, "Inertial Signals"))
y_test = np.loadtxt(os.path.join(test_path, "y_test.txt")) - 1
x_test, x_valid, y_test, y_valid = train_test_split(x_test, y_test, test_size=0.5, shuffle=True)