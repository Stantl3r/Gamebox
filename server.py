import socket
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time
import io
from video import convert

port = 8082
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

    # Streaming video
    while True:
        convert(image, gaming_machine, conn)

        #Wait for receive message, then captures screen again
        conn.recv(4096).decode()
        image = ImageGrab.grab()
        print("New Image")


    conn.close()
