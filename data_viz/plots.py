from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


cand_sentiment_filepath = "data/candidate_bs.json"
news_sentiment_filepath = "data/news_bs.json"
cand_news_sentiment_filepath = "data/cand_by_newspaper_bs.json"
clean_articles_filepath = "data/clean_articles.json"

# Read in the data
cand_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/candidate_bs.json', orient='index')
cand_sentiment_df['neg'] = cand_sentiment_df['neg'] * -1
candidates = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Lori Lightfoot','Roderick Sawyer','Paul Vallas','Willie Wilson']
cand_sentiment_df['candidates'] = candidates

news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/news_bs.json', orient='index')
# cand_news_sentiment_df is a little weird w formatting hopefully it works for now
cand_news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/cand_by_newspaper_bs.json')

# TODO get article info from maddie and also most common words.
# clean_articles_df = pd.read_csv(pathlib.Path(__file__).parent.parent / clean_articles_filepath, usecols=['candidate_id', 'newspaper_id', 'url', 'date'], nrows = 50)

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = px.bar(cand_sentiment_df, x='candidates', y=['pos','neg'], labels={'candidates':'Candidate', 'value': 'Sentiment'}, title='Sentiment Scores By Candidate')
fig.layout.update(showlegend=False)



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
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

app.layout = html.Div(children=[NAVBAR, dcc.Graph(id='example_graph', figure=fig)]) #, BODY

if __name__ == "__main__":
    app.run_server(debug=False, port=8056)