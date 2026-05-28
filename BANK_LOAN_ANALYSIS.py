#!/usr/bin/env python
# coding: utf-8

# #  BANK LOAN ANALYSIS REPORT

# ###   Import Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px


# In[2]:


df =pd.read_excel("C:/Users/KIIT0001/Downloads/financial_loan_data_excel.xlsx")


# In[4]:


df.head()


# In[5]:


df.tail()


# ###  Metadata of Data

# In[6]:


print("No. of rows:",df.shape[0])


# In[7]:


print("No. of columns:",df.shape[1])


# ###  Data types

# In[8]:


df.dtypes


# In[9]:


df.describe()


# ###  Total Loan Applications

# In[10]:


total_loan_applications =df['id'].count()
print("Total Loan Applications:",total_loan_applications)


# ###  MTD Total Loan Applications

# In[11]:


latest_issue_date =df['issue_date'].max()
latest_year =latest_issue_date.year
latest_month =latest_issue_date.month

mtd_data =df[(df['issue_date'].dt.year ==latest_year) & (df['issue_date'].dt.month ==latest_month)]

mtd_loan_applications =mtd_data['id'].count()

print(f"MTD Loan Applications (for {latest_issue_date.strftime('%B %Y')}):{mtd_loan_applications} ")


# ###  Total Funded Amount

# In[12]:


total_funded_amount = df['loan_amount'].sum()
total_funded_amount_millions =total_funded_amount/1000000
print("Total Funded Amount: ${:.2f}M".format(total_funded_amount_millions))


# ###  MTD- Total Funded Amount

# In[13]:


latest_issue_date =df['issue_date'].max()
latest_year =latest_issue_date.year
latest_month =latest_issue_date.month

mtd_data =df[(df['issue_date'].dt.year ==latest_year) & (df['issue_date'].dt.month ==latest_month)]

mtd_total_funded_amount = mtd_data['loan_amount'].sum()
mtd_total_funded_amount_millions= mtd_total_funded_amount/1000000

print(" MTD Total Funded Amount: ${:.2f}M".format(mtd_total_funded_amount_millions))


# ###  Total  Amount Received

# In[16]:


total_amount_received = df['total_payment'].sum()
total_amount_received_millions =total_amount_received/1000000
print("Total Amount Received: ${:.2f}M".format(total_amount_received_millions))


# ###  MTD Total Amount Received

# In[17]:


latest_issue_date =df['issue_date'].max()
latest_year =latest_issue_date.year
latest_month =latest_issue_date.month

mtd_data =df[(df['issue_date'].dt.year ==latest_year) & (df['issue_date'].dt.month ==latest_month)]

mtd_total_amount_received = mtd_data['total_payment'].sum()
mtd_total_amount_received_millions= mtd_total_amount_received/1000000

print(" MTD Total  Amount Received: ${:.2f}M".format(mtd_total_amount_received_millions))


# ###  Average Interest Rate

# In[22]:


average_interest_rate = df['int_rate'].mean()*100
print("Average Interest Rate:{:.2f}%" .format(average_interest_rate))


# ###  Average Debt-to-Income Ratio (DTI)

# In[23]:


average_dti = df['dti'].mean()*100
print("Average DTI:{:.2f}%" .format(average_dti))


# ###  Good Loan Metrics

# In[26]:


good_loans=df[df['loan_status'].isin(["Fully Paid","Current"])]

total_loan_applications = df['id'].count()

good_loan_applications =good_loans['id'].count()
good_loan_funded_amount =good_loans['loan_amount'].sum()
good_loan_received =good_loans['total_payment'].sum()

good_loan_funded_amount_millions=good_loan_funded_amount/1000000
good_loan_received_millions= good_loan_received/1000000

good_loan_percentage = (good_loan_applications/total_loan_applications)*100

print("Good Loan Applications:",good_loan_applications)
print("Good Loan Funded Amount (in millions):${:.2f}M" .format(good_loan_funded_amount_millions))
print("Good Loan total Received (in millions):${:.2f}M".format(good_loan_received_millions))
print("Percentage of Good Loan Applications :{:.2f}%".format(good_loan_percentage))


# ###  Bad Loan Metrics

# In[27]:


bad_loans=df[df['loan_status'].isin(["Charged Off"])]

total_loan_applications = df['id'].count()

bad_loan_applications =bad_loans['id'].count()
bad_loan_funded_amount =bad_loans['loan_amount'].sum()
bad_loan_received =bad_loans['total_payment'].sum()

bad_loan_funded_amount_millions=bad_loan_funded_amount/1000000
bad_loan_received_millions= bad_loan_received/1000000

bad_loan_percentage = (bad_loan_applications/total_loan_applications)*100

print("Bad Loan Applications:",bad_loan_applications)
print("Bad Loan Funded Amount (in millions):${:.2f}M" .format(bad_loan_funded_amount_millions))
print("Bad Loan total Received (in millions):${:.2f}M".format(bad_loan_received_millions))
print("Percentage of Bad Loan Applications :{:.2f}%".format(bad_loan_percentage))


# ###  Monthly Trends by Issue Date for Total Funded Amount

# In[31]:


monthly_funded = (
    df.sort_values('issue_date')
      .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
      .groupby('month_name',sort=False)['loan_amount']
      .sum()
      .div(1000000)
      .reset_index(name='loan_amount_millions')

)

plt.figure(figsize=(10,5))
plt.fill_between(monthly_funded['month_name'],monthly_funded['loan_amount_millions'],color='skyblue',alpha=0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['loan_amount_millions'],color='blue',linewidth=2)

for i,row in monthly_funded.iterrows():
    plt.text(i,row['loan_amount_millions'] + 0.1,f"{row['loan_amount_millions']:.2f}",
             ha='center',va='bottom',fontsize=9,rotation=0,color='black')
    
plt.title('Total Funded Amount by Month',fontsize=14)
plt.xlabel('Month')
plt.ylabel('Funded Amount($ Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'], rotation=45)
plt.grid(True,linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()




# ###  Monthly Trends by issued Date for Total Amount Received

# In[34]:


monthly_received = (
   df.sort_values('issue_date')
     .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
     .groupby('month_name',sort=False)['total_payment']
     .sum()
     .div(1000000)
     .reset_index(name='received_amount_millions')

)

plt.figure(figsize=(10,5))
plt.fill_between(monthly_received['month_name'],monthly_received['received_amount_millions'],color='lightgreen',alpha=0.5)
plt.plot(monthly_received['month_name'],monthly_received['received_amount_millions'],color='green',linewidth=2)

for i,row in monthly_received.iterrows():
   plt.text(i,row['received_amount_millions'] + 0.1,f"{row['received_amount_millions']:.2f}",
            ha='center',va='bottom',fontsize=9,rotation=0,color='black')
   
plt.title('Total Received Amount by Month',fontsize=14)
plt.xlabel('Month')
plt.ylabel('Received Amount($ Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'], rotation=45)
plt.grid(True,linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()





# ###  Monthly Trends by Issue date for Total Loan Applications

# In[38]:


monthly_applications = (
   df.sort_values('issue_date')
     .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
     .groupby('month_name',sort=False)['id']
     .count()
     .reset_index(name='loan_applications_count')

)

plt.figure(figsize=(10,5))
plt.fill_between(monthly_applications['month_name'],monthly_applications['loan_applications_count'],color='orange',alpha=0.5)
plt.plot(monthly_applications['month_name'],monthly_applications['loan_applications_count'],color='darkorange',linewidth=2)

for i,row in monthly_applications.iterrows():
   plt.text(i,row['loan_applications_count'] + 0.5,f"{row['loan_applications_count']}",
            ha='center',va='bottom',fontsize=9,rotation=0,color='black')
   
plt.title('Total Loan Applications by Month',fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Applications')
plt.xticks(ticks=range(len(monthly_applications)), labels=monthly_applications['month_name'], rotation=45)
plt.grid(True,linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()




# ###  Regional Analysis by State for Total Funded Amount

# In[40]:


state_funding = df.groupby('address_state')['loan_amount'].sum().sort_values(ascending=True)
state_funding_thousands = state_funding /1000

plt.figure(figsize=(10,8))
bars = plt.barh(state_funding_thousands.index,state_funding_thousands.values,color='lightcoral')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10,bar.get_y() + bar.get_height() / 2, f'{width:,.0f}K' ,va='center',fontsize=9)

    
plt.title('Total Funded Amount by State (in $ Thousands)')
plt.xlabel('Funded Amount ($ \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ### Regional Analysis by State for Total  Amount Received

# In[42]:


state_received = df.groupby('address_state')['total_payment'].sum().sort_values(ascending=True)
state_received_thousands = state_received /1000

plt.figure(figsize=(10,8))
bars = plt.barh(state_received_thousands.index,state_received_thousands.values,color='lightblue')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10,bar.get_y() + bar.get_height() / 2, f'{width:,.0f}K' ,va='center',fontsize=9)

    
plt.title('Total  Amount Received by State (in $ Thousands)')
plt.xlabel(' Amount Received ($ \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ###  Regional Analysis by State for Total Loan Applications

# In[44]:


state_applications = df.groupby('address_state')['id'].sum().sort_values(ascending=True)
state_applications_thousands = state_applications /1000

plt.figure(figsize=(10,8))
bars = plt.barh(state_applications_thousands.index,state_applications_thousands.values,color='lightgreen')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10,bar.get_y() + bar.get_height() / 2, f'{width:,.0f}K' ,va='center',fontsize=9)

    
plt.title('Total  Loan Applications by State (in $ Thousands)')
plt.xlabel(' Loan Applications ( \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ###  Loan Term Analysis by Total Funded Amount

# In[45]:


term_funding_millions = df.groupby('term')['loan_amount'].sum() /1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_funding_millions,
    labels=term_funding_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum(term_funding_millions)/100:.1f}M",startangle=90,
    wedgeprops={'width':0.4}

)
plt.gca().add_artist(plt.Circle((0,0),0.70,color='white'))
plt.title("Total Funded Amount by Term (in $ Millions)")
plt.show()


# ### Loan Term Analysis by Total Amount Received

# In[46]:


term_received_millions = df.groupby('term')['total_payment'].sum() /1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_received_millions,
    labels=term_received_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum(term_received_millions)/100:.1f}M",startangle=90,
    wedgeprops={'width':0.4}

)
plt.gca().add_artist(plt.Circle((0,0),0.70,color='white'))
plt.title("Total Amount Received by Term (in $ Millions)")
plt.show()


# ###  Loan Term Analysis by Total Loan Applications

# In[52]:


term_applications_thousands = df.groupby('term')['id'].count()

plt.figure(figsize=(5,5))
plt.pie(
    term_applications_thousands,
    labels=term_applications_thousands.index,
    autopct=lambda p: f"{p:.1f}%\n{p*sum(term_applications_thousands)/100:.0f}",startangle=90,
    wedgeprops={'width':0.4}

)
plt.gca().add_artist(plt.Circle((0,0),0.70,color='white'))
plt.title("Total Loan Applications by Term (in Thousands)")
plt.show()


# ### Employee Length by Total Funded Amount

# In[9]:


emp_funding= df.groupby('emp_length')['loan_amount'].sum() 
emp_funding_thousands = emp_funding.sort_values()/1000
plt.figure(figsize=(10,6))
bars=plt.barh(emp_funding_thousands.index,emp_funding_thousands,color='purple')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"${width:,.0f}K", va= 'center',fontsize=9)
    
plt.xlabel("Funded Amount ($ Thousands)")
plt.title("Total Funded Amount by Employment Length")
plt.grid(axis='x',linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()


# ###  Employee Length by Total Amount Received

# In[10]:


emp_received= df.groupby('emp_length')['total_payment'].sum() 
emp_received_thousands = emp_received.sort_values()/1000
plt.figure(figsize=(10,6))
bars=plt.barh(emp_received_thousands.index,emp_received_thousands,color='purple')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"${width:,.0f}K", va= 'center',fontsize=9)
    
plt.xlabel("Amount Received ($ Thousands)")
plt.title("Total  Amount Received by Employment Length")
plt.grid(axis='x',linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()


# ###  Employee Length by Total Loan Applications

# In[14]:


emp_loan_applications= df.groupby('emp_length')['id'].count() 
emp_loan_applications_thousands = emp_loan_applications.sort_values()
plt.figure(figsize=(10,6))
bars=plt.barh(emp_loan_applications.index,emp_loan_applications,color='purple')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"{width:,.0f}", va= 'center',fontsize=9)
    
plt.xlabel("Loan Aplications ( Thousands)")
plt.title("Total  Number of Loan Applications by Employment Length")
plt.grid(axis='x',linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()


# ###  Loan Purpose By Total funded Amount

# In[15]:


emp_funding= df.groupby('purpose')['loan_amount'].sum() 
emp_funding_millions = emp_funding.sort_values()/1000000
plt.figure(figsize=(10,6))
bars=plt.barh(emp_funding_millions.index,emp_funding_millions,color='skyblue')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"${width:,.2f}M", va= 'center',fontsize=9)
    
plt.title(" TotalFunded Amount by Loan Purpose ($ Millions)",fontsize=14)
plt.xlabel(" Funded Amount ($ Millions)")
plt.ylabel=('Loan Purpose')
plt.grid(axis='x',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ###  Loan Purpose By Total Amount Received

# In[16]:


emp_received= df.groupby('purpose')['total_payment'].sum() 
emp_received_millions = emp_received.sort_values()/1000000
plt.figure(figsize=(10,6))
bars=plt.barh(emp_received_millions.index,emp_received_millions,color='lightcoral')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"${width:,.2f}M", va= 'center',fontsize=9)
    
plt.title(" Total Received Amount by Loan Purpose ($ Millions)",fontsize=14)
plt.xlabel(" Received Amount ($ Millions)")
plt.ylabel=('Loan Purpose')
plt.grid(axis='x',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ###  Loan Purpose By Total Loan Applications

# In[18]:


emp_loan_applications= df.groupby('purpose')['id'].count() 
emp_loan_applications_thousands = emp_loan_applications.sort_values()
plt.figure(figsize=(10,6))
bars=plt.barh(emp_loan_applications_thousands.index,emp_loan_applications_thousands,color='green')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5,bar.get_y() + bar.get_height() /2, 
            f"{width:,.0f}", va= 'center',fontsize=9)
    
plt.title(" Total Loan Applications by Loan Purpose (thousands)",fontsize=14)
plt.xlabel("Loan Applications (Thousands)")
plt.ylabel=('Loan Purpose')
plt.grid(axis='x',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ###  Home Ownership by Total Funded Amount

# In[ ]:


home_funding = df.groupby('home_ownership')['loan_amount'].sum().reset_index()
home_funding['loan_amount_millions']=home_funding['loan_amount']/1000000

fig = px.treemap(
    home_funding,
    path=['home_ownership'],
    values= 'loan_amount_millions',
    color= 'loan_amount_millions',
    color_continuous_scale ='Blues',
    title='Total Funded Amount by Home Ownership($ Millions)'
)

fig.show()


# ###  Home Ownership by Total Amount Received

# In[23]:


home_received = df.groupby('home_ownership')['total_payment'].sum().reset_index()
home_received['total_payment_millions']=home_received['total_payment']/1000000

fig = px.treemap(
    home_received,
    path=['home_ownership'],
    values= 'total_payment_millions',
    color= 'total_payment_millions',
    color_continuous_scale ='greens',
    title='Total Amount  Received by Home Ownership($ Millions)'
)

fig.show()


# ###  Home Ownership by Total Loan Applications

# In[1]:


home_total_applications = df.groupby('home_ownership')['id'].count().reset_index()
home_total_applications['id_thousands']=home_total_applications['id']
fig = px.treemap(
    home_total_applications,
    path=['home_ownership'],
    values= 'id_thousands',
    color= 'id_thousands',
    color_continuous_scale ='blues',
    title='Total Loan Applications by Home Ownership '
)

fig.show()


# In[ ]:




