# -*- coding: utf-8 -*-
"""
Project: Money saver assessment tool
Started in April 2022
@author: Etienne Auroux
"""

import pandas as pd
import numpy as np
import re
import math
import plotly.graph_objects as go

def check_format(country_choice,money_start,money_goal,time_goal):
    message='ok'
    
    data_sheet=pd.read_excel('countries_and_rates.xlsx',sheet_name='Rates',skiprows=1)
    data_values=data_sheet.values
    countries=data_values[:,0]
    
    if country_choice not in countries:
        message='country_not_in_list'
    
    count_amount=0
    try:
        int(money_start)
    except ValueError:
        message='format_money_start'
        count_amount+=1
    try:
        int(money_goal)
    except ValueError:
        message='format_money_goal'
        count_amount+=1
    if count_amount==2:
        message='format_money_both'
        
    if count_amount==0:
        if int(money_goal)<=0:
            message='money_goal<=0'
        elif int(money_start)<0:
            message='money_start<0'
        elif int(money_goal)<=0 and int(money_start)<0:
            message='money_both<=0'
        elif int(money_goal)<=int(money_start):
            message='goal<=start'
     
    pattern=r'[^A-Za-z0-9]+'
    time_goal=re.sub(pattern,'',time_goal)
    time_goal=time_goal.replace('s','')
    time_goal=time_goal.lower()
    time_words='year'
    period_index=-1
    index=time_goal.find(time_words)
    if index!=-1:
        period_index=index
    elif period_index==-1:
        try:
            int(time_goal)
        except ValueError:
            message='format_period'
    
    if count_amount!=0 and message=='format_period':
        message='amount_period'
          
    return message

#From now, all functions assume message='ok' was the result of check_format
def user_choice(country_choice): #usa uk don't work, will go away if dropdown
    data_sheet=pd.read_excel('countries_and_rates.xlsx',sheet_name='Rates',skiprows=1)
    data_values=data_sheet.values
    countries=data_values[:,0]
    
    country_choice=country_choice.lower()
    
    if country_choice=='usa':
        country_choice='united states of america'
    elif country_choice=='uk':
        country_choice='united kingdom'
    
    for i in range(len(countries)):
        if countries[i].lower()==country_choice:
            choice=data_values[i,:]
            break
        else:
            choice=np.zeros(8)
    
    return choice

def period_transform(time_goal):
    pattern=r'[^A-Za-z0-9]+'
    time_goal=re.sub(pattern,'',time_goal)
    time_goal=time_goal.replace('s','')
    time_goal=time_goal.lower()
    time_words='year'
    index=time_goal.find(time_words)
    if index!=-1:
        period=int(time_goal[:index])
        period_index=index
        
        try:
            int(time_goal[:period_index])
        except ValueError:
            period=int(time_goal[:period_index])+1
    else:
        period=int(time_goal)
            
    unit='year'
      
    return unit,period

def calibration_xaxis(time_goal):
    unit,period=period_transform(time_goal)
    
    x_label='Time ('+unit+'s)'
            
    if period%10==0:
        x_tick=np.arange(0,period+0.1*period,0.1*period)
    elif period%10!=0 and period%5==0:
        x_tick=np.arange(0,period+0.2*period,0.2*period)
    elif period%10!=0 and period%5!=0 and period%3==0:
        x_tick=np.arange(0,round(period+(1/6)*period),round((1/6)*period))
    elif period%10!=0 and period%5!=0 and period%3!=0 and period%2==0:
        x_tick=np.arange(0,period+0.25*period,0.25*period)
    else:
        x_tick=np.arange(0,round(period+0.2*period),round(0.2*period))
    
    x_tick_label=[]
    for i in range(len(x_tick)):
        x_tick_label=np.append(x_tick_label,str(int(x_tick[i])))
        
    x_lim=[-0.05*x_tick[-1],1.05*x_tick[-1]]
        
    return x_label,x_tick,x_tick_label,x_lim

def calibration_yaxis(country,money_start,money_goal):
    choice=user_choice(country)
    money_start=int(money_start)
    money_goal=int(money_goal)

    if money_goal<5e3:
        y_label='Savings ('+choice[1]+')'
        norm=1
    elif money_goal>=5e3 and money_goal<5e6:
        y_label='Savings (thousand '+choice[1]+')'
        norm=1e3
    elif money_goal>=5e6 and money_goal<5e9:
        y_label='Savings (million '+choice[1]+')'
        norm=1e6
    elif money_goal>=5e9 and money_goal<5e12:
        y_label='Savings (billion '+choice[1]+')'
        norm=1e9
    else:
        y_label='Savings (trillion '+choice[1]+')'
        norm=1e12
        
    n_tick=5
    step=(money_goal-money_start)/n_tick
    y_tick=np.arange(money_start,money_goal+step,step)
    y_tick_label=[]
    for i in range(len(y_tick)):
        y_tick_label=np.append(y_tick_label,str(int(y_tick[i]/norm)))
    
    height=y_tick[-1]-y_tick[0]
    y_lim=[y_tick[0]-0.05*height,y_tick[-1]+0.05*height]
         
    return y_label,y_tick,y_tick_label,y_lim

def growth(rate,money_start,money_goal,period):
    money_start=int(money_start)
    money_goal=int(money_goal)
    original_goal=money_goal
    period=int(period)+1
    
    message='searching'
    bypass=False
    while message=='searching':
        term1=money_start*(1+rate/100)**period
        term2=sum((1+rate/100)**(period-i) for i in range(1,period))
        increment=(money_goal-term1)/term2

        if increment<0:
            increment=0
            bypass=True
        
        ydata=[]
        ydata=np.append(ydata,money_start)

        for i in range(1,period):
            ydata=np.append(ydata,ydata[i-1]*(1+rate/100)+increment)
            
        if ydata[-1]<0.99*original_goal and bypass==False:
            money_goal*=1.01
        elif ydata[-1]>1.01*original_goal and bypass==False:
            money_goal*=0.99
        else:
            message='found'
    
    return ydata,increment

def algorithm(rates,repartition,money_bank,money_start,money_goal,period):
    money_goal=int(money_goal)
    original_goal=money_goal
    money_start=int(money_start)
    money_bank=int(money_bank)
    period=int(period)+1
        
    message='searching'
    bypass=False
    while message=='searching':
        increment=equation(period,money_start,money_goal,repartition,rates)
        if increment<0:
            increment=0
            bypass=True
            
        portfolio=[]
        for i in range(len(repartition)):
            portfolio=np.append(portfolio,money_start*repartition[i]/100)
        
        ydata_portfolio=np.zeros((period,4))
        ydata_portfolio[0,:]=portfolio
        
        ydata=[]
        ydata=np.append(ydata,sum(ydata_portfolio[0,:])+money_bank)

        for i in range(1,period):
            for j in range(len(portfolio)):
                portfolio[j]=portfolio[j]*(1+rates[j]/100)+increment*repartition[j]/100
            ydata_portfolio[i,:]=portfolio
            ydata=np.append(ydata,sum(ydata_portfolio[i,:])+money_bank)
            
        if ydata[-1]<0.99*original_goal and bypass==False:
            money_goal*=1.01
        elif ydata[-1]>1.01*original_goal and bypass==False:
            money_goal*=0.99
        else:
            message='found'
            
    return ydata,ydata_portfolio,increment

def custom_sum(x,period):
    return sum((1+x/100)**(period-i) for i in range(1,period))

def equation(period,money_start,money_goal,repartition,rates):
    term1=0
    term2=0
    for i in range(0,4):
        term1+=money_start*(repartition[i]/100)*(1+rates[i]/100)**period
        term2+=(repartition[i]/100)*custom_sum(rates[i],period)
    increment=(money_goal-term1)/term2
    
    return increment

def risk_estimation(repartition,rates):
    if repartition[1]==repartition[2]==repartition[3]==0:
        colorScatter='green'
        riskLevel='very low'
    elif repartition[2]==repartition[3]==0:
        if repartition[0]>repartition[1] and rates[1]<10:
            colorScatter='green'
            riskLevel='very low'
        elif repartition[0]>repartition[1] and 10<=rates[1]<25:
            colorScatter='lightgreen'
            riskLevel='low'
        elif repartition[0]>repartition[1] and rates[1]>=25:
            colorScatter='orange'
            riskLevel='moderate'
        elif repartition[0]<=repartition[1] and rates[1]<10:
            colorScatter='lightgreen'
            riskLevel='low'
        elif repartition[0]<=repartition[1] and 10<=rates[1]<25:
            colorScatter='orange'
            riskLevel='moderate'
        else:
            colorScatter='pink'
            riskLevel='high'
    elif repartition[2]+repartition[3]<15:
        if repartition[0]>repartition[1] and rates[1]<10:
            colorScatter='lightgreen'
            riskLevel='low'
        elif repartition[0]>repartition[1] and 10<=rates[1]<25:
            colorScatter='orange'
            riskLevel='moderate'
        elif repartition[0]>repartition[1] and rates[1]>=25:
            colorScatter='pink'
            riskLevel='high'
        elif repartition[0]<=repartition[1] and rates[1]<10:
            colorScatter='orange'
            riskLevel='moderate'
        elif repartition[0]<=repartition[1] and 10<=rates[1]<25:
            colorScatter='pink'
            riskLevel='high'
        else:
            colorScatter='red'
            riskLevel='very high'
    elif 15<=repartition[2]+repartition[3]<30:
        if rates[1]<25 and rates[2]<10 and rates[3]<10:
            colorScatter='orange'
            riskLevel='moderate'
        elif rates[1]>=25 and rates[2]<10 and rates[3]<10:
            colorScatter='pink'
            riskLevel='high'
        elif rates[1]<25 and (10<=rates[2]<25 or 10<=rates[2]<25):
            colorScatter='pink'
            riskLevel='high'
        else:
            colorScatter='red'
            riskLevel='very high'
    elif 30<=repartition[2]+repartition[3]<70:
        if rates[1]<25 and rates[2]<10 and rates[3]<10:
            colorScatter='pink'
            riskLevel='high'
        else:
            colorScatter='red'
            riskLevel='very high'
    else:
        colorScatter='red'
        riskLevel='very high'
        
    return colorScatter,riskLevel
    
def investment_options(country,money_start,money_goal,time_goal):
    choice=user_choice(country)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    
    unit,period=period_transform(time_goal)
    
    periodic_bank=(int(money_goal)-int(money_start))/period
    ydata_bank=np.arange(int(money_start),int(money_goal)+periodic_bank,periodic_bank) 
    ydata_bill,periodic_bill=growth(choice[4],money_start,money_goal,period)
    ydata_bond,periodic_bond=growth(choice[5],money_start,money_goal,period)
    ydata_estate,periodic_estate=growth(choice[6],money_start,money_goal,period)
    ydata_stock,periodic_stock=growth(choice[7],money_start,money_goal,period)
    
    ymax=np.array([ydata_bill[-1],ydata_bond[-1],ydata_estate[-1],ydata_stock[-1]])
    periodics=np.array([periodic_bill,periodic_bond,periodic_estate,periodic_stock])
    if 0 in periodics:
        index=np.where(ymax==max(ymax))
        y_label,y_tick,y_tick_label,y_lim=calibration_yaxis(country,money_start,ymax[index])
    else:
        y_label,y_tick,y_tick_label,y_lim=calibration_yaxis(country,money_start,money_goal)
    
    xdata=np.arange(0,period+1,1)
    
    x_inset=['Bank account','Government bills','Corporate bonds','Real estate','Common socks']
    y_inset=np.array([periodic_bank,periodic_bill,periodic_bond,periodic_estate,periodic_stock])
    bar_labels=[]
    for i in range(len(y_inset)):
        bar_labels=np.append(bar_labels,str(int(y_inset[i])))
    if 0 in y_inset:
        index=np.where(y_inset==0)
        y_inset[index]=1
    color_bar=['white','green','orange','pink','red']
    
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=xdata,y=ydata_bank,
                   mode='lines+markers',
                   name='Bank account',
                   line=dict(color='white',width=6),
                   marker=dict(color='white',size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.add_trace(go.Scatter(x=xdata,y=ydata_bill,
                   mode='lines+markers',
                   name='Government bills',
                   line=dict(color='green',width=6),
                   marker=dict(color='green',size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.add_trace(go.Scatter(x=xdata,y=ydata_bond,
                   mode='lines+markers',
                   name='Corporate bonds',
                   line=dict(color='orange',width=6),
                   marker=dict(color='orange',size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.add_trace(go.Scatter(x=xdata,y=ydata_estate,
                   mode='lines+markers',
                   name='Real estate',
                   line=dict(color='pink',width=6),
                   marker=dict(color='pink',size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.add_trace(go.Scatter(x=xdata,y=ydata_stock,
                   mode='lines+markers',
                   name='Common stocks',
                   line=dict(color='red',width=6),
                   marker=dict(color='red',size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.add_trace(go.Bar(x=x_inset,y=y_inset,
                         xaxis='x2',yaxis='y2',
                         marker_color=color_bar,
                         marker_line=dict(width=0),
                         text=bar_labels,
                         texttemplate='%{text:.3s}',
                         textposition='auto',
                         hovertemplate=None,
                         hoverinfo='skip',
                         showlegend=False))
    fig.update_xaxes(title_text=x_label,
                     range=x_lim,
                     tickvals=x_tick,
                     ticktext=x_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=15,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_yaxes(title_text=y_label,
                     range=y_lim,
                     tickvals=y_tick,
                     ticktext=y_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=20,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_layout(font=dict(size=20,color='white',family='sans-serif'),
                      margin={'l':0,'r':0,'b':0,'t':80},
                      height=600,
                      showlegend=True,
                      plot_bgcolor='#1f2c56',
                      paper_bgcolor='#1f2c56',
                      autosize=True,
                      hovermode='x unified',
                      hoverlabel_namelength=-1,
                      xaxis2=dict(
                          domain=[0.05, 0.45],
                          anchor='x2',
                          showgrid=False,
                          showticklabels=False),
                      yaxis2=dict(
                          domain=[0.5, 0.95],
                          anchor='y2',
                          showgrid=False,
                          showticklabels=False,
                          zeroline=False))
    annotations=[]
    annotations.append(dict(xref='paper',yref='paper',x=0.0, y=1.05,
                              xanchor='left',yanchor='bottom',
                              text=choice[0],
                              font=dict(family='sans-serif',
                                        size=40,
                                        color='white'),
                              showarrow=False))
    annotations.append(dict(xref='paper',yref='paper',x=0.05, y=0.95,
                              xanchor='left',yanchor='bottom',
                              text='Money to add each year ('+choice[1]+')',
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False))
    fig.update_layout(annotations=annotations)
    
    return fig

def computer_scatter(country,money_start,money_goal,time_goal,risk):
    unit,period=period_transform(time_goal)
    money_start=int(money_start)
    money_goal=int(money_goal)
    
    if risk=='very low':
        repartition=[70,30,0,0]
        colorScatter='green'
    elif risk=='low':
        repartition=[50,30,20,0]
        colorScatter='lightgreen'
    elif risk=='moderate':
        repartition=[30,30,20,20] 
        colorScatter='orange'
    elif risk=='high':
        repartition=[10,20,20,50]
        colorScatter='pink'
    elif risk=='very high':
        repartition=[0,0,30,70]
        colorScatter='red'
        
    if money_start<10000:
        message='should not invest'
        money_bank=money_start/2
    elif 10000<=money_start<20000:
        message='on the line'
        money_bank=money_start/2
    elif money_start>=20000:
        message='ok to invest'
        money_bank=10000
        
    money_start-=money_bank
        
    choice=user_choice(country)
    rates=choice[4:8]
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    xdata=np.arange(0,period+1,1)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    y_label,y_tick,y_tick_label,y_lim=calibration_yaxis(country,money_start+money_bank,money_goal)
    
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=xdata,y=ydata_optimal,
                   mode='lines+markers',
                   name='Portfolio growth',
                   line=dict(color=colorScatter,width=6),
                   marker=dict(color=colorScatter,size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.update_xaxes(title_text=x_label,
                     range=x_lim,
                     tickvals=x_tick,
                     ticktext=x_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=15,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_yaxes(title_text=y_label,
                     range=y_lim,
                     tickvals=y_tick,
                     ticktext=y_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=20,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_layout(font=dict(size=20,color='white',family='sans-serif'),
                      margin={'l':20,'r':20,'b':0,'t':80},
                      showlegend=False,
                      plot_bgcolor='#1f2c56',
                      paper_bgcolor='#1f2c56',
                      autosize=False,
                      hovermode='x unified',
                      hoverlabel_namelength=-1
                      )
    annotations=[]
    annotations.append(dict(xref='paper',yref='paper',x=0.0,y=1.05,
                              xanchor='left',yanchor='bottom',
                              text=choice[0],
                              font=dict(family='sans-serif',
                                        size=40,
                                        color='white'),
                              showarrow=False))
    annotations.append(dict(xref='paper',yref='paper',x=0.04,y=0.65,
                              xanchor='left',yanchor='bottom',
                              text='Money to add<br>each year:<br>'+str(int(periodic_optimal))+' '+choice[1],
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False,
                              align='left'))
    fig.update_layout(annotations=annotations)
    
    return fig,message

def computer_pie(country,money_start,money_goal,time_goal,risk,hover_index):
    unit,period=period_transform(time_goal)
    money_goal=int(money_goal)
    money_start=int(money_start)
    
    if risk=='very low':
        repartition=[70,30,0,0]
    elif risk=='low':
        repartition=[50,30,20,0]
    elif risk=='moderate':
        repartition=[30,30,20,20]
    elif risk=='high':
        repartition=[10,20,20,50]
    elif risk=='very high':
        repartition=[0,0,30,70]
        
    if money_start<10000:
        money_bank=money_start/2
    elif 10000<=money_start<20000:
        money_bank=money_start/2
    elif money_start>=20000:
        money_bank=10000
        
    money_start=money_start-money_bank
        
    choice=user_choice(country)
    rates=choice[4:8]
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    
    colors_pie=['White','Green','Orange','Pink','Red']
    labels_pie=['Bank','Government bills','Corporate bonds','Real estate','Common stocks']
    values_pie=[money_bank]
    portfolio=ydata_optimal_portfolio[hover_index]

    values_pie=np.append(values_pie,portfolio)
    message='working'
    while message=='working':
        if 0 in values_pie:
            remove=np.where(values_pie==0)
            colors_pie=np.delete(colors_pie,remove) #this is the pb heroku
            labels_pie=np.delete(labels_pie,remove)
            values_pie=np.delete(values_pie,remove)
        else:
            message='done'

    fig=go.Figure()
    fig.add_trace(go.Pie(labels=labels_pie,values=values_pie,
                         textinfo='label',
                         textfont_size=20,
                         textposition='inside',
                         hole=0,
                         marker=dict(colors=colors_pie),
                         opacity=1,
                         hovertemplate=None,
                         hoverinfo='skip',
                         showlegend=True,
                         automargin=True)
        )
    fig.update_layout(font=dict(size=20,color='white',family='sans-serif'),
                      showlegend=False,
                      plot_bgcolor='#1f2c56',
                      paper_bgcolor='#1f2c56',
                      autosize=False,
                      margin=dict(t=0,b=0,l=20,r=80)
                      )
    fig.update_layout(annotations=[dict(text='Portfolio allocation:',
                                        x=0.0,y=1.0,
                                        font_size=25,
                                        font_family='sans-serif',
                                        showarrow=False)])
    
    return fig

def user_customization(country,money_start,money_goal,time_goal,rates,bank,repartition):
    unit,period=period_transform(time_goal)
            
    choice=user_choice(country)
    rate_bill=choice[4]
    rates=np.insert(rates,0,rate_bill)
    
    money_start=int(money_start)
    money_bank=money_start*bank/100 
    
    money_start-=money_bank
    
    if sum(repartition)<100:
        money_start_calibration=0
        money_start-=money_start*(100-sum(repartition))/100
        for j in range(len(repartition)):
            money_start_calibration+=money_start*repartition[j]/100
    else:
        money_start_calibration=money_start
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    xdata=np.arange(0,period+1,1)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    if periodic_optimal==0:
        y_label,y_tick,y_tick_label,y_lim=calibration_yaxis(country,int(money_start_calibration),int(ydata_optimal[-1]))
    else:
        y_label,y_tick,y_tick_label,y_lim=calibration_yaxis(country,int(money_start_calibration),money_goal)
    
    colorScatter,riskLevel=risk_estimation(repartition,rates)
    
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=xdata,y=ydata_optimal,
                   mode='lines+markers',
                   name='Portfolio growth',
                   line=dict(color=colorScatter,width=6),
                   marker=dict(color=colorScatter,size=18),
                   hoverinfo='name+y',
                   yhoverformat='.3s')
        )
    fig.update_xaxes(title_text=x_label,
                     range=x_lim,
                     tickvals=x_tick,
                     ticktext=x_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=15,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_yaxes(title_text=y_label,
                     range=y_lim,
                     tickvals=y_tick,
                     ticktext=y_tick_label,
                     ticks='inside',
                     tickwidth=2,
                     ticklen=10,
                     title_font=dict(size=30,family='sans-serif'),
                     title_standoff=20,
                     showgrid=False,
                     color='white',
                     linewidth=2,
                     mirror=False,
                     zeroline=False,
                     automargin=True)
    fig.update_layout(font=dict(size=20,color='white',family='sans-serif'),
                      margin={'l':20,'r':20,'b':0,'t':80},
                      showlegend=False,
                      plot_bgcolor='#1f2c56',
                      paper_bgcolor='#1f2c56',
                      autosize=False,
                      hovermode='x unified',
                      hoverlabel_namelength=-1
                      )
    annotations=[]
    annotations.append(dict(xref='paper',yref='paper',x=0.0, y=1.05,
                              xanchor='left',yanchor='bottom',
                              text=choice[0],
                              font=dict(family='sans-serif',
                                        size=40,
                                        color='white'),
                              showarrow=False))
    annotations.append(dict(xref='paper',yref='paper',x=0.02,y=0.75,
                              xanchor='left',yanchor='bottom',
                              text='Money to add<br>each year: '+str(int(periodic_optimal))+' '+choice[1],
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False,
                              align='left'))
    annotations.append(dict(xref='paper',yref='paper',x=0.02,y=0.6,
                              xanchor='left',yanchor='bottom',
                              text='Risk level: '+riskLevel,
                              font=dict(family='sans-serif',
                                        size=25,
                                        color=colorScatter),
                              showarrow=False,
                              align='left'))
    fig.update_layout(annotations=annotations)
    
    return fig