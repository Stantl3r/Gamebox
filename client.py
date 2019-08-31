import socket
import cv2
from video import stream
from pynput.mouse import *

NUMBER_OF_CLICKS = 0
MOUSE_CLICK = False
MOUSE_SCROLL = None

def on_click(x, y, button, pressed):
    MOUSE_CLICK = True
    NUMBER_OF_CLICKS += 1

if __name__ == "__main__":
    stream_machine = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    port = 8080
    stream_machine.connect(('192.168.0.46', port))
    data = stream_machine.recv(4096)
    print("Message received: ", data.decode())

    mouse = Controller()
    #listener = Listener(on_click=on_click, on_scroll=on_scroll)
    #listener.start()

    # Streaming video
    while True:
        # Retrieves frame
        frame = stream(stream_machine)

        # Displays frame
        cv2.namedWindow("Streaming", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Streaming",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Streaming", frame)
        if cv2.waitKey(1) == 27:
            break

        # Send mouse controls
        x, y = mouse.position
        stream_machine.send(str(x).encode())
        stream_machine.recv(1096)
        stream_machine.send(str(y).encode())
        stream_machine.recv(1096)

    cv2.destroyAllWindows()
    stream_machine.close()