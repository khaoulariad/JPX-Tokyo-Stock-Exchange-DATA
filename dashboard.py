from dbEngine.dbEngine import DbEngine
from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


def performAction(engine, connection, option1, option2, start, end):

    # Perform some action based on the selected options
    query = text(f"select SecuritiesCode from stock_list where Name = '{option1}';")
    r = connection.execute(query)
    i = r.fetchall()[0][0]
    query = text(f"select * from stock_prices where SecuritiesCode = {i};")
    r = connection.execute(query)
    data = pd.DataFrame(r.fetchall())
    if(len(data)!=0):
        if start > end:
            st.error('start date can not be less than end date')
        else:
            data = data[(data['Date'] >= pd.to_datetime(start)) & (data['Date'] <= pd.to_datetime(end))]
            if(len(data)!=0):
                st.subheader(f"Historical chart of {option1}")
                if option2 == 'ALL':
                    fig = go.Figure()
                    yColumns = ['Open', 'Close', 'High','Low']
                    for col in yColumns:
                        fig.add_trace(go.Scatter(x=data['Date'], y=data[col], mode='lines', name=col))
                    
                    st.plotly_chart(fig)
                else:
                    plotdata = data[['Date',option2]]
                    fig = px.line(plotdata, x='Date', y=option2, title='Stock Values Over Time')
                    st.plotly_chart(fig)
            else:
                st.error('no data for this date range')
    else:
        st.write('no data available')

# Initialize the database engine and connection
dbEngine = DbEngine()
engine = dbEngine.createDbengine()
connection = engine.connect()

# Query to get all stock names
query = text('select Name from stock_list;')
r = connection.execute(query)
stockCodes = np.unique([i[0] for i in r.fetchall()])
prices = ['Open', 'Close', 'High', 'Low', 'ALL']

# Streamlit app
st.title('Stocks Historical Prices')

# Dropdown for selecting stock code and price option
codeSelected = st.selectbox('Select Stock', stockCodes)
priceSelected = st.selectbox('Select OHLC Price', prices)

# Date inputs for selecting date range
defaultStartDate = datetime(2017, 1, 4)
defaultEndDate = datetime(2021, 12, 3)
col1, col2 = st.columns(2)
with col1:
    startDate = st.date_input('Start Date', value=defaultStartDate)
with col2:
    endDate = st.date_input('End Date', value=defaultEndDate)

# Button to plot the selected data
if st.button('Plot'):
    performAction(engine, connection, codeSelected, priceSelected, startDate, endDate)