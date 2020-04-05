import random
# Generate offices for every agent
agent_offices = {}
for i in range(10):
    offices = []
    for j in range(random.randint(1,3)):
        office = random.randint(1,10)
        if office in offices:
            continue
        else:
            offices.append(office)
    agent_offices[i] = offices

import itertools

agent_count = len([elem for minilist in list(itertools.chain(agent_offices.values())) for elem in minilist])


# Generate rating for every zipcode:
zipcode_rating = {}
for i in range(94101, 94111):
    zipcode_rating[i] = random.randint(3,10)

import random
import scipy
# Data simulation
'''
Created a function as it would be too tedious to manually create
enough data to fit the task description
'''

# Around 20 per month
def list_house(list_date):
    
    agent_id = random.randint(1,agent_count)
    offices = [elem for minilist in list(itertools.chain(agent_offices.values())) for elem in minilist]
    office_id = offices[agent_id-1]
    size = random.randint(1500,2500) # in square feet
    bedroom_count = random.randint(1,3)
    bathroom_count = random.randint(1,2)
    zipcode = random.randint(94101, 94110)
    condition = random.randint(5,10)
    
    '''
    Price is a function of size, bedroom_count, bathroom_count, zipcode, condition

    Base price in San Francisco: $1000 per square foot
    https://www.businessinsider.com/san-francisco-housing-market-facts-rent-2019-5
    
    San Francisco prices are indeed, inhumanely expensive, 
    and I have tried my best with researched estimations
    to replicate actual prices given details about the house
    but because the assignment implies that houses be at least 100,000
    I have halved the prices
    '''
    
    reasonable = False
    while reasonable == False:
        price = 100001
        if price > 100000:
            price = 0.25*int((size*1000)*((bedroom_count+3)/6)*(bathroom_count+3/5)*(zipcode_rating[zipcode]/10)*(condition/10))
            reasonable = True
        else:
            continue

    return {'agent_id': agent_id, 
            'office_id': office_id, 
            'size': size, 
            'bedroom_count': bedroom_count, 
            'bathroom_count': bathroom_count, 
            'zipcode': zipcode, 
            'condition': condition, 
            'price': price,
            'list_date': list_date}

# Random date generator
# https://kite.com/python/answers/how-to-generate-a-random-date-between-two-dates-in-python

import datetime
import random

def date_generator(start_month, end_month):
    if start_month != 12:
        start_date = datetime.date(2019, start_month, 1)
        end_date = datetime.date(2019, end_month, 1)
    else:
        start_date = datetime.date(2019, start_month, 1)
        end_date = datetime.date(2019, start_month, 31)
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


# Final random data generator

dates = []
for month in range(1,13):
    for j in range(random.randint(10,20)):
        dates.append(date_generator(month, month+1))
dates.sort()

data = []
for date in dates:
    data.append(list_house(date))

data

import sqlalchemy 
from sqlalchemy import create_engine, Column, Text, String, Date, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker 

from datetime import datetime
import numpy as np
import names
import os

engine = create_engine('sqlite:///db_cs162.db')
engine.connect()

Base = declarative_base() 

# Location: San Francisco
# Zipcode w/ one office each: 94101 -> 94110
# Agents: 20; 
# Jean, Mark, James, Tanner, Mike, Kane, Adam, Chelsea, Sam, Alex,
# Zane, Jack, Jake, Kennedy, Amanda, Kean, Tabatha, Hiro, Ken, Dave
# Time span: January 2019 to December 2019

class Offices(Base):
    __tablename__ = "Offices"
    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    zipcode = Column(Integer)

# Can have multiple rows for multiple agents with multiple offices
class Agents(Base):
    __tablename__ = "Agents"
    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    email_address = Column(String(40))
    office_id = Column(Integer, ForeignKey('Offices.id'))

class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key = True)
    name = Column(String(20))

class ListedHouses(Base):
    __tablename__ = "ListedHouses"
    id = Column(Integer, primary_key = True)
    agent_id = Column(Integer, ForeignKey('Agents.id'))
    office_id = Column(Integer, ForeignKey('Offices.id'))
    customer_id = Column(Integer, ForeignKey('Customers.id'))
    size = Column(Integer)
    bedroom_count = Column(Integer)
    bathroom_count = Column(Integer)
    zipcode = Column(Integer)
    condition = Column(Integer)
    price = Column(Numeric(precision=9,decimal_return_scale=2))
    list_date = Column(Date)
    sold = Column(Boolean)
    
class Sales(Base):
    __tablename__ = "Sales"
    id = Column(Integer, primary_key = True)
    house_id = Column(Integer, ForeignKey('ListedHouses.id'))
    customer_id = Column(Integer, ForeignKey('Customers.id'))
    sale_date  = Column(Date)
    sale_price = Column(Numeric(precision=9,decimal_return_scale=2), ForeignKey('ListedHouses.price'))
    
# Individual commissions!
class Commissions(Base):
    __tablename__ = "Commissions"
    id = Column(Integer, primary_key = True)
    agent_id = Column(Integer, ForeignKey('Agents.id'))    
    commission = Column(Integer)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create one office per zipcode
for zipcode in range(94101, 94111):
    session.add(Offices(name=f"Office_{zipcode}", zipcode=zipcode))

try:
    session.commit()

except:
    session.rollback()
    raise

finally:
    session.close()

agents = []
while len(agents) != 10:
    new_agent = names.get_first_name()
    if new_agent not in agents:
        agents.append(new_agent)
        
Session = sessionmaker(bind=engine)
session = Session()

# Simulate agents
for agent in agents:
    for office_id in agent_offices[i]:
        session.add(Agents(name=agent, 
                           email_address=f'{agent}@yahoo.com', 
                           office_id=office_id))

try:
    session.commit()

except:
    session.rollback()
    raise

finally:
    session.close()
    
Session = sessionmaker(bind=engine)
session = Session()

# List Houses
for d in data:
    customer = names.get_first_name()
    
    if session.query(Customers.name).filter_by(name=customer).first() == None:
        session.add(Customers(name=customer))
    
    session.add(ListedHouses(agent_id=d['agent_id'], 
                            office_id=d['office_id'], 
                            customer_id=session.query(Customers.id).filter_by(name=customer).first()[0],
                            size=d['size'], 
                            bedroom_count=d['bedroom_count'],
                            bathroom_count=d['bathroom_count'],
                            zipcode=d['zipcode'],
                            condition=d['condition'],
                            price=d['price'],
                            list_date=d['list_date']))

try:
    session.commit()

except:
    session.rollback()
    raise

finally:
    session.close()

'''
Function to determine sale of every listed house

Every sale counts as one transaction where

Start:
    session = Session()
End:
    session.close()
'''

Session = sessionmaker(bind=engine)
session = Session()

# Sell Houses
for i in range(1,len(data)+1):
    
    house = session.query(ListedHouses.id, 
                          ListedHouses.customer_id,
                          ListedHouses.list_date,
                          ListedHouses.price).filter_by(id=i).first()
    
    # randomization to simulate how not all houses are sold
    if random.random()<0.7:
        session.add(Sales(house_id=house[0],
                         customer_id=house[1],
                         sale_date=house[2]+timedelta(random.uniform(5,90)),
                         sale_price=house[3]))

        session.query(ListedHouses).filter_by(id=i).first().sold = True

try:
    session.commit()

except:
    session.rollback()
    raise

finally:
    session.close()

from sqlalchemy import func

Session = sessionmaker(bind=engine)
session = Session()

count = func.count(ListedHouses.office_id).label("Count")

for i in range(1,12):
    top_5_offices = session.query(Sales.id, Offices.name, count)\
        .filter(Sales.sale_date.between(datetime(2019,i,1),datetime(2019,i+1,1)))\
        .join(ListedHouses, Sales.house_id==ListedHouses.id)\
        .join(Offices, ListedHouses.office_id==Offices.id)\
        .group_by(Offices.id)\
        .order_by(count.desc())\
        .limit(5)\
        .all()
    try:
        x = np.take(np.array(top_5_offices), 1, axis=1)
        y = [int(i) for i in np.take(np.array(top_5_offices), 2, axis=1)]
    except:
        x = 'None'
        y = 0
    
    plt.figure(figsize=(8,4))
    plt.bar(x,y)
    plt.title(f"Top 5 Offices by Sales in {calendar.month_name[i]} 2019")
    plt.xlabel("Office zipcode")
    plt.ylabel("Number of sales")
    plt.show()

count = func.count(ListedHouses.office_id).label("Count")

for i in range(1,12):
    top_5_agents = session.query(Sales.id, Agents.name, Agents.email_address, count)\
        .filter(Sales.sale_date.between(datetime(2019,i,1),datetime(2019,i+1,1)))\
        .join(ListedHouses, Sales.house_id==ListedHouses.id)\
        .join(Agents, ListedHouses.office_id==Agents.id)\
        .group_by(Agents.name)\
        .order_by(count.desc())\
        .limit(5)\
        .all()
    
    try:
        x = [str(agent) for agent in np.take(np.array(top_5_agents), 1, axis=1)]
        y = [int(count) for count in np.take(np.array(top_5_agents), 3, axis=1)]
    except:
        x = 'None'
        y = 0
    

    plt.figure(figsize=(8,4))
    plt.bar(x,y)
    plt.title(f"Top 5 Offices by Agent in {calendar.month_name[i]} 2019")
    plt.xlabel("Agent name")
    plt.ylabel("Number of sales")
    plt.show()
    
    print(''.join(f"Name: {agent[1]}, Email Address: {agent[2]}, Sales: {agent[3]}\n" for agent in top_5_agents))

'''
Apply given rules of commission
'''

Session = sessionmaker(bind=engine)
session = Session()

# Add Commission for every Sale
for s in session.query(Sale).all():

    p = s.sale_price
    
    if p < 100000:
        percent = 0.1
    elif p > 100000 and p <= 200000:
        percent = 0.075
    elif p > 200000 and p <= 500000:
        percent = 0.06
    elif p > 500000 and p <= 1000000:
        percent = 0.05
    elif p > 1000000:
        percent = 0.04
    
    session.add(Commission(agent_id=session.query(ListedHouse).all()[s.house_id-1].agent_id,
                           commission=round(percent*float(p), 2)))

try:
    session.commit()

except:
    session.rollback()
    raise

finally:
    session.close()
    
# Calculate Total Commission for every Agent
comm = func.sum(Commissions.commission).label("SumCommission")

session.query(Commissions.id, Agents.name, Commissions.commission)\
    .join(Agents, Commissions.agent_id==Agents.id)\
    .group_by(Agents.name)\
    .all()

for i in range(1,12):
    monthly_sales = session.query(Sales.id, ListedHouses.list_date, Sales.sale_date)\
        .filter(Sales.sale_date.between(datetime(2019,i,1),datetime(2019,i+1,1)))\
        .join(ListedHouses, Sales.house_id==ListedHouses.id)\
        .all()
    
    print(f"{calendar.month_name[i]} Average Listing Time: {round(np.mean([(sale[2]-sale[1]).days for sale in monthly_sales]), 2)}")

for i in range(1,12):
    monthly_sales = session.query(Sales.sale_price)\
        .filter(Sales.sale_date.between(datetime(2019,i,1),datetime(2019,i+1,1)))\
        .all()
    
    print(f"{calendar.month_name[i]} Average Selling Price: {round(np.mean([sale for sale in monthly_sales]), 2)}")

count = func.count(ListedHouses.office_id).label("Count")

for i in range(1,12):
    top_5_offices = session.query(Sales.id, Offices.zipcode, count)\
        .filter(Sales.sale_date.between(datetime(2019,i,1),datetime(2019,i+1,1)))\
        .join(ListedHouses, Sales.house_id==ListedHouses.id)\
        .join(Offices, ListedHouses.office_id==Offices.id)\
        .group_by(Offices.id)\
        .order_by(count.desc())\
        .limit(5)\
        .all()
    try:
        x = [str(i) for i in np.take(np.array(top_5_offices), 1, axis=1)]
        y = [int(i) for i in np.take(np.array(top_5_offices), 2, axis=1)]
    except:
        x = 'None'
        y = 0
    
    plt.figure(figsize=(8,4))
    plt.bar(x,y)
    plt.title(f"Top 5 Zipcodes by Sales in {calendar.month_name[i]} 2019")
    plt.xlabel("Zipcode")
    plt.ylabel("Number of sales")
    plt.show()