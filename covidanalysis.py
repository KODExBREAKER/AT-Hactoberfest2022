#!/usr/bin/env python
# coding: utf-8

# In[54]:


from tkinter import *
from tkinter.ttk import *
import requests
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import seaborn as sns


# In[55]:


fname="covid-19-data.csv"
data_url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
data=requests.get(data_url).content
csv_file=open(fname,"wb")
csv_file.write(data)
csv_file.close()
df=pd.read_csv(fname)


# In[56]:


total_cases=df.groupby('location')['new_cases'].sum()
total_cases=total_cases.sort_values(ascending=False)
most_affected_c=total_cases[1:11].index
cases=total_cases[1:11].values
total_deaths=df.groupby('location')['new_deaths'].sum()
deaths=total_deaths[most_affected_c].values
cases_death_df=pd.DataFrame({'Country':most_affected_c,'Total Cases':cases,'Total Death':deaths})
print(cases_death_df)


# In[57]:


def topTen():
    plot_data=pd.melt(cases_death_df,id_vars=['Country'],value_vars=['Total Cases','Total Death']
                     ,var_name='Metric',value_name='Case Count')
    plt.figure(figsize=(12,5))
    sns.barplot(x='Country',hue='Metric',y='Case Count',data=plot_data)
    plt.show()


# In[58]:


def topTenTesting():
    total_test=df.groupby('location')['new_tests'].sum().values
    population=df.groupby('location')['population'].nth(-1)
    testing_rate=(total_test/population).sort_values(ascending=False)[:10]
    plt.figure(figsize=(12,5))
    sns.barplot(x=testing_rate.values,y=testing_rate.index,orient="h")
    plt.show()
    


# In[59]:


def countryCompare():
    country1="India"
    country2="China"
    country1_data=df.loc[df['location']==country1]
    country1_cases=country1_data[['date','total_cases']]
    country2_data=df.loc[df['location']==country2]
    country2_cases=country2_data[['date','total_cases']]
    datewise_cases=country1_cases.merge(country2_cases,how='inner',on='date')
    plt.figure(figsize=(12,8))
    plt.plot(datewise_cases['date'].values,datewise_cases['total_cases_x'].values,color='blue',label=country1)
    plt.plot(datewise_cases['date'].values,datewise_cases['total_cases_y'].values,color='red',label=country2)
    plt.xticks([datewise_cases['date'][i] if i%15==0 else '' for i in range(len(datewise_cases.index))],rotation=45)
    plt.legend()
    plt.xlabel("Date");
    plt.ylabel("Rate of Covid Cases")
    plt.show()
    


# In[60]:


def factor():
    df_corr=pd.DataFrame(most_affected_c.values,columns=['Country'])
    df_corr['Total Cases']=cases
    
    pop_density=df.groupby('location')['population_density'].nth(-1)
    df_corr['Population Density']=pop_density[most_affected_c].values
    
    median_age=df.groupby('location')['median_age'].nth(-1)
    df_corr['Median Age']=median_age[most_affected_c].values
    
    diabetes_prevalence=df.groupby('location')['diabetes_prevalence'].nth(-1)
    df_corr['Diabetes']=diabetes_prevalence[most_affected_c].values
    
    stringency_index=df.groupby('location')['stringency_index'].nth(-1)
    df_corr['Stringency Index']=stringency_index[most_affected_c].values
    
    cardiovasc_death_rate=df.groupby('location')['cardiovasc_death_rate'].nth(-1)
    df_corr['Death Rate']=cardiovasc_death_rate[most_affected_c].values
    
    aged_70_older=df.groupby('location')['aged_70_older'].nth(-1)
    df_corr['Age 70 Or Older']=aged_70_older[most_affected_c].values
    heat=pd.DataFrame({"Correlation Values":df_corr.corr()['Total Cases'].values},
                     index=df_corr.corr()['Total Cases'].index)
    sns.heatmap(heat,annot=True)
    plt.show()


# In[ ]:


frame=Tk()
frame.geometry('600x500')
frame.resizable(0,0)
frame.title("Covid-19 Analysis")
st=Style()
b1=Button(frame,text="Top Ten Country" ,command=topTen)
b1.pack(pady=5)
b2=Button(frame,text="Top Ten Testing" ,command=topTenTesting)
b2.pack(pady=5)
b3=Button(frame,text="Compare Two Country" ,command=countryCompare)
b3.pack(pady=5)
b4=Button(frame,text="Correlation Factor" ,command=factor)
b4.pack(pady=5)
frame.mainloop()


# In[ ]:




