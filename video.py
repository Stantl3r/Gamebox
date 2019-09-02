import numpy as np
import cv2
from PIL import Image
import tkinter as tk

def convert(image, gaming_socket):
    image.save("screen", format='PNG', optimize=True, quality=85)
    binary_img = open("screen", 'rb')
    img_bytes = binary_img.read()
    gaming_socket.send(str(len(img_bytes)).encode())
    gaming_socket.recv(4096)
    print("Sending")
    gaming_socket.send(img_bytes)

def stream(gaming_socket):
    width, height = get_resolution()

    # Gets size (in bytes) of screen
    size = int(gaming_socket.recv(4096))
    gaming_socket.send("Got size".encode())

    # Retreives captures of screen from connected computer
    capture = open("stream", 'wb')
    while size != 0:
        print(size, min(size, 1048576))
        data = gaming_socket.recv(min(size, 1048576))
        capture.write(data)
        size -= len(data)
    capture.close()

    # Displays screen on stream computer
    img = Image.open("stream")
    image = np.array(img)
    image = cv2.resize(image, (width, height))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def get_resolution():
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def send_resolution(gaming_socket):
    width, height = get_resolution()
    gaming_socket.send(str(width).encode())
    gaming_socket.recv(1096)
    gaming_socket.send(str(height).encode())
    gaming_socket.recv(1096)
    return width, height

def calc_resolution(gaming_socket):
    width, height = get_resolution()
    stream_width = int(gaming_socket.recv(1096).decode())
    gaming_socket.send("Width".encode())
    stream_height = int(gaming_socket.recv(1096).decode())
    gaming_socket.send("Height".encode())
    return width, height