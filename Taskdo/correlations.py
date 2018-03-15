import pandas as pd
import numpy as np
data = pd.read_csv('data.csv')
data_copy= data.copy()

#for getting a common format for the hours
for i in range(data_copy['Start Time'].size):
    if(len(data_copy['Start Time'][i]) == 5):
        data_copy['Start Time'][i] = data_copy['Start Time'][i]+':00'

# for getting common format for the hours
for i in range(data_copy['End Time'].size):
    if(len(data_copy['End Time'][i]) == 5):
        data_copy['End Time'][i] = data_copy['End Time'][i]+':00'


#conversion into date time index and calculating the duration
data_copy['Start Time'] = pd.to_datetime(data_copy['Start Time'],format="%H:%M:%S")
data_copy['End Time'] = pd.to_datetime(data_copy['End Time'],format="%H:%M:%S")
data_copy['Duration'] = data_copy['End Time'] - data_copy['Start Time']
data_copy['Refined Percentage'] = data_copy['Percentage of Successful Completion']/2
#morning_data = data_copy.set_index('Start Time').between_time('08:00:00', '11:59:59')

#print(list(morning_data.index))
#for entry in (morning_data.index.tolist()):
#    for i in range(data_copy.size):
#         if (data_copy.iloc[i,4] == entry):
#            data_copy.iloc[i]['Time of the Day'] = "Morning"

print(data_copy.info())
print(data_copy.head(5))

#intel

def f(row):
    if row['Type of Task'] == 'Intellectual (e.g. study, read, do homework, write a paper, watch documentary, etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Intel'] = data_copy.apply(f, axis=1)

def g(row):
    if row['Type of Task'] == 'Physical Work (e.g. House Maintenance, Gardening etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Physical'] = data_copy.apply(g, axis=1)

def h(row):
    if row['Type of Task'] == 'Spiritual (e.g. Meditation, Prayers etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Spiritual'] = data_copy.apply(h, axis=1)

def i(row):
    if row['Type of Task'] == 'Fitness and Health (eg: Swimming, Jogging, Workout etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Fitness'] = data_copy.apply(i, axis=1)

def j(row):
    if row['Type of Task'] == 'Social Activity (e.g. Parents, Kids etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Social'] = data_copy.apply(j, axis=1)







data_copy = data_copy.drop('Percentage of Successful Completion', axis=1)
data_copy['Duratime'] = pd.to_numeric(data_copy['Duration'], errors='raise')
data_copy['Duratime'] = data_copy['Duratime']/60000000000
print(data_copy.head(20))

corr = data_copy.corr(method='pearson')
print(corr)
