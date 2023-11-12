import os
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from ..utils.index import actions, DATA_PATH, SEQUENCE_LENGTH

label_map = { label: num for num, label in enumerate(actions) }

print(label_map)

sequences, labels = [], []
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
        window = []
        for frame_num in range(SEQUENCE_LENGTH):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy"))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)