#-----------------------------------------------------------------------------------#
#-------------------PLANTIALLA DE CODIGO--------------------------------------------#
#-------------------PROGRAMA SHOTER_GAME_PDI----------------------------------------#
#-------------------POR: -----------------------------------------------------------#
#-------------------Natalia Perez Enamorado-- CC ------------------------------------------------------------#
#-------------------Juan Pablo Romero Laverde-- CC 1128463855-----------------------#
#-------------------CURSO: PROCESAMIENTO DIGITAL DE IMAGENES------------------------#
#-----------------------------------------------------------------------------------#
import pygame, random
import cv2
import numpy as np
import imutils
import threading
import win32com.client 
 
#-------------------------------------------------------------------#
#-------------1. Inicialización de varibales globales---------------#
#-------------------------------------------------------------------#

# Se inicializan los colores para la vizualización
color_comienzo = (204, 204, 0)
color_terminacion = (204, 0, 204)
color_far = (255, 0, 0)

color_comienzo_far = (204, 204, 0)
color_far_terminacion = (204, 0, 204)
color_comienzo_end = (0, 255, 255)

color_contorno = (0, 255, 0) # Color del contorno general 
color_ymin = (0, 130, 255)  # Color del punto más alto del contorno
color_dedos = (0, 255, 255) # Color de los dedos 

cap = cv2.VideoCapture(0)
Shell =  win32com.client.Dispatch("WScript.Shell")

der = False
izq = False
disparo = False

WIDTH = 800 #Tamaño de la ventana del juego Largo ancho
HEIGHT = 600 #Tamaño de la ventana del juego 
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

#-------------------------------------------------------------------#
#----------------------1. Metodos del sistema ----------------------#
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
#-------------------1.1 Metodo propio del juego---------------------#
#-------------------------------------------------------------------#

	

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

#-------------------------------------------------------------------------------#
#-------------------1.1 Metodo propio del control del juego---------------------#
#------------------------------------------------------------------------------#
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100

#---En este punto se controla el juego, para reutilizar codigo-----------------#
#---y mejorar la eficiencia del juego se implemnte lo siguiente----------------#
#---si se preciona la tecla izquieda o derecha  O los metodos del--------------#
#---procesamiendo digital de la imagen hacen las variables globales der, izq---#
#---True  entonces la nave se mueve de un lado al otro-------------------------#

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		#Tecla izquierda o variable izq true, la nave se mueve a la izquierda
		if keystate[pygame.K_LEFT] or izq==True:
			self.speed_x = -5
		#Tecla derecha o variable der true, la nave se mueve a la derecha
		if keystate[pygame.K_RIGHT] or der==True:
			self.speed_x = 5
		#Limites de la ventana 
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		#laser_sound.play()

	def dedoscamp():
		bg = None # background o fondo que se utilizara apara tomar la mano que se muestre en la camara
		cap #Se llama la variale global cap que es la captura de camara
		
		while True:
			#inicializacion de camara para que se visualice en pantalla
			ret, frame = cap.read()
			if ret == False:
				break

			# Redimensionar la imagen para que tenga un ancho de 640
			frame = imutils.resize(frame, width=640)
			frame = cv2.flip(frame, 1)
			frameAux = frame.copy()

			if bg is not None:

				# Determinar la región de interés
				VENBINARI = frame[50:300, 380:600] #se crea la ventana binaria 
				cv2.rectangle(frame, (380-2, 50-2), (600+2, 300+2), color_dedos, 1) #rectangulo de interes
				grayVENBINARI = cv2.cvtColor(VENBINARI, cv2.COLOR_BGR2GRAY)

				# Región de interés del fondo de la imagen
				bgVENBINARI = bg[50:300, 380:600]

				# Determinar la imagen binaria (background vs foreground)
				dif = cv2.absdiff(grayVENBINARI, bgVENBINARI) # Realizar la diferencia entre el fondo con foreground para obtener la la imagen de la mano en blanco 
				_, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
				th = cv2.medianBlur(th, 7)

				# Encontrando los contornos de la imagen binaria
				cnts, _ = cv2.findContours(
					th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Guardar los contornos en un arreglo de contornos
				cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1] #Ordenar los contornos encontrados

				for cnt in cnts:

					# Encontrar el centro del contorno de la mano 
					M = cv2.moments(cnt)
					if M["m00"] == 0:
						M["m00"] = 1
					x = int(M["m10"]/M["m00"])
					y = int(M["m01"]/M["m00"])
					cv2.circle(VENBINARI, tuple([x, y]), 5, (0, 255, 0), -1)

					# Encontrar el punto más alto del contorno para tenerlo como referencia 
					ymin = cnt.min(axis=1)
					cv2.circle(VENBINARI, tuple(ymin[0]), 5, color_ymin, -1)

					# Contorno encontrado a través de cv2.convexHull
					hull1 = cv2.convexHull(cnt)
					cv2.drawContours(VENBINARI, [hull1], 0, color_contorno, 2)

					# Se optienen los defectos convexos
					hull2 = cv2.convexHull(cnt, returnPoints=False)
					defects = cv2.convexityDefects(cnt, hull2)

					# Se debe verificar si existen defectos convexos, asi identificaremos si ha dedos levantados  
					if defects is not None:

						inicio = []  # Contenedor en donde se almacenarán los puntos iniciales de los defectos convexos
						fin = []  # Contenedor en donde se almacenarán los puntos finales de los defectos convexos
						dedos = 0  # Contador para el número de dedos levantados

						for i in range(defects.shape[0]):

							s, e, f, d = defects[i, 0]
							start = cnt[s][0]
							end = cnt[e][0]
							far = cnt[f][0]

							# Encontrar el triángulo asociado a cada defecto convexo para determinar ángulo de los dedos y poder identificar de acuerdo a eso si hay dedos levantados
							far_a = np.linalg.norm(far-end)
							far_b = np.linalg.norm(far-start)
							far_c = np.linalg.norm(start-end)

							#Se encuentras los angulos de los defectos convexos
							angulo = np.arccos(
								(np.power(far_a, 2)+np.power(far_b, 2)-np.power(far_c, 2))/(2*far_a*far_b))
							angulo = np.degrees(angulo)
							angulo = int(angulo)

							# Se descartarán los defectos convexos que se encuentren de acuerdo a la distanacia x que hay entre un punto y otro
							# entre los puntos inicial, final y más alelago, por el ángulo y d
							if np.linalg.norm(start-end) > 20 and angulo < 90 and d > 12000:

								# Almacenamos todos los puntos iniciales y finales que han sido
								# obtenidos
								inicio.append(start)
								fin.append(end)

								# Visualización de distintos datos obtenidos

								cv2.circle(VENBINARI, tuple(start), 5, color_comienzo, 2)
								cv2.circle(VENBINARI, tuple(end), 5, color_terminacion, 2)
								cv2.circle(VENBINARI, tuple(far), 7, color_far, -1)

						# Si no se han almacenado puntos de inicio (o fin), puede tratarse de
						# 0 dedos levantados o 1 dedo levantado
						if len(inicio) == 0:
							minY = np.linalg.norm(ymin[0]-[x, y])
							if minY >= 110:
								dedos = dedos + 1
								cv2.putText(VENBINARI, '{}'.format(dedos), tuple(
									ymin[0]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)

						# Si se han almacenado puntos de inicio, se contará el número de dedos levantados en la ventana binaria
						for i in range(len(inicio)):
							dedos = dedos + 1
							cv2.putText(VENBINARI, '{}'.format(dedos), tuple(
								inicio[i]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)
							if i == len(inicio)-1:
								dedos = dedos + 1
								cv2.putText(VENBINARI, '{}'.format(dedos), tuple(
									fin[i]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)

						# Se muestra en panatalla el número de dedos levantados en el rectángulo donde se coloca la mano para identificar los dedos levantados
						cv2.putText(frame, '{}'.format(dedos), (390, 45),
									1, 4, (color_dedos), 2, cv2.LINE_AA)

						#Traer las variables globales del sistema  para realizar cambios en ella 
						global der
						global izq
						global disparo

						#De acuero a la cantidad de dedos levantados se cambian las variables para actualizar el momiento 
						#Estos movimientos estan definidos en el metodo update(self)
						if dedos == 3:							 
							der = True							
							izq = False
							disparo = False

						if dedos == 4:							 
							der = True							
							izq = False
							disparo = True											
							
						if dedos == 2:							 
							der = False
							izq = True
							disparo = False

						if dedos == 1:							 
							der = False
							izq = True
							disparo = True


						if dedos == 0: 
							der = False
							izq = False
							disparo = False

						if dedos == 5:
							disparo = True
							der = False
							izq = False 
							
					
				#Se muesntran las ventanas 		
				cv2.imshow('Ventana Binaria', th)
			cv2.imshow('Frame', frame)

			#Se debe precionar la tecla i para tomar el fondo de la imagen que se restrara con la mano cuando esta 
			#Se ponga en el rectangulo reconocedor
			k = cv2.waitKey(20)
			if k == ord('i'):
				bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
			if k == 27:
				break
		cap.release()
		cv2.destroyAllWindows()
	

#-------------------------------------------------------------------------------#
#-------------------1.2 Hilo de ejecución del sistema---------------------------#
#-------------------------------------------------------------------------------#	
	ThreadMain = threading.Thread(target=dedoscamp)
	ThreadMain.start()

#-------------------------------------------------------------------------------#
#----------------------2. Metodos propios del sistema---------------------------#
#-------------------------------------------------------------------------------#
class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


def show_go_screen():
	screen.blit(background, [0,0])
	draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())


####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)


#pygame.mixer.music.play(loops=-1)
#-------------------------------------------------------------------------------#
#-------------------3. Ejecución del sistema------------------------------------#
#-------------------------------------------------------------------------------#


#### ----------GAME OVER
game_over = True
running = True
while running:
	if game_over:

		show_go_screen()

		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)
		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

		score = 0


	clock.tick(60)

#-----------------------------------------------------------------------------------------------------------------#
#-------------------3.1 Ejecución del disparo deacuero a la variable global del disparo---------------------------#
#-----------------------------------------------------------------------------------------------------------------#

	if disparo==True:
		player.shoot()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()


	all_sprites.update()

	#colisiones - meteoro - laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	# Checar colisiones - jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	# Escudo.
	draw_shield_bar(screen, 5, 5, player.shield)

	pygame.display.flip()

#-------------------------------------------------------------------------------#
#-------------------4. Finalización del programa--------------------------------#
#-------------------------------------------------------------------------------#	
pygame.quit()