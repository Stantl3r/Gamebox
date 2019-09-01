import socket, json, time
from PIL import ImageGrab
from video import convert, calc_resolution
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from mouse import move_mouse, click_mouse
from keyboard import press_keys

# if __name__ == "__main__":
def streaming():
    port = 5000
    stream_machine = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    stream_machine.bind((host_name, port))
    stream_machine.listen(1)
    print(host_name)

    while True:
        # Initializations
        conn, addr = stream_machine.accept()
        conn.send("Testing connection . . .".encode())
        image = ImageGrab.grab()

        mouse = MouseController()
        keyboard = KeyController()

        width, height = calc_resolution(conn)
        # Streaming video
        while True:
            convert(image, conn)

            #Wait for receive message, then captures screen again
            conn.recv(1096).decode()
            image = ImageGrab.grab()
            print("New Image")

            # Move mouse
            move_mouse(conn, mouse, width, height)

            # Click mouse
            click_mouse(conn, mouse)

            # Keyboard
            press_keys(conn, keyboard)

        conn.close()