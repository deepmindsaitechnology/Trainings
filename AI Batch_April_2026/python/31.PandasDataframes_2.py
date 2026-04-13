#How to read data from CSV files. 
import os
os.getcwd()
os.chdir('C:\Venkat\Personal\Trainings\Datasets')

import pandas as pd
import numpy as np
# reading Without header file.
chicago=pd.read_csv('ChicagoEmployees_NoHeader.csv') # By Default consider first row as header
#chicago=pd.read_csv('ChicagoEmployees_NoHeader.csv',header=0) # By Default consider first row as header
#chicago=pd.read_csv('ChicagoEmployees_NoHeader.csv',header=1) # ignore first row and consider second row as header (this will usefull while we have extra headers
#chicago=pd.read_csv('ChicagoEmployees_NoHeader.csv',header=None) # read With out header csv file i.e all available rows will consider as data rows only.
#chicago=pd.read_csv('ChicagoEmployees_NoHeader.csv',header=None,prefix='COLUMN') # read With out header csv file i.e all available rows will consider as data rows and coulumn names will be Column1, ..

# reading options for Wit header file.
#file headers=['Name','Job Titles','Department','Full or Part-Time','Salary or Hourly','Typical Hours','Annual Salary','Hourly Rate']
chicago=pd.read_csv('ChicagoEmployees.csv') # By Default consider first row as header
#chicago=pd.read_csv('ChicagoEmployees.csv',header=0) # By Default consider first row as header
#chicago=pd.read_csv('ChicagoEmployees.csv',header=1) # ignore first row and consider second row as header (this will usefull while we have extra headers

# read file with only fixed columns and rows.
chicago=pd.read_csv('ChicagoEmployees.csv',usecols=[1,2]) # to read only some columns.
#chicago=pd.read_csv('ChicagoEmployees.csv',usecols=['Name','Department']) # with columns names to read only some columns.
#chicago=pd.read_csv('ChicagoEmployees.csv',names=['EMP Name','DEPT'],usecols=['EMP Name','DEPT']) # with columns names to read only some columns and renaming them with new names.

chicago=pd.read_csv('ChicagoEmployees.csv',nrows=6)  # to read only some rows.

# read the  file with header details either with existing columns or providing columns names.
chicago=pd.read_csv('ChicagoEmployees.csv',names=['Name','Job Titles','Department','Full or Part-Time','Salary or Hourly','Typical Hours','Annual Salary','Hourly Rate']) # with columns names to read only some columns.
#chicago=pd.read_csv('ChicagoEmployees.csv',names=['Emp_Name','Job_Title','Dept','FP_Time','Sal_Hrl','Typical_hr','Annual_sal','Hrl_Rate'],header=0) # with columns names to read only some columns.
# want to get  first 10 rows from Specific columns  
chicago['Department'].head(10)
chicago[['Department','Job Titles']].head(10)

chicago.shape
chicago.info()
chicago.describe()
chicago.head()

chicago=pd.read_csv('ChicagoEmployees.csv',names=['Emp_Name','Job_Title','Dept','FP_Time','Sal_Hrl','Typical_hr','Annual_sal','Hrl_Rate'],header=0) # with columns names to read only some columns.

# Extract the detailks from file for for part time employees and >20 work.
#Boolean  & read values based on condition. 
#"Full or Part-Time = 'P' and Typical Hours > 20 "
chicago[['FP_Time','Typical_hr']].head() # First 5 rows for gievn columns only
chicago.FP_Time == 'P'   # Boolean out come
chicago_PT_Employees = chicago[(chicago.FP_Time == 'P') & (chicago.Typical_hr > 20) ] # data set with condition true

# Write to new csv/txt and read back
chicago_PT_Employees.head()
chicago_PT_Employees.to_csv('chicago_PT_Employees.csv')
newcsv=pd.read_csv('chicago_PT_Employees.csv',header=0,names=['EName','Designation','Branch'],usecols=[1,2,3])
print(newcsv)

#*****************************************

chicago=pd.read_csv('ChicagoEmployees.csv',names=['Emp_Name','Job_Title','Dept','FP_Time','Sal_Hrl','Typical_hr','Annual_sal','Hrl_Rate'],header=0) # with columns names to read only some columns.
chicago=pd.read_csv('Student.csv',names=['RNO','Name','MATH','SCIENCE','ENGLISH','SPORTS'],header=0) # with columns names to read only some columns.

chicago.shape
chicago.describe()
chicago.describe(include=['object']) # Only to describe string columns.
chicago.describe(include='all')

chicago.head()

# process on statistical & other functions functions. 
chicago.sum() # default axis = 0 , Sum of all rows into single (number will add and string will concatinate)
chicago.sum(1) # here axis = 1 , Sum of all columns into single (number will add and ignore strings)
chicago.mean() # takes all the rows and get the average for numerical columns
chicago.mean(1) # takes all the numerical columns for each row and get the average.
chicago[['MATH','SCIENCE','ENGLISH']].mean(1)

# Group by agreegate or spliting DataFrame
chicago.groupby('SPORTS')  # Group by with single column
chicago.groupby('SPORTS').groups # to get groups

grouped = chicago.groupby('SPORTS') 
grouped.get_group('Tennis')  # to get only specific group

for sport,group in grouped: # to print the details at group level like report.
   print (sport)
   print (group)
#chicago.groupby('Name',axis=1).groups # to get groups
chicago.groupby(['SPORTS','Name']) # Group by with single column
chicago.groupby(['SPORTS','Name']).groups

chicago.groupby('SPORTS').count()

grouped = chicago.groupby('SPORTS') 
grouped.size() # Size of each group.
grouped.size() # Size of each group.
grouped.agg(np.size) # Size of each group aggregate (for all columns)

grouped['MATH'].agg(np.mean) # MATH mean for SPORTS group level. 

grouped['MATH'].agg([np.sum, np.mean, np.std])


# sorting and order the columns
chicago.sort_index()
chicago.sort_index(ascending=False) # sorting on index
chicago.sort_index(axis=1) # sorting on columns heading (alphabetic order of columns)
chicago.sort_index(ascending=False,axis=1)

chicago.sort_values(by='Name') # sort by column name
chicago.sort_values(by=['Name','MATH'])

# Geeting Unique values in Columns
chicago.SPORTS.unique()

# Working on Dates & Times series data
pd.date_range('1/1/2020', periods=5) # Default Day frequency
pd.date_range('31/1/2020', periods=5,freq='M')

s = pd.Series(pd.date_range('2012-1-1', periods=3, freq='D'))
td = pd.Series([ pd.Timedelta(days=i) for i in range(3) ])
df = pd.DataFrame(dict(A = s, B = td))

#Filter on DataFrame 
chicago.groupby('SPORTS').filter(lambda x : len(x)>3) # get only >3 occurances from SPORTS grp.


# Check input file data, Drop missing data and replace input data with appropriate data values.

df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f','h'],
                  columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) # reindexing to inser NA values 

df['one'].isnull()
df['one'].notnull()
df['one'].sum() # all NAs will consider as 0 for sum.

#droping Missing data (NA)
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f','h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
df.dropna()
df.dropna(axis=1) # dropping of total Column
df

#Filling with generic values
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f','h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

df['one'].fillna(0) # to fill for specific coloumn.
df.fillna(0) # to change all NA values to 0 in the df.
df.fillna(method='ffill') # NA values will fill with before values fill/pad are the methoids same.
df.fillna(method='bfill') # NA values will fill with after values(back fill) bfill/backfill are the methoids same.

#replace with generic values
df = pd.DataFrame({'one':[10,20,30,40,50,2000], 'two':[1000,0,30,40,50,60]})
df.replace({1000:10,2000:60})


