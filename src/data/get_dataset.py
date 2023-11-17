import os
import json
import numpy as np
from ..utils.index import extract_keypoints, actions, NO_SEQUENCES, SEQUENCE_LENGTH, DATA_PATH

for action in actions:
    for sequence in range(NO_SEQUENCES):
        try:
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

for action in actions:
        with open(f'data/{action}.json', 'r') as file:
            data = json.load(file)
            for sequence in range(NO_SEQUENCES):
                    for frame in range(SEQUENCE_LENGTH):
                        results = data[sequence]['landmarks'][frame]
                        keypoints = extract_keypoints(results)
                        npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame))
                        np.save(npy_path, keypoints)
                        