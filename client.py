import socket
import cv2
from video import stream

stream_machine = socket.socket()
host_name = socket.gethostbyname(socket.gethostname())
port = 8082
stream_machine.connect(('192.168.0.46', port))
data = stream_machine.recv(4096)
print("Message received: ", data.decode())

# Streaming video
while True:
    # Retrieves frame
    frame = stream(stream_machine)

    # Displays frame
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
stream_machine.close()
