#In Pandas Series is one dimentional data structures
#Data frames are two dimentional data structures.

import pandas as pd 

#creating Sample Data frame 
col1 = ['John','Martin','Fen','Mark'] 
col2 = [26,50,55,42] 
col3 = [0,0,1,0] 
 
df1 = pd.DataFrame({'pname':col1, 'page':col2,'tested(+/-)':col3}) 

df1.shape 
df1.info() 
df1.describe() 

df1.head()      # first 5 rows
df1.head(2)     # only 2 rows of top data 
df1.tail()      # last 5  rows 

#slicing rows of frame 
df1[0:2] 
df1[0:4] 
df1[0:] 
df1[:2] 
df1[-2:] 

# slicing / access frame content by column/columns 
df1.pid 
df1['pname'] 
df1[['pname','page']] 

#Slicing/selecting subsets of rows and columns 
df1.iloc[0:2,] 
df1.iloc[[0,2],] 
df1.iloc[0:2,0] 
df1.iloc[0:2,[0,2]] 
df1.loc[0:2,['pname']] 
 
# creating new column(s) 
df1['col4'] = 0  # creating new column with all values as 0
df1['pid'] = [1,2,3,4]  # adding new coulumn with header and different values.
print(df1)

# set Coulumn as Index instaed of default index.
df1.set_index('pid').head() #setting a column as Index instaed of system index (0,1,...) just for dispaly
df1.set_index('pid',inplace=True) #index changing permanatly in DF.
print(df1)

#Extracting details by row level
#df1.ix[[1,2,3]]
#Extracting single value
#df1.ix[1,2]

# Rename/Change the columns names
df1.rename(columns={'page':'p_age','pname':'p_name'}).head() # for display change
df1.rename(columns={'page':'p_age','pname':'p_name'},inplace=True) # for display change
print(df1)

#dropping a column 
df2 = df1.drop('col4',1) 

#filtering rows of dataframe by condition 
type(df1.p_age > 50) 
df1[df1.p_age>50] 
 
# Another example
import pandas as pd
data={
      'students':['Ram','Mahesh','Vicky','Vinay','Sharma','Jay'],
      'maths':[99,94,93,98,97,93],
      'science':[96,91,96,94,98,96],
      'sports':['baseball','cricket','tt','badminton','tt','boxing']
      }

std=pd.DataFrame(data,columns=['students','maths','science','sports'])
print(std)

#Data frame with one dimention List
list1= [1,2,3,4,5,6]
ldata=pd.DataFrame(list1,columns=['Ranks'])
print(ldata)

#Data frame with multi dimentional List
list1= [[1,2,3,4,5,6],[3,4,5,7,8,9]]
ldata=pd.DataFrame(list1,columns=['l1','l2','l3','l4','l5','l6'])
print(ldata)

#Data Frames Merging files by Pandas
import pandas as pd
frame1=pd.DataFrame({'key':range(5)})

frame1=pd.DataFrame({'key':range(5),'value_1':['a','b','c','d','e']})
frame2=pd.DataFrame({'key':range(2,7),'value_2':['t','u','v','w','x']})

print(frame1)
print(frame2)

# Merge - only overlapping (common ey values will be displyed
print(pd.merge(frame1,frame2,on='key'))
#merge = pd.merge(df1,df2, on = ['key1','key2']) # merge on only specific column(s)

## Joins left, right and full (outer)
print(pd.merge(frame1,frame2,on='key',how='right'))
print(pd.merge(frame1,frame2,on='key',how='left'))
print(pd.merge(frame1,frame2,on='key',how='outer'))

# Data frames Joining. two different DataFrames details.(with out having common columns join on Index)
df1 = pd.DataFrame({'Int_rate':[2,3,6,1,2],'Ind_GDP':[50,34,55,43,61]}, index = [2006,2007,2008,2009,2010])
df2 = pd.DataFrame({'Low_tier_HPI':[50,40,60,44,56],'UNEmp_rate':[5,4,3,6,5]}, index = [2006,2008,2010,2012,2014])
joined=df1.join(df2)

##Concatenation / Union of 2 dataframes with Horizental / vertical:
print(pd.concat([frame1,frame2],sort=False))
print(pd.concat([frame1,frame2],axis=1))


#Another example for merge
df1 = pd.DataFrame({'GDP':['100','122','111','98','109'],'Emp_Growth_rate':[5.1,4.5,2.9,6.4,6.2],}, index = [2006,2007,2008,2009,2010])
df2 = pd.DataFrame({'GDP':['100','122','111','98','109'],'Emp_Growth_rate':[5.1,4.5,2.9,6.4,6.2],}, index = [2011,2012,2013,2014,2015])

merge = pd.merge(df1,df2) # all columns are same expect Index

merge = pd.merge(df1,df2, on = 'GDP') # merge on only specific column(s)
#merge = pd.merge(df1,df2, on = ['GDP','Emp_Growth_rate']) # merge on only specific column(s)

# Data munging converting one data format to another format of data.

import os
os.getcwd()
os.chdir('C:\Venkat\Personal\Trainings\Datasets')
os.getcwd()

import pandas as pd

chicago=pd.read_csv('ChicagoEmployees.csv',header=0,index_col=None) # While reading no columns are marked as index.
#chicago=pd.read_csv('ChicagoEmployees.csv',header=0,index_col=['Name']) # While reading no columns are marked as index.

chicago.head()
#headers=['Name','Title','Department','Salary', etc]
chicago=pd.read_csv('ChicagoEmployees.csv',header=0) # reading with header / with out header header=1

chicago.to_html('ChicagoEmployees.html')

######################################################################

