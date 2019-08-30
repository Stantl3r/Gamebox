import socket
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time
import io

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
    while True:
        # Sends screen capture to client machine
        image.save("screen", format='PNG')
        binary_img = open("screen", 'rb')
        img_bytes = binary_img.read()
        conn.send(str(len(img_bytes)).encode())
        conn.recv(4096)
        print("Sending")
        conn.send(img_bytes)

        #Wait for receive message, then captures screen again
        conn.recv(4096).decode()
        image = ImageGrab.grab()
        print("New Image")


    conn.close()
