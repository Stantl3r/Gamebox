import numpy as np
import cv2
from PIL import Image
import tkinter as tk

def convert(image, gaming_socket, streaming_socket):
    image.save("screen", format='PNG', optimize=True, quality=85)
    binary_img = open("screen", 'rb')
    img_bytes = binary_img.read()
    streaming_socket.send(str(len(img_bytes)).encode())
    streaming_socket.recv(4096)
    print("Sending")
    streaming_socket.send(img_bytes)

def stream(streaming_socket):
    width, height = get_resolution()

    # Gets size (in bytes) of screen
    size = int(streaming_socket.recv(4096))
    streaming_socket.send("Got size".encode())

    # Retreives captures of screen from connected computer
    capture = open("stream", 'wb')
    while size != 0:
        print(size, min(size, 1048576))
        data = streaming_socket.recv(min(size, 1048576))
        capture.write(data)
        size -= len(data)
    capture.close()
    # streaming_socket.send("Received".encode())
    # print("Received")

    # Displays screen on stream computer
    img = Image.open("stream")
    image = np.array(img)
    image = cv2.resize(image, (width, height))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def get_resolution():
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def send_resolution(streaming_socket):
    width, height = get_resolution()
    streaming_socket.send(str(width).encode())
    streaming_socket.recv(1096)
    streaming_socket.send(str(height).encode())
    streaming_socket.recv(1096)
    return width, height

def calc_resolution(streaming_socket):
    width, height = get_resolution()
    stream_width = int(streaming_socket.recv(1096).decode())
    streaming_socket.send("Width".encode())
    stream_height = int(streaming_socket.recv(1096).decode())
    streaming_socket.send("Height".encode())
    return width, height