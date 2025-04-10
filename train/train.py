import requests, zipfile, io, os, pickle
import numpy as np

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATA_PATH = os.path.join("dataset", "uci_har")

def extract_features(path): 
    file_names = os.listdir(path)
    res = []
    for name in file_names:
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
y_train = np.loadtxt(os.path.join(train_path, "y_train.txt"))

x_test = extract_features(os.path.join(test_path, "Inertial Signals"))
y_test = np.loadtxt(os.path.join(test_path, "y_test.txt"))

print("\nTraining Set:")
print(f"x_train: {x_train.shape}")
print(f"y_train: {y_train.shape}\n")

print("Test Set:")
print(f"x_test: {x_test.shape}")
print(f"y_test: {y_test.shape}\n")






