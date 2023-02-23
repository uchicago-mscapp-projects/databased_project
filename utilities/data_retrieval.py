"""
This module contains functions that retrieve data from the sqlite database.
There are functions for returning specific datasets and for getting the table
used as inputs in the scraper functions.
"""

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
        from_statement = 'candidate JOIN candidate_info ON candidate.candidate_id = candidate_info.candidate_id'
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


def search_strings(newspaper_id = ''):
    """
    Pull the list of candidate names and output a list of newspaper search strs
    
    Inputs:
        newspaper_id (str): the id of the newspaper you want to have search info for
            newspaper ids are ['news_cs','news_cd','news_hp',
            'news_tt','news_ln']
    
    Outputs:
        df (dataframe): a dataframe with all scraper input info
    """
    candidate_combinations = query(columns= ['candidate.candidate_id',
                                             'candidate.name_tokens',
                                             'candidate_info.announcement_date'])
    news_searches = candidate_combinations.copy()
    news_searches['newspaper_id'] = pd.Series([newspaper_id for _ in range(len(news_searches.index))])
        
    return news_searches