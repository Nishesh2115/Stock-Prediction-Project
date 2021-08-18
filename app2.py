#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:11:04 2021

@author: nisheshgogia
"""


import logging
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, datetime, timedelta
from st_aggrid import GridOptionsBuilder, AgGrid
import base64
import logging
import xgboost as xgb
import pickle


def get_stock_ticker_summary(stock):#done
    try:
        print(f"Preparing data for {stock}")
        ticker = yf.Ticker(stock)
        market_cap = get_market_cap(ticker.info['marketCap'])
        df_holders = ticker.institutional_holders
        holders=''
        if df_holders is not None:
            holders = [{row['Holder']: f"{round(row['% Out'] * 100, 2)}%"} for index, row in df_holders.iterrows()]

        stock_detail = {
            'Region': ticker.info['market'],
            'Exchange': ticker.info['exchange'],
            'Symbol': stock,
            'Name': ticker.info['shortName'],
            'Sector': ticker.info['sector'],
            'Industry': ticker.info['industry'],
            'Marketcap': market_cap,
            'InstitutionalHolders': holders
            
        }
        return stock_detail
    except Exception as e:
        stock_detail = {
            'Region': '',
            'Exchange': '', 'Symbol': stock,
            'Name': '', 'Sector': stock,
            'Industry': '', 'Marketcap': stock,
            'InstitutionalHolders': stock
        }
        return stock_detail

def download_data(stock_list):#done
    df1=pd.DataFrame()
    for stock in stock_list:
        logging.info(f"Downloading data for {stock}")
        df = yf.download(stock, start=from_date, end=to_date)
        
        df['Symbol'] = stock
        stocks_sum = get_stock_ticker_summary(stock)
        stocks_sum = pd.json_normalize(stocks_sum)
        df_sum = pd.DataFrame(stocks_sum)
        a=df.merge(df_sum,how='outer',on='Symbol')
        a['Date']=df.index
        df1=df1.append(a)

    df1=df1[['Date','Open', 'High', 'Low', 'Close', 'Volume', 'Symbol',
       'Region', 'Exchange', 'Name', 'Sector', 'Industry', 'Marketcap',
       'InstitutionalHolders']]
    df1.reset_index(drop=True,inplace=True)
    return df1
   
def get_data(stock_list):#done
    pd.options.display.float_format = "{:,.2f}".format
    da=download_data(stock_list)
    loaded_model=pickle.load(open('finalizedxgboost_modelfn21.sav', 'rb'))
    ML_Recommendation=loaded_model.predict(da[['Close','Open', 'High', 'Low','Volume']].values)
    da['Recommendation']=ML_Recommendation

    da=da[['Date','Open', 'High', 'Low', 'Close', 'Volume','Recommendation','Symbol',
       'Region', 'Exchange', 'Name', 'Sector', 'Industry', 'Marketcap',
       'InstitutionalHolders']]
    da = da.round(decimals=2)
    #print(da[['Date','Open', 'High', 'Low', 'Close', 'Volume', 'Recommendation','Symbol']])

    return da


def get_market_cap(marketcap):#done
    if marketcap:
        marketcap_billions = marketcap / 1000000000
        if marketcap_billions >= 10:
            market_cap = "Largecap"
        elif marketcap_billions >= 2 and marketcap_billions < 10:
            market_cap = "Midcap"
        elif marketcap_billions >= .25 and marketcap_billions < 2:
            market_cap = "Smallcap"
        elif marketcap_billions < .25:
            market_cap = "Microcap"
        return market_cap
    else:
        return 'Unknown'

st.set_page_config(layout="wide")


#@st.cache(allow_output_mutation=True, ttl=60 * 60)
@st.cache(suppress_st_warning=True,allow_output_mutation=True, ttl=60 * 60)


def run_script():
    st.title('Stocks Entry/Exit Predictor')

    choice = ['CurrentDay', 'Last 7 days', 'Last 30 days']


    num_days = st.sidebar.radio("Select your Choice", choice)

    stocks = st.text_input("Enter the Stock(s) code separated by comma.", 'wipro.ns')
    stock_list = list(stocks.upper().split(","))
    day_of_week = datetime.today().strftime('%A')
    
    
    global from_date
    
    
    if num_days == 'CurrentDay':
       if day_of_week == 'Sunday':
           from_date = datetime.today().date() + timedelta(days=-2)
       elif day_of_week == 'Saturday':
           from_date = datetime.today().date() + timedelta(days=-1)
       else:
           from_date = datetime.today().date() + timedelta(days=0)

   
    if num_days == 'Last 7 days':
        from_date = datetime.today().date() + timedelta(days=-7)
    elif num_days == 'Last 30 days':
        from_date = datetime.today().date() + timedelta(days=-30)
        

    global to_date
    to_date=date.today()



    df = get_data(stock_list)
    df=df[['Date','Open', 'High', 'Low', 'Close', 'Volume','Recommendation','Symbol',
       'Region', 'Exchange', 'Name', 'Sector', 'Industry', 'Marketcap',
       'InstitutionalHolders']]
    df = df.round(decimals=2)

    
    st.dataframe(df)
    
    
    
    coded_data = base64.b64encode(df.to_csv(index=False).encode()).decode()
    st.markdown(
        f'<a href="data:file/csv;base64,{coded_data}" download="data.csv">Download Data</a>',
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    run_script()
    



    