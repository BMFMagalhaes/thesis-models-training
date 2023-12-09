import socket
import pandas as pd
import time
import tensorflow as tf
import os
import pyautogui as mouse
from tensorflow import keras
import numpy as np
import onnxruntime as rt
from collections import deque

# Esta abordagem como não foi usada não está otimizada e está implementada de uma forma um pouco "bruta"
# O programa em C guarda todas as imagens que recebe do Leap Motion e este simplesmente vai buscar a mais recente e periodicamente
# elimina para não ficar infinitamente a ocupar memória

frame_exists = False
# Pode ser grayscale ou rgb
color_mode = "grayscale"

# Estas definições estão aqui para alterar conforme o modelo foi treinado
resize = False
rescale = False

# Load do modelo TensorFlow
session = rt.InferenceSession("./onnx/final-models/cnn1-img-aug-fold0.onnx")

# Setup do modo de controlo da diferença entre dois frames (não é uma boa opção)
# Ver como fiz para as features para trazer a outra forma de controlo para aqui
stack = deque(maxlen=2)
stack.append((70, 10))
# Server IP address and port
server_ip = '127.0.0.1'
server_port = 56234

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_action = "Hello"
# Connect to the server
client_socket.connect((server_ip, server_port))
print('Connected to server {}:{}'.format(server_ip, server_port))

while(True):
    frame_exists = False
    # Send data to the server
    message = 'Hello, server!'
    client_socket.sendall(message.encode())

    # Receive data from the server
    data = client_socket.recv(1024)
    print('Received message from server:', data.decode())
    data = data.decode()
    image_path = f"C:\\teste\\{data}.png"
    if (os.path.exists(image_path) and os.path.exists("C:\\teste\\hand-position.csv")):
        # Flag to check if there are things to do
        frame_exists = True

        dataframe = pd.read_csv("C:\\teste\\hand-position.csv", header=0, index_col=False)
        hand_palm_x = dataframe.at[0, "palm.position.x"]
        hand_palm_z = dataframe.at[0, "palm.position.z"]
        stack.append((hand_palm_x, hand_palm_z))

        # Linear interpolation of camera coordinates to screen coordinates
        camera_x_min = -200
        camera_x_max = 200
        camera_y_min = -150
        camera_y_max = 150
        # Screen resolution
        screen_width = 1920
        screen_height = 1080
        screen_x = int(((hand_palm_x - camera_x_min) / (camera_x_max - camera_x_min)) * screen_width)
        screen_y = int(((hand_palm_z - camera_y_min) / (camera_y_max - camera_y_min)) * screen_height)

        # Gets the image to predict and resizes it to the shape expected by the model
        img = keras.utils.load_img(f"C:\\teste\\{data}.png", target_size=(640,240), color_mode=color_mode)
        img_array = keras.utils.img_to_array(img)
        if (resize):
            img_array = keras.preprocessing.image.smart_resize(img_array, (224,224))
        if (rescale):
            img_array = img_array / 255.0
        #img_array = layers(img_array)
        #print(rescaled_img)
        if (resize):
            img_array = np.reshape(img_array, (1, 224, 224, 3))
        else:
            img_array = np.reshape(img_array, (1, 240, 640, 1))


    else:
        print("Não há frames para prever.")

    # Periodicamente elimina as imagens como referi anteriormente
    items = os.listdir("C:\\teste")
    if(len(items) > 50):
        for filename in os.listdir("C:\\teste"):
            file_path = os.path.join("C:\\teste\\", filename)
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)

    if (frame_exists):
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name  #
        start_time = time.time()
        res = session.run(output_names=[output_name], input_feed={input_name: img_array})
        end_time = time.time()
        # Print the elapsed time
        print(f"The code took {end_time - start_time} seconds to run.")
        class_names = ["Clique", "Mover", "Rodar", "Zoom in", "Zoom out", "Mouse"]
        predicted_class= class_names[np.argmax(res)]
        predicted_value = np.max(res)
        predicted_value = round(predicted_value, 4)
        print(f"Predicted class: {predicted_class} with {predicted_value}% confidence")

    
        ##### Mouse control ######
        if((current_action == 'Mover') and (predicted_class!='Mover')):
                mouse.mouseUp(button='left')
            # Release event for Rotate action
        if((current_action == 'Rodar') and (predicted_class != 'Rodar')):
                mouse.mouseUp(button='middle')
            # Click event for clock action - If last action was a click, it doesn't click again
        if ((predicted_class == 'Clique') and (current_action != 'Clique')):
                mouse.click()
                current_action = 'Clique'
            # Move event - It presses left click down and then just moves mouse until action change
        if (predicted_class == 'Mover'):
            if (current_action != 'Mover'):
                print(current_action)
                current_action = 'Mover'
                mouse.mouseDown(button='left')
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            mouse.move(horizontal_move, vertical_move*0.6, duration=0.1)
        # Rotate event - It presses middle clicj down and then just moves mouse until action change
        if (predicted_class == 'Rodar'):
            if (current_action != 'Rodar'):
                print(current_action)
                current_action = 'Rodar'
                mouse.mouseDown(button='middle')
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            mouse.move(horizontal_move, vertical_move*0.6, duration=0.1)
        # Zoom in event - Scrolls up
        if (predicted_class == 'Zoom in'):
            current_action = 'Zoom in'
            mouse.scroll(6)
        # Zoom out event - Scrolls down
        if (predicted_class == 'Zoom out'):
            current_action = 'Zoom out'
            mouse.scroll(-6)
        # Mouse event - Moves mouse according to frame difference
        if (predicted_class == 'Mouse'):
            current_action = 'Mouse'
            horizontal_move = stack[1][0] - stack[0][0]
            vertical_move = stack[1][1] - stack[0][1]
            #mouse.move(horizontal_move, vertical_move*0.6, duration=0.1)
            mouse.moveTo(screen_x, screen_y, _pause=False)
        stack.pop()


# Close the connection
client_socket.close()
