import numpy as np
import cv2

dispW=1920
dispH=1080
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap=cv2.VideoCapture(camSet) 
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
frame_width = int(cap.get(3))
frame_height =  int(cap.get(4))
out=cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 7, (frame_width, frame_height))


from threading import Thread
import threading
import time

recordVideo = True
detected = True

def VideoWriting():
    global frame
    global writeVideo
    firstTime = False
    writeVideo = False


    while recordVideo:
        # if(True == firstTime and True == detected and True == writeVideo):
            # print("init")
            # frame_width = int(cap.get(3))
            # frame_height =  int(cap.get(4))
            # out=cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 7, (frame_width, frame_height))
            # firstTime = False
        if(True == writeVideo):
            out.write(frame)
            print("VideoWriting :: Frame")
            writeVideo = False
        if(False == detected):
            firstTime = True
            out.release()
    
    if(out.isOpened() ):
        print("Released")
        out.release()

th = []

th.append(Thread(target=VideoWriting) )
th[-1].daemon = True
th[-1].start()

while(True):
    ret, frame = cap.read()
    if ret==True:
        writeVideo = True
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

recordVideo = False

for thd in th:
    thd.join()