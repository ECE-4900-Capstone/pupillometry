import cv2
print(cv2.__version__)
import os
dispW=1920
dispH=1080
flip=2

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)

cv2.namedWindow('nanoCam')

cnt = 0

directory = r'/home/esl-jetson/Desktop/pyPro'
os.chdir(directory)

while True:
    ret, frame = cam.read()
    if not ret:
        print('failed to grab frame')
        break
    cv2.imshow('nanoCam', frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        #Esc hit
        print('Escape hit, closing...')
        break
    if k%256 == 32:
        #SPACE hit
        img_name = 'picture1{}.png'.format(cnt)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        cnt += 1
cam.release()
cv2.destroyAllWindows()
    