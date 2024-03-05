# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("Bike_Share_daily.csv")
hour_df = pd.read_csv("Bike_Share_hourly.csv")

def create_musim_df(df):
    musim_df = day_df.groupby(by='season').agg({
        'cnt': ['max', 'min', 'mean', 'sum']}).reset_index()
    return musim_df

def create_workingday_df(df):
    workingday_df = day_df.groupby(by='workingday').agg({
        'cnt': ['mean']}).astype(int).reset_index()
    return workingday_df

def create_weekly_df(df):
    weekly_df = day_df.groupby(by='weekday').agg({'cnt': ['mean']})
    weekly_df['cnt'].astype(int).reset_index()
    return weekly_df

def create_daily_df(df):
    daily_df = day_df.groupby(by='dteday').agg({'cnt': ['mean']})
    daily_df['cnt'].astype(int).reset_index()
    return daily_df

def create_yearly_df(df):
    year_df = day_df.groupby(by=['yr', 'mnth']).agg({
        'cnt': ['sum']}).reset_index()
    return year_df

# change data type from 'object' to 'datetime'
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# sidebar 
st.sidebar.markdown("**Bike Sharing Dashboard**")

with st.sidebar:
    # Add Logo
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Periode',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date])
    
main_day = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# Df
per_musim_df = create_musim_df(main_day)
per_daytype_df = create_workingday_df(main_day)
per_week_df = create_weekly_df(main_day)
per_day_df = create_daily_df(main_day)
per_year_df = create_yearly_df(main_day)

# Dashboard
st.header('Dashboard Peminjaman Sepeda')

col1, col2 = st.columns(2)

with col1:
    total_df = per_day_df['cnt'].sum()
    st.metric('Total Peminjam', value= total_df.astype(int))

# Visualisasi Data
# 1. Bagaimana peran musim (season) terhadap jumlah penyewaan sepeda?
    st.subheader('Tren Rata-rata Peminjaman Sepeda Per Season')

    # Grouping by season and aggregating the mean of 'cnt'
    by_season_df = day_df.groupby(by='season').agg({'cnt': 'mean'})

    # Plotting
    st.bar_chart(by_season_df)

    # Display the season with the highest sum
    max_season = by_season_df['cnt'].idxmax()
    st.write(f"Musim dengan jumlah peminjaman tertinggi adalah: {max_season}")

# 2. Bagaimana pengaruh jenis hari (working day atau holiday) terhadap sewa sepeda harian?
    st.subheader('Rata-rata Peminjaman Hari Libur vs Hari Kerja')
    
    # Grouping by workingday and aggregating the mean of 'cnt'
    by_workingday_df = day_df.groupby(by='workingday').agg({'cnt': 'mean'})

    # Plotting 
    st.bar_chart(by_workingday_df)

    # additional 
    st.write("Orang-orang lebih banyak melakukan peminjaman sepeda saat hari kerja")

    
