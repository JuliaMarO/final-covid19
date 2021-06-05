"""
Experiment summary
------------------
Treat each province/state in a country cases over time
as a vector, do a simple K-Nearest Neighbor between 
countries. What country has the most similar trajectory
to a given country?
"""

import sys
sys.path.insert(0, '..')

from utils import data
import os
import sklearn
import numpy as np
import json
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')


# ------------ HYPERPARAMETERS -------------
BASE_PATH = '../COVID-19/csse_covid_19_data/'
MIN_CASES = 500000
# ------------------------------------------

deaths = os.path.join(
    BASE_PATH, 
    'csse_covid_19_time_series',
    'time_series_covid19_deaths_global.csv')
deaths = data.load_csv_data(deaths)

confirmed = os.path.join(
    BASE_PATH, 
    'csse_covid_19_time_series',
    'time_series_covid19_confirmed_global.csv')
confirmed = data.load_csv_data(confirmed)

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
cm = plt.get_cmap('jet')
NUM_COLORS = 1
LINE_STYLES = ['solid', 'dashed', 'dotted']
NUM_STYLES = len(LINE_STYLES)

for val in np.unique(confirmed["Country/Region"]):
    df = data.filter_by_attribute(
        confirmed, "Country/Region", val)
    cases, labels = data.get_cases_chronologically(df)
    cases = cases.sum(axis=0)

    df_deaths = data.filter_by_attribute(
        deaths, "Country/Region", val)
    death_cases, death_labels = data.get_cases_chronologically(df_deaths)
    death_cases = death_cases.sum(axis=0)

    #if cases[-1] > MIN_CASES:
    if labels[0,1] == "US":
        NUM_COLORS += 1

colors = [cm(i) for i in np.linspace(0, 1, NUM_COLORS)]
legend = []
handles = []

# basically, for country in countries in our list of confirmed
for val in np.unique(confirmed["Country/Region"]):

    # here's the fancy stuff
    # i have cases and deaths and I want to graph cases[y-19] - deaths[y]

    df = data.filter_by_attribute(
        confirmed, "Country/Region", val)
    cases, labels = data.get_cases_chronologically(df)
    cases = cases.sum(axis=0)

    df_deaths = data.filter_by_attribute(
        deaths, "Country/Region", val)
    death_cases, death_labels = data.get_cases_chronologically(df_deaths)
    death_cases = death_cases.sum(axis=0)

    #if cases[-1] > MIN_CASES:
    if labels[0,1] == "US":
        i = len(legend)

        # generate recovered
        recovered = []

        for j in range(19, len(cases)):
            recovered.append(cases[j-19] - death_cases[j])

        lines = ax.plot(recovered, label=labels[0,1])
        handles.append(lines[0])
        lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
        lines[0].set_color(colors[i])
        legend.append(labels[0, 1])

ax.set_ylabel('# of confirmed recoveries')
ax.set_xlabel("Time (days since Jan 22, 2020)")

ax.set_yscale('log')
ax.legend(handles, legend, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4)
plt.tight_layout()
plt.savefig('results/US_generated_recoveries.png')