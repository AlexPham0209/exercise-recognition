import requests, zipfile, io, os

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATA_PATH = os.path.join("dataset", "UCI HAR")

# Download Human Activity Recognition dataset 
print("Downloading dataset...")
r = requests.get(URL, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(DATA_PATH)

# Extract downloaded dataset
print("Extract UCI HAR Dataset...")
with zipfile.ZipFile(os.path.join(DATA_PATH, "UCI HAR Dataset.zip"), 'r') as zip_ref:
    zip_ref.extractall(DATA_PATH)




