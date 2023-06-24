import csv
import matplotlib.pyplot as plt

CSVfilename = "C:\\Users\Owner\PycharmProjects\Capstone\pyPro\Capstone\FinalCSV\Run0_Lindsey_Hard_11_11_ts2.csv"

# Write to CSV
f = open(CSVfilename, newline='')
reader = csv.reader(f)

Frame = []
Diameter = []
for row in reader:
    if row != [] and row[0] != 'Frame':
        print(row)
        Frame.append(int(row[0]))
        Diameter.append(float(row[1]))
f.close()

print(Frame)

plt.plot(Frame, Diameter)
plt.show()