#streamlit page config
import streamlit as st
import pandas as pd
import numpy as np

#streamlit page config
st.set_page_config(
    page_title="DataGrow",
    page_icon=":earth_americas:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
#remove the hyperlink  
def hide_anchor_link():
    st.markdown("""
        <style>
        .css-15zrgzn {display: none}
        </style>
        """, unsafe_allow_html=True)


hide_anchor_link()

def crop_recommendation_model(city,season,nitrogen,phosphorus,potassium,ph):
    df2=pd.read_csv('Final_Clean_Dataset/crop.csv')
    df3=pd.read_csv('Final_Clean_Dataset/monthly_rainfall.csv')
    df2['city']=df2['city'].str.lower()
    df3['city']=df3['city'].str.lower()
    #drop all other city except the city given by the user
    df2=df2[df2['city']==city]
    df3=df3[df3['city']==city]
    #drop all other season except the season given by the user
    df2=df2[df2['season']==season]
    #if df season = kharif then use df1 kharif_min_temp, kharif_max_temp, kharif_rainfall
    if season=='Kharif':
        df2['min_temp']=df3['Kharif_min_temp']
        df2['max_temp']=df3['Kharif_max_temp']
        df2['rainfall_user']=df3['Kharif_rain']
    elif season=='Rabi':
        df2['min_temp']=df3['Rabi_min_temp']
        df2['max_temp']=df3['Rabi_max_temp']
        df2['rainfall_user']=df3['Rabi_rain']
    elif season=='Summer':
        df2['min_temp']=df3['Summer_min_temp']
        df2['max_temp']=df3['Summer_max_temp']
        df2['rainfall_user']=df3['Summer_rain']
    elif season=='Winter':
        df2['min_temp']=df3['Winter_min_temp']
        df2['max_temp']=df3['Winter_max_temp']
        df2['rainfall_user']=df3['Winter_rain']
    elif season=='Autumn':
        df2['min_temp']=df3['Autumn_min_temp']
        df2['max_temp']=df3['Autumn_max_temp']
        df2['rainfall_user']=df3['Autumn_rain']
    elif season=='Whole_Year':
        df2['min_temp']=df3['Annual_min']
        df2['max_temp']=df3['Annual_max']
        df2['rainfall_user']=df3['Annual']
    nitrogen=float(nitrogen)
    phosphorus=float(phosphorus)
    potassium=float(potassium)
    ph=float(ph)
    
    df2['n_rank']=abs(df2['N']-nitrogen)
    df2['p_rank']=abs(df2['P']-phosphorus)
    df2['k_rank']=abs(df2['K']-potassium)
    df2['ph_rank']=abs(df2['ph']-ph)
    df2['total_rank']=df2['n_rank']+df2['p_rank']+df2['k_rank']+df2['ph_rank']
    df2=df2.sort_values(by='total_rank')
    
    #rank should be 1 for the best crop and 2 for the second best crop and so on
    df2['rank']=df2['total_rank'].rank(method='first')
    #change the rank to integer
    df2['rank']=df2['rank'].astype(int)
    #remove the index column
    df2=df2.reset_index(drop=True)
    #change the column name
    
    df2=df2.rename(columns={'rank':'Rank','crop':'Crop','modal_price':'Expected Selling Price'})
    #make the first letter of the crop name capital
    df2['Crop']=df2['Crop'].str.title()
    #add a corresponding emoji to the crop name based on the crop
    df2['Crop']=df2['Crop'].str.replace('Rice','Rice 🌾')
    df2['Crop']=df2['Crop'].str.replace('Maize','Maize 🌽')
    df2['Crop']=df2['Crop'].str.replace('Cotton','Cotton 👨‍🌾')
    df2['Crop']=df2['Crop'].str.replace('Grapes','Grapes 🍇')
    df2['Crop']=df2['Crop'].str.replace('Orange','Orange 🍊')
    df2['Crop']=df2['Crop'].str.replace('Pomegranate','Pomegranate 🍐')
    df2['Crop']=df2['Crop'].str.replace('Banana','Banana 🍌')
    df2['Crop']=df2['Crop'].str.replace('Apple','Apple 🍎')
    df2['Crop']=df2['Crop'].str.replace('Papaya','Papaya 🍍')
    df2['Crop']=df2['Crop'].str.replace('Barley','Barley 🌾')
    df2['Crop']=df2['Crop'].str.replace('Wheat','Wheat 🌾')
    df2['Crop']=df2['Crop'].str.replace('Jute','Jute 🌾')
    df2['Crop']=df2['Crop'].str.replace('Arhar','Arhar 🌾🍲')
    df2['Crop']=df2['Crop'].str.replace('Mung','Mung 🌾🍲')
    df2=df2[['Rank','Crop','Expected Selling Price']]
    return df2




st.title("DataGrow")
st.markdown("## Making data grow and helping farmers grow")

#format this text to appear in yellow color
st.markdown("<span style='color:yellow'> Just Select you location and season and we will tell you the best crop to grow according to your soil and climate conditions </span>",unsafe_allow_html=True)


st.markdown("##### A data science project by ExeAI")

#streamlit dropdown button for selecting the state and then city from dataset
df = pd.read_csv("Final_Clean_Dataset/crop.csv")

#dictionary for state and corresponding cities by filtering cities from dataset
df1 = df.groupby('state')['city'].apply(list).to_dict()
df1 = {k: v for k, v in sorted(df1.items(), key=lambda item: item[0])}

state = st.selectbox('Select State', list(df1.keys()))
#make cities unique
df1[state] = list(set(df1[state]))
city = st.selectbox('Select City', df1[state])





#after selecting state and city, display the options to enter season

if state and city:
    season = st.selectbox('Select Season', df['season'].unique())
    if season:
        nitrogen=st.slider('Nitrogen', 10, 150, 75)
        phosphorus=st.slider('Phosphorus', 10, 150, 50)
        pottasium=st.slider('Pottasium', 10, 150, 75)
        ph=st.slider('ph', 4, 10, 7)

if st.button('Get Crop Recommendation',key='crp'):
    #replace _ with space in city name
    city=city.replace('_',' ')
    state=state.replace('_',' ')
    season=season.replace('_',' ')
    st.text("")
    st.text("")
    st.markdown("### You selected <span style='color:yellow'>{}</span> in <span style='color:yellow'>{}</span> in <span style='color:yellow'>{}</span> Season".format(city,state,season),unsafe_allow_html=True)
    #round the values of nitrogen, phosphorus, pottasium and ph
    nitrogen=round(nitrogen,2)
    phosphorus=round(phosphorus,2)
    pottasium=round(pottasium,2)
    ph=round(ph,2)
    st.text("")
    st.text("")
    st.markdown("### Your soil has <span style='color:yellow'>Nitrogen</span>: {}, <span style='color:yellow'>Phosphorus</span>: {}, <span style='color:yellow'>Pottasium</span>: {}, <span style='color:yellow'>ph</span>: {}".format(nitrogen,phosphorus,pottasium,ph),unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.markdown("### Your recommended crops are: ")
    city = city.replace(' ','_')
    state = state.replace(' ','_')
    season = season.replace(' ','_')
    city = city.lower()
    df4=crop_recommendation_model(city,season,nitrogen,phosphorus,pottasium,ph)
    
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df4)
    
    