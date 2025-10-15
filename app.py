import streamlit as st
import pandas as pd
import joblib
import numpy as np

from category_encoders import TargetEncoder 
from sklearn.ensemble import RandomForestClassifier 


OHE_COLS = ['nationality_x', 'nationality_y', 'location', 'country']
TARGET_ENCODE_COLS = ['driverRef', 'constructorRef']


try:
    model = joblib.load('model.pkl') 
    encoder = joblib.load('target_encoder.joblib')
    feature_cols = joblib.load('feature_columns.joblib')
    
except FileNotFoundError as e:
    st.error(f"{e}")
    st.stop() 
except Exception as e:
    st.error(f"{e}")
    st.stop()

try:
    driver_options = encoder.mapping[0]['mapping'].index.tolist()
    constructor_options = encoder.mapping[1]['mapping'].index.tolist()
except Exception as e: 
    st.warning("⚠️ Could not extract categories from encoder map. Using sample options. Prediction should still be accurate.")
    driver_options = ['hamilton', 'verstappen', 'alonso', 'leclerc', 'unknown']
    constructor_options = ['mercedes', 'red_bull', 'ferrari', 'mclaren', 'unknown']


st.set_page_config(page_title="F1 Finish Predictor", layout="wide")
st.title("Formula 1 Target Finish Predictor (Random Forest) 🏎️")
st.markdown("Use the sidebar to input race conditions and driver/constructor details to predict if the target finish (1) will be achieved.")


with st.sidebar:
    st.header("1. Driver & Constructor")
    driver_ref = st.selectbox("Driver Reference", options=driver_options, index=driver_options.index('verstappen') if 'verstappen' in driver_options else 0)
    constructor_ref = st.selectbox("Constructor Reference", options=constructor_options, index=constructor_options.index('red_bull') if 'red_bull' in constructor_options else 0)

    st.header("2. Race & Grid")
    year = st.slider("Year", 2010, 2024, 2024)
    round_num = st.slider("Race Round", 1, 23, 10)
    grid = st.slider("Starting Grid Position", 1, 24, 1)
    driver_age = st.number_input("Driver Age (Years)", min_value=18.0, max_value=60.0, value=25.0, step=0.1)

    st.header("3. Circuit & Location Details")
    nationality_x = st.selectbox("Driver Nationality", ['British', 'Dutch', 'Spanish', 'German', 'Finnish', 'French'])
    nationality_y = st.selectbox("Constructor Nationality", ['British', 'Austrian', 'Italian', 'German', 'French'])
    location = st.selectbox("Circuit Location", ['Monaco', 'Silverstone', 'Sakhir', 'Sao Paulo', 'Spielberg'])
    country = st.selectbox("Circuit Country", ['UK', 'Bahrain', 'Monaco', 'Brazil', 'Austria'])
    
    st.subheader("Coordinates (Numerical)")
    lat = st.number_input("Latitude", value=43.73, step=0.01, format="%.2f")
    lng = st.number_input("Longitude", value=7.42, step=0.01, format="%.2f")
    alt = st.number_input("Altitude (m)", value=50, step=1)
    


if st.button("PREDICT TARGET FINISH", type="primary"):
    
    input_data = {
        'year': [year], 'round': [round_num], 'grid': [grid], 
        'lat': [lat], 'lng': [lng], 'alt': [alt], 'driver_age': [driver_age],
        'driverRef': [driver_ref], 'constructorRef': [constructor_ref],
        'nationality_x': [nationality_x], 'nationality_y': [nationality_y],
        'location': [location], 'country': [country]
    }
    input_df = pd.DataFrame(input_data)

    te_features = encoder.transform(input_df[TARGET_ENCODE_COLS])
    te_features.columns = [f'{col}_TargetEncoded' for col in TARGET_ENCODE_COLS]
    
    ohe_features = pd.get_dummies(input_df[OHE_COLS], columns=OHE_COLS, drop_first=True)
    
    dropped_cols = TARGET_ENCODE_COLS + OHE_COLS + ['surname', 'forename', 'dob', 'name', 'name_y', 'circuitRef', 'circuitId', 'date']
    final_features = input_df.drop(columns=[col for col in dropped_cols if col in input_df.columns], errors='ignore')
    
    final_features = pd.concat([final_features.reset_index(drop=True), 
                                te_features.reset_index(drop=True), 
                                ohe_features.reset_index(drop=True)], axis=1)

    missing_cols = set(feature_cols) - set(final_features.columns)
    for c in missing_cols:
        final_features[c] = 0 

    final_features = final_features.drop(columns=set(final_features.columns) - set(feature_cols), errors='ignore')

    final_features = final_features[feature_cols]

    prediction = model.predict(final_features)[0]
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Prediction Result:")
        if prediction == 1:
            st.success("✅ TARGET FINISH ACHIEVED!")
            st.balloons()
        else:
            st.error("❌ TARGET FINISH NOT ACHIEVED")

    with col2:
        try:
            proba = model.predict_proba(final_features)[0][1]
            st.metric(label="Probability of Success", value=f"{proba*100:.2f}%")
        except:
            st.info("Probability score not available (Model does not support `predict_proba`).")
            
    st.markdown("---")
    st.caption("Feature Vector used for prediction (must match model expectations):")
    st.dataframe(final_features)
