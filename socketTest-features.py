import socket
import pandas as pd
import tensorflow as tf
import time
import os
import pyautogui as mouse
import numpy as np
from collections import deque
import onnxruntime as rt
import joblib
import json

# This makes the API not crash when the cursor reaches a corner
mouse.FAILSAFE = False

# False here uses the cursor interpolation from the most current frame
# True uses the frame difference to change the cursor (not very good option)
frame_diff = False

# False when using svm
# True when using a TensorFlow model
tensorF = False

# Loads a TensorFlow session
session = rt.InferenceSession("./onnx/final-models/features-with-act-fold0.onnx")
# Loads the SVM model
svm_model = joblib.load("./featureBased/svm.sav")

# Server IP address and port
server_ip = '127.0.0.1'
server_port = 56234
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

# Debug information
#physical_devices = tf.config.list_physical_devices()
#print(physical_devices)
#print(sess)
stack = deque(maxlen=2)
(x,y) = mouse.size()
stack.append((70, 10))
mouse.moveTo(x/2, y/2)


# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))
print('Connected to server {}:{}'.format(server_ip, server_port))

#Scaling
def load_scaling_params(file_path):
    with open(file_path, "r") as params_file:
        scaling_params = json.load(params_file)
    scaler_mean = scaling_params["mean"]
    scaler_scale = scaling_params["scale"]
    return scaler_mean, scaler_scale

# Specify the path to the scaling parameters file
scaling_params_file = "scaling_params.json"

# Load the scaling parameters
scaler_mean, scaler_scale = load_scaling_params(scaling_params_file)

def scale_real_time_sample(sample, scaler_mean, scaler_scale):
    # Scale the real-time sample using the saved scaling parameters
    scaled_sample = (sample - scaler_mean) / scaler_scale
    return scaled_sample

class_names = ["Clique", "Mover", "Rodar", "Zoom in", "Zoom out", "Mouse"]
current_action = "Hello"

while(True):
    # Send data to the server
    message = 'Hello, server!'
    ask_time = time.time()
    client_socket.sendall(message.encode())

    # Receive data from the server
    data = client_socket.recv(1024)
    #print('Received message from server:', data.decode())
    if os.path.exists("C:\\teste\\new-row.csv"):
        # Reads the new frame
        dataframe = pd.read_csv("C:\\teste\\new-row.csv", header=0, index_col=False)
        dataframe.columns = dataframe.columns.str.strip() # Leading and trailing empty spaces from columns removed

        # Get the hand coordinates
        hand_palm_x = dataframe.at[0, "palm.position.x"]
        # If you want the mouse control to be on the vertical plane instead of the horizontal plane you change the palm.position.z to .y
        hand_palm_z = dataframe.at[0, "palm.position.z"]
        print(hand_palm_z)
        stack.append((hand_palm_x, hand_palm_z))

        # Linear interpolation of camera coordinates to screen coordinates
        camera_x_min = -120
        camera_x_max = 120
        camera_y_min = -100
        camera_y_max = 100
        # Screen resolution
        screen_width = 1920
        screen_height = 1080
        screen_x = int(((hand_palm_x - camera_x_min) / (camera_x_max - camera_x_min)) * screen_width)
        screen_y = int(((hand_palm_z - camera_y_min) / (camera_y_max - camera_y_min)) * screen_height)
        print(screen_y)

        # Scales the most recent frame to predict
        if (tensorF):
            scaled_sample = scale_real_time_sample(dataframe, scaler_mean, scaler_scale)
            numpy_array = scaled_sample.to_numpy()
        else:
            scaled_sample = scale_real_time_sample(dataframe, scaler_mean, scaler_scale)
            normalized_row = scaled_sample.drop(columns=['visible_time','grab_angle','pinch_strength','left/right','palm.dir.x','palm.dir.y','palm.dir.z','palm.normal.x','palm.normal.y','palm.normal.z','palm.orienta.x','palm.orienta.y','palm.orienta.z','palm.orienta.w','palm.velocity.x','palm.velocity.y','palm.velocity.z','palm.width','thumb_extend','index_extend','middle_extended','ring_extended','pinky_extend','arm.rot.x','arm.rot.y','arm.rot.z','arm.rot.w','arm.width','arm.prev.x','arm.prev.y','arm.prev.z','arm.next.x','arm.next.y','arm.next.z','thumb.metacarpal.rot.x','thumb.metacarpal.rot.y','thumb.metacarpal.rot.z','thumb.metacarpal.rot.w','thumb.metacarpal.width','thumb.metacarpal.prev.x','thumb.metacarpal.prev.y','thumb.metacarpal.prev.z','thumb.metacarpal.next.x','thumb.metacarpal.next.y','thumb.metacarpal.next.z','thumb.proximal.rot.x','thumb.proximal.rot.y','thumb.proximal.rot.z','thumb.proximal.rot.w','thumb.proximal.width','thumb.proximal.prev.x','thumb.proximal.prev.y','thumb.proximal.prev.z','thumb.proximal.next.x','thumb.proximal.next.y','thumb.proximal.next.z','thumb.intermediate.rot.x','thumb.intermediate.rot.y','thumb.intermediate.rot.z','thumb.intermediate.rot.w','thumb.intermediate.width','thumb.intermediate.prev.x','thumb.intermediate.prev.y','thumb.intermediate.prev.z','thumb.intermediate.next.x','thumb.intermediate.next.y','thumb.intermediate.next.z','thumb.distal.rot.x','thumb.distal.rot.y','thumb.distal.rot.z','thumb.distal.rot.w','thumb.distal.width','thumb.distal.prev.x','thumb.distal.prev.y','thumb.distal.prev.z','index.metacarpal.rot.x','index.metacarpal.rot.y','index.metacarpal.rot.z','index.metacarpal.rot.w','index.metacarpal.width','index.metacarpal.prev.x','index.metacarpal.prev.y','index.metacarpal.prev.z','index.metacarpal.next.x','index.metacarpal.next.y','index.metacarpal.next.z','index.proximal.rot.x','index.proximal.rot.y','index.proximal.rot.z','index.proximal.rot.w','index.proximal.width','index.proximal.prev.x','index.proximal.prev.y','index.proximal.prev.z','index.proximal.next.x','index.proximal.next.y','index.proximal.next.z','index.intermediate.rot.x','index.intermediate.rot.y','index.intermediate.rot.z','index.intermediate.rot.w','index.intermediate.width','index.intermediate.prev.x','index.intermediate.prev.y','index.intermediate.prev.z','index.intermediate.next.x','index.intermediate.next.y','index.intermediate.next.z','index.distal.rot.x','index.distal.rot.y','index.distal.rot.z','index.distal.rot.w','index.distal.width','index.distal.prev.x','index.distal.prev.y','index.distal.prev.z','middle.metacarpal.rot.x','middle.metacarpal.rot.y','middle.metacarpal.rot.z','middle.metacarpal.rot.w','middle.metacarpal.width','middle.metacarpal.prev.x','middle.metacarpal.prev.y','middle.metacarpal.prev.z','middle.metacarpal.next.x','middle.metacarpal.next.y','middle.metacarpal.next.z','middle.proximal.rot.x','middle.proximal.rot.y','middle.proximal.rot.z','middle.proximal.rot.w','middle.proximal.width','middle.proximal.prev.x','middle.proximal.prev.y','middle.proximal.prev.z','middle.proximal.next.x','middle.proximal.next.y','middle.proximal.next.z','middle.intermediate.rot.x','middle.intermediate.rot.y','middle.intermediate.rot.z','middle.intermediate.rot.w','middle.intermediate.width','middle.intermediate.prev.x','middle.intermediate.prev.y','middle.intermediate.prev.z','middle.intermediate.next.x','middle.intermediate.next.y','middle.intermediate.next.z','middle.distal.rot.x','middle.distal.rot.y','middle.distal.rot.z','middle.distal.rot.w','middle.distal.width','middle.distal.prev.x','middle.distal.prev.y','middle.distal.prev.z','ring.metacarpal.rot.x','ring.metacarpal.rot.y','ring.metacarpal.rot.z','ring.metacarpal.rot.w','ring.metacarpal.width','ring.metacarpal.prev.x','ring.metacarpal.prev.y','ring.metacarpal.prev.z','ring.metacarpal.next.x','ring.metacarpal.next.y','ring.metacarpal.next.z','ring.proximal.rot.x','ring.proximal.rot.y','ring.proximal.rot.z','ring.proximal.rot.w','ring.proximal.width','ring.proximal.prev.x','ring.proximal.prev.y','ring.proximal.prev.z','ring.proximal.next.x','ring.proximal.next.y','ring.proximal.next.z','ring.intermediate.rot.x','ring.intermediate.rot.y','ring.intermediate.rot.z','ring.intermediate.rot.w','ring.intermediate.width','ring.intermediate.prev.x','ring.intermediate.prev.y','ring.intermediate.prev.z','ring.intermediate.next.x','ring.intermediate.next.y','ring.intermediate.next.z','ring.distal.rot.x','ring.distal.rot.y','ring.distal.rot.z','ring.distal.rot.w','ring.distal.width','ring.distal.prev.x','ring.distal.prev.y','ring.distal.prev.z','ring.distal.next.x','ring.distal.next.y','ring.distal.next.z','pinky.metacarpal.rot.x','pinky.metacarpal.rot.y','pinky.metacarpal.rot.z','pinky.metacarpal.rot.w','pinky.metacarpal.width','pinky.metacarpal.prev.x','pinky.metacarpal.prev.y','pinky.metacarpal.prev.z','pinky.metacarpal.next.x','pinky.metacarpal.next.y','pinky.metacarpal.next.z','pinky.proximal.rot.x','pinky.proximal.rot.y','pinky.proximal.rot.z','pinky.proximal.rot.w','pinky.proximal.width','pinky.proximal.prev.x','pinky.proximal.prev.y','pinky.proximal.prev.z','pinky.proximal.next.x','pinky.proximal.next.y','pinky.proximal.next.z','pinky.intermediate.rot.x','pinky.intermediate.rot.y','pinky.intermediate.rot.z','pinky.intermediate.rot.w','pinky.intermediate.width','pinky.intermediate.prev.x','pinky.intermediate.prev.y','pinky.intermediate.prev.z','pinky.intermediate.next.x','pinky.intermediate.next.y','pinky.intermediate.next.z','pinky.distal.rot.x','pinky.distal.rot.y','pinky.distal.rot.z','pinky.distal.rot.w','pinky.distal.width','pinky.distal.prev.x','pinky.distal.prev.y','pinky.distal.prev.z','pinky.distal.next.x','pinky.distal.next.y','pinky.distal.next.z'])
        read_time = time.time()
        #print(f"The socket took {read_time - ask_time} seconds to run.")
        

        # Gives a prediction on the most recent frame to predict
        start_time = time.time()
        if (tensorF):
            input_name = session.get_inputs()[0].name
            output_name = session.get_outputs()[0].name
            res = session.run(output_names=[output_name], input_feed={input_name: numpy_array})
        else:
            res = svm_model.predict(normalized_row)
        end_time = time.time()
        print(f"The code took {end_time - start_time} seconds to run.")
        if(tensorF):
            predicted_class= class_names[np.argmax(res)]
            predicted_value = np.max(res)
            predicted_value = round(predicted_value, 4)
            print(f"Predicted class: {predicted_class} with {predicted_value}% confidence")
        else:
            predicted_class = class_names[res[0]]
            print(predicted_class)

        ###### Mouse control #########
        # Release event for Move action
        if((current_action == 'Mover') and (predicted_class!='Mover')):
            mouse.mouseUp(button='left')
        # Release event for Rotate action
        if((current_action == 'Rodar') and (predicted_class != 'Rodar')):
            mouse.mouseUp(button='middle')
        # Click event for clock action - If last action was a click, it doesn't click again
        if ((predicted_class == 'Clique') and (current_action == 'Mouse')):
            #if (current_action != 'Zoom in' and current_action != 'Zoom out'):
            mouse.click()
            current_action = 'Clique'
        # Move event - It presses left click down and then just moves mouse until action change
        if (predicted_class == 'Mover'):
            if (current_action != 'Mover'):
                current_action = 'Mover'
                mouse.mouseDown(button='left')
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            if(frame_diff):
                mouse.move(horizontal_move*0.6, vertical_move*0.4, _pause = False)
            else:
                mouse.moveTo(screen_x, screen_y, _pause= False)
        # Rotate event - It presses middle clicj down and then just moves mouse until action change
        if (predicted_class == 'Rodar'):
            if (current_action != 'Rodar'):
                print(current_action)
                current_action = 'Rodar'
                mouse.mouseDown(button='middle')
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            if(frame_diff):
                mouse.move(horizontal_move*0.6, vertical_move*0.4, _pause=False)
            else:
                mouse.moveTo(screen_x, screen_y, _pause= False)
        # Zoom in event - Scrolls up
        if (predicted_class == 'Zoom in'):
            current_action = 'Zoom in'
            mouse.scroll(50)
        # Zoom out event - Scrolls down
        if (predicted_class == 'Zoom out'):
            current_action = 'Zoom out'
            mouse.scroll(-50)
        # Mouse event - Moves mouse according to frame difference
        if (predicted_class == 'Mouse'):
            current_action = 'Mouse'
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            if(frame_diff):
                mouse.move(horizontal_move*0.6, vertical_move*0.4, _pause=False)
            else:
                mouse.moveTo(screen_x, screen_y, _pause= False)
        if(predicted_class != current_action):
            time.sleep(1)
        # Removes the penultimate frame of the stack so the most recent one can be added
        stack.pop()

# Close the connection
client_socket.close()

