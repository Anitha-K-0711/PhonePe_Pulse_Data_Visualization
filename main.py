import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
import streamlit as st
from PIL import Image
import warnings

warnings.filterwarnings("ignore")

# mysql server connection using sqlalchemy
connection = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="password", db="phonepe_pulse"))

# fetching datas from mysql using pandas
query1 = 'select * from agg_trans_table'
df_agg_trans = pd.read_sql_query(sql=text(query1), con=connection.connect())
query2 = 'select * from agg_user_summary_table'
df_agg_user_summary = pd.read_sql_query(sql=text(query2), con=connection.connect())
query3 = 'select * from agg_user_table'
df_agg_user = pd.read_sql_query(sql=text(query3), con=connection.connect())
query4 = 'select * from lat_long_district'
df_lat_long_district = pd.read_sql_query(sql=text(query4), con=connection.connect())
query5 = 'select * from lat_long_state'
df_lat_long_state = pd.read_sql_query(sql=text(query5), con=connection.connect())
query6 = 'select * from map_trans_table'
df_map_trans = pd.read_sql_query(sql=text(query6), con=connection.connect())
query7 = 'select * from map_user_table'
df_map_user = pd.read_sql_query(sql=text(query7), con=connection.connect())

image  = Image.open('logo.png') # uploading phonepe logo

# Title for the dashboard and a description on this app
st.set_page_config(layout="wide")
colQ1,colQ2 = st.columns([0.8,0.2])
with colQ1:
    st.title(':purple[PHONEPE PULSE DATA ANALYSIS]')
with colQ2:
    st.image(image, width=150)
with st.expander('About the App'):
    st.write(
        """This App is created to visualize PhonePe Pulse github repository data (https://github.com/PhonePe/pulse) 
        to have a ring-side view of how India sends, spends, manages and grows its money. This App demystifies and 
        shares the what, why and how of digital payments in India. It is your window to the world of how India 
        transacts with interesting trends, deep insights and in-depth analysis based on the PhonePe data. This App 
        ensures to give insights and detailed knowledge on geographical analysis, transaction analysis, 
        user data analysis and top 3 states data."""
    )

# Data preparation for geographical analysis
df = df_agg_trans.groupby(["state"])[["total_transaction_count", "total_amount"]].sum()
df = df.reset_index()

df_lat_long_state = df_lat_long_state.sort_values(by='state')
df_lat_long_state = df_lat_long_state.reset_index(drop=True)
del df_lat_long_state['index']

state_list = df_agg_trans['state'].unique()
state_list = tuple(state_list)

choropleth_data = df_lat_long_state.copy()
for column in df.columns:
    choropleth_data[column] = df[column]

df1 = df_agg_trans.groupby(['state', 'year', 'quater'])[["total_transaction_count", "total_amount"]].sum()
df1.to_csv('df1.csv')
df2 = pd.read_csv('df1.csv')

df_state_final = pd.merge(df2, df_lat_long_state, how="outer", on="state")
df_district_final = pd.merge(df_map_trans, df_lat_long_district, how="outer", on=["state", "district_name"])
del df_district_final["index_x"]
del df_district_final["index_y"]

# GEOGRAPHICAL ANALYSIS
st.write('## :green[GEOGRAPHICAL ANALYSIS]')
c1, c2 = st.columns(2)
with c1:
    Year = st.selectbox('Please select the year', ("2018", "2019", "2020", "2021", "2022"), key=3)
with c2:
    Quater = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key=4)

Year = int(Year)
Quater = int(Quater)

plot_state = df_state_final[(df_state_final["year"] == Year) & (df_state_final["quater"] == Quater)]
plot_state_final = plot_state.groupby(['state', 'year', 'quater', 'latitude', 'longitude', 'code']).sum()
plot_state_final = plot_state_final.sort_values(by=['state'], ascending=False)
plot_state_final = plot_state_final.reset_index()

fig1 = px.scatter_geo(plot_state_final,
                      lon=plot_state_final['longitude'],
                      lat=plot_state_final['latitude'],
                      text=plot_state_final['code'],
                      hover_name='state',
                      hover_data=['total_transaction_count', 'total_amount', 'year'])
fig1.update_traces(marker={'color': "#D5FFCC", 'size': 0.3})

plot_district = df_district_final[(df_district_final["year"] == Year) & (df_district_final["quater"] == Quater)]
plot_district = plot_district.sort_values(by=['district_name'], ascending=False)
plot_district = plot_district.reset_index()
plot_district['amount'] = plot_district['total_amount']

fig2 = px.scatter_geo(plot_district,
                      lat=plot_district['latitude'],
                      lon=plot_district['longitude'],
                      color=plot_district['amount'],
                      size=plot_district['total_transaction_count'],
                      hover_name='district_name',
                      hover_data=['total_transaction_count', 'total_amount', 'year', 'state', 'quater'],
                      title='district_name',
                      size_max=22)
fig2.update_traces(marker={'color': "#CC0044", 'line_width': 1})

choropleth_data['state'] = choropleth_data['state'].replace(
    ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
     'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
     'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
     'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya',
     'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
     'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'],
    ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
     'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
     'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
     'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
     'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
     'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'])
# In order to get the landscape of India Map, you need to upload the states of India in the above format only

choropleth_data = choropleth_data.sort_values(by='state', ascending=False)
choropleth_data = choropleth_data.reset_index()
fig = px.choropleth(choropleth_data,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='total_transaction_count',
                    color_continuous_scale='Reds'
                    )
fig.update_geos(fitbounds='locations', visible=False)
fig.add_trace(fig2.data[0])
fig.add_trace(fig1.data[0])

st.write('### **:blue[PhonePe India Map]**')
col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions district wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
    )
    st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewise and districtwise.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
    )

# FIG 2 HIDDEN BAR GRAPH
plot_state_final = plot_state_final.sort_values(by=['total_transaction_count'])
fig = px.bar(plot_state_final, x='state', y='total_transaction_count', title=str(Year) + '  Quarter:  ' + str(Quater))
with st.expander("Click to view Bar Graph for the same data"):
    st.plotly_chart(fig, use_container_width=True)
    st.info(
        '**:blue[The above bar graph shows the increasing order of PhonePe Transactions according to the states of India. Here we can observe the top states with highest transactions]**')

# TRANSACTION ANALYSIS
st.write('## :green[TRANSACTION ANALYSIS]')
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['STATE ANALYSIS', 'DISTRICT ANALYSIS', 'PAYMENT TYPE ANALYSIS', 'YEAR-WISE ANALYSIS', 'OVERALL ANALYSIS'])

# STATE ANALYSIS
with tab1:
    payment_mode_state_wise = df_agg_trans.copy()

    colT1, colT2 = st.columns(2)
    with colT1:
        pay_mode = st.selectbox('Please select the Payment Mode', (
            'Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'),
                                key='a')
    with colT2:
        state = st.selectbox('Please select the state', state_list, key='b')
    State = state
    PaymentMode = pay_mode
    Year = [2018, 2019, 2020, 2021, 2022]
    payment_mode_state_wise = payment_mode_state_wise.loc[
        (payment_mode_state_wise['state'] == State) & (payment_mode_state_wise['year'].isin(Year)) & (
                payment_mode_state_wise['payment_mode'] == PaymentMode)]
    payment_mode_state_wise = payment_mode_state_wise.sort_values(by=['year'])
    payment_mode_state_wise['quater'] = "Q" + payment_mode_state_wise['quater'].astype(str)
    payment_mode_state_wise['year_quarter'] = payment_mode_state_wise['year'].astype(str) + "-" + \
                                              payment_mode_state_wise['quater'].astype(str)
    fig = px.bar(payment_mode_state_wise, x='year_quarter', y='total_transaction_count',
                 color='total_transaction_count', color_continuous_scale='Inferno')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    colA1, colA2 = st.columns([7, 3])
    with colA1:
        st.write('#### ' + State.upper())
        st.plotly_chart(fig, use_container_width=True)
    with colA2:
        st.info(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by you
            - X Axis is basically all years with all quarters 
            - Y Axis represents total transactions in selected mode
            """
        )
        st.info(
            """
            Important Observations:
            - User can observe the pattern of payment modes in a State 
            - We get a basic idea about which mode of payments are either increasing or decreasing in a state
            """
        )

# DISTRICT ANALYSIS
with tab2:
    colB1, colB2, colB3 = st.columns(3)
    with colB1:
        year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='c')
    with colB2:
        state = st.selectbox('Please select the state', state_list, key='d')
    with colB3:
        quarter = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key='e')

    districts = df_map_trans.loc[(df_map_trans['year'] == int(year)) & (df_map_trans['state'] == state) & (
            df_map_trans['quater'] == int(quarter))]
    l = len(districts)
    fig = px.bar(districts, x='district_name', y='total_transaction_count', color='total_transaction_count',
                 color_continuous_scale='viridis', text='district_name')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    colC1, colC2 = st.columns([4, 1])
    with colC1:
        st.write('#### ' + state.upper() + ' WITH ' + str(l) + ' DISTRICTS')
        st.plotly_chart(fig, use_container_width=True)
    with colC2:
        st.info(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by you
            - X Axis represents the districts of selected state
            - Y Axis represents total transactions
            """
        )
        st.info(
            """
            Important Observations:
            - User can observe how transactions are happening in districts of a selected state 
            - We can observe the leading district in a state
            """
        )

# PAYMENT TYPE ANALYSIS
with tab3:
    colG1, colG2, colG3 = st.columns(3)
    with colG1:
        year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='h')
    with colG2:
        state = st.selectbox('Please select the state', state_list, key='i')
    with colG3:
        quarter = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key='j')
    analysis_on = st.selectbox('Please select the values to visualize', ('total_transaction_count', 'total_amount'))

    payment_analysis = df_agg_trans.loc[(df_agg_trans['year'] == int(year)) & (df_agg_trans['state'] == state) & (
            df_agg_trans['quater'] == int(quarter))]

    fig1 = px.pie(payment_analysis, values=analysis_on, names='payment_mode', hole=0.5, hover_data=['year'],
                  color_discrete_sequence=px.colors.sequential.Emrld_r)
    fig2 = px.bar(payment_analysis, x='payment_mode', y=analysis_on, color=analysis_on, color_continuous_scale='emrld_r')

    colH1, colH2 = st.columns([7, 3])
    with colH1:
        st.write('#### ' + state.upper())
        st.plotly_chart(fig2)
    with colH2:
        st.info(
            """
            Details of BarGraph:
            - This entire data belongs to selected Year, selected Quarter and selected State
            - X Axis is all the available payment modes
            - Y Axis represents total transactions or total amount according to the analysis type you select
            """
        )
        st.info(
            """
            Important Observations: 
            - It is clearly understood from bar graph and pie chart about which payment mode is the leading contributor of the selected criterias
            - Based on leading payment mode contributors Phonepe can provide offers to that particular state and to that particular payment mode
            """
        )
    with st.expander('See Pie Chart for the same data'):
        st.plotly_chart(fig1)

# YEAR-WISE ANALYSIS
with tab4:
    colD1, colD2 = st.columns(2)
    with colD1:
        mode = st.selectbox('Please select the Payment Mode', (
            'Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'),
                            key='z')
    with colD2:
        year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='f')

    payment_mode_year_wise = df_agg_trans.copy()
    year = int(year)
    payment_mode_year_wise = payment_mode_year_wise.loc[
        (payment_mode_year_wise['year'] == year) & (payment_mode_year_wise['payment_mode'] == mode)]
    state_groupby = payment_mode_year_wise.groupby('state')
    state_df_final = state_groupby.sum()
    state_df_final['state'] = list(state_list)
    state_df_final = state_df_final.sort_values(by=['total_transaction_count'])
    fig = px.bar(state_df_final, x='state', y='total_transaction_count', color='total_transaction_count',
                 color_continuous_scale='rainbow')
    colE1, colE2 = st.columns([3.8, 1.2])
    with colE1:
        st.write('#### ' + str(year) + ' DATA ANALYSIS')
        st.plotly_chart(fig, use_container_width=True)
    with colE2:
        st.info(
            """
            Details of BarGraph:
            - This entire data belongs to selected Year
            - X Axis is all the states in increasing order of Total transactions
            - Y Axis represents total transactions in selected mode
            """
        )
        st.info(
            """
            Important Observations:
            - We can observe the leading state with highest transactions in the selected payment mode
            - We get basic idea about regional performance of Phonepe
            - Depending on the regional performance Phonepe can provide offers to particular place
            """
        )

# OVERALL ANALYSIS
with tab5:
    year_df = df_agg_trans.groupby('year')
    year_df_final = year_df.sum()
    year_list = df_agg_trans['year'].unique()
    year_df_final['year'] = year_list
    del year_df_final['quater']

    fig = px.pie(year_df_final, values='total_transaction_count', names='year', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Electric,
                 title='TOTAL TRANSACTIONS (2018 TO 2022)')

    colF1, colF2 = st.columns([0.65, 0.35])
    with colF1:
        st.write('#### :green[Drastic Increase in Transactions :rocket:]')
        st.plotly_chart(fig, use_container_width=True)
    with colF2:
        st.write('#### :green[Year Wise Transaction Analysis in India]')
        del year_df_final['index']
        st.markdown(year_df_final.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        st.write(' ')
        st.info(
            """
            Important Observations:
            - It is very clearly understood that online transactions drastically increased
            - Initially in 2018,2019 the transactions are less but with time the online payments increased 
            - We can clearly see that more than 50% of total Phonepe transactions in india happened are from the year 2022
            """
        )

# USER ANALYSIS
st.write('## :green[USER DATA ANALYSIS]')
tab1, tab2, tab3, tab4 = st.tabs(
    ['STATE ANALYSIS', 'DISTRICT ANALYSIS', 'USER DEVICE YEAR-WISE ANALYSIS', 'OVERALL ANALYSIS'])

# STATE ANALYSIS
with tab1:
    st.write('### :blue[State & Userbase]')
    state = st.selectbox('Please select the state', state_list, key='m')

    df_state_analysis = df_agg_user_summary.groupby(['state', 'year'])
    y = df_agg_user_summary['state'] + '-' + df_agg_user_summary['year'].astype(str)

    x_df = df_state_analysis.sum()
    x_df['state_year'] = y.unique()
    state_name = x_df['state_year'].str[:-5]
    x_df['state'] = state_name

    select_state = x_df.loc[x_df['state'] == state]
    total_app_opens = select_state['app_opens'].sum()
    total_reg_users = select_state['registered_users'].sum()
    select_state['app_opens'] = select_state['app_opens'].mul(100 / total_app_opens)
    select_state['registered_users'] = select_state['registered_users'].mul(100 / total_reg_users)

    fig = go.Figure(data=[
        go.Bar(name='App Opens %', x=select_state['state_year'], y=select_state['app_opens'],
               marker={'color': 'crimson'}),
        go.Bar(name='Registered Users %', x=select_state['state_year'], y=select_state['registered_users'],
               marker={'color': 'lightslategrey'})
    ])
    fig.update_layout(barmode='group')
    colI1, colI2 = st.columns([7, 3])
    with colI1:
        st.write('#### ', state.upper())
        st.plotly_chart(fig, use_container_width=True)
    with colI2:
        st.info(
            """
            Details of BarGraph:
            - User need to select a state
            - The X Axis shows both Registered users and App opens
            - The Y Axis shows the Percentage of Registered users and App opens
            """
        )
        st.info(
            """
            Important Observations:
            - User can observe how the App Opens and Registered Users are growing in a state with time
            - One can observe how user base is growing exceptionally
            """
        )

# DISTRICT ANALYSIS
with tab2:
    colJ1, colJ2, colJ3 = st.columns(3)
    with colJ1:
        year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='n')
    with colJ2:
        state = st.selectbox('Please select the state', state_list, key='o')
    with colJ3:
        quarter = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key='p')
    analysis_on = st.selectbox('Please select the values to visualize', ('app_openings', 'registered_user_count'))

    districts = df_map_user.loc[
        (df_map_user['year'] == int(year)) & (df_map_user['state'] == state) & (df_map_user['quater'] == int(quarter))]
    l = len(districts)
    fig = px.bar(districts, x='place_name', y=analysis_on, color=analysis_on, color_continuous_scale='delta')

    colK1, colK2 = st.columns([4, 1])
    with colK1:
        st.write('#### ' + state.upper() + ' WITH ' + str(l) + ' DISTRICTS')
        st.plotly_chart(fig, use_container_width=True)
        st.info(
            '**:blue[The same heights of bars in some graphs convey that some parts of that data are missing.]**')

    with colK2:
        st.info(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by you
            - X Axis represents the districts of selected state
            - Y Axis represents App Openings or Registered User Count according to the analysis type you select
            """
        )
        st.info(
            """
            Important Observations:
            - User can observe how App Openings and Registered User Count are happening in districts of a selected state
            - We can observe the leading district in a state
            - Based on these results Phonepe can provide offers to that particular district to attract more users
            """
        )

# USER DEVICE YEAR-WISE ANALYSIS
with tab3:
    st.write('#### :orange[Brand Share]')
    colL1, colL2, colL3 = st.columns(3)
    with colL1:
        year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='q')
    with colL2:
        state = st.selectbox('Please select the state', state_list, key='r')
    with colL3:
        quarter = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key='s')

    user_device = df_agg_user.loc[
        (df_agg_user['year'] == int(year)) & (df_agg_user['state'] == state) & (df_agg_user['quater'] == int(quarter))]

    treemap_fig = px.treemap(user_device, path=['state', 'brand_name'], values='percentage_share_of_brand',
                             hover_data=['year', 'quater'],
                             color='registered_user_count_per_brand', color_continuous_scale=px.colors.sequential.matter,
                             title='User Device Distribution in ' + state + ' in ' + str(year) + ' at ' + str(quarter))

    colM1, colM2 = st.columns([4, 1])
    with colM1:
        st.write('#### ', state.upper() + ' IN ' + year)
        st.plotly_chart(treemap_fig, use_container_width=True)
    with colM2:
        st.info(
            """
            Details of Tree Map:
            - Initially we select data by means of State and Year
            - Percentage of registered users is represented with Tree Map for each device brand
            - Each device brand are represented by rectangles of tree map
            """
        )
        st.info(
            """
            Important Observations:
            - The percentage of registered users are represented by size of the rectangles in tree map
            - User can observe the top leading brands in a particular state
            - PhonePe can provide discounts and suggestions for the upcoming and growing brands based on this analysis
            """
        )

    bar_fig = px.bar(user_device, x='brand_name', y='registered_user_count_per_brand',
                     color='registered_user_count_per_brand',
                     color_continuous_scale=px.colors.sequential.matter)
    with st.expander('See Bar Graph for the same data'):
        st.plotly_chart(bar_fig)

    fig = px.pie(user_device, values='registered_user_count_per_brand', names='brand_name', hole=0.5,
                 hover_data=['year'],
                 color_discrete_sequence=px.colors.sequential.matter_r)
    with st.expander('See Pie Chart for the same data'):
        st.plotly_chart(fig)

# OVERALL ANALYSIS
with tab4:
    years = df_agg_user_summary.groupby('year')
    years_list = df_agg_user_summary['year'].unique()
    years_table = years.sum()
    del years_table['quater']
    years_table['year'] = years_list

    colN1, colN2 = st.columns([7, 3])
    with colN1:
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
        fig.add_trace(
            go.Pie(labels=years_table['year'], values=years_table['registered_users'],marker_colors=px.colors.sequential.Aggrnyl, name='USERS'), 1, 1)
        fig.add_trace(go.Pie(labels=years_table['year'], values=years_table['app_opens'],marker_colors=px.colors.sequential.Aggrnyl, name='APP OPENS'), 1, 2)
        fig.update_traces(hole=0.6, hoverinfo='label+percent+name')
        fig.update_layout(title_text='USERS DATA (2018 TO 2022)',
                          annotations=[dict(text='USERS', x=0.18, y=0.5, font_size=20, showarrow=False),
                                       dict(text='APP OPENS', x=0.82, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig)

    with colN2:
        del years_table['index']
        st.markdown(years_table.style.hide(axis='index').to_html(), unsafe_allow_html=True)
        st.info(
            """
            Important Observation:
            -  We can see that the Registered Users and App opens are increasing year by year
            """
        )

# TOP 3 STATES DATA
st.write('## :green[TOP 3 STATES DATA]')
colO1, colO2 = st.columns(2)
with colO1:
    year = st.selectbox('Please select the year', ('2018', '2019', '2020', '2021', '2022'), key='t')
with colO2:
    quarter = st.selectbox('Please select the quarter', ('1', '2', '3', '4'), key='u')

user_summary = df_agg_user_summary.loc[(df_agg_user_summary['year'] == int(year)) & (df_agg_user_summary['quater'] == int(quarter))]

user_summary_r = user_summary.sort_values(by=['registered_users'], ascending = False)
user_summary_r_final = user_summary_r[['state','registered_users']][0:3]

agg_trans_summary = df_agg_trans.loc[(df_agg_trans['year'] == int(year)) & (df_agg_trans['quater'] == int(quarter))]
x = agg_trans_summary.groupby('state')

m = x.sum().sort_values(by='total_transaction_count', ascending=False)
n = x.sum().sort_values(by='total_amount', ascending=False)

final_ttc = m['total_transaction_count'][0:3]
final_ttc.to_csv('top_3_ttc.csv')

final_ta = n['total_amount'][0:3]
final_ta.to_csv('top_3_ta.csv')

colP1, colP2, colP3 = st.columns(3)
with colP1:
    st.markdown('#### :blue[Registered Users]')
    st.markdown(user_summary_r_final.style.hide(axis="index").to_html(), unsafe_allow_html=True)
with colP2:
    st.markdown('#### :blue[Total Transactions]')
    st.markdown(pd.read_csv('top_3_ttc.csv').style.hide(axis="index").to_html(), unsafe_allow_html=True)
with colP3:
    st.markdown('#### :blue[Total Amount]')
    st.markdown(pd.read_csv('top_3_ta.csv').style.hide(axis="index").to_html(), unsafe_allow_html=True)
