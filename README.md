Demo video: https://www.linkedin.com/posts/rajarajeswari-s-49671428b_hello-everyone-my-new-project-phonepe-activity-7180220064678260736-xd5G?utm_source=share&utm_medium=member_desktop

Problem Statement:
The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.
The solution must include the following steps:
1. Extract data from the Phonepe pulse Github repository through scripting and clone it.
2. Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.
3. Insert the transformed data into a MySQL database for efficient storage and retrieval.
4. Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.
5. Fetch the data from the MySQL database to display in the dashboard.
6. Provide at least 10 different dropdown options for users to select different facts and figures to display on the dashboard.

To run this project, 
1.You need to install the packages from requirements.txt .
2.Connection string for MySQL.
3.collect datas and create table from data table.py .
4.Run main app.py  .

Data extraction: 
Clone the Github using git to fetch the data from the https://github.com/PhonePe/pulse  Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.

Data transformation:
Using a scripting language such as Python, along with libraries such as Pandas, to manipulate and convert the datas as dataframe.From top folder created seperate dataframe for district and pincodes.

Database insertion:
connect to a MySQL database and insert the transformed data using SQL commands.To avoid duplication I have used if else statement.

Visualization:
Using the Streamlit and Plotly libraries in Python and created an interactive and visually appealing dashboard.Used geo visualization,pie chart,donut chart and scatter plot.
