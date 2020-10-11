#
#	En este script creamos la ventana de nuestro juego
#						y
#	creamos nuestro jugador y le damos movimiento
#
#			Creador: Mundo Python
#
#			youtube: Mundo Python
#
#

import pygame, random


WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def dedoscamp():
		cap = cv2.VideoCapture(0)
		bg = None

		while True:
			ret, frame = cap.read()
			if ret == False:
				break

			# Redimensionar la imagen para que tenga un ancho de 640
			frame = imutils.resize(frame, width=640)
			frame = cv2.flip(frame, 1)
			frameAux = frame.copy()

			if bg is not None:

				# Determinar la región de interés
				ROI = frame[50:300, 380:600]
				cv2.rectangle(frame, (380-2, 50-2), (600+2, 300+2), color_dedos, 1)
				grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)

				# Región de interés del fondo de la imagen
				bgROI = bg[50:300, 380:600]

				# Determinar la imagen binaria (background vs foreground)
				dif = cv2.absdiff(grayROI, bgROI)
				_, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
				th = cv2.medianBlur(th, 7)

				# Encontrando los contornos de la imagen binaria
				cnts, _ = cv2.findContours(
					th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

				for cnt in cnts:

					# Encontrar el centro del contorno
					M = cv2.moments(cnt)
					if M["m00"] == 0:
						M["m00"] = 1
					x = int(M["m10"]/M["m00"])
					y = int(M["m01"]/M["m00"])
					cv2.circle(ROI, tuple([x, y]), 5, (0, 255, 0), -1)

					# Punto más alto del contorno
					ymin = cnt.min(axis=1)
					cv2.circle(ROI, tuple(ymin[0]), 5, color_ymin, -1)

					# Contorno encontrado a través de cv2.convexHull
					hull1 = cv2.convexHull(cnt)
					cv2.drawContours(ROI, [hull1], 0, color_contorno, 2)

					# Defectos convexos
					hull2 = cv2.convexHull(cnt, returnPoints=False)
					defects = cv2.convexityDefects(cnt, hull2)

					# Seguimos con la condición si es que existen defectos convexos
					if defects is not None:

						inicio = []  # Contenedor en donde se almacenarán los puntos iniciales de los defectos convexos
						fin = []  # Contenedor en donde se almacenarán los puntos finales de los defectos convexos
						dedos = 0  # Contador para el número de dedos levantados

						for i in range(defects.shape[0]):

							s, e, f, d = defects[i, 0]
							start = cnt[s][0]
							end = cnt[e][0]
							far = cnt[f][0]

							# Encontrar el triángulo asociado a cada defecto convexo para determinar ángulo
							a = np.linalg.norm(far-end)
							b = np.linalg.norm(far-start)
							c = np.linalg.norm(start-end)

							angulo = np.arccos(
								(np.power(a, 2)+np.power(b, 2)-np.power(c, 2))/(2*a*b))
							angulo = np.degrees(angulo)
							angulo = int(angulo)

							# Se descartarán los defectos convexos encontrados de acuerdo a la distnacia
							# entre los puntos inicial, final y más alelago, por el ángulo y d
							if np.linalg.norm(start-end) > 20 and angulo < 90 and d > 12000:

								# Almacenamos todos los puntos iniciales y finales que han sido
								# obtenidos
								inicio.append(start)
								fin.append(end)

								# Visualización de distintos datos obtenidos

								cv2.circle(ROI, tuple(start), 5, color_comienzo, 2)
								cv2.circle(ROI, tuple(end), 5, color_terminacion, 2)
								cv2.circle(ROI, tuple(far), 7, color_far, -1)

						# Si no se han almacenado puntos de inicio (o fin), puede tratarse de
						# 0 dedos levantados o 1 dedo levantado
						if len(inicio) == 0:
							minY = np.linalg.norm(ymin[0]-[x, y])
							if minY >= 110:
								dedos = dedos + 1
								cv2.putText(ROI, '{}'.format(dedos), tuple(
									ymin[0]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)

						# Si se han almacenado puntos de inicio, se contará el número de dedos levantados
						for i in range(len(inicio)):
							dedos = dedos + 1
							cv2.putText(ROI, '{}'.format(dedos), tuple(
								inicio[i]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)
							if i == len(inicio)-1:
								dedos = dedos + 1
								cv2.putText(ROI, '{}'.format(dedos), tuple(
									fin[i]), 1, 1.7, (color_dedos), 1, cv2.LINE_AA)

						# Se visualiza el número de dedos levantados en el rectángulo izquierdo
						cv2.putText(frame, '{}'.format(dedos), (390, 45),
									1, 4, (color_dedos), 2, cv2.LINE_AA)

						if dedos != 0:
							if dedos == 1:
								rigth = True
								left = False
								down = False
								up = False
								action = False
							if dedos == 2:
								rigth = False
								left = True
								down = False
								up = False
								action = False
							if dedos == 3:
								rigth = False
								left = False
								down = True
								up = False
								action = False
							if dedos == 4:
								rigth = False
								left = False
								down = False
								up = True
								action = False
							if dedos == 5:
								rigth = False
								left = False
								down = False
								up = False
								action = True

						print(rigth)
						print(left)
						print(down)
						print(up)
						print(action)
				cv2.imshow('th', th)
			cv2.imshow('Frame', frame)

			k = cv2.waitKey(20)
			if k == ord('i'):
				bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
			if k == 27:
				break
		cap.release()
		cv2.destroyAllWindows()


all_sprites = pygame.sprite.Group()


player = Player()
all_sprites.add(player)


# Game Loop
running = True
while running:
	# Keep loop running at the right speed
	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		

	# Update
	all_sprites.update()

	#Draw / Render
	screen.fill(BLACK)
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display.
	pygame.display.flip()


pygame.quit()
