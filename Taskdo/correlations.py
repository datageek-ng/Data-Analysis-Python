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


#print(data_copy.info())
#print(data_copy.head(5))

#intel

def f(row):
    if row['Type of Task'] == 'Intellectual (e.g. study, read, do homework, write a paper, watch documentary, etc.)':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['Intellectual'] = data_copy.apply(f, axis=1)

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
data_copy['Start_time'] = data_copy['Start Time']
data_copy['End_time'] = data_copy['End Time']





#morning_data = data_copy.set_index('Start Time').between_time('08:00:00', '11:59:59')

#print(list(morning_data.index))
#for entry in (morning_data.index.tolist()):
#    for i in range(data_copy.size):
#         if (data_copy.iloc[i,4] == entry):
#            data_copy.iloc[i]['Time of the Day'] = "Morning"
# print(morning_data.head())

#coverting according to date time
times = list([0,4,8,12,16,20])
labels = ['midnight','early-morning','morning', 'afternoon', 'evening', 'night']
periods = dict(zip(times, labels))

def period(row):
    visit_start = {'hour': row.Start_time.hour, 'min': row.Start_time.minute} # get hour, min of visit start
    visit_end = {'hour': row.End_time.hour, 'min': row.End_time.minute} # get hour, min of visit end
    for period_start, label in periods.items():
        period_end = period_start + 4
        if period_start <= visit_start['hour'] < period_end:
            if period_start <= visit_end['hour'] < period_end or (period_end - visit_start['hour']) * 60 - visit_start['min'] > (visit_end['hour'] - period_end) * 60 + visit_end['min']:
                return label
            else:
                return periods[period_end] # assign label of following period

data_copy['period'] = data_copy.apply(period, axis=1)

def a1(row):
    if row['period'] == 'midnight':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['midnight'] = data_copy.apply(a1, axis=1)


def a2(row):
    if row['period'] == 'early-morning':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['early-morning'] = data_copy.apply(a2, axis=1)

def a3(row):
    if row['period'] == 'morning':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['morning'] = data_copy.apply(a3, axis=1)

def a4(row):
    if row['period'] == 'afternoon':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['afternoon'] = data_copy.apply(a4, axis=1)



def a5(row):
    if row['period'] == 'evening':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['evening'] = data_copy.apply(a5, axis=1)


def a6(row):
    if row['period'] == 'night':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['night'] = data_copy.apply(a6, axis=1)


def b1(row):
    if row['Indoor or Outdoor?'] == 'Indoor':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['indoor'] = data_copy.apply(b1, axis=1)

def b2(row):
    if row['Indoor or Outdoor?'] == 'Outdoor':
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['outdoor'] = data_copy.apply(b2, axis=1)






corr = data_copy.corr(method='pearson')






# function for creating and column of multiple task types with respect to time and location
def create_multi_period(column):
    data_copy[column+' early-morning'] = (data_copy[column]) & (data_copy['early-morning'])
    data_copy[column+' morning'] = (data_copy[column]) & (data_copy['morning'])
    data_copy[column + ' afternoon'] = (data_copy[column]) & (data_copy['afternoon'])
    data_copy[column + ' evening'] = (data_copy[column]) & (data_copy['evening'])
    data_copy[column + ' night'] = (data_copy[column]) & (data_copy['night'])
    data_copy[column + ' midnight'] = (data_copy[column]) & (data_copy['midnight'])
    data_copy[column + ' indoor'] = (data_copy[column]) & (data_copy['indoor'])
    data_copy[column + ' outdoor'] = (data_copy[column]) & (data_copy['outdoor'])
create_multi_period('Intellectual')
create_multi_period('Physical')
create_multi_period('Spiritual')
create_multi_period('Fitness')
create_multi_period('Social')


data_copy['Date'] = pd.to_datetime(data_copy['Date'])
data_copy['day_of_week'] = data_copy['Date'].dt.weekday_name




def w1(row):
    if (row['day_of_week'] == 'Monday') | (row['day_of_week'] =='Tuesday') | (row['day_of_week'] == 'Wednesday') | (row['day_of_week'] =='Thursday') | (row['day_of_week'] =='Friday'):
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['weekday'] = data_copy.apply(w1, axis=1)


def w2(row):
    if (row['day_of_week'] == 'Monday') | (row['day_of_week'] =='Tuesday') | (row['day_of_week'] == 'Wednesday') | (row['day_of_week'] =='Thursday') | (row['day_of_week'] =='Friday'):
        val = 0
        return val
    else:
        val=1
        return val
#Then apply it to your dataframe passing in the axis=1 option:
data_copy['weekend'] = data_copy.apply(w2, axis=1)







corr = data_copy.corr(method='pearson')

corr.to_excel('new.xlsx')

data_copy.to_excel('new2.xlsx')

def optimal(time_of_the_day):
    corr_slice = corr[time_of_the_day]
    corr_slice_1 = corr_slice.iloc[1:6]
    corr_slice_2 = corr_slice.iloc[13:15]
    type1 = corr_slice_1.idxmax()
    type2 = corr_slice_2.idxmax()
    return type1+' '+type2




print('Best Task type for Morning time with respect to occurence:'+ optimal('morning'))
print('Best Task type for Afternoon time with respect to occurence:'+ optimal('afternoon'))
print('Best Task type for Evening time with respect to occurence:'+ optimal('evening'))
print('Best Task type for Night time with respect to occurence:'+ optimal('night'))

print("\n")
print("\n")

# it is done for intellectual tasks, similarly can be done for other task types too
def optimal_Intel_time():
    corr_slice = corr.iloc[15:21,0]
    type1 = corr_slice.idxmax()
    return type1[12:]

def optimal_Intel_location():
    corr_slice = corr.iloc[21:23,0]
    type1 = corr_slice.idxmax()
    return type1[12:]


print("Best time for intellectual tasks with respect to completion:"+optimal_Intel_time())
print("Best location for intellectual tasks with respect to completion:"+optimal_Intel_location())






