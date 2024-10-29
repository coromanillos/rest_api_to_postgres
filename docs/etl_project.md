# Preface
- This data project will explore processing real time data, delving into the fundamentals of data engineering. We will be focusing on gaining technical skills, as well as improving our understanding of ETL (Extraction, Transformation, Loading) concepts. 
- By the end of this project, we will have gained a better understanding of the ETL pipelines, and common techniques and technologies that can be used to enhance them.

## Objective
- Display a data visualization of company intraday stock price information. Have the data stored both for historical record keeping as well as data analytics for end users. 

- Explore: cron jobs, Prisma, postgreSQL, Node.js, Jupyter Notebooks.

1. Design the Schema
Define Data Models: Identify the entities you'll be working with (e.g., users, transactions) and design your PostgreSQL schema to reflect these entities.
Create Migrations: Use Prisma to create migrations based on your schema design.

2. Set Up PostgreSQL
Install PostgreSQL: Ensure that PostgreSQL is installed and running on your machine or server.
Create Database: Set up a new database for your project and create the necessary tables based on your schema.

3. Extract Data from API
Choose a Library: Use Python's requests library or Node.js's built-in http/axios for making API calls.
Implement Data Extraction:
Write a Python or Node.js script that periodically calls the API and retrieves real-time data.
Implement error handling for API failures.

4. Transform Data
Validation and Cleansing:
Write transformation functions that will validate the data. For example, check for missing fields, ensure data types are correct (e.g., strings instead of numbers), etc.
Implement any necessary data transformations (e.g., converting formats, normalizing data).
Testing: Validate your transformation functions using sample data in Jupyter notebooks to ensure they work as expected.

5. Load Data into PostgreSQL
Use Prisma ORM:
Set up Prisma in your Node.js application to connect to your PostgreSQL database.
Write scripts to insert the transformed data into the appropriate tables.
Batch Inserts: Consider using batch inserts for efficiency, especially if processing large volumes of data.

6. Automate the Pipeline with Cron Jobs
Create a Cron Job: Set up a cron job that runs your data extraction and loading script at specified intervals (e.g., every hour).
Ensure the cron job is configured to handle logging and error notifications.
Test the Cron Job: Manually trigger the job and ensure it runs as expected.

7. Documentation and Visualization with Jupyter Notebooks
Document the Process: Use Jupyter notebooks to create documentation for your project, including:
An overview of the architecture.
Code snippets of the extraction, transformation, and loading processes.
Results of your data validations.
Visualization: If applicable, visualize the data trends using libraries like Matplotlib or Seaborn to demonstrate the effectiveness of your pipeline.