import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import csv
import os

# Get Video input filename
videoFilename = "C:\\Users\Owner\PycharmProjects\Capstone\Recordings\Jacob_12_01\Jacob_WMC_12_1_2021_.avi" #input("Enter Video Filename:")

# Get csv filename from user
CSVfileName = "Run1_" + os.path.basename(videoFilename).split('.')[0] + ".csv" #input("Enter CSV Filename:")

# Load Pre-Trained Model - make sure this file is in your working directory
eye_cascade = cv2.CascadeClassifier('C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\haarcascae_eye.xml')

# Load recording
cap = cv2.VideoCapture(videoFilename)

# USER PARAMETERS
BypassEyeDetection = True

n1 = 6  # 2 - the larger n is, the smoother curve will be - THIS IS THE FILTER NUMBER THAT WILL BE SAVED IN THE CSV
n2 = 8
n3 = 4
NumToExclude = 6 # 1 - Number of zero points to exclude after filtering

Bright_Contrast_Alpha = 50 # 50   # The higher both Alpha and Beta, the brighter. The further apart they are, the more contrast
Bright_Contrast_Beta = 655 # 655

eyeDetect_scaleFactor = 1.05 # 1.05 - higher = more cpu and more accurate
eyeDetect_minSize = 1 # 7

ey = 200
eh = 450
ex = 350
ew = 450

# Line 87-88, can decide whether using adaptive filtering or not. Each better in some cases
threshold_param1 = 15 # 11 - BlockSize?? - must be odd
threshold_param2 = 3 # 2 - difference from block size that will be recognized??

MinRadius = 90
MaxRadius = 160
houghcircle_paramA = 4 # 4
houghcircle_paramB = 200 # 200
houghcircle_param1 = 20 # 20
houghcircle_param2 = 250  # 150 Accumulator threshold - the higher, the less circles there will be and hopefully higher probability

FrameNumber = 0
FrameList = []
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
        FrameNumber = FrameNumber + 1
        img = cv2.resize(img, (1280, 720))  # Resize image
        # cv2.imshow('nanoCam', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use trained model to detect eye. Return dimensions/location of eye.
        # First parameter is scaleFactor - smaller = more processing. Bigger = miss faces
        # Second Parameter is minSize - Number of neighboring frames that must agree with decision. Higher = fewer detections, but higher quality
        eyes = eye_cascade.detectMultiScale(gray, eyeDetect_scaleFactor, eyeDetect_minSize) #TODO: CHanged this from 1.05, 7

        cv2.normalize(gray, gray, 50, 655, cv2.NORM_MINMAX)  # Adjust Brightness and Contrast

        #If Eye detected by ML
        if (len(eyes) > 0 or BypassEyeDetection == True):
            a = "Eye Open"

            if (blink == True):
                blink = False

            cv2.putText(img, a, (1100, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("Eyes", eyes)

            # Run the code with eye detection
            if BypassEyeDetection == True:
                # loopCount = loopCount+1
                # print("loop1" + str(loopCount))

                cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                # Resize frame using dimensions obtained from ML algorithm
                roi_gray2 = gray[ey:ey + eh, ex:ex + ew]
                roi_color2 = img[ey:ey + eh, ex:ex + ew]
                # roi_gray2 = gray
                # roi_color2 = img

                # Apply image smoothing - results in less circles being placed on random noise
                blur = cv2.GaussianBlur(roi_gray2, (7, 7), 10)  # TODO : CHANGED THIS from roi_gray2
                erosion = cv2.erode(blur, kernel, iterations=2)
                cv2.imshow("erosion", erosion)

                # Apply image contrast filtering. Adaptive filtering works better for getting rid of noise
                # ret3, th3 = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                th3 = cv2.adaptiveThreshold(erosion, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, threshold_param1, threshold_param2)  # TODO: Changed this from 11, 2
                cv2.imshow("threshold", th3)

                # Find circles!! - # TODO: Decide whether circles should be placed on threashold filtering or erosion (Cropped smoothed image)
                # circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 4, 200, param1=20, param2=150, minRadius=0, maxRadius=MaxRadius)
                circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, houghcircle_paramA, houghcircle_paramB,
                                           param1=houghcircle_param1, param2=houghcircle_param2, minRadius=MinRadius,
                                           maxRadius=MaxRadius)
                print("Circles", circles)

                # If circles are found
                try:
                    # loopCount = loopCount + 1
                    # print("loop" + str(loopCount))
                    for i in circles[0, :]:
                        # Check size of radius to see if circle is reasonable
                        if (i[2] > MinRadius and i[2] < MaxRadius):
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
                            FrameList.append(FrameNumber)
                            cv2.putText(img, str('{0:.2f}'.format(dmm)) + "mm", (1100, 60), font, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)

                            # Draw center point
                            cv2.circle(roi_color2, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)
                            # cv2.imshow('erosion', erosion)
                except Exception as e:
                    print("error in circle fitting,", e)
                    pass
            # Run the code without eye detection
            else:
                for (ex, ey, ew, eh) in eyes:
                    # loopCount = loopCount+1
                    # print("loop1" + str(loopCount))
                    # cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                    # Resize frame using dimensions obtained from ML algorithm
                    roi_gray2 = gray[ey:ey + eh, ex:ex + ew]
                    roi_color2 = img[ey:ey + eh, ex:ex + ew]
                    # roi_gray2 = gray
                    # roi_color2 = img

                    # Apply image smoothing - results in less circles being placed on random noise
                    blur = cv2.GaussianBlur(roi_gray2, (7, 7), 10) #TODO : CHANGED THIS from roi_gray2
                    erosion = cv2.erode(blur, kernel, iterations=2)
                    # cv2.imshow("erosion", erosion)

                    # Apply image contrast filtering. Adaptive filtering works better for getting rid of noise
                    # ret3, th3 = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    th3 = cv2.adaptiveThreshold(erosion, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, threshold_param1, threshold_param2) #TODO: Changed this from 11, 2
                    cv2.imshow("threshold", th3)

                    # Find circles!! - # TODO: Decide whether circles should be placed on threashold filtering or erosion (Cropped smoothed image)
                    # circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 4, 200, param1=20, param2=150, minRadius=0, maxRadius=MaxRadius)
                    circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, houghcircle_paramA, houghcircle_paramB, param1=houghcircle_param1, param2=houghcircle_param2, minRadius=MinRadius, maxRadius=MaxRadius)
                    print("Circles", circles)

                    # If circles are found
                    try:
                        # loopCount = loopCount + 1
                        # print("loop" + str(loopCount))
                        for i in circles[0, :]:
                            # Check size of radius to see if circle is reasonable
                            if (i[2] > MinRadius and i[2] < MaxRadius):
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
                                FrameList.append(FrameNumber)
                                cv2.putText(img, str('{0:.2f}'.format(dmm)) + "mm", (1100, 60), font, 1, (0, 0, 255), 2,
                                            cv2.LINE_AA)

                                # Draw center point
                                cv2.circle(roi_color2, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)
                                cv2.imshow('erosion',erosion)
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
    print(len(diameter))
    print(len(FrameList))

    # Plot unfiltered data
    plt.figure(0)
    plt.plot(FrameList, diameter)
    plt.ylabel('Pupil Diameter')
    plt.xlabel('Frame Number')
    plt.title('No Filtering')
    # plt.show()

    # sos = signal.butter(4, 1/4, 'low', analog=True, output='sos')
    # w, h = signal.freqs(b, a)
    # filteredDiameter = signal.sosfilt(sos, diameter)

    # Filter Data
    b1 = [1.0 / n1] * n1
    b2 = [1.0 / n2] * n2
    b3 = [1.0 / n3] * n3
    a = 1
    filteredDiameter1 = list(signal.lfilter(b1, a, diameter))
    filteredDiameter2 = list(signal.lfilter(b2, a, diameter))
    filteredDiameter3 = list(signal.lfilter(b3, a, diameter))

    # Plot Filtered Data
    print("filteredDiameter1: ", filteredDiameter1)
    print("filteredDiameter2: ", filteredDiameter2)
    print("filteredDiameter3: ", filteredDiameter3)

    plt.figure(1)
    plt.plot(FrameList[NumToExclude:], filteredDiameter1[NumToExclude:])
    plt.ylabel('Pupil Diameter')
    plt.xlabel('Frame Number')
    plt.title('n = ' + str(n1))

    plt.figure(2)
    plt.plot(FrameList[NumToExclude:], filteredDiameter2[NumToExclude:])
    plt.ylabel('Pupil Diameter')
    plt.xlabel('Frame Number')
    plt.title('n = ' + str(n2))

    plt.figure(3)
    plt.plot(FrameList[NumToExclude:], filteredDiameter3[NumToExclude:])
    plt.ylabel('Pupil Diameter')
    plt.xlabel('Frame Number')
    plt.title('n = '+ str(n3))

    # Write to CSV
    f = open(CSVfileName, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(["Frame", "Diameter"])
    for i in range(NumToExclude, len(filteredDiameter1)):
        writer.writerow([str(FrameList[i]), str(filteredDiameter1[i])])
    f.close()

    plt.show()