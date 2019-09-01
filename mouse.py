from pynput.mouse import *
import json, time

def send_mouse_pos(gaming_socket, mouse, width, height):
    x, y = mouse.position
    x_ratio = x/width
    y_ratio = y/height
    gaming_socket.send(str(x_ratio).encode())
    gaming_socket.recv(1096)
    gaming_socket.send(str(y_ratio).encode())
    gaming_socket.recv(1096)

def send_mouse_clicks(gaming_socket, CLICKS):
    stream_clicks = json.dumps({"0": CLICKS})
    gaming_socket.send(stream_clicks.encode())
    gaming_socket.recv(1096)

def move_mouse(gaming_socket, mouse, width, height):
    mouse_pos_x = gaming_socket.recv(4096).decode()
    gaming_socket.send("X Position".encode())
    mouse_pos_y = gaming_socket.recv(4096).decode()
    gaming_socket.send("Y Position".encode())
    print("X: " + mouse_pos_x, "Y: " + mouse_pos_y)
    mouse.position = (float(mouse_pos_x) * width, float(mouse_pos_y) * height)

def click_mouse(gaming_socket, mouse):
    pickled_clicks = gaming_socket.recv(8096)
    json_clicks = json.loads(pickled_clicks.decode())
    mouse_clicks = json_clicks.get("0")
    for click in mouse_clicks:
        print("Mouse clicked")
        if click[0] == "left":
            mouse.press(Button.left)
            time.sleep(click[1])
            mouse.release(Button.left)
        else:
            mouse.press(Button.right)
            time.sleep(click[1])
            mouse.release(Button.right)
    gaming_socket.send("Mouse clicks".encode())