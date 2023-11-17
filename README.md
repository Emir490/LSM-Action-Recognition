# LSM Action Recognition

## Overview
This project focuses on implementing action recognition for the LSM (Mexican Sign Language) using deep learning. The core functionality involves processing a dataset of JSON files into numpy arrays representing keypoints for pose, face, and hands, obtained via the MediaPipe framework. The project uses TensorFlow and Keras for training a Sequential model with LSTM layers, allowing for effective recognition of LSM actions.

## Features
* Data Processing: Converts JSON files into organized numpy arrays, stored in structured folders indicating actions, sequences per action, and frames per sequence.
* Keypoint Extraction: Utilizes MediaPipe to extract keypoints related to pose, face, and hands.
* Model Training: Employs a Sequential model with two LSTM layers and a Dense layer, optimized for time-series data inherent in action recognition tasks.
* Performance Visualization: Integrates TensorBoard for tracking and visualizing the model's training performance.
* Real-time Testing: Includes a script for real-time LSM action recognition using MediaPipe Holistic and OpenCV's webcam functionalities.
* Predictive Analysis: Uses Matplotlib, Seaborn, and Scikit-learn for evaluating and visualizing model predictions.

## Installation
### Prerequisites
* Python 3.11
* Pip (Python package installer)

### Required Libraries
Install the required libraries by running:
```pip install -r requirements.txt```

## Usage

To run any script, use the Python module execution syntax. It is crucial to include the `-m` flag for the script to execute correctly.

For example, to train the model, navigate to the project's root directory and run:
```python -m src.models.train```

## Real-time Testing
To test the model in real-time, ensure you have a functioning webcam. Run the real-time testing script as follows:
```python -m src.tests.test```