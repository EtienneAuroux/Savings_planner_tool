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
def user_choice(country_choice):
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
    else:
        period=int(time_goal)
            
    unit='year'
      
    try:
        int(time_goal[:period_index])
    except ValueError:
        period=float(time_goal[:period_index])+1
        
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

def calibration_yaxis_linear(country,money_start,money_goal):
    choice=user_choice(country)
    money_start=money_start.replace(' ','')
    money_goal=money_goal.replace(' ','')

    if int(money_goal)<5e3:
        y_label='Savings ('+choice[1]+')'
        norm=1
    elif int(money_goal)>=5e3 and int(money_goal)<5e6:
        y_label='Savings (thousand '+choice[1]+')'
        norm=1e3
    elif int(money_goal)>=5e6 and int(money_goal)<5e9:
        y_label='Savings (million '+choice[1]+')'
        norm=1e6
    elif int(money_goal)>=5e9 and int(money_goal)<5e12:
        y_label='Savings (billion '+choice[1]+')'
        norm=1e9
    else:
        y_label='Savings (trillion '+choice[1]+')'
        norm=1e12
    
    order_start=len(money_start)-1
    if int(money_start)<0.05*int(money_goal):
        y_start=0
    else:
        y_start=math.floor(int(money_start)/(10**order_start))*10**order_start
    
    order=len(money_goal)-1
    if round(int(money_goal),-order)<int(money_goal):
        y_end=round(int(money_goal),-order)+5*10**(order-1)
    elif round(int(money_goal),-order)>int(money_goal):
        y_end=round(int(money_goal),-order)
    else:
        y_end=int(money_goal)
        
    n_tick=5
    step=(y_end-y_start)/n_tick
    y_tick=np.arange(y_start,y_end+step,step)
    
    y_tick_label=[]
    for i in range(len(y_tick)):
        y_tick_label=np.append(y_tick_label,str(int(y_tick[i]/norm)))
        
    y_lim=[-0.05*y_tick[-1],1.05*y_tick[-1]]
        
    return y_label,y_tick,y_tick_label,y_lim

def individual_algorithm(rate,money_start,money_goal,period):
    epsilon=10
    guess=(int(money_goal)-int(money_start))/period
    ydata=[int(money_start)]
    
    message='searching'
    while message=='searching':
        i=1
        while i<period+1:
            i+=1
            ydata_new=ydata[-1]*(1+rate/100)+guess
            ydata=np.append(ydata,ydata_new)
        spread=ydata[-1]-int(money_goal)
        if abs(spread)>epsilon:
            guess-=spread/period
            ydata=[int(money_start)]
        else:
            message='found'
            
    return ydata,guess

    
def individual_ways(country,money_start,money_goal,time_goal):
    choice=user_choice(country)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    y_label,y_tick,y_tick_label,y_lim=calibration_yaxis_linear(country,money_start,money_goal)
    
    unit,period=period_transform(time_goal)
    
    periodic_bank=(int(money_goal)-int(money_start))/period
    ydata_bank=np.arange(int(money_start),int(money_goal)+periodic_bank,periodic_bank) 
    ydata_bill,periodic_bill=individual_algorithm(choice[4],money_start,money_goal,period)
    ydata_bond,periodic_bond=individual_algorithm(choice[5],money_start,money_goal,period)
    ydata_estate,periodic_estate=individual_algorithm(choice[6],money_start,money_goal,period)
    ydata_stock,periodic_stock=individual_algorithm(choice[7],money_start,money_goal,period)

    xdata=np.arange(0,period+1,1)
    
    x_inset=['Bank account','Government bills','Corporate bonds','Real estate','Common socks']
    y_inset=[periodic_bank,periodic_bill,periodic_bond,periodic_estate,periodic_stock]
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
                         text=y_inset,
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
                              text='Minimum yearly contribution ('+choice[1]+')',
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False))
    fig.update_layout(annotations=annotations)
    
    return fig

def mix_algorithm(rates,repartition,money_bank,money_start,money_goal,period): #problem of divergence for high rates
    epsilon=10
    guess=(int(money_goal)-money_start)/period
    
    portfolio_init=[]
    for i in range(len(repartition)):
        portfolio_init=np.append(portfolio_init,money_start*repartition[i]/100)
    
    alert='ok'
    message='searching'
    while message=='searching':
        i=1
        ydata=[money_start+money_bank]
        portfolio=np.zeros(4)
        ydata_portfolio=np.zeros((int(period)+1,4))
        for j in range(len(portfolio_init)):
            portfolio[j]=portfolio_init[j]
        ydata_portfolio[0,:]=portfolio
        while i<period+1:
            i+=1
            for j in range(len(rates)):
                portfolio[j]=portfolio[j]*(1+rates[j]/100)
            ydata_new=sum(portfolio)+guess
            for j in range(len(repartition)):
                portfolio[j]+=guess*repartition[j]/100
            ydata=np.append(ydata,ydata_new+money_bank)
            ydata_portfolio[i-1,:]=portfolio
        spread=ydata[-1]-int(money_goal)
        if abs(spread)>epsilon:
            guess-=spread/period
            if abs(guess)>1e100:
                alert='divergence'
                break
        else:
            message='found'
            
    if alert=='divergence':
        origin_goal=int(money_goal)
        count=0
        while message=='searching':
            guess=brute_force(int(period)+1,int(money_start),int(money_goal),repartition,rates)
            i=1
            ydata=[money_start+money_bank]
            portfolio=np.zeros(4)
            ydata_portfolio=np.zeros((int(period)+1,4))
            for j in range(len(portfolio_init)):
                portfolio[j]=portfolio_init[j]
            ydata_portfolio[0,:]=portfolio
            while i<period+1:
                i+=1
                for j in range(len(rates)):
                    portfolio[j]=portfolio[j]*(1+rates[j]/100)
                ydata_new=sum(portfolio)+guess
                for j in range(len(repartition)):
                    portfolio[j]+=guess*repartition[j]/100
                ydata=np.append(ydata,ydata_new+money_bank)
                ydata_portfolio[i-1,:]=portfolio
                if ydata[-1]<0.95*origin_goal:
                    money_goal=int(money_goal)*1.01
                    count+=1
                elif ydata[-1]>1.05*origin_goal:
                    money_goal=int(money_goal)*0.99
                    count+=1
                else:
                    message='found'
            
    return ydata,ydata_portfolio,guess

def custom_sum(x,period):
    return sum((1+x/100)**(i-1) for i in range(1,period))

def brute_force(period,money_start,money_goal,repartition,rates):
    term1=0
    term2=0
    for i in range(0,4):
        term1+=money_start*(repartition[i]/100)*(1+rates[i]/100)**period
        term2+=(repartition[i]/100)*custom_sum(rates[i],period)
    increment=(money_goal-term1)/term2
    
    return increment

def mix_way_scatter(country,money_start,money_goal,time_goal,risk): #add color change and text for risk level.
    unit,period=period_transform(time_goal)
    
    if risk=='very low': #Which does not mean risk is 0
        repartition=[70,30,0,0]
        colorScatter='green'
    elif risk=='low': #risk is defined as the risk of seeing your savings decrease
        repartition=[50,30,20,0]
        colorScatter='lightgreen'
    elif risk=='moderate':
        repartition=[30,30,20,20] #note that bank savings are not here, there should always be money in the bank for safety, this will be a fixed amount
        colorScatter='orange'
    elif risk=='high': #in user_way function, the user can choose to have 0 in the bank but not here.
        repartition=[10,20,20,50]
        colorScatter='pink'
    elif risk=='very high': #Which is still investing not speculating
        repartition=[0,0,30,70] #it will show as a pie chart on plot
        colorScatter='red'
        
    if int(money_start)<10000:
        message='should not invest'
        money_bank=int(money_start)/2
    elif int(money_start)>=10000 and int(money_start)<20000:
        message='on the line'
        money_bank=int(money_start)/2
    elif int(money_start)>=20000:
        message='on the line'
        money_bank=10000
        
    money_start=int(money_start)-money_bank
        
    choice=user_choice(country)
    rates=choice[4:8]
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=mix_algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    xdata=np.arange(0,period+1,1)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    y_label,y_tick,y_tick_label,y_lim=calibration_yaxis_linear(country,str(int(money_start)),money_goal)
    
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
                              text='Minimum yearly<br>contribution:<br>'+str(int(periodic_optimal))+' '+choice[1],
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False,
                              align='left'))
    fig.update_layout(annotations=annotations)
    
    return fig,message

def mix_way_pie(country,money_start,money_goal,time_goal,risk,hover_index):
    unit,period=period_transform(time_goal)
    
    if risk=='very low': #Which does not mean risk is 0
        repartition=[70,30,0,0]
    elif risk=='low': #risk is defined as the risk of seeing your savings decrease
        repartition=[50,30,20,0]
    elif risk=='moderate':
        repartition=[30,30,20,20] #note that bank savings are not here, there should always be money in the bank for safety, this will be a fixed amount
    elif risk=='high': #in user_way function, the user can choose to have 0 in the bank but not here.
        repartition=[10,20,20,50]
    elif risk=='very high': #Which is still investing not speculating
        repartition=[0,0,30,70] #it will show as a pie chart on plot
        
    if int(money_start)<10000:
        money_bank=int(money_start)/2
    elif int(money_start)>=10000 and int(money_start)<20000:
        money_bank=int(money_start)/2
    elif int(money_start)>=20000:
        money_bank=10000
        
    money_start=int(money_start)-money_bank
        
    choice=user_choice(country)
    rates=choice[4:8]
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=mix_algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    
    colors_pie=['White','Green','Orange','Pink','Red']
    labels_pie=['Bank','Government bills','Corporate bonds','Real estate','Common stocks']
    values_pie=[money_bank]
    portfolio=ydata_optimal_portfolio[hover_index]
    values_pie=np.append(values_pie,portfolio)
    remove_index=[]
    for i in range(len(values_pie)):
        if values_pie[i]==0:
            remove_index=np.append(remove_index,i)
    colors_pie=np.delete(colors_pie,remove_index)
    labels_pie=np.delete(labels_pie,remove_index)
    values_pie=np.delete(values_pie,remove_index)
    
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

def custom_way(country,money_start,money_goal,time_goal,rates,bank,repartition): #add color change and text for risk level.
    unit,period=period_transform(time_goal)
            
    choice=user_choice(country)
    rate_bill=choice[4]
    rates=np.insert(rates,0,rate_bill)
    
    money_start=int(money_start)
    money_bank=money_start*bank/100
    money_start-=money_bank
    
    ydata_optimal,ydata_optimal_portfolio,periodic_optimal=mix_algorithm(rates,repartition,money_bank,money_start,money_goal,period)
    xdata=np.arange(0,period+1,1)
    x_label,x_tick,x_tick_label,x_lim=calibration_xaxis(time_goal)
    y_label,y_tick,y_tick_label,y_lim=calibration_yaxis_linear(country,str(int(money_start)),money_goal)
    
    if periodic_optimal>int(money_goal)/10:
        colorScatter='green'
        riskLevel='very low'
    elif periodic_optimal<=int(money_goal)/10 and periodic_optimal>int(money_goal)/12.5:
        colorScatter='lightgreen'
        riskLevel='low'
    elif periodic_optimal<=int(money_goal)/12.5 and periodic_optimal>int(money_goal)/16.67:
        colorScatter='orange'
        riskLevel='moderate'
    elif periodic_optimal<=int(money_goal)/16.67 and periodic_optimal>int(money_goal)/25:
        colorScatter='pink'
        riskLevel='high'
    else:
        colorScatter='red'
        riskLevel='very high'
    
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
                              text='Minimum yearly<br>contribution: '+str(int(periodic_optimal))+' '+choice[1],
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False,
                              align='left'))
    annotations.append(dict(xref='paper',yref='paper',x=0.02,y=0.6,
                              xanchor='left',yanchor='bottom',
                              text='Risk level:',
                              font=dict(family='sans-serif',
                                        size=25,
                                        color='white'),
                              showarrow=False,
                              align='left'))
    annotations.append(dict(xref='paper',yref='paper',x=0.19,y=0.6,
                              xanchor='left',yanchor='bottom',
                              text=riskLevel,
                              font=dict(family='sans-serif',
                                        size=25,
                                        color=colorScatter),
                              showarrow=False,
                              align='left'))
    fig.update_layout(annotations=annotations)
    
    return fig