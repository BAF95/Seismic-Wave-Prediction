import requests
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib as plt
# url: references default USGS API url
# data_url = the actual data url

url = "https://earthquake.usgs.gov/fdsnws/event/1/[query[format=geojson]]"
data_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2020-4-01&endtime=2020-5-01&eventtype=earthquake"

# json response and data format
response = requests.get(data_url)
data = response.json()

# needed_data = ["magType", "mag", "dmin"]
# mag = data["features"][0]["properties"]["mag"]
# magType = data["features"][0]["properties"]["magType"]
# dmin = data["features"][0]["properties"]["dmin"]

# creates lists for needed data
dmin = []
mag = []
magType = []
none = []

#wrapper to extract data from GEOJson
for x in data["features"]:
    if x["properties"]["dmin"] == None:
        none.append((x["properties"]["dmin"]))
    else:
        dmin.append(x["properties"]["dmin"])
for x in data["features"]:
    if x["properties"]["mag"] == None:
        none.append((x["properties"]["mag"]))
    else:
        mag.append(x["properties"]["mag"])
for x in data["features"]:
    if x["properties"]["magType"] == None:
        none.append((x["properties"]["magType"]))
    else:
        magType.append(x["properties"]["magType"])

# creates dataframe from lists
dmin_Df = pd.DataFrame({"Depth": dmin})
mag_df = pd.DataFrame({"Magnitude":mag})
mag_df["Magnitude"] = mag_df["Magnitude"].abs()
magType_df = pd.DataFrame({"Waveform":magType})

print(dmin_Df.max(), dmin_Df.min())
# used to show statistics distribution of prediction variables
# a good distribution of wave forms is important
Waveformtotals = magType_df.value_counts()
Waveformtotals = Waveformtotals.rename("Count")
Waveformtotals.to_csv(path_or_buf="data/Waveformtotals.csv")
print(magType_df.value_counts())

# merges dataframes made above
Ses_DF = pd.DataFrame(dmin_Df)
Ses_DF = Ses_DF.merge(mag_df, "inner", right_index=True, left_index=True)
Ses_DF = Ses_DF.merge(magType_df, "inner", right_index=True, left_index=True)






# sets variables to be predicted
X = Ses_DF[["Magnitude", "Depth"]]
y = Ses_DF["Waveform"]

# test train split
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
# model creation
clf = SVC()

# fits data
clf.fit(X_train, Y_train)

# scores model
score = clf.score(X_test, Y_test)
print(f"Accuracy of model: {score*100}%")
# predicted model
predicted = clf.predict(X_train)
predicted = pd.DataFrame({"Predicted_Waveform":predicted})


# merges predicted and actual Waveforms
compared = predicted.merge(y, "inner", right_index=True, left_index=True)


# compared accuracy list passes a True if the prediction matches the actual waveform, and False if it doesn't
# i is the index for the while loop
# i_list creates an index within the data for later processing
compared_accuracy = []
i = 0
i_list = []
# while loop for passing correct or incorrect predictions
# while i is less then length, so every element gets covered
while i < len(compared):
    # finds the values un compared Dataframe at index i
    value = compared.loc[i]

    # transposes value
    value = value.T
    # assigns actual value to com1 and predicted value to com2
    com1 = value["Waveform"]
    com2 = value["Predicted_Waveform"]
    # compares com to com 2 if same then true if different false then adds 1 to i index
    if com1 == com2:
       compared_accuracy.append("True")
       i_list.append(i)
       i += 1

    else:
       compared_accuracy.append("False")
       i_list.append(i)
       i += 1

#creates datafrome from list for accuracy and index list
compared_accuracyDF = pd.DataFrame({"Match": compared_accuracy})
i_listDF = pd.DataFrame({"Index": i_list})
# merges compared with index,accuracy, and magnitude, depth
compared = compared.merge(i_listDF, "inner", right_index=True, left_index=True)
compared = compared.merge(compared_accuracyDF, "inner", right_index=True, left_index=True)
compared = compared.merge(X, "inner", right_index=True, left_index=True)




# writes compared to csv
compared.to_csv(path_or_buf="data/PredictionData.csv")

# creates a Key stats DF with Accurate Predicted Total

# counts number of true and false values
Accurate_Predicted_Total = compared["Match"].value_counts()
# calculates actual/experimental %
Accurate_Predicted_Total["Actual Percentage"] = (Accurate_Predicted_Total["True"]/compared["Index"].max())*100
# grabs theoretical % from score variable above
Accurate_Predicted_Total["Theoretical Percentage"] = score*100
# calculates percent error (actual-theoretical)/theoretical
# NOTE: any value of absolute value should bre read as positive even if negative
Accurate_Predicted_Total["Percent Error"] = (((score*100)-(Accurate_Predicted_Total["True"]/compared["Index"].max())*100)/(score*100))*100
Accurate_Predicted_Total.to_csv(path_or_buf="data/Keystats.csv")

# EXTRA CODE FOR FUTURE USE
# score = predicted.score(X,y)
# score = clf.score(X_test,Y_test)
# print(score)
# NB = naive_bayes.GaussianNB()

# plot = plt.plot()