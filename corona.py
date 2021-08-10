import pandas as pd 
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')

df_total = df.groupby("Country", as_index=False).agg(
    {
        "Confirmed" : "max",
        "Deaths" : "max",
        "Recovered" : "max"
    }
)
df_top10 = df_total.nlargest(10,"Confirmed")
top10_countries_conf = df_top10['Country'].tolist()
top10_confirmed = df_top10['Confirmed'].tolist()

df_top10 = df_total.nlargest(10,"Recovered")
top10_countries_rec = df_top10['Country'].tolist()
top10_recovered = df_top10['Recovered'].tolist()

df_top10 = df_total.nlargest(10,"Deaths")
top10_countries_deaths = df_top10['Country'].tolist()
top10_deaths = df_top10['Deaths'].tolist()

st.title('COVID-19 Analysis')
st.write("Current Covid-19 scenario in the world")

update = df.Date.tail(1).tolist()

st.sidebar.markdown(f"Last Updated on: {update[0]}")

st.sidebar.markdown(f'''
        <h1 align='center'> WorldWide Data</h1><br>
        <div style='width:18rem;background-color:yellow;'>
        <center>
        <h3>Total Cases:</h3>
        <p>{sum(df_total['Confirmed'])}</p>
        </center>
        
    </div>''',unsafe_allow_html=True)

st.sidebar.markdown(f'''<div style='width:18rem;background-color:PowderBlue;'>
        <center>
        <h3>Recovered Cases:</h3>
        <p>{sum(df_total['Recovered'])}</p>
        </center>
    </div>''',unsafe_allow_html=True)

st.sidebar.markdown(f'''<div style='width:18rem;background-color:BlanchedAlmond;'>
        <center>
        <h3>Deaths:</h3>
        <p>{sum(df_total['Deaths'])}</p>
        </center>
    </div>''',unsafe_allow_html=True)

pages = st.sidebar.selectbox(
    "Select your page:",
    ['Homepage','Country-Wise','Data Visualisation']
)
def show_fig(choice):
    fig = px.line(data_frame=df,x='Date',y=choice,color='Country')
    st.plotly_chart(fig,use_container_width=True)

def country_data(co):
        df_2 = df[df['Country']==co]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_2['Date'], y=df_2['Confirmed'],
                    mode='lines',
                    name='Confirmed'))
        fig2.add_trace(go.Scatter(x=df_2['Date'], y=df_2['Recovered'],
                    mode='lines+markers',
                    name='Recovered'))
        fig2.add_trace(go.Scatter(x=df_2['Date'], y=df_2['Deaths'],
                    mode='markers', name='Deaths'))

        st.plotly_chart(fig2)
def data_visual(ch,co):        
        new_df = df[df['Country'].isin(co)]
        fig = px.bar(new_df, x='Country',y =ch,color='Country',
                   animation_frame = 'Date', animation_group='Country')
        st.plotly_chart(fig,use_container_width=True)


if pages=='Homepage':
    ch = st.selectbox(
    "What do you want to see:",
    ['----','Confirmed','Recovered','Deaths'])
    
    if ch=='Confirmed':
        show_fig(ch)
    elif ch=='Recovered':
        show_fig(ch)
    elif ch=='Deaths':
        show_fig(ch)

elif pages=='Country-Wise':
    country = st.selectbox('Select your Country',
          df['Country'].unique())
    country_data(country)
    
elif pages=='Data Visualisation':
    choice=st.selectbox(
        "Top 10 Country's Graphs by:",
        ['Confirmed','Recovered','Deaths'])
    if choice=='Confirmed':
        co=top10_countries_conf
    elif choice=='Recovered':
        co=top10_countries_rec
    else:
        co=top10_countries_deaths
    data_visual(choice,co)