import streamlit as st
import requests
import pydeck as pdk
import plotly.express as px
import pandas as pd

# Function to fetch weather data
def fetch_weather(city):
    api_key = "OpenWeather API key"  # Replace with your actual OpenWeather API key
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    current_weather_response = requests.get(current_weather_url).json()
    forecast_response = requests.get(forecast_url).json()
    return current_weather_response, forecast_response

# Streamlit UI components
st.title('Weather Dashboard')

# Add CSS for custom theme from external file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("static/style.css")

# Sidebar for city input
with st.sidebar:
    city = st.text_input('Enter a city name')
    get_weather = st.button('Get Weather')

if get_weather:
    current_weather, forecast = fetch_weather(city)
    
    if 'coord' in current_weather:
        # Map display using pydeck
        map_data = pd.DataFrame({'lat': [current_weather['coord']['lat']], 'lon': [current_weather['coord']['lon']]})
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=current_weather['coord']['lat'], longitude=current_weather['coord']['lon'], zoom=11),
            layers=[pdk.Layer('ScatterplotLayer', data=map_data, get_position='[lon, lat]', get_color='[76, 175, 80, 160]', get_radius=200)],
        ))

        # Displaying the weather details
        st.subheader(f"Weather in {current_weather['name']} ({current_weather['sys']['country']})")
        st.write(f"**Temperature:** {current_weather['main']['temp']} °C")
        st.write(f"**Weather:** {current_weather['weather'][0]['description']}")
        st.write(f"**Humidity:** {current_weather['main']['humidity']}%")
        st.write(f"**Wind Speed:** {current_weather['wind']['speed']} m/s")
        
        # Forecast graph using plotly
        df = pd.DataFrame({
            'date': [item['dt_txt'] for item in forecast['list']],
            'temp': [item['main']['temp'] for item in forecast['list']],
            'weather': [item['weather'][0]['description'] for item in forecast['list']]
        })

        fig = px.line(df, x='date', y='temp', title='7 Day Temperature Forecast')
        st.plotly_chart(fig)

        # Creating a 7-day forecast table
        st.subheader('7-Day Weather Forecast')
        df['date'] = pd.to_datetime(df['date'])
        df['day'] = df['date'].dt.date
        daily_forecast = df.groupby('day').agg({'weather': 'first', 'temp': 'mean'}).reset_index()
        daily_forecast.columns = ['Date', 'Weather', 'Avg Temp (°C)']
        st.table(daily_forecast)

    else:
        st.error("Failed to retrieve data. Please check the city name and try again.")
