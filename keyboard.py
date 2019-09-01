import json, time
from pynput.keyboard import Key

def send_keyboard_input(streaming_socket, KEYPRESS):
    keyboard_input = json.dumps({"Keyboard": KEYPRESS})
    streaming_socket.send(keyboard_input.encode())
    streaming_socket.recv(1096)

def press_keys(streaming_socket, keyboard):
        special_keys = {"backspace": Key.backspace,
                        "shift": Key.shift, 
                        "tab": Key.tab, 
                        "space": Key.space,
                        "enter": Key.enter,
                        "ctrl": Key.ctrl,
                        "cmd": Key.cmd,
                        "alt": Key.alt
        }
        json_keyboard = json.loads(streaming_socket.recv(8096).decode())
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
        streaming_socket.send("Keyboard input".encode())