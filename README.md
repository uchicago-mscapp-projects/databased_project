*This README.md file was generated on 03-04-23 by Madeleine Roberts*
# CAPP 30122 databased_project
Examining the Scope and Sentiment of Local Newspaper Coverage on the 2023 Primary Election's Mayoral Candidates in Chicago

## Authors
- [Abe Burton](https://github.com/abejburton)
- [Kathryn Link-Oberstar](https://github.com/klinkoberstar)
- [Lee-Or Bentovim](https://github.com/bentoviml)
- [Madeleine Roberts](https://github.com/MadeleineKRoberts) 

## Introduction
## Installation

```bash
poetry install
python3 -m pip install nltk
```

## Usage
Project must be run in the Poetry virtual environment. 
Within project terminal, initalize virual environment by running:
```bash
poetry shell
```


Execute the data visualization of Dash by running:
```bash
python -m databased/dash
```


Execute all scrapers/apis by running:
```bash
python -m databased/scrapers
```
<sub>Note: this command will take about ?? minutes to complete.</sub>


Execute all data cleaning by running:
```bash
python -m databased/clean
```
<sub>Note: this command will take about 2 minutes to complete.</sub>


Execute all data analysis by running:
```bash
python -m databased/analysis
```
<sub>Note: this command will take about 35 minutes to complete. However, if you comment out lines 54 and 55 in basic_sentiment.py the command will execute in about 2 minutes. The completion of the JSON for overall newspaper sentiment will be prevented as a result of this.</sub>




