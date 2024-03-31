#packages
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px

#mysql connection
mydb=sql.connect(host="localhost",user="root",password="root",database= "phonepe_pulse",port = "3306")
cursor=mydb.cursor()
#india_states
geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

#streamlit page
st.set_page_config(
    page_title="Phonepe Pulse",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="auto")

st.title("Phonepe Pulse Data Visualization and Exploration")

selected = option_menu(menu_title=None,options= ["Home", 'Explore Data','Insights'], 
          default_index=0,orientation='horizontal')

# function aggregated transaction based on count
def agg_trans_count(year,Quarter,trans_type):
    cursor.execute("select States, sum(Transaction_count) as Total_Transactions from aggregated_transaction where year =%s and quarter =%s and Transaction_type=%s group by States order by States ",(year,Quarter,trans_type))
    df1 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df1,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_Transactions',
                color_discrete_sequence=px.colors.sequential.speed)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and transaction_count")
    st.plotly_chart(fig,use_container_width=True)

# function aggregated transaction based on amount
def agg_trans_amnt(year,Quarter,trans_type):
    cursor.execute("select States, sum(Transaction_amount) as Total_amount from aggregated_transaction where year =%s and quarter =%s and Transaction_type=%s group by States order by States",(year,Quarter,trans_type))
    df2 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df2,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_amount',
                color_discrete_sequence=px.colors.sequential.Sunsetdark)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and transaction_amount")
    st.plotly_chart(fig,use_container_width=True)

#function aggregated user based on count
def agg_user_count(year,Quarter):
    cursor.execute("select States, sum(Transaction_count) as Total_Transactions from aggregated_user where year =%s and quarter =%s  group by States order by States ",(year,Quarter))
    df3 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df3,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_Transactions',
                color_discrete_sequence=px.colors.sequential.Viridis)          
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and transaction_count")
    st.plotly_chart(fig,use_container_width=True)  

#function aggregated user based on percentage
def agg_user_percentage(year,Quarter):
    cursor.execute("select States, avg(Percentage)*100 as Percentage from aggregated_user where year =%s and quarter =%s  group by States order by States ",(year,Quarter))
    df3 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df3,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Percentage',
                color_discrete_sequence=px.colors.sequential.Viridis_r)          
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and percentage")
    st.plotly_chart(fig,use_container_width=True)  

#function map transaction based on amount
def map_trans_amount(year,Quarter):
    cursor.execute("select States, sum(Transaction_amount) as Total_amount from map_transaction where year =%s and quarter =%s group by States order by States",(year,Quarter))
    df4 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df4,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_amount',
                color_continuous_scale='sunset')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and transaction_amount")
    st.plotly_chart(fig,use_container_width=True)

#function map transaction based on count
def map_trans_count(year,Quarter):
    cursor.execute("select States, sum(Transaction_count) as Total_count from map_transaction where year =%s and quarter =%s group by States order by States",(year,Quarter))
    df4 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(df4,geojson=geojson,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_count',
                color_discrete_sequence=px.colors.sequential.Purp)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=" Transactions based on states and transaction_count")
    st.plotly_chart(fig,use_container_width=True)

#function map user states
def map_user(states):
    st.write("### :violet[ Transactions based on State district wise,registered users and appopens:]")
    cursor.execute("select States,Districts,sum(RegisteredUser) as registeredUsers from map_user where States =%s group by States,Districts",(states,))
    dff = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.choropleth(
        dff,
        geojson=geojson,
        featureidkey='properties.ST_NM',
        locations='States',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text="States")
    st.plotly_chart(fig,use_container_width=True)

#function map user based on registered users
def map_user_reg(states):
    cursor.execute("select States,Districts,sum(RegisteredUser) as registeredUsers from map_user where States =%s group by Districts order by registeredUsers desc",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.bar(df,
                     title='State_district vs Registered users',
                     x="Districts",
                     y="registeredUsers",
                     orientation='v',
                     color='registeredUsers',
                     color_discrete_sequence=px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig,use_container_width=True)

#function map user based on appopens
def map_user_appopens(states):
    cursor.execute("select States,Districts,sum(AppOpens) as AppOpens from map_user where States =%s group by Districts order by AppOpens desc",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.bar(df,
                     title='State_district vs AppOpens ',
                     x="Districts",
                     y="AppOpens",
                     orientation='v',
                     color='AppOpens',
                     color_discrete_sequence=px.colors.sequential.Mint)
    st.plotly_chart(fig,use_container_width=True)

#function top transaction based on district amount
def top_tran_dist(states):
    cursor.execute("select States,District,sum(District_transaction_amount) as Transaction_amount from top_transaction_district where States =%s group by District",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='Transaction_amount',
                             names='District',
                             title='State district wise vs amount',
                             color_discrete_sequence=px.colors.sequential.Oryel,
                             hover_data=['Transaction_amount'],
                             labels={'Transaction_amount':'Total amount'})
    st.plotly_chart(fig,use_container_width=True) 

#function top transaction based on district count
def top_tran_distcount(states):
    cursor.execute("select States,District,sum(District_transaction_count) as Transaction_count from top_transaction_district where States =%s group by District",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='Transaction_count',
                             names='District',
                             title='State district wise vs count',
                             color_discrete_sequence=px.colors.sequential.OrRd_r,
                             hover_data=['Transaction_count'],
                             labels={'Transaction_count':'Count'})
    st.plotly_chart(fig,use_container_width=True)

#function top transaction based on pincodes amount
def top_tran_pin(states):
    cursor.execute("select States,Pincodes,sum(Pincode_transaction_amount) as Transaction_amount from top_transaction_pincode where States =%s group by Pincodes",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='Transaction_amount',
                             names='Pincodes',
                             title='State pincode wise vs amount',
                             color_discrete_sequence=px.colors.sequential.haline,
                             hover_data=['Transaction_amount'],
                             labels={'Transaction_amount':'Total amount'})
    st.plotly_chart(fig,use_container_width=True) 

#function top transaction based on pincodes count
def top_tran_pincount(states):
    cursor.execute("select States,Pincodes,sum(Pincode_transaction_count) as Transaction_count from top_transaction_pincode where States =%s group by Pincodes",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='Transaction_count',
                             names='Pincodes',
                             title='State pincode wise vs count',
                             color_discrete_sequence=px.colors.sequential.haline_r,
                             hover_data=['Transaction_count'],
                             labels={'Transaction_count':'Count'})
    st.plotly_chart(fig,use_container_width=True) 

#function top user district
def top_user_dist(states):
    cursor.execute("select States,District,sum(District_registereduser) as registereduser from top_user_district where States =%s group by District",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='registereduser',
                             names='District',
                             title='State district wise vs registereduser',
                             color_discrete_sequence=px.colors.sequential.Reds_r,
                             hover_data=['registereduser'],
                             labels={'registereduser':'registereduser'})
    st.plotly_chart(fig,use_container_width=True) 

#function top user pincode
def top_user_pin(states):
    cursor.execute("select States,Pincodes,sum(Pincode_registereduser) as registereduser from top_user_pincode where States =%s group by Pincodes",(states,))
    df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(df, values='registereduser',
                             names='Pincodes',
                             title='State pincode wise vs registereduser',
                             color_discrete_sequence=px.colors.sequential.Reds,
                             hover_data=['registereduser'],
                             labels={'registereduser':'registereduser'})
    st.plotly_chart(fig,use_container_width=True) 

#function insights query
def query1():
    cursor.execute("SELECT Brands,AVG(Percentage)*100 as Percentage From aggregated_user Group by Brands Order by Percentage DESC LIMIT 10 ")
    q1 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :blue[ Top 10 Brands based on percentage and count:]")
    fig = px.bar(q1,
                     title='Top 10 Brands based on percentage',
                     x="Brands",
                     y="Percentage",
                     orientation='v',
                     color='Brands',
                     color_discrete_sequence=px.colors.sequential.YlGnBu)
    st.plotly_chart(fig)
    
    cursor.execute("SELECT Brands,SUM(Transaction_count) as Total_count From aggregated_user Group by Brands Order by Total_count DESC LIMIT 10 ")
    q1_2 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig = px.pie(q1_2, values='Total_count',
                             names='Brands',
                             title='Top 10 Brands based on count',
                             color_discrete_sequence=px.colors.sequential.YlGnBu_r,
                             hover_data=['Total_count'],
                             labels={'Total_count':'Total_count'})
    st.plotly_chart(fig,use_container_width=True)

def query2():
    cursor.execute("SELECT Brands,AVG(Percentage)*100 as Percentage From aggregated_user Group by Brands Order by Percentage LIMIT 10 ")
    q2 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :orange[ Least 10 Brands based on percentage and count:]")
    fig = px.bar(q2,
                     title='Least 10 Brands based on percentage ',
                     x="Brands",
                     y="Percentage",
                     orientation='v',
                     color='Brands',
                     color_discrete_sequence=px.colors.sequential.Inferno)
    st.plotly_chart(fig)
    
    cursor.execute("SELECT Brands,SUM(Transaction_count) as Total_count From aggregated_user Group by Brands Order by Total_count LIMIT 10 ")
    q2p = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    fig1 = px.pie(q2p, values='Total_count',
                             names='Brands',
                             title='Least 10 Brands based on count',
                             color_discrete_sequence=px.colors.sequential.Inferno_r,
                             hover_data=['Total_count'],
                             labels={'Total_count':'Total_count'})
    st.plotly_chart(fig1,use_container_width=True)

def query3():
    st.write("### :violet[ Top 10 States based on amount and count:]")
    col1,col2=st.columns(2)
    with col1:
        cursor.execute("SELECT States,SUM(Transaction_amount) AS Transaction_amount FROM map_transaction GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10 ")
        q3 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q3, values='Transaction_amount',
                                names='States',
                                title='Top 10 States based on  amount',
                                color_discrete_sequence=px.colors.sequential.Emrld_r,
                                hover_data=['Transaction_amount'],
                                labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT States,SUM(Transaction_count) AS Transaction_count FROM map_transaction GROUP BY States ORDER BY Transaction_count DESC LIMIT 10 ")
        q3_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q3_, values='Transaction_count',
                                names='States',
                                title='Top 10 States based  on count',
                                color_discrete_sequence=px.colors.sequential.Magenta_r,
                                hover_data=['Transaction_count'],
                                labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

def query4():
    st.write("### :grey[ Least 10 States based on amount and count:]")
    col1,col2=st.columns(2)
    with col1:
        cursor.execute("SELECT States,SUM(Transaction_amount) AS Transaction_amount FROM map_transaction GROUP BY States ORDER BY Transaction_amount  LIMIT 10 ")
        q4 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q4, values='Transaction_amount',
                                names='States',
                                title='Least 10 States based on  amount',
                                color_discrete_sequence=px.colors.sequential.gray,
                                hover_data=['Transaction_amount'],
                                labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT States,SUM(Transaction_count) AS Transaction_count FROM map_transaction GROUP BY States ORDER BY Transaction_count  LIMIT 10 ")
        q4_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q4_, values='Transaction_count',
                                names='States',
                                title='Least 10 States based  on count',
                                color_discrete_sequence=px.colors.sequential.Greys,
                                hover_data=['Transaction_count'],
                                labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

def query5(states):
    st.write("### :blue[ Top 5 districts for each state based on amount,count and registered users:]")
    col1,col2,col3=st.columns(3)
    with col1:
        cursor.execute("SELECT District, SUM(District_transaction_amount) AS Total_amount FROM top_transaction_district WHERE States = %s GROUP BY District ORDER BY Total_amount DESC LIMIT 5",(states,))
        q5 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q5, values='Total_amount',
                                    names='District',
                                    title='Top 5 districts for each state based on amount',
                                    color_discrete_sequence=px.colors.sequential.Rainbow,
                                    hover_data=['Total_amount'],
                                    labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT District, SUM(District_transaction_count) AS Total_count FROM top_transaction_district WHERE States = %s GROUP BY District ORDER BY Total_count DESC LIMIT 5",(states,))
        q5_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q5_, values='Total_count',
                                    names='District',
                                    title='Top 5 districts for each state based on count',
                                    color_discrete_sequence=px.colors.sequential.Plotly3,
                                    hover_data=['Total_count'],
                                    labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

    with col3:
        cursor.execute("SELECT District, SUM(District_registereduser) AS Total_registeredusers FROM top_user_district WHERE States = %s GROUP BY District ORDER BY Total_registeredusers DESC LIMIT 5",(states,))
        q_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q_, values='Total_registeredusers',
                                    names='District',
                                    title='Top 5 districts for each state based on registeredusers',
                                    color_discrete_sequence=px.colors.sequential.ice,
                                    hover_data=['Total_registeredusers'],
                                    labels={'Total_registeredusers':'Total_registeredusers'})
        st.plotly_chart(fig,use_container_width=True)

def query6(states):
    st.write("### :orange[ Least 5 districts for each state based on amount,count and registered users:]")
    col1,col2,col3=st.columns(3)
    with col1:
        cursor.execute("SELECT District, SUM(District_transaction_amount) AS Total_amount FROM top_transaction_district WHERE States = %s GROUP BY District ORDER BY Total_amount  LIMIT 5",(states,))
        q6 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q6, values='Total_amount',
                                    names='District',
                                    title='Least 5 districts for each state based on amount',
                                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                                    hover_data=['Total_amount'],
                                    labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT District, SUM(District_transaction_count) AS Total_count FROM top_transaction_district WHERE States = %s GROUP BY District ORDER BY Total_count LIMIT 5",(states,))
        q6_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q6_, values='Total_count',
                                    names='District',
                                    title='Least 5 districts for each state based on count',
                                    color_discrete_sequence=px.colors.sequential.Plotly3_r,
                                    hover_data=['Total_count'],
                                    labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

    with col3:
        cursor.execute("SELECT District, SUM(District_registereduser) AS Total_registeredusers FROM top_user_district WHERE States = %s GROUP BY District ORDER BY Total_registeredusers LIMIT 5",(states,))
        ds = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(ds, values='Total_registeredusers',
                                    names='District',
                                    title='Least 5 districts for each state based on registeredusers',
                                    color_discrete_sequence=px.colors.sequential.ice_r,
                                    hover_data=['Total_registeredusers'],
                                    labels={'Total_registeredusers':'Total_registeredusers'})
        st.plotly_chart(fig,use_container_width=True)

def query7(states):
    st.write("### :red[ Top 5 pincodes for each state based on amount,count and registered users:]")
    col1,col2,col3=st.columns(3)
    with col1:
        cursor.execute("SELECT Pincodes, SUM(Pincode_transaction_amount) AS Total_amount FROM top_transaction_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_amount DESC LIMIT 5",(states,))
        q7 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q7, values='Total_amount',
                                    names='Pincodes',
                                    title='Top 5 pincodes for each state based on amount',
                                    color_discrete_sequence=px.colors.sequential.Pinkyl,
                                    hover_data=['Total_amount'],
                                    labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT Pincodes, SUM(Pincode_transaction_count) AS Total_count FROM top_transaction_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_count DESC LIMIT 5",(states,))
        q7_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q7_, values='Total_count',
                                    names='Pincodes',
                                    title='Top 5 pincodes for each state based on count',
                                    color_discrete_sequence=px.colors.sequential.Magma,
                                    hover_data=['Total_count'],
                                    labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

    with col3:
        cursor.execute("SELECT Pincodes, SUM(Pincode_registereduser) AS Total_registeredusers FROM top_user_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_registeredusers DESC LIMIT 5",(states,))
        q = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q, values='Total_registeredusers',
                                    names='Pincodes',
                                    title='Top 5 pincodes for each state based on registeredusers',
                                    color_discrete_sequence=px.colors.sequential.Peach,
                                    hover_data=['Total_registeredusers'],
                                    labels={'Total_registeredusers':'Total_registeredusers'})
        st.plotly_chart(fig,use_container_width=True)

def query8(states):
    st.write("### :orange[ Least 5 pincodes for each state based on amount,count and registered users:]")
    col1,col2,col3=st.columns(3)
    with col1:
        cursor.execute("SELECT Pincodes, SUM(Pincode_transaction_amount) AS Total_amount FROM top_transaction_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_amount  LIMIT 5",(states,))
        q8 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q8, values='Total_amount',
                                    names='Pincodes',
                                    title='Least 5 pincodes for each state based on amount',
                                    color_discrete_sequence=px.colors.sequential.Pinkyl_r,
                                    hover_data=['Total_amount'],
                                    labels={'Transaction_amount':'Transaction_amount'})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("SELECT Pincodes, SUM(Pincode_transaction_count) AS Total_count FROM top_transaction_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_count LIMIT 5",(states,))
        q8_ = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q8_, values='Total_count',
                                    names='Pincodes',
                                    title='Least 5 pincodes for each state based on count',
                                    color_discrete_sequence=px.colors.sequential.Magma_r,
                                    hover_data=['Total_count'],
                                    labels={'Transaction_count':'Transaction_count'})
        st.plotly_chart(fig,use_container_width=True)

    with col3:
        cursor.execute("SELECT Pincodes, SUM(Pincode_registereduser) AS Total_registeredusers FROM top_user_pincode WHERE States = %s GROUP BY Pincodes ORDER BY Total_registeredusers LIMIT 5",(states,))
        c8 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(c8, values='Total_registeredusers',
                                    names='Pincodes',
                                    title='Least 5 pincodes for each state based on registeredusers',
                                    color_discrete_sequence=px.colors.sequential.Peach_r,
                                    hover_data=['Total_registeredusers'],
                                    labels={'Total_registeredusers':'Total_registeredusers'})
        st.plotly_chart(fig,use_container_width=True)
def query9():
    st.write("### :blue[ Highest Transaction type based on amount and count:]")
    col1,col2=st.columns(2)
    with col1:
        cursor.execute("SELECT Transaction_type,SUM(Transaction_amount) As Total_amount FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Total_amount DESC ")
        q9 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(q9, values='Total_amount',
                                    names='Transaction_type',
                                    title='Highest Transaction type based on amount',
                                    color_discrete_sequence=px.colors.sequential.Teal,
                                    hover_data=['Total_amount'],
                                    labels={'Total_amount':'Total_amount'},hole=0.5)
        st.plotly_chart(fig,use_container_width=True)
                                       
                                            
    with col2:
        cursor.execute("SELECT Transaction_type,SUM(Transaction_count) As Total_count FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Total_count DESC ")
        c9 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        fig = px.pie(c9, values='Total_count',
                                    names='Transaction_type',
                                    title='Highest Transaction type based on count',
                                    color_discrete_sequence=px.colors.sequential.Teal_r,
                                    hover_data=['Total_count'],
                                    labels={'Total_count':'Total_count'},hole=0.5)
        st.plotly_chart(fig,use_container_width=True)
        

def query10():
        st.write("### :black[ Top 30 districts based on registered users and appopens:]")
        cursor.execute("SELECT Districts,SUM(RegisteredUser) As registered_users FROM map_user GROUP BY Districts ORDER BY registered_users DESC LIMIT 30 ")
        q10 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        q10['registered_users'] = pd.to_numeric(q10['registered_users'])
        fig = px.scatter(q10, x='Districts',y='registered_users',
                                title='Top 30 districts based on registered users',
                                color='Districts',size='registered_users',
                                    color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(fig,use_container_width=True)
                                            
    
        cursor.execute("SELECT Districts,SUM(AppOpens) As AppOpens FROM map_user GROUP BY Districts ORDER BY AppOpens DESC LIMIT 30 ")
        c9 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        c9['AppOpens'] = pd.to_numeric(c9['AppOpens'])
        fig = px.scatter(c9, x='Districts',y='AppOpens',
                                title='Top 30 districts based on app opens',
                                color='Districts',size='AppOpens',
                                    color_discrete_sequence=px.colors.sequential.Cividis)
        st.plotly_chart(fig,use_container_width=True)

#streamlit page
if selected=="Home":
    col1,col2 = st.columns(2)
    with col1:
        st.image(r"c:\Users\raji\guvi\logo.PNG")
        st.subheader("PhonePe is an Indian multinational digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016."

                       "The PhonePe app is accessible in 11 Indian languages. It enables users to perform various financial transactions such as sending and receiving money, recharging mobile and DTH services, topping up data cards, making utility payments, conducting in-store payments.")
    with col2:
        st.video(r"c:\Users\raji\guvi\upi.mp4")
    col3,col4=st.columns(2)
    with col3:
        st.video(r"c:\Users\raji\guvi\pulse-video.mp4")
    with col4:
        st.subheader("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-art payments infrastructure built as Public Goods championed by the central bank and the government."
                     "PhonePe Pulse visualization provides a comprehensive overview of various metrics and trends related to transactions and user activity on the PhonePe platform.")

        
    
if selected=="Explore Data":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        options=st.radio("Analysis",["Transaction","User"])
        if options=="Transaction":
            col1,col2,col3=st.columns(3)
            st.write("### :green[ Transactions based on states transaction_amount and transaction_count :]")
            with col1:
                year=st.selectbox("Select year",(2018,2019,2020,2021,2022,2023))
            with col2:
                Quarter=st.selectbox("Select Quarter",(1,2,3,4))
            with col3:
                trans_type=st.selectbox("Select type",("Recharge & bill payments","Peer-to-peer payments","Merchant payments","Financial Services",
                                            "Others"))
            col4,col5=st.columns(2)
            with col4:
                agg_trans_count(year,Quarter,trans_type)
                
            with col5:
                agg_trans_amnt(year,Quarter,trans_type)

        if options=="User":
            col1,col2=st.columns(2)
            with col1:
                year=st.selectbox("Select year",(2018,2019,2020,2021,2022,2023), key="year_selectbox")
            with col2:
                Quarter=st.selectbox("Select Quarter",(1,2,3,4), key="quarter_selectbox")
            st.write("### :blue[ Transactions based on states  transaction_count  and percentage:]")
            col3,col4=st.columns(2)
            with col3:
                agg_user_count(year,Quarter) 
            with col4:
                agg_user_percentage(year,Quarter)  

    with tab2:
        options=st.radio("Analysis",["Transaction","User"],key="tab2")
        if options=="Transaction":
            col1,col2=st.columns(2)
            st.write("### :blue[ Transactions based on states transaction_amount and transaction_count :]")
            with col1:
                year=st.selectbox("Select year",(2018,2019,2020,2021,2022,2023), key="year_map")
            with col2:
                Quarter=st.selectbox("Select Quarter",(1,2,3,4),key="map_q")
            col3,col4=st.columns(2)
            with col3:
                map_trans_amount(year,Quarter)
            with col4:
                map_trans_count(year,Quarter)

        if options=="User":
            states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"))

            
            map_user(states)
            map_user_reg(states)
            map_user_appopens(states)

    with tab3:
        options=st.radio("Analysis",["Transaction","User"],key="tab3")
        states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),key='state')
        
        if options=="Transaction":
            st.write("### :orange[ Transactions based on State district wise amount and count:]")
            col1,col2=st.columns(2)
            with col1:
                top_tran_dist(states)
            with col2:
                top_tran_distcount(states)
            st.write("### :blue[ Transactions based on State pincode wise amount and count:]")    
            col3,col4=st.columns(2)
            with col3:
                top_tran_pin(states)
            with col4:
                top_tran_pincount(states)

        if options=="User":
            st.write("### :red[ Transactions based on State district wise and pincode wise registered users:]")
            col1,col2=st.columns(2)
            with col1:
                top_user_dist(states)
            with col2:
                top_user_pin(states)

if selected=="Insights":
    Insights=st.selectbox("Select Insights",("Top 10 Brands","Least 10 Brands","Top 10 States ","Least 10 States",
                                "Top 5 Districts for each state","Least 5 Districts for each state",
                                "Top 5 Pincodes for each state","Least 5 Pincodes for each state",
                                "Highest Transaction type","Top 30 Districts"))
    if Insights=="Top 10 Brands":
        query1()
    
    if Insights=="Least 10 Brands":
        query2()

    if Insights=="Top 10 States ":
        query3()

    if Insights=="Least 10 States":
        query4()

    if Insights=="Top 5 Districts for each state":
        states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),key='state22')
        query5(states)

    if Insights=="Least 5 Districts for each state":
        states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),key='query')
        query6(states)
    
    if Insights=="Top 5 Pincodes for each state":
        states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),key='35')
        query7(states)

    if Insights=="Least 5 Pincodes for each state":
        states=st.selectbox("Select state",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Chandigarh","Chhattisgarh",
                                                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
                                                "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
                                                "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                                "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),key='insights')
        query8(states)

    if Insights=="Highest Transaction type":
        query9()

    if Insights=="Top 30 Districts":
        query10()    
            