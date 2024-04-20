import streamlit as st
import pickle
import numpy as np

# function to deserialized the saved pickle file 
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# deserialized dictionary which holds the objects of predictive model and encoder
data = load_model()

random_forest_classifier_model = data['model']
nominal_features_encoder = data['nominal_columns_encoder']

# function to construct the road accidents' severity prediction page 
def show_predict_page():
    st.title("Road Accident's Severity Prediction")
    st.write("Please select values for the following input features:")

    age_band_of_driver = (
        '18-30', '31-50', 'Under 18', 'Over 51', 'Unknown'
    )


    type_of_vehicle_dict = {
        'Automobile': 'Automobile', 'Public (> 45 seats)': 'Public (> 45 seats)', 
        'Lorry (41 - 100 tonnes)': 'Lorry (41?100Q)', 'Unknown': 'Unknown',
        'Public (12 seats)': 'Public (12 seats)', 'Taxi': 'Taxi',
        'Pick up (<= 10 tonnes)': 'Pick up upto 10Q', 'Stationwagen': 'Stationwagen',
        'Other': 'Other', 'Lorry (11 - 40 tonnes)': 'Lorry (11?40Q)',
        'Long lorry': 'Long lorry', 'Public (13 - 45 seats)': 'Public (13?45 seats)'
    }

    type_of_vehicle_inputs = (
        'Automobile', 'Taxi', 'Stationwagen', 'Pick up (<= 10 tonnes)', 'Lorry (11 - 40 tonnes)',
        'Lorry (41 - 100 tonnes)', 'Long lorry', 'Public (12 seats)', 'Public (13 - 45 seats)', 
        'Public (> 45 seats)', 'Other', 'Unknown'
    )

    type_of_vehicle = (
       'Automobile', 'Public (> 45 seats)', 'Lorry (41?100Q)', 'Unknown',
       'Public (13?45 seats)', 'Lorry (11?40Q)', 'Long lorry',
       'Public (12 seats)', 'Taxi', 'Pick up upto 10Q', 'Stationwagen',
       'Other'
    )

    area_accident_occured = (
       'Residential areas', 'Office areas', 'Recreational areas',
       'Industrial areas', 'Church areas', 'Outside rural areas',
       'School areas', 'Other'
    )

    road_surface_type = (
       'Asphalt roads', 'Earth roads', 'Asphalt roads with some distress',
       'Gravel roads', 'Other'
    )

    light_conditions = (
       'Daylight', 'Darkness - lights lit', 'Darkness - no lighting',
       'Darkness - lights unlit'
    )

    weather_conditions = (
        'Normal', 'Raining', 'Other'
    )

    age_band_of_casualty = (
        'Under 18', '18-30', '31-50', 'Over 51', 'Unknown'
    )

    hour_of_day = (0, 1, 2, 3, 4, 5, 6,
                   7, 8, 9, 10, 11, 12,
                   13, 14, 15, 16, 17, 18,
                   19, 20, 21, 22, 23)
    
    
    # Construct the sliders and selection boxes for users to select values for the respective  input features
    number_of_vehicles_involved = st.slider("Number of Vehicles Involved", 1, 7, 1)

    number_of_casualties = st.slider("Number of Casualties", 1, 8, 1)

    hour_of_day = st.selectbox('Hour of Day', hour_of_day)

    age_band_of_driver = st.selectbox('Age Band of Driver', age_band_of_driver)

    type_of_vehicle = type_of_vehicle_dict[st.selectbox('Type of Vehicles', type_of_vehicle_inputs)]

    area_accident_occured = st.selectbox('Area Accident Occured', area_accident_occured)

    road_surface_type = st.selectbox('Type of Road Surface', road_surface_type)

    light_conditions = st.selectbox('Condition of Light', light_conditions)

    weather_conditions = st.selectbox('Conditions of Weather', weather_conditions)

    age_band_of_casualty = st.selectbox('Age Band of Casualty', age_band_of_casualty)

    col1, col2, col3 = st.columns([0.33, 0.3, 0.3])
    with col1:
        pass
    with col2:
        btn = st.button("Predict Severity")
    # Predict the road accident's severity after the predict button is clicked
    if btn:
        x = np.array([[number_of_vehicles_involved, number_of_casualties, hour_of_day,
                       age_band_of_driver, type_of_vehicle, area_accident_occured,
                       road_surface_type, light_conditions, weather_conditions, age_band_of_casualty]])
        x[:, 3:] = nominal_features_encoder.transform(x[:, 3:])
        x = x.astype(float)

        #save the result of severity prediction 
        severity = random_forest_classifier_model.predict(x)
        #assigned the precision, recall, and f1-score for each severity class
        global precision,recall,f1score
        if (severity == 0):
            severity = 'Fatal Injury'
            precision = 0.98
            recall = 0.98
            f1score = 0.98
        elif (severity == 1):
            severity = 'Serious Injury'
            precision = 0.87
            recall = 0.84
            f1score = 0.86
        else:
            severity = 'Slight Injury'
            precision = 0.84
            recall = 0.87
            f1score = 0.85

        st.subheader(f"{severity}")

        column1, column2, column3= st.columns(3)
        with column1:
            st.write('Precision')
            st.write(precision)
        
        with column2:
            st.write('Recall')
            st.write(recall)

        with column3:
            st.write('F1 Score')
            st.write(f1score)

    with col3:
        pass

        
    

    # ok = st.button("Predict Severity")
    # if ok:
    #     x = np.array([[number_of_vehicles_involved, number_of_casualties, hour_of_day,
    #                    age_band_of_driver, type_of_vehicle, area_accident_occured,
    #                    road_surface_type, light_conditions, weather_conditions, age_band_of_casualty]])
    #     x[:, 3:] = nominal_features_encoder.transform(x[:, 3:])
    #     x = x.astype(float)

    #     severity = random_forest_classifier_model.predict(x)

    #     if (severity == 0):
    #         severity = 'Fatal Injury'
    #     elif (severity == 1):
    #         severity = 'Serious Injury'
    #     else:
    #         severity = 'Slight Injury'
        
    #     st.subheader(f"{severity}")