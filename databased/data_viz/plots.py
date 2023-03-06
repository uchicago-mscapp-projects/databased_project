"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: plots.py
Authors: Abe Burton and Lee-Or Bentovim
Note: We wrote this file entirely jointly and all work is equally attributable to both of us

Outputs:
    None: opens a Dash page on local server with all visualizations

Description:
    Creates all the plots and generates a dashboard to display our analysis

Some guidance was drawn from this plotly example:
https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-nlp/app.py
"""
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import data_viz.data_processing as dp


VOTE_SHARE = {'cand_kb':.109, 'cand_cg':.137, 'cand_jg':.021, 'cand_bj':.211,
'cand_sk':.013, 'cand_rs':.004, 'cand_pv':.332,'cand_ww':.093, 'cand_ll':.169}

# Dataset 1: Mentions by Candidate
count_cand_df = dp.mentions_candidate()
# Dataset 2: News Sentiment by candidate and paper
cand_news_sentiment_df_formatted = dp.sent_cand_paper()
# Dataset 3: Most Frequent Word by Candidate and Newspaper
word_df_formatted = dp.word_freq()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"""

# Make Graphs
# Static Graphs live here, dynamic graphs are created in callbacks

"""
def vote_scatter():
    """Create scatterplot of Mentions vs. Vote Share"""
    temp_df = count_cand_df[count_cand_df['newspapers'] == 'All Sites']
    # Remove rows we don't want to plot, Lightfoot removed as incumbent
    temp_df.set_index('candidate_id',inplace=True)
    temp_df = pd.concat([temp_df,pd.Series(VOTE_SHARE)],axis=1)
    temp_df = temp_df[temp_df['candidates'] != 'Lori Lightfoot']
    temp_df.rename(columns={0:'vote_share'}, inplace=True)
    mentions_scatter = px.scatter(temp_df, x='mentions', y = 'vote_share',
                                text='candidates', labels={'mentions':'Number of Mentions',
                                'vote_share': 'Vote Share'})

    mentions_scatter.update_traces(marker=dict(color ='darkviolet', size=10),
                                textposition='bottom center')

    return mentions_scatter

"""

# Make Cards (One per section) for inserting into the app layout

"""

# This card refers to Newspaper Mentions by Candidate
mentions_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Article Mentions by Candidate and Newspaper")),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(html.P("Choose a News Source:"), md=12),
                    dbc.Col([
                        dcc.Dropdown(
                            id='mentions-input',
                            options=[
                                {'label': source, 'value': source}
                                for source in
                                count_cand_df\
                                ['newspapers'].unique()
                            ],
                            value='All Sites',
                        )
                    ], md=12),
                    dcc.Graph(id='mentions-graph'),
                ],
                )
            ],
            style={'marginTop':0, 'marginBottom':0},
        ),
        dbc.CardFooter(""),
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
                dcc.Graph(id='mentions_scatter', figure=vote_scatter())
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


"""
# Callbacks

# Create graphs with decorators so that the graphs update
    when a dropdown is selected
"""

# Callback for Mentions Bar
@app.callback(
    Output('mentions-graph', 'figure'),
    Input('mentions-input', 'value')
)
def mentions_bar(selection):
    """
    This Callback creates the mentions graph for the selected newspaper

    Inputs:
        selection (str): selection is determined when the value at id
                mentions-input is changed

    Outputs:
        mentions (graph object): the bar graph created, which returns to the id
                at mentions-graph as a figure
    """
    temp_df = count_cand_df[count_cand_df['newspapers'] == selection]
    mentions = px.bar(temp_df, x='candidates', y='mentions',
                labels={'candidates':'Candidate', 'mentions':'Number of Mentions'})
    mentions.update_traces(marker=dict(color = 'mediumseagreen'))

    return mentions

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
                labels={'candidates': 'Candidate', 'value': 'Sentiment Percentage'},
                color_discrete_sequence=['mediumseagreen', 'darkviolet'])

    newnames = {'True':'Positive', 'False': 'Negative'}
    graph.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
    graph.update_layout(legend={'title_text':''})

    return graph


app.layout = html.Div(children=[NAVBAR, BODY])  


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


def run_data_viz():
    """
    This function runs everything in the plots file and creates the app. It is
    called by the make file for the project
    """

    app.run_server(debug=False, port=8042)


if __name__ == "__main__":

    app.run_server(debug=False, port=8042)
