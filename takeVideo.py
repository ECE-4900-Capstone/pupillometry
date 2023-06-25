import cv2
print(cv2.__version__)
import os
import numpy as np

# import queue from Queue
dispW=1920
dispH=1080
flip=4

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet) 
frame_width = int(cam.get(3))
frame_height =  int(cam.get(4))

UserInputData = input("Enter Video FileName (no extension):")
out=cv2.VideoWriter(UserInputData + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 7, (frame_width, frame_height))

cv2.namedWindow('nanoCam')

directory = r'/home/esl-jetson/Desktop/pyPro'
os.chdir(directory)

if cam.isOpened()==False:
    print("Error opening video stream")


recordBool = False

while(True):
    ret, frame = cam.read()
    if ret == True:
        # out.write(frame)

        # frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        # cv2.normalize(frame, frame, 50, 655, cv2.NORM_MINMAX)

        cv2.imshow('nanoCam', frame)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break

        if k%256 == 32:
            #SPACE hit
            recordBool = not recordBool
            
        if recordBool == True:
            # t = time.time()
            out.write(frame)
            # print(time.time() - t)

    else:
        print('failed to grab frame')
        break

cam.release()
cv2.destroyAllWindows()
    