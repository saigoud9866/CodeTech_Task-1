import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st 
import pandas as pd  


API_KEY = 'b6d790672e135ef563f336f8daa935af'  
CITY = 'Hyderabad'
UNITS = 'metric' 
lat = '17.4065'
lon = '78.4772'

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch data:", response.json())
    exit()

data = response.json()
print(data)

current_temp = data['main']['temp']
feels_like = data['main']['feels_like']
temp_min = data['main']['temp_min']
temp_max = data['main']['temp_max']
humidity = data['main']['humidity']
pressure = data['main']['pressure']
wind_speed = data['wind']['speed']
weather_description = data['weather'][0]['description'].capitalize()
rain_volume = data.get('rain', {}).get('1h', 0)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

st.title(f"🌦️ Weather Dashboard - {CITY}")
st.caption(f"Last updated: {timestamp}")

st.subheader(f"Current Weather: {weather_description}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature (°C)", f"{current_temp}°C")
    st.metric("Feels Like (°C)", f"{feels_like}°C")
    st.metric("Min Temp (°C)", f"{temp_min}°C")

with col2:
    st.metric("Max Temp (°C)", f"{temp_max}°C")
    st.metric("Humidity", f"{humidity}%")
    st.metric("Pressure", f"{pressure} hPa")

with col3:
    st.metric("Wind Speed", f"{wind_speed} m/s")
    st.metric("Rain Volume", f"{rain_volume} mm")

st.divider()

weather_df = pd.DataFrame({
    'Parameter': ['Temperature', 'Feels Like', 'Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Wind Speed', 'Rain (1h)'],
    'Value': [current_temp, feels_like, temp_min, temp_max, humidity, pressure, wind_speed, rain_volume]
})

st.subheader("📊 Weather Parameters Bar Chart")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Value', y='Parameter', data=weather_df, palette='coolwarm', ax=ax)
ax.set_xlabel("Values")
ax.set_ylabel("Parameters")
ax.set_title("Current Weather Stats")
st.pyplot(fig)

st.divider()
