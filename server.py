import socket, pickle
from PIL import ImageGrab
from video import convert, calc_resolution
from pynput.mouse import Button, Controller
import time

if __name__ == "__main__":
    port = 8080
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

        mouse = Controller()

        width, height = calc_resolution(conn)
        # Streaming video
        while True:
            convert(image, gaming_machine, conn)

            #Wait for receive message, then captures screen again
            conn.recv(4096).decode()
            image = ImageGrab.grab()
            print("New Image")

            # Move mouse
            mouse_pos_x = conn.recv(4096).decode()
            conn.send("X Position".encode())
            mouse_pos_y = conn.recv(4096).decode()
            conn.send("Y Position".encode())
            print("X: " + mouse_pos_x, "Y: " + mouse_pos_y)
            try:
                mouse.position = (float(mouse_pos_x) * width, float(mouse_pos_y) * height)
            except:
                continue

            # Click mouse
            pickled_clicks = conn.recv(8096)
            mouse_clicks = pickle.loads(pickled_clicks)
            for click in mouse_clicks:
                print("Mouse clicked")
                mouse.position = click[0]
                mouse.press(click[1])
                time.sleep(click[2])
                mouse.release(click[1])
            conn.send("Mouse clicks".encode())


        conn.close()