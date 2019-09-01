import socket, json, time
import cv2
from video import stream, send_resolution
from pynput.mouse import *
from mouse import send_mouse_pos, send_mouse_clicks

global START, END

def on_click(x, y, button, pressed):
    global START
    global END
    if pressed:
        START = time.time()
    else:
        END = time.time()
        press_time = END - START
        if button == Button.left:
            CLICKS.append(("left", press_time))
        else:
            CLICKS.append(("right", press_time))


if __name__ == "__main__":
    stream_machine = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    port = 8080
    stream_machine.connect(('192.168.0.68', port))
    data = stream_machine.recv(4096)
    print("Message received: ", data.decode())
    CLICKS = []

    mouse = Controller()
    mouse_listener = Listener(on_click=on_click)
    mouse_listener.start()

    width, height = send_resolution(stream_machine)

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
        stream_machine.send("Received".encode())
        print("Received")

        # Send mouse position
        send_mouse_pos(stream_machine, mouse, width, height)

        # Send mouse clicks
        send_mouse_clicks(stream_machine, CLICKS)
        CLICKS.clear()

    mouse_listener.stop()
    cv2.destroyAllWindows()
    stream_machine.close()