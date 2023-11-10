import numpy as np

actions = np.array(['J', 'Ñ', 'Z'])

def extract_keypoints(results):
    pose = np.array(results['pose'])
    face = np.array(results['face'])
    lh = np.array(results['leftHand'])
    rh = np.array(results['rightHand'])
    
    return np.concatenate([pose, face, lh, rh])
    