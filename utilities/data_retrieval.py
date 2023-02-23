import sqlite3
import pathlib
import pandas as pd

def query_builder(dataset = None, columns = None):
    """
    Build a SQL query string based to pull the requested dataset and columns

    Inputs:
        dataset (str): name of a dataset to pull
        columns (lst): list of columns to pull from the merged data in the form
            ['dataset_name.column_name', 'second_dataset.column_name']
    Outputs:
        query: str
    """
    select_statement = ['*']
    from_statement = ''

    if dataset:
        from_statement = dataset
    else:
        from_statement = 'articles LEFT JOIN newspaper ON article.newspaper_id = newspaper.newspaper_id LEFT JOIN candidate_info ON articles.candidate_id = candidate_info.candidate_id'
    if columns:
        select_statement = columns

    select_statement = ', '.join(select_statement)
    query = f'SELECT {select_statement} FROM {from_statement}'

    return query


def query(dataset = None, columns = None):
    """
    Execute a query
    
    Inputs:
        dataset (str): name of a dataset to pull
        columns (lst): list of columns to pull from the merged data in the form
            ['dataset_name.column_name', 'second_dataset.column_name']

    Outputs: 
        df (dataframe): A dataframe with the requested sql data
    """
    filepath = pathlib.Path(__file__).parent.parent / 'data/news_database.db'
    connection = sqlite3.connect(filepath)
    query = query_builder(dataset, columns)
    df = pd.read_sql_query(query, connection)
    connection.close()

    return df
