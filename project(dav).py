# -*- coding: utf-8 -*-
"""PROJECT(dav).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_6RWLWPhi1-Je9tUDWvHYlVYqTqTq_zU
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')

airlinedata = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Airline data set (1).csv')

airlinedata.info()

airlinedata

## Check for wrong or unrealistic entry

for i in airlinedata.iloc[:,2:].columns:
    print(airlinedata[i].value_counts())
    print('='*25)

airlinedata.shape

## value counts or unique counts of 'id' column is same as number of records, it means there is no duplicate 'id'.

airlinedata['id'].value_counts().sum()

airlinedata.drop('Unnamed: 0', axis=1, inplace=True)

airlinedata.info()

#command removes all rows with missing values from the airlinedata DataFrame and modifies the DataFrame in place.
airlinedata.dropna(inplace=True)

airlinedata.isnull().sum()

airlinedata

airlinedata.describe()

## Select Passengers of age equal to 16 or more than 16.
airlinedata=airlinedata[airlinedata['Age']>=16]

# Lower and Upper fence range of Departure delay
q1_of_departure=np.percentile(airlinedata['Departure Delay in Minutes'],25)
q3_of_departure=np.percentile(airlinedata['Departure Delay in Minutes'],75)
iqr_of_departure=q3_of_departure-q1_of_departure
lower_fence_of_departure_delay=q1_of_departure-(1.5*iqr_of_departure)
upper_fence_of_departure_delay=q3_of_departure+(1.5*iqr_of_departure)

# Lower and Upper fence range of Arrival delay
q1_of_arrival=np.percentile(airlinedata['Arrival Delay in Minutes'],25)
q3_of_arrival=np.percentile(airlinedata['Arrival Delay in Minutes'],75)
iqr_of_arrival=q3_of_arrival-q1_of_arrival
lower_fence_of_arrival_delay=q1_of_arrival-(1.5*iqr_of_arrival)
upper_fence_of_arrival_delay=q3_of_arrival+(1.5*iqr_of_arrival)

# Remove Outliers (Outside the Lower and Upper fence range)
airlinedata=airlinedata[airlinedata['Departure Delay in Minutes']>lower_fence_of_departure_delay]
airlinedata=airlinedata[airlinedata['Departure Delay in Minutes']<upper_fence_of_departure_delay]
airlinedata=airlinedata[airlinedata['Arrival Delay in Minutes']>lower_fence_of_arrival_delay]
airlinedata=airlinedata[airlinedata['Arrival Delay in Minutes']<upper_fence_of_arrival_delay]

airlinedata.describe()

airlinedata.head(5)

airlinedata.columns

#This code calculates and prints the percentage distribution of passenger satisfaction levels from the airlinedata DataFrame.
satisfaction=round(airlinedata['satisfaction'].value_counts(normalize=True)*100,2)
print('Satisfaction or Dissatisfaction among the passengers',satisfaction)

#The plot shows how departure delays affect passenger satisfaction by displaying counts of delays with satisfaction levels differentiated by color.
plt.figure(figsize=(12,6))
sns.countplot(data=airlinedata[airlinedata['Departure Delay in Minutes']>0], x='Departure Delay in Minutes', hue='satisfaction')
plt.title('Departure delay impact on satisfaction')
plt.show()

# Arrival delay time impact on satisfaction of the passengers

plt.figure(figsize=(12,6))
sns.countplot(data=airlinedata[airlinedata['Arrival Delay in Minutes']>0], x='Arrival Delay in Minutes', hue='satisfaction')
plt.title('Arrival delay impact on satisfaction')
plt.show()

# Arrival delay impact on type of travllers

plt.figure(figsize=(6,4))
sns.countplot(data=airlinedata[airlinedata['Arrival Delay in Minutes']>5], x='Type of Travel', hue='satisfaction')
plt.title('Arrival delayed more than 5 minutes impact on type of travllers')
plt.show()

# Impact of arrival delay on loyal and disloyal Business travellers satisfaction.

plt.figure(figsize=(6,4))
sns.countplot(data=airlinedata[(airlinedata['Arrival Delay in Minutes']>5) & (airlinedata['Type of Travel']=='Business travel')], x='Customer Type', hue='satisfaction')
plt.title('Impact of arrival delay on loyal and disloyal business travellers satisfaction')
plt.show()

no_wifi=airlinedata[airlinedata['Inflight wifi service']==0]
no_online_booking=airlinedata[airlinedata['Ease of Online booking']==0]
no_online_boarding=airlinedata[airlinedata['Online boarding']==0]

# Inflight wifi service not available by class

print('Passengers report NO wifi')
print('Total','     ',no_wifi.count()['Inflight wifi service'])
print('-'*25)
print('Ratio of Class passengers who report no wifi')
print(round(no_wifi['Class'].value_counts()/airlinedata['Class'].value_counts()*100,2) )
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_wifi['Class'].value_counts()/airlinedata['Class'].value_counts(), labels=['Business','Eco','Eco Plus'], autopct='%1.2f%%')
plt.title('Share of ratio of class passengers who report no wifi')
plt.show()

airlinedata.columns

# Pivot table of those preferred Class who report no Inflight wifi service

pt_no_wifi=airlinedata[airlinedata['Inflight wifi service']==0].pivot_table(values='Inflight wifi service', index='satisfaction', columns='Class', aggfunc='count')
pt_no_wifi=round(pt_no_wifi/airlinedata[airlinedata['Inflight wifi service']==0]['Inflight wifi service'].count()*100,2)

# Heat map of pt_no_wifi

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_wifi, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of preferred class who reported no Inflight wifi service')
plt.show()

## Online booking service not available by type of travellers

print('Passengers report NO Online booking service')
print('Total','     ',no_online_booking.count()['Ease of Online booking'])
print('-'*25)
print('Ratio of Type of travellers who report No Online booking')
print(round(no_online_booking['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts()*100,2))
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_online_booking['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts(), labels=['Business travel','Personal Travel'], autopct='%1.2f%%')
plt.title('Share of ratio of Type of travellers who report No Online booking')
plt.show()

pt_no_online_booking=airlinedata[airlinedata['Ease of Online booking']==0].pivot_table(values='Ease of Online booking', index='satisfaction', columns='Type of Travel', aggfunc='count')
pt_no_online_booking=round(pt_no_online_booking/airlinedata[airlinedata['Ease of Online booking']==0]['Ease of Online booking'].count()*100,2)

## Heat map of pt_no_online_booking

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_online_booking, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of travellers who reported no Online booking service')
plt.show()

#This code snippet reports the count and ratio of travelers who report no online boarding service, and visualizes the ratio as a pie chart.
print('Passengers report NO Online boarding service')
print('Total','     ',no_online_boarding.count()['Online boarding'])
print('-'*25)
print('Ratio Type of travellers who report No Online boarding')
print(round(no_online_boarding['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts()*100,2))
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_online_boarding['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts(), labels=['Business travel','Personal Travel'], autopct='%1.2f%%')
plt.title('Share of ratio Type of travellers who report No Online boarding')
plt.show()

# Pivot table of those Travellers who report no online boarding service

pt_no_online_boarding=airlinedata[airlinedata['Online boarding']==0].pivot_table(values='Online boarding', index='satisfaction', columns='Type of Travel', aggfunc='count')
pt_no_online_boarding=round(pt_no_online_boarding/airlinedata[airlinedata['Online boarding']==0]['Online boarding'].count()*100,2)

## Heat map of pt_no_online_booking

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_online_boarding, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of travellers who reported no Online boarding service')
plt.show()

# Airline Amenities with mode (Most Frequent) of rating equal to 3 or less than 3 ( General )

for i in airlinedata.iloc[:,7:21]:
    if airlinedata[i].mode()[0]<=3:
        print(i,'Most frequent Rating: ',airlinedata[i].mode()[0])
        print('-'*25)

airlinedata[['Inflight wifi service', 'Ease of Online booking', 'Gate location']].describe()

# Count plot of Inflight wifi rating

plt.figure(figsize=(6,4))
sns.countplot(data= airlinedata[airlinedata['Inflight wifi service']!=0], x='Inflight wifi service', palette='rocket' )
plt.title('Count plot of inflight wifi service')
plt.show()

# Which Class give what rating to in flight wifi service

plt.figure(figsize=(8,4))
sns.countplot(data=airlinedata[airlinedata['Inflight wifi service']!=0], hue='Inflight wifi service', x='Class', palette='rocket')
plt.title('Preferred Class rating distribution of Inflight wifi service')
plt.show()

# Count plot of Ease of Online booking rating

plt.figure(figsize=(6,4))
sns.countplot(data= airlinedata[airlinedata['Ease of Online booking']!=0], x='Ease of Online booking', palette='rocket')
plt.title('Count plot of Ease of Online booking')
plt.show()

# Which Class give what rating to in flight wifi service

plt.figure(figsize=(8,5))
sns.countplot(data=airlinedata[airlinedata['Ease of Online booking']!=0], hue='Ease of Online booking', x='Type of Travel', palette='rocket')
plt.title('Type of travellers rating distribution of Ease of online booking')
plt.show()

# Mean rating of particular amenity is small then 3 by Class and type of travellers

print('Mean of Ratings of amenities by class and type of travellers ( any mean of rating smaller than 3)')
print('')
for i in airlinedata.iloc[:,7:21]:
    pt=airlinedata[airlinedata[i]!=0].pivot_table(values=i, index='Class', columns='Type of Travel', aggfunc='mean', margins=True, margins_name='Total')
    if i == 'Gate location':
        continue
    if np.any(pt.values<3):
        print(i)
        print('-'*25)
        print(pt)
        print('='*25)

#Travellers rating distribution on Online boarding

plt.figure(figsize=(8,4))
sns.countplot(data=airlinedata[airlinedata['Online boarding']!=0], hue='Online boarding',x='Type of Travel', palette='rocket')
plt.title('Type of Travellers rating distribution on Online boarding')
plt.show()

#'Online boarding' feature across different types of travelers, excluding those with a rating of zero, using a specific color palette.
plt.figure(figsize=(8,4))
sns.boxplot(data=airlinedata[airlinedata['Online boarding']!=0], hue='Type of Travel', x='Online boarding', y='Type of Travel', palette='rocket')
plt.title('Type of Travellers rating distribution on Online boarding')
plt.show()

#the distribution of "Online boarding" ratings across different "Type of Travel" categories, highlighting the differences between them.
plt.figure(figsize=(8, 4))
sns.lineplot(data=airlinedata[airlinedata['Online boarding'] != 0],
             x='Type of Travel',
             y='Online boarding',
             hue='Type of Travel',
             palette='rocket',
             marker='o',
             ci=None)  # 'ci=None' removes the confidence interval bands
plt.title('Type of Travellers rating distribution on Online boarding')
plt.show()

#the "Online boarding" feature, categorized by the "Type of Travel" (e.g., Business or Personal), highlighting how different types of travelers rate their online boarding experience.
plt.figure(figsize=(8,4))
sns.histplot(data=airlinedata[airlinedata['Online boarding']!=0], hue='Online boarding', x='Type of Travel', palette='rocket', multiple="stack")
plt.title('Type of Travellers rating distribution on Online boarding')
plt.show()

import seaborn as sns

# Creating a catplot
# to show the distribution of travel types in relation to online boarding usage.
sns.catplot(
    data=airlinedata[airlinedata['Online boarding'] != 0],
    x='Type of Travel',
    hue='Online boarding',
    kind='count',
    palette='rocket',
    height=4,
    aspect=2
)

plt.title('Type of Travellers Rating Distribution on Online Boarding')
plt.show()

