import socket
import cv2
from video import stream
import pyautogui

if __name__ == "__main__":
    stream_machine = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    port = 8081
    stream_machine.connect(('192.168.0.46', port))
    data = stream_machine.recv(4096)
    print("Message received: ", data.decode())

    # Streaming video
    while True:
        # Retrieves frame
        frame = stream(stream_machine)

        # Displays frame
        # cv2.namedWindow("Streaming", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Streaming",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Streaming", frame)
        if cv2.waitKey(1) == 27:
            break

        x, y = pyautogui.position()
        print(str(x).rjust(4), str(y).rjust(4))
        stream_machine.send(str(x).rjust(4).encode())
        stream_machine.recv(1096)
        stream_machine.send(str(y).rjust(4).encode())
        stream_machine.recv(1096)



    cv2.destroyAllWindows()
    stream_machine.close()