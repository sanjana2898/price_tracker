import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column,String,Integer,Float
import pandas as pd
import time
import plotly.express as px
from orm import Products
import scraper as sc
import json
from datetime import datetime
from send_mail import post

st.header("Product Price Tracking Automated System")
st.sidebar.title('Final yr. project at AMITY')

# connect to database
engine = create_engine('sqlite:///trackdb.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()
st.sidebar.success('database connected')
  

st.title('Instructions')
st.write('Please visit the website to select a product to track')
st.write('https://www.amazon.in/')

plot_area = st.empty()
data_area = st.empty()

product_name = st.text_input('enter the product name to show')
amz_urls = st.text_input('Enter url for amazon')
flip_urls = st.text_input('Enter url for flipkart')
myn_urls = st.text_input('Enter url for Myntra')
btn = st.button('Check tracker')
if (amz_urls or flip_urls or  myn_urls) and btn:
    df = []
    if amz_urls:
        details = sc.extract_amazon_data(amz_urls)
        df.append(details)
    
    if flip_urls:
        details = sc.extract_flipkart_data(flip_urls)
        df.append(details)
    
    if myn_urls:
        details = sc.extract_myntra_data(myn_urls)
        df.append(details)
    
    st.write(pd.DataFrame(df))

st.subheader('Run Tracker ')
time_gap = st.select_slider("How Much time difference between each tracking call",['10 sec','10 mins','1 hour','12 hours','1 day'])
btn2 = st.button('Run Tracker continously')
if (amz_urls or flip_urls or  myn_urls) and btn2:
    if time_gap == '10 sec':
        wait = 10
    elif time_gap == '10 mins':
        wait = 60 * 10
    elif time_gap == '1 hour':
        wait = 60 * 60
    elif time_gap == '12 hours':
        wait = 60 * 60 * 12
    elif time_gap == '1 day':
        wait = 60 * 60 * 24
    else:
        wait = 5

    
    dfs = []
    while True:
        if amz_urls:
            details = sc.extract_amazon_data(amz_urls)
            details['date'] = datetime.utcnow()
            product = Products(name=details['name'],
                            price=details['price'],
                            deal=details['deal'],
                            url=details['url'],
                            date= details['date'],
                            website= details['website'])
            dfs.append(details)
            sess.add(product)
            sess.commit()
        if flip_urls:
            details = sc.extract_flipkart_data(flip_urls)
            details['date'] = datetime.utcnow()
            product = Products(name=details['name'],
                            price=details['price'],
                            deal=details['deal'],
                            url=details['url'],
                            date= details['date'],
                            website= details['website'])
            dfs.append(details)
            sess.add(product)
            sess.commit()
        if myn_urls:
            details = sc.extract_myntra_data(myn_urls)
            details['date'] = datetime.utcnow()
            product = Products(name=details['name'],
                            price=details['price'],
                            deal=details['deal'],
                            url=details['url'],
                            date= details['date'],
                            website= details['website'])
            dfs.append(details)
            sess.add(product)
            sess.commit()
        
        data = pd.DataFrame(dfs)    
        data['date']=pd.to_datetime(data['date'])   
        fig = px.line(data_frame=data,x=data.index,y=data['price'],line_group='name',color='website') 
        plot_area.subheader('graphical output')
        plot_area.plotly_chart(fig)
        data_area.write(data)
        time.sleep(wait)

op = st.sidebar.checkbox("show tracked product data manually")
if op:
    try:
        df = pd.read_sql('products',engine)
        st.write(df)
    except Exception as e:
        st.error('No tracking data available')

