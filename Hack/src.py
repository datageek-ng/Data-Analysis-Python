import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
a = pd.read_csv('sleep_data.csv')

a['Date'] = pd.to_datetime(a['Date'])
a['day_of_week'] = a['Date'].dt.weekday_name

# function for averaging duration of sleep by day of the week
def day_avg(day_of_week):
  b= a[(a['day_of_week']==day_of_week)]
  c=b.mean()
  return (c['Duration']*60)

#print(day_avg('Saturday'))
# making weekday columns
def w1(row):
    if (row['day_of_week'] == 'Monday') | (row['day_of_week'] =='Tuesday') | (row['day_of_week'] == 'Wednesday') | (row['day_of_week'] =='Thursday') | (row['day_of_week'] =='Friday'):
        val = 1
        return val
    else:
        val=0
        return val
#Then apply it to your dataframe passing in the axis=1 option:
a['weekday'] = a.apply(w1, axis=1)
#print(a.head())

#computing weekday_mean
weekday_mean = a[(a['weekday'] == 1)].mean()
weekday_avg = (weekday_mean['Duration'])*60
print("Average minutes of sleep per weekday "+str(weekday_avg))

# computing weekend_mean
weekend_mean = a[(a['weekday'] == 0)].mean()
weekend_avg = (weekend_mean['Duration'])*60
print("Average minutes of sleep per weekend "+str(weekend_avg))


#average by day of the week
print("Averages by day in minutes: \n")
print("Monday - "+str(day_avg("Monday")))
print("Tuesday - "+str(day_avg("Tuesday")))
print("Wednesday - "+str(day_avg("Wednesday")))
print("Thursday - "+str(day_avg("Thursday")))
print("Friday - "+str(day_avg("Friday")))
print("Saturday - "+str(day_avg("Saturday")))
print("Sunday - "+str(day_avg("Sunday")))

# Transforming and cleansing data
a.rename(columns={'Got up': 'Got_up', 'How quickly fell asleep': 'How_quickly_fell_asleep', 'How easy got up':'How_easy_got_up', 'How felt afterwards' : 'How_felt_afterwards'}, inplace=True)

a['Slept']=pd.to_datetime(a['Slept'], format='%H:%M')
a['Got_up']=pd.to_datetime(a['Got_up'], format='%H:%M')
#a['Date'].dt.day

a['Slept']=pd.to_datetime(dict(year=a['Date'].dt.year,month=a['Date'].dt.month, day=a['Date'].dt.day, hour=a['Slept'].dt.hour, minute=a['Slept'].dt.minute))
a['Got_up']=pd.to_datetime(dict(year=a['Date'].dt.year,month=a['Date'].dt.month, day=a['Date'].dt.day, hour=a['Got_up'].dt.hour, minute=a['Got_up'].dt.minute))


# Applying Sleep duration definition
def w2(row):
    if (row['Duration'] < 1):
        return 'Very Short' 
    elif((row["Duration"]>=1) and (row["Duration"]<2) ):
        return 'Short'  
    elif((row["Duration"]>=2) and (row["Duration"]<4) ):
        return 'Medium'
    elif((row["Duration"]>=4) and (row["Duration"]<=7) ):
        return 'Long'
    elif(row["Duration"]>7):
        return 'Very Long'     
      
#Then apply it to your dataframe passing in the axis=1 option:
a['Duration_type'] = a.apply(w2, axis=1)


a['start_hour']=a['Slept'].dt.hour
print(a.head())

#Applying time of the day definition on start time 
def w3(row):
    #start_hour = row['Slept'].dt.hour
    if(row['start_hour'] >=4 and row['start_hour']< 8 ):
        return 'Early-Morning' 
    elif(row['start_hour'] >=8 and row['start_hour'] < 12 ):
        return 'Morning'  
    elif(row['start_hour'] >=12 and row['start_hour'] < 16 ):
        return 'Afternoon' 
    elif(row['start_hour'] >=16 and row['start_hour'] < 21 ):
        return 'Evening' 
    elif (row['start_hour'] >=21 and row['start_hour'] <=23 ):
        return 'Night'
    elif (row['start_hour'] >=0 and row['start_hour'] < 4 ):
        return 'Mid-Night'
        
      
#Then apply it to your dataframe passing in the axis=1 option:
a['Day_type_start'] = a.apply(w3, axis=1)

#print(a.head())

#drilling weekday data
wd = a[(a['weekday']==1)]
#print(wd.head())

#drilling weekend data
we = a[(a['weekday']==0)]
#print(we.head())


#finding frequency of type of sleeps on weekdays and weekends

#print((wd['Duration_type'].value_counts()/5))
#print((we['Duration_type'].value_counts()/2))

# function for calculating average sleep time at given time of the day
def avg_sleep_time(time_day):
  print("Overall average "+time_day+" sleep in hours:"+ str(a[(a['Day_type_start']== time_day)]['Duration'].mean()))
  print("Weekday average "+time_day+" sleep in hours:"+ str(wd[(wd['Day_type_start']== time_day)]['Duration'].mean()))
  print("Weekend average "+time_day+" sleep in hours:"+ str(we[(we['Day_type_start']== time_day)]['Duration'].mean()))

avg_sleep_time("Early-Morning")
avg_sleep_time("Morning")
avg_sleep_time("Afternoon")
avg_sleep_time("Evening")
avg_sleep_time("Night")
avg_sleep_time("Mid-Night")


# function for calculating average sleep time at given type of sleep
def avg_sleep_type(sleep_type):
  print("Overall average "+sleep_type+" sleep in hours:"+ str(a[(a['Duration_type']== sleep_type)]['Duration'].mean()))
  print("Weekday average "+sleep_type+" sleep in hours:"+ str(wd[(wd['Duration_type']== sleep_type)]['Duration'].mean()))
  print("Weekend average "+sleep_type+" sleep in hours:"+ str(we[(we['Duration_type']== sleep_type)]['Duration'].mean()))

avg_sleep_type("Very Short")
avg_sleep_type("Short")
avg_sleep_type("Medium")
avg_sleep_type("Long")
avg_sleep_type("Very Long")





#wd[(wd[(wd['Day_type_start'] == "Early-Morning")]['Duration_type'] == 'Very Short')]['Duration'].mean()

#wd.groupby(('Day_type_start','Duration_type'))["Duration"].mean()

#print(a.groupby(('weekday','Day_type_start','Duration_type'))["Duration"].mean())
#print('\n')
#print(a.groupby(('day_of_week','Day_type_start','Duration_type'))["Duration"].mean())
#


#print(a.groupby(('weekday','Day_type_start','Duration_type'))["Duration"].count())
#print('\n')
#g = a.groupby(('day_of_week','Day_type_start','Duration_type'))["Duration"].count()


#overall difference stats

resu2 = a.groupby(('weekday'))["Duration"].mean()*60
print(resu2)

# difference in mean duration with regrds to start sleep time

resu = a.groupby(('Day_type_start','weekday'))["Duration"].mean()*60
print(resu)
#pl1 = resu.plot()
#plt.show()



# % of sleep types based on weekday and Weekend

resu3 = (a.groupby(('weekday'))['Duration_type'].value_counts()/a.groupby(('weekday'))['Duration_type'].count())*100 


#same analysis with weekdays
res1 = a.groupby(('day_of_week'))['Duration'].mean()*60
print(res1)

#difference based on sleep start time
res2 = a.groupby(('day_of_week', 'Day_type_start'))['Duration'].mean()*60
print(res2)


#% of slep types based on all days of week
res3 = (a.groupby(('day_of_week'))['Duration_type'].value_counts()/a.groupby(('day_of_week'))['Duration_type'].count())*100 
print(res3)


# overall mean of all categories
over_res = (a.groupby(('day_of_week', 'Day_type_start', 'Duration_type'))['Duration'].mean())*60


#gx = a.groupby(('day_of_week', 'Day_type_start'))['How_quickly_fell_asleep'].mean().idxmax()

#def mean_min(row):
#  return mean(row)*60

#print(a.groupby(('day_of_week','Day_type_start','Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'}))

#print(a.groupby(('weekday','Day_type_start','Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'}))
#print(a.groupby(('weekday','Day_type_start', 'Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'}))


# One final DataFrame for all averages on reqd attributes

# with respect to weekday and weekend
new_wd = pd.DataFrame(a.groupby(('weekday','Day_type_start', 'Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 

new_wd['How_easy_got_up'].idxmin()

# with respect to days of the week
new_d = pd.DataFrame(a.groupby(('day_of_week','Day_type_start', 'Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 
(' '.join(new_d['How_quickly_fell_asleep'].idxmax()))+' period'

a.head()

    
    
    
    












