import numpy as np

DATA_PATH = 'data/Actions'
NO_SEQUENCES = 100
SEQUENCE_LENGTH = 30

# actions = np.array(['acceso', 'aceptar', 'ayudar', 'descansar', 'dinero', 'duda', 'hacer', 'nada', 'otro', 'regresar'])

actions = np.array(['acceso', 'aceptar', 'ayudar', 'descansar', 'dinero', 'duda', 'gracias', 'hacer', 'hola', 'nada', 'necesitar', 'regresar', 'sin_accion', 'tambien', 'todo', 'traducir', 'urgente'])

def extract_keypoints(results):
    pose = np.array(results['pose'])
    face = np.array(results['face'])
    lh = np.array(results['leftHand'])
    rh = np.array(results['rightHand'])
    
    return np.concatenate([pose, face, lh, rh])
    