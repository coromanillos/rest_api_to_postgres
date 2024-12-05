# ETL Process Documentation

## Overview
This document outlines the ETL (Extract, Transform, Load) Pipeline.	
this process is responsible for extracting Balance Sheet data from the Alpha Vantage API, transforming it to ensure consistency and data integrity, and staging it into a PostgreSQL database. 

### Key Steps
1. **Extract**: Pull data from the API.

2. **Transform**: Clean and prepare data for the target schema.

3. **Load**: Insert the data into the PostgreSQL database.

---

## 1. Extract

### Source
- **API**: Alpha Vantage API
- **Endpoint**: `https://www.alphavantage.co/query`
- **Parameters**: 
  - `function=ALPHA_VANTAGE_INTRADAY`
  - `symbol=IBM`
  - `interval=5min`
  - `apikey=your_api_key_here`

### Process
Data is fetched using the `requests` library. The **raw data** is saved in the `etl_project/data/raw_data/` directory with a timestamp for each extraction.

The **raw data** will then be processed for consistency, and saved in the 'etl_project/data/processed_data' directory with a timestamp for data consistency cleaning completion.

Saving both the raw data and the processed data locally is good practice for testing and validation, as well as for keeping historical records locally. This will also reduce load on databases as validation can happen outside of the database and data can be uploaded in batches. In critical events, this local data can serve as backup data if the ETL process has errors later on.

## 2. Transform

### Source
- **Raw Data**: Saved to directory as a json file after extraction step.

### Process
 - Extract time series data saved to a directory for raw data in a json format.

 - Validate and transform the data.

 - Save the processed data to a specified location.

 - Log datetime for successful/unsuccessful process.

 - Error checks for common issues

 - **TEST:** Parallel Processing module for enhanced data transformation speed.





- Look into encrypting local data, for security and data privacy. i.e banking data with personal info, etc.

- Data extracted from the Alpha Vantage **BALANCE_SHEET** REST API is not time-series nor incremental data. There is no real point in automating this via cron job scheduling and logging. Pivot the project to maximize modularity and reusability for one-time endpoint extractions...

- Finally, look into cloud options, Amazon S3 may be a popular long term solution for data, rather than leaving in in a postgres database.

