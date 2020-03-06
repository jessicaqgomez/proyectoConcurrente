from tkinter import*
import socket
from  _thread import *
from PIL import ImageTk,Image 
import ctypes
import mouse


class Cliente():
	def __init__(self):
		self.username=""
		self.socket = socket.socket()    	
		self.estado = None
		self.comenzar = False
		self.turno = False
		self.acabo = False
		self.hostname = "localhost"
		self.port = 25000
		
		self.conectarse()
	
	def conectarse(self):
		try:
			self.socket.connect((self.hostname, self.port))
		except Exception as e:
			self.socket = None
			print("no se conecto",e)
class Registro():
	def __init__(self):
		self.Cliente = Cliente()
		self.raiz = Tk()
		self.join = False
		self.raiz.title("registro")
		self.raiz.resizable(False,False)
		self.username = ""
		self.estado = None
		
		self.frame=Frame(self.raiz,width="500",height="280")
		self.frame.pack()
		self.raiz.config(bg="black")
		self.image = Image.open("imagenes/logo.jpg")
		
		self.image.thumbnail((500,310), Image.ANTIALIAS)
		self.image1 = ImageTk.PhotoImage(self.image) 
		self.CheckVar1 = IntVar()
		#self.Cliente.conectarse()

		
		def obtenerRespuesta():
			while True:
				command = self.Cliente.socket.recv(1024).decode("UTF-8")
				subCommand = command[0:4]

				if subCommand == "4000":
					self.estado = None
				elif subCommand == "4001":
					msg = command[5:].split(" ")
					print(msg)
					if msg[1].upper() == "SI" or  msg[1].upper() == "si":
						self.Cliente.turno = True
					else:
						self.Cliente.turno = False 
					print(self.Cliente, command[5:])
					self.raiz.iconify()
					m = mouse.Principal(self.Cliente.socket, self.username, self.raiz, self.username, self.Cliente.turno)
				elif subCommand == "5000":
					pass
				

			
		def registrar():
			try:
			
				start_new_thread(obtenerRespuesta, ())
				self.username = txtUsername.get() 
				msg= ("REGISTER "+self.username+"\n").encode("UTF-8")
				print(msg)
			
				self.Cliente.socket.send(msg)
				btnJoin.config(state=NORMAL)
				btnRegister.config(state=DISABLED)
				
			except Exception as e:
				raise e
		
		def Join():
			msg= ("JOIN\n").encode("UTF-8")
			self.Cliente.socket.send(msg)

			

		label1 = Label(self.frame, image=self.image1, textvariable="labelText",font=("Times New Roman", 24), height=4, fg="blue") 
		label1.place(x=0,y=0, relwidth=1, relheight=1)


		lblUsername=Label(self.frame,text="Usarname",bg="black", fg="white",font=(12))
		lblUsername.place(x=50,y=200)
		
		lblError = Label(self.frame,text="Servidor no disponible en el momento",bg="black",fg="red",font=(10))
		lblError.place(x=10,y=250)
		txtUsername=Entry(self.frame,width=15, state =NORMAL)	
		txtUsername.place(x=150,y=200)

		
		btnRegister=Button(self.frame, text="Register", command= lambda:registrar(), state =NORMAL)
		btnRegister.place(x=255,y=200)

		
		btnJoin=Button(self.frame, text="Join", command= lambda:Join(), state =DISABLED)
		btnJoin.place(x=310,y=200)	
		

		if(self.Cliente.socket == None):
			btnRegister.config(state= DISABLED)
			txtUsername.config(state=DISABLED)
		else:
			lblError.config(text=self.Cliente.hostname + "/"+str(self.Cliente.port))	
			lblError.config(foreground="green")
		

		self.raiz.mainloop()


r = Registro()
