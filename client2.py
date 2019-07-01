import socket
import os
import subprocess

s = socket.socket()
host = '127.0.0.1'
port = 1234

s.connect((host, port))

while True:
	data = s.recv(1024)
	if len(data) > 0:
		print("[Server] " + data.decode("utf-8"))
	msg_to_server = input("=> ")
	s.send(str.encode(msg_to_server))