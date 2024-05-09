# SQLAlchemy-Challenge
## General Overview
- Used Python and SQLAlchemy to do a basic climate analysis and data exploration of my climate database. Specifically, used SQLAlchemy ORM queries, Pandas, and Matplotlib.
## Tasks
- Precipitation Analysis:
  - Found the most recent date in the dataset.
  - Got the previous 12 months of precipitation data by querying the previous 12 months of data.
  - Selected only the "date" and "prcp" values.
  - Loaded the query results into a Pandas DataFrame and explicitly set the column names.
  - Sorted the DataFrame values by "date".
  - Plotted the results by using the DataFrame plot method.
  - Used Pandas to print the summary statistics for the precipitation data.
- Station Analysis:
  - Designed a query to calculate the total number of stations in the dataset.
  - Designed a query to find the most-active stations.
  - Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
  - Designed a query to get the previous 12 months of temperature observation (TOBS) data.
- Designed a Climate App
## Instructions for running app.py
- Download folder or copy repository to your desktop.
- Open up the repository in VS code or your perferred IDE.
- Navigate to app.py and then run the file.
- Note: If you're having trouble running this file, try changing the file path for create_engine to an absolute path.
