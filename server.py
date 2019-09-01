import socket, json, time
from PIL import ImageGrab
from video import convert, calc_resolution
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from mouse import move_mouse, click_mouse

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

        mouse = MouseController()
        keyboard = KeyController()
        special_keys = {"backspace": Key.backspace,
                        "shift": Key.shift, 
                        "tab": Key.tab, 
                        "space": Key.space,
                        "enter": Key.enter,
                        "ctrl": Key.ctrl,
                        "cmd": Key.cmd,
                        "alt": Key.alt
        }

        width, height = calc_resolution(conn)
        # Streaming video
        while True:
            convert(image, gaming_machine, conn)

            #Wait for receive message, then captures screen again
            conn.recv(1096).decode()
            image = ImageGrab.grab()
            print("New Image")

            # Move mouse
            move_mouse(conn, mouse, width, height)

            # Click mouse
            click_mouse(conn, mouse)

            # Keyboard
            json_keyboard = json.loads(conn.recv(8096).decode())
            keyboard_input = json_keyboard.get("Keyboard")
            for key in keyboard_input:
                print("Key Pressed")
                if len(key[0]) < 4:
                    real_key = key[0].split('\'')[1]
                    print(real_key)
                    keyboard.press(real_key)
                    time.sleep(key[1])
                    keyboard.release(real_key)
                else:
                    print("Special key")
                    check_key = key[0].split('.')[1]
                    if check_key in special_keys:
                        keyboard.press(special_keys[check_key])
                        time.sleep(key[1])
                        keyboard.release(special_keys[check_key])
                    else:
                        continue
            conn.send("Keyboard input".encode())



        conn.close()