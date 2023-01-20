import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#page layout
st.set_page_config(layout='wide',page_title="StartUp Analysis")

df=pd.read_csv("startup data")
#converting to date time object
df['Date']=pd.to_datetime(df['Date'],errors="coerce")
#forming new column by the name year where only year values will be displayed
df["Year"]=df["Date"].dt.year
#forming new column by the name month where only month values will be displayed
df["Month"]=df["Date"].dt.month

#forming function for overall analysis
def load_overall_analysis():
    st.title("Overal  Analysis")
    column1,column2,column3,column4= st.columns(4)
    with column1:
        #showing total investment
        total_investment=df['Amount in Crore Rs.'].sum()
        st.metric("Total Investment",str(total_investment)+ " Cr")
    with column2:
        #Maximum investment in one single Startup
        max_investment=round(df.groupby("Startup")['Amount in Crore Rs.'].max().sort_values(ascending=False).head(1).values[0])
        startup_name=df.groupby("Startup")['Amount in Crore Rs.'].max().sort_values(ascending=False).head(1).index[0]
        st.metric("Maximum investment in a single StartUp",str(max_investment)+ " Cr"+ " "+(startup_name))
    with column3:
        #Average investment in Indian Startups
        avg_investment=round(df.groupby("Startup")['Amount in Crore Rs.'].sum().mean())
        st.metric("Average Investment",str(avg_investment) + " Cr")
    with column4:
        #Total number of startup funded
        total_funded_startups=df["Startup"].nunique()
        st.metric("Total number of StartUps",total_funded_startups)

 #MOM analysis

    st.subheader("Month On Month Analysis-Amount of Funding")
    temp_df1 = df.groupby(['Year', 'Month'])["Amount in Crore Rs."].sum().reset_index()
    temp_df1['Joint column'] = temp_df1['Year'].astype(str) + "-" + temp_df1['Month'].astype(str)
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df1['Joint column'],temp_df1["Amount in Crore Rs."] )
    st.pyplot(fig5)


    st.subheader("Month On Month Analysis-Number of StartUps")
    temp_df2 = df.groupby(['Year', 'Month'])["Startup"].count().reset_index()
    temp_df2['Joint column'] = temp_df2['Year'].astype(str) + "-" + temp_df2['Month'].astype(str)
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df2['Joint column'], temp_df2["Startup"])
    st.pyplot(fig6)


#forming a function for investors
def load_investor_details(investor):
    st.title(investor)
    #5 Recent investments
    rec5_investments=df[df["Investor"].str.contains('investor')].head()[
        ['Date', 'Startup', 'Vertical', 'City', 'Amount in Crore Rs.']]
    st.subheader('5 Recent Investments')
    st.dataframe(rec5_investments)

    #5 Top investments by a investor
    top5_investments=df[df["Investor"].str.contains(investor)].groupby('Startup')['Amount in Crore Rs.'].sum().sort_values(ascending=False).head(5)
    st.subheader('Top 5 Investments')
    st.dataframe(top5_investments)
    column1, column2 = st.columns(2)
    with column1:
        # ploting bar graph of above investments
        st.subheader("Top 5 Investments through Graph")
        fig,ax=plt.subplots()
        ax.bar(top5_investments.index,top5_investments.values)
        st.pyplot(fig)
    with column2:
        #sector wise investment
        st.subheader("Sectors invested in")
        sectorwise_investments=df[df["Investor"].str.contains(investor)].groupby('Vertical')['Amount in Crore Rs.'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(sectorwise_investments,labels=sectorwise_investments.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    column1, column2 = st.columns(2)
    with column1:
        #stages of investment
        st.subheader("Stages of Investment")
        stages_of_investments = df[df["Investor"].str.contains(investor)].groupby('Investment')['Amount in Crore Rs.'].sum()
        fig3, ax3 = plt.subplots()
        ax3.pie(stages_of_investments, labels=stages_of_investments.index, autopct="%0.01f%%")
        st.pyplot(fig3)
    with column2:
        #Investment in different cities
        st.subheader("Investment in different Cities")
        cities_investments = df[df["Investor"].str.contains(investor)].groupby('City')[
            'Amount in Crore Rs.'].sum()
        fig3, ax3 = plt.subplots()
        ax3.pie(cities_investments, labels=cities_investments.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    column1,column2= st.columns(2)
    with column1:
        #year on year investment
        st.subheader("YOY Investment")
        yoy_investments = df[df["Investor"].str.contains(investor)].groupby('Year')[
            'Amount in Crore Rs.'].sum()
        fig4, ax4 = plt.subplots()
        ax4.plot(yoy_investments.index,yoy_investments.values)
        st.pyplot(fig4)

st.title("Startup Dashboard")
st.sidebar.title("Startup Funding Analysis")
option =st.sidebar.selectbox("Select One",["Overall Analysis","StartUp","Investor"])
if option == "Overall Analysis":
    button0=st.sidebar.button("Show Overall Analysis")
    if button0:
        load_overall_analysis()
elif option == "StartUp":
    st.sidebar.selectbox("Select StartUp",sorted(list(df['Startup'].unique())))
    st.title("StartUp Analysis")
    button1=st.sidebar.button("Find StartUp Details")
else:
    selected_investor=st.sidebar.selectbox("Select Investor",set(df["Investor"].str.split(',').sum()))
    st.title("Investor Analysis")
    button2 = st.sidebar.button("Find Investor Details")
    if button2:
        load_investor_details(selected_investor)
