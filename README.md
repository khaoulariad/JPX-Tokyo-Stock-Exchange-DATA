## Introduction
We will build an ETL pipeline for the data from https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/data.
This dataset contains historic data for a variety of Japanese stocks and options, it may be used to train a prediction model that why it is split into multiple folders that cover different time windows and serve different purposes: 
- train_files : Data folder covering the main training period.
- supplemental_files : Data folder containing a dynamic window of supplemental training data updated reguraly.
- example_test_files : Data folder covering the public test period.
  The previous folders contain the same csvs : options, trades, stock_prices, secondary_stock_prices and financials.
- data_specifications: Folder for individual columns definitions of each csv.
- stock_list.csv : a single file for mapping between the SecuritiesCode and company names

## Requirements
### Python Packages
To run the project, multiple python packages are required, you can directly run the command to install them all :
```shell
$ pip install --upgrade -r requirements.txt 
```

### Kaggle
You need to login to your kaggle account and get the api token from there, a json file will be downloaded, save it to c:/users/'your user'/.kaggle

### MySql
It is pretty simple to settup mysql in your machine, you can downlowd it from https://dev.mysql.com/downloads/installer/. During installation, you'll be prompted to configure the MySQL server :
- Make sure to set a password for root and change it in the **config.json** file provided.
- When it asks to "Disallow root login remotely?" answer No because we will need to communicate to the server from a web app.
  
## Extraction 
Kaggle offers an API in python to load datasets, and interacts with competitions. It requires an API token, (see requirements).
We will extract the dataset with the api and save them locally as is (csv format).

## Transform and Store
Given the manageable size of the current dataset, we could have opted to keep the transformed data in **CSV format**, which would have been a feasible solution. Additionally, we could have chosen to save the data in **Delta Parquet** format, which offers superior performance and storage efficiency, particularly beneficial for handling larger datasets.  

To ensure a production-ready solution, we chose to use a **MySQL** database. MySQL efficiently handles large datasets with various storage engines that optimize performance and will allow easy updates whenever new data needs to be reloaded from the source.  
We will focus on the train_data folder and create tables for each csv file we have.

## How To Use
First make sure to follow the requirements.  
To downlowd data, create datbase and populate it :
```sh
$ python etlPipeline.py
```
The program will take around 10-12 mins only for the initial setup (creating the table for options.csv file takes the most of it), after that it runs rapidly.  

To display the dashboard :
```sh
$ streamlit run dashboard.py
```
