from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt

### Read in the data
# Candidate Sentiment By Newspaper data is in a tricky json format. Reformat
# to work with pandas.
cand_news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/analysis/data/sentiment.json')
cand_news_sentiment_df_formatted = pd.DataFrame(columns = ['news_id','candidate_id','neg','pos','neu','compound','candidates', 'newspapers'])

name_dict = {'cand_kb':'Kam Buckner', 'cand_cg':'Chuy García', 'cand_jg':"Ja'Mal Green", 'cand_bj':'Brandon Johnson', 'cand_sk':'Sophia King', 'cand_rs':'Roderick Sawyer', 'cand_pv':'Paul Vallas','cand_ww':'Willie Wilson', 'cand_ll':'Lori Lightfoot'}
news_dict = {'news_cc':"Crain's Chicago", 'news_ct':'Chicago Tribune', 'news_cd':"Chicago Defender", 'news_hp':'Hyde Park Herald', 'news_ln':'Lawndale News', 'news_tt':'The Triibe', 'overall_sentiment':'Overall Sentiment'}

for col in cand_news_sentiment_df.columns:
    for row in cand_news_sentiment_df[col].items():

        if not isinstance(row[1], float):
            temp_df = {'news_id':col, 'candidate_id':row[0],'neg':row[1]['neg'],'pos':row[1]['pos'], 'neu':row[1]['neu'], 'compound':row[1]['compound'], 'candidates':name_dict[row[0]], 'newspapers':news_dict[col]}
            cand_news_sentiment_df_formatted = cand_news_sentiment_df_formatted.append(temp_df, ignore_index = True)
        else:
            temp_df = {'news_id':col, 'candidate_id':row[0], 'neg':None, 'pos':None, 'neu':None, 'compound':None, 'candidates':None, 'newspapers':None}
            cand_news_sentiment_df_formatted = cand_news_sentiment_df_formatted.append(temp_df, ignore_index = True)

cand_news_sentiment_df_formatted.dropna(inplace=True)
cand_news_sentiment_df_formatted.reset_index(drop=True, inplace=True)
cand_news_sentiment_df_formatted['neg'] = cand_news_sentiment_df_formatted['neg'] * -1

            
# TODO get article info from maddie and also most common words.
# clean_articles_df = pd.read_csv(pathlib.Path(__file__).parent.parent / clean_articles_filepath, usecols=['candidate_id', 'newspaper_id', 'url', 'date'], nrows = 50)
# Candidate references in articles count
count_cand_df = pd.read_json('/home/abejburton/capp30122/databased_project/analysis/data/count_cand.json', orient='index')
count_cand_df.rename(columns={0:'mentions'}, inplace=True)
MENTION_LABELS = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Roderick Sawyer','Paul Vallas','Willie Wilson','Lori Lightfoot','Total Articles','Total Unique Articles']
count_cand_df['candidates'] = MENTION_LABELS
count_cand_df.drop(['total_num_articles_scraped'], inplace=True)

words_df = pd.read_json("/home/abejburton/capp30122/databased_project/analysis/data/word_freq_cand_by_news.json")
word_df_formatted = pd.DataFrame(columns = ['news_id','candidate_id','word','freq','candidates', 'newspapers'])
news_dict_wordcloud = {'news_cc':"Crain's Chicago", 'news_ct':'Chicago Tribune', 'news_cd':"Chicago Defender", 'news_hp':'Hyde Park Herald', 'news_ln':'Lawndale News', 'news_tt':'The Triibe', 'all_sites':'All Sites'}

for col in words_df.columns:
    for index, row in words_df[col].items():
        if not isinstance(row, float):
            for pair in row:
                temp_df = {'news_id':col, 'candidate_id':index,'word':pair[0],'freq':pair[1], 'candidates':name_dict[index], 'newspapers':news_dict_wordcloud[col]}
                word_df_formatted = word_df_formatted.append(temp_df, ignore_index = True)
            
words_freq_cand_df = pd.read_json("/home/abejburton/capp30122/databased_project/analysis/data/word_freq_candidate.json", orient='index')

for col in words_freq_cand_df.columns:
    for index, row in words_freq_cand_df[col].items():
            if row is not None:
                temp_df = {'news_id':'all_sites', 'candidate_id':index,'word':row[0],'freq':row[1], 'candidates':name_dict[index], 'newspapers':news_dict_wordcloud['all_sites']}
                word_df_formatted = word_df_formatted.append(temp_df, ignore_index = True)


### Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Make Graphs
mentions = px.bar(count_cand_df, x='candidates', y='mentions', labels={'candidates':'Candidate', 'mentions':'Number of Mentions'})
mentions.update_traces(marker=dict(color = 'blue'))
#sentiment.layout.update(showlegend=False)

# Make Cards
mentions_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Number of Newspaper Mentions by Candidate")),
        dbc.CardBody(
            [
                dcc.Graph(id='mentions_graph', figure=mentions)
            ]
        ),
        dbc.CardFooter("Newspapers: Chicago Tribune, Chicago Defender, Crain's Chicago, Hyde Park Herald, Lawndale News, The Triibe"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

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
                                for source in cand_news_sentiment_df_formatted['newspapers'].unique()
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
        dbc.CardFooter("Sentiment represents the percent of words used in sentences where the candidate is mentioned that are positive or negative"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

wordcloud_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Most Common Words by Candidate and Newspaper")),
        dbc.Alert(
            "Not enough data to render these plots, please adjust the filters",
            id="no-data-alert",
            color="warning",
            style={"display": "none"},
        ),
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

# Put together body of cards
BODY = html.Div(children=[
    dbc.Row([dbc.Col(md=2),dbc.Col(mentions_card),dbc.Col(md=2),], style={'marginTop':30}),
    dbc.Row([dbc.Col(md=2),dbc.Col(sentiment_card),dbc.Col(md=2),], style={'marginTop':30}),
    dbc.Row([dbc.Col(md=2),dbc.Col(wordcloud_card),dbc.Col(md=2),], style={'marginTop':30}),
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
    style={'backgroundColor':'slategray'},
)

# Create app layout
app.layout = html.Div(children=[NAVBAR, BODY])


"""
Callbacks

Create graphs with decorators so that the graphs update when a dropdown
is selected
"""

@app.callback(
    Output('sentiment-graph', 'figure'),
    Input('sentiment-input', 'value')
)
def sentiment_graph(selection):
    """ Callback to create the sentiment graph for the selected newspaper"""
    temp_df = cand_news_sentiment_df_formatted[cand_news_sentiment_df_formatted['newspapers'] == selection]
    graph = px.bar(temp_df, x='candidates', y=['pos', 'neg'],
                   labels={'candidates': 'Candidate'})
    print(selection)
    return graph


@app.callback(
    [
        Output("wordcloud", "figure"),
        Output("frequency-figure", "figure"),
        Output("no-data-alert", "style"),
    ],
    [
        Input("news-drop", "value"),
        Input("candidate-drop", "value"),
    ],
)
def update_wordcloud_plot(news_value_drop, cand_value_drop):
    """ Callback to rerender wordcloud plot with the given filters """
    temp_df = word_df_formatted[(word_df_formatted['newspapers'] == news_value_drop) & (word_df_formatted['candidates'] == cand_value_drop)]
    # Create the wordcloud
    cloud = WordCloud(max_font_size=400, background_color='white', width=2500, height=1250)
    temp_df.set_index('word', inplace=True, drop=False)
    freq_dict = pd.DataFrame(temp_df['freq']).to_dict()['freq']
    cloud.generate_from_frequencies(freq_dict)
    wordcloud_figure = px.imshow(cloud)
    wordcloud_figure.update_xaxes(visible=False)
    wordcloud_figure.update_yaxes(visible=False)
    
    # Create the bar graph
    frequency_figure = px.bar(temp_df.iloc[:20].iloc[::-1], x='freq', y='word', orientation='h')
    frequency_figure.update_traces(marker=dict(color = 'blue'))

    alert_style = {"display": "none"}
    if (wordcloud_figure == {}) or (frequency_figure == {}):
        alert_style = {"display": "block"}
    print("redrawing wordcloud...done")

    return (wordcloud_figure, frequency_figure, alert_style)


if __name__ == "__main__":
    # Run the app on the specified port
    app.run_server(debug=False, port=8059)