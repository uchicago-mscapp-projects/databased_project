import sys

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
#from databased.data_viz #need function to call ?

def run():
    print()
    print("********************************************************************************************************************************")
    print()
    print("Welcome to the CAPP 122 databased project.")
    print("Examining the Scope and Sentiment of Local Newspaper Coverage on the 2023 Primary Election's Mayoral Candidates in Chicago")

    render_project()

def render_project():
    print()
    print("To execute a desired aspect of the project please enter one of the following commands:")
    print("\t 1 - Open Data Visualization")
    print("\t 2 - Scrape All Newspapers")
    print("\t 3 - Clean Scraped Data")
    print("\t 4 - Conduct Data Analysyis")
    print("\t 5 - Run Entire Project Start to Finish (Scrape -> Clean -> Analyze -> Visualize)")
    print("\t 6 - End Program")
    print()
    user_input = input("Please input the number of your desired command: ")

    try:
        user_input = int(user_input)
    except ValueError:
        user_input = -1
        
    
    if user_input == 1:
        print("\nRendering DASH for Data Visualization:")
        # Will need to enter the command for data viz here
        ask_continue()

    elif user_input == 2:
        run_scrapers()
        ask_continue()

    elif user_input == 3:
        print("\nCleaning Data")
        export_clean()
        ask_continue()

    elif user_input == 4:
        run_analysis()
        ask_continue()

    elif user_input == 5:
        print("\nExecuting Entire Project")
        
        run_scrapers()

        print("\nCleaning Data")
        export_clean()

        run_analysis()

        print("\nRendering DASH for Data Visualization:")
        # Will need to enter the command for data viz here
        ask_continue()
    elif user_input == 6:
        print("\nClosing Project.")

        print("\n********************************************************************************************************************************\n")
        return
    else:
        print("\nERROR! User input not recognized. Please input the singular digit of your desired command and press enter.")
        render_project()




def run_analysis():
    print("\nCalculating Total Article Counts:")
    retrieve_total_article_counts()

    print("\nCalculating Most Frequently Used Words:")
    most_frequent()

    print("\nAnalyzing Sentiment:")
    basic_sentence_sentiment()


def run_scrapers():
    print("\nScraping the Chicago Defender:")
    defender_scrape()
    
    print("\nScraping the Hyde Park Harold:")
    hph_scrape() 

    print("\nScraping Lawndale News:")
    ln_scrape()

    print("\nScraping the TRiiBE:")
    triibe_scrape()

    print("\nAccessing APIs of the Chicago Tribune and Crain's Chicago Business:")
    run_selection()
    # ^ TODO ask kathryn if tar files are created from this, if so delete and rerun to ensure it works
   
def ask_continue():
    user_input = input("\nWould you like to enter another command (y/n): ")

    if user_input == 'y':
        render_project()
        # call begining render
    elif user_input == 'n':
        print("Closing Project.")
        print("\n********************************************************************************************************************************\n")
    else:
        print("\nERROR! Unrecognized User Input. Please input the singular letter of your desired command and press enter.")
        ask_continue()
