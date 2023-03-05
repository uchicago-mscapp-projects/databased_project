"""
Project: CAPP 122 DataBased Project
File name: app.py

Executes the dataBASED project.

@Author: Madeleine Roberts
@Date: Mar 4, 2023
"""

import sys
from textwrap import dedent

# Scrapers
from databased.scrapers.defender import defender_scrape
from databased.scrapers.scrape_lawndale import ln_scrape
from databased.scrapers.hph_scraper import hph_scrape
from databased.scrapers.tribune_crain_select import run_selection
from databased.scrapers.triibe import triibe_scrape

# Data Cleaning
from databased.cleaning.clean import export_clean

# Analysis
from databased.analysis.article_counts import retrieve_total_article_counts
from databased.analysis.most_frequent_words import most_frequent
from databased.analysis.basic_sentiment import basic_sentence_sentiment

# Data Visualization
#from databased.data_viz.plots.app import run_server

def run():
    """
    Print an intial message for executing the CAPP 122 dataBASED project. 
    Then, call the `render_project` function.
    """
    print(dedent(
    """
    ********************************************************************************************************************************
    CAPP 122 dataBASED project
    Examining the Scope and Sentiment of Local Newspaper Coverage on the 2023 Primary Election's Mayoral Candidates in Chicago"""
    ))
    render_project()

def render_project():
    """
    Print a message with instructions for executing different aspects of the project based on user input.
    Takes user input as a string and executes the corresponding aspect of the project.
    """
    print(dedent(
        """
        To execute a desired aspect of the project please enter one of the following commands:
        \t 1 - Open Data Visualization
        \t 2 - Scrape All Newspapers
        \t 3 - Clean Scraped Data
        \t 4 - Conduct Data Analysyis
        \t 5 - Run Entire Project Start to Finish (Scrape -> Clean -> Analyze -> Visualize)
        \t 6 - End Program
        """))
    
    user_input = input("Please input the number of your desired command: ")

    # Ensure correct user input
    try:
        user_input = int(user_input)
    except ValueError:
        user_input = -1
        
    # Visualize command
    if user_input == 1:
        print("\nRendering DASH for Data Visualization:")
        # TODO we need to figure this out
        ask_continue()
   
    # Scrape command
    elif user_input == 2:
        run_scrapers()
        ask_continue()
    
    # Clean command
    elif user_input == 3:
        print("\nCleaning Data:")
        export_clean()
        ask_continue()

    # Analysis command
    elif user_input == 4:
        run_analysis()
        ask_continue()

    # Run entire project command
    elif user_input == 5:
        print("\nExecuting Entire Project")

        run_scrapers()

        print("\nCleaning Data:")
        export_clean()

        run_analysis()

        print("\nRendering DASH for Data Visualization:")
        # Will need to enter the command for data viz here
        ask_continue()

    # Close command
    elif user_input == 6:
        close_project()
        return

    # Invalid input
    else:
        print("\nERROR! User input not recognized. Please input the singular digit of your desired command and press enter.")
        render_project()


def run_analysis():
    """
    Executes the data analysis files.
    """
    print("\nCalculating Total Article Counts:")
    retrieve_total_article_counts()

    print("\nCalculating Most Frequently Used Words:")
    most_frequent()

    print("\nAnalyzing Sentiment:")
    basic_sentence_sentiment()


def run_scrapers():
    """
    Executes all newpaper scrapers and APIs.
    """
    print("\nScraping the Chicago Defender:")
    defender_scrape()
    
    print("\nScraping the Hyde Park Herald:")
    hph_scrape() 
    # TODO add print statement within this file

    print("\nScraping Lawndale News:")
    ln_scrape()

    print("\nScraping The TRiiBE:")
    triibe_scrape()

    print("\nAccessing APIs of the Chicago Tribune and Crain's Chicago Business:")
    run_selection()
    # ^ TODO ask kathryn if tar files are created from this, if so delete and rerun to ensure it works


def close_project():
    """
    Closes project
    """
    print("Closing Project.")
    print("\n********************************************************************************************************************************\n")
   

def ask_continue():
    """
    Prompts user if they would like to execute another portion of the project
    """
    user_input = input("\nWould you like to enter another command (y/n): ")

    if user_input == 'y':
        render_project()
        
    elif user_input == 'n':
        close_project()
    else:
        print("\nERROR! Unrecognized User Input. Please input the singular letter of your desired command and press enter.")
        ask_continue()


