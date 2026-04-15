import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Helper function
def create_daily_rentals_df(df):
    daily_rentals_df = df.groupby("dteday")["total_rentals"].sum().reset_index()
    return daily_rentals_df

def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby(["hour", "workingday"])["total_rentals"].mean().reset_index()
    return hourly_rentals_df

def create_user_type_df(df):
    user_type_df = df.groupby("season")[["casual", "registered"]].mean().reset_index()
    return user_type_df


# Load data
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")


# Cleaning data
day_clean = day_df.copy()
hour_clean = hour_df.copy()

day_clean["dteday"] = pd.to_datetime(day_clean["dteday"])
hour_clean["dteday"] = pd.to_datetime(hour_clean["dteday"])

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain",
    4: "Heavy Rain"
}

day_clean["season"] = day_clean["season"].map(season_map)
day_clean["weathersit"] = day_clean["weathersit"].map(weather_map)

hour_clean["season"] = hour_clean["season"].map(season_map)
hour_clean["weathersit"] = hour_clean["weathersit"].map(weather_map)

day_clean.rename(columns={
    "yr": "year",
    "mnth": "month",
    "cnt": "total_rentals"
}, inplace=True)

hour_clean.rename(columns={
    "yr": "year",
    "mnth": "month",
    "hr": "hour",
    "cnt": "total_rentals"
}, inplace=True)

day_clean["year"] = day_clean["year"].map({0: 2011, 1: 2012})
hour_clean["year"] = hour_clean["year"].map({0: 2011, 1: 2012})



# Sidebar filter
with st.sidebar:
    st.image("https://raw.githubusercontent.com/cicanuraeni/bike-sharing-analysis/refs/heads/main/harisankar-sahoo-8XeyRrz-t0o-unsplash.png")
    st.header("Filter Dashboard")

    selected_year = st.selectbox(
        "Pilih Tahun",
        options=["Semua", 2011, 2012]
    )

if selected_year != "Semua":
    main_day_df = day_clean[day_clean["year"] == selected_year]
    main_hour_df = hour_clean[hour_clean["year"] == selected_year]
else:
    main_day_df = day_clean.copy()
    main_hour_df = hour_clean.copy()


# Siapkan dataframe
daily_rentals_df = create_daily_rentals_df(main_day_df)
hourly_rentals_df = create_hourly_rentals_df(main_hour_df)
user_type_df = create_user_type_df(main_day_df)


# Header
st.header("Bike Sharing Dashboard :sparkles:")
st.subheader("Daily Rentals Overview")

col1, col2, col3 = st.columns(3)

with col1:
    total_days = daily_rentals_df["dteday"].nunique()
    st.metric("Total Days Recorded", value=total_days)

with col2:
    avg_rentals = round(daily_rentals_df["total_rentals"].mean(), 0)
    st.metric("Average Daily Rentals", value=int(avg_rentals))

with col3:
    max_rentals = daily_rentals_df["total_rentals"].max()
    st.metric("Highest Daily Rentals", value=int(max_rentals))


# Chart 1: Tren penyewaan
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rentals"],
    linewidth=2,
    color="pink"
)
ax.set_title("Tren Penyewaan Sepeda (2011-2012)")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(alpha=0.3)

st.pyplot(fig)


# Chart 2: Peak hour
st.subheader("Perbandingan Penyewaan per Jam")

fig, ax = plt.subplots(figsize=(16, 8))

working_day_df = hourly_rentals_df[hourly_rentals_df["workingday"] == 1]
holiday_df = hourly_rentals_df[hourly_rentals_df["workingday"] == 0]

ax.plot(
    working_day_df["hour"],
    working_day_df["total_rentals"],
    label="Working Day",
    color="red",
    linewidth=2
)

ax.plot(
    holiday_df["hour"],
    holiday_df["total_rentals"],
    label="Holiday",
    color="black",
    linewidth=2
)

ax.set_title("Perbandingan Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)


# Chart 3: Casual vs Registered
st.subheader("Casual vs Registered per Season")

season_order = ["Spring", "Summer", "Fall", "Winter"]
user_type_df["season"] = pd.Categorical(user_type_df["season"], categories=season_order, ordered=True)
user_type_df = user_type_df.sort_values("season")

fig, ax = plt.subplots(figsize=(16, 8))
bar_width = 0.35
x = range(len(user_type_df))

ax.bar(
    [i - bar_width / 2 for i in x],
    user_type_df["casual"],
    width=bar_width,
    label="Casual",
    color="red"
)

ax.bar(
    [i + bar_width / 2 for i in x],
    user_type_df["registered"],
    width=bar_width,
    label="Registered",
    color="black"
)

ax.set_title("Perbandingan Pengguna Casual vs Registered per Season")
ax.set_xlabel("Season")
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
ax.set_xticks(list(x))
ax.set_xticklabels(user_type_df["season"])
ax.legend()
ax.grid(axis="y", alpha=0.3)

st.pyplot(fig)
