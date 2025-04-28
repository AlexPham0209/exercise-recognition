import io
import os
import zipfile

import requests

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATA_PATH = os.path.join("data", "uci_har")

if __name__ == "__main__":
    if not os.path.isdir(DATA_PATH):
        quit()

    # Download Human Activity Recognition dataset 
    print("Downloading dataset...")
    r = requests.get(URL, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(DATA_PATH)

    # Extract downloaded dataset
    print("Extract UCI HAR Dataset...")
    with zipfile.ZipFile(os.path.join(DATA_PATH, "UCI HAR Dataset.zip"), 'rb') as zip_ref:
        zip_ref.extractall(DATA_PATH)
