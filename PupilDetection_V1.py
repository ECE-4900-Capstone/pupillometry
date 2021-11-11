import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import csv

# Load Pre-Trained Model
eye_cascade = cv2.CascadeClassifier('C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\haarcascae_eye.xml')

# Load recording
cap = cv2.VideoCapture("C:\\Users\Owner\PycharmProjects\Capstone\Recordings\Zach_control1_11_9.avi")

# USER PARAMETERS
MaxRadius = 200


loopCount = 0
diameter = []
blink = False
bcount = -1
kernel = np.ones((5, 5), np.uint8)
global a
font = cv2.FONT_HERSHEY_SIMPLEX

# Use Try statement to except end-of-video errors
try:
    while 1:
        ret, img = cap.read()
        img = cv2.resize(img, (1280, 720))  # Resize image
        # cv2.imshow('nanoCam', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use trained model to detect eye. Return dimensions/location of eye.
        # First parameter is scaleFactor - smaller = more processing. Bigger = miss faces
        # Second Parameter is minSize - Number of neighboring frames that must agree with decision. Higher = fewer detections, but higher quality
        eyes = eye_cascade.detectMultiScale(gray, 1.05, 7) #TODO: CHanged this from 1.05, 7

        #If Eye detected by ML
        if (len(eyes) > 0):
            a = "Eye Open"

            if (blink == True):
                blink = False

            cv2.putText(img, a, (1100, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("Eyes", eyes)

            for (ex, ey, ew, eh) in eyes:
                # loopCount = loopCount+1
                # print("loop" + str(loopCount))
                # cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                # Resize frame using dimensions obtained from ML algorithm
                roi_gray2 = gray[ey:ey + eh, ex:ex + ew]
                roi_color2 = img[ey:ey + eh, ex:ex + ew]
                # roi_gray2 = gray[ey:ey + 550, ex:ex + 550]
                # roi_color2 = img[ey:ey + 550, ex:ex + 550]

                # Apply image smoothing - results in less circles being placed on random noise
                blur = cv2.GaussianBlur(roi_gray2, (5, 5), 10) #TODO : CHANGED THIS from roi_gray2
                erosion = cv2.erode(blur, kernel, iterations=2)
                # cv2.imshow("erosion", erosion)

                # Apply image contrast filtering. Adaptive filtering works better for getting rid of noise
                # ret3, th3 = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                th3 = cv2.adaptiveThreshold(erosion, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) #TODO: Changed this from 11, 2
                cv2.imshow("threshold", th3)

                # Find circles!! - # TODO: Decide whether circles should be placed on threashold filtering or erosion (Cropped smoothed image)
                # circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 4, 200, param1=20, param2=150, minRadius=0, maxRadius=MaxRadius)
                circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 4, 200, param1=20, param2=150, minRadius=0, maxRadius=MaxRadius)
                print("Circles", circles)

                # If circles are found
                try:
                    loopCount = loopCount + 1
                    print("loop" + str(loopCount))
                    for i in circles[0, :]:
                        # Check size of radius to see if circle is reasonable
                        if (i[2] > 0 and i[2] < MaxRadius):
                            print(int(i[0]), int(i[1]), int(i[2]))
                            # cv2.circle(roi_color2, (int(366), int(298)), int(152), (0, 0, 255), 1)

                            # Draw circle over image
                            cv2.circle(roi_color2, (int(i[0]), int(i[1])), int(i[2]), (0, 0, 255), 1)
                            cv2.putText(img, "Pupil Pos:", (450, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                            cv2.putText(img, "X " + str(int(i[0])) + " Y " + str(int(i[1])), (430, 60), font, 1,
                                        (0, 0, 255), 2, cv2.LINE_AA)
                            d = (i[2] / 2.0)
                            dmm = 1 / (25.4 / d)
                            diameter.append(dmm)
                            cv2.putText(img, str('{0:.2f}'.format(dmm)) + "mm", (1100, 60), font, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)

                            # Draw center point
                            cv2.circle(roi_color2, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)
                            # cv2.imshow('erosion',erosion)
                except Exception as e:
                    print("error in circle fitting,", e)
                    pass

        else:
            if (blink == False):
                blink = True
                if blink == True:
                    cv2.putText(img, "Blink", (1100, 90), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            a = "Eye Close"
            cv2.putText(img, a, (1100, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    plt.plot(diameter)
    plt.ylabel('pupil Diameter')
    plt.show()
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print("except,", e)
    print(diameter)

    # Plot unfiltered data
    plt.figure(0)
    plt.plot(diameter)
    plt.ylabel('pupil Diameter')
    # plt.show()

    # sos = signal.butter(4, 1/4, 'low', analog=True, output='sos')
    # w, h = signal.freqs(b, a)
    # filteredDiameter = signal.sosfilt(sos, diameter)

    # Filter Data
    n = 2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1
    filteredDiameter = list(signal.lfilter(b, a, diameter))

    # Plot Filtered Data
    print(filteredDiameter)
    plt.figure(1)
    plt.plot(filteredDiameter[1:])
    plt.ylabel('pupil Diameter')

    # Write to CSV
    f = open("extractedPupil.csv", 'w')
    writer = csv.writer(f)
    writer.writerow(["Frame", "Diameter"])
    for i in range(len(filteredDiameter)):
        writer.writerow([str(i), str(filteredDiameter[i])])
    f.close()

    plt.show()