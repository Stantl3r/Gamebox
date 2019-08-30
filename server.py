import socket
from PIL import ImageGrab
from video import convert
import pyautogui

if __name__ == "__main__":
    port = 8081
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

            mouse_pos_x = conn.recv(1096).decode()
            conn.send("X Position".encode())
            mouse_pos_y = conn.recv(1096).decode()
            print("X: " + mouse_pos_x, "Y: " + mouse_pos_y)
            conn.send("Y Position".encode())

        conn.close()