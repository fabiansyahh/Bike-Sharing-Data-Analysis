import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
biker_hour = pd.read_csv("hour.csv")

# Preprocessing
biker_hour['temp'] *= 41
biker_hour['season'] = biker_hour['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
biker_hour ['season'] = biker_hour.season.astype('category')
biker_hour.rename(columns={'season' : 'Season', 'temp' : 'Temperature', 'cnt' : 'Total Renter'}, inplace=True)
biker_hour['Temperature'] = biker_hour['Temperature'].round()

# Grouping by Season and Temperature
seasons = biker_hour.groupby('Season')[['Total Renter']].sum().reset_index()
bins = np.arange(biker_hour['Temperature'].min(), biker_hour['Temperature'].max() + 1, 5)
biker_hour['Temperature_bin'] = pd.cut(biker_hour['Temperature'], bins=bins)
renter_by_temp = biker_hour.groupby('Temperature_bin')['Total Renter'].sum()

# Streamlit app
st.title('Data Analysis Project')
st.header("Topik Analisis Data")
st.write("1. Apakah ada hubungan musim dengan penyewa sepeda secara keseluruhan setiap jam, apakah musim dapat mempengaruhi bisnis sewa sepeda?")
st.write("2. Apakah ada hubungan temperature dengan penyewa sepeda secara keseluruhan setiap jam, apakah suhu udara pada jam tersebut dapat mempengaruhi bisnis sewa sepeda?")
st.write(" ")
st.write("Analisis data Bike Sharing yang saya lakukan dapat menjawab kedua pertanyaan di atas.")
st.header(" ")
st.header("Hasil dari Analisis Data:")

# Display bar plot for Total Renter vs Season
st.subheader('Hubungan Jumlah Penyewa dengan Musim')
season_order = ['Winter', 'Spring', 'Summer', 'Fall']
sns.barplot(x='Season', y='Total Renter', data=seasons, order=season_order, color='#00008B', edgecolor='#000000')
plt.title("Total Renter VS Season")
plt.xlabel("Season")
plt.ylabel("Total Renter")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
st.write("")

# Display bar plot for Total Renter vs Temperature
st.subheader('Hubungan Jumlah Penyewa dengan Suhu')
plt.figure(figsize=(11, 5))
plt.bar(renter_by_temp.index.astype(str), renter_by_temp, color='#00008B', edgecolor='#000000')
plt.xlabel('Temperature (°C)')
plt.ylabel('Total Renter')
plt.title('Total Renter VS Temperature')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
st.write("Musim gugur menunjukkan jumlah penyewa sepeda yang paling tinggi, diikuti oleh musim panas, musim dingin, dan musim semi. Hal tersebut menunjukkan bahwa musim dapat mempengaruhi bisnis sewa sepeda, dengan musim gugur menjadi periode paling menguntungkan untuk bisnis tersebut. Rentang suhu udara antara 26 hingga 31 derajat Celsius menunjukkan jumlah penyewa sepeda paling tinggi. Jumlah penyewa sepeda juga cenderung menurun seiring dengan peningkatan atau penurunan suhu udara dari rentang tersebut. Hal ini menunjukkan adanya hubungan non-linear antara suhu udara dan jumlah penyewa sepeda, dengan suhu tertentu yang menjadi puncak popularitas dalam persewaan sepeda.")
