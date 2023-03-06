"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: data_processing.py
Authors: Abe Burton and Lee-Or Bentovim
Note: We wrote this file entirely jointly and all work is equally attributable to both of us

Description:
    This file takes the clean data from nlp analysis json files and adjusts
    the format in various ways to match the plot specifications in dataframes
"""
import sys
import pathlib
import pandas as pd

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

parent_string = str(pathlib.PurePath(sys.path[0]).parents[0]) + '/databased_project/databased/analysis/data/'

"""

# Dataset 1: Mentions by Candidate

"""
def mentions_candidate():
    """
    This creates the dataset with information on the number of mentions for
    each candidate in each newspaper that is used in the mentions graph in the
    dashboard.

    Outputs:
        count_cand_df (dataframe): dataframe for use in mentions graph
    """
    name_id_list = 7*list(NAME.keys())
    name_list = 7*list(NAME.values())
    names_dict = {'candidate_id': name_id_list, 'candidates': name_list}
    count_cand_df = pd.DataFrame(names_dict)
    count_cand_df['mentions'] = 0

    news_dict = {'news_cc':"Crain's Chicago Business", 'news_ct':'Chicago Tribune',
        'news_cd':"Chicago Defender", 'news_hp':'Hyde Park Herald',
        'news_ln':'Lawndale News', 'news_tt':'The Triibe', 'all_sites':'All Sites'}

    news_id_list = 9 * list(news_dict.keys())
    news_list = 9 * list(news_dict.values())
    news_dict_formatted = pd.DataFrame({'news_id': news_id_list, 'newspapers': news_list})
    count_cand_df = count_cand_df.join(news_dict_formatted)

    count_cand_path = parent_string + 'count_cand_by_news.json'
    cand_news_count_df = pd.read_json(count_cand_path)

    for col in cand_news_count_df.columns:
        if col in news_dict.keys():
            for row in cand_news_count_df[col].items():
                count_cand_df.loc[(count_cand_df['news_id'] == col) & (count_cand_df['candidate_id'] == row[0])] = [row[0], NAME[row[0]], row[1], col, news_dict[col]]


    all_sites_path = parent_string + 'count_cand.json'
    all_sites_df = pd.read_json(all_sites_path, orient='index')
    all_sites_df.rename(columns={0:'mentions'}, inplace=True)
    all_sites_df.drop(['total_num_articles_scraped', 'total_unique_articles_scraped'], inplace=True)

    for key, val in all_sites_df.itertuples():
        count_cand_df.loc[(count_cand_df['news_id'] == 'all_sites') & (count_cand_df['candidate_id'] == key)] = [key, NAME[key], val, 'all_sites', 'All Sites']

    count_cand_df['mentions'] = count_cand_df['mentions'].fillna(0)

    return count_cand_df


"""

# Dataset 2: News Sentiment by candidate and paper

"""
def sent_cand_paper():
    """
    This creates the dataset with information on the sentiment for
    each candidate in each newspaper that is used in the sentiment graph in the
    dashboard.

    Outputs:
        cand_news_sentiment_df_formatted (dataframe): dataframe for use in mentions graph
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
            else:

                temp_pos_df = pd.Series({'news_id': col, 'candidate_id': row[0],
                                        'value': 0,
                                        'candidates': NAME[row[0]],
                                        'newspapers': NEWS[col]})

                temp_neg_df = pd.Series({'news_id': col, 'candidate_id': row[0],
                                        'value': 0,
                                        'candidates': NAME[row[0]],
                                        'newspapers': NEWS[col]})

            cand_news_sentiment_df_formatted = pd.concat([cand_news_sentiment_df_formatted,
                                    temp_pos_df.to_frame().T], ignore_index=True)
            cand_news_sentiment_df_formatted = pd.concat([cand_news_sentiment_df_formatted,
                                    temp_neg_df.to_frame().T], ignore_index=True)    

    # Adds a column flagging if the associated value is positive or negative for graph
    cand_news_sentiment_df_formatted['sign'] = cand_news_sentiment_df_formatted['value'] >= 0

    return cand_news_sentiment_df_formatted

"""

# Dataset 3: Most Frequent Word by Candidate and Newspaper

"""

def word_freq():
    """
    This creates the dataset with information on the word frequency for each
    candidate and newspaper.

    Outputs:
        word_df_formatted (dataframe): dataframe for use in wordclouds
    """
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
                temp_df = pd.Series({'news_id':'all_sites', 'candidate_id':index,
                'word':row[0],'freq':row[1], 'candidates':NAME[index], 
                'newspapers':'All Sites'})

                word_df_formatted = pd.concat([word_df_formatted, 
                                    temp_df.to_frame().T], ignore_index=True)
         
    return word_df_formatted
