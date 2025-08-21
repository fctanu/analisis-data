import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Bike Sharing Data Analysis")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Calculate statistics and prepare data
day_max = day_df['cnt'].max()
day_min = day_df['cnt'].min()
day_mean = day_df['cnt'].mean()
hour_max = hour_df['cnt'].max()
hour_min = hour_df['cnt'].min()
hour_mean = hour_df['cnt'].mean()

monthly_avg_rentals = day_df.groupby(day_df['dteday'].dt.month)['cnt'].mean().reset_index()
monthly_avg_rentals.columns = ['bulan', 'cnt']

hourly_avg_rentals = hour_df.groupby('hr')['cnt'].mean().reset_index()

day_df['is_weekend'] = day_df['dteday'].dt.dayofweek.isin([5, 6])
avg_rentals_weekday_weekend = day_df.groupby('is_weekend')['cnt'].mean().reset_index()
avg_rentals_weekday_weekend['tipe_hari'] = avg_rentals_weekday_weekend['is_weekend'].map({False: 'Hari Kerja (Senin-Jumat)', True: 'Akhir Pekan (Sabtu-Minggu)'})

avg_rentals_by_weather = hour_df.groupby('weathersit')['cnt'].mean().reset_index()
weather_sit_mapping = {1: 'Jernih', 2: 'Kabut', 3: 'Salju/Hujan Ringan', 4: 'Hujan Salju Berat'}
avg_rentals_by_weather['weathersit'] = avg_rentals_by_weather['weathersit'].map(weather_sit_mapping)

hour_df['persentase_kasual'] = hour_df['casual'] / hour_df['cnt'] * 100
hour_df['persentase_terdaftar'] = hour_df['registered'] / hour_df['cnt'] * 100
casual_registered_df = hour_df.groupby('hr')[['persentase_kasual', 'persentase_terdaftar']].mean().reset_index()

total_rentals_df = day_df.groupby('dteday')['cnt'].sum().reset_index()

rfm_df = day_df.groupby('instant').agg({
    'dteday': lambda x: (day_df['dteday'].max() - x.max()).days,
    'instant': 'count',
    'cnt': 'sum'
}).rename(columns={
    'dteday': 'Recency',
    'instant': 'Frequency',
    'cnt': 'Monetary'
}).reset_index()

# Streamlit app
st.title("Bike Sharing Data Analysis")

# Statistik Penyewaan
st.subheader("Statistik Penyewaan")
fig, ax = plt.subplots(figsize=(10, 6))
stats = ['Day Max', 'Day Min', 'Day Mean', 'Hour Max', 'Hour Min', 'Hour Mean']
values = [day_max, day_min, day_mean, hour_max, hour_min, hour_mean]
bars = ax.bar(stats, values, color=sns.color_palette("husl", 8))
ax.set_ylabel('Jumlah', fontsize=12)
plt.xticks(rotation=45, ha='right')
max_bar = bars[0]
max_bar.set_color('red')
ax.text(max_bar.get_x() + max_bar.get_width()/2., max_bar.get_height(),
        f'{int(day_max)}', ha='center', va='bottom')
st.pyplot(fig)

# Rata-rata Penyewaan per Bulan
st.subheader("Rata-rata Penyewaan per Bulan")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(monthly_avg_rentals['bulan'], monthly_avg_rentals['cnt'], color='skyblue')
for bar in bars:
    if bar.get_height() > 5000:
        bar.set_color('coral')
ax.set_xlabel('Bulan', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
ax.set_xticks(range(1, 13))
ax.grid(axis='y')
st.pyplot(fig)

# Rata-rata Penyewaan per Jam
st.subheader("Rata-rata Penyewaan per Jam")
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['skyblue' if cnt <= 300 else 'coral' for cnt in hourly_avg_rentals['cnt']]
ax.bar(hourly_avg_rentals['hr'], hourly_avg_rentals['cnt'], color=colors)
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

# Rata-rata Penyewaan: Hari Kerja vs Akhir Pekan
st.subheader("Rata-rata Penyewaan: Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(avg_rentals_weekday_weekend['tipe_hari'], avg_rentals_weekday_weekend['cnt'], color=sns.color_palette("husl", 8)[3:5])
ax.set_xlabel('Tipe Hari', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
plt.xticks(rotation=45, ha='right')
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{int(bar.get_height())}', ha='center', va='bottom')
st.pyplot(fig)

# Rata-rata Penyewaan Berdasarkan Cuaca
st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(avg_rentals_by_weather['weathersit'], avg_rentals_by_weather['cnt'], color=sns.color_palette("husl", 8)[5:])
ax.set_xlabel('Situasi Cuaca', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
plt.xticks(rotation=45, ha='right')
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{int(bar.get_height())}', ha='center', va='bottom')
st.pyplot(fig)

# Pengguna Kasual vs Terdaftar per Jam
st.subheader("Pengguna Kasual vs Terdaftar per Jam")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(casual_registered_df['hr'], casual_registered_df['persentase_kasual'], label='Kasual', color=sns.color_palette("husl", 8)[0])
ax.plot(casual_registered_df['hr'], casual_registered_df['persentase_terdaftar'], label='Terdaftar', color=sns.color_palette("husl", 8)[1])
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Persentase', fontsize=12)
ax.legend()
ax.set_xticks(range(0, 24, 2))
st.pyplot(fig)

# Total Penyewaan dari Waktu ke Waktu
st.subheader("Total Penyewaan dari Waktu ke Waktu")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(total_rentals_df['dteday'], total_rentals_df['cnt'], color=sns.color_palette("husl", 8)[2], linewidth=2)
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Total Penyewaan', fontsize=12)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Distribusi RFM
st.subheader("Distribusi RFM")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(rfm_df['Recency'], kde=True, color=sns.color_palette("husl", 8)[3], ax=ax1)
ax1.set_title('Distribusi Recency', fontsize=14)
ax1.set_xlabel('Recency (hari)', fontsize=12)
ax1.set_ylabel('Frekuensi', fontsize=12)

sns.histplot(rfm_df['Frequency'], kde=True, color=sns.color_palette("husl", 8)[4], ax=ax2)
ax2.set_title('Distribusi Frequency', fontsize=14)
ax2.set_xlabel('Frequency', fontsize=12)
ax2.set_ylabel('Frekuensi', fontsize=12)

sns.histplot(rfm_df['Monetary'], kde=True, color=sns.color_palette("husl", 8)[5], ax=ax3)
ax3.set_title('Distribusi Monetary', fontsize=14)
ax3.set_xlabel('Monetary (jumlah penyewaan)', fontsize=12)
ax3.set_ylabel('Frekuensi', fontsize=12)

st.pyplot(fig)
