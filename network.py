import socket, json
from server import streaming
from client import gaming
from threading import Thread


def create_server():
    server_sock = socket.socket()
    host_name = socket.gethostbyname(socket.gethostname())
    if "stream" in machine:
        streaming_machines.append(host_name)
    else:
        gaming_machines.append(host_name)
    server_sock.bind((host_name, 5001))
    return server_sock, host_name



def gaming_server(server_sock):
    while True:
        conn, addr = server_sock.accept()
        json_type = conn.recv(4096)
        machine_type = json.loads(json_type.decode())
        if "stream" in machine_type:
            streaming_machines.append(machine_type["stream"])
            conn.send("All machines on network: {}".format(gaming_machines + streaming_machines).encode())
        else:
            gaming_machines.append(machine_type["game"])
            conn.send("Available machines to connect to: {}".format(streaming_machines).encode())



if __name__ == "__main__":
    # Machines used to play games that are being streamed
    gaming_machines = []

    # Machines used to stream games for others to play
    streaming_machines = []

    server_sock = None
    node = None
    waiting = False
    machine = input("Will this device be used to stream local games or play games? ")
    server = input("Is there a server already running? ")

    # Initialize server if there is not one currently
    if "no" in server or "No" in server:
        server_sock, host_name = create_server()
        server_sock.listen()
        print("New Server: " + host_name)
    # Else enter IP of server and connect to it
    else:
        ip = input("Please enter in the server IP: ")
        node = socket.socket()
        host_name = socket.gethostbyname(socket.gethostname())
        node.settimeout(5)
        while True:
            try:
                node.connect((ip, 5001))
                print("Connected to: " + ip)
                break
            except socket.timeout:
                response = input("No server detected. Enter a different IP? (y/n) ")
                if response == "y":
                    ip = input("IP Address: ")
                    continue
                else:
                    print("Initializing this machine as the server.")
                    server_sock, host_name = create_server()
                    server_sock.listen()
                    print("New Server: " + host_name)
                    node = None
                    break

    # If this machine is running the server
    if server_sock is not None:
        if "stream" in machine:
            print("Waiting for machine to connect . . .")
            process = Thread(target=streaming, args=())
            process.start()
        else:
            print("Waiting for an available machine . . .")
            waiting = True
        while True:
            conn, addr = server_sock.accept()
            json_type = conn.recv(4096)
            machine_type = json.loads(json_type.decode())
            if "stream" in machine_type:
                streaming_machines.append(machine_type["stream"])
                conn.send("All machines on network: {}".format(gaming_machines + streaming_machines).encode())
                if waiting is True:
                    process = Thread(target=gaming_server, args=(server_sock,))
                    process.start()
                    gaming(machine_type["stream"])
            else:
                gaming_machines.append(machine_type["game"])
                conn.send("Available machines to connect to: {}".format(streaming_machines).encode())
    # Else the machine is not running the server
    else:
        if "stream" in machine:
            node.send(json.dumps({"stream": host_name}).encode())
            print(node.recv(4096).decode())
            print("Waiting for machine to connect . . .")
            streaming()
        else:
            node.send(json.dumps({"game": host_name}).encode())
            print(node.recv(4096).decode())
            ip_connect = input("Which machine did you want to connect to? ")
            gaming(ip)
