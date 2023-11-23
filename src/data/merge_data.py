import os
import json
import numpy as np

actions = np.array(['acceso', 'aceptar', 'ayudar', 'descansar', 'dinero', 'duda', 'gracias', 'hacer', 'hola', 'nada', 'necesitar', 'regresar', 'sin_accion', 'tambien', 'todo', 'traducir', 'urgente'])

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

BASE_PATH = 'data/Señas/'
PATH_1 = 'data/omar/'
PATH_2 = 'data/AlejandroSeñas/'
PATH_3 = 'data/Señas_Abner/'

# Iterate over each action
for action in actions:
    # Construct file paths
    file_path_1 = os.path.join(PATH_1, f"{action}.json")
    file_path_2 = os.path.join(PATH_2, f"{action}.json")
    file_path_3 = os.path.join(PATH_3, f"{action}.json")
    file_path_merged = os.path.join(BASE_PATH, f"{action}.json")
    
    # Check if both files exist
    if os.path.exists(file_path_1) and os.path.exists(file_path_2) and os.path.exists(file_path_3):
        # Load data from files
        data1 = load_json_data(file_path_1)
        data2 = load_json_data(file_path_2)
        data3 = load_json_data(file_path_3)

        # Merge data
        merged_data = data1 + data2 + data3

        # Save merged data
        save_json_data(file_path_merged, merged_data)

        print(f"Merged data saved for action '{action}'. Total length: {len(merged_data)}")
    else:
        print(f"Files for action '{action}' not found.")