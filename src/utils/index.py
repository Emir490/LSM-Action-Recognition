import numpy as np

DATA_PATH = 'data/Signs'
NO_SEQUENCES = 30
SEQUENCE_LENGTH = 30

actions = np.array(['J', 'Ñ', 'Z'])

def extract_keypoints(results):
    pose = np.array(results['pose'])
    face = np.array(results['face'])
    lh = np.array(results['leftHand'])
    rh = np.array(results['rightHand'])
    
    return np.concatenate([pose, face, lh, rh])
    