import cv2
print(cv2.__version__)
import os
from imutils.video import FPS
import argparse
import numpy as np
from threading import Thread
import sys
# import queue from Queue
dispW=1920
dispH=1080
flip=2

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet) 
frame_width = int(cam.get(3))
frame_height =  int(cam.get(4))

cnt = 0
out=cv2.VideoWriter('outpy' + str(cnt) + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 7, (frame_width, frame_height))
# cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)

cv2.namedWindow('nanoCam')



directory = r'/home/esl-jetson/Desktop/pyPro'
os.chdir(directory)

if cam.isOpened()==False:
    print("Error opening video stream")

# construct the argument parse and parse the argument
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", required=True,
#     help="path to input video file")
# args = vars(ap.parse_args())

# class FileVideoStream:
#     def __init__(self, path, queueSize=128):
#         # initialize the file video stream along with the boolean
#         # used to indicate if the thread should be stopped or not
#         self.stream = cv2.VideoCapture(path)
#         self.stopped = False
#         # initialize the queue used to store frames read from
#         # the video file
#         self.Q = Queue(maxsize=queueSize)

#     def start(self):
#         # start a thread to read frames from the file video stream
#         t = Thread(target=self.update, args=())
#         t.daemon = True
#         t.start()
#         return self

#     def update(self):
#         # keep looping infinitely
#         while True:
#             # if the thread indicator variable is set, stop the
#             # thread
#             if self.stopped:
#                 return
#             # otherwise, ensure the queue has room in it
#             if not self.Q.full():
#                 # read the next frame from the file
#                 (grabbed, frame) = self.stream.read()
#                 # if the `grabbed` boolean is `False`, then we have
#                 # reached the end of the video file
#                 if not grabbed:
#                     self.stop()
#                     return
#                 # add the frame to the queue
#                 self.Q.put(frame)

#     def read(self):
#         # return next frame in the queue
#         return self.Q.get()

#     def more(self):
#         # return True if there are still frames in the queue
#         return self.Q.qsize() > 0

#     def stop(self):
#         # indicate that the thread should be stopped
#         self.stopped = True

# open a pointer to the video stream and start the FPS timer
# stream = cv2.VideoCapture(args["video"])
fps = FPS().start()

recordBool = False

while(True):
    ret, frame = cam.read()
    if ret == True:
        # out.write(frame)

        # frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        # cv2.normalize(frame, frame, 50, 655, cv2.NORM_MINMAX)

        # display the size of the queue on the frame
	    # cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
		# (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow('nanoCam', frame)
        fps.update()
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        
    # if k%256 == 27:
    #     #Esc hit
    #     print('Escape hit, closing...')
    #     break
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
        # img_name = 'video1{}.mp4'.format(cnt)
        # cv2.imwrite(img_name, frame)
        # print("{} written!".format(img_name))
        # cnt += 1
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cam.release()
cv2.destroyAllWindows()
    