import numpy as np
import cv2
from PIL import Image
import tkinter as tk

def convert(image, gaming_socket, streaming_socket):
    image.save("screen", format='PNG')
    binary_img = open("screen", 'rb')
    img_bytes = binary_img.read()
    streaming_socket.send(str(len(img_bytes)).encode())
    streaming_socket.recv(4096)
    print("Sending")
    streaming_socket.send(img_bytes)

def stream(streaming_socket):
    # Gets size (in bytes) of screen
    size = int(streaming_socket.recv(4096))
    streaming_socket.send("Got size".encode())

    # Retreives captures of screen from connected computer
    capture = open("stream", 'wb')
    while size != 0:
        print(size)
        data = streaming_socket.recv(min(size, 40960000))
        capture.write(data)
        size -= len(data)
    capture.close()
    streaming_socket.send("Received".encode())
    print("Received")

    # Displays screen on stream computer
    img = Image.open("stream")
    image = np.array(img)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def get_resolution():
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()