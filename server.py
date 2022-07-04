from socket import socket, AF_INET, SOCK_STREAM
import ssl
import os
from threading import Thread

numHost = 0
serverName = "Server"
password = ""
def sendMess(c):
	while True:
		ms = input(f"Me> ")
		c.sendall(f"server>{ms}".encode())

def handleClient(conn, uname):
	conn.send(f"\t You are connected to {serverName} as {uname}".encode())
	while True:
		mess = conn.recv(1024)
		mess= mess.decode()
		if mess == "bye":
			break
		# print("\033[A\033[A")
		print(f"{mess}")
		t = Thread(target=sendMess, args=(conn,))
		t.start()
	conn.close()
def acceptConnection(s_soc):
	c,addr = s_soc.accept()
	passwd = c.recv(1024).decode()
	if(passwd!=password):
		c.send(b"403")
		c.close()
	else:
		message = c.recv(1024).decode()
		print(+message+f" has joined the chat")
		t = Thread(target=handleClient, args=(c, message,))
		t.start()
		sendMess(c)


def createServer(host, port):
	s = socket(AF_INET,SOCK_STREAM)
	os.system("cls")
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain('new.pem','private.key')
	try:
		s.bind((host, port))
		print(f"{green} [+] Server is now listening on {host}:{port}")
		s.listen(3)
		s_soc = context.wrap_socket(s,server_side=True)
	except Exception as e:
		print(f"[-] Error binding, check if the port is free {e}")
	while True:
		acceptConnection(s_soc)


createServer("localhost", 1143)
