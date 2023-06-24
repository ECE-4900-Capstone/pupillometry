import csv
import os
import matplotlib.pyplot as plt

# Get Control csv filename
control_file = "C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\Run1_jacob_control0_12_1.csv"  # input("Enter Control CSV Filename:")

# Get Input csv filename
input_file_Control = control_file
input_file_Easy = "C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\Run1_Jacob_Easy_12_01_2021.csv"  # input("Enter Input CSV Filename:")
input_file_Hard = "C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\Run1_Jacob_Hard_12_01_2021.csv"
input_file_WMC = "C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\Run1_Jacob_WMC_12_01_test2.csv"

# Get output csv filename
CSVfilename_Control = os.path.basename(input_file_Control).split('.')[0] + "_normalized.csv"
CSVfilename_Easy = os.path.basename(input_file_Easy).split('.')[0] + "_normalized.csv" # input("Enter Output CSV Filename:")
CSVfilename_Hard = os.path.basename(input_file_Hard).split('.')[0] + "_normalized.csv"
CSVfilename_WMC = os.path.basename(input_file_WMC).split('.')[0] + "_normalized.csv"

control_average = 0.0
count = 0

f = open(control_file, newline='')
reader = csv.reader(f)
Frame_control = []
Diameter_control = []
for row in reader:
    if row != [] and row[0] != 'Frame':
        Frame_control.append(int(row[0]))
        Diameter_control.append(float(row[1]))
f.close()

control_average = sum(Diameter_control)/len(Diameter_control)
print(control_average)

# Control
f_output = open(CSVfilename_Control, 'w', newline='')
writer = csv.writer(f_output)
writer.writerow(["Frame", "Normalized Diameter", "Original Diameter"])
f_input = open(input_file_Control, newline='')
reader = csv.reader(f_input)
Frame_Control = []
Diameter_Control = []
Normalized_Control = []
for row in reader:
    if row != [] and row[0] != 'Frame':
        CurrentFrame = int(row[0])
        CurrentDiameter = float(row[1])
        Frame_Control.append(CurrentFrame)
        Diameter_Control.append(CurrentDiameter)
        normalized_value = (CurrentDiameter - control_average)/control_average
        Normalized_Control.append(normalized_value)
        writer.writerow([CurrentFrame, normalized_value, CurrentDiameter])
f_input.close()
f_output.close()

plt.figure(0)
plt.title("Normalized Control")
plt.plot(Frame_Control, Normalized_Control)
plt.figure(1)
plt.title("Original Control")
plt.plot(Frame_Control, Diameter_Control)


# Easy
if input_file_Easy is not None:
    f_output = open(CSVfilename_Easy, 'w', newline='')
    writer = csv.writer(f_output)
    writer.writerow(["Frame", "Normalized Diameter", "Original Diameter"])
    f_input = open(input_file_Easy, newline='')
    reader = csv.reader(f_input)
    Frame_Easy = []
    Diameter_Easy = []
    Normalized_Easy = []
    for row in reader:
        if row != [] and row[0] != 'Frame':
            CurrentFrame = int(row[0])
            CurrentDiameter = float(row[1])
            Frame_Easy.append(CurrentFrame)
            Diameter_Easy.append(CurrentDiameter)
            normalized_value = (CurrentDiameter - control_average)/control_average
            Normalized_Easy.append(normalized_value)
            writer.writerow([CurrentFrame, normalized_value, CurrentDiameter])
    f_input.close()
    f_output.close()

    plt.figure(2)
    plt.title("Normalized Easy")
    plt.plot(Frame_Easy, Normalized_Easy)
    plt.figure(3)
    plt.title("Original Easy")
    plt.plot(Frame_Easy, Diameter_Easy)

# Hard
if input_file_Hard is not None:
    f_output = open(CSVfilename_Hard, 'w', newline='')
    writer = csv.writer(f_output)
    writer.writerow(["Frame", "Normalized Diameter", "Original Diameter"])
    f_input = open(input_file_Hard, newline='')
    reader = csv.reader(f_input)
    Frame_Hard = []
    Diameter_Hard = []
    Normalized_Hard = []
    for row in reader:
        if row != [] and row[0] != 'Frame':
            CurrentFrame = int(row[0])
            CurrentDiameter = float(row[1])
            Frame_Hard.append(CurrentFrame)
            Diameter_Hard.append(CurrentDiameter)
            normalized_value = (CurrentDiameter - control_average)/control_average
            Normalized_Hard.append(normalized_value)
            writer.writerow([CurrentFrame, normalized_value, CurrentDiameter])
    f_input.close()
    f_output.close()

    plt.figure(4)
    plt.title("Normalized Hard")
    plt.plot(Frame_Hard, Normalized_Hard)
    plt.figure(5)
    plt.title("Original Hard")
    plt.plot(Frame_Hard, Diameter_Hard)

# WMC
if input_file_WMC is not None:
    f_output = open(CSVfilename_WMC, 'w', newline='')
    writer = csv.writer(f_output)
    writer.writerow(["Frame", "Normalized Diameter", "Original Diameter"])
    f_input = open(input_file_WMC, newline='')
    reader = csv.reader(f_input)
    Frame_WMC = []
    Diameter_WMC = []
    Normalized_WMC = []
    for row in reader:
        if row != [] and row[0] != 'Frame':
            CurrentFrame = int(row[0])
            CurrentDiameter = float(row[1])
            Frame_WMC.append(CurrentFrame)
            Diameter_WMC.append(CurrentDiameter)
            normalized_value = (CurrentDiameter - control_average)/control_average
            Normalized_WMC.append(normalized_value)
            writer.writerow([CurrentFrame, normalized_value, CurrentDiameter])
    f_input.close()
    f_output.close()

    plt.figure(6)
    plt.title("Normalized WMC")
    plt.plot(Frame_WMC, Normalized_WMC)
    plt.figure(7)
    plt.title("Original WMC")
    plt.plot(Frame_WMC, Diameter_WMC)

plt.show()


