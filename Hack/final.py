
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


print('\nAnalysis based on Duration')

#overall difference stats
print('\naverage based on 1-weekday/0-weekend ')
resu2 = a.groupby(('weekday'))["Duration"].mean()
print(resu2)
re2df = pd.DataFrame(resu2)
re2df['we']=pd.Series(['weekend','weekday'])
print(re2df.head())
re2df.plot(x='we', y='Duration', kind='bar')
plt.title('Average sleep in hours based on weekdays and weekends')
plt.show()


# difference in mean duration with regrds to start sleep time

print('\naverage based on 1-weekday/0-weekend and the time of the day at sleep start')
resu = a.groupby(('Day_type_start','weekday'))["Duration"].mean()*60
print(resu)
resudf=pd.DataFrame(resu)
resudf.plot(kind='barh')
plt.title('Weekday, Sleepstart vs Duration in mins')
plt.show()
#pl1 = resu.plot()
#plt.show()



# % of sleep types based on weekday and Weekend
print('\naverage % of sleepn based on 1-weekday/0-weekend and the type of Duration')
resu3 = (a.groupby(('weekday'))['Duration_type'].value_counts()/a.groupby(('weekday'))['Duration_type'].count())*100 
print(resu3)
res3df=pd.DataFrame(resu3)
res3df.plot(kind='barh')
plt.title('weekday/weekend,duration type vs percentage of type')
plt.show()

print('\n \nAnalysis based on Duration with individual days')
#same analysis with weekdays
print('\naverage based on days of the week')
res1 = a.groupby(('day_of_week'))['Duration'].mean()*60
print(res1)
res1df = pd.DataFrame(res1)
res1df.plot(kind='barh')
plt.title('Day of week vs duration in minutes')
plt.show()


#difference based on sleep start time
print('\naverage based on individualweek days and the time of the day at sleep start')
res2 = a.groupby(('day_of_week', 'Day_type_start'))['Duration'].mean()*60
print(res2)
res2df=pd.DataFrame(res2)
res2df.plot(kind='barh')
plt.title('Day of week, Start time vs Duration in mins')
plt.show()

#% of slep types based on all days of week
print('\naverage % of sleepn based on individual days of the week and the type of Duration')
res3 = (a.groupby(('day_of_week'))['Duration_type'].value_counts()/a.groupby(('day_of_week'))['Duration_type'].count())*100 
print(res3)
res3df=pd.DataFrame(res3)
res3df.plot(kind='barh')
plt.title('Day of week, length of sleep vs percentage in total')
plt.show()

# overall mean of all categories
#over_res = (a.groupby(('day_of_week', 'Day_type_start', 'Duration_type'#))['Duration'].mean())*60

# One final DataFrame for all averages on reqd attributes
print('\nAnalysis on how quickly fell asleep')
# with respect to weekday and weekend
new_wd = pd.DataFrame(a.groupby(('weekday','Day_type_start')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 


# with respect to days of the week
new_d = pd.DataFrame(a.groupby(('day_of_week','Day_type_start')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 
print('\nHow_quickly_fell_asleep on individual days')
print(new_d['How_quickly_fell_asleep'])


print('\nHow_quickly_fell_asleep on weekdays/weekends')
print(new_wd['How_quickly_fell_asleep'])
print('\n')

new_d.plot(kind='barh')
plt.show()
new_wd.plot(kind='barh')
plt.show()



print('\nAnalysis on How easily got up')
new_wd = pd.DataFrame(a.groupby(('weekday','Day_type_start', 'Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 


# with respect to days of the week
new_d = pd.DataFrame(a.groupby(('day_of_week','Day_type_start', 'Duration_type')).agg({'Duration': 'mean', 'How_quickly_fell_asleep' : 'mean', 'How_easy_got_up': 'mean', 'How_felt_afterwards': 'mean'})) 

print('\nHow_easy_got_up on individual days')
print(new_d['How_easy_got_up'])
print('\nHow_easy_got_up on weekdays/weekends')
print(new_wd['How_easy_got_up'])
print('\n')



print('\nAnalysis on How_felt_afterwards')
print('\nHow_felt_afterwards on individual days')
print(new_d['How_felt_afterwards'])
print('\nHow_felt_afterwards on weekdays/weekends')
print(new_wd['How_felt_afterwards'])
print('\n')


new_d.plot(kind='barh')
plt.show()
new_wd.plot(kind='barh')
plt.show()




#new_wd['How_easy_got_up'].idxmin()
#(' '.join(new_d['How_quickly_fell_asleep'].idxmax()))+' period'