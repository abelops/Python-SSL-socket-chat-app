from socket import socket, AF_INET, SOCK_STREAM
import ssl
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os	

typ = ""
password=""
serverName=""
serSock = ""
socketList = []
#Server connection
def sendMess(c,userName,messCont,messVal):
	c.send(f"{userName}>{messVal}".encode())


def broadCastMessage(mess):
	print(typ)
	if (typ== "server"):
		for i in socketList:
			i.send(mess.encode())
			print("HERE IS THE THING")

def recMess(c_sock,ussCont,messCont):
	while True:
		mess = c_sock.recv(1024).decode()
		print(mess)
		if("joined" in mess):
			userNm = mess.split(" ")[0]
			ulabel = tk.Label(ussCont, text=f"{userNm}\n", bg="#142245",fg="#00ddff")
			ulabel.pack(fill="both")
		ulabel = tk.Label(messCont, wraplength=367,text=f"{mess} \n", bg="#142245",fg="#00ddff")
		ulabel.pack(side= TOP, anchor="w")
		broadCastMessage(mess)


def handleClient(conn, uname, messCont):
	# conn.send(f"\t You are connected to {serverName} as {uname}".encode())
	while True:
		mess = conn.recv(1024)
		mess= mess.decode()
		if mess == "bye":
			break
		# print("\033[A\033[A")
		print(f"{mess}")
		ulabel = tk.Label(messCont, wraplength=367,text=f"{mess} \n", bg="#142245",fg="#00ddff")
		ulabel.pack(side= TOP, anchor="w")
		broadCastMessage(mess)
	conn.close()



def acceptConnection(s_soc, messCont, ussCont):
	c,addr = s_soc.accept()
	global serSock
	global socketList
	serSock = c
	passwd = c.recv(1024).decode()
	global password
	userName = ""
	if(str(passwd)!=str(password)):
		print(passwd+" "+password)
		messagebox.showerror("Incorrect password", "Incorrect password")
		c.send(b"403")
		c.close()
	else:
		socketList.append(c)
		print(socketList)
		c.send(b"200")
		message = c.recv(1024).decode()
		userNm = message.split(" ")[0]
		userName=userNm
		ulabel = tk.Label(ussCont, text=f"{userNm}\n", bg="#142245",fg="#00ddff")
		ulabel.pack(fill="both")
		ulabel = tk.Label(messCont, text=f"{message} \n", bg="#142245",fg="#00ddff")
		ulabel.pack(fill="both")
		print("got connection")
		waitCon = Thread(target=waitConns, args=(s_soc, messCont, ussCont,))
		waitCon.start()
		t = Thread(target=handleClient, args=(c, message,messCont))
		t.start()


def waitConns(s_soc, messCont, ussCont):
	print("Waiting for connections")
	conns = Thread(target=acceptConnection, args=(s_soc, messCont, ussCont,))
	conns.start()
		# acceptConnection(s_soc, messCont, ussCont)


#server socket creation
def createServer(host, port,username):
	s = socket(AF_INET,SOCK_STREAM)
	os.system("cls")
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain('new.pem','private.key')
	try:
		s.bind((host, port))
		root = tk.Tk()
		root.resizable(0, 0)
		canvas = tk.Canvas(root, height=600, width=600)
		canvas.pack()


		frame = tk.Frame(root, bg="#142245",height=600, width=600)
		frame.place(relx=0, rely=0, relwidth=1, relheight=1)

		leftFrame = tk.Frame(frame, bg="#142245")
		leftFrame.place(relx=0, rely=0, relwidth=0.75, relheight=0.93)

		textCanvas = tk.Canvas(leftFrame, bd=0, bg="#142245" )
		textCanvas.pack(fill="both", expand=1)
		

		messFrame = tk.Frame(textCanvas, bg="#142245")
		messFrame.place(relx=0, rely=0, relwidth=1, relheight=1)


		scrollMess = tk.Scrollbar(messFrame, orient="vertical", command=textCanvas.yview)
		scrollMess.place(relx=0.83, rely=0, relheight=1)


		textCanvas.configure(yscrollcommand=scrollMess.set)
		textCanvas.bind('<Configure>', lambda e:textCanvas.configure(scrollregion = textCanvas.bbox("all")))
		
		messCont = Frame(textCanvas, bg="#142245")
		textCanvas.create_window((0,0), window=messCont, anchor="nw")

		# for i in range(100):
		ulabel = tk.Label(messCont, wraplength=367,text=f"Waiting for client connection ...... \n", bg="#142245",fg="#00ddff")
		ulabel.pack()


		rightFrame = tk.Frame(root, bg="#142245")
		rightFrame.place(relx=0.65, rely=0, relwidth=0.35, relheight=0.93)
		
		rightLabel = tk.Label(rightFrame, text="List of users", fg="#00ddff", font="montserrat 18", bg="#142245")
		rightLabel.pack(fill="both")

		rightCanvas = tk.Canvas(rightFrame, bg="#142245", borderwidth=0)
		rightCanvas.pack(fill="both", expand=1)

		userFrame = tk.Frame(rightCanvas, bg="#142245")
		userFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

		textList = tk.Frame(userFrame, bd=0, bg="#0e1730")
		textList.pack(fill="both")

		scroll = tk.Scrollbar(userFrame, orient="vertical", command=rightCanvas.yview)
		scroll.place(relx=0.9, rely=0, relheight=1)

		rightCanvas.configure(yscrollcommand=scroll.set)
		rightCanvas.bind('<Configure>', lambda e:rightCanvas.configure(scrollregion = rightCanvas.bbox("all")))		

		ussCont = Frame(rightCanvas)
		rightCanvas.create_window((0,0), window=ussCont)

		sendBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		sendBorder.place(relx=0.62, rely=0.933, height=40, relwidth=0.2)

		leaveBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		leaveBorder.place(relx=0.82, rely=0.933, height=40, relwidth=0.18)

		inpBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		inpBorder.place(relx=0, rely=0.933, height=40, relwidth=0.62)


		leaveButton = tk.Button(leaveBorder, text="Leave", bg="#083754", fg="#00ddff", borderwidth=0)
		leaveButton.pack(fill="both", expand=1)
		entry = tk.Entry(inpBorder, bg="#0c5582", borderwidth=0)
		entry.pack(fill="both", expand=1)
		

		s.listen(3)
		s_soc = context.wrap_socket(s,server_side=True)

		def sendMessage():
			messVal = entry.get()	
			ulabel = tk.Label(messCont, wraplength=367,text=f"{username}>{messVal} \n", bg="#142245",fg="#00ddff")
			ulabel.pack( side= TOP, anchor="w")
			mes = f"{username}>{messVal}"
			# sendMess(serSock,username,messCont, messVal)
			broadCastMessage(mes)
		button = tk.Button(sendBorder, text="Send Message", bg="#083754", fg="#00ddff", borderwidth=0, command=sendMessage)
		button.pack(fill="both", expand=1)
		waitConnThread = Thread(target=waitConns, args=(s_soc, messCont, ussCont,))
		waitConnThread.start()
		root.mainloop()
	except Exception as e:
		print(f"[-] Error binding, check if the port is free {e}")



def connectServer(host, port, username, password, root):
	s = socket(AF_INET, SOCK_STREAM)
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
	context.load_verify_locations('new.pem')

	c_sock = context.wrap_socket(s, server_hostname=host)
	c_sock.connect((host,port))
	global typ
	typ= "client"
	c_sock.send(password.encode())
	passCon = c_sock.recv(1024).decode()
	if(passCon=="403"):
		c_sock.close()
	elif(passCon=="200"):
		root.destroy()
		c_sock.send((username+" joined the server").encode())
		# mess = c_sock.recv(1024).decode()
		root = tk.Tk()
		root.resizable(0, 0)
		canvas = tk.Canvas(root, height=600, width=600)
		canvas.pack()

		frame = tk.Frame(root, bg="#142245",height=600, width=600)
		frame.place(relx=0, rely=0, relwidth=1, relheight=1)


		leftFrame = tk.Frame(frame, bg="#142245")
		leftFrame.place(relx=0, rely=0, relwidth=0.75, relheight=0.93)

		textCanvas = tk.Canvas(leftFrame, bd=0, bg="#142245" )
		textCanvas.pack(fill="both", expand=1)
		

		messFrame = tk.Frame(textCanvas, bg="#142245")
		messFrame.place(relx=0, rely=0, relwidth=1, relheight=1)


		scrollMess = tk.Scrollbar(messFrame, orient="vertical", command=textCanvas.yview)
		scrollMess.place(relx=0.83, rely=0, relheight=1)


		textCanvas.configure(yscrollcommand=scrollMess.set)
		textCanvas.bind('<Configure>', lambda e:textCanvas.configure(scrollregion = textCanvas.bbox("all")))
		
		messCont = Frame(textCanvas, bg="#142245")
		textCanvas.create_window((0,0), window=messCont, anchor="nw")

		# for i in range(100):
		# 	ulabel = tk.Label(messCont, wraplength=367,text=f"{i}. List of users List of users List of users List of users List of usersList of users List of users\n", bg="#142245",fg="#00ddff")
		# 	ulabel.pack()
		ulabel = tk.Label(messCont, wraplength=367,text=f" You joined the chat \n", bg="#142245",fg="#00ddff")
		ulabel.pack(side= TOP, anchor="w")

		rightFrame = tk.Frame(root, bg="#142245")
		rightFrame.place(relx=0.65, rely=0, relwidth=0.35, relheight=0.93)
		

		rightLabel = tk.Label(rightFrame, text="List of users", fg="#00ddff", font="montserrat 18", bg="#142245")
		rightLabel.pack(fill="both")

		rightCanvas = tk.Canvas(rightFrame, bg="#142245", borderwidth=0)
		rightCanvas.pack(fill="both", expand=1)


		userFrame = tk.Frame(rightCanvas, bg="#142245")
		userFrame.place(relx=0, rely=0, relwidth=1, relheight=1)



		textList = tk.Frame(userFrame, bd=0, bg="#0e1730")
		textList.pack(fill="both")


		scroll = tk.Scrollbar(userFrame, orient="vertical", command=rightCanvas.yview)
		scroll.place(relx=0.9, rely=0, relheight=1)


		rightCanvas.configure(yscrollcommand=scroll.set)
		rightCanvas.bind('<Configure>', lambda e:rightCanvas.configure(scrollregion = rightCanvas.bbox("all")))
		

		ussCont = Frame(rightCanvas)
		rightCanvas.create_window((0,0), window=ussCont)

		
		# for line in range(100):
		# 	ulabel = tk.Label(ussCont, text=f"{line}. List of users\n", bg="#142245",fg="#00ddff")
		# 	ulabel.pack(fill="both")



		sendBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		sendBorder.place(relx=0.62, rely=0.933, height=40, relwidth=0.2)


		leaveBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		leaveBorder.place(relx=0.82, rely=0.933, height=40, relwidth=0.18)

		inpBorder = tk.Frame(frame, highlightbackground = "#011b2b", highlightthickness = 2, bd=0)
		inpBorder.place(relx=0, rely=0.933, height=40, relwidth=0.62)


		def sendMessage():
			messVal = entry.get()	
			sendMess(c_sock,username,messCont,messVal)


		button = tk.Button(sendBorder, text="Send Message", bg="#083754", fg="#00ddff", borderwidth=0, command=sendMessage)
		button.pack(fill="both", expand=1)

		leaveButton = tk.Button(leaveBorder, text="Leave", bg="#083754", fg="#00ddff", borderwidth=0)
		leaveButton.pack(fill="both", expand=1)
		entry = tk.Entry(inpBorder, bg="#0c5582", borderwidth=0)
		entry.pack(fill="both", expand=1)
		
		t = Thread(target=recMess, args=(c_sock,ussCont,messCont))
		t.start()
		root.mainloop()





def sel():
   selection = "You selected the option " + str(var.get())
   return var.get()



root = tk.Tk()
var = IntVar()
root.resizable(0, 0)
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()

frame = tk.Frame(root, bg="#142245")
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

R1 = Radiobutton(frame, text="Serve", bg="#142245", selectcolor="#142245", borderwidth=0, fg="#00ddff", variable=var, value=1,command=sel)
R1.place(relx=0.3, rely=0.16,anchor = W )

R2 = Radiobutton(frame, text="Join", bg="#142245", selectcolor="#142245", borderwidth=0, fg="#00ddff", variable=var, value=2,command=sel)
R2.place(relx=0.6, rely=0.16,anchor = W )


serNm = Label(frame, text="Host",bg="#142245", fg="#00ddff")
serNm.place(relx=0.3, rely=0.24)
hostEnt = Entry(frame, bd=0)
hostEnt.place(relx=0.3, rely=0.285, relheight=0.07, relwidth=0.4)


portNm = Label(frame, text="Port",bg="#142245", fg="#00ddff")
portNm.place(relx=0.3, rely=0.38)
portEnt = Entry(frame, bd=0)
portEnt.place(relx=0.3, rely=0.43, relheight=0.07, relwidth=0.4)


passNm = Label(frame, text="Password",bg="#142245", fg="#00ddff")
passNm.place(relx=0.3, rely=0.52)
passEnt = Entry(frame, bd=0, show="*")
passEnt.place(relx=0.3, rely=0.58, relheight=0.07, relwidth=0.4)


unameNm = Label(frame, text="Username",bg="#142245", fg="#00ddff")
unameNm.place(relx=0.3, rely=0.66)
unameEnt = Entry(frame, bd=0)
unameEnt.place(relx=0.3, rely=0.71, relheight=0.07, relwidth=0.4)
def getEntry():
	global password
	global serverName
	typee = str(sel())
	server = hostEnt.get()
	serverName=server
	port = portEnt.get()
	password = passEnt.get()
	userName = unameEnt.get()
	print(server+" "+password+" "+typee)
	if(typee==0 or server=="" or password =="" or port=="" or userName==""):
		messagebox.showerror("Empty fields", "Make sure that connection type, server and password are not empty")
	else:
		global typ
		if(typee=="1"):
			root.destroy()
			typ= "server"
			createServer(server, int(port), userName)
		elif(typee=="2"):
			typ= "client"
			connectServer(server, 1143, userName, password,root)
		else:
			messagebox.showerror("Unknown Error", "Unknown Error occured please try again")

submitBut = Button(frame, text="Start", bg="#083754", fg="#00ddff", borderwidth=0, command=getEntry)
submitBut.place(relx=0.3, rely=0.80, relheight=0.07, relwidth=0.4)

root.mainloop()


#Client Connection 
def initConn():
	root = tk.Tk()
	root.resizable(0, 0)
	canvas = tk.Canvas(root, height=400, width=400)
	canvas.pack()

	frame = tk.Frame(root, bg="#142245")
	frame.place(relx=0, rely=0, relwidth=1, relheight=1)

	R1 = Radiobutton(frame, text="Serve", variable=var, value=1,command=sel)
	R1.pack( anchor = W )

	R2 = Radiobutton(frame, text="Join", variable=var, value=2,command=sel)
	R2.pack( anchor = W )


	root.mainloop()




# def 
# def main():
	# chatBox()
	# initConn()
	# connectServer("localhost", 1143,"abelops")

# main()