import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca data
@st.cache_data
def load_data():
    data = pd.read_csv('day.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

df = load_data()

# Judul dashboard
st.title('Bike Sharing Analysis')

# Sidebar untuk filter
st.sidebar.header('Select Year')
year = st.sidebar.selectbox('Pilih Tahun', options=[2011, 2012])
filtered_df = df[df['dteday'].dt.year == year]

# Grafik total sewa sepeda per bulan
st.subheader(f'Total Rental Bikes in Each Months ({year})')
monthly_rentals = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M'))['cnt'].sum().reset_index()
monthly_rentals['dteday'] = monthly_rentals['dteday'].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_rentals['dteday'], monthly_rentals['cnt'])
ax.set_xlabel('Months')
ax.set_ylabel('Total Rental Bikes')
st.pyplot(fig)

# Mapping musim
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
filtered_df['season_name'] = filtered_df['season'].map(season_map)

# Menghitung jumlah total sewa sepeda per musim untuk tahun yang dipilih
season_rentals = filtered_df.groupby('season_name')['cnt'].sum().sort_values(ascending=False)

# Visualisasi
st.subheader(f'Total Rental Bikes in Each Season ({year})')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=season_rentals.index, y=season_rentals.values, ax=ax)
ax.set_xlabel('Seasons')
ax.set_ylabel('Total Rental Bikes')
ax.set_title(f'Total Rental Bikes in Each Season ({year})')

# Menambahkan label jumlah pada setiap bar
for i, v in enumerate(season_rentals.values):
    ax.text(i, v, f'{v:,}', ha='center', va='bottom')

# Menampilkan plot di Streamlit
st.pyplot(fig)
