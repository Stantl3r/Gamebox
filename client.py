import socket
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time

stream_machine = socket.socket()
host_name = socket.gethostbyname(socket.gethostname())
port = 8081
stream_machine.connect(('192.168.0.46', port))
data = stream_machine.recv(4096)
print("Message received: ", data.decode())

width = stream_machine.recv(4096)
time.sleep(1)
height = stream_machine.recv(4096)
width, height = width.decode(), height.decode()
print(width, height)

# Streaming video
while True:
    # Gets size (in bytes) of screen
    size = int(stream_machine.recv(4096))
    stream_machine.send("Got size".encode())

    # Retreives gaming screen
    myfile = open("screen1", 'wb')
    while size != 0:
        print(size)
        data = stream_machine.recv(min(size, 40960000))
        myfile.write(data)
        size -= len(data)
    myfile.close()
    stream_machine.send("Received".encode())
    print("Received")

    # Displays screen on stream computer
    img = Image.open("screen1")
    image = np.array(img)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
stream_machine.close()