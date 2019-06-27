# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port))

#Telling the server that a new slave has come
s.send('ON'.encode())
# receive data from the server 
while True:
   msg = input("Write msg: ")
   s.send(msg.encode())

   msg = input("End Connection:  ")

   
# close the connection 
s.close()       

