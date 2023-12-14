import sys
import socket

# s=socket.socket(family=AF_INET,type=SOCK_STREAM,port=)

try:
   sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err:
   print("Reason %s" %str(err))

print('Socket created')

target_host=input("Enter the target_host name to connect:  ")
target_port=input("Enter the target port:   ")
try:
   sock.connect((target_host,int(target_port)))
   # print("soekct connect to: "+target_host+target_port)
   print("Socket connect to %s on port %s" %(target_host,target_port))
   sock.shutdown(2)
except socket.error as err:
   print("Failed to connect to %s on port %s" %(target_host,target_port))
   print("Reason %s " %str(err))
   sys.exit()
   
   
import socket

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',12345))#host ip address, port #

server_socket.listen(5) #take a backlog: max 5 sockets accepted

while True:
   print("Server waiting for connection")
   client_socket,addr=server_socket.accept()
   print("Client connected from ",addr)
   while True:
      data=client_socket.recv(1024)
      if not data or data.decode('utf-8') =='END':
         break
      print("received payload from client: %s" %data.decode('utf-8'))
      try:
         print("")
         client_socket.send(bytes('Hey client','utf-8'))
      except:
         print("Exited by the user")
   client_socket.close()
server_socket.close()


import socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#ipv4, TCP protocol

client_socket.connect(('127.0.0.1',12345))
#send data to server
payload='Hey Server, '

try:
   while True:
      client_socket.send(payload.encode('utf-8'))
      data=client_socket.recv(1024)
      print(str(data))
      more=input("Would you want to send to server? ")
      if more.lower()=='y':
         payload=input("Enter Payload: ")
      else:
         break
except:
   print("Exited by user.")
client_socket.close()


import socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

msg="Hello UDP SERVER"
client_socket.sendto(msg.encode('utf-8'),('127.0.0.1',12345))
data,add=client_socket.recvfrom(4096)
print("Server says ")
print(str(data))
client_socket.close()  


import sys
import socket

# s=socket.socket(family=AF_INET,type=SOCK_STREAM,port=)

try:
   sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err:
   print("Reason %s" %str(err))

print('Socket created')

target_host=input("Enter the target_host name to connect:  ")
target_port=input("Enter the target port:   ")
try:
   sock.connect((target_host,int(target_port)))
   # print("soekct connect to: "+target_host+target_port)
   print("Socket connect to %s on port %s" %(target_host,target_port))
   sock.shutdown(2)
except socket.error as err:
   print("Failed to connect to %s on port %s" %(target_host,target_port))
   print("Reason %s " %str(err))
   sys.exit()
   
   
import socket

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',12345))#host ip address, port #

server_socket.listen(5) #take a backlog: max 5 sockets accepted

while True:
   print("Server waiting for connection")
   client_socket,addr=server_socket.accept()
   print("Client connected from ",addr)
   while True:
      data=client_socket.recv(1024)
      if not data or data.decode('utf-8') =='END':
         break
      print("received payload from client: %s" %data.decode('utf-8'))
      try:
         print("")
         client_socket.send(bytes('Hey client','utf-8'))
      except:
         print("Exited by the user")
   client_socket.close()
server_socket.close()


import socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#ipv4, TCP protocol

client_socket.connect(('127.0.0.1',12345))
#send data to server
payload='Hey Server, '

try:
   while True:
      client_socket.send(payload.encode('utf-8'))
      data=client_socket.recv(1024)
      print(str(data))
      more=input("Would you want to send to server? ")
      if more.lower()=='y':
         payload=input("Enter Payload: ")
      else:
         break
except:
   print("Exited by user.")
client_socket.close()


import socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

msg="Hello UDP SERVER"
client_socket.sendto(msg.encode('utf-8'),('127.0.0.1',12345))
data,add=client_socket.recvfrom(4096)
print("Server says ")
print(str(data))
client_socket.close()   

 

