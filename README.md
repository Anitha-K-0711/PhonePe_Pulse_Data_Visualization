# PhonePe_Pulse_Data_Visualization
Hi all! I created this App to visualize PhonePe Pulse github repository data (https://github.com/PhonePe/pulse) to have a ring-side view of how India sends, spends, manages and grows its money using Plotly and Streamlit.

#### Requirements of the project
Python

Pandas

GitHub Cloning

MySQL

MySQL-Connector-Python

Streamlit

Plotly


#### Link for web app: 

#### Extracting data from github and converting it to csv files
The dataset I used in my streamlit web app to visualize and analyse is taken from https://github.com/PhonePe/pulse.
After cloning files from the github repo, I created a For loop to loop through each folder and get datas from it and then append it to a dataframe to make it easy to convert it to csv files.

Refer data_extraction_phonepe.ipynb for the full code of this entire process.

Now we have to repeat this process for all respective folders and convert everything to proper csv files

#### Preprocessing and uploading the data into MySQL database
The necessary cleaning and preprocessing are done to each and every csv files to check for duplicate rows, null values, outliers, datatypes and to check whether the data is distributed uniformly with respect to all classes.
After preprocessing the datas, It is ready to insert the csv files to MySQL database for efficient storage and retrieval.

To insert datas into Mysql I used sqlalchemy (In order to establish connection you want pymysql also). In order to insert csv to Mysql we need to establish connection to Mysql server. After connecting we create table to insert csv file to Mysql database. 

Repeat the above process for all csv files to insert into Mysql database. Refer data_preprocessing_phonepe.ipynb for the full code of this entire process.

#### DASHBOARD
#### The main components of dashboard are
1 GEOGRAPHICAL ANALYSIS

2 TRANSACTION ANALYSIS

3 USER DATA ANALYSIS

4 TOP STATES DATA ANALYSIS


Refer main.py for the full code of this entire process.

#### Geographical Analysis
The India map shows the Total Transactions of PhonePe in both state-wise and District-wise.It comes with a zoom option and on hover, it displays the content related to that particular state or district. 

The main functions I have used to create this map are Plotly scatter_geo for plotting districts and states and Plotly choropleth for drawing the states in India map.

#### Transaction Analysis
The Transaction Analysis mainly contains the visualization of total Transactions count and total amount in each state and district. I have used different graphs available in plotly to represent this data. I have created 5 different tabs and analysed the transaction data of phonepe in detail.

Those tabs are,

a. State Analysis

b. District Analysis

c. Payment Type Analysis

d. Year-Wise Analysis

e. Overall Analysis


The main functions I have used for the above are px.bar and px.pie ('px' stands for Plotly Express)
For each and every analysis, I have provided details of the figure and important insights and observations of the figure to its right side of the dashboard.

Also, If the viewer of the app is interested on further graphs and charts to explore into, I have also provided hidden Pie chart figures on some tabs. This will further help the viewer to visualize the data more precisely.

#### 3 User Data Analysis
The Users data mainly contains the registered users count and app openings via different mobile brands in each state and district. I have used different graphs available in plotly to represent this data. I have created 4 different tabs and analysed the user data of phonepe in detail.

Those tabs are,

a. State Analysis

b. District Analysis

c. User Device Year-Wise Analysis

d. Overall Analysis


The main functions I have used for the above are go.Bar, go.Pie px.bar, px.treemap and px.pie ('px' stands for Plotly Express & 'go' stands for Graph Objects)

For each and every analysis, I have provided details of the figure and important insights and observations of the figure to its right side of the dashboard.

Also, If the viewer of the app is interested on further graphs and charts to explore into, I have also provided hidden Pie chart and Bar graph figures on some tabs. This will further help the viewer to visualize the data more precisely.

#### Top States Data Analysis
According to the Year and Quarter the viewer selects, the tables of top 3 states in the category of registered users, total transactions and total amount are displayed.

I have simply used pandas sort_values, groupby and indexing functions to retrieve this data.
