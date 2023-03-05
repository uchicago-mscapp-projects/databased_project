
"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: plots.py
Authors: Abe Burton and Lee-Or Bentovim 
Note: We wrote this file entirely jointly and all work is equally attributable to both of us

Outputs:
    None: opens a Dash page on local server with all visualizations

Description:
    TODO: Lorem ipsum 

Some guidance was drawn from this plotly example: 
https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-nlp/app.py
"""

from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import pathlib
import sys

VOTE_SHARE = {'cand_kb':.109, 'cand_cg':.137, 'cand_jg':.021, 'cand_bj':.211,
'cand_sk':.013, 'cand_rs':.004, 'cand_pv':.332,'cand_ww':.093, 'cand_ll':.169}

NAME = {'cand_kb':'Kam Buckner', 'cand_cg':'Chuy García',
        'cand_jg':"Ja'Mal Green", 'cand_bj':'Brandon Johnson',
        'cand_sk':'Sophia King', 'cand_rs':'Roderick Sawyer',
        'cand_pv':'Paul Vallas','cand_ww':'Willie Wilson',
        'cand_ll':'Lori Lightfoot'}

NEWS = {'news_cc':"Crain's Chicago Business", 'news_ct':'Chicago Tribune',
        'news_cd':"Chicago Defender", 'news_hp':'Hyde Park Herald',
        'news_ln':'Lawndale News', 'news_tt':'The Triibe',
        'overall_sentiment':'Overall Sentiment'}
MENTION_LABELS = ['Kam Buckner', 'Chuy García', "Ja'Mal Green", 'Brandon Johnson',
                'Sophia King', 'Roderick Sawyer', 'Paul Vallas',
                'Willie Wilson', 'Lori Lightfoot', 'Total Unique Articles']


"""

# Data Reading and Reformatting
# Much of the data is imported in JSON formats that need reformatting

"""

parent_string = str(pathlib.PurePath(sys.path[0]).parents[0]) + '/analysis/data/'

"""

# Dataset 1: Mentions by Candidate

"""

count_cand_path = parent_string + 'count_cand.json'
count_cand_df = pd.read_json(count_cand_path, orient='index')
count_cand_df.rename(columns={0:'mentions'}, inplace=True)
count_cand_df.drop(['total_num_articles_scraped'], inplace=True)
count_cand_df['candidates'] = MENTION_LABELS


"""

# Dataset 2: News Sentiment by candidate and paper

"""

cand_news_sentiment_df_path = parent_string + 'sentiment.json'
cand_news_sentiment_df = pd.read_json(cand_news_sentiment_df_path)
cand_news_sentiment_df_formatted = pd.DataFrame(columns = 
                ['news_id','candidate_id','value','candidates', 'newspapers'])


for col in cand_news_sentiment_df.columns:
    for row in cand_news_sentiment_df[col].items():
        
        # Pandas reads missing values as nan (type float), exclude those rows
        if not isinstance(row[1], float):

            # Collapses positive and negative values into one column
            temp_pos_df = pd.Series({'news_id': col, 'candidate_id': row[0],
                                     'value': row[1]['pos'], 
                                     'candidates': NAME[row[0]],
                                     'newspapers': NEWS[col]})

            temp_neg_df = pd.Series({'news_id': col, 'candidate_id': row[0],
                                     'value': -1 * row[1]['neg'], 
                                     'candidates': NAME[row[0]], 
                                     'newspapers': NEWS[col]})

            cand_news_sentiment_df_formatted = pd.concat([cand_news_sentiment_df_formatted, 
                                    temp_pos_df.to_frame().T], ignore_index=True)
            cand_news_sentiment_df_formatted = pd.concat([cand_news_sentiment_df_formatted, 
                                    temp_neg_df.to_frame().T], ignore_index=True)

# Adds a column flagging if the associated value is positive or negative for graph
cand_news_sentiment_df_formatted['sign'] = cand_news_sentiment_df_formatted['value'] > 0

# clean_articles_df = pd.read_csv(pathlib.Path(__file__).parent.parent / clean_articles_filepath, usecols=['candidate_id', 'newspaper_id', 'url', 'date'], nrows = 50)

"""

# Dataset 3: Most Frequent Word by Candidate and Newspaper

"""

# This df comes from a JSON of Word frequency by candidate and newspaper
words_df_path = parent_string + 'word_freq_cand_by_news.json'
words_df = pd.read_json(words_df_path)
word_df_formatted = pd.DataFrame(columns = ['news_id', 'candidate_id',
                                'word','freq','candidates', 'newspapers'])

for col in words_df.columns:
    for index, row in words_df[col].items():

        # Pandas reads missing values as nan (type float), exclude those rows
        if not isinstance(row, float):
            for pair in row:
                temp_df = pd.Series({'news_id':col, 'candidate_id':index,
                                'word':pair[0],'freq':pair[1],
                                'candidates':NAME[index], 'newspapers':NEWS[col]})
                word_df_formatted = pd.concat([word_df_formatted, 
                                        temp_df.to_frame().T], ignore_index=True)


# This df comes from a JSON of Word frequency from all sites combined
words_freq_cand_df_path = parent_string + 'word_freq_candidate.json'
words_freq_cand_df = pd.read_json(words_freq_cand_df_path, orient='index')

for col in words_freq_cand_df.columns:
    for index, row in words_freq_cand_df[col].items():

            # Due to JSON conversion, some rows appear as None, exclude them
            if row is not None:
                temp_df = pd.Series({'news_id':'all_sites', 'candidate_id':index,'word':row[0],'freq':row[1], 'candidates':NAME[index], 'newspapers':'All Sites'})
                word_df_formatted = pd.concat([word_df_formatted, temp_df.to_frame().T], ignore_index=True)

"""

#Create the app

"""


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


"""

# Make Graphs
# Static Graphs live here, live graphs are created in callbacks

"""

# Mentions Graph
mentions = px.bar(count_cand_df, x='candidates', y='mentions', 
            labels={'candidates':'Candidate', 'mentions':'Number of Mentions'})
mentions.update_traces(marker=dict(color = 'mediumseagreen'))

# Mentions vs. Vote Share
temp_df = count_cand_df

# Remove rows we don't want to plot, Lightfoot removed as incumbent
temp_df.drop(['total_unique_articles_scraped', 'cand_ll'], inplace=True)
temp_df = pd.concat([temp_df,pd.Series(VOTE_SHARE)],axis=1)
temp_df.rename(columns={0:'vote_share'}, inplace=True)
mentions_scatter = px.scatter(temp_df, x='mentions', y = 'vote_share', 
                            text='candidates', labels={'mentions':'Number of Mentions','vote_share': 'Vote Share'})
mentions_scatter.update_traces(marker=dict(color ='darkviolet', size=10),
                               textposition='bottom center')

"""

# Make Cards (One per section)

"""

# This card refers to Newspaper Mentions by Candidate
mentions_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Newspaper Mentions by Candidate")),
        dbc.CardBody(
            [
                dcc.Graph(id='mentions_graph', figure=mentions)
            ]
        ),
        dbc.CardFooter("Newspapers: Chicago Tribune, Chicago Defender,\
                        Crain's Chicago Business, Hyde Park Herald,\
                        Lawndale News, The Triibe"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

# This card refers to Sentiment by Candidate and Newspaper
sentiment_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Sentiment by Candidate and Newspaper")),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(html.P("Choose a News Source:"), md=12),
                    dbc.Col([
                        dcc.Dropdown(
                            id='sentiment-input',
                            options=[
                                {'label': source, 'value': source}
                                for source in 
                                cand_news_sentiment_df_formatted\
                                ['newspapers'].unique()
                            ],
                            value='Overall Sentiment',
                        )
                    ], md=12),
                    dcc.Graph(id='sentiment-graph'),
                ],
                )
            ],
            style={'marginTop':0, 'marginBottom':0},
        ),
        dbc.CardFooter("Sentiment represents the percent of words used in\
        sentences where the candidate is mentioned that are positive or negative"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

# This card refers to Most Common Words by Candidate and Newspaper
wordcloud_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Most Common Words by Candidate and Newspaper")),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(html.P("Choose a News Source:"), md=6),
                    dbc.Col(html.P("Choose a Candidate:"), md=6),
                    dbc.Col([
                        dcc.Dropdown(
                            id='news-drop',
                            options=[
                                {'label': source, 'value': source}
                                for source in word_df_formatted['newspapers'].unique()
                            ],
                            value='All Sites',
                        )
                    ], md=6),
                    dbc.Col([
                        dcc.Dropdown(
                            id='candidate-drop',
                            options=[
                                {'label': source, 'value': source}
                                for source in word_df_formatted['candidates'].unique()
                            ],
                            value='Lori Lightfoot',
                        )
                    ], md=6),
                ],
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Loading(
                            id="loading-frequencies",
                            children=[dcc.Graph(id="frequency-figure")],
                            type="default",
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dcc.Loading(
                            id="loading-wordcloud",
                            children=[dcc.Graph(id="wordcloud")],
                            type="default",
                        ),
                        md=8,
                    ),
                ],
                ),
            ],
            style={'marginTop':0, 'marginBottom':0},
        ),
        dbc.CardFooter(""),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

# This card refers to Newspaper Mentions by Candidate
scatter_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Vote Share vs. Number of Mentions")),
        dbc.CardBody(
            [
                dcc.Graph(id='mentions_scatter', figure=mentions_scatter)
            ]
        ),
        dbc.CardFooter("Lori Lightfoot excluded due to Incumbency. Correlation ~0.45"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

"""

# Creating a NavBar and Body for displaying our data

"""

# Put together body of cards
BODY = html.Div(children=[
    dbc.Row([dbc.Col(md=2),dbc.Col(mentions_card),dbc.Col(md=2),], style={'marginTop':0}),
    dbc.Row([dbc.Col(md=2),dbc.Col(sentiment_card),dbc.Col(md=2),], style={'marginTop':30}),
    dbc.Row([dbc.Col(md=2),dbc.Col(wordcloud_card),dbc.Col(md=2),], style={'marginTop':30}),
    dbc.Row([dbc.Col(md=2),dbc.Col(scatter_card),dbc.Col(md=2),], style={'marginTop':30}),
],
    style={'backgroundColor':'slategray'}
)

# Create Navbar
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("dataBased: Mayoral Candidate Coverage Analysis")
                    ),
                ],
            ),
        )
    ],
    color="white",
    dark=False,
    sticky="top",
)

# Create app layout
app.layout = html.Div(children=[NAVBAR, BODY])


"""
# Callbacks

# Create graphs with decorators so that the graphs update 
    when a dropdown is selected
"""

# Callback for Sentiment Graph
@app.callback(
    Output('sentiment-graph', 'figure'),
    Input('sentiment-input', 'value')
)
def sentiment_graph(selection):
    """ 
    This Callback creates the sentiment graph for the selected newspaper

    Inputs: 
        selection (str): selection is determined when the value at id
                sentiment-input is changed
    
    Outputs:
        graph (graph object): the bar graph created, which returns to the id
                at sentiment-graph as a figure
    """
    temp_df = cand_news_sentiment_df_formatted[cand_news_sentiment_df_formatted\
                                                ['newspapers'] == selection]
    graph = px.bar(temp_df, x='candidates', y='value', color='sign',
                labels={'candidates': 'Candidate', 'values': 'Value'},
                color_discrete_sequence=['mediumseagreen','darkviolet'])

    newnames = {'True':'Positive', 'False': 'Negative'}
    graph.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )

    graph.update_layout(legend={'title_text':''})
    return graph


@app.callback(
    [
        Output("wordcloud", "figure"),
        Output("frequency-figure", "figure"),
    ],
    [
        Input("news-drop", "value"),
        Input("candidate-drop", "value"),
    ],
)
def update_wordcloud_plot(news_value_drop, cand_value_drop):
    """ 
    This Callback creates the wordcloud and frequency graphs for the 
    selected newspaper and candidate pairing

    Inputs: 
        news_value_drop (str): news_value_drop is determined when the value at 
                id news-drop is changed
        cand_value_drop (str): cand_value_drop is determined when the value at 
                id candidate-drop is changed
    
    Outputs:
        wordcloud_figure (image object): the wordcloud created, which returns to
                the id at wordcloud as a figure
        frrequency_figure (graph object): the bar graph created, which returns to
                the id at frequency-figure as a figure
    """
    temp_df = word_df_formatted[(word_df_formatted['newspapers'] == 
        news_value_drop) & (word_df_formatted['candidates'] == cand_value_drop)]

    # Create the wordcloud
    cloud = WordCloud(max_font_size=400, background_color='white', 
                      width=2500, height=1250)
    temp_df.set_index('word', inplace=True, drop=False)
    freq_dict = pd.DataFrame(temp_df['freq']).to_dict()['freq']
    cloud.generate_from_frequencies(freq_dict)

    wordcloud_figure = px.imshow(cloud)
    wordcloud_figure.update_xaxes(visible=False)
    wordcloud_figure.update_yaxes(visible=False)
    
    # Create the bar graph
    frequency_figure = px.bar(temp_df.iloc[:20].iloc[::-1], x='freq', y='word',
                orientation='h', labels={'freq': 'Frequency', 'word': 'Word'})

    frequency_figure.update_traces(marker=dict(color = 'mediumseagreen'))

    return (wordcloud_figure, frequency_figure)

if __name__ == "__main__":
    # Run the app on the specified port
    app.run_server(debug=False, port=8059)