# JAZHL Research Team
# ECE 4900 Capstone 2
# Authored by Jacob Haehn, Hayden Clark

# Imports
import csv
import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
import math


# Google Drive access for data - deprecated
#from google.colab import drive
#drive.mount('/content/drive')

# Functions
# =============================================================================
# def train_ML(inputFile, finalizedModelFilepath):
#     # Extract Data
#     X, y = extract_data(inputFile)
# 
#     # Optional step for verifying initial accuracy of log_reg
#     # training_accuracy_check()
# 
#     # Perform ML training
#     trainedModel = cross_validation(X, y, finalizedModelFilepath)
#                                     
#     return trainedModel
# =============================================================================
    
# =============================================================================
# def run_ML_predict(finalizedModelFilepath, testPupilRadius):
#     # Load Trained Model
#     trainedModel = load_trained_model(finalizedModelFilepath)
# 
#     # Make Cognitive Load Predictions
#     logreg = sk.linear_model.LogisticRegression(C=1e5, solver = 'liblinear')
#     #cognitiveLoadPrediction = logreg.predict(testPupilRadius)
# 
#     return logreg.predict(testPupilRadius) #previously cognitiveLoadPrediction
# =============================================================================

# Functions
def extract_data(inputFile): # Function used for data extraction

  # Define columns for data extraction
  #frameNumberCol = 0
  radiusChangeCol = 0
  groundTruthCol = 1

  # Open CSV file
  with open(inputFile, newline='') as csvfile:
        # Read CSV
        csv_data = list(csv.reader(csvfile, delimiter=','))

        # Extract rows of CSV and store in list
        radiusList = []
        groundTruthList = []
    
        for row in csv_data[0:]:

          radiusList.append(float(row[radiusChangeCol]))
          truth_val = int(row[groundTruthCol])
          groundTruthList.append(truth_val)

        #print(frameNumberList)
        #print(radiusList)
        #print(groundTruthList)
        
        #extra loop to truncate ground truth data
        #truncatedGroundTruthList =  groundTruthList
        return radiusList, groundTruthList


def training_accuracy_check(X, y):
    # Log. Reg. solver 
    logreg = sk.linear_model.LogisticRegression(C=1e5, solver = 'liblinear')
    X = np.array(X).reshape(-1, 1)
    logreg.fit(X,y)

    # Check accuracy of classifier (should be 100% on the training data)
    yhat = logreg.predict(X)
    acc = np.mean(yhat == y)
    print("Accuracy on training data = %f" % acc)

def cross_validation(X, y): #deleted additional parameter "finalizedModelFilepath"
    # Cross-Validation (need to edit variables)

    from sklearn.metrics import precision_recall_fscore_support
    from sklearn.model_selection import KFold

    X = np.array(X).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)

    nfold = 20
    kf = KFold(n_splits=nfold,shuffle=False)
    prec = []
    rec = []
    f1 = []
    acc = []
    for train, test in kf.split(X):            
        # Get training and test data
        Xtr = X[train]
        ytr = y[train]
        Xts = X[test]
        yts = y[test]
        
        # Fit a model
        # print("Fitting Model " + train + "," + test + "...")
        logreg = sk.linear_model.LogisticRegression(C=1e5, solver = 'liblinear')
        logreg.fit(Xtr, ytr)
        yhat = logreg.predict(Xts)
        
        # Measure performance
        # print("Measuring Performance " + train + "," + test + "...")
        preci,reci,f1i,_= precision_recall_fscore_support(yts,yhat,average='binary') 
        prec.append(preci)
        rec.append(reci)
        f1.append(f1i)
        acci = np.mean(yhat == yts)
        acc.append(acci)

    print("Finished training")
    # Take average values of the metrics
    precm = np.mean(prec)
    recm = np.mean(rec)
    f1m = np.mean(f1)
    accm= np.mean(acc)

    # Compute the standard errors
    prec_se = np.std(prec,ddof=1)/np.sqrt(nfold)
    rec_se = np.std(rec,ddof=1)/np.sqrt(nfold)
    f1_se = np.std(f1,ddof=1)/np.sqrt(nfold)
    acc_se = np.std(acc,ddof=1)/np.sqrt(nfold)

    print('Precision = {0:.4f}, SE={1:.4f}'.format(precm,prec_se))
    print('Recall =    {0:.4f}, SE={1:.4f}'.format(recm, rec_se))
    print('f1 =        {0:.4f}, SE={1:.4f}'.format(f1m, f1_se))
    print('Accuracy =  {0:.4f}, SE={1:.4f}'.format(accm, acc_se))
    
    print(logreg.intercept_)
    print(logreg.coef_)
    
    finalizedModelFilepath = 'finalizedModel.sav'
    print("Saving model to " + finalizedModelFilepath)
    pickle.dump(logreg, open(finalizedModelFilepath, 'wb'))

    return logreg 



def load_trained_model(finalizedModelFilepath):
      loaded_model = pickle.load(open(finalizedModelFilepath, 'rb'))
      result = loaded_model.score(X, y)
      print(result)
  
      return loaded_model




if __name__ == '__main__':
    inputFile = "BigAssTrainingData.csv"
    
    X, y = extract_data(inputFile) #X = radiusList, y = groundTruthList
    
    training_accuracy_check(X, y)
    # print(X)
    # print(y)
    cross_validation(X, y)