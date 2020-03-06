import pygame,sys
import os
from pygame.locals import*
import ctypes
import threading

class Principal():
	def __init__(self, cliente, rival, root, username, turno):
		pygame.init()
		user32 = ctypes.windll.user32
		user32.SetProcessDPIAware()
		ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		self.ventana =pygame.display.set_mode((user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))) 
		pygame.display.set_caption(rival)
		centro= (((ancho))/2, (alto)/2)
		self.rival = rival
		self.username = username
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % centro
		self.Null = pygame.image.load("imagenes/Null.png")
		self.barco = pygame.image.load("imagenes/barco.png")
		self.submarino =pygame.image.load("imagenes/submarino.png")
		self.pego	 = pygame.image.load("imagenes/pego.png")
		self.nopego =  pygame.image.load("imagenes/nopego.png")
		self.disparo =  pygame.image.load("imagenes/disparo.png")


		self.raiz = root
		self.mensaje = "esperando"
		self.Matriz1=[]
		self.Matriz2=[]
		self.MatrizOponente2=[]
		self.MatrizOponente1=[]
		
		self.rMatrizOponente2=[]
		self.rMatrizOponente1=[]

		self.turno = turno
		self.Comenzar = False
		self.cantBarcos = 10
		self.Cliente = cliente
		

		
		for i in range (10):
			self.Matriz1.append([])
			self.Matriz2.append([])
			self.MatrizOponente1.append([])
			self.MatrizOponente2.append([])
			

			self.rMatrizOponente1.append([])
			self.rMatrizOponente2.append([])
			for j in range (10):
				self.Matriz1[i].append(None)
				self.Matriz2[i].append(None)
				self.MatrizOponente1[i].append(None)
				self.MatrizOponente2[i].append(None)

				self.rMatrizOponente1[i].append(None)
				self.rMatrizOponente2[i].append(None)
		
				
		for i in range(10):
			for j in range(10):
				self.rMatrizOponente1[i][j] = pygame.Rect(j*28 + 660  ,i*28+150, 28, 28)
				self.rMatrizOponente2[i][j] = pygame.Rect(j*28 + 960   ,i*28+150, 28, 28)

		
		self.mouseRect = None
		
		self.b5 = pygame.Rect(50,460,28,140)
		self.im_b5 = pygame.image.load("imagenes/b5.png")
		self.b4 = pygame.Rect(100,460,28,112)
		self.im_b4 = pygame.image.load("imagenes/b4.png")
		self.b31 = pygame.Rect(150,460,28,84)
		self.im_b31 = pygame.image.load("imagenes/b3.png")
		self.b32 = pygame.Rect(200,460,28,84)
		self.im_b32 = pygame.image.load("imagenes/b3.png")
		self.b2 = pygame.Rect(250,460,28,56)
		self.im_b2 = pygame.image.load("imagenes/b2.png")
		self.barcoSeleccionado=None


		self.s5 = pygame.Rect(300+50,460,28,140)
		self.im_s5 = pygame.image.load("imagenes/s5.png")
		self.s4 = pygame.Rect(300+100,460,28,112)
		self.im_s4 = pygame.image.load("imagenes/s4.png")
		self.s31 = pygame.Rect(300+150,460,28,84)
		self.im_s31 = pygame.image.load("imagenes/s3.png")
		self.s32 = pygame.Rect(300+200,460,28,84)
		self.im_s32 = pygame.image.load("imagenes/s3.png")
		self.s2 = pygame.Rect(300+250,460,28,56)
		self.im_s2 = pygame.image.load("imagenes/s2.png")
		self.SubmarinoSeleccionado=None


		self.Ships=[]
		self.Ships.append(self.b5)
		self.Ships.append(self.b4)
		self.Ships.append(self.b31)
		self.Ships.append(self.b32)
		self.Ships.append(self.b2)

		self.Submarines=[]
		self.Submarines.append(self.s5)
		self.Submarines.append(self.s4)
		self.Submarines.append(self.s31)
		self.Submarines.append(self.s32)
		self.Submarines.append(self.s2)

		self.Naval = self.Ships + self.Submarines

	
		self.isDraging =  None
		self.inicial = None

		self.dragg = False
		self.iniciar()
	def PasarMatrizAPlano(self, matriz):
		plano =""

		for i in range (10):
			for j in range (10):
				val = matriz[i][j]
				if val == None:
					val = "1"
					
				plano = plano + val
			plano = plano + "f"
		return plano

	def pintarSubmarinos(self):
		if self.im_s5 != None:
			self.ventana.blit(self.im_s5, (self.s5[0], self.s5[1]))
		if self.im_s4 != None:
			self.ventana.blit(self.im_s4, (self.s4[0], self.s4[1]))
		if self.im_s31 != None:
			self.ventana.blit(self.im_s31, (self.s31[0], self.s31[1]))
		if self.im_s32 != None:
			self.ventana.blit(self.im_s32, (self.s32[0], self.s32[1]))
		if self.im_s2 != None:
			self.ventana.blit(self.im_s2, (self.s2[0], self.s2[1]))
	def pintarBarcos(self):
			if self.im_b5 != None:
				self.ventana.blit(self.im_b5, (self.Ships[0][0], self.Ships[0][1]))
			if self.im_b4 != None:
				self.ventana.blit(self.im_b4, (self.Ships[1][0], self.Ships[1][1]))
			if self.im_b31 != None:
				self.ventana.blit(self.im_b31, (self.Ships[2][0], self.Ships[2][1]))
			if self.im_b32 != None:
				self.ventana.blit(self.im_b32, (self.Ships[3][0], self.Ships[3][1]))
			if self.im_b2 != None:
				self.ventana.blit(self.im_b2, (self.Ships[4][0], self.Ships[4][1]))
	def obtenerRespuesta(self):
		fontMensajes = pygame.font.SysFont('Cosole', 20)
		while True:
			
			if self.Cliente != None:
				command = self.Cliente.recv(1024).decode("UTF-8")
				if command != None:
					subCommand = command[0:4]
					

					if subCommand == "2003":
						pass
					elif subCommand =="9899":
						if self.turno:
							self.mensaje = "Turno: tu turno"
						else:
							self.mensaje = "Turno: Oponente"

					elif subCommand =="2007":
						if len(command) > 5:

							coo = command[5:].split(",")
							x = int(coo[0])
							y = int(coo[1])
							print("2007 ", self.Matriz1[x][y])
							print()
							
							if self.Matriz1[x][y] == None:
								self.Matriz1[x][y] = "2" 
							elif self.Matriz1[x][y] == "0":
								self.Matriz1[x][y] = "3" 

						
					elif subCommand =="3007":
						if len(command) > 5:

							coo = command[5:].split(",")
							x = int(coo[0])
							y = int(coo[1])
							print("3007 ", self.Matriz2[x][y])
							if self.Matriz2[x][y] == None:
								self.Matriz2[x][y] = "2" 
							elif self.Matriz2[x][y] == "0":
								self.Matriz2[x][y] = "3" 
							
						
					elif subCommand == "2004":
						self.turno = True
						self.mensaje = "Turno: tu turno"
						if len(command) > 5:
							coo = command[5:].split(",")
							x = int(coo[0])
							y = int(coo[1])
							print("para 2004",self.Matriz1[x][y])
							if self.Matriz1[x][y] == None:
								self.Matriz1[x][y] = "2" 
							elif self.Matriz1[x][y] == "0":
								self.Matriz1[x][y] = "3" 
							print("x,y",x,y )
					elif subCommand == "3004":
						self.turno = True
						print("entra a 3004")
						self.mensaje = "Turno: tu turno"
						if len(command) > 5:
							coo = command[5:].split(",")
							x = int(coo[0])
							y = int(coo[1])

							if self.Matriz2[x][y] == None:
								self.Matriz2[x][y] = "2" 
							elif self.Matriz2[x][y] == "0":
								self.Matriz2[x][y] = "3" 
						
					elif subCommand == "2006":
						self.mensaje = "Turno: Oponente"
						self.turno = False
					elif subCommand =="1111":
						self.mensaje= "YOU WIN"
						self.acabo = True
					elif subCommand =="-111":
						self.mensaje = "YOU LOSE"
						self.acabo = True

					

			
	def  pintarOponente(self):
			
		for i in range(10):
			for j in range(10):

				x1,y1=self.rMatrizOponente1[i][j].x, self.rMatrizOponente1[i][j].y
				x2,y2=self.rMatrizOponente2[i][j].x, self.rMatrizOponente2[i][j].y

				if self.MatrizOponente1[i][j] == None :
					self.ventana.blit(self.Null, (x1,y1))
				elif self.MatrizOponente1[i][j] == "1":
					self.ventana.blit(self.pego, (x1,y1))
				elif self.MatrizOponente1[i][j] == "2":
					self.ventana.blit(self.pego, (x1,y1))
				elif self.MatrizOponente1[i][j] == "3":
					self.ventana.blit(self.nopego, (x1,y1))
				elif self.MatrizOponente1[i][j] == "0":
					self.ventana.blit(self.barco, (x1,y1))
				elif self.MatrizOponente1[i][j] == "4":
					self.ventana.blit(self.disparo, (x1,y1))
				
				if self.MatrizOponente2[i][j] == None :
					self.ventana.blit(self.Null, (x2,y1))
				elif self.MatrizOponente2[i][j] == "1":
					self.ventana.blit(self.pego, (x2,y2))
				elif self.MatrizOponente2[i][j] == "2":
					self.ventana.blit(self.pego, (x2,y2))
				elif self.MatrizOponente2[i][j] == "3":
					self.ventana.blit(self.nopego, (x2,y2))
				elif self.MatrizOponente2[i][j] == "0":
					self.ventana.blit(self.barco, (x2,y2))
				elif self.MatrizOponente2[i][j] == "4":
					self.ventana.blit(self.disparo, (x2,y2))
				
				"""if self.MatrizOponente2[i][j] == None:
					self.ventana.blit(self.Null, (x2,y2))
				elif self.MatrizOponente2[i][j] == "1":
					self.ventana.blit(self.pego, (x2,y2))
				elif self.MatrizOponente2[i][j] == "2":
					self.ventana.blit(self.submarino, (x2,y2))"""
	
	def pintarMatriz (self):
		for i in range(10):
			for j in range(10):
				if self.Matriz1[i][j] == None :
					self.ventana.blit(self.Null, (j*28+30,i*28+150))
				elif self.Matriz1[i][j] == "0":
					self.ventana.blit(self.barco, (j*28+30,i*28+150))
				elif self.Matriz1[i][j] == "2":
					self.ventana.blit(self.nopego, (j*28+30,i*28+150))
				elif self.Matriz1[i][j] == "3":
					self.ventana.blit(self.pego, (j*28+30,i*28+150))
				elif self.Matriz1[i][j] == "1":
					self.ventana.blit(self.Null, (j*28+30,i*28+150))
				elif self.Matriz1[i][j] == "4":
					self.ventana.blit(self.disparo, (j*28+30,i*28+150))

				if self.Matriz2[i][j] == None :
					self.ventana.blit(self.Null, (j*28+30+300,i*28+150))
				elif self.Matriz2[i][j] == "0":
					self.ventana.blit(self.submarino, (j*28+30+300,i*28+150))
				elif self.Matriz2[i][j] == "2":
					self.ventana.blit(self.nopego, (j*28+30+300,i*28+150))
				elif self.Matriz2[i][j] == "3":
					self.ventana.blit(self.pego, (j*28+30+300,i*28+150))
				elif self.Matriz2[i][j] == "1":
					self.ventana.blit(self.Null, (j*28+30+300,i*28+150))
				elif self.Matriz2[i][j] == "4":
					self.ventana.blit(self.disparo, (j*28+30+300,i*28+150))

	def mostrar(self):
		text = ""
		
		for i in range (10):	
			for j in range (10):
				if self.Matriz1[i][j]== None:
					text = text+"-"		
				else:
					text = text+self.Matriz1[i][j]	
			text = text +"\n"		
		print(text)	
	def iniciar(self):
		thread = threading.Thread(name="obtenerRespuesta", target=self.obtenerRespuesta)
		thread.start()
		fontMensajes = pygame.font.SysFont('Cosole', 20)
		while(True):
			self.mouseRect = pygame.Rect(pygame.mouse.get_pos()[0]-3,pygame.mouse.get_pos()[1]-3,6,6)

			self.ventana.fill((153,217,234))	
			textsurface = fontMensajes.render(self.mensaje, False, (0,0,0))
			self.ventana.blit(textsurface,(50,50))
			for evento in pygame.event.get():
				if evento.type == QUIT:
					self.raiz.destroy()
					pygame.quit()
					sys.exit()
					self.Cliente.close()
				elif evento.type == pygame.MOUSEBUTTONDOWN :
					encontro = False
					if  evento.button ==1:	
						for i in self.Naval:
							if self.mouseRect.colliderect(i):
								self.barcoSeleccionado = i
								self.SubmarinoSeleccionado = i
								self.dragg = True
						
						if self.turno and self.Comenzar:
							colocoB = True
							for i in range(10):
								for j in range(10):
									if colocoB and not encontro and self.mouseRect.colliderect(self.rMatrizOponente1[i][j]) and self.MatrizOponente1[i][j] != "2":
										if self.MatrizOponente1[i][j] == None or  self.MatrizOponente1[i][j] == "1":
											self.MatrizOponente1[i][j] = "4"
										else:
											self.MatrizOponente1[i][j] = "4"
										coordenada = (str(i) + "," + str(j));
										msg= ("SHIPATTACK " + coordenada+"\n").encode("UTF-8")
										self.Cliente.send(msg)
										colocoB = False
										#print(self.turno , self.Comenzar)
							for i in range(10):
								for j in range(10):
									if colocoB and not encontro and self.mouseRect.colliderect(self.rMatrizOponente2[i][j]) and self.MatrizOponente2[i][j] != "2":
										if self.MatrizOponente2[i][j] == None or  self.MatrizOponente2[i][j] == "1":
											self.MatrizOponente2[i][j] = "4"
										else:
											self.MatrizOponente2[i][j] = "4"
										coordenada = (str(i) + "," + str(j));
										msg= ("SUBATTACK " + coordenada+"\n").encode("UTF-8")
										self.Cliente.send(msg)
										print(msg)
										colocoB = False
										#print(self.turno , self.Comenzar)			

					elif  evento.button ==3:	
						for i in self.Naval:
							if self.mouseRect.colliderect(i):
								aux = i[2]
								i[2] = i[3]
								i[3] = aux
								if i[2]>i[3]:
									if i == self.Ships[0]:
										self.im_b5=pygame.image.load("imagenes/b51.png")
									elif  i == self.Ships[1]:
										self.im_b4=pygame.image.load("imagenes/b41.png")
									elif  i == self.Ships[2]:
										self.im_b31=pygame.image.load("imagenes/b31.png")
									elif  i == self.Ships[3]:
										self.im_b32=pygame.image.load("imagenes/b31.png")
									elif  i == self.Ships[4]:
										self.im_b2=pygame.image.load("imagenes/b21.png")

									elif i == self.Submarines[0]:
										self.im_s5=pygame.image.load("imagenes/s51.png")
									elif  i == self.Submarines[1]:
										self.im_s4=pygame.image.load("imagenes/s41.png")
									elif  i == self.Submarines[2]:
										self.im_s31=pygame.image.load("imagenes/s31.png")
									elif  i == self.Submarines[3]:
										self.im_s32=pygame.image.load("imagenes/s31.png")
									elif  i == self.Submarines[4]:
										self.im_s2=pygame.image.load("imagenes/s21.png")

								else:	
									if i == self.Ships[0]:
										self.im_b5=pygame.image.load("imagenes/b5.png")
									elif  i == self.Ships[1]:
										self.im_b4=pygame.image.load("imagenes/b4.png")
									elif  i == self.Ships[2]:
										self.im_b31=pygame.image.load("imagenes/b3.png")
									elif  i == self.Ships[3]:
										self.im_b32=pygame.image.load("imagenes/b3.png")
									elif  i == self.Ships[4]:
										self.im_b2=pygame.image.load("imagenes/b2.png")
									elif i == self.Submarines[0]:
										self.im_s5=pygame.image.load("imagenes/s5.png")
									elif  i == self.Submarines[1]:
										self.im_s4=pygame.image.load("imagenes/s4.png")
									elif  i == self.Submarines[2]:
										self.im_s31=pygame.image.load("imagenes/s3.png")
									elif  i == self.Submarines[3]:
										self.im_s32=pygame.image.load("imagenes/s3.png")
									elif  i == self.Submarines[4]:
										self.im_s2=pygame.image.load("imagenes/s2.png")		
				elif evento.type == pygame.MOUSEBUTTONUP:
					if evento.button == 1:      
						x,y = (int((self.mouseRect.y - 150)/28 ),int ((self.mouseRect.x - 28)/28))  
						turno = True   
						self.dragg = False
						if x>=0 and x<=9 and y>=0 and y<=9 :
							#Barco5
							if self.barcoSeleccionado == self.Ships[0] and self.Ships[0] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Ships[0][2]>self.Ships[0][3]:
									if y + 5 <=9:
										for i in range (y , y+5):
											self.Matriz1[x][i]="0"
										self.barcoSeleccionado= None
										self.im_b5 = None
										self.Ships[0]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[0]  = pygame.Rect(50,460,28,140)
										self.im_b5 = pygame.image.load("imagenes/b5.png")
								else:
									if x + 5 <=9:
										for i in range (x , x+5):
											self.Matriz1[i][y]="0"
										self.barcoSeleccionado= None
										self.im_b5 = None
										self.Ships[0]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[0] = pygame.Rect(50,460,28,140)
										self.im_b5 = pygame.image.load("imagenes/b5.png")

										
							#Barco 4
							elif self.barcoSeleccionado == self.Ships[1] and self.Ships[1] != None:
								self.cantBarcos=self.cantBarcos - 1

								if self.Ships[1][2]>self.Ships[1][3]:
									if y + 4 <=9:
										for i in range (y , y+5):
											self.Matriz1[x][i]="0"
										self.barcoSeleccionado= None
										self.im_b4 = None
										self.Ships[1]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[1]  = pygame.Rect(100,460,28,140)
										self.im_b4 = pygame.image.load("imagenes/b4.png")
								else:
									if x + 4 <=9:
										for i in range (x , x+4):
											self.Matriz1[i][y]="0"
										self.barcoSeleccionado= None
										self.im_b4 = None
										self.Ships[1]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[1] = pygame.Rect(100,460,28,140)
										#self.b5 = pygame.Rect(50,460,28,140)
										self.im_b4 = pygame.image.load("imagenes/b4.png")

							#Barco 31
							elif self.barcoSeleccionado == self.Ships[2] and self.Ships[2] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Ships[2][2]>self.Ships[2][3]:
									if y + 3 <=9:
										for i in range (y , y+3):
											self.Matriz1[x][i]="0"
										self.barcoSeleccionado= None
										self.im_b31 = None
										self.Ships[2]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[1]  = pygame.Rect(150,460,28,140)
										self.im_b31 = pygame.image.load("imagenes/b3.png")
								else:
									if x + 3 <=9:
										for i in range (x , x+3):
											self.Matriz1[i][y]="0"
										self.barcoSeleccionado= None
										self.im_b31 = None
										self.Ships[2]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[2] = pygame.Rect(150,460,28,140)
										self.im_b31 = pygame.image.load("imagenes/b3.png")
					
							#Barco 32
							elif self.barcoSeleccionado == self.Ships[3] and self.Ships[3] != None:
								self.cantBarcos=self.cantBarcos - 1

								if self.Ships[3][2]>self.Ships[3][3]:
									if y + 3 <=9:
										for i in range (y , y+3):
											self.Matriz1[x][i]="0"
										self.barcoSeleccionado= None
										self.im_b32 = None
										self.Ships[3]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[3]  = pygame.Rect(150,460,28,140)
										self.im_b32 = pygame.image.load("imagenes/b3.png")
								else:
									if x + 3 <=9:
										for i in range (x , x+3):
											self.Matriz1[i][y]="0"
										self.barcoSeleccionado= None
										self.im_b32 = None
										self.Ships[3]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[3] = pygame.Rect(200,460,28,140)
										self.im_b32 = pygame.image.load("imagenes/b3.png")
					
							#Barco 2
							elif self.barcoSeleccionado == self.Ships[4] and self.Ships[4] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Ships[4][2]>self.Ships[4][3]:
									if y + 2 <=9:
										for i in range (y , y+2):
											self.Matriz1[x][i]="0"
										self.barcoSeleccionado= None
										self.im_b2 = None
										self.Ships[4]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[4]  = pygame.Rect(250,460,28,140)
										self.im_b2 = pygame.image.load("imagenes/b2.png")
								else:
									if x + 2 <=9:
										for i in range (x , x+2):
											self.Matriz1[i][y]="0"
										self.barcoSeleccionado= None
										self.im_b2 = None
										self.Ships[4]  = None
									else:
										self.barcoSeleccionado= None
										self.Ships[4] = pygame.Rect(250,460,28,140)
										self.im_b2 = pygame.image.load("imagenes/b2.png")
						else:
							if y>=11 and y <=20 :
								y = y - 11


						#Submarine 5
							if self.SubmarinoSeleccionado == self.Submarines[0] and self.Submarines[0] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Submarines[0][2]>self.Submarines[0][3]:
									if y + 5 <=9:
										for i in range (y , y+5):
											self.Matriz2[x][i]="0"
										self.SubmarinoSeleccionado= None
										self.im_s5 = None
										self.Submarines[0]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[0]  = pygame.Rect(300+50,460,28,140)
										self.im_s5 = pygame.image.load("imagenes/s5.png")
								else:
									if x + 5 <=9:
										for i in range (x , x+5):
											self.Matriz2[i][y]="0"
										self.SubmarinoSeleccionado= None
										self.im_s5 = None
										self.Submarines[0]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[0] = pygame.Rect(300+50,460,28,140)
										self.im_s5 = pygame.image.load("imagenes/s5.png")

										
							#Submarine  4
							elif self.SubmarinoSeleccionado == self.Submarines[1] and self.Submarines[1] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Submarines[1][2]>self.Submarines[1][3]:
									if y + 4 <=9:
										for i in range (y , y+5):
											self.Matriz2[x][i]="0"
										self.SubmarinoSeleccionado= None
										self.im_s4 = None
										self.Submarines[1]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[1]  = pygame.Rect(300+100,460,28,140)
										self.im_s4 = pygame.image.load("imagenes/s4.png")
								else:
									if x + 4 <=9:
										for i in range (x , x+4):
											self.Matriz2[i][y]="0"
										self.SubmarinoSeleccionado= None
										self.im_s4 = None
										self.Submarines[1]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[1] = pygame.Rect(300+100,460,28,140)
										#self.b5 = pygame.Rect(50,460,28,140)
										self.im_s4 = pygame.image.load("imagenes/s4.png")

							#Submarine  31
							elif self.SubmarinoSeleccionado == self.Submarines[2] and self.Submarines[2] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Submarines[2][2]>self.Submarines[2][3]:
									if y + 3 <=9:
										for i in range (y , y+3):
											self.Matriz2[x][i]="0"
										self.SubmarinoSeleccionado= None
										self.im_s31 = None
										self.Submarines[2]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[1]  = pygame.Rect(300+150,460,28,140)
										self.im_s31 = pygame.image.load("imagenes/s3.png")
								else:
									if x + 3 <=9:
										for i in range (x , x+3):
											self.Matriz2[i][y]="0"
										self.SubmarinoSeleccionado= None
										self.im_s31 = None
										self.Submarines[2]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[2] = pygame.Rect(300+150,460,28,140)
										self.im_s31 = pygame.image.load("imagenes/s3.png")
					
							#Submarine  32
							elif self.SubmarinoSeleccionado == self.Submarines[3] and self.Submarines[3] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Submarines[3][2]>self.Submarines[3][3]:
									if y + 3 <=9:
										for i in range (y , y+3):
											self.Matriz2[x][i]="0"
										self.SubmarinoSeleccionado= None
										self.im_s32 = None
										self.Submarines[3]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[3]  = pygame.Rect(300+150,460,28,140)
										self.im_s32 = pygame.image.load("imagenes/s3.png")
								else:
									if x + 3 <=9:
										for i in range (x , x+3):
											self.Matriz2[i][y]="0"
										self.SubmarinoSeleccionado= None
										self.im_s32 = None
										self.Submarines[3]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[3] = pygame.Rect(300+200,460,28,140)
										self.im_s32 = pygame.image.load("imagenes/s3.png")
					
							#Submarine  2
							elif self.SubmarinoSeleccionado == self.Submarines[4] and self.Submarines[4] != None:
								self.cantBarcos=self.cantBarcos - 1
								if self.Submarines[4][2]>self.Submarines[4][3]:
									if y + 2 <=9:
										for i in range (y , y+2):
											self.Matriz2[x][i]="0"
										self.SubmarinoSeleccionado= None
										self.im_s2 = None
										self.Submarines[4]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[4]  = pygame.Rect(300+250,460,28,140)
										self.im_s2 = pygame.image.load("imagenes/s2.png")
								else:
									if x + 2 <=9:
										for i in range (x , x+2):
											self.Matriz2[i][y]="0"
										self.SubmarinoSeleccionado= None
										self.im_s2 = None
										self.Submarines[4]  = None
									else:
										self.SubmarinoSeleccionado= None
										self.Submarines[4] = pygame.Rect(300+250,460,28,140)
										self.im_s2 = pygame.image.load("imagenes/s2.png")
				elif evento.type == pygame.MOUSEMOTION:

					if self.dragg:	
						if self.barcoSeleccionado == self.Ships[0]:
							self.Ships[0] .x = self.mouseRect.x
							self.Ships[0] .y = self.mouseRect.y
							self.barcoSeleccionado= self.Ships[0]
						elif self.barcoSeleccionado == self.Ships[1]:
							self.Ships[1] .x = self.mouseRect.x
							self.Ships[1] .y = self.mouseRect.y
							self.barcoSeleccionado= self.Ships[1]
						elif self.barcoSeleccionado == self.Ships[2]:
							self.Ships[2] .x = self.mouseRect.x
							self.Ships[2] .y = self.mouseRect.y
							self.barcoSeleccionado= self.Ships[2]
						elif self.barcoSeleccionado == self.Ships[3]:
							self.Ships[3] .x = self.mouseRect.x
							self.Ships[3] .y = self.mouseRect.y
							self.barcoSeleccionado= self.Ships[3]
						elif self.barcoSeleccionado == self.Ships[4]:
							self.Ships[4] .x = self.mouseRect.x
							self.Ships[4] .y = self.mouseRect.y
							self.barcoSeleccionado= self.Ships[4]
						if self.SubmarinoSeleccionado == self.Submarines[0]:
							self.Submarines[0] .x = self.mouseRect.x
							self.Submarines[0] .y = self.mouseRect.y
							self.SubmarinoSeleccionado= self.Submarines[0]
						elif self.SubmarinoSeleccionado == self.Submarines[1]:
							self.Submarines[1] .x = self.mouseRect.x
							self.Submarines[1] .y = self.mouseRect.y
							self.SubmarinoSeleccionado= self.Submarines[1]
						elif self.SubmarinoSeleccionado == self.Submarines[2]:
							self.Submarines[2] .x = self.mouseRect.x
							self.Submarines[2] .y = self.mouseRect.y
							self.SubmarinoSeleccionado= self.Submarines[2]
						elif self.SubmarinoSeleccionado == self.Submarines[3]:
							self.Submarines[3] .x = self.mouseRect.x
							self.Submarines[3] .y = self.mouseRect.y
							self.SubmarinoSeleccionado= self.Submarines[3]
						elif self.SubmarinoSeleccionado == self.Submarines[4]:
							self.Submarines[4] .x = self.mouseRect.x
							self.Submarines[4] .y = self.mouseRect.y
							self.SubmarinoSeleccionado= self.Submarines[4]
			self.pintarMatriz()	
			self.pintarOponente()
			self.pintarBarcos()
			self.pintarSubmarinos()
			#self.obtenerRespuesta()

			#print(self.turno , self.Comenzar)
			if self.cantBarcos ==0:

				ship = self.PasarMatrizAPlano(self.Matriz1)
				subs = self.PasarMatrizAPlano(self.Matriz2)
				print(ship)
				print()
				print(self.Matriz1)
				msg= ("SENDSHIP " + ship+"\n").encode("UTF-8")
				self.Cliente.send(msg)
				msg= ("SENDSUBB " + subs+"\n").encode("UTF-8")
				self.Cliente.send(msg)
				self.Comenzar = True
				self.cantBarcos =-1
			pygame.display.update()

