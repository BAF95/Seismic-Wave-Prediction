import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

waveform_per = pd.read_csv("data/Waveformtotals.csv")
waveform_labels = waveform_per["Waveform"]
waveform_data = waveform_per["Count"]
waveform_percent = (waveform_per["Count"]/waveform_data.sum())*100
# explode = [.5,.25,.25,-.5,0,0,0,0,0]

pieplot = plt.pie(x=waveform_data,labels=waveform_labels, radius=1.1, autopct="%1.1f%%")
plt.savefig("visualization/Percentage_of_Total_Waveform_Pie_Chart.png", )
plt.show()


predicition_data = pd.read_csv("data/PredictionData.csv")

trueDF = predicition_data.loc[predicition_data["Match"] == True]
falseDF = predicition_data.loc[predicition_data["Match"] == False]





truex = trueDF["Depth"]
truey = trueDF["Magnitude"]

falsex = falseDF["Depth"]
falsey = falseDF["Magnitude"]


colors = ['red','green','blue','purple', 'yellow', 'magenta', 'black', 'brown', 'cyan']

# setup the figure
fig, (ax, ax1) = plt.subplots(nrows=2, figsize=(10,10))

ax.scatter(truex, truey, c="green")
ax.set_xlabel("Depth")
ax.set_ylabel("Magnitude")
ax.set_title("Correct Predictions Depth vs. Magnitude")
ax1.scatter(falsex,falsey, marker="x", c="red")
ax1.set_xlabel("Depth")
ax1.set_ylabel("Magnitude")
ax1.set_title("Incorrect Predictions Depth vs. Magnitude")
plt.savefig("visualization/Correct_vs_Incorrect_Over_Depth_and_Magnitude.png")
plt.show()