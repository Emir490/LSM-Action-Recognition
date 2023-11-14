import numpy as np

DATA_PATH = 'data/Actions'
NO_SEQUENCES = 90
SEQUENCE_LENGTH = 30

actions = np.array(['acceso', 'duda', 'nada'])

def extract_keypoints(results):
    pose = np.array(results['pose'])
    face = np.array(results['face'])
    lh = np.array(results['leftHand'])
    rh = np.array(results['rightHand'])
    
    return np.concatenate([pose, face, lh, rh])
    