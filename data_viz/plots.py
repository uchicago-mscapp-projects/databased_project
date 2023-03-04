from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Read in the data
cand_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/candidate_bs.json', orient='index')
cand_sentiment_df['neg'] = cand_sentiment_df['neg'] * -1
CANDIDATES = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Lori Lightfoot','Roderick Sawyer','Paul Vallas','Willie Wilson']
cand_sentiment_df['candidates'] = CANDIDATES

news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/news_bs.json', orient='index')

# Candidate Sentiment By Newspaper data is in a tricky json format. Reformat
# to work with pandas.
cand_news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/cand_by_newspaper_bs.json')
cand_news_sentiment_df_formatted = pd.DataFrame(columns = ['candidate_id','neg','pos','neu','compound','news_id'])
for col in cand_news_sentiment_df.columns:
    for row in cand_news_sentiment_df[col].items():
        if not isinstance(row[1], float):
            temp_df = {'candidate_id':row[0],'neg':row[1]['neg'],'pos':row[1]['pos'], 'neu':row[1]['neu'], 'compound':row[1]['compound'], 'news_id':col}
            cand_news_sentiment_df_formatted = cand_news_sentiment_df_formatted.append(temp_df, ignore_index = True)
        else:
            temp_df = {'candidate_id':row[0], 'neg':None, 'pos':None, 'neu':None, 'compound':None, 'news_id':col}
            cand_news_sentiment_df_formatted = cand_news_sentiment_df_formatted.append(temp_df, ignore_index = True)
cand_news_sentiment_df_formatted.dropna(inplace=True)
cand_news_sentiment_df_formatted.reset_index(drop=True, inplace=True)
            
# TODO get article info from maddie and also most common words.
# clean_articles_df = pd.read_csv(pathlib.Path(__file__).parent.parent / clean_articles_filepath, usecols=['candidate_id', 'newspaper_id', 'url', 'date'], nrows = 50)

count_cand_df = pd.read_json('/home/abejburton/capp30122/databased_project/analysis/data/count_cand.json', orient='index')
count_cand_df.rename(columns={0:'mentions'}, inplace=True)
MENTION_LABELS = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Roderick Sawyer','Paul Vallas','Willie Wilson','Lori Lightfoot','Total Articles','Total Unique Articles']
count_cand_df['candidates'] = MENTION_LABELS
count_cand_df.drop(['total_num_articles_scraped'], inplace=True)
# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

mentions = px.bar(count_cand_df, x='candidates', y='mentions', labels={'candidates':'Candidate', 'mentions':'Number of Mentions'})
sentiment = px.bar(cand_sentiment_df, x='candidates', y=['pos','neg'], labels={'candidates':'Candidate', 'value': 'Sentiment'})
sentiment.layout.update(showlegend=False)

mentions_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Number of Mentions by Candidate")),
        dbc.CardBody(
            [
                dcc.Graph(id='mentions_graph', figure=mentions)
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

sentiment_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Sentiment by Candidate")),
        dbc.CardBody(
            [
                dcc.Graph(id='sentiment_graph', figure=sentiment)
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={"marginTop": 0, "marginBottom": 0},
)

BODY = html.Div(children=[
    dbc.Row([dbc.Col(md=2),dbc.Col(mentions_card),dbc.Col(md=2),], style={'marginTop':30}),
    dbc.Row([dbc.Col(md=2),dbc.Col(sentiment_card),dbc.Col(md=2),], style={'marginTop':30}),
])

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("dataBased: Mayoral Candidate Coverage Analysis", className="ml-2")
                    ),
                ],
                align="center"
            ),
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

app.layout = html.Div(children=[NAVBAR, BODY])

if __name__ == "__main__":
    app.run_server(debug=False, port=8056)