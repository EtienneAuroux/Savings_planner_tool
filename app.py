# -*- coding: utf-8 -*-
"""
Project: Money saver assessment tool
Started in April 2022
@author: Etienne Auroux
"""

from support_functions import check_format,user_choice,individual_ways,mix_way_scatter,mix_way_pie,custom_way
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise
import os

##Layout of the webpage
default_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
app=dash.Dash(__name__,external_stylesheets=[default_stylesheets,dbc.themes.BOOTSTRAP]) #initialising dash app
server=app.server
server.wsgi_app=WhiteNoise(server.wsgi_app,root=os.path.join(os.path.dirname(__file__),'static'),prefix='static/')

app.layout=html.Div(id='parent',children=[
    html.Img(id='header_icon',className='headerAvatar',src=r'static\app_logo.svg'),
    html.H1('Savings planner',className='headerMain'),
    html.Div(id='column_layout',className='row',children=[
        html.Div(id='left_column',className='left',children=[
            html.Div(id='left_column_top',className='block inputBlock',children=[
                html.H3('Input parameters',className='headerBlock headerInput'),
                html.Div(id='country_question',children=[
                    html.P('Country:',className='textBlock textCountry',style={'display':'inline-block'}),
                    dcc.Input(id='input_country',className='inputField inputCountry',type='text',placeholder=' e.g., Japan, France, ...',style={'display':'inline-block'})
                    ]),
                html.Div(id='period_question',children=[
                    html.P('Saving period:',className='textBlock textPeriod',style={'display':'inline-block'}),
                    dcc.Input(id='input_period',className='inputField inputPeriod',type='text',placeholder=' e.g., 10 years, 15',style={'display':'inline-block'})
                    ]),
                html.Div(id='goal_question',children=[
                    html.P('Saving goal:',className='textBlock textSaving',style={'display':'inline-block'}),
                    dcc.Input(id='input_goal',className='inputField inputGoal',type='text',placeholder=' e.g., 10000, 1000000',style={'display':'inline-block'})
                    ]),
                html.Div(id='start_question',children=[
                    html.P('Starting amount:',className='textBlock textStarting',style={'display':'inline-block'}),
                    dcc.Input(id='input_start',className='inputField inputStart',type='text',placeholder=' e.g., 0, 200000',style={'display':'inline-block'})
                    ]),
                dbc.Button('Submit request',id='submit_button',className='buttonSubmit',n_clicks=0,style={'display':'inline-block'}),
                dbc.Button('Reset',id='reset_button',className='buttonReset',n_clicks=0,style={'display':'inline-block'})
                ]),
            dbc.Collapse(id='hide_left_choice2',children=[
                html.Div(id='left_column_choice2',className='block parameterBlock2',children=[
                    html.H3('Parameters',className='headerBlock headerParameterBlock2'),
                    html.H5('Risk level',className='subHeaderBlock subHeaderParameterBlock2'),
                    dcc.Slider(id='risk_slider_choice2',className='riskSlider',min=1,max=5,step=1,value=3,marks={
                        1: {'label':'very low','style':{'color':'lawngreen','fontSize':14}},
                        2: {'label':'low','style':{'color':'lightgreen','fontSize':14}},
                        3: {'label':'moderate','style':{'color':'orange','fontSize':14}},
                        4: {'label':'high','style':{'color':'pink','fontSize':14}},
                        5: {'label':'very high','style':{'color':'red','fontSize':14}}
                        })
                    ])
                ],is_open=False),
            dbc.Collapse(id='hide_left_choice3',children=[
                html.Div(id='left_column_choice3',className='block parameterBlock3',children=[
                    html.H3('Parameters',className='headerBlock headerParameterBlock3'),
                    html.Div(id='bank_bill',className='bankBill',children=[
                        html.Div(id='bank_div',className='bankDiv',children=[
                            html.H5('Bank',className='subHeaderBlock subHeaderBank'),
                            html.H6('Share',className='subsubHeaderBlock subsubHeaderBank'),
                            dcc.Slider(id='share_bank',className='bankSlider',min=0,max=100,step=1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True})
                            ],style={'display':'inline-block'}),
                        html.Div(id='bill_div',className='billDiv',children=[
                            html.H5('Government bills',className='subHeaderBlock subHeaderBill'),
                            html.H6('Share',className='subsubHeaderBlock subsubHeaderBill'),
                            dcc.Slider(id='share_bill',className='billSlider',min=0,max=100,step=1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True})
                            ],style={'display':'inline-block'})
                         ]),
                    html.H5('Corporate bonds',className='subHeaderBlock subHeaderBond'),
                    html.Div(id='bond',className='bondSection',children=[
                        html.Div(id='bond_share_div',className='bondShareDiv',children=[
                            html.H6('Share',className='subsubHeaderBlock subsubHeaderBondShare'),
                            dcc.Slider(id='share_bond',className='bondSliderShare',min=0,max=100,step=1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'}),
                        html.Div(id='bond_rate_div',className='bondRateDiv',children=[
                            html.H6('Rate of return',className='subsubHeaderBlock subsubHeaderBondRates'),
                            dcc.Slider(id='rate_bond',className='bondSliderRates',min=0,max=50,step=0.1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'})
                        ]),
                    html.H5('Real estate',className='subHeaderBlock subHeaderEstate'),
                    html.Div(id='estate',className='estateSection',children=[
                        html.Div(id='estate_share_div',className='estateShareDiv',children=[
                            html.H6('Share',className='subsubHeaderBlock subsubHeaderEstateShare'),
                            dcc.Slider(id='share_estate',className='estateSliderShare',min=0,max=100,step=1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'}),
                        html.Div(id='estate_rate_div',className='estateRateDiv',children=[
                            html.H6('Rate of return',className='subsubHeaderBlock subsubHeaderEstateRates'),
                            dcc.Slider(id='rate_estate',className='estateSliderRates',min=0,max=50,step=0.1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'})
                        ]),
                    html.H5('Common stocks',className='subHeaderBlock subHeaderStock'),
                    html.Div(id='stock',className='stockSection',children=[
                        html.Div(id='stock_share_div',className='stockdShareDiv',children=[
                            html.H6('Share',className='subsubHeaderBlock subsubHeaderStockShare'),
                            dcc.Slider(id='share_stock',className='stockSliderShare',min=0,max=100,step=1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'}),
                        html.Div(id='stock_rate_div',className='stockRateDiv',children=[
                            html.H6('Rate of return',className='subsubHeaderBlock subsubHeaderStockRates'),
                            dcc.Slider(id='rate_stock',className='stockSliderRates',min=0,max=50,step=0.1,marks=None,
                                       tooltip={'placement':'bottom','always_visible':True}),
                            ],style={'display':'inline-block'})
                        ])
                    ])
                ],is_open=False)
            ]),
        html.Div(id='right_column',className='right',children=[
            dbc.Collapse(id='hide_right',children=[
                dbc.Collapse(id='hide_choice',children=[
                    html.Div(id='choice_1',className='block choice choice1',children=[
                        html.H3('Investment\noptions',className='headerBlock headerChoice1'),
                        html.Img(id='choice1_icon',className='choiceLogo',src=r'static\choice1_logo.svg'),
                        html.Br(),
                        dbc.Button('Click here',id='choice1_button',className='buttonChoice button1',n_clicks=0)
                        ],style={'display':'inline-block'}),
                    html.Div(id='choice_2',className='block choice choice2',children=[
                        html.H3('Computer\'s\nsuggestion',className='headerBlock headerChoice2'),
                        html.Img(id='choice2_icon',className='choiceLogo',src=r'static\choice2_logo.svg'),
                        html.Br(),
                        dbc.Button('Click here',id='choice2_button',className='buttonChoice button2',n_clicks=0)
                        ],style={'display':'inline-block'}),
                    html.Div(id='choice_3',className='block choice choice3',children=[
                        html.H3('User\'s\ncustomization',className='headerBlock headerChoice3'),
                        html.Img(id='choice3_icon',className='choiceLogo',src=r'static\choice3_logo.svg'),
                        html.Br(),
                        dbc.Button('Click here',id='choice3_button',className='buttonChoice button3',n_clicks=0)
                        ],style={'display':'inline-block'})
                    ],is_open=True),
                dbc.Collapse(id='hide_choice1',children=[
                    html.Div(id='graph1_div',className='block graphChoice1',children=[
                        dcc.Graph(id='graph1',className='graphChoice1Scatter',figure={})
                        ])
                    ],is_open=False),
                dbc.Collapse(id='hide_choice2',children=[
                    html.Div(id='graph2_div',className='block graphChoice2',children=[
                        dcc.Graph(id='graph2_scatter',className='graphChoice2Scatter',figure={},style={'display':'inline-block'}),
                        dcc.Graph(id='graph2_pie',className='graphChoice2Pie',figure={},style={'display':'inline-block'})
                        ])
                    ],is_open=False),
                dbc.Collapse(id='hide_choice3',children=[
                    html.Div(id='graph3_div',className='block graphChoice3',children=[
                        dcc.Graph(id='graph3',className='graphChoice3Scatter',figure={})
                        ])
                    ],is_open=False),
                dbc.Collapse(id='hide_return',children=[
                    dbc.Button('Return to the choices',id='back_choice',className='buttonPrevious',n_clicks=0)
                    ],is_open=False)
                ],is_open=False),
            dbc.Collapse(id='hide_error_input',children=[
                html.Div(id='middle_column_input',className='block errorBlock',children=[
                    html.H3('Error',id='error_heading_input',className='headerError'),
                    html.Img(id='error_icon_input',className='errorLogo',src=r'static\error_logo.svg'),
                    html.P(id='error_text_input',className='errorMessage'),
                    dbc.Collapse(id='hide_contact_link',children=[
                        html.A('Contact me.',href='https://etienneauroux.com/#contactme',id='contact_country',className='linkContact',target='_blank')
                        ],is_open=False)
                    ]),
                html.Div(id='mask_input',className='maskDiv')
                ],is_open=False),
            dbc.Collapse(id='hide_error_repartition',children=[
                html.Div(id='middle_column_repartition',className='block errorBlock',children=[
                    html.H3('Error',id='error_heading_repartition',className='headerError'),
                    html.Img(id='error_icon_repartition',className='errorLogo',src=r'static\error_logo.svg'),
                    html.P('Your portfolio is bigger than 100 %, please adjust your shares accordingly.',id='error_text_repartition',className='errorMessage')
                    ]),
                html.Div(id='mask_repartition',className='maskDiv')
                ],is_open=False)            
            ])
        ]),
    html.Div(id='bottom_bar',className='bottomInfo',children=[
        html.A('App by Etienne Auroux',href='https://etienneauroux.com',id='signature',className='linkHome',target='_blank'),
        html.Div(id='source_div',className='sourceDiv',children=[
            html.H5('Sources',id='heading_source',className='headerSource',style={'display':'inline-block'}),
            html.Div(id='source_list_div',className='sourceList',children=[
                html.Div(id='rates_source',className='sourceRates',children=[
                    html.P('Grow rates: ',className='sourceRatesText',style={'display':'inline-block'}),
                    html.A('[1]',href='https://www.frbsf.org/economic-research/wp-content/uploads/sites/4/wp2017-25.pdf',id='source_rates_1',className='sourceRates1',target='_blank',style={'display':'inline-block'})
                    ]),
                html.Div(id='inflation_source',className='sourceInflation',children=[
                    html.P('Inflation: ',className='sourceInflationText',style={'display':'inline-block'}),
                    html.A('[2]',href='https://www.worldbank.org/en/research/brief/inflation-database',id='source_inflation_1',className='sourceInflation1',target='_blank',style={'display':'inline-block'})
                    ])
                ],style={'display':'inline-block'})
            ]),
        html.Div(id='disclaimer_div',className='disclaimerDiv',children=[
            html.P('For informational purposes only.',className='disclaimerText1'),
            html.P('Do not constitute financial advice.',className='disclaimerText2'),
            html.P('Consult a professional investment advisor,',className='disclaimerText3'),
            html.P('before making any investment decision.',className='disclaimerText4')
            ])
        ])
    ])

@app.callback(
    Output('submit_button','n_clicks'),
    Input('reset_button','n_clicks')
)
def reset_layout(clicks):
    if clicks==0:
        raise PreventUpdate
    else:
        return 0

@app.callback(
    Output('submit_button','disabled'),
    Input('submit_button','n_clicks')
)
def submit_switch(clicks):
    if clicks==0:
        switch=False
    else:
        switch=True
    return switch

@app.callback(
    [Output('hide_error_input','is_open'),
     Output('error_text_input','children'),
     Output('hide_right','is_open'),
     Output('hide_contact_link','is_open')],
    Input('submit_button','n_clicks'),
    [State('input_country','value'),
     State('input_period','value'),
     State('input_goal','value'),
     State('input_start','value')]
)
def toggle_choice(clicks,country_choice,time_goal,money_goal,money_start):
    if clicks==0:
        switch_error=False
        message_error=''
        switch_choice=False
        switch_link=False
    else:
        switch_error=True
        switch_choice=False
        switch_link=False
        test_result=check_format(country_choice,money_start,money_goal,time_goal)
        if test_result=='format_money_start':
            message_error='The starting amount must be a number.'
        elif test_result=='format_money_goal':
            message_error='The saving goal must be a number.'
        elif test_result=='format_money_both':
            message_error='The starting amount and the saving goal must be numbers.'
        elif test_result=='money_goal<=0':
            message_error='The saving goal must be bigger than zero.'
        elif test_result=='money_start<0':
            message_error='The starting amount must be bigger than zero.'
        elif test_result=='money_both<=0':
            message_error='The saving goal and starting amount must be bigger than zero.'
        elif test_result=='goal<=start':
            message_error='The saving goal must be bigger than the starting amount.'
        elif test_result=='format_period':
            message_error='The saving period must be a number of years, for example: \"10 years\".'
        elif test_result=='amount_period':
            message_error='Wrong format for the starting amount and/or (saving goal) and the saving period.'
        elif test_result=='country_not_in_list':
            message_error='This country is not yet implemented. You can make a request here:'
            switch_link=True
        else:
            message_error=''
            switch_error=False
            switch_choice=True
    return switch_error,message_error,switch_choice,switch_link

@app.callback(
    Output('hide_return','is_open'),
    [Input('choice1_button','n_clicks'),
     Input('choice2_button','n_clicks'),
     Input('choice3_button','n_clicks')]
)
def toggle_return_button(clicks1,clicks2,clicks3):
    if clicks1==0 and clicks2==0 and clicks3==0:
        return False
    else:
        return True

@app.callback( #User has chosen "Investment options"
    [Output('hide_choice1','is_open'),
     Output('graph1','figure')],
    [Input('choice1_button','n_clicks'),
     Input('submit_button','n_clicks')],
    [State('input_country','value'),
     State('input_period','value'),
     State('input_goal','value'),
     State('input_start','value')]
)
def toggle_choice1(clicks1,submit,country_choice,time_goal,money_goal,money_start):
    if clicks1==0:
        investment_options={}
        switch_graph=False
    elif submit==0:
        investment_options={}
        switch_graph=False
    else:
        investment_options=individual_ways(country_choice,money_start,money_goal,time_goal)
        switch_graph=True
    return switch_graph,go.Figure(data=investment_options)

@app.callback( #User has chosen "Computer suggestion"
    [Output('hide_choice2','is_open'),
     Output('hide_left_choice2','is_open'),
     Output('graph2_scatter','figure'),
     Output('graph2_pie','figure')],
    [Input('choice2_button','n_clicks'),
     Input('submit_button','n_clicks'),
     Input('risk_slider_choice2','value'),
     Input('graph2_scatter','hoverData')],
    [State('input_country','value'),
     State('input_period','value'),
     State('input_goal','value'),
     State('input_start','value')]
)
def toggle_choice2(clicks2,submit,value,hoverData,country_choice,time_goal,money_goal,money_start):
    if clicks2==0:
        switch_graph=False
        switch_parameter=False
        scatter={}
        pie={}
    elif submit==0:
        switch_graph=False
        switch_parameter=False
        scatter={}
        pie={}
    else:
        switch_graph=True
        switch_parameter=True
        if value==1:
            risk_choice='very low'
        elif value==2:
            risk_choice='low'
        elif value==3:
            risk_choice='moderate'
        elif value==4:
            risk_choice='high'
        elif value==5:
            risk_choice='very high'
        if hoverData is None:
            pie=mix_way_pie(country_choice,money_start,money_goal,time_goal,risk_choice,0)
        else:
            hover_data = hoverData["points"][0]
            num=hover_data["pointNumber"]
            pie=mix_way_pie(country_choice,money_start,money_goal,time_goal,risk_choice,int(num))
        scatter,message=mix_way_scatter(country_choice,money_start,money_goal,time_goal,risk_choice)
    return switch_graph,switch_parameter,go.Figure(data=scatter),go.Figure(data=pie)

@app.callback(
    [Output('share_bank','value'),
     Output('share_bill','value'),
     Output('share_bond','value'),
     Output('share_estate','value'),
     Output('share_stock','value'),
     Output('rate_bond','value'),
     Output('rate_estate','value'),
     Output('rate_stock','value')],
    Input('submit_button','n_clicks'),
    State('input_country','value')
)
def default_slider_values(clicks,country_choice):
    if clicks==0:
        raise PreventUpdate
    else:
        choice=user_choice(country_choice)
        sbank=0
        sbill=30
        sbond=30
        sestate=20
        sstock=20
        rbond=choice[5]
        restate=choice[6]
        rstock=choice[7]
        return sbank, sbill, sbond, sestate, sstock, rbond, restate, rstock

@app.callback( #User has chosen "User customization"
    [Output('hide_choice3','is_open'),
      Output('hide_left_choice3','is_open'),
      Output('graph3','figure'),
      Output('hide_error_repartition','is_open')],
    [Input('choice3_button','n_clicks'),
     Input('submit_button','n_clicks'),
      Input('share_bank','value'),
      Input('share_bill','value'),
      Input('share_bond','value'),
      Input('share_estate','value'),
      Input('share_stock','value'),
      Input('rate_bond','value'),
      Input('rate_estate','value'),
      Input('rate_stock','value')],
    [State('input_country','value'),
      State('input_period','value'),
      State('input_goal','value'),
      State('input_start','value')]
)
def toggle_choice3(clicks3,submit,sbank,sbill,sbond,sestate,sstock,rbond,restate,rstock,country_choice,time_goal,money_goal,money_start):
    if clicks3==0:
        switch_graph=False
        switch_parameter=False
        switch_error=False
        scatter={}
    elif submit==0:
        switch_graph=False
        switch_parameter=False
        switch_error=False
        scatter={}
    else:
        switch_parameter=True
        repartition=[sbill,sbond,sestate,sstock]
        if sum(repartition)>100:
            switch_graph=False
            switch_error=True
            scatter={}
        else:
            switch_graph=True
            switch_error=False
            rates=[rbond,restate,rstock]
            bank=sbank
            scatter=custom_way(country_choice,money_start,money_goal,time_goal,rates,bank,repartition)
    return switch_graph,switch_parameter,go.Figure(data=scatter),switch_error

@app.callback( #User wants to go back to choices
    [Output('choice1_button','n_clicks'),
     Output('choice2_button','n_clicks'),
     Output('choice3_button','n_clicks')],
    Input('back_choice','n_clicks')
)
def return_to_choices(clicks):
    if clicks:
        clicks1=0
        clicks2=0
        clicks3=0
        return clicks1,clicks2,clicks3
    else:
        raise PreventUpdate

port=8051
if __name__ =='__main__':
    app.run_server(debug=True,port=port,use_reloader=False)