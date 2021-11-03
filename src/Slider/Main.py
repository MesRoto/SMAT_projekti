from warnings import catch_warnings
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib
import pandas as pd
from matplotlib.widgets import Slider
from scipy.stats import exponnorm
from scipy.optimize import curve_fit, minimize
import scipy
from scipy.interpolate import interp1d

import Functions as F
import ReadData as rd

df = rd.ReadData()
df = rd.CreateFeature_df(df)

#print(df)

#Tested graph
selected = df[df["flow"] == 100]
selected = selected[selected["sample"] == 1]

#print(selected)
########################
#Sliders
########################

start = 0
stop = 265
test_start = -5
test_stop = 15

area = np.linspace(start, stop, 1000)
testarea = np.linspace(test_start, test_stop, 1000)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.3)

ax.set_xlabel("Time [s]")

#Custom testing area adjusters.
start_position = plt.axes([0.05, 0.18, 0.03, 0.5])
start_position_slider = Slider(start_position, "Range Start", -10, 300, valinit=0, orientation="vertical")
stop_position = plt.axes([0.15, 0.18, 0.03, 0.5])
stop_position_slider = Slider(stop_position, "Range Stop", -10, 300, valinit=265, orientation="vertical")

#Myy sliders for controlling the central point of the peak.
myy_position = plt.axes([0.25, 0.18, 0.65, 0.03])
# Slider size, position
myy_slider = Slider(myy_position, 'Myy', -100, 200, valinit=0)
# Slider range

#Sigma sliders for controlling the width of the peak.
sigma_position = plt.axes([0.25, 0.13, 0.65, 0.03])
sigma_slider = Slider(sigma_position, 'Sigma', -5, 50, valinit=1)

#Lambda sliders for controlling the tail.
lamda_position = plt.axes([0.25, 0.08, 0.65, 0.03])
lamda_slider = Slider(lamda_position, 'Lambda', 0.001, 5, valinit=1)

#Height slider to control the scale of the graph.
h_position = plt.axes([0.25, 0.03, 0.65, 0.03])
h_slider = Slider(h_position, 'Height', 1, 5000000, valinit=1000000)


fig.text(0.47, 0.92, "Exponentially Modified Gaussian graph", fontsize= 20)

#Setup input and tissue graphs.
#######################
selected["midpoint"] = (selected["time_end"] + selected["time_start"]) / 2
cubic_tissue = interp1d(selected["midpoint"], selected["tissue"], kind='cubic')
cubic_input = interp1d(selected["midpoint"], selected["input"], kind='cubic')
min_inter, max_inter = min(selected["midpoint"]), max(selected["midpoint"])
xnew = np.linspace(min_inter, max_inter, num=1000, endpoint=True)

def update(val):

    #clear the old graph
    ax.clear()
    
    myy = myy_slider.val
    sigma = sigma_slider.val
    lamda = lamda_slider.val
    h = h_slider.val

    newstart = start_position_slider.val
    newstop = stop_position_slider.val

    print(myy, sigma, lamda, h, newstart, newstop)

    #Custom drawing area
    custom_area = np.linspace(newstart, newstop, 1000)


    # Draw model graph
    # Notice that the graph can be manipulated via the specified drawing are
    # ie. if the graph is drawn from 0 to 20 it is stretched when compared to
    # 0 to 100
    # To have the graph drawn to same drawing area set custom_area == area.
    ax.plot(area, F.EMG(custom_area, myy, sigma, lamda, h), color = "blue")


    #Draw input and tissue graphs
    ax.plot(selected["midpoint"], selected["tissue"], 'o', xnew, cubic_tissue(xnew), '-')
    ax.plot(selected["midpoint"], selected["input"], 'o', xnew, cubic_input(xnew), '-')

myy_slider.on_changed(update)
sigma_slider.on_changed(update)
lamda_slider.on_changed(update)
h_slider.on_changed(update)

start_position_slider.on_changed(update)
stop_position_slider.on_changed(update)
plt.show()

# Parameters
# Sample 1, Flow 200 Inputiin sopii:
# testarea = 0-20, myy = 40, sigma = 10.14, lamda = 0.068, h = 3.392*10^6
# testarea = -5-15, myy = -0.4, sigma = 1.56, lamda = 0.424, h = 1.235*10^6


