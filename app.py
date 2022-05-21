#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import dash_auth



# # Load and clean data

# In[5]:


##Overall Score

zocial_df = pd.read_excel("Zocial Metric.xlsx", converters={'Facebook ID (Edited)':str,'Twitter ID (Edited)':str,
                                                           'Instagram ID (Edited)':str})

indicators_category = zocial_df['Category'].sort_values().unique()
indicators_platform = ['Overall Score','Facebook Score','Twitter Score', 'Instagram Score', 'Youtube Score']

##############################################################################################
##Facebook Score

facebook_df = pd.read_csv('Facebook Score.csv', converters={'Account ID':str})
facebook_df.replace('Dessert & Beverage Café', 'Dessert & beverage café', inplace=True)

indicators_category_facebook = facebook_df['Category'].sort_values().unique()
indicators_category_facebook = indicators_category_facebook.tolist()
indicators_metric_facebook = list(facebook_df.iloc[:,-16:].columns)

for i in indicators_metric_facebook[:-2]:
    breaklist = i.split(' ')
    if 'Metric' not in breaklist:
        indicators_metric_facebook.remove(i)
        
indicators_metric_facebook = [indicators_metric_facebook[-1]] + indicators_metric_facebook[:-1]
variable_list_facebook = list(facebook_df.columns[2:11]) + list(facebook_df.columns[13:17]) + indicators_metric_facebook[1:] + [indicators_metric_facebook[0]]

##############################################################################################
##Twitter Score

twitter_df = pd.read_csv("TwitterScore(final for TW Dashboard).csv",converters = {"Account ID":str,"Twitter ID(Edited)":str})
twitter_df.replace('Dessert & Beverage Caf?','Dessert & beverage café',inplace=True)
twitter_df.replace('Dessert & beverage caf?','Dessert & beverage café',inplace=True)

indicators_category_twitter = twitter_df['Category'].sort_values().unique()
indicators_category_twitter = indicators_category_twitter.tolist()

indicators_brand_twitter = twitter_df['Brand'].unique()

indicators_month_twitter = twitter_df['Month'].unique()

twitter_df = twitter_df.rename(columns={'FollowerGrowthMetric':'Follower Growth Metric','RetweetMetric':'Retweet Metric','Retweet_FollowerMetric':'Retweet/Follower Metric',
                                       'FavoriteMetric' :'Favorite Metric','Reply_TweetMetric':'Reply/Tweet Metric','ReplyToOtherMetric':'Reply to Other Metric',
                                       'ReplyTimeMetric' :'Reply Time Metric','SentimentMetric':'Sentiment on Comments'})


twitter_metric_df = twitter_df[['Brand','Category','Month','Score','Follower Growth Metric','Favorite Metric','Retweet Metric','Retweet/Follower Metric','Reply/Tweet Metric','Reply to Other Metric','Reply Time Metric','Sentiment on Comments']]
twitter_metric_df =pd.melt(twitter_metric_df,id_vars=['Brand','Category','Month'],var_name='indicator', value_name='value')
indicators_metric_twitter = twitter_metric_df['indicator'].unique()


twitter_data_df = twitter_df[['Brand','Category','Month','Follower Count','Reply Count','Reply To Other Count', 'Reply Response Time Count','Positive Count','Negative Count','Neutral Count','Favorite','Retweet','Share on Facebook','Engagement','Tweet']]
twitter_data_df =pd.melt(twitter_data_df,id_vars=['Brand','Category','Month'],var_name='Raw Data', value_name='value')
indicators_data_twitter = twitter_data_df['Raw Data'].unique()


variable_list_twitter = list(twitter_df.columns[3:10])+list(twitter_df.columns[14:16])+list(twitter_df.columns[17:31])


twitter_df = twitter_df.astype({'Score':int,'Follower Growth Metric':int,'Favorite Metric':int,'Retweet Metric':int,'Retweet/Follower Metric':int,'Reply/Tweet Metric':int,'Reply to Other Metric':int,'Reply Time Metric':int,'Sentiment on Comments':int})

twitter_df_sentiment = twitter_df.copy()
twitter_df_sentiment["Sentiment Count"] = twitter_df_sentiment['Positive Count']+twitter_df_sentiment['Neutral Count']+twitter_df_sentiment['Negative Count']
twitter_df_sentiment = twitter_df_sentiment[["Brand","Category","Month","Score","Sentiment on Comments","Negative Count","Positive Count","Neutral Count","Sentiment Count"]]
twitter_df_sentiment["%Negative Count"] = (twitter_df_sentiment["Negative Count"]*100)/twitter_df_sentiment["Sentiment Count"]
twitter_df_sentiment["%Positive Count"] = (twitter_df_sentiment["Positive Count"]*100)/twitter_df_sentiment["Sentiment Count"]
twitter_df_sentiment["%Neutral Count"] = (twitter_df_sentiment["Neutral Count"]*100)/twitter_df_sentiment["Sentiment Count"]


##############################################################################################
#Instagram Score
instagram_df = pd.read_excel("Instagram_Final(2).xlsx")
instagram_df.replace('Dessert & Beverage CafÃ©','Dessert & beverage café',inplace=True)
instagram_df.replace('Dessert & beverage cafÃ©','Dessert & beverage café',inplace=True)

instagram_df = instagram_df.rename(columns={'month':'Month','category':'Category','account_name':'Brand','score':'Score','follower_growth_metric':'Follower Growth Metric','sentiment_on_comment_metric':'Sentiment on Comments','avg_like_metric':'Avg Like Metric','avg_comment_metric':'Avg Comment Metric','view_and_video_metric':'View and Video Metric','follower_count':'Follower Count','view':'View','post_video_count':'Post and Video Count','like_count':'Like','comment_count':'Comment'})

indicators_category_instagram = instagram_df['Category'].sort_values().unique()
indicators_category_instagram = indicators_category_instagram.tolist()

indicators_month_instagram = instagram_df['Month'].unique()

indicators_brand_instagram = instagram_df['Brand'].unique()


dfMetricInstagram= instagram_df[['Brand','Category','Month','Score','Follower Growth Metric','Sentiment on Comments','Avg Like Metric','Avg Comment Metric','View and Video Metric']]
dfMetricInstagram =pd.melt(dfMetricInstagram,id_vars=['Brand','Category','Month'],var_name='indicator', value_name='value')
indicators_metric_instagram = dfMetricInstagram['indicator'].unique()

dfDataInstagram= instagram_df[['Brand','Category','Month','Follower Count', 'Post and Video Count',
       'Positive Count', 'Neutral Count', 'Negative Count','Avg Like', 'Avg Comment', 'View',
       'View And Video', 'Like', 'Comment']]
dfDataInstagram =pd.melt(dfDataInstagram,id_vars=['Brand','Category','Month'],var_name='Raw Data', value_name='value')
indicators_data_instagram = dfDataInstagram['Raw Data'].unique()

variable_list_instagram = list(instagram_df.columns[6:11])+list(instagram_df.columns[12:24])

instagram_df = instagram_df.astype({'Score':int})
instagram_df = instagram_df.astype({'Follower Growth Metric':int})
instagram_df = instagram_df.astype({'Sentiment on Comments':int})
instagram_df = instagram_df.astype({'Avg Like Metric':int})
instagram_df = instagram_df.astype({'Avg Comment Metric':int})
instagram_df = instagram_df.astype({'View and Video Metric':int})

instagram_df_sentiment = instagram_df.copy()
instagram_df_sentiment["Sentiment Count"] = instagram_df_sentiment['Positive Count']+instagram_df_sentiment['Neutral Count']+instagram_df_sentiment['Negative Count']
instagram_df_sentiment = instagram_df_sentiment[["Brand","Category","Month","Score","Sentiment on Comments","Negative Count","Positive Count","Neutral Count","Sentiment Count"]]
instagram_df_sentiment["%Negative Count"] = (instagram_df_sentiment["Negative Count"]*100)/instagram_df_sentiment["Sentiment Count"]
instagram_df_sentiment["%Positive Count"] = (instagram_df_sentiment["Positive Count"]*100)/instagram_df_sentiment["Sentiment Count"]
instagram_df_sentiment["%Neutral Count"] = (instagram_df_sentiment["Neutral Count"]*100)/instagram_df_sentiment["Sentiment Count"]

##############################################################################################
#Youtube_score
youtube_df = pd.read_csv("Youtube Score.csv")
youtube_df.replace('Dessert & Beverage Cafรฉ','Dessert & beverage café',inplace=True)
youtube_df.replace('Dessert & beverage cafรฉ','Dessert & beverage café',inplace=True)

youtube_df = youtube_df.rename(columns={'Youtube Score':'Score','Sentiment on Comments':'Sentiment','Sentiment on Comment Metric':'Sentiment on Comments'})
youtube_df.dropna(inplace=True)

indicators_category_youtube = youtube_df['Category'].sort_values().unique()
indicators_category_youtube = indicators_category_youtube.tolist()

indicators_brand_youtube = youtube_df['Brand'].unique()
indicators_month_youtube = youtube_df['Month'].unique()

dfMetricYoutube= youtube_df[['Brand','Category','Month','Score','Subscribers Growth Metric','Sentiment on Comments','Like Views Metric','Comment Views Metric','Views Metric','Like Dislikes Views Metric']]
dfMetricYoutube =pd.melt(dfMetricYoutube,id_vars=['Brand','Category','Month'],var_name='indicator', value_name='value')
indicators_metric_youtube = dfMetricYoutube['indicator'].unique()

dfDataYoutube= youtube_df[['Brand','Category','Month','Subscriber Count',
       'Positive Count', 'Neutral Count', 'Negative Count', 'Like', 'Dislike',
       'Favorite', 'Comment', 'Views']]
dfDataYoutube =pd.melt(dfDataYoutube,id_vars=['Brand','Category','Month'],var_name='Raw Data', value_name='value')
indicators_data_youtube = dfDataYoutube['Raw Data'].unique()

variable_list_youtube = list(youtube_df.columns[5:25])


youtube_df = youtube_df.astype({'Score':int})
youtube_df = youtube_df.astype({'Subscribers Growth Metric':int})
youtube_df = youtube_df.astype({'Sentiment on Comments':int})
youtube_df = youtube_df.astype({'Like Views Metric':int})
youtube_df = youtube_df.astype({'Comment Views Metric':int})
youtube_df = youtube_df.astype({'Like Dislikes Views Metric':int})
youtube_df = youtube_df.astype({'Views Metric':int})

youtube_df_sentiment = youtube_df.copy()
youtube_df_sentiment["Sentiment Count"] = youtube_df_sentiment['Positive Count']+youtube_df_sentiment['Neutral Count']+youtube_df_sentiment['Negative Count']
youtube_df_sentiment = youtube_df_sentiment[["Account ID","Brand","Category","Month","Score","Sentiment on Comments","Negative Count","Positive Count","Neutral Count","Sentiment Count"]]
youtube_df_sentiment["%Negative Count"] = (youtube_df_sentiment["Negative Count"]*100)/youtube_df_sentiment["Sentiment Count"]
youtube_df_sentiment["%Positive Count"] = (youtube_df_sentiment["Positive Count"]*100)/youtube_df_sentiment["Sentiment Count"]
youtube_df_sentiment["%Neutral Count"] = (youtube_df_sentiment["Neutral Count"]*100)/youtube_df_sentiment["Sentiment Count"]


# # App layout

# In[6]:

VALID_USERNAME_PASSWORD_PAIRS = {
    'visualization': 'wisesight'
}

# =================================== Initiate App and Style ==================================== #

app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# =================================== App layout ==================================== #

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Overall Social Metric Score', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Facebook Score', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Twitter Score', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Instagram Score', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Youtube Score', value='tab-5', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    
# =================================== Tab 1: Overall Score ==================================== #

    if tab == 'tab-1':
        return html.Div([
            html.H1("WiseSight Social Metric Award (Overall)", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-overall',
                options=[{'label': c, 'value': c} for c in indicators_category],
                value='Airline'
            )])
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Platform',dcc.Dropdown(
                id='Platform-dropdown-overall',
                options=[{'label': c, 'value': c} for c in indicators_platform],
                value=indicators_platform[0]
            )])
        ], 
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='overall-limit-input-overall',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='overall-brand-input-overall',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 

        html.Div([
            dcc.Graph(id='LineGraph-overall')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-overall', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
                                                              8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)
        ], style={'width': '100%', 'display': 'inline-block'}),
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='BarGraph-overall')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Graph(id='Grouped-BarGraph-overall')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
]), 
        ])
    
# =================================== Tab 2: Facebook Score ==================================== #

    elif tab == 'tab-2':
        return html.Div([
            html.H1("WiseSight Social Metric Award (Facebook)", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d1-facebook',
                options=[{'label': c, 'value': c} for c in indicators_category_facebook],
                value='Airline'
            )])
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Indicator',dcc.Dropdown(
                id='ScoreAndMetric-dropdown-d1-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value="Facebook Score"
            )])
        ], 
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='facebook-limit-d1',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='facebook-d1-brand-input',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 

        html.Div([
            dcc.Graph(id='LineGraph-d1-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d1-facebook', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
       html.Div([
            dcc.Dropdown(id='metric-checklist-d1-facebook',
            options=[{'label': c, 'value': c} for c in indicators_metric_facebook], multi=True,
            style={'width': '100%','float':'right'},
            value=[indicators_metric_facebook[c] for c in range(5)])
       ]),        
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='ScoreGraph-d1-facebook')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Graph(id='Grouped-BarGraph-d1-facebook')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
], style={'border': '1px solid'}),
        
####### Layout Extention for Tab 2

        html.H1("Facebook Metric Analysis by Indicators", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d2-facebook',
                options=[{'label': c, 'value': c} for c in indicators_category_facebook],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='facebook-limit-d2',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='facebook-d2-brand-input',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})            
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
        }),
        html.Br(),
        html.Div([
            dcc.Slider(id='month-slider-d2-facebook', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='SentimentGraph-d2-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
    ], style={'border': '1px solid'}),
            
        html.H1("Relationship analysis", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value=variable_list_facebook[0]
            )])
        ],
        style={'width': '30%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value=variable_list_facebook[1]
            )])
        ],
        style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='facebook-limit-d3',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'}),
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
        }),
        html.Br(),
        html.Div([
            dcc.Slider(id='month-slider-d4-facebook', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
                
        html.Div([
            dcc.Graph(id='Relationship-graph-d3-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})

        ], style={'border': '1px solid'}),
            
        html.Div([
        html.Br(),
        html.Div([
         html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d4-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value=variable_list_facebook[0]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d4-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value=variable_list_facebook[1]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='facebook-limit-d4',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d3-facebook',
                options=[{'label': c, 'value': c} for c in indicators_category_facebook],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='facebook-d3-brand-input',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Size',dcc.Dropdown(
                id='size-dropdown-d3-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook],
                value=variable_list_facebook[0]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
        }),
        html.Div([
            dcc.Graph(id='Relationship-graph2-d3-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            dcc.Slider(id='month-slider-d3-facebook', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Data',dcc.Dropdown(
                id='Data-dropdown-d3-facebook',
                options=[{'label': c, 'value': c} for c in variable_list_facebook[:13]],multi = True,
                value=variable_list_facebook[:2]
            )])
        ], 
        style={'width': '99%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='RawData-graph-d3-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
    ], style={'border': '1px solid'}),
        html.Div([
        html.Div([
            html.Label([
                    'Category',dcc.Dropdown(
                    id='Category-dropdown-d4-facebook',
                    options=[{'label': c, 'value': c} for c in indicators_category_facebook + ["Overall"]],
                    value="Overall"
                )],style={'width': '39%', 'display': 'inline-block'}),
            ],style={'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
                    }),        
        html.Br(),
        html.Div([
            dcc.Graph(id='Heatmap-d2-facebook')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
        ], style={'border': '1px solid'})
        
        ])
        
    elif tab == 'tab-3':
        return html.Div([
            html.H1("WiseSight Social Metric Award (Twitter)", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d1-twitter',
                options=[{'label': c, 'value': c} for c in indicators_category_twitter],
                value='Airline'
            )])
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Indicator',dcc.Dropdown(
                id='ScoreAndMetric-dropdown-d1-twitter',
                options=[{'label': c, 'value': c} for c in indicators_metric_twitter],
                value=indicators_metric_twitter[0]
            )])
        ], 
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='twitter-limit-d1',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='twitter-brand-d1',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),  

        html.Div([
            dcc.Graph(id='LineGraph-d1-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d1-twitter', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
       html.Div(['Indicator',
            dcc.Dropdown(id='metric-checklist-d1-twitter',
            options=[{'label': c, 'value': c} for c in indicators_metric_twitter],multi=True,
            style={'width': '100%','float':'right'},
            value=[indicators_metric_twitter[c] for c in range(5)])
       ]),        
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='ScoreGraph-d1-twitter')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Graph(id='Grouped-BarGraph-d1-twitter')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
],style={'border': '1px solid'}),
            
####### Layout Dash 2 ###########
            
         html.H1("Twitter Metric Analysis by indicators", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d2-twitter',
                options=[{'label': c, 'value': c} for c in indicators_category_twitter],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='twitter-limit-d2',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='twitter-brand-d2',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 

        html.Div([
            dcc.Graph(id='FollowerGraph-d2-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d2-twitter', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)
        ], style={'width': '100%', 'display': 'inline-block'}),
        
        html.Br(),
            
               
        html.Div([
            dcc.Graph(id='SentimentGraph-d2-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
    ],style={'border': '1px solid'}),
            
            
####### Layout Dash 3 ##########

        html.H1("Relationship analysis", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-twitter',
                options=[{'label': c, 'value': c} for c in variable_list_twitter],
                value=variable_list_twitter[7]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-twitter',
                options=[{'label': c, 'value': c} for c in variable_list_twitter],
                value=variable_list_twitter[10]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='twitter-limit-d3',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-twitter', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            dcc.Graph(id='Relationship-graph1-d3-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
            
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-2-twitter',
                options=[{'label': c, 'value': c} for c in variable_list_twitter],
                value=variable_list_twitter[7]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-2-twitter',
                options=[{'label': c, 'value': c} for c in variable_list_twitter],
                value=variable_list_twitter[10]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='twitter-limit-d3-2',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),    
        
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d3-twitter',
                options=[{'label': c, 'value': c} for c in indicators_category_twitter],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Size',dcc.Dropdown(
                id='Size-dropdown-d3-twitter',
                options=[{'label': c, 'value': c} for c in variable_list_twitter],
                value=variable_list_twitter[9]
            )])
        ],
        style={'width': '33%','display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='twitter-brand-d3',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 
              
        html.Div([
            dcc.Graph(id='Relationship-graph2-d3-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-2-twitter', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Data',dcc.Dropdown(
                id='Data-dropdown-d3-twitter',
                options=[{'label': c, 'value': c} for c in indicators_data_twitter],multi = True,
                value=indicators_data_twitter[7:9]
            )])
        ], 
        style={'width': '99%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='Relationship-graph3-d3-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
        html.Div([
            html.Label([
                    'Category',dcc.Dropdown(
                    id='Category-dropdown-d4-twitter',
                    options=[{'label': c, 'value': c} for c in indicators_category_twitter + ["Overall"]],
                    value="Overall"
                )],style={'width': '99%', 'display': 'inline-block'}),
            ],style={'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
                    }),
            
        html.Br(),
        html.Div([
            dcc.Graph(id='Heatmap-d4-twitter')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
    ],style={'border': '1px solid'}),
    ])
    
    elif tab == 'tab-4':
        return html.Div([
            html.H1("WiseSight Social Metric Award (Instagram)", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d1-instagram',
                options=[{'label': c, 'value': c} for c in indicators_category_instagram],
                value='Airline'
            )])
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Indicator',dcc.Dropdown(
                id='ScoreAndMetric-dropdown-d1-instagram',
                options=[{'label': c, 'value': c} for c in indicators_metric_instagram],
                value=indicators_metric_instagram[0]
            )])
        ], 
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='instagram-limit-d1',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='instagram-brand-d1',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),  
        html.Div([
            dcc.Graph(id='LineGraph-d1-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d1-instagram', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
       html.Div(['Indicator',
            dcc.Dropdown(id='metric-checklist-d1-instagram',
            options=[{'label': c, 'value': c} for c in indicators_metric_instagram],multi=True,
            style={'width': '100%','float':'right'},
            value=[indicators_metric_instagram[c] for c in range(5)])
            
       ]),        
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='ScoreGraph-d1-instagram')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Graph(id='Grouped-BarGraph-d1-instagram')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
],style={'border': '1px solid'}),
            
####### Instagram Layout Dash 2 Extention #######
            
        html.H1("Instagram Metric Analysis by indicators",style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d2-instagram',
                options=[{'label': c, 'value': c} for c in indicators_category_instagram],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='instagram-limit-d2',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='instagram-brand-d2',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 

        html.Div([
            dcc.Graph(id='FollowerGraph-d2-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d2-instagram', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)
        ], style={'width': '100%', 'display': 'inline-block'}),
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='SentimentGraph-d2-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
    ],style={'border': '1px solid'}),
    
    ####### Instagram Layout Dash 3 ##########
        html.H1("Relationship analysis", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-instagram',
                options=[{'label': c, 'value': c} for c in variable_list_instagram],
                value=variable_list_instagram[0]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-instagram',
                options=[{'label': c, 'value': c} for c in variable_list_instagram],
                value=variable_list_instagram[1]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='instagram-limit-d3',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-instagram', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            dcc.Graph(id='Relationship-graph1-d3-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
            
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-2-instagram',
                options=[{'label': c, 'value': c} for c in variable_list_instagram],
                value=variable_list_instagram[0]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-2-instagram',
                options=[{'label': c, 'value': c} for c in variable_list_instagram],
                value=variable_list_instagram[1]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='instagram-limit-d3-2',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),    
        
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d3-instagram',
                options=[{'label': c, 'value': c} for c in indicators_category_instagram],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Size',dcc.Dropdown(
                id='Size-dropdown-d3-instagram',
                options=[{'label': c, 'value': c} for c in variable_list_instagram],
                value=variable_list_instagram[2]
            )])
        ],
        style={'width': '33%','display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='instagram-brand-d3',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 
              
        html.Div([
            dcc.Graph(id='Relationship-graph2-d3-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-2-instagram', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Data',dcc.Dropdown(
                id='Data-dropdown-d3-instagram',
                options=[{'label': c, 'value': c} for c in indicators_data_instagram],multi = True,
                value=indicators_data_instagram[7:9]
            )])
        ], 
        style={'width': '99%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='Relationship-graph3-d3-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
        html.Div([
            html.Label([
                    'Category',dcc.Dropdown(
                    id='Category-dropdown-d4-instagram',
                    options=[{'label': c, 'value': c} for c in indicators_category_instagram + ["Overall"]],
                    value="Overall"
                )],style={'width': '99%', 'display': 'inline-block'}),
            ],style={'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
                    }),
            
        html.Br(),
        html.Div([
            dcc.Graph(id='Heatmap-d4-instagram')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
    ],style={'border': '1px solid'}),
    ])

        
    else:
        return html.Div([   
            html.H1("WiseSight Social Metric Award (Youtube)",style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d1-youtube',
                options=[{'label': c, 'value': c} for c in indicators_category_youtube],
                value='Airline'
            )])
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Indicator',dcc.Dropdown(
                id='ScoreAndMetric-dropdown-d1-youtube',
                options=[{'label': c, 'value': c} for c in indicators_metric_youtube],
                value=indicators_metric_youtube[0]
            )])
        ], 
        style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='youtube-limit-d1',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='youtube-brand-d1',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '25%', 'float':'right','display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),  

        html.Div([
            dcc.Graph(id='LineGraph-d1-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d1-youtube', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
       html.Div(['Indicator',
            dcc.Dropdown(id='metric-checklist-d1-youtube',
            options=[{'label': c, 'value': c} for c in indicators_metric_youtube],multi=True,
            style={'width': '100%','float':'right'},
            value=[indicators_metric_youtube[c] for c in range(5)])
       ]),        
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='ScoreGraph-d1-youtube')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Graph(id='Grouped-BarGraph-d1-youtube')
        ], style={'width': '49%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
],style={'border': '1px solid'}),
            
####### Youtube Layout Dash 2 #######
            
        html.H1("Youtube Metric Analysis by indicators",style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d2-youtube',
                options=[{'label': c, 'value': c} for c in indicators_category_youtube],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='youtube-limit-d2',
                placeholder='Enter a value...',
                type='number',
                value=5,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='youtube-brand-d2',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '80%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 


        html.Div([
            dcc.Graph(id='FollowerGraph-d2-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Br(),
        
        html.Div([
            dcc.Slider(id='month-slider-d2-youtube', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)
        ], style={'width': '100%', 'display': 'inline-block'}),
        
        html.Br(),
            
        html.Div([
            dcc.Graph(id='SentimentGraph-d2-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'})
    ],style={'border': '1px solid'}),
       ####### Youtube Layout Dash 3 ##########

        html.H1("Relationship analysis", style={'textAlign': 'center'}),
        html.Div([
        html.Div([
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-youtube',
                options=[{'label': c, 'value': c} for c in variable_list_youtube],
                value=variable_list_youtube[7]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-youtube',
                options=[{'label': c, 'value': c} for c in variable_list_youtube],
                value=variable_list_youtube[10]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='youtube-limit-d3',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-youtube', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            dcc.Graph(id='Relationship-graph1-d3-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
            
        html.Div([
            html.Label([
                'Y-Axis',dcc.Dropdown(
                id='Y-Axis-dropdown-d3-2-youtube',
                options=[{'label': c, 'value': c} for c in variable_list_youtube],
                value=variable_list_youtube[7]
            )])
        ],
        style={'width': '33%', 'float': 'left','display': 'inline-block'}),
        html.Div([
            html.Label([
                'X-Axis',dcc.Dropdown(
                id='X-Axis-dropdown-d3-2-youtube',
                options=[{'label': c, 'value': c} for c in variable_list_youtube],
                value=variable_list_youtube[10]
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Top',html.Br(),dcc.Input(
                id='youtube-limit-d3-2',
                placeholder='Enter a value...',
                type='number',
                value=10,
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%','float':'right','display': 'inline-block'}),    
        
        html.Div([
            html.Label([
                'Category',dcc.Dropdown(
                id='Category-dropdown-d3-youtube',
                options=[{'label': c, 'value': c} for c in indicators_category_youtube],
                value='Airline'
            )])
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.Label([
                'Size',dcc.Dropdown(
                id='Size-dropdown-d3-youtube',
                options=[{'label': c, 'value': c} for c in variable_list_youtube],
                value=variable_list_youtube[9]
            )])
        ],
        style={'width': '33%','display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Select Brand',html.Br(),dcc.Input(
                id='youtube-brand-d3',
                placeholder='Ex. Central World, Ais',
                type='text',
                value='',
                style = {'width': '90%','display': 'inline-block'}
            )])
        ],
        style={'width': '33%', 'float':'right','display': 'inline-block'})    
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }), 
              
        html.Div([
            dcc.Graph(id='Relationship-graph2-d3-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        html.Div([
            dcc.Slider(id='month-slider-d3-2-youtube', min=0,max=12, marks={0:'All Year',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
            8:'8',9:'9',10:'10',11:'11',12:'12'},value=0)],
            style={'width': '100%', 'display': 'inline-block'}),
            
        html.Div([
            html.Label([
                'Data',dcc.Dropdown(
                id='Data-dropdown-d3-youtube',
                options=[{'label': c, 'value': c} for c in indicators_data_youtube],multi = True,
                value=indicators_data_youtube[7:9]
            )])
        ], 
        style={'width': '99%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='Relationship-graph3-d3-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20','border-bottom': '1px solid'}),
        html.Div([
            html.Label([
                    'Category',dcc.Dropdown(
                    id='Category-dropdown-d4-youtube',
                    options=[{'label': c, 'value': c} for c in indicators_category_youtube + ["Overall"]],
                    value="Overall"
                )],style={'width': '99%', 'display': 'inline-block'}),
            ],style={'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
                    }),
            
        html.Br(),
        html.Div([
            dcc.Graph(id='Heatmap-d4-youtube')
        ], style={'width': '100%', 'height': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
    ],style={'border': '1px solid'}),
    ]),

        

# =================================== Call Back ==================================== #

##Call back Overall

@app.callback(
    dash.dependencies.Output('LineGraph-overall', 'figure'),
    [dash.dependencies.Input("Category-dropdown-overall", "value"),
    dash.dependencies.Input("Platform-dropdown-overall", "value"),
    dash.dependencies.Input("overall-limit-input-overall", "value"),
    dash.dependencies.Input("overall-brand-input-overall", "value")]
)
def update_figure(Selected_Category, Selected_Platform, Selected_Limit, Selected_Brands):
    dff = zocial_df[zocial_df['Category'] == Selected_Category]
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Overall Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        zocial_df['Lower Brand'] = zocial_df['Brand'].str.lower()
        additional_df = zocial_df[zocial_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        fig = px.line(
            dff2, x = "Month", y=Selected_Platform,color = "Brand",
            title="{} Top {} by Month".format(Selected_Platform,Selected_Limit))
            
        return fig
            
    fig = px.line(
        dff, x = "Month", y=Selected_Platform,color = "Brand",
        title="{} Top {} by Month".format(Selected_Platform,Selected_Limit)
    )
    return fig

@app.callback(
    dash.dependencies.Output('Grouped-BarGraph-overall', 'figure'),
    [dash.dependencies.Input("Category-dropdown-overall", "value"),
    dash.dependencies.Input("month-slider-overall", "value"),
    dash.dependencies.Input("overall-limit-input-overall", "value"),
    dash.dependencies.Input("overall-brand-input-overall", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Limit, Selected_Brands):
    dff = zocial_df[zocial_df['Category'] == Selected_Category]
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Overall Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    dff.reset_index(inplace=True)
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        zocial_df['Lower Brand'] = zocial_df['Brand'].str.lower()
        additional_df = zocial_df[zocial_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[
                go.Bar(name='Facebook', x=dff2["Brand"], y=dff2["Facebook Score"], marker=dict(color='blue')),
                go.Bar(name='Twitter,', x=dff2["Brand"], y=dff2["Twitter Score"], marker=dict(color='#00acee')),
                go.Bar(name='Instagram', x=dff2["Brand"], y=dff2["Instagram Score"], marker=dict(color='#9370DB')),
                go.Bar(name='Youtube', x=dff2["Brand"], y=dff2["Youtube Score"], marker=dict(color='red'))])
            fig.update_layout(title="Score Top {} All Year by Platforms".format(Selected_Limit),
                             xaxis_title="Brand",yaxis_title="Score", xaxis={'categoryorder':'total descending'})
            return fig
    
        dff2 = dff2[dff2['Month'] == Selected_Month]
        fig = go.Figure(data=[
            go.Bar(name='Facebook', x=dff2["Brand"], y=dff2["Facebook Score"], marker=dict(color='blue')),
            go.Bar(name='Twitter,', x=dff2["Brand"], y=dff2["Twitter Score"], marker=dict(color='#00acee')),
            go.Bar(name='Instagram', x=dff2["Brand"], y=dff2["Instagram Score"], marker=dict(color='#9370DB')),
            go.Bar(name='Youtube', x=dff2["Brand"], y=dff2["Youtube Score"], marker=dict(color='red'))])
        fig.update_layout(title="Score Top {} in Month {} by Platforms".format(Selected_Limit,Selected_Month),
                         xaxis_title="Brand",yaxis_title="Score", xaxis={'categoryorder':'total descending'})

        return fig
    
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[
            go.Bar(name='Facebook', x=dff["Brand"], y=dff["Facebook Score"],marker=dict(color='blue')),
            go.Bar(name='Twitter,', x=dff["Brand"], y=dff["Twitter Score"],marker=dict(color='#00acee')),
            go.Bar(name='Instagram', x=dff["Brand"], y=dff["Instagram Score"],marker=dict(color='#9370DB')),
            go.Bar(name='Youtube', x=dff["Brand"], y=dff["Youtube Score"],marker=dict(color='red'))])
        fig.update_layout(title="Score Top {} All Year by Platforms".format(Selected_Limit),
                            xaxis_title="Brand",yaxis_title="Score", xaxis={'categoryorder':'total descending'})
        return fig
    
    dff = dff[dff['Month'] == Selected_Month]
    fig = go.Figure(data=[
        go.Bar(name='Facebook', x=dff["Brand"], y=dff["Facebook Score"],marker=dict(color='blue')),
        go.Bar(name='Twitter,', x=dff["Brand"], y=dff["Twitter Score"],marker=dict(color='#00acee')),
        go.Bar(name='Instagram', x=dff["Brand"], y=dff["Instagram Score"],marker=dict(color='#9370DB')),
        go.Bar(name='Youtube', x=dff["Brand"], y=dff["Youtube Score"],marker=dict(color='red'))])
    fig.update_layout(title="Score Top {} in Month {} by Platforms".format(Selected_Limit,Selected_Month),
                        xaxis_title="Brand",yaxis_title="Score", xaxis={'categoryorder':'total descending'})

    return fig

@app.callback(
    dash.dependencies.Output('BarGraph-overall', 'figure'),
    [dash.dependencies.Input("Category-dropdown-overall", "value"),
    dash.dependencies.Input("month-slider-overall", "value"),
    dash.dependencies.Input("overall-limit-input-overall", "value"),
    dash.dependencies.Input("overall-brand-input-overall", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Limit, Selected_Brands):
    dff = zocial_df[zocial_df['Category'] == Selected_Category]
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Overall Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    dff.reset_index(inplace=True)
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        zocial_df['Lower Brand'] = zocial_df['Brand'].str.lower()
        additional_df = zocial_df[zocial_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            dff2["Overall Score"] = dff2["Overall Score"].apply(round)
            fig = px.bar(
                dff2, x = "Brand", y="Overall Score",color="Brand",
                text='Overall Score',
                title="Overall Score Top {} by All Year".format(Selected_Limit)).update_xaxes(categoryorder="total descending")      
            return fig
    
        dff2 = dff2[dff2['Month'] == Selected_Month]
        dff2["Overall Score"] = dff2["Overall Score"].apply(round)
        fig = px.bar(
            dff2, x = "Brand", y="Overall Score",color="Brand",
            text='Overall Score',
            title="Overall Score Top {} in Month {}".format(Selected_Limit,Selected_Month)).update_xaxes(categoryorder="total descending")
        return fig
        
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        dff["Overall Score"] = dff["Overall Score"].apply(round)
        fig = px.bar(
            dff, x = "Brand", y="Overall Score",color="Brand",
            text='Overall Score',
            title="Overall Score Top {} by All Year".format(Selected_Limit)).update_xaxes(categoryorder="total descending")      
        return fig
    
    dff = dff[dff['Month'] == Selected_Month]
    dff["Overall Score"] = dff["Overall Score"].apply(round)
    fig = px.bar(
        dff, x = "Brand", y="Overall Score",color="Brand",
        text='Overall Score',
        title="Overall Score Top {} in Month {}".format(Selected_Limit,Selected_Month)).update_xaxes(categoryorder="total descending")
    return fig

##Call back Facebook

@app.callback(
    dash.dependencies.Output('LineGraph-d1-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-facebook", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-facebook", "value"),
    dash.dependencies.Input("facebook-limit-d1", "value"),
    dash.dependencies.Input("facebook-d1-brand-input", "value")]
)
def update_figure(Selected_Category, Selected_Platform, Selected_Limit, Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        fig = px.line(
            dff2, x = "Month", y=Selected_Platform,color = "Brand",
            title="{} Top {} by Month".format(Selected_Platform,Selected_Limit))
            
        return fig
    
    fig = px.line(
        dff, x = "Month", y=Selected_Platform,color = "Brand",
        title="{} Top {} by Month".format(Selected_Platform,Selected_Limit)
    )
    return fig

@app.callback(
    dash.dependencies.Output('Grouped-BarGraph-d1-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-facebook", "value"),
    dash.dependencies.Input("month-slider-d1-facebook", "value"),
    dash.dependencies.Input("facebook-limit-d1", "value"),
    dash.dependencies.Input("metric-checklist-d1-facebook", "value"),
    dash.dependencies.Input("facebook-d1-brand-input", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Limit, Selected_Checklist, Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in Selected_Checklist])
            fig.update_layout(title="Score by Metric Top {} All Year".format(Selected_Limit),
                              xaxis_title="Brand",yaxis_title="Score",xaxis={'categoryorder':'total descending'})
            return fig
    
        dff2 = dff2[dff2['Month'] == Selected_Month]
        fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in Selected_Checklist])   
        fig.update_layout(title="Score by Metric Top {} in Month {}".format(Selected_Limit,Selected_Month),
                         xaxis_title="Brand",yaxis_title="Score",xaxis={'categoryorder':'total descending'})

        return fig
    
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in Selected_Checklist])
        fig.update_layout(title="Score by Metric Top {} All Year".format(Selected_Limit),
                         xaxis_title="Brand",yaxis_title="Score",xaxis={'categoryorder':'total descending'})
        return fig
    
    dff = dff[dff['Month'] == Selected_Month]
    fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in Selected_Checklist])   
    fig.update_layout(title="Score by Metric Top {} in Month {}".format(Selected_Limit,Selected_Month),
                     xaxis_title="Brand",yaxis_title="Score",xaxis={'categoryorder':'total descending'})
    
    return fig

@app.callback(
    dash.dependencies.Output('ScoreGraph-d1-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-facebook", "value"),
    dash.dependencies.Input("month-slider-d1-facebook", "value"),
    dash.dependencies.Input("facebook-limit-d1", "value"),
    dash.dependencies.Input("facebook-d1-brand-input", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Limit, Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            dff2["Facebook Score"] = dff2["Facebook Score"].apply(round)
            fig = px.bar(
                dff2, x = "Brand", y="Facebook Score",color="Brand",
                text="Facebook Score",
                title="Facebook Score Top {} All Year".format(Selected_Limit)).update_xaxes(categoryorder="total descending")       
            return fig

        dff2["Facebook Score"] = dff2["Facebook Score"].apply(round)
        dff2 = dff2[dff2['Month'] == Selected_Month]
        fig = px.bar(
            dff2, x = "Brand", y="Facebook Score",color="Brand",
            text="Facebook Score",
            title="Facebook Score Top {} in Month {}".format(Selected_Limit,Selected_Month)).update_xaxes(categoryorder="total descending") 
        return fig
        
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        dff["Facebook Score"] = dff["Facebook Score"].apply(round)
        fig = px.bar(
            dff, x = "Brand", y="Facebook Score",color="Brand",
            text="Facebook Score",
            title="Facebook Score Top {} All Year".format(Selected_Limit)).update_xaxes(categoryorder="total descending")       
        return fig
    
    dff["Facebook Score"] = dff["Facebook Score"].apply(round)
    dff = dff[dff['Month'] == Selected_Month]
    fig = px.bar(
        dff, x = "Brand", y="Facebook Score",color="Brand",
        text="Facebook Score",
        title="Facebook Score Top {} in Month {}".format(Selected_Limit,Selected_Month)).update_xaxes(categoryorder="total descending") 
    return fig

@app.callback(
    dash.dependencies.Output('SentimentGraph-d2-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-facebook", "value"),
    dash.dependencies.Input("month-slider-d2-facebook", "value"),
    dash.dependencies.Input("facebook-limit-d2", "value"),
    dash.dependencies.Input("facebook-d2-brand-input", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Limit, Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        dff2 = dff2[['Brand', 'Month','Positive Count', 'Neutral Count', 'Negative Count']]
        dff2['Neutral Percentage'] = (dff2['Neutral Count']/(dff2['Positive Count']+dff2['Neutral Count']+dff2['Negative Count']))*100
        dff2['Negative Percentage'] = (dff2['Negative Count']/(dff2['Positive Count']+dff2['Neutral Count']+dff2['Negative Count']))*100
        dff2['Positive Percentage'] = (dff2['Positive Count']/(dff2['Positive Count']+dff2['Neutral Count']+dff2['Negative Count']))*100
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in dff2.columns[-3:]])
            fig.update_layout(title="Sentiment Proportion Top {} in All Year".format(Selected_Limit),barmode='stack',
                              xaxis_title="Brand",yaxis_title="Percentage")
            return fig
    
        dff2 = dff2[dff2['Month'] == Selected_Month]
        fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in dff2.columns[-3:]])
        fig.update_layout(title="Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month),barmode='stack',
                         xaxis_title="Brand",yaxis_title="Percentage")
        return fig

    dff = dff[['Brand', 'Month','Positive Count', 'Neutral Count', 'Negative Count']]
    dff['Neutral Percentage'] = (dff['Neutral Count']/(dff['Positive Count']+dff['Neutral Count']+dff['Negative Count']))*100
    dff['Negative Percentage'] = (dff['Negative Count']/(dff['Positive Count']+dff['Neutral Count']+dff['Negative Count']))*100
    dff['Positive Percentage'] = (dff['Positive Count']/(dff['Positive Count']+dff['Neutral Count']+dff['Negative Count']))*100
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in dff.columns[-3:]])
        fig.update_layout(title="Sentiment Proportion Top {} in All Year".format(Selected_Limit),barmode='stack',
                         xaxis_title="Brand",yaxis_title="Percentage")
        return fig
    
    dff = dff[dff['Month'] == Selected_Month]
    fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in dff.columns[-3:]])
    fig.update_layout(title="Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month),barmode='stack',
                     xaxis_title="Brand",yaxis_title="Percentage")
    return fig

@app.callback(
    dash.dependencies.Output('Relationship-graph-d3-facebook', 'figure'),
    [dash.dependencies.Input("Y-Axis-dropdown-d3-facebook", "value"),
    dash.dependencies.Input("X-Axis-dropdown-d3-facebook", "value"),
    dash.dependencies.Input("month-slider-d4-facebook", "value"),
    dash.dependencies.Input("facebook-limit-d3", "value")]
)
def update_figure(Selected_Y, Selected_X, Selected_Month,Selected_Limit):
    dff = facebook_df.copy()
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Category").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Category'].isin(limit)]
    dff.reset_index(inplace = True)
    
    if Selected_Month == 0:
        dff = dff.groupby(["Brand","Category"],as_index=False).mean()
        fig = px.scatter(dff, x = Selected_X, y= Selected_Y,color = "Category",hover_name="Brand",
                         title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig
    
    dff = dff[dff['Month'] == Selected_Month]
    fig = px.scatter(dff, x = Selected_X, y= Selected_Y,color = "Category",hover_name="Brand",
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X, Selected_Month))
    return fig

@app.callback(
    dash.dependencies.Output('Relationship-graph2-d3-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-facebook", "value"),
     dash.dependencies.Input("month-slider-d3-facebook", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d4-facebook", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d4-facebook", "value"),
     dash.dependencies.Input("size-dropdown-d3-facebook", "value"),
     dash.dependencies.Input("facebook-limit-d4", "value"),
     dash.dependencies.Input("facebook-d3-brand-input", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Y, Selected_X, Selected_Size,Selected_Limit,Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby("Brand",as_index=False).mean()
            fig = px.scatter(dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
            return fig

        dff2 = dff2[dff2['Month'] == Selected_Month] 
        fig = px.scatter(dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
        return fig
    
    if Selected_Month == 0:
        dff = dff.groupby("Brand",as_index=False).mean()
        fig = px.scatter(dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    dff = dff[dff['Month'] == Selected_Month] 
    fig = px.scatter(dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig

@app.callback(
    dash.dependencies.Output('RawData-graph-d3-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-facebook", "value"),
     dash.dependencies.Input("month-slider-d3-facebook", "value"),
     dash.dependencies.Input("Data-dropdown-d3-facebook", "value"),
     dash.dependencies.Input("facebook-limit-d4", "value"),
     dash.dependencies.Input("facebook-d3-brand-input", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Data,Selected_Limit,Selected_Brands):
    merged_df = pd.merge(facebook_df, zocial_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    brand_df = zocial_df[zocial_df['Month'] == 1]
    dff = pd.merge(dff, brand_df[['Brand', 'Facebook ID (Edited)']], how='left', left_on="Account ID", right_on="Facebook ID (Edited)")
    sum_dff = dff.groupby(by="Brand").mean()
    limit_df = sum_dff.sort_values(by=['Facebook Score'],ascending=False).head(Selected_Limit)
    limit = list(limit_df.index)
    dff = dff[dff['Brand'].isin(limit)]
    
    if Selected_Brands != '':
        Selected_Brands = Selected_Brands.lower()
        brands = Selected_Brands.split(', ')
        merged_df['Lower Brand'] = merged_df['Brand'].str.lower()
        additional_df = merged_df[merged_df['Lower Brand'].isin(brands)]
        dff2 = dff.append(additional_df, ignore_index=True)            
        dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            dff2 = dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in Selected_Data])
            fig.update_layout(title="Facebook Data All Year", xaxis={'categoryorder':'total descending'})
            return fig
        
        dff2 = dff2[dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=dff2["Brand"], y=dff2[c]) for c in Selected_Data])
        fig.update_layout(title="Facebook Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    if Selected_Month == 0:
        dff = dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in Selected_Data])
        fig.update_layout(title="Facebook Data All Year", xaxis={'categoryorder':'total descending'})
        return fig
                        
    dff = dff[dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=dff["Brand"], y=dff[c]) for c in Selected_Data])
    fig.update_layout(title="Facebook Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig

@app.callback(
    dash.dependencies.Output('Heatmap-d2-facebook', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d4-facebook", "value")]
)
def update_figure(Selected_Category):
    if Selected_Category == 'Overall':
        dff = facebook_df.drop([c for c in facebook_df.columns if c not in variable_list_facebook], axis = 1)
        fig = px.imshow(dff.corr(),
                       labels=dict(color="Correlation Coefficient"),
                       x = [c for c in dff.columns],
                       y = [c for c in dff.columns])
        fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
        return fig
    dff = facebook_df[facebook_df['Category'] == Selected_Category]
    dff.drop([c for c in dff.columns if c not in variable_list_facebook], axis = 1,inplace=True)
    fig = px.imshow(dff.corr(),
                    labels=dict(color="Correlation Coefficient"),
                    x = [c for c in dff.columns],
                    y = [c for c in dff.columns])
    fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
    return fig

## Call back Twitter D1 ##

#Graph 1-1 Line
@app.callback(
    dash.dependencies.Output('LineGraph-d1-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-twitter", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d1", "value"),
    dash.dependencies.Input("twitter-brand-d1", "value")]
)
def update_figure(Selected_Category,Selected_Metric,Selected_Limit, Selected_Brands):
        twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
        sum_twitter_dff = twitter_dff.groupby("Brand").mean()
        limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_twitter = list(limit_twitter_df.index)
        twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
            additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
            twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
            twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
            fig = px.line(twitter_dff2, x = "Month", color = "Brand",y= Selected_Metric,
                            title="Twitter {} Top {} by Month".format(Selected_Metric,Selected_Limit))
            return fig
        
        fig = px.line(
        twitter_dff, x = "Month", y=Selected_Metric,color = "Brand",
        title="Twitter {} Top {} by Month".format(Selected_Metric,Selected_Limit)
        )
        return fig
    
#Graph 1-2 Score
@app.callback(
    dash.dependencies.Output('ScoreGraph-d1-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-twitter", "value"),
    dash.dependencies.Input("month-slider-d1-twitter", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d1", "value"),
    dash.dependencies.Input("twitter-brand-d1", "value")])


def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):
    twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
    sum_twitter_dff = twitter_dff.groupby("Brand").mean()
    limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter = list(limit_twitter_df.index)
    twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
    twitter_dff.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
        additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
        twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
        twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            twitter_dff2 = twitter_dff2.groupby("Brand",as_index=False).mean()
            twitter_dff2 = twitter_dff2.astype({'Score':int,'Follower Growth Metric':int,'Favorite Metric':int,'Retweet Metric':int,'Retweet/Follower Metric':int,'Reply/Tweet Metric':int,'Reply to Other Metric':int,'Reply Time Metric':int,'Sentiment on Comments':int})
            fig = px.bar(twitter_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Twitter {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
            fig.update_layout(showlegend=False)
            return fig
    
        twitter_dff2 = twitter_dff2[twitter_dff2['Month'] == Selected_Month]
        fig = px.bar(twitter_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
          title = "Twitter {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    if Selected_Month == 0:
        twitter_dff = twitter_dff.groupby("Brand",as_index=False).mean()
        twitter_dff = twitter_dff.astype({'Score':int,'Follower Growth Metric':int,'Favorite Metric':int,'Retweet Metric':int,'Retweet/Follower Metric':int,'Reply/Tweet Metric':int,'Reply to Other Metric':int,'Reply Time Metric':int,'Sentiment on Comments':int})
        fig = px.bar(twitter_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Twitter {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    twitter_dff = twitter_dff[twitter_dff['Month'] == Selected_Month]
    fig = px.bar(twitter_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
    title = "Twitter {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    return fig

#Graph 1-3 Grouped

@app.callback(
    dash.dependencies.Output('Grouped-BarGraph-d1-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-twitter", "value"),
    dash.dependencies.Input("month-slider-d1-twitter", "value"),
    dash.dependencies.Input("metric-checklist-d1-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d1", "value"),
    dash.dependencies.Input("twitter-brand-d1", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):

    twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
    sum_twitter_dff = twitter_dff.groupby("Brand").mean()
    limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter = list(limit_twitter_df.index)
    twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
    twitter_dff.reset_index(inplace = True)  
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
        additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
        twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
        twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            twitter_dff2 = twitter_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff2["Brand"], y=twitter_dff2[c]) for c in Selected_Metric])
            fig.update_layout(title="Twitter Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
            return fig
                        
        twitter_dff2 = twitter_dff2[twitter_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff2["Brand"], y=twitter_dff2[c]) for c in Selected_Metric])
        fig.update_layout(title="Twitter Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    if Selected_Month == 0:
        twitter_dff = twitter_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff["Brand"], y=twitter_dff[c]) for c in Selected_Metric])
        fig.update_layout(title="Twitter Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
        return fig
                        
    twitter_dff = twitter_dff[twitter_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff["Brand"], y=twitter_dff[c]) for c in Selected_Metric])
    fig.update_layout(title="Twitter Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig


## Call back Twitter D2 ##

@app.callback(dash.dependencies.Output('FollowerGraph-d2-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d2", "value"),
    dash.dependencies.Input("twitter-brand-d2", "value")])
              
def update_figure(Selected_Category,Selected_Limit,Selected_Brands):
        twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
        sum_twitter_dff = twitter_dff.groupby("Brand").mean()
        limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_twitter = list(limit_twitter_df.index)
        twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
            additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
            twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
            twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
            
            fig = px.line(twitter_dff2, x = "Month", color = "Brand",y= "Follower Count",
            title="Twitter Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
            return fig

        
        fig = px.line(twitter_dff, x = "Month", color = "Brand",y= "Follower Count",
        title="Twitter Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
        return fig



#Graph 2-3 Sentiment

@app.callback(
    dash.dependencies.Output('SentimentGraph-d2-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-twitter", "value"),
    dash.dependencies.Input("month-slider-d2-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d2", "value"),
    dash.dependencies.Input("twitter-brand-d2", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Limit,Selected_Brands):
    twitter_dff_sentiment = twitter_df_sentiment[twitter_df_sentiment['Category'] == Selected_Category]
    sum_twitter_dff_sentiment = twitter_dff_sentiment.groupby("Brand").mean()
    limit_twitter_df_sentiment = sum_twitter_dff_sentiment.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter_df_sentiment = list(limit_twitter_df_sentiment.index)
    twitter_dff_sentiment = twitter_dff_sentiment[twitter_dff_sentiment['Brand'].isin(limit_twitter_df_sentiment)]
    twitter_dff_sentiment.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        twitter_df_sentiment['Lower Brand'] = twitter_df_sentiment['Brand'].str.lower()
        additional_twitter_df_sentiment = twitter_df_sentiment[twitter_df_sentiment['Lower Brand'].isin(brands)]
        twitter_dff2_sentiment = twitter_dff_sentiment.append(additional_twitter_df_sentiment, ignore_index=True)            
        twitter_dff2_sentiment.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            twitter_dff2_sentiment = twitter_dff2_sentiment.groupby("Brand",as_index=False).mean()
            fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=twitter_dff2_sentiment["%Neutral Count"], x=twitter_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=twitter_dff2_sentiment["%Negative Count"], x=twitter_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=twitter_dff2_sentiment["%Positive Count"], x=twitter_dff2_sentiment["Brand"])
            ])
            fig.update_layout(barmode="stack",title="Twitter Sentiment Proportion Top {} in All Year".format(Selected_Limit))
            return fig    
        twitter_dff2_sentiment = twitter_dff2_sentiment[twitter_dff2_sentiment['Month'] == Selected_Month]
        twitter_dff2_sentiment = twitter_dff2_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=twitter_dff2_sentiment["%Neutral Count"], x=twitter_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=twitter_dff2_sentiment["%Negative Count"], x=twitter_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=twitter_dff2_sentiment["%Positive Count"], x=twitter_dff2_sentiment["Brand"])
            ])
        fig.update_layout(barmode="stack",title="Twitter Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
        return fig
    
    
    if Selected_Month == 0:
        twitter_dff_sentiment = twitter_dff_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=twitter_dff_sentiment["%Neutral Count"], x=twitter_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=twitter_dff_sentiment["%Negative Count"], x=twitter_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=twitter_dff_sentiment["%Positive Count"], x=twitter_dff_sentiment["Brand"])
        ])
        fig.update_layout(barmode="stack",title="Twitter Sentiment Proportion Top {} in All Year".format(Selected_Limit))
        return fig    
    twitter_dff_sentiment = twitter_dff_sentiment[twitter_dff_sentiment['Month'] == Selected_Month]
    twitter_dff_sentiment = twitter_dff_sentiment.groupby("Brand",as_index=False).mean()
    fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=twitter_dff_sentiment["%Neutral Count"], x=twitter_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=twitter_dff_sentiment["%Negative Count"], x=twitter_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=twitter_dff_sentiment["%Positive Count"], x=twitter_dff_sentiment["Brand"])
        ])
    fig.update_layout(barmode="stack",title="Twitter Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
    return fig

#Graph 3-1 Relationship analysis
@app.callback(
    dash.dependencies.Output('Relationship-graph1-d3-twitter', 'figure'),
    [dash.dependencies.Input("month-slider-d3-twitter", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-twitter", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-twitter", "value"),
     dash.dependencies.Input("twitter-limit-d3", "value")]
)
def update_figure(Selected_Month,Selected_Y, Selected_X, Selected_Limit):
    twitter_dff = twitter_df.copy()
    sum_twitter_dff = twitter_dff.groupby("Category").mean()
    limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter = list(limit_twitter_df.index)
    twitter_dff = twitter_df[twitter_df['Category'].isin(limit_twitter)]
    twitter_dff.reset_index(inplace = True)
    
    if Selected_Month == 0:
        twitter_dff = twitter_dff.groupby(["Brand","Category"],as_index=False).mean()
        fig = px.scatter(twitter_dff, x = Selected_X, y= Selected_Y,color = "Category",hover_name="Brand",
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    twitter_dff = twitter_dff[twitter_dff['Month'] == Selected_Month] 
    fig = px.scatter(twitter_dff, x = Selected_X, y= Selected_Y, color = "Category",hover_name="Brand",
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-2 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph2-d3-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-twitter", "value"),
     dash.dependencies.Input("month-slider-d3-2-twitter", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-2-twitter", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-2-twitter", "value"),
     dash.dependencies.Input("Size-dropdown-d3-twitter", "value"),
     dash.dependencies.Input("twitter-limit-d3-2", "value"),
     dash.dependencies.Input("twitter-brand-d3", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Y, Selected_X, Selected_Size,Selected_Limit,Selected_Brands):
    twitter_dff = twitter_df.copy()
    twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
    sum_twitter_dff = twitter_dff.groupby("Brand").mean()
    limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter = list(limit_twitter_df.index)
    twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
        additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
        twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
        twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            twitter_dff2 = twitter_dff2.groupby("Brand",as_index=False).mean()
            fig = px.scatter(twitter_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
            return fig

        twitter_dff2 = twitter_dff2[twitter_dff2['Month'] == Selected_Month] 
        fig = px.scatter(twitter_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
        return fig
    
    if Selected_Month == 0:
        twitter_dff = twitter_dff.groupby("Brand",as_index=False).mean()
        fig = px.scatter(twitter_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    twitter_dff = twitter_dff[twitter_dff['Month'] == Selected_Month] 
    fig = px.scatter(twitter_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-3 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph3-d3-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-twitter", "value"),
    dash.dependencies.Input("month-slider-d3-2-twitter", "value"),
    dash.dependencies.Input("Data-dropdown-d3-twitter", "value"),
    dash.dependencies.Input("twitter-limit-d3-2", "value"),
    dash.dependencies.Input("twitter-brand-d3", "value")])


def update_figure(Selected_Category, Selected_Month, Selected_Data, Selected_Limit, Selected_Brands):

    twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
    sum_twitter_dff = twitter_dff.groupby("Brand").mean()
    limit_twitter_df = sum_twitter_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_twitter = list(limit_twitter_df.index)
    twitter_dff = twitter_df[twitter_df['Brand'].isin(limit_twitter)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        twitter_df['Lower Brand'] = twitter_df['Brand'].str.lower()
        additional_twitter_df = twitter_df[twitter_df['Lower Brand'].isin(brands)]
        twitter_dff2 = twitter_dff.append(additional_twitter_df, ignore_index=True)            
        twitter_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            twitter_dff2 = twitter_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff2["Brand"], y=twitter_dff2[c]) for c in Selected_Data])
            fig.update_layout(title="Twitter Data All Year", xaxis={'categoryorder':'total descending'})
            return fig
                        
        twitter_dff2 = twitter_dff2[twitter_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff2["Brand"], y=twitter_dff2[c]) for c in Selected_Data])
        fig.update_layout(title="Twitter Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    
    if Selected_Month == 0:
        twitter_dff = twitter_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff["Brand"], y=twitter_dff[c]) for c in Selected_Data])
        fig.update_layout(title="Twitter Data All Year", xaxis={'categoryorder':'total descending'})
        return fig
                        
    twitter_dff = twitter_dff[twitter_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=twitter_dff["Brand"], y=twitter_dff[c]) for c in Selected_Data])
    fig.update_layout(title="Twitter Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig


#Graph 3-4 Relationship analysis Heatmap

@app.callback(
    dash.dependencies.Output('Heatmap-d4-twitter', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d4-twitter", "value")]
)
def update_figure(Selected_Category):
    if Selected_Category == 'Overall':
        twitter_dff = twitter_df.drop([c for c in twitter_df.columns if c not in variable_list_twitter], axis = 1)
        fig = px.imshow(twitter_dff.corr().fillna(0),
                       labels=dict(color="Correlation Coefficient"),
                       x = [c for c in twitter_dff.columns],
                       y = [c for c in twitter_dff.columns])
        fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
        return fig
    twitter_dff = twitter_df[twitter_df['Category'] == Selected_Category]
    twitter_dff.drop([c for c in twitter_dff.columns if c not in variable_list_twitter], axis = 1,inplace=True)
    fig = px.imshow(twitter_dff.corr().fillna(0),
                    labels=dict(color="Correlation Coefficient"),
                    x = [c for c in twitter_dff.columns],
                    y = [c for c in twitter_dff.columns])
    fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
    return fig

################################ Callback Instagram Dash 1 ####################################

@app.callback(
    dash.dependencies.Output('LineGraph-d1-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-instagram", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d1", "value"),
    dash.dependencies.Input("instagram-brand-d1", "value")]
)
def update_figure(Selected_Category,Selected_Metric,Selected_Limit, Selected_Brands):
        instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
        sum_instagram_dff = instagram_dff.groupby("Brand").mean()
        limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_instagram = list(limit_instagram_df.index)
        instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
            additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
            instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)            
            instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
            fig = px.line(instagram_dff2, x = "Month", color = "Brand",y= Selected_Metric,
                            title="Instagram {} Top {} by Month".format(Selected_Metric,Selected_Limit))
            return fig
        
        fig = px.line(
        instagram_dff, x = "Month", y=Selected_Metric,color = "Brand",
        title="Instagram {} Top {} by Month".format(Selected_Metric,Selected_Limit)
        )
        return fig

@app.callback(
    dash.dependencies.Output('ScoreGraph-d1-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-instagram", "value"),
    dash.dependencies.Input("month-slider-d1-instagram", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d1", "value"),
    dash.dependencies.Input("instagram-brand-d1", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):
    instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
    sum_instagram_dff = instagram_dff.groupby("Brand").mean()
    limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram = list(limit_instagram_df.index)
    instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
    instagram_dff.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
        additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
        instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)            
        instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            instagram_dff2 = instagram_dff2.groupby("Brand",as_index=False).mean()
            instagram_dff2 = instagram_dff2.astype({'Score':int,'Follower Growth Metric':int,'Sentiment on Comments':int,'Avg Like Metric':int,'Avg Comment Metric':int,'View and Video Metric':int})
            fig = px.bar(instagram_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Instagram {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
            fig.update_layout(showlegend=False)
            return fig
    
        instagram_dff2 = instagram_dff2[instagram_dff2['Month'] == Selected_Month]
        fig = px.bar(instagram_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
          title = "Instagram {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    if Selected_Month == 0:
        instagram_dff = instagram_dff.groupby("Brand",as_index=False).mean()
        instagram_dff = instagram_dff.astype({'Score':int,'Follower Growth Metric':int,'Sentiment on Comments':int,'Avg Like Metric':int,'Avg Comment Metric':int,'View and Video Metric':int})
        fig = px.bar(instagram_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Instagram {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    instagram_dff = instagram_dff[instagram_dff['Month'] == Selected_Month]
    fig = px.bar(instagram_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
    title = "Instagram {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    dash.dependencies.Output('Grouped-BarGraph-d1-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-instagram", "value"),
    dash.dependencies.Input("month-slider-d1-instagram", "value"),
    dash.dependencies.Input("metric-checklist-d1-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d1", "value"),
    dash.dependencies.Input("instagram-brand-d1", "value")]
)
def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):

    instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
    sum_instagram_dff = instagram_dff.groupby("Brand").mean()
    limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram = list(limit_instagram_df.index)
    instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
    instagram_dff.reset_index(inplace = True)  
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
        additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
        instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)            
        instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            instagram_dff2 = instagram_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff2["Brand"], y=instagram_dff2[c]) for c in Selected_Metric])
            fig.update_layout(title="Instagram Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
            return fig
                        
        instagram_dff2 = instagram_dff2[instagram_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff2["Brand"], y=instagram_dff2[c]) for c in Selected_Metric])
        fig.update_layout(title="Instagram Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    if Selected_Month == 0:
        instagram_dff = instagram_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff["Brand"], y=instagram_dff[c]) for c in Selected_Metric])
        fig.update_layout(title="Instagram Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
        return fig
                        
    instagram_dff = instagram_dff[instagram_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff["Brand"], y=instagram_dff[c]) for c in Selected_Metric])
    fig.update_layout(title="Instagram Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig

#############Call Back Instagram Dash 2###########

@app.callback(
    dash.dependencies.Output('FollowerGraph-d2-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d2", "value"),
    dash.dependencies.Input("instagram-brand-d2", "value")]
)
def update_figure(Selected_Category,Selected_Limit,Selected_Brands):
        instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
        sum_instagram_dff = instagram_dff.groupby("Brand").mean()
        limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_instagram = list(limit_instagram_df.index)
        instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
            additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
            instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)            
            instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
            
            fig = px.line(instagram_dff2, x = "Month", color = "Brand",y= "Follower Count",
            title="Instagram Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
            return fig

        
        fig = px.line(instagram_dff, x = "Month", color = "Brand",y= "Follower Count",
        title="Instagram Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
        return fig



@app.callback(
    dash.dependencies.Output('SentimentGraph-d2-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-instagram", "value"),
    dash.dependencies.Input("month-slider-d2-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d2", "value"),
    dash.dependencies.Input("instagram-brand-d2", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Limit,Selected_Brands):
    instagram_dff_sentiment = instagram_df_sentiment[instagram_df_sentiment['Category'] == Selected_Category]
    sum_instagram_dff_sentiment = instagram_dff_sentiment.groupby("Brand").mean()
    limit_instagram_df_sentiment = sum_instagram_dff_sentiment.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram_df_sentiment = list(limit_instagram_df_sentiment.index)
    instagram_dff_sentiment = instagram_dff_sentiment[instagram_dff_sentiment['Brand'].isin(limit_instagram_df_sentiment)]
    instagram_dff_sentiment.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        instagram_df_sentiment['Lower Brand'] = instagram_df_sentiment['Brand'].str.lower()
        additional_instagram_df_sentiment = instagram_df_sentiment[instagram_df_sentiment['Lower Brand'].isin(brands)]
        instagram_dff2_sentiment = instagram_dff_sentiment.append(additional_instagram_df_sentiment, ignore_index=True)            
        instagram_dff2_sentiment.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            instagram_dff2_sentiment = instagram_dff2_sentiment.groupby("Brand",as_index=False).mean()
            fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=instagram_dff2_sentiment["%Neutral Count"], x=instagram_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=instagram_dff2_sentiment["%Negative Count"], x=instagram_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=instagram_dff2_sentiment["%Positive Count"], x=instagram_dff2_sentiment["Brand"])
            ])
            fig.update_layout(barmode="stack",title="Instagram Sentiment Proportion Top {} in All Year".format(Selected_Limit))
            return fig    
        instagram_dff2_sentiment = instagram_dff2_sentiment[instagram_dff2_sentiment['Month'] == Selected_Month]
        instagram_dff2_sentiment = instagram_dff2_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=instagram_dff2_sentiment["%Neutral Count"], x=instagram_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=instagram_dff2_sentiment["%Negative Count"], x=instagram_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=instagram_dff2_sentiment["%Positive Count"], x=instagram_dff2_sentiment["Brand"])
            ])
        fig.update_layout(barmode="stack",title="Instagram Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
        return fig
    
    
    if Selected_Month == 0:
        instagram_dff_sentiment = instagram_dff_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=instagram_dff_sentiment["%Neutral Count"], x=instagram_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=instagram_dff_sentiment["%Negative Count"], x=instagram_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=instagram_dff_sentiment["%Positive Count"], x=instagram_dff_sentiment["Brand"])
        ])
        fig.update_layout(barmode="stack",title="Instagram Sentiment Proportion Top {} in All Year".format(Selected_Limit))
        return fig    
    instagram_dff_sentiment = instagram_dff_sentiment[instagram_dff_sentiment['Month'] == Selected_Month]
    instagram_dff_sentiment = instagram_dff_sentiment.groupby("Brand",as_index=False).mean()
    fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=instagram_dff_sentiment["%Neutral Count"], x=instagram_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=instagram_dff_sentiment["%Negative Count"], x=instagram_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=instagram_dff_sentiment["%Positive Count"], x=instagram_dff_sentiment["Brand"])
        ])
    fig.update_layout(barmode="stack",title="Instagram Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
    return fig

#Instagram Graph 3-1 Relationship analysis
@app.callback(
    dash.dependencies.Output('Relationship-graph1-d3-instagram', 'figure'),
    [dash.dependencies.Input("month-slider-d3-instagram", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-instagram", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-instagram", "value"),
     dash.dependencies.Input("instagram-limit-d3", "value")]
)
def update_figure(Selected_Month,Selected_Y, Selected_X, Selected_Limit):
    instagram_dff = instagram_df.copy()
    sum_instagram_dff = instagram_dff.groupby("Category").mean()
    limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram = list(limit_instagram_df.index)
    instagram_dff = instagram_df[instagram_df['Category'].isin(limit_instagram)]
    instagram_dff.reset_index(inplace = True)
    
    if Selected_Month == 0:
        instagram_dff = instagram_dff.groupby(["Brand","Category"],as_index=False).mean()
        fig = px.scatter(instagram_dff, x = Selected_X, y= Selected_Y,color = "Category",hover_name="Brand",
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    instagram_dff = instagram_dff[instagram_dff['Month'] == Selected_Month] 
    fig = px.scatter(instagram_dff, x = Selected_X, y= Selected_Y, color = "Category",hover_name="Brand",
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-2 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph2-d3-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-instagram", "value"),
     dash.dependencies.Input("month-slider-d3-2-instagram", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-2-instagram", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-2-instagram", "value"),
     dash.dependencies.Input("Size-dropdown-d3-instagram", "value"),
     dash.dependencies.Input("instagram-limit-d3-2", "value"),
     dash.dependencies.Input("instagram-brand-d3", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Y, Selected_X, Selected_Size,Selected_Limit,Selected_Brands):
    instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
    sum_instagram_dff = instagram_dff.groupby("Brand").mean()
    limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram = list(limit_instagram_df.index)
    instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
        additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
        instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)            
        instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            instagram_dff2 = instagram_dff2.groupby("Brand",as_index=False).mean()
            fig = px.scatter(instagram_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
            return fig

        instagram_dff2 = instagram_dff2[instagram_dff2['Month'] == Selected_Month] 
        fig = px.scatter(instagram_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
        return fig
    
    if Selected_Month == 0:
        instagram_dff = instagram_dff.groupby("Brand",as_index=False).mean()
        fig = px.scatter(instagram_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    instagram_dff = instagram_dff[instagram_dff['Month'] == Selected_Month] 
    fig = px.scatter(instagram_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-3 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph3-d3-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-instagram", "value"),
    dash.dependencies.Input("month-slider-d3-2-instagram", "value"),
    dash.dependencies.Input("Data-dropdown-d3-instagram", "value"),
    dash.dependencies.Input("instagram-limit-d3-2", "value"),
    dash.dependencies.Input("instagram-brand-d3", "value")])


def update_figure(Selected_Category, Selected_Month, Selected_Data, Selected_Limit, Selected_Brands):
    instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
    sum_instagram_dff = instagram_dff.groupby("Brand").mean()
    limit_instagram_df = sum_instagram_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_instagram = list(limit_instagram_df.index)
    instagram_dff = instagram_df[instagram_df['Brand'].isin(limit_instagram)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        instagram_df['Lower Brand'] = instagram_df['Brand'].str.lower()
        additional_instagram_df = instagram_df[instagram_df['Lower Brand'].isin(brands)]
        instagram_dff2 = instagram_dff.append(additional_instagram_df, ignore_index=True)
        instagram_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            instagram_dff2 = instagram_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff2["Brand"], y=instagram_dff2[c]) for c in Selected_Data])
            fig.update_layout(title="Instagram Data All Year", xaxis={'categoryorder':'total descending'})
            return fig
                        
        instagram_dff2 = instagram_dff2[instagram_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff2["Brand"], y=instagram_dff2[c]) for c in Selected_Data])
        fig.update_layout(title="Instagram Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    
    if Selected_Month == 0:
        instagram_dff = instagram_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff["Brand"], y=instagram_dff[c]) for c in Selected_Data])
        fig.update_layout(title="Instagram Data All Year", xaxis={'categoryorder':'total descending'})
        return fig
                        
    instagram_dff = instagram_dff[instagram_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=instagram_dff["Brand"], y=instagram_dff[c]) for c in Selected_Data])
    fig.update_layout(title="Instagram Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig


#Instagram Graph 3-4 Relationship analysis Heatmap

@app.callback(
    dash.dependencies.Output('Heatmap-d4-instagram', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d4-instagram", "value")]
)
def update_figure(Selected_Category):
    if Selected_Category == 'Overall':
        instagram_dff = instagram_df.drop([c for c in instagram_df.columns if c not in variable_list_instagram], axis = 1)
        fig = px.imshow(instagram_dff.corr(),
                       labels=dict(color="Correlation Coefficient"),
                       x = [c for c in instagram_dff.columns],
                       y = [c for c in instagram_dff.columns])
        fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
        return fig
    instagram_dff = instagram_df[instagram_df['Category'] == Selected_Category]
    instagram_dff.drop([c for c in instagram_dff.columns if c not in variable_list_instagram], axis = 1,inplace=True)
    fig = px.imshow(instagram_dff.corr(),
                    labels=dict(color="Correlation Coefficient"),
                    x = [c for c in instagram_dff.columns],
                    y = [c for c in instagram_dff.columns])
    fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
    return fig

################# Callback Youtube Dash 1###################

@app.callback(
    dash.dependencies.Output('LineGraph-d1-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-youtube", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d1", "value"),
    dash.dependencies.Input("youtube-brand-d1", "value")]
)
def update_figure(Selected_Category,Selected_Metric,Selected_Limit, Selected_Brands):
        youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
        sum_youtube_dff = youtube_dff.groupby("Brand").mean()
        limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_youtube = list(limit_youtube_df.index)
        youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
            additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
            youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
            youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
            fig = px.line(youtube_dff2, x = "Month", color = "Brand",y= Selected_Metric,
                            title="Youtube {} Top {} by Month".format(Selected_Metric,Selected_Limit))
            return fig
        
        fig = px.line(
        youtube_dff, x = "Month", y=Selected_Metric,color = "Brand",
        title="Youtube {} Top {} by Month".format(Selected_Metric,Selected_Limit)
        )
        return fig

@app.callback(
    dash.dependencies.Output('ScoreGraph-d1-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-youtube", "value"),
    dash.dependencies.Input("month-slider-d1-youtube", "value"),
    dash.dependencies.Input("ScoreAndMetric-dropdown-d1-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d1", "value"),
    dash.dependencies.Input("youtube-brand-d1", "value")]
)

def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):
    youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
    sum_youtube_dff = youtube_dff.groupby("Brand").mean()
    limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube = list(limit_youtube_df.index)
    youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
    youtube_dff.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
        additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
        youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
        youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            youtube_dff2 = youtube_dff2.groupby("Brand",as_index=False).mean()
            youtube_dff2 = youtube_dff2.astype({'Score':int,'Subscribers Growth Metric':int,'Sentiment on Comments':int,'Like Views Metric':int,'Comment Views Metric':int,'Like Dislikes Views Metric':int,'Views Metric':int})
            fig = px.bar(youtube_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Youtube {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
            fig.update_layout(showlegend=False)
            return fig
    
        youtube_dff2 = youtube_dff2[youtube_dff2['Month'] == Selected_Month]
        fig = px.bar(youtube_dff2, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
          title = "Youtube {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    if Selected_Month == 0:
        youtube_dff = youtube_dff.groupby("Brand",as_index=False).mean()
        youtube_dff = youtube_dff.astype({'Score':int,'Subscribers Growth Metric':int,'Sentiment on Comments':int,'Like Views Metric':int,'Comment Views Metric':int,'Like Dislikes Views Metric':int,'Views Metric':int})
        fig = px.bar(youtube_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
                  title = "Youtube {} Top {} All Year".format(Selected_Metric,Selected_Limit)
                ).update_xaxes(categoryorder="total descending")
        fig.update_layout(showlegend=False)
        return fig
    
    youtube_dff = youtube_dff[youtube_dff['Month'] == Selected_Month]
    fig = px.bar(youtube_dff, x = "Brand", y=Selected_Metric,color = "Brand",text=Selected_Metric,
    title = "Youtube {} Top {} in Month {} ".format(Selected_Metric,Selected_Limit,Selected_Month) 
            ).update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    return fig


@app.callback(
    dash.dependencies.Output('Grouped-BarGraph-d1-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d1-youtube", "value"),
    dash.dependencies.Input("month-slider-d1-youtube", "value"),
    dash.dependencies.Input("metric-checklist-d1-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d1", "value"),
    dash.dependencies.Input("youtube-brand-d1", "value")]
)

def update_figure(Selected_Category, Selected_Month, Selected_Metric, Selected_Limit, Selected_Brands):

    youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
    sum_youtube_dff = youtube_dff.groupby("Brand").mean()
    limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube = list(limit_youtube_df.index)
    youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
    youtube_dff.reset_index(inplace = True)  
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
        additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
        youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
        youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
    
        if Selected_Month == 0:
            youtube_dff2 = youtube_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff2["Brand"], y=youtube_dff2[c]) for c in Selected_Metric])
            fig.update_layout(title="Youtube Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
            return fig
                        
        youtube_dff2 = youtube_dff2[youtube_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff2["Brand"], y=youtube_dff2[c]) for c in Selected_Metric])
        fig.update_layout(title="Youtube Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    if Selected_Month == 0:
        youtube_dff = youtube_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff["Brand"], y=youtube_dff[c]) for c in Selected_Metric])
        fig.update_layout(title="Youtube Score and Metric Top {} All Year".format(Selected_Limit), xaxis={'categoryorder':'total descending'})
        return fig
                        
    youtube_dff = youtube_dff[youtube_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff["Brand"], y=youtube_dff[c]) for c in Selected_Metric])
    fig.update_layout(title="Youtube Score and Metric Top {} in Month {}".format(Selected_Limit,Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig

################## Call Back Youtube Dash 2 #######################

@app.callback(
    dash.dependencies.Output('FollowerGraph-d2-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d2", "value"),
    dash.dependencies.Input("youtube-brand-d2", "value")]
)
def update_figure(Selected_Category,Selected_Limit,Selected_Brands):
        youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
        sum_youtube_dff = youtube_dff.groupby("Brand").mean()
        limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
        limit_youtube = list(limit_youtube_df.index)
        youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
        
        if Selected_Brands != '':
            brands = Selected_Brands.lower().split(', ')
            youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
            additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
            youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
            youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
            
            fig = px.line(youtube_dff2, x = "Month", color = "Brand",y= "Subscriber Count",
            title="Youtube Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
            return fig

        
        fig = px.line(youtube_dff, x = "Month", color = "Brand",y= "Subscriber Count",
        title="Youtube Follower {} Top {} in 1 Year".format(Selected_Category,Selected_Limit))
        return fig


@app.callback(
    dash.dependencies.Output('SentimentGraph-d2-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d2-youtube", "value"),
    dash.dependencies.Input("month-slider-d2-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d2", "value"),
    dash.dependencies.Input("youtube-brand-d2", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Limit,Selected_Brands):
    youtube_dff_sentiment = youtube_df_sentiment[youtube_df_sentiment['Category'] == Selected_Category]
    sum_youtube_dff_sentiment = youtube_dff_sentiment.groupby("Brand").mean()
    limit_youtube_df_sentiment = sum_youtube_dff_sentiment.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube_df_sentiment = list(limit_youtube_df_sentiment.index)
    youtube_dff_sentiment = youtube_dff_sentiment[youtube_dff_sentiment['Brand'].isin(limit_youtube_df_sentiment)]
    youtube_dff_sentiment.reset_index(inplace = True)
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        youtube_df_sentiment['Lower Brand'] = youtube_df_sentiment['Brand'].str.lower()
        additional_youtube_df_sentiment = youtube_df_sentiment[youtube_df_sentiment['Lower Brand'].isin(brands)]
        youtube_dff2_sentiment = youtube_dff_sentiment.append(additional_youtube_df_sentiment, ignore_index=True)            
        youtube_dff2_sentiment.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            youtube_dff2_sentiment = youtube_dff2_sentiment.groupby("Brand",as_index=False).mean()
            fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=youtube_dff2_sentiment["%Neutral Count"], x=youtube_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=youtube_dff2_sentiment["%Negative Count"], x=youtube_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=youtube_dff2_sentiment["%Positive Count"], x=youtube_dff2_sentiment["Brand"])
            ])
            fig.update_layout(barmode="stack",title="Youtube Sentiment Proportion Top {} in All Year".format(Selected_Limit))
            return fig    
        youtube_dff2_sentiment = youtube_dff2_sentiment[youtube_dff2_sentiment['Month'] == Selected_Month]
        youtube_dff2_sentiment = youtube_dff2_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
            go.Bar(name='Neutral Percentage', y=youtube_dff2_sentiment["%Neutral Count"], x=youtube_dff2_sentiment["Brand"]),
            go.Bar(name='Negative Percentage', y=youtube_dff2_sentiment["%Negative Count"], x=youtube_dff2_sentiment["Brand"]),
            go.Bar(name='Positive Percentage', y=youtube_dff2_sentiment["%Positive Count"], x=youtube_dff2_sentiment["Brand"])
            ])
        fig.update_layout(barmode="stack",title="Youtube Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
        return fig
    
    
    if Selected_Month == 0:
        youtube_dff_sentiment = youtube_dff_sentiment.groupby("Brand",as_index=False).mean()
        fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=youtube_dff_sentiment["%Neutral Count"], x=youtube_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=youtube_dff_sentiment["%Negative Count"], x=youtube_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=youtube_dff_sentiment["%Positive Count"], x=youtube_dff_sentiment["Brand"])
        ])
        fig.update_layout(barmode="stack",title="Youtube Sentiment Proportion Top {} in All Year".format(Selected_Limit))
        return fig    
    youtube_dff_sentiment = youtube_dff_sentiment[youtube_dff_sentiment['Month'] == Selected_Month]
    youtube_dff_sentiment = youtube_dff_sentiment.groupby("Brand",as_index=False).mean()
    fig = go.Figure(data=[
        go.Bar(name='Neutral Percentage', y=youtube_dff_sentiment["%Neutral Count"], x=youtube_dff_sentiment["Brand"]),
        go.Bar(name='Negative Percentage', y=youtube_dff_sentiment["%Negative Count"], x=youtube_dff_sentiment["Brand"]),
        go.Bar(name='Positive Percentage', y=youtube_dff_sentiment["%Positive Count"], x=youtube_dff_sentiment["Brand"])
        ])
    fig.update_layout(barmode="stack",title="Youtube Sentiment Proportion Top {} in Month {}".format(Selected_Limit,Selected_Month))
    return fig

#Youtube Graph 3-1 Relationship analysis
@app.callback(
    dash.dependencies.Output('Relationship-graph1-d3-youtube', 'figure'),
    [dash.dependencies.Input("month-slider-d3-youtube", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-youtube", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-youtube", "value"),
     dash.dependencies.Input("youtube-limit-d3", "value")]
)
def update_figure(Selected_Month,Selected_Y, Selected_X, Selected_Limit):
    youtube_dff = youtube_df.copy()
    sum_youtube_dff = youtube_dff.groupby("Category").mean()
    limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube = list(limit_youtube_df.index)
    youtube_dff = youtube_df[youtube_df['Category'].isin(limit_youtube)]
    youtube_dff.reset_index(inplace = True)
    
    if Selected_Month == 0:
        youtube_dff = youtube_dff.groupby(["Brand","Category"],as_index=False).mean()
        fig = px.scatter(youtube_dff, x = Selected_X, y= Selected_Y,color = "Category",hover_name="Brand",
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    youtube_dff = youtube_dff[youtube_dff['Month'] == Selected_Month] 
    fig = px.scatter(youtube_dff, x = Selected_X, y= Selected_Y, color = "Category",hover_name="Brand",
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-2 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph2-d3-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-youtube", "value"),
     dash.dependencies.Input("month-slider-d3-2-youtube", "value"),
     dash.dependencies.Input("Y-Axis-dropdown-d3-2-youtube", "value"),
     dash.dependencies.Input("X-Axis-dropdown-d3-2-youtube", "value"),
     dash.dependencies.Input("Size-dropdown-d3-youtube", "value"),
     dash.dependencies.Input("youtube-limit-d3-2", "value"),
     dash.dependencies.Input("youtube-brand-d3", "value")]
)
def update_figure(Selected_Category,Selected_Month,Selected_Y, Selected_X, Selected_Size,Selected_Limit,Selected_Brands):
    youtube_dff = youtube_df.copy()
    youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
    sum_youtube_dff = youtube_dff.groupby("Brand").mean()
    limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube = list(limit_youtube_df.index)
    youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
        additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
        youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
        youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            youtube_dff2 = youtube_dff2.groupby("Brand",as_index=False).mean()
            fig = px.scatter(youtube_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
            return fig

        youtube_dff2 = youtube_dff2[youtube_dff2['Month'] == Selected_Month] 
        fig = px.scatter(youtube_dff2, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
        return fig
    
    if Selected_Month == 0:
        youtube_dff = youtube_dff.groupby("Brand",as_index=False).mean()
        fig = px.scatter(youtube_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship All Year".format(Selected_Y,Selected_X))
        return fig

    youtube_dff = youtube_dff[youtube_dff['Month'] == Selected_Month] 
    fig = px.scatter(youtube_dff, x = Selected_X, y= Selected_Y,color = "Brand", size = Selected_Size,
                     title="{} and {} Relationship Month {}".format(Selected_Y,Selected_X,Selected_Month))
    return fig


#Graph 3-3 Relationship analysis

@app.callback(
    dash.dependencies.Output('Relationship-graph3-d3-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d3-youtube", "value"),
    dash.dependencies.Input("month-slider-d3-2-youtube", "value"),
    dash.dependencies.Input("Data-dropdown-d3-youtube", "value"),
    dash.dependencies.Input("youtube-limit-d3-2", "value"),
    dash.dependencies.Input("youtube-brand-d3", "value")])

def update_figure(Selected_Category, Selected_Month, Selected_Data, Selected_Limit, Selected_Brands):
    youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
    sum_youtube_dff = youtube_dff.groupby("Brand").mean()
    limit_youtube_df = sum_youtube_dff.sort_values(['Score'],ascending=False).head(Selected_Limit)
    limit_youtube = list(limit_youtube_df.index)
    youtube_dff = youtube_df[youtube_df['Brand'].isin(limit_youtube)]
    
    if Selected_Brands != '':
        brands = Selected_Brands.lower().split(', ')
        youtube_df['Lower Brand'] = youtube_df['Brand'].str.lower()
        additional_youtube_df = youtube_df[youtube_df['Lower Brand'].isin(brands)]
        youtube_dff2 = youtube_dff.append(additional_youtube_df, ignore_index=True)            
        youtube_dff2.drop_duplicates(inplace=True, ignore_index=True)
        
        if Selected_Month == 0:
            youtube_dff2 = youtube_dff2.groupby(by="Brand",as_index=False).mean()
            fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff2["Brand"], y=youtube_dff2[c]) for c in Selected_Data])
            fig.update_layout(title="Youtube Data All Year", xaxis={'categoryorder':'total descending'})
            return fig
                        
        youtube_dff2 = youtube_dff2[youtube_dff2['Month'] == Selected_Month]                 
        fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff2["Brand"], y=youtube_dff2[c]) for c in Selected_Data])
        fig.update_layout(title="Youtube Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
        return fig
    
    
    if Selected_Month == 0:
        youtube_dff = youtube_dff.groupby(by="Brand",as_index=False).mean()
        fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff["Brand"], y=youtube_dff[c]) for c in Selected_Data])
        fig.update_layout(title="Youtube Data All Year", xaxis={'categoryorder':'total descending'})
        return fig
                        
    youtube_dff = youtube_dff[youtube_dff['Month'] == Selected_Month]                 
    fig = go.Figure(data=[go.Bar(name= c, x=youtube_dff["Brand"], y=youtube_dff[c]) for c in Selected_Data])
    fig.update_layout(title="Youtube Data Month {}".format(Selected_Month), xaxis={'categoryorder':'total descending'})
    return fig


#Graph 3-4 Relationship analysis Heatmap

@app.callback(
    dash.dependencies.Output('Heatmap-d4-youtube', 'figure'),
    [dash.dependencies.Input("Category-dropdown-d4-youtube", "value")]
)
def update_figure(Selected_Category):
    if Selected_Category == 'Overall':
        youtube_dff = youtube_df.drop([c for c in youtube_df.columns if c not in variable_list_youtube], axis = 1)
        fig = px.imshow(youtube_dff.corr().fillna(0),
                       labels=dict(color="Correlation Coefficient"),
                       x = [c for c in youtube_dff.columns],
                       y = [c for c in youtube_dff.columns])
        fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
        return fig
    youtube_dff = youtube_df[youtube_df['Category'] == Selected_Category]
    youtube_dff.drop([c for c in youtube_dff.columns if c not in variable_list_youtube], axis = 1,inplace=True)
    fig = px.imshow(youtube_dff.corr().fillna(0),
                    labels=dict(color="Correlation Coefficient"),
                    x = [c for c in youtube_dff.columns],
                    y = [c for c in youtube_dff.columns])
    fig.update_layout(title='Correlation Heatmap ({})'.format(Selected_Category), width=1000, height=800)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




