import os
import numpy as np
from sklearn.model_selection import train_test_split
PATH = os.path.join('data', 'workout')
features = []
labels = []
label = 0

for folder in os.listdir(PATH):
    samples = os.path.join(PATH, folder)

    if not os.path.isdir(samples):
        continue
    
    res = []
    for file in os.listdir(samples):
        sample_path = os.path.join(samples, file)
        sample = np.loadtxt(sample_path).reshape((-1, 238, 6))
        res.append(sample)

    
    if len(res) <= 0:
        continue
    
    res = np.concatenate(res, axis=0)
    features.append(res)
    labels.extend([label] * res.shape[0])
    label += 1 

features = np.concatenate(features, axis=0)
labels = np.array(labels)
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
