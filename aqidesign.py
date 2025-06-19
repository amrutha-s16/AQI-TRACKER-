import streamlit as st
import pickle
import plotly.graph_objects as go
# Background and title setup
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("http://wallpapers-clan.com/wp-content/uploads/2023/07/blue-sky-clouds-aesthetic-wallpaper.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color:white;'>AIR QUALITY INDEX CALCULATION</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:white; font-size:18px;'>Enter pollutant concentration levels to calculate the Air Quality Index (AQI) and determine how safe the air is to breathe.</p>",
    unsafe_allow_html=True
)

# Input fields
co = st.number_input("Enter the CO (mg/m³) value", min_value=0.0)
ozone = st.number_input("Enter the Ozone (µg/m³) value", min_value=0.0)
no = st.number_input("Enter the NO (µg/m³) value", min_value=0.0)
no2 = st.number_input("Enter the NO2 (µg/m³) value", min_value=0.0)
nox = st.number_input("Enter the NOX (µg/m³) value", min_value=0.0)
nh3 = st.number_input("Enter the NH3 (µg/m³) value", min_value=0.0)
so2 = st.number_input("Enter the SO2 (µg/m³) value", min_value=0.0)
pm2 = st.number_input("Enter the PM2.5 (µg/m³)", min_value=0.0)
pm10 = st.number_input("Enter the PM10 (µg/m³)", min_value=0.0)

# Load models
model1 = pickle.load(open("scalmodel.pkl", "rb"))
model = pickle.load(open("aqimodel.pkl", "rb"))

inp = [[co, ozone, no, no2, nox, nh3, so2, pm2, pm10]]
scal = model1.transform(inp)

if st.button('Predict'):
    result = float(model.predict(scal)[0])
    aqi = round(result)
    st.markdown(f"<h2 style='color:white;'>Predicted AQI: {aqi}</h2>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result,
        title={'text': "AQI Meter"},
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [51, 100], 'color': "yellow"},
                {'range': [101, 150], 'color': "orange"},
                {'range': [151, 200], 'color': "red"},
                {'range': [201, 300], 'color': "purple"},
                {'range': [301, 500], 'color': "maroon"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': result
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)    
    if aqi <= 50:
        st.success("Air Quality: Good 😊")
        
    elif aqi <= 100:
        st.info("Air Quality: Moderate 😐")
        
    elif aqi <= 150:
        st.warning("Air Quality: Unhealthy for Sensitive Groups ⚠️")
        
    elif aqi <= 200:
        st.error("Air Quality: Unhealthy ❌")
        
    elif aqi <= 300:
        st.error("Air Quality: Very Unhealthy 🚫")
        
    elif aqi <= 500:
        st.error("Air Quality: Hazardous ☠️")
    else:
        st.markdown("Not Polluted ")