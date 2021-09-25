import os
from flask import render_template, url_for, request, redirect, flash, session, Flask, Response, Blueprint
from software import app
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout, LSTM
import json
from wtforms import TextField, Form
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from jinja2 import TemplateNotFound
from software.api_call import get_values
import datetime
import requests


@app.route("/")
@app.route("/home")
@app.route("/home", methods=['GET','POST'])
def home():

    prediction1=0.0
    currentprice=0.0
    symbol='.'
    rsi=0.0
    macd=0.0
    score=0.0
    score1=0.0
    title='Welcome to impish gull'
    te=0


    if request.method == 'POST':

        user = request.form['nm']
        ti12 = TimeSeries(key='0SWK3900UOOOSR7N')
        data, meta_data = ti12.get_symbol_search(keywords=user)
        if not data or data=='None':
            return render_template('notfound.html', title='NotFound')
            te=te+1
        else:
            if not data[0]['2. name'] or not data[0]['1. symbol']:
                return render_template('notfound.html', title='NotFound')
                te=te+1
            else:
                helloo=data[0]['2. name']
                symbol=data[0]['1. symbol']

                #---------------------------------------------------------------------------------------------------

                weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
                company=symbol
                api_key='0SWK3900UOOOSR7N'
                ALPHAVANTAGE_API_KEY='0SWK3900UOOOSR7N'
                # Find out what day 
                year=datetime.datetime.now().year
                month=datetime.datetime.now().month
                day=datetime.datetime.now().day
                thisXMas = datetime.date(year,month,day)
                thisXMasDay = thisXMas.weekday()
                thisXMasDayAsString = weekDays[thisXMasDay]
                d=datetime.timedelta(days = 1)
                d1=datetime.timedelta(days = 1)
                todayprice= datetime.date(year,month,day)
                todayprice1= datetime.date(2017,12,30)

                # chech if market is open 
                if thisXMasDayAsString == "Saturday":
                    d = datetime.timedelta(days = 1)
                    thisXMas = thisXMas - d
                    thisXMasDayAsString = "Friday"
                    todayprice=todayprice-d
                if thisXMasDayAsString == "Sunday":
                    d = datetime.timedelta(days = 2)
                    thisXMas = thisXMas - d
                    thisXMasDayAsString = "Friday"
                    todayprice=todayprice-d

                todaypricee = web.DataReader(company, 'av-daily', todayprice-d, api_key='0SWK3900UOOOSR7N')
                todaypricee1 = web.DataReader(company, 'av-daily', todayprice1+d1, api_key='0SWK3900UOOOSR7N')
                #

                start = dt.datetime(2012,1,1)
                end = dt.datetime(2020,1,1)

                data = web.DataReader(company, 'av-daily', start, end, api_key='0SWK3900UOOOSR7N')

                #

                scaler = MinMaxScaler(feature_range=(0,1))
                scaled_data= scaler.fit_transform(data['close'].values.reshape(-1,1))

                prediction_days = 60
                learn1 =[]
                learn2 = []

                for x in range(prediction_days, len(scaled_data)):
                    learn1.append(scaled_data[x-prediction_days:x, 0])
                    learn2.append(scaled_data[x, 0])

                learn1,learn2=np.array(learn1), np.array(learn2)
                learn1 = np.reshape(learn1,( learn1.shape[0],learn1.shape[1],1))

                #

                model=Sequential()

                model.add(LSTM(units=50, return_sequences=True, input_shape=(learn1.shape[1], 1)))

                model.add(Dropout(0.2))

                model.add(LSTM(units=50, return_sequences=True))

                model.add(Dropout(0.2))

                model.add(LSTM(units=50))

                model.add(Dropout(0.2))

                model.add(Dense(units=1))#prediction of next closing

                model.compile(optimizer='adam', loss= 'mean_squared_error')

                model.fit(learn1, learn2, epochs=1, batch_size=32)

                testingfrom=dt.datetime(2020,1,1)

                testingto = dt.datetime.now()

                test_data = web.DataReader(company, 'av-daily', testingfrom, testingto, api_key='0SWK3900UOOOSR7N' )

                actual_prices= test_data['close'].values

                total_dataset= pd.concat((data['close'], test_data['close']), axis=0)

                lstminputs = total_dataset[len(total_dataset) - len(test_data)- prediction_days:].values
                lstminputs = lstminputs.reshape(-1,1)
                lstminputs = scaler.transform(lstminputs)

                testing1 = []

                for x in range(prediction_days, len(lstminputs)):
                    testing1.append(lstminputs[x-prediction_days:x, 0])

                testing1 = np.array(testing1)
                testing1= np.reshape(testing1, (testing1.shape[0],testing1.shape[1],1))

                predicted_prices= model.predict(testing1)
                predicted_prices = scaler.inverse_transform(predicted_prices)

                #

                actualprice = [lstminputs[len(lstminputs) + 1 - prediction_days:len(lstminputs+1),0]]
                actualprice = np.array(actualprice)
                actualprice = np.reshape(actualprice, (actualprice.shape[0], actualprice.shape[1],1))

                prediction = model.predict(actualprice)
                prediction = scaler.inverse_transform(prediction)
                prediction= prediction.tolist()

                prediction1= prediction[0][0]

                todaypriceee=todaypricee.values.tolist()
                todaypriceee1=todaypricee1.values.tolist()
                currentprice= todaypriceee[0][2]
                currentprice1=todaypriceee1[0][2]

        #-------------------here goes the LSTM code--------------------------------------------

        #=====================================================================rsi
                ti1 = TechIndicators(key='0SWK3900UOOOSR7N', output_format='pandas')
                data, meta_data = ti1.get_rsi(symbol=symbol, interval='monthly', series_type='high')
                data_date_changed = data['2020-05-17':'2021-05-18']#---------------------------------------------------date
                data_date_changed=data_date_changed.values.tolist()
                if not data_date_changed:
                    return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                    te=te+1
                else:
                    data_date_changed=float(data_date_changed[-1][0])
                    rsi=data_date_changed
                    if rsi>70:
                        score=score+7
                    elif rsi<30:
                        score=score-7
                    elif 50<rsi<70:
                        score=score+5
                    elif 30<rsi<=50:
                        score=score-3    
                #-----------------------------------------------------------------------------------
                #=====================================================================macd
                    ti = TechIndicators(key='0SWK3900UOOOSR7N', output_format='pandas')
                    data, meta_data = ti.get_macd(symbol=symbol, interval='monthly', series_type='high')
                    data_date_changed = data['2020-12-31':]
                    data_date_changed1 = data['2020-05-18':]
                    #data_date_changed = data['2017-12-31':]#---------------------------------------------------date
                    ##########print(data_date_changed)
                    #data_date_changed1 = data['2016-05-18':]#---------------------------------------------------date
                    #############print(data_date_changed1)
                    data_date_changed=data_date_changed.values.tolist()
                    data_date_changed1=data_date_changed1.values.tolist()
                    ###########print(data_date_changed)
                    ##########print(data_date_changed1)
                    if not data_date_changed or data_date_changed=='None':
                        return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                        te=te+1
                    elif not data_date_changed1 or data_date_changed1=='None':
                        return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                        te=te+1
                    else:
                        macd=[float(i) for i in data_date_changed[0]][0]
                        ##############print (macd)
                        #macd=[float(i) for i in data_date_changed]
                        ##print(macd)
                        macd1=[float(i) for i in data_date_changed1[0]][0]
                        ##############print (macd1)
                        signalline=[float(i) for i in data_date_changed[0]][1]
                        signalline1=[float(i) for i in data_date_changed1[0]][1]

                        if (macd1-signalline1)==(macd-signalline):
                            score=score
                        elif (macd > signalline):
                            if(macd1-signalline1)>(macd-signalline):
                                score=score-9
                            if(macd1-signalline1)<(macd-signalline):
                                score=score+9
                            if macd1<signalline1:
                                score= score+10
                        elif (macd<signalline):
                            if (signalline1-macd1)<(signalline-macd):
                                score=score+9
                            if (signalline1-macd1)>(signalline-macd):
                                score=score-9
                            if macd1>signalline1:
                                score= score-10
                    #-----------------------------------------------------------------------------------
                    #============================================================================obv

                    #-----------------------------------------------------------------------------------
                        #============================================================================balance-sheet

                        base_url = 'https://www.alphavantage.co/query?'
                        params = {'function': 'OVERVIEW',
                                 'symbol': symbol,
                                 'apikey': '0SWK3900UOOOSR7N'}

                        response = requests.get(base_url, params=params)
                        #description=response.json()['Description']

                        params = {'function': 'BALANCE_SHEET',
                                 'symbol': symbol,
                                 'apikey': '0SWK3900UOOOSR7N'}

                        response = requests.get(base_url, params=params)
                        if not response.json()['annualReports'] or response.json()['annualReports']=='None':
                            return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                            te=te+1
                        else:
                            report=response.json()['annualReports']
                            if not report or report=='None':
                                return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                te=te+1
                            else:
                                if (not report[3]) or (report[3]=='None'):
                                    return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                    te=te+1
                                else:
                                    if not (report[3])['totalShareholderEquity'] or (report[3])['totalShareholderEquity']=='None':
                                        return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                        te=te+1
                                    else:
                                        if (not report[4]) or (report[4]=='None'):
                                            return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                            te=te+1
                                        else:                                
                                            if not (report[4])['totalShareholderEquity'] or (report[4])['totalShareholderEquity']=='None':
                                                return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                                te=te+1

                                            else:
                                                ##########print((report[4])['totalShareholderEquity'])
                                                if not (report[3])['totalCurrentAssets'] or (report[3])['totalCurrentAssets']=='None':
                                                    return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                                    te=te+1

                                                else:
                                                    if not (report[3])['totalCurrentLiabilities'] or (report[3])['totalCurrentLiabilities']=='None':
                                                        return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=11111)
                                                        te=te+1
                                                    else:
                                                        ShareholderEquity= float((report[0])['totalShareholderEquity'])
                                                        ShareholderEquity1= float((report[1])['totalShareholderEquity'])
                                                        totalcassets= float((report[0])['totalCurrentAssets'])
                                                        totalcliabilities=float((report[0])['totalCurrentLiabilities'])
                                                        #ShareholderEquity= float((report[3])['totalShareholderEquity'])#-------------------------------date its the report number(easy)
                                                        #ShareholderEquity1= float((report[4])['totalShareholderEquity'])
                                                        #totalcassets= float((report[3])['totalCurrentAssets'])
                                                        #totalcliabilities=float((report[3])['totalCurrentLiabilities'])

                                                        if ShareholderEquity>0.0:
                                                            score=score+11
                                                        else:
                                                            score-30

                                                        if ShareholderEquity1<ShareholderEquity:
                                                            score=score+11
                                                        else:
                                                            score=score-20

                                                        if (totalcassets/totalcliabilities)<1.0:
                                                            score=score-26
                                                        elif (totalcassets/totalcliabilities)>1.0:
                                                            score=score+12
                                                        elif (totalcassets/totalcliabilities)>2.0:
                                                            score=score+22
                                                        elif (totalcassets/totalcliabilities)>3.0:
                                                            score=score+32
                                                        elif (totalcassets/totalcliabilities)>4.0:
                                                            score=score+36
                                                    #---------------------------------------------------------------------income stament
                                                        
                                                        params1 = {'function': 'INCOME_STATEMENT',
                                                                 'symbol': symbol,
                                                                 'apikey': '0SWK3900UOOOSR7N'}

                                                        response1 = requests.get(base_url, params=params1)

                                                        report1=response1.json()
                                                        #print('1',report1)
                                                        report1=list(report1.values())[1]
                                                        #print('2',report1)
                                                        #report1=list(report1[0].values())
                                                        report1=list(report1[0].values())#------------------------------------------------date is the report number down to 2016 hence report max 4

                                                        #netincome= float((report1[0])['netIncome'])
                                                        #operatingincome= float((report1[0])['operatingIncome'])
                                                        #totalrevenue=float((report1[0])['totalRevenue'])

                                                        #print('3',report1)
                                                        netincome= float(report1[25])
                                                        operatingincome= float(report1[6])
                                                        totalrevenue=float(report1[3])

                                                        ##pprint(operatingincome)
                                                        ##pprint(totalrevenue)
                                                        ##pprint(netincome)

                                                        #if ((operatingincome/totalrevenue)*100)<=5:
                                                           # score=score-5
                                                        #elif 5<((operatingincome/totalrevenue)*100)<=10:
                                                            #score=score-3
                                                        #elif 10<((operatingincome/totalrevenue)*100)<=15:
                                                            #score=score-2
                                                        if 15<((operatingincome/totalrevenue)*100)<=20:
                                                            score=score+5
                                                        elif ((operatingincome/totalrevenue)*100)>20:
                                                            score=score+7

                                                        if operatingincome>0:
                                                            score=score+9
                                                        else:
                                                            score=score-15

                                                #---------------------------------------------------------------------


                                                        if score > float(int(score)):
                                                            score= score
                                                        else:
                                                            score=int(score)

                                                #--------------------------------------------------------------------

                                                        score1=score
                                                        score=0.0
                                                        return render_template('home.html', title=helloo, usr=user, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=score1)
    else:
        return render_template('home.html', title=title, prediction1=prediction1, currentprice=currentprice, symbol=symbol, rsi=rsi)

 
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("home.html")
 
if __name__ == '__main__':
    app.run(debug=True)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/scoring")
def scoring():
    return render_template('scoring.html', title='Scoring')

@app.route("/notfound")
def notfound():
    return render_template('notfound.html', title='NotFound')
