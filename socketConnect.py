#import socket
from socket import SOCK_STREAM, socket, AF_INET

connection = socket(AF_INET, SOCK_STREAM)
connection.connect(("10.0.2.10", 8080))

connection.send(b"Connection established")

connection.close()