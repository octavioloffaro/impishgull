import os
from flask import render_template, url_for, request, redirect, flash, session, Flask, Response, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
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
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from jinja2 import TemplateNotFound
import datetime
import requests
import csv
import time
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000



currentprice=0.0
symbol='.'
rsi=0.0
macd=0.0
score=0.0
score1=0.0
graphs = []
graphs1 = []
te=0
counter=0
#tikers= ['MMM','AOS','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AAP','AMD','AES','AFL','A','APD','AKAM','ALK','ARE','ALB','ALXN','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','APA','AAPL','AMAT','APTV','ADM','ANET','AJG','AIZ','T','ATO','ADSK','ADP','AZO','AVB','AVY','BKR','BLL','BAC','BAX','BDX','BRK.B','BBY','BIO','BIIB','BLK','BA','BKNG','BWA','BXP','BSX','BMY','BR','BF.B','CHRW','COG','CDNS','CZR','CPB','COF','CAH','KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP','CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','COP','ED','STZ','CPRT','GLW','CTVA','COST','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DXCM','FANG','DLR','DFS','DISCA','DISCK','DISH','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DRE','DD','DXC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ENPH','ETR','EOG','EFX','EQIX','EQR','ESS','EL','ETSY','RE','EVRG','ES','EXC','EXPE','EXPD','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FISV','FLT','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','GPS','GRMN','IT','GNRC','GD','GE','GIS','GM','GPC','GILD','GPN','GL','GS','GWW','HAL','HBI','HIG','HAS','HCA','PEAK','HSIC','HES','HPE','HLT','HFC','HOLX','HD','HON','HRL','HST','HWM','HPQ','HUM','HBAN','HII','IEX','IDXX','INFO','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IFF','IP','IPG','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JKHY','J','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KHC','KR','LB','LHX','LH','LRCX','LW','LVS','LEG','LDOS','LEN','LLY','LNC','LIN','LYV','LKQ','LMT','L','LOW','LUMN','LYB','MTB','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MXIM','MKC','MCD','MCK','MDT','MRK','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MPWR','MNST','MCO','MS','MSI','MSCI','NDAQ','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NSC','NTRS','NOC','NLOK','NCLH','NOV','NRG','NUE','NVDA','NXPI','ORLY','OXY','ODFL','OMC','OKE','ORCL','OTIS','PCAR','PKG','PH','PAYX','PAYC','PYPL','PENN','PNR','PBCT','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD','PNC','POOL','PPG','PPL','PFG','PG','PGR','PLD','PRU','PTC','PEG','PSA','PHM','PVH','QRVO','QCOM','PWR','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SPG','SWKS','SNA','SO','LUV','SWK','SBUX','STT','SYK','SIVB','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','BK','CLX','COO','HSY','MOS','TRV','TMO','TJX','TSCO','TT','TDG','TRMB','TFC','TWTR','TYL','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UPS','URI','UNH','UHS','UNM','VLO','VTR','VRSN','VRSK','VZ','VRTX','VFC','VIAC','VTRS','V','VNO','VMC','WRB','WBA','WMT','WM','WAT','WEC','WFC','WELL','WST','WDC','WU','WAB','WRK','WY','WHR','WMB','WLTW','WYNN','XEL','XLNX','XYL','YUM','ZBRA','ZBH','ZION','ZTS']
tikers= ['MMM','AOS','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AAP','AMD','AES','AFL','A','APD','AKAM','ALK','ARE','ALB','ALXN','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','APA','AAPL','AMAT','APTV','ADM','ANET','AJG','AIZ','T','ATO','ADSK','ADP','AZO','AVB','AVY','BKR','BLL','BAC','BAX','BDX','BRK.B','BBY','BIO','BIIB','BLK','BA','BKNG','BWA','BXP','BSX','BMY','BR','BF.B','CHRW','COG','CDNS','CZR','CPB','COF','CAH','KMX','CCL','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP','CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG']
#tikers= ['WLTW','WYNN','XEL','XLNX','XYL','YUM','ZBRA','ZBH','ZION','ZTS']
#tikers= ['MMM','AOS','ABT','ABBV','ABMD','ACN']
j=0
print('hello')
for i in tikers:
    counter=counter+1
    user = i
    ti12 = TimeSeries(key='0SWK3900UOOOSR7N')
    data, meta_data = ti12.get_symbol_search(keywords=user)
    j=j+1
    count=(j*100)/len(tikers)
    print ('Progression: ',count ,'%')
    if not data or data=='None':
        print('nooooo')
        te=te+1
    else:
        if not data[0]['2. name'] or not data[0]['1. symbol']:
            print (nooooo)
            te=te+1
        else:
            helloo=data[0]['2. name']
            symbol=data[0]['1. symbol']

            print(symbol,helloo)


            #---------------------------------------------------------------------------------------------------
            # weekdays as a tuple

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
            #todayprice= datetime.date(year,month,day)# -----------------------------alter this for date
            todayprice= datetime.date(2019,12,30)
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

            todaypricee = web.DataReader(company, 'av-daily', todayprice+d, api_key='0SWK3900UOOOSR7N')# -------date change to newest date
            todaypricee1 = web.DataReader(company, 'av-daily', todayprice1+d1, api_key='0SWK3900UOOOSR7N')# -----date change to oldest date
            #print(type(todaypricee))

            todaypriceee=todaypricee.values.tolist()
            todaypriceee1=todaypricee1.values.tolist()
            currentprice= todaypriceee[0][2]
            currentprice1=todaypriceee1[0][2]
        #score starts here



             
        #=====================================================================rsi
            ti1 = TechIndicators(key='0SWK3900UOOOSR7N', output_format='pandas')
            data, meta_data = ti1.get_rsi(symbol=symbol, interval='monthly', series_type='high')
            data_date_changed = data['2017-05-20':'2017-12-31']#---------------------------------------------------date
            data_date_changed=data_date_changed.values.tolist()
            if not data_date_changed:
                print ('nooooooooooo')
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
                data_date_changed = data['2017-12-31':]#---------------------------------------------------date
                ##########print(data_date_changed)
                data_date_changed1 = data['2016-05-18':]#---------------------------------------------------date
                #############print(data_date_changed1)
                data_date_changed=data_date_changed.values.tolist()
                data_date_changed1=data_date_changed1.values.tolist()
                ###########print(data_date_changed)
                ##########print(data_date_changed1)
                if not data_date_changed or data_date_changed=='None':
                    print ('nooooooooooo')
                    te=te+1
                elif not data_date_changed1 or data_date_changed1=='None':
                    print ('nooooooooooo')
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

                    
                #---------------------------------------------------------------------score

                    if score > float(int(score)):
                        score= score
                    else:
                        score=int(score)


                    score1=score
                    graphs.append(score1)
                    score=0.0
                #------------------------------------------------------------------price difference

                    difference = currentprice - currentprice1
                    if difference ==0 :
                        pdifference=0
                    else:
                        pdifference = (difference*100)/currentprice1


                    ##print(pdifference)
                    graphs.append(pdifference)
                    ##print (graphs)
                    graphs1.append(graphs)
                    ##print (graphs1)
                    graphs=[]

                    #time.sleep(3)


##print (graphs1)
winsound.Beep(frequency, duration)
print ('number of stocks',counter)
print('number that were unsuccesful', te)
print('success rate', (te*100/counter))
df=pd.DataFrame(graphs1)
df.to_csv('file3.csv', index=False, header=False)