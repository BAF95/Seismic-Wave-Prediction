import requests
import json
import os
from pprint import pprint
import sklearn as sk
import pandas as pd
from sklearn import naive_bayes
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import BaseNB
from sklearn.model_selection import train_test_split
url = "https://earthquake.usgs.gov/fdsnws/event/1/[query[format=geojson]]"
data_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2019-01-01&endtime=2019-01-31&eventtype=earthquake"
output_path = os.path.join("/images/")

response = requests.get(data_url)
data = response.json()

#needed_data = ["magType", "mag", "dmin"]
# mag = data["features"][0]["properties"]["mag"]
# magType = data["features"][0]["properties"]["magType"]
# dmin = data["features"][0]["properties"]["dmin"]
# pprint(data)
dmin = []
mag = []
magType = []
none = []

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

# creates dataframe from list
dmin_Df = pd.DataFrame({"Depth min": dmin})


mag_df = pd.DataFrame({"Magnitude":mag})
mag_df["Magnitude"] = mag_df["Magnitude"].abs()


magType_df = pd.DataFrame({"Waveform":magType})
print(magType_df.value_counts())

# merges fataframes made above
Ses_DF = pd.DataFrame(dmin_Df)
Ses_DF = Ses_DF.merge(mag_df, "inner", right_index=True, left_index=True)
Ses_DF = Ses_DF.merge(magType_df, "inner", right_index=True, left_index=True)






# print(Ses_DF)
X = Ses_DF[["Magnitude", "Depth min"]]
# X = Ses_DF["Magnitude"]

y = Ses_DF["Waveform"]
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
clf = MultinomialNB()

clf.fit(X_train, Y_train)
# MultinomialNB()
score = clf.score(X_test, Y_test)
print(f"Accuracy of model: {score*100}%")
predicted = clf.predict(X)

# score = predicted.score(X,y)
print(predicted)

# score = clf.score(X_test,Y_test)
# print(score)
# NB = naive_bayes.GaussianNB()

