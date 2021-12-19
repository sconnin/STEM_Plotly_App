# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 12:32:19 2021

@author: seanc
"""

# import libraries

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Output, Input
import json




# import data and clean document

url = 'https://raw.githubusercontent.com/sconnin/STEM_Plotly_App/main/stem_inst_diversity_plotly.csv'
url_ethnic = 'https://raw.githubusercontent.com/sconnin/STEM_Plotly_App/main/ethnic_perc_plotly.csv'
url_slope = 'https://raw.githubusercontent.com/sconnin/STEM_Plotly_App/main/stem_inst_diversity_coeff.csv'

# Dataframe for Simpson scores

df = pd.read_csv(url)

# Dataframe for racial composition

df_ethnic = pd.read_csv(url_ethnic)

# Dataframe for institutional trends

df_coeff = pd.read_csv(url_slope)

df_coeff = df_coeff.round({'slope': 3})
df_coeff = df_coeff[df_coeff['metric'] == 'simpson'].reset_index(drop=True)

trend=pd.cut(df_coeff.slope,bins=[-0.33, -0.009, .009, 0.33],labels=['Decreasing', 'Unchanged','Increasing'])
trend=pd.DataFrame(data=trend).rename(columns={"slope": "trend"})

df_coeff = df_coeff.reset_index(drop=True).join(trend)

# Dataframe for tables

tbl_df = df.loc[:,['name', 'year', 'sector', 'state', 'metric', 'size', 'value']]

# Camel case headers and captialize character values in dataframes

df.columns = df.columns.str.title()
df['Metric'] = df['Metric'].str.capitalize()
df['Sector'] = df['Sector'].str.capitalize()

df_coeff.columns = df_coeff.columns.str.title()
df_coeff['Metric'] = df['Metric'].str.capitalize()
df_coeff['Sector'] = df['Sector'].str.capitalize()

# Create selection lists

sector_choice = ['Public', 'Private_nonprofit']

size_choice = ['< 1000', '1,000 - 4,999', '5,000 - 9,999', '10,000 - 19,999', '20,000 +']

region_choice = ['Northeast', 'Southeast', 'Great_Lakes', 'Mid_East',
                 'Plains', 'Rocky_Mountains', 'Southwest', 'Far_West', 'Not_Reported']

metric_choice = ['Simpson'] # set for use with size dropdown tab 3

slope_interval_choice = ['Decreasing', 'Unchanged','Increasing']

# set mapbox token

px.set_mapbox_access_token(
    "pk.eyJ1Ijoic2Nvbm5pbiIsImEiOiJjaW9nN29ta20wMWk3dHhrbThpaWxobmxvIn0.UFNQ0SoB3DcbkNQRbNR_iw")
 
# initiate app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# initiate layout

app.layout = dbc.Tabs([

# =============================================================================
# Tab 1 
# =============================================================================

    dbc.Tab([ 

        html.Div([

            dbc.Row([
                dbc.Col(html.Div(
                    html.H1("Racial Diversity in Post-Secondary Science Education",
                        style={
                               'padding-top' : '40px',
                               'padding-bottom' : '10px',
                               'font-size': '50',
                               'font-weight': 'bold'}
                               )
                        ),
                    ) # close col
                ],style={'margin-left': '38px', 'margin-bottom': '5px', 'margin-right':'20'}, justify="around"), # close row
            
            dbc.Row([
                
                dbc.Col(
                    dcc.Markdown('''  
                
                Demand for skilled professionals in science, technology, engineering, and math (STEM) has increased 79% over the past three decades in the United States. And projections from the U.S. Bureau of Labor Statistics point to an additional 8% increase in STEM occupations between 2019-2029, more than double that of other employment sectors.
                
                In parallel, educators, policy makers, and industry leaders have worked to increase recruitment and advanced degree attainment among women and racial minorities in STEM disciplines.
                
                This application is a prototype for tracking diversity as a component of undergraduate attainment in STEM fields by institution, nationwide. The data are currently disaggregated at the level of student (racial category) and campus (academic sector, size, region, location).
                
                    '''), width = '8'
                ), # close col
            
                dbc.Col(
                    dcc.Markdown('''
            
                        #### Intended Audience:
                        
                        * _STEM educators seeking funding for educational resources and programs._
                
                        * _Campus officers who oversee diversity initiatives and related benchmarking._
                
                        * _Industry recruiters looking to optimize their outreach activities._
                        
                        * _Students seeking an inclusive learning environment in STEM._
                        
                        '''), width = '3', style={'background-color': '#F5F5F5', 'padding-top': '20px'} 
                        ), # close column
                ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
            ), # close row

            dbc.Row([
                dbc.Col(html.Div(
                    html.H1("Measuring Diversity",
                        style={
                               'padding-top' : '10px',
                               'padding-bottom' : '10px',
                               'font-size': '50',
                               'font-weight': 'bold'}
                               )
                        ),
                    ) # close col
                ],style={'margin-left': '38px', 'margin-bottom': '5px', 'margin-right':'20'}, justify="around"
            ), # close row
            
            dbc.Row([      
                dbc.Col(
                    dcc.Markdown('''
                    
                         __This project applies a composite measure of diversity (Simpson’s Index of Diversity) to account for both group representation and size in a single metric.__
                         
                         Simpson scores presented here are based on annual STEM graduation totals summed across racial category for each institution. 
                         
                         The index ranges in value from 0 to 1 (the higher the value the higher the diversity) and can be interpreted as the:
                             
                         * _probability that two individuals selected at random from a population 'do not' belong to the same group._  
                        
                         The data are drawn from the Integrated Post-Secondary Education Data System for the period 2010-2020 and include 1960 public and private-nonprofit institutions.

                            '''), width = '8', 
                        ), # close column
                   
                    dbc.Col(
                       dcc.Markdown('''
               
                           #### Explore the Map:
                           
                           * _Select one or more institutional sectors for display._
                           
                           * _Use zoom and pan features to change location or scale._
                           
                           * _Hover over a marker to view campus information._
                   
                           * _Use the time player to see changes in over time._
                           

                           '''), width = '3', style={'background-color': '#F5F5F5', 'padding-top': '20px'} 
                           ), # close column
                   ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
            ), # close row
                            
            dbc.Row([

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Select an Institution Sector", className="card-title"),
                        dcc.Checklist(
                            id='map_sector',
                            options=[{'label': i, 'value': i} for i in sector_choice],
                            value=['Public'],
                            inputStyle={"margin-right": "20px", "margin-left": '20px'},  # space box and text
                            style={
                                'font-style': 'italic',
                                'color': 'white',
                                'border': 'round'},
                                ), #close checklist
                            ])  # close card body
                        ], color="success", inverse=True, outline=False), #close card
                    width = '4') # close col
                ], style={'margin-left': '70px','margin-top': '15px','margin-bottom': '15px'}, justify="start"
            ),# close row              

            dbc.Row([
                dbc.Col(
                    html.H6('Simpsons Index of Diversity: measures the probability that two individuals randomly selected from a sample will belong to the same category. Changes in Simpson\'s index are indicated by marker color and size to aid interpretation.',
                        style={
                            'padding-top' : '20px',
                            'font-style': 'italic',
                            'font-weight': 'bold'}),
                    width ='11'), # close col
                ], style={'margin-left': '38px'}, justify = 'around'
            ), # close row
         
            dbc.Row([
                
                dbc.Col(dcc.Graph(id='stem_simpson', 
                            figure={},
                            config={
                                'doubleClick':False,
                                'displayModeBar':True,
                                'watermark':False},
                            className="border border-2"
                        ), width='11')
                ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '30px'}, justify="around"
            ), #close row
           
        
            dbc.Row([      
                dbc.Col(
                    dcc.Markdown('''
                                 
                        #### Questions to Consider:
    
                         * Which institutions have the highest/lowest racial diversity scores in STEM?
                         
                         * Which institutions have made progress toward greater racial representation among STEM graduates?   
                         
                         * What institutional factors included here may be important to diversity goals in STEM?
    
                            '''), width = '8', 
                        ), # close column
                ], style={'margin-left': '38px','margin-top': '20px','margin-bottom': '5px', 'margin-right':'20'}, justify="start"
            ), #close row
                        
            
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('''
                                 #### Sources
                                 
                                 [Computer Science.org](https://www.computerscience.org/resources/diversity-inclusion-in-stem/)
                                 
                                 [US Bureau of Labor Statistics](https://www.bls.gov/opub/btn/volume-10/why-computer-occupations-are-behind-strong-stem-employment-growth.htm)
                                 
                                 [Pew Research](https://www.pewresearch.org/fact-tank/2021/04/14/6-facts-about-americas-stem-workforce-and-those-training-for-it/)
                                 
                                 [Simpson's Index of Diversity](http://www.countrysideinfo.co.uk/simpsons.htm)
                                  
                                 [British Education Research Journal](https://eric.ed.gov/?q=Oxford+AND+debate&id=EJ1204728)
                                 
                                 #### Data
                                 
                                 [Integrated Postsecondary Education Database System](https://nces.ed.gov/ipeds/)
                                 
                                 _Note: data selected for this project comprise the period from 2010-2020, excluding 2011-12 and 2016-17. The latter were omitted due to data quality concerns. STEM completion totals used to calculate Simpson's Index of Diversity (in aggregate) included the following disciplines: Computer Science, Biological Science, Engineering, Mathematics, and Physcial Science._
                                 
                            ''')
                        ]), #close column  
                ], style={'margin-left': '38px','margin-top': '10px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
            ), # close row
                        
            
            dcc.Store(id='datasets')  # table data

        ])  # close html div

    ], label="Racial Diversity"),  # close dbc.Tab1


# =============================================================================
# Tab 2
# =============================================================================

    dbc.Tab([
        
        dbc.Row([dbc.Col(html.Div(
            html.H1("Progress Within and Across Institutions.",
                    style={
                           'padding-top' : '40px',
                           'padding-bottom' : '10px',
                           'font-size': '50',
                           'font-weight': 'bold'},
                           )), 
                width='11') # close col
            ], justify='around'
        ), # close row
        
        dbc.Row([
            
            dbc.Col(
                dcc.Markdown('''  
            
                    Benchmarks are an important assessment tool for institutions seeking to diversify racial representation and completion in undergraduate STEM programs. With appropriate metrics and review, educators can make informed decisions around goals, resource allocation, and performance.   

                    Trends in STEM graduation across racial categories are generally aggregated at the national level for reporting purposes. 

                    This application provides quick-search capabilities that highlight institution-level trends in racial composition within and across years over the past decade based on Simpson’s Index of Diversity - providing potential benchmarks for assessment and comparison to peer institutions.  

                '''), width = '11'
                ), # close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), #close row
            
        dbc.Row([       
                dbc.Col(
                    dcc.Markdown('''
        
                    #### Use and Interpret This Page:
                    
                    **Institution-level trends in Simpson's Index of Diversity (2010-2020) are represented in Figure 1. Three categories are defined for this purpose:**
                    
                    * _Decreasing - institutions where racial diversity among STEM graduates has declined over the period._
                    
                    * _Unchanged - institutions where racial diversity among STEM graduates has been relatively stable._
                    
                    * _Increasing - institutions where racial diversity among STEM graduates has grown over the period._
                    
                    **The categories are formed on the basis of a linear model fit to annual calculations of Simpson's index.**
                    
                    * _Use the check-list to view the distribution of institutions identified within each category._ 
                    
                    * _Hover over an institution marker on the map (Figure 1) - data rendered include the slope of this trendline._ 
                    
                    * _Slopes < -.009 = Decreasing; slopes between  -.009 and .009 = Unchanged; slopes .010 and above = Increasing._
                    
                    * _Note: the direction of trend is relative and does not indicate the magnitude of Simpson's Index of Diversity scores._ 
            
                    **The figures can be used to cross-filter additional information for each institution.** 
            
                    * _Double-click on a map marker to update Figure 2: which provides annual measurements of Simpson's Index of Diversity as well as the average value for all institutions combined._
                    
                    * _Hover over a 'node' in Figure 2 (blue) to update Figure 3: which graphs the racial composition of STEM graduates for a given academic year at the selected institution._
                    

                    '''), width = '11', style={'background-color': '#F5F5F5', 'padding-top': '20px'} 
                    ), # close column
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), # close row
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Select a Category", className="card-title"),
                        dcc.Checklist(
                            id ='map2_trend',
                            options=[{'label': i, 'value': i} for i in slope_interval_choice],
                            value=['Increasing'],
                            inputStyle={"margin-right": "20px", "margin-left": '20px'},  # space box and text
                            style={
                                'font-style': 'italic',
                                'color': 'white',
                                'border': 'round'},
                                ), #close checklist
                            ]),  # close card body
                        ], color="success", inverse=True, outline=False), #close card
                    width = '6') # close col
                ], style={'margin-left': '70px','margin-top': '15px','margin-bottom': '15px'}, justify="start"
            ),# close row         
    
    dbc.Row([
        dbc.Col(
            html.H6('Trend in Simpsons Index of Diversity across institutions: 2010-2020.',
                style={
                    'padding-top' : '20px',
                    'font-style': 'italic',
                    'font-weight': 'bold'}
                ),
            width ='11'), #close col
        ], style={'margin-left': '38px'}, justify = 'around'
    ), # close row
        
        dbc.Row([
            dbc.Col(dbc.Card(
                dcc.Graph(id='map2', figure={},
                    config={
                        'doubleClick':False,
                        'displayModeBar':True,
                        'watermark':False}
                    ),
                ), 
            width='11'), # close col
        ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '15px'}, justify="around"
    ), #close row
        
        
# Graphs for individual institution and distribution
        
        dbc.Row([
            dbc.Col(
                html.H6('Click on Institution Marker in Figure 1 to update Figure 2.',
                    style={
                        'padding-top' : '20px',
                        'font-style': 'italic',
                        'font-weight': 'bold'}),
            width ='5'), #close col
        
            dbc.Col(
                html.H6('Hover over a line-node in Figure 2 to update Figure 3 by Year.',
                    style={
                        'padding-top' : '20px',
                        'font-style': 'italic',
                        'font-weight': 'bold'}),
                width ='5'), # close col
            ], style={'margin-left': '38px'}, justify = 'around'
        ), # close row
     
        dbc.Row([
            dbc.Col(dcc.Graph(id='inst_trend', figure={},
                className='shadow',
                config={
                    'doubleClick':False,
                    'displayModeBar':False,
                    'watermark':False}), 
                    width='5',
                    lg={'size':5}), 
            
            dbc.Col(dcc.Graph(id='inst_ethnicity', figure={},
                className='shadow',
                config={
                    'doubleClick':False,
                    'displayModeBar':False,
                    'watermark':False}), 
                    width='5',
                    lg={'size':5}
                ) # close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '15px'}, justify="around"
        ),  # close row
        
    ], label="Institutions"), # close tab 2
    
# =============================================================================
# Tab 3 
# =============================================================================
    
    dbc.Tab([
        
        dbc.Row(dbc.Col(html.Div(
            html.H1("Highest and Lowest Scores by Year",
                    style={
                           'padding-top' : '40px',
                           'padding-bottom' : '20px',
                           'font-size': '50',
                           'font-weight': 'bold'}
                           )
                    ), width='11'
                ), justify='around' # close col
        ), # close row
        
        dbc.Row([
            
            dbc.Col(
                dcc.Markdown('''  
            
                    Institutions that host racially diverse undergraduate STEM programs can serve as models for other institutions. And provide a talent pool for employers seeking skilled workers accustomed to racially diverse settings.
            
                    This application supports complex queries that enable users to identify insitutions at the high and low end of annual diversity scores as well as overall trend. 
            
                    Simpson's Index of Diversity forms the basis for these comparisons. 

                '''), width = '11'
                ), # close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), #close row
            
        dbc.Row([       
                dbc.Col(
                    dcc.Markdown('''
        
                        #### Construct Data Tables:
\
                        **The top 10 and bottom 10 ranked insititutions (based on diversity score) can be generated for a given year using the dropdown lists below**
                    
                        * _First select a year and then select from the remaining dropdown lists._
                    
                        * _List selections can be updated individually once the data tables have been rendered._
                    
                        **The top 10 and bottom 10 ranked insititutions based on overall diversity trend can be generated based on metric**
                    
                        * _Use the metric dropdown-list to view groupings based on overall diversity trend._

                    '''), width = '11', style={'background-color': '#F5F5F5', 'padding-top': '20px'} 
                    ), # close column
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), # close row
        

        dbc.Row([
             dbc.Col(dbc.Card([
                 dbc.CardBody([
                     html.H4("Select a Year", className="card-title"),
                     dcc.Dropdown(id='year_drop', 
                        options=[{'label': i, 'value': i} for i in df["Year"].unique()], 
                        value=None,
                        style={
                            'font-style': 'italic',
                            'color': 'darkblue'}),
                     ]), # close card body
                 ], color="success", inverse=True, outline=False), # close card 
            width='3'), #close col

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Select a Sector", className="card-title"),
                        dcc.Dropdown(id='sector_drop',
                            options=[], 
                            style={
                                'font-style': 'italic',
                                'color': 'darkblue'},
                            value=None),
                        ]), # close card body
                  ], color="success", inverse=True, outline=False), # close card 
            width = '3'), # close col

              dbc.Col(dbc.Card([
                  dbc.CardBody([
                      html.H4("Select a Size", className="card-title"),
                          dcc.Dropdown(id='size_drop',
                            options=[],
                            style={
                                'font-style': 'italic',
                                'color': 'darkblue'},
                            value=None),
                          ]), # close card body
                      ], color="success", inverse=True, outline=False), # close card 
                  width='3'), # close col   
            ], style={'margin-left': '70px','margin-top': '15px','margin-bottom': '15px'}, justify="start"
        ), #close row

        dbc.Row([dbc.Col(
            html.H6("Top 10 Institutions Ranked by Diversity Score",
                style={
                    'padding-top' : '20px',
                    'padding-bottom' : '20px',
                    'font-style': 'italic',
                    'color': 'darkblue',
                    'font-weight': 'bold'}), width = '11'
                ) #close col
            ], justify = 'around'
        ), #close row
        
        dbc.Row([
            dbc.Col(
                html.Div(
                    id="top_10"), 
                    width='11',
                    lg={'size':11}
                ), # close col
            ], justify = 'around', style={'paddingTop': 5}
        ), #close row
        
        dbc.Row([
            dbc.Col(
                html.H6("Bottom 10 Institutions Ranked by Diversity Score",
                    style={
                        'padding-top' : '20px',
                        'padding-bottom' : '10px',
                        'font-style': 'italic',
                        'color': 'darkblue',
                        'font-weight': 'bold'}
                    ),width = '11'
                ) #close col
            ], justify = 'around'
        ), #close row
        
        dbc.Row([
            dbc.Col(
                html.Div(
                    id="bot_10"), 
                    width='11',
                    lg={'size':11}
                ), # close  col
            ], justify = 'around', style={'paddingTop': 20}
        ),#close row

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Metric", className="card-title"),
                            dcc.Dropdown(id='inst_slope',
                                options=[{'label': i, 'value': i} for i in metric_choice],
                                style={
                                    'font-style': 'italic',
                                    'color': 'darkblue'}, value=None),
                            ]), # close card body
                         ], color="success", inverse=True, outline=False), # close card 
                 width= '3'), # close col    
            ], style={'margin-left': '70px','margin-top': '20px','margin-bottom': '15px'}, justify="start"
        ), #close row #close row 

        dbc.Row([
            dbc.Col(
                html.H6("Top 10 Institutions Ranked by Overall Diversity Trend.",
                    style={
                        'padding-top' : '20px',
                        'padding-bottom' : '20px',
                        'font-style': 'italic',
                        'color': 'darkblue',
                        'font-weight': 'bold'}), width = '11'
                ) #close col
            ], justify = 'around'
        ), #close row
        
        dbc.Row([
            dbc.Col(
                html.Div(id="metric_top10"), 
                    width='11',
                    lg={'size':11}
                ), # close col   
            ], justify = 'around', style={'paddingTop': 5}
        ), #close row
        
        dbc.Row([
            dbc.Col(
                html.H6("Bottom 10 Institutions Ranked by Overall Diversity Trend",
                    style={
                        'padding-top' : '20px',
                        'padding-bottom' : '20px',
                        'font-style': 'italic',
                        'color': 'darkblue',
                        'font-weight': 'bold'}), width = '11'
                ) #close col
            ], justify = 'around'
        ), #close row
                
        dbc.Row([
            dbc.Col(
                html.Div(id="metric_bot10"), 
                    width='11',
                    lg={'size':11}
                    ), # close col   
            ], justify = 'around', style={'paddingTop': 5}
        ), #close row      

    ], label="Scorings"), # close tab 3

# =============================================================================
# Tab 4 
# =============================================================================

    dbc.Tab([
        
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H1("Disaggregating Institutional Factors",
                            style={
                                'padding-top' : '40px',
                                'padding-bottom' : '10px',
                                'font-size': '50',
                                'font-weight': 'bold'}
                           )
                    ), width='11'
                ) # close col
            ], justify='around'
        ), # close row
        
        dbc.Row([
            
            dbc.Col(
                dcc.Markdown('''
            
                    This application disagregates institutional characteristics (Sector, Region, Location, Size) to facilitate comparisons across peer campuses.   
            
                    The characteristics included provide a starting point for considering a broader range of factors that may be associated with racial diversity in STEM programs.   

                    '''), width = '11'
                ), #close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), #close row
            
        dbc.Row([       
                dbc.Col(
                    dcc.Markdown('''
        
                        #### How to Interpret the Graphs:
 
                        **Each graph displays differences in Simpson's Index of Diversity over time for a selected institutional characteristic**
                    
                        * _Each characteristic is comprised of two or more levels - i.e., subcategories._
                    
                        * _Color shade is used to encode the value of diversity scores to enable comparison across subcategories._
                    
                        * _Lighter shades within a color gradient indicate higher diversity scores. Considering location, for example, average diversity scores are highest in urban locations._   

                    '''), width = '11', style={'background-color': '#F5F5F5', 'padding-top': '20px'} 
                ), # close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), # close row
        
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Metric", className="card-title"),
                            dcc.Dropdown(id='heatmaps',
                                options=[{'label': i, 'value': i} for i in metric_choice],
                                style={
                                    'font-style': 'italic',
                                    'color': 'darkblue'},
                                value='Simpson'),
                            ]), # close card body
                        ], color="success", inverse=True, outline=False), # close card 
                width= '3'), # close col
            ], style={'margin-left': '70px','margin-top': '20px','margin-bottom': '25px'}, justify="start"
        ), #close row #close row  

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='hmap_sector', figure={}), 
                    className='shadow',
                    width = '11',
                    lg={'size':11}
                    ) # close col
            ], style={'margin-left': '40px','margin-top': '20px','margin-bottom': '15px'}, justify="around"
        ), # close row
        
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='hmap_region', figure={}),
                    className='shadow',
                    width = '11',
                    lg={'size':11},
                    align="center"
                ),# close col
            ], style={'margin-left': '40px','margin-top': '20px','margin-bottom': '15px'}, justify="around"
        ), # close row
        
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='hmap_location', figure={}), 
                    className='shadow',
                    width = '11',
                    lg={'size':11},
                    align="center" 
                ), # close col
            ], style={'margin-left': '40px','margin-top': '20px','margin-bottom': '15px'}, justify="around"
        ), # close row
    
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='hmap_size', figure={}),
                    className='shadow',
                    width = '11',
                    lg={'size':11},
                    align="center" 
                    ), # close col
            ], style={'margin-left': '40px','margin-top': '20px','margin-bottom': '15px'}, justify="around"
        ), #Close row
    ], label = 'Trends'), # close tab

# =============================================================================
# tab 5
# =============================================================================

    dbc.Tab([
        
        dbc.Row(
            [dbc.Col(
                html.Div(
                    html.H1("Make a Connection.",
                        style={
                           'padding-top' : '40px',
                           'padding-bottom' : '10px',
                           'font-size': '50',
                           'font-weight': 'bold'},
                           )
                        ), width='11'
                ) # close col
            ], justify='around'
        ), # close row
        
        dbc.Row([
            dbc.Col(
                dcc.Markdown('''
            
                    This application was created by Dr. Sean Connin to help support efforts around racial inclusion in post-secondary STEM education. Updates are planned to incorporate data on gender and disciplinary field.
                    
                    Feedback and suggestions for further improvement are welcome. 
                    
                    The author can be contacted at [Sean Connin](/https://www.linkedin.com/in/sean-connin-7b06b425/).
                    
                    '''), width = '11'
                ), #close col
            ], style={'margin-left': '38px','margin-top': '15px','margin-bottom': '5px', 'margin-right':'20'}, justify="around"
        ), #close row
        
    ],label='About'), # close tab

])  # close dbc.Tabs

# =============================================================================
# tab 1 callback
# =============================================================================

@app.callback(
        Output('datasets', 'data'), 
        Input('map_sector', 'value')
        )   #close callback

def clean_data(value):
    
    df_map = df[df['Sector'].isin(value)]

    df_map = df_map.groupby(['Name', 'Year', 'State', 'City', 'Region',
                        'Sector', 'Latitude', 'Longitude', 'Metric', 'Size'], as_index=False).agg('mean', 1)
    df_map = df_map.sort_values(by=['Year'])

# Simpson index

    df_sim = df_map[df_map['Metric'] == 'Simpson']
    df_sim.rename(columns={'Value': 'Simpson Diversity Index'}, inplace=True)

    datasets = {
        'df_sim': df_sim.to_json(orient='split', date_format='iso')
        }

    return json.dumps(datasets)

@app.callback(
        Output(component_id = 'stem_simpson', component_property = 'figure'),
        Input(component_id = 'datasets', component_property = 'data')
    ) # close callback

def update_simpson(datasets):
    
    datasets = json.loads(datasets)
    df_sim = pd.read_json(datasets['df_sim'], orient='split')

# Create map

    stem_simpson = px.scatter_mapbox(df_sim,
            lat='Latitude',
            lon='Longitude',
            center={"lat": 38.91478, "lon": -96.17902},
            zoom=3.0,
            color='Simpson Diversity Index',
            size='Simpson Diversity Index',
            size_max=12,
            color_continuous_scale="Viridis",
            hover_name='Name',
            hover_data={
                'Year': True,
                'City': True,
                'Latitude': False,
                'Longitude': False,
                'Sector': True,
                'Size': True,
                'Simpson Diversity Index': True},      
            opacity=0.5,
            animation_frame='Year',
            height=650,
            title='Figure 1. Diversity in Undergraduate STEM Programs: Simpson Index',
            labels={'Simpson Diversity Index': 'Simpsons Index of Diversity'},
        ) # close mapbox

    return stem_simpson 

# =============================================================================
# Tab 2 Callback
# =============================================================================

@app.callback(
        Output('map2', 'figure'), 
        Input('map2_trend', 'value')
    ) #close callback

def tab2_map(value):
    
    df_map2 = df_coeff[df_coeff["Trend"].isin(value)]

#Create map
    
    map2 = px.scatter_mapbox(df_map2, 
                lat = 'Latitude',
                lon = 'Longitude',
                center = {"lat": 38.91478, "lon": -96.17902},
                zoom = 2.8,
                color = 'Trend',
                color_discrete_sequence=['#e9b91c', '#ae1324', '#ce7b12'],
                category_orders={"Trend": ['Decreasing', 'Unchanged', 'Increasing']},
                hover_name= 'Name',
                hover_data={
                    'Latitude': False,
                    'Longitude': False,
                    'Sector': True,
                    'Size': True,
                    'Slope':True},
                opacity = 0.7,
                height=500,                 
                title = "Figure 1. Overall Trend in Simpson's Index of Diversity by Institution",
                labels={'Simpsons Index Score':'Simpson Index of Diversity'}
            ) # close map

    map2.update_traces(marker={'size': 9}),
    
    return map2

@app.callback(
        Output(component_id='inst_trend', component_property='figure'),
        Input(component_id='map2', component_property='clickData')
    ) # close callback

def inst_trends(clickData):

    if not clickData:
        inst_name = 'Trinity University'
    else:
        inst_name = clickData['points'][0]['hovertext'] # hovertext provides inst name 

    # subset data to instition identifed by hover

    inst_df = df[df["Name"] == inst_name]  # filter name via. hover
    inst_df = inst_df[inst_df["Metric"] == "Simpson"]
    inst_df = inst_df.sort_values(by=['Year'])
    
    annual_range = {'Year': ['2010-2011', '2012-2013', '2013-2014', '2014-3015', '2015-2016', '2017-2018', '2018-2019', '2019-2020'], 'Mean': [.31,.33, .35, .36, .37, .39,.40, .41], 'QRT_25':[.16, .18, .20, .21, .22, .25, .26, .27], 'QRT_75':[.45, .48, .50, .51, .52, .54, .55, .56]}

    annual_range = pd.DataFrame(annual_range)
    
# Build figure 2

    inst_fig = px.line(inst_df, x='Year', y='Value', 
                       template='plotly_white',
                       category_orders={"Year": ['2010-2011', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2017-2018', '2018-2019', '2019-2020']},
                       hover_data={
                           'Year': True,
                           'Value': True,
                           'Sector': False},
                       custom_data=['Name'],
                       height = 400,
                       title='Figure 2. Simpsons Index of Diversity vs. Year:<br> {}'.format(inst_name),
                markers=True
            )# close fig

    inst_fig.update_layout(
        xaxis_title="Academic Year",
        yaxis_title="Simpson Index Score",
        yaxis_range=[0,1])

    inst_fig.update_traces(line_color='#26828e', line_width=3)
    inst_fig.update_traces(name=inst_name, showlegend = True)
    
    inst_fig.add_trace(
        go.Scatter(
            x=['2010-2011', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2017-2018', '2018-2019', '2019-2020'],
            y=[.31,.33, .35, .36, .37, .39,.40, .41],
            hoverinfo='skip',
            line=go.scatter.Line(color="gray"),
            showlegend=True,
            name='Mean of Institutions')
        ) # close trace
    
    inst_fig.update_layout(
        legend=dict(  #postion the legend inside the graph
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01)
        )# close update

    return inst_fig

# Build figure 3

@app.callback(
        Output(component_id='inst_ethnicity', component_property='figure'),
        Input(component_id='inst_trend', component_property='hoverData')
    ) #close callback

def update_distribution(hoverData):

    if not hoverData:
        inst_year = '2010-2011'
        inst_name = 'Trinity University'
    else:
        inst_year = hoverData['points'][0]['x']
        inst_name = hoverData['points'][0]['customdata'][0]

    df_e = df_ethnic[(df_ethnic['Year'] == inst_year) & (df_ethnic['Name'] == inst_name)]
    df_e["Percent"] = df_e["Percent"].astype(float)
    df_e = df_e.sort_values(by=['Ethnicity'], ascending=False)

    hist_fig = px.bar(df_e, x= 'Ethnicity', y = 'Percent',
                            title='Figure 3. Racial Composition at {}: <br> Year = {}'.format(
                                inst_name, inst_year),
                            color = 'Percent',
                            height = 400,
                            template="plotly_white"
                    ) # close fig

    hist_fig.update_layout(
        xaxis_title="Racial Category",
        yaxis_title="Percent of Total Stem Graduates")
    
    hist_fig.update_traces(marker_color='#26828e')
 
    hist_fig.update(layout_coloraxis_showscale=False)
    
    return hist_fig

# =============================================================================
# Tab 3 callback
# =============================================================================

# Build tables

@app.callback(
        Output('sector_drop', 'options'),
        Input('year_drop', 'value')
    ) #close callback

def update_dropdown_2(yr):

    if(yr != None):
        df_filtered = df[(df["Year"]==yr)]
        return [{'label': i, 'value': i} for i in sector_choice]
    else:
        return []
    
@app.callback(
        Output('size_drop', 'options'),
        Input('sector_drop', 'value'),
    ) # close callback

def update_dropdown_3(sect):
    if(sect != None):
        df_filtered = df[(df["Sector"]==sect)]
        return [{'label': i, 'value': i} for i in size_choice]
    else:
        return []
    
@app.callback(
        Output('top_10', 'children'),
        Input('year_drop', 'value'),
        Input('sector_drop', 'value'),
        Input('size_drop', 'value')
    ) #close callback

def update_top10(yr, sect, size): 

    if(yr != None and sect != None and size != None):
        df_filtered = df[(df["Year"]==yr) & (df["Sector"]==sect) & (df["Size"]==size) & (df["Metric"]=='Simpson')] 
        df_filtered = df_filtered.loc[:, ['Name', 'Year', 'Sector', 'State', 'Metric', 'Size', 'Value']]
        df_filtered = df_filtered.sort_values(['Value'], ascending=[False])
        df_filtered = df_filtered.head(10)

        return [dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            sort_action="native",
                style_cell_conditional=[
                    {'if': {'column_id': c},
                     'textAlign': 'left'} for c in ['Name', 'Year']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'}
                ) # close data table
            ] # close dash table
    else:
        print("none")
        return []
    
@app.callback(
        Output('bot_10', 'children'),
        Input('year_drop', 'value'),
        Input('sector_drop', 'value'),
        Input('size_drop', 'value')
    ) # close callback
    
def update_bot10(yr, sect, size):
    
    if(yr != None and sect != None and size != None): # and met != None
        
        df_filtered = df[(df["Year"]==yr) & (df["Sector"]==sect) & (df["Size"]==size) & (df["Metric"]== "Simpson")] 
        df_filtered = df_filtered.loc[:, ['Name', 'Year', 'Sector', 'State', 'Metric', 'Size', 'Value']]
        df_filtered = df_filtered.sort_values(['Value'], ascending=[False])
        df_filtered = df_filtered.tail(10)

        return [dash_table.DataTable(
            id='table2',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            sort_action="native",
                style_cell_conditional=[
                    {'if': {'column_id': c},
                     'textAlign': 'left'} for c in ['Name', 'Year']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'}
                ) # close data table
            ] #close dash table
    else:
        print("none")
        return []
    
# callback for slope tables

@app.callback(
        Output('metric_top10', 'children'),        
        Input('inst_slope', 'value')
    ) # close callback

def update_slope(inst_slope):
    
    if(inst_slope != None):
        df_c = df_coeff[(df_coeff["Metric"]==inst_slope)]
        df_c = df_c.loc[:, ['Name', 'Sector', 'Location', 'Size', 'Metric',  'Slope']]
        df_c['Slope'] = df_c['Slope'].round(decimals = 2)
        df_c = df_c.sort_values(['Slope'], ascending=[False])
        df_c = df_c.head(10)
    
        return [dash_table.DataTable(
            id='metric_top',
            columns=[{"name": i, "id": i} for i in df_c.columns],
            data=df_c.to_dict('records'),
            sort_action="native",
                style_cell_conditional=[
                    {'if': {'column_id': c},
                     'textAlign': 'left'} for c in ['Name', 'Year']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'}
        )]
    else:
        print("none")
        return []
        
@app.callback(
        Output('metric_bot10', 'children'),        
        Input('inst_slope', 'value')
    ) # close callback

def update_slope2(inst_slope):
    
    if(inst_slope != None):
        df_c2 = df_coeff[(df_coeff["Metric"]==inst_slope)]
        df_c2 = df_c2.loc[:, ['Name', 'Sector', 'Location', 'Size', 'Metric',  'Slope']]
        df_c2 = df_c2.sort_values(['Slope'], ascending=[False])
        df_c2['Slope'] = df_c2['Slope'].round(decimals = 2)
        df_c2 = df_c2.tail(10)
        
        return [dash_table.DataTable(
            id='metric_bot',
            columns=[{"name": i, "id": i} for i in df_c2.columns],
            data=df_c2.to_dict('records'),
            sort_action="native",
                style_cell_conditional=[
                    {'if': {'column_id': c},
                     'textAlign': 'left'} for c in ['Name', 'Year']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'}
        )]
    else:
        print("none")
        return []

# =============================================================================
# Tab 4 callback
# =============================================================================

#heat maps

@app.callback(
        Output('hmap_sector', 'figure'),
        Output('hmap_region', 'figure'),
        Output('hmap_location', 'figure'),
        Output('hmap_size', 'figure'), 
        Input('heatmaps', 'value')
    ) # close callback

def heat_maps(heatmaps):
    
    df_heat = df[df['Metric'] == heatmaps]
    df_heat = df_heat[(df_heat['Region'] != 'Not_Reported') & (df_heat['Location'] != 'Not_Reported') & (df_heat['Size'] != 'Not_Reported')]

    hmap_sector =px.density_heatmap(df_heat, x="Year", y="Sector", z="Value",  
                histfunc="avg",
                color_continuous_scale='Teal_r', # r for reversed
                title='Figure 1. Change in Average {} Score by <br>Sector and Year'.format(heatmaps),
                height = 500)
    
    hmap_sector.update_layout(
        xaxis_title="Academic Year",
        yaxis_title="Sector",
        title_x=0.15)
    
    hmap_sector.update_yaxes(ticksuffix = "  ")
    
    hmap_sector.update_xaxes(tickangle=45)
    
    hmap_region = px.density_heatmap(df_heat, x="Year", y="Region", z="Value",
                histfunc="avg",
                color_continuous_scale='gray',
                category_orders={"Region": ['Far_West', 'Southwest', 'Mid_East', 'Southeast', 'New_England', 'Rocky_Mountains', 'Great_Lakes', 'Plains']},
                title='Figure 2. Change in Average {} Score by<br>Region and Year'.format(heatmaps),
                height = 500,
                template="plotly_white")

    hmap_region.update_layout(
        xaxis_title="Academic Year",
        yaxis_title="Region",
        title_x=0.15)
    
    hmap_region.update_yaxes(ticksuffix = "  ")
    
    hmap_region.update_xaxes(tickangle=45)

    hmap_location = px.density_heatmap(df_heat, x="Year", y="Location", z="Value",
                histfunc="avg",
                title='Figure 3. Change in Average {} Score by <br>Location and Year'.format(heatmaps),
                color_continuous_scale='Purples_r',
                height = 500,
                template="plotly_white")
    
    hmap_location.update_layout(
        xaxis_title="Academic Year",
        yaxis_title="Location",
        title_x= 0.15)
    
    hmap_location.update_yaxes(ticksuffix = "  ")
    
    hmap_location.update_yaxes(autorange="reversed")
    
    hmap_location.update_xaxes(tickangle=45)
    
    hmap_size = px.density_heatmap(df_heat, x="Year", y="Size", z="Value",
                histfunc="avg",
                color_continuous_scale='OrRd_r',
                category_orders={"Size": ['< 1,000', '1,000 - 4,999', '5,000 - 9,999', '10,000 - 19,999', '20,000 +']},
                title='Figure 4. Change in Average {} Score by<br>Size and Year'.format(heatmaps),
                height = 500,
                template="plotly_white")
    
    hmap_size.update_layout(
        xaxis_title = "Academic Year",
        yaxis_title = "Institution Size",
        title_x=0.15)
    
    hmap_size.update_yaxes(ticksuffix = "  ")
    
    hmap_size.update_yaxes(autorange="reversed")
    
    hmap_size.update_xaxes(tickangle=45)
    
    return hmap_sector, hmap_region, hmap_location, hmap_size
  
#app calls

if __name__ == '__main__':
    app.run_server(debug = True, use_reloader=False)