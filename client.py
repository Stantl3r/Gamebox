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
global_size = int(stream_machine.recv(4096).decode())
while True:
    data = b''
    size = global_size
    while size != 0:
        read_size = stream_machine.recv(min(size, 40960000))
        size -= len(read_size)
        data += read_size
        print(size)
    stream_machine.send("Received".encode())
    print("Received")
    image = Image.frombytes('RGBA', (int(width), int(height)), data)
    image = np.array(image)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
stream_machine.close()
