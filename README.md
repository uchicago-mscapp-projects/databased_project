*This README.md file was generated on 03-04-23 by Madeleine Roberts*
# CAPP 30122 dataBASED Project
Examining the Scope and Sentiment of Local Newspaper Coverage on the 2023 Primary Election's Mayoral Candidates in Chicago

## Authors
- [Abe Burton](https://github.com/abejburton)
- [Kathryn Link-Oberstar](https://github.com/klinkoberstar)
- [Lee-Or Bentovim](https://github.com/bentoviml)
- [Madeleine Roberts](https://github.com/MadeleineKRoberts) 

## Introduction
The project aims to analyze the press coverage of Chicago's mayoral primary race and investigate how candidates are covered differently in local newspapers. We scraped/accessed the APIs of six different Chicago focused media sites to collect data. We then conducted data analysis to identify which topics are brought up most often and sentiment analysis to examine the tone of the articles. This analysis was performed for the candidate overall, the paper overall and for the candidate in each paper.


## Installation
Note can only be run with 

1. [Install Poetry to Local Machine](https://python-poetry.org/docs/)

2. Clone the Project Repository via SSH

```bash
git@github.com:uchicago-capp122-spring23/databased_project.git
```

3. Install Virtual Environment and Dependencies

```bash
poetry shell
poetry install
```

## Usage
Project **must** be run in the Poetry virtual environment. 
Upon completion of above installation requirements and within project terminal, 
and on each subsequent rendering of project, initialize virtual environment by running:

```bash
poetry shell
```
<br />


**Execute the project by running:**
```bash
python -m databased
```
<sub> This command may take a minute to load project to terminal.</sub>
<br />
<br />

You are then prompted to enter a singular digit command to execute a portion or the entire project, as seen below. 
<br />

```bash
To execute a desired aspect of the project please enter one of the following commands:
    1 - Open Data Visualization
    2 - Scrape All Newspapers
    3 - Clean Scraped Data
    4 - Conduct Data Analysis
    5 - Run Entire Project Start to Finish (Scrape -> Clean -> Analyze -> Visualize)
    6 - End Program
    
Please input the number of your desired command:
```
<sub>example: "1[Return]" will run the data visualization.</sub>

<br />

**Command 1 - Opens Data Visualization**

Renders a Dash to visualize the final results of the dataBASED project.

Notes: 
<br />
&emsp; This command will take about 1 minute to render Dash.
<br />
&emsp; Dash will throw a warning "This is a development server," this error is fine.

<br />

**Command 2 - Executes All Scrapers/Proquest API**

Runs all scrapers and Proquest API to collect newspaper articles about Chicago's mayoral candidates. The retrieved data is then stored in JSON format and outputted to the databased/data folder.

Note: This command will take about 20 minutes to complete.

<br />

**Command 3 - Executes All Data Cleaning**

Runs data cleaning on all scraped data; strips stop words, normalizes case, and selects only sentences that refer to the candidate that is the subject of the article. The cleaned data is then stored in JSON format and outputted to the databased/data folder.

Note: This command will take about 1 minute to complete.

<br />


**Command 4 - Execute All Data Analysis**

Runs data analysis on cleaned candidate data to calculate word frequency, sentiment, and article counts for the candidate, the newspaper, and for the candidate within each paper. The results are outputted to JSON files within databased/analysis/data folder.

Note: This command will take about 12 minutes to complete. However, if you comment out lines 54 and 55 in basic_sentiment.py the command will execute in about 1 minute. The completion of the JSON for overall newspaper sentiment will be prevented as a result of this.

<br />


**Command 5 - Execute Entire Project**

Runs entire project start to finish. Runs scrapers/Proquest API, then cleans article data, conducts data analysis, and renders the visualization of results.

Note: this command will take about 45 minutes to complete.

<br />

**Command 6 - Close Project**

Terminates python scripts.

## Overall Notes
If you encounter issues with nltk or pyarrow please run the following commands within the poetry shell:
```bash
python3 -m pip install nltk
python3 pip install pyarrow 
```
<br />
Upon extensive testing, sometimes a scraper will become blocked by servers. If this occurs, run program again and they should run completely.

## Acknowledgments
CAPP 122 Instructor - Professor James Turk

CAPP 122 Project TA - Yifu Hou

Local Chicago New Sources Used for Data Collection:
- [Crain's Chicago Business](https://www.chicagobusiness.com/)
- [Chicago Defender](https://chicagodefender.com/)
- [Chicago Tribune](https://www.chicagotribune.com/)
- [Hyde Park Herald](https://www.hpherald.com/)
- [Lawndale News](http://www.lawndalenews.com/)
- [The TRiiBE](https://thetriibe.com/)

