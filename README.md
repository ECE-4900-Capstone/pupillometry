# pupillometry - pupil-detection
This branch contais files for performing pupil size detection on pre-recorded videos

PupilDetection_V1.py: main file for performing pupil size detection
haarcascae_eye.xml: pre-trained model for detecting eye location in PupilDetection_V1.py
normalize_to_control.py: takes the CSV output results from PupilDetection_V1.py and normalizes the pupil size for Easy/Hard/WMC (Working Memory Capacity) tests to the control test. 
PlotCSV.py: Plot CSV results
