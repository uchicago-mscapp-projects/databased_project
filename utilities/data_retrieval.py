import sqlite3
import pathlib

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

    # the select statement
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
    list
        A list of parks that match the given parameters.  Each park should be an instance of
        `sqlite.Row` with the appropriate fields (see "What attributes should be returned?"
         in the README).
    """
    # filepath = pathlib.Path(__file__).parent.p
    # get the connection working and then we're all good
    connection = sqlite3.connect('data/news_databse.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query, variables = query_builder(params)

    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()

    return results