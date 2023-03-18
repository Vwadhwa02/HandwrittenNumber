import numpy as np
import pygame,sys
import tensorflow as tf
from pygame.locals import *
from keras.models import load_model
import cv2
WINDOWSIZEX=640
WINDOWSIZEY=480
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,10)
IMAGESAVE=False
BOUN=5
model=load_model("network1.h5")
PREDICT=True




Label={0:'Zero',1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine'}

#intialize 
pygame.init()
DISPLAYSURF=pygame.display.set_mode((WINDOWSIZEX,WINDOWSIZEY))
WHITE_INT=DISPLAYSURF.map_rgb(WHITE)
# white=(255,255,255)
# black=(0,0,0)
# red=(255,0,10)

F=pygame.font.Font("freesansbold.ttf",18)
#FONT=pygame.font.Font("Segoe UI.tfff")
pygame.display.set_mode((WINDOWSIZEX,WINDOWSIZEY))
pygame.display.set_caption("digital board")

iswriting=False

num_xcord=[]
num_ycord=[]


#system loop
while True:
    for ev in pygame.event.get():
        if ev.type==QUIT:
            pygame.quit()
            sys.exit()
        if ev.type==MOUSEMOTION and iswriting:
            (xcord,ycord)=ev.pos
            pygame.draw.circle(DISPLAYSURF,WHITE,(xcord,ycord),4,0)
            num_xcord.append(xcord)
            num_ycord.append(ycord)
        if ev.type==MOUSEBUTTONDOWN:
            iswriting=True
        
        if ev.type==MOUSEBUTTONUP:
            iswriting=False
            num_xcord=sorted(num_xcord)
            num_ycord=sorted(num_ycord)

        #surrounding them
            rect_min_x,rect_max_x=max(num_xcord[0]-BOUN,0),min(WINDOWSIZEX,num_xcord[-1]+BOUN)
            rect_min_y,rect_max_y=max(num_ycord[0]-BOUN,0),min(WINDOWSIZEY,num_ycord[-1]+BOUN)

            num_xcord=[]
            num_ycord=[]

            im_ar=np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x,rect_min_y:rect_max_y].T.astype(np.float32)

            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt +=1
            
            if PREDICT:
                image=cv2.resize(im_ar,(28,28))
                image=np.pad(image,(10,10),constant_values=0)
                image=cv2.resize(image,(28,28))/255
                label=str(Label[np.argmax(model.predict(image.reshape(1,28,28,1)))])

                textsurface=F.render(label,True,RED,WHITE)
                textRec=textsurface.get_rect()
                textRec.left,textRec.bottom=rect_min_x,rect_max_y
                DISPLAYSURF.blit(textsurface,textRec)

            if ev.type==KEYDOWN:
                if ev.unicode=="n":
                    DISPLAYSURF.fill(BLACK)
        pygame.display.update()
 
