import cv2
import numpy as np
from keras.models import load_model, Sequential
import mediapipe as mp
from ..utils.index import actions

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

model: Sequential = load_model('model_fail')

colors = [
    (245, 117, 16),    # Original Orange
    (117, 245, 16),    # Original Green
    (16, 117, 245),    # Original Blue
    (128, 0, 128),     # Purple
    (255, 192, 203),   # Pink
    (255, 255, 0),     # Yellow
    (0, 255, 255),     # Cyan
    (255, 0, 255),     # Magenta
    (192, 192, 192),   # Silver
    (128, 128, 0),     # Olive
    (0, 0, 128),       # Navy Blue
    (128, 0, 0),       # Maroon
    (255, 165, 0),     # Orange
    (0, 128, 0),       # Dark Green
    (75, 0, 130),      # Indigo
    (255, 20, 147),    # Deep Pink
    (70, 130, 180)     # Steel Blue
]

def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    # Adjust these parameters to change the size and position of the rectangles
    rect_start_y = 30   # Starting y-coordinate for the first rectangle
    rect_height = 20    # Height of each rectangle
    spacing = 25        # Space between rectangles
    text_offset = 15    # Offset for text placement

    for num, prob in enumerate(res):
        # Calculate the y-coordinate for the current rectangle
        rect_y = rect_start_y + num * spacing
        # Draw the rectangle
        cv2.rectangle(output_frame, (0, rect_y), (int(prob * 100), rect_y + rect_height), colors[num], -1)
        # Put the text
        cv2.putText(output_frame, actions[num], (0, rect_y + text_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    return output_frame

def mediapipe_detection(image, model: Sequential):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             ) 
    
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

sequence = []
sentence = []
predictions = []
threshold = 0.8

cap = cv2.VideoCapture(0)
# Set mediapipe model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()
        
        # Flip frame horizontally (mirror mode off)
        frame = cv2.flip(frame, 1)
        
        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        
        # Draw landmakrs
        draw_landmarks(image, results)
        
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
        
        sequence.append(keypoints)
        sequence = sequence[-30:]
        
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions.append(np.argmax(res))
            
            # Viz logic
            if np.unique(predictions[-10:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])
                        
            if len(sentence) > 5:
                sentence = sentence[-5:]
                
            # Viz probabilites
            image = prob_viz(res, actions, image, colors)
        
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show to screen
        cv2.imshow('OpenCV Feed', image)
        
        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()