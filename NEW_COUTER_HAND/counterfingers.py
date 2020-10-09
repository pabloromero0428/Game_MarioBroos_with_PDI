import cv2
import numpy as np
import imutils

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture("videoEntrada.mp4")
bg = None

# COLORES PARA VISUALIZACIÓN
color_start = (204,204,0)
color_end = (204,0,204)
color_far = (255,0,0)

color_start_far = (204,204,0)
color_far_end = (204,0,204)
color_start_end = (0,255,255)

color_contorno = (0,255,0)
color_ymin = (0,130,255) # Punto más alto del contorno
#color_angulo = (0,255,255)
#color_d = (0,255,255)
color_fingers = (0,255,255)

rigth = False
left = False
down = False
up = False
action= False


while True:
    ret, frame = cap.read()
    if ret == False: break

    frame = imutils.resize(frame, width=640)
    frame = cv2.flip(frame,1)
    frameAux = frame.copy()

    if bg is not None:
        cv2.imshow('bg', bg)

        # Determinar la región de interés en la cual se pondra la mano
        ROI = frame[50:300,380:600]
        cv2.rectangle(frame,(380-2,50-2),(600+2,300+2), color_fingers,1)
        grayROI =cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY) #primer plano en escala de grises
        
        # Región de interés del fondo de la imagen
        bgROI = bg[50:300,380:600] #fondo en escala de grises

        # Determinar la imagen binaria (background vs foreground)
        dif = cv2.absdiff(grayROI,bgROI) #la resta de el 
        _,th = cv2.threshold(dif,30,255, cv2.THRESH_BINARY) #imagen binarisada
        th = cv2.medianBlur(th,7) # sin cortes en la mano 

	    # Encontrando los contornos de la imagen binaria
        cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #obtenemos los contornos
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1] #ordenamos los contornos optenidos

        #Encontrar el centro del contorno 
        for cnt in cnts:
            M= cv2.moments(cnt)
            if M["m00"] == 0: M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(ROI,tuple([x,y]),5,(0,255,0),-1)

            # Punto más alto del contorno
            ymin = cnt.min(axis=1)
            cv2.circle(ROI,tuple(ymin[0]),5,color_ymin,-1)

            # Contorno encontrado a través de cv2.convexHull
            hull1 = cv2.convexHull(cnt)
            cv2.drawContours(ROI,[hull1],0,color_contorno,2)

            # Defectos convexos
            hull2 = cv2.convexHull(cnt,returnPoints=False)
            defects = cv2.convexityDefects(cnt,hull2)

            if defects is not None:

                inicio = []
                fin = []
                finger = []

                for i in range(defects.shape[0]):

                    s,e,f,d = defects[i,0]
                    start = cnt[s][0]
                    end = cnt[e][0]
                    far = cnt[f][0]

                    a = np.linalg.norm(far-end)
                    b = np.linalg.norm(far-start)
                    c = np.linalg.norm(start-end)

                    angulo = np.arccos((np.power(a,2)+np.power(b,2)-np.power(c,2))/(2*a*b))
                    angulo = np.degrees(angulo)
                    angulo = int(angulo)

                    if np.linalg.norm(start-end) > 20 and angulo < 90 and d > 12000:

                        inicio.append(start)
                        fin.append(end)

                        cv2.circle(ROI,tuple(start),5,color_start,2)
                        cv2.circle(ROI,tuple(end),5,color_end,2)
                        cv2.circle(ROI,tuple(far),7,color_far,-1)




        
        cv2.imshow('dif', dif)
        cv2.imshow('th', th)

    cv2.imshow('Frame', frame)

    k= cv2.waitKey(20)

    if k == ord("i"):
        bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

        
