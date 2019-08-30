import socket
import numpy as np
import cv2
from PIL import ImageGrab
import time

port = 8081
gaming_machine = socket.socket()
host_name = socket.gethostbyname(socket.gethostname())
gaming_machine.bind((host_name, port))
gaming_machine.listen(1)
print(host_name)

while True:
    # Initializations
    conn, addr = gaming_machine.accept()
    conn.send("Testing connection . . .".encode())
    image = ImageGrab.grab()

    # Getting screen dimensions
    width, height = image.size
    print(width, height)
    conn.send(str(width).encode())
    time.sleep(1)
    conn.send(str(height).encode())

    # Streaming video
    conn.send(str(len(image.tobytes())).encode())
    while True:
        print("Sending")
        conn.send(image.tobytes())
        if conn.recv(4096).decode() == "Received":
            image = ImageGrab.grab()
            print("New Image")

    conn.close()
