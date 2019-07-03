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
		if data.decode("utf-8") == "ping":
			s.send(str.encode("pong"))
		else:
			print("[Server] " + data.decode("utf-8"))
	
