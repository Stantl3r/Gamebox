import socket, json, time
import cv2
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from pynput.keyboard import Listener as KeyListener
from mouse import send_mouse_pos, send_mouse_clicks
from video import stream, send_resolution


def on_click(x, y, button, pressed):
    if pressed:
        CURRENT_CLICK.append(time.time())
    else:
        if button == Button.left:
            CLICKS.append(("left", time.time() - CURRENT_CLICK[0]))
        else:
            CLICKS.append(("right", time.time() - CURRENT_CLICK[0]))
        CURRENT_CLICK.clear()


def on_press(key):
    CURRENT_KEY[str(key)] = time.time()


def on_release(key):
    try:
        KEYPRESS.append((str(key), time.time() - CURRENT_KEY[str(key)]))
        CURRENT_KEY.pop(str(key))
    except:
        None


if __name__ == "__main__":
    port = 8080
    stream_machine = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    stream_machine.connect(('192.168.0.46', port))
    data = stream_machine.recv(4096)
    print("Message received: ", data.decode())

    CURRENT_CLICK = []
    CLICKS = []
    mouse = MouseController()
    mouse_listener = MouseListener(on_click=on_click)
    mouse_listener.start()

    CURRENT_KEY = {}
    KEYPRESS = []
    keyboard = KeyController()
    keyboard_listener = KeyListener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

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

        # Send keyboard input
        keyboard_input = json.dumps({"Keyboard": KEYPRESS})
        stream_machine.send(keyboard_input.encode())
        stream_machine.recv(1096)
        KEYPRESS.clear()
        CURRENT_KEY.clear()

    mouse_listener.stop()
    cv2.destroyAllWindows()
    stream_machine.close()