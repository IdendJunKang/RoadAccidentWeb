import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# function to load the road accident's severity dataset into DataFrame
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_RTA_dataset.csv")
    return df

df = load_data()

# function to construct the road accidents' severity dataset exploration page
def show_explore_page():
    # calculate the mean of number of casualties and number of vehicles involved
    casualties_rate = df['Number_of_casualties'].mean()
    vehicles_involvement_rate = df['Number_of_vehicles_involved'].mean()

    st.title('Metrics')
    col1, col2 = st.columns(2)
    col1.metric('Rate of Casualties', round(casualties_rate,2))
    col2.metric('Rate of Vehicles Involvement', round(vehicles_involvement_rate,2))

    # table for displaying fatal accident proportion via selection of influencial factors of accident
    st.title('Proportion of fatal road accident of influencial factors')
    factor_selection = st.selectbox('', ('Light Conditions', 'Weather Conditions'))
    if factor_selection == 'Light Conditions':
        light_conditions_df = df.groupby(by='Light_conditions',as_index=False).size()
        
        light_conditions_df.rename(columns={"size": "No of road accident"}, inplace=True)

        daylight_fatal_injury = df[df['Light_conditions'] == 'Daylight']['Accident_severity'].value_counts()[2] / light_conditions_df.iloc[3,1] * 100
        darkness_lights_lit_fatal_injury = df[df['Light_conditions'] == 'Darkness - lights lit']['Accident_severity'].value_counts()[2] / light_conditions_df.iloc[0,1] * 100
        darkenss_no_lighting_fatal_injury = df[df['Light_conditions'] == 'Darkness - no lighting']['Accident_severity'].value_counts()[2] /  light_conditions_df.iloc[2,1] * 100
        darkness_lights_unlit_fatal_injury = 0

        fatal_accident_composition_data = np.array([darkness_lights_lit_fatal_injury, darkness_lights_unlit_fatal_injury, darkenss_no_lighting_fatal_injury, daylight_fatal_injury])
        fatal_accident_composition_data = pd.Series(fatal_accident_composition_data, name='fatal road accident proportion')

        light_conditions_df['fatal road accident proportion in %'] = fatal_accident_composition_data
        light_conditions_df.sort_values(by=['fatal road accident proportion in %'], ascending=False, inplace=True)

        st.write(light_conditions_df.style.background_gradient(cmap='Blues'))

    elif factor_selection == 'Weather Conditions':
        weather_conditions_df = df.groupby(by='Weather_conditions', as_index=False).size()
        weather_conditions_df.rename(columns={"size": "No of road accident"}, inplace=True)
        normal_weather_fatal_injury = df[df['Weather_conditions'] == 'Normal']['Accident_severity'].value_counts()[2] / weather_conditions_df.iloc[0,1] * 100
        raining_fatal_injury = df[df['Weather_conditions'] == 'Raining']['Accident_severity'].value_counts()[2] / weather_conditions_df.iloc[2,1] * 100
        other_weather_fatal_injury = 0
        weather_fatal_accident_composition_data = np.array([normal_weather_fatal_injury, other_weather_fatal_injury, raining_fatal_injury])
        weather_fatal_accident_composition_data = pd.Series(weather_fatal_accident_composition_data, name='fatal road accident proportion')

        weather_conditions_df['fatal road accident proportion in %'] = weather_fatal_accident_composition_data
        weather_conditions_df.sort_values(by=['fatal road accident proportion in %'], ascending=False, inplace=True)

        st.write(weather_conditions_df.style.background_gradient(cmap='Blues'))



    def accident_severity_countplot(df):
        countplot = sns.countplot(x=df['Accident_severity'])
        for container in countplot.containers:
            countplot.bar_label(container)
        st.pyplot(countplot.get_figure())
    
    st.title('Distribution of road accident severity by number of casualties')
    number_of_casualties = st.selectbox('Number of casualties', (1,2,3,4,5,6,7,8))
    if number_of_casualties == 1:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 1]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 2:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 2]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 3:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 3]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 4:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 4]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 5:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 5]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 6:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 6]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    elif number_of_casualties == 7:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 7]
        accident_severity_countplot(filtered_df_based_on_casualties_number)
    else:
        filtered_df_based_on_casualties_number = df[df['Number_of_casualties'] == 8]
        accident_severity_countplot(filtered_df_based_on_casualties_number)

    # fig = px.bar(filtered_df_based_on_casualties_number, x = 'Accident_severity', template='seaborn',)
    # st.plotly_chart(fig)

    
    # countplot = sns.countplot(x=df['Accident_severity'])

    # for container in countplot.containers:
    #         countplot.bar_label(container)

    # st.pyplot(countplot.get_figure())

    st.title('Proportion of casualties by road accidents areas')
    pie_fig = px.pie(df, values='Number_of_casualties', names = 'Area_accident_occured', hole=0.5)
    pie_fig.update_traces(text = df['Area_accident_occured'], textposition='outside')
    st.plotly_chart(pie_fig)



    

    # Construct a pie chart for displaying road accident severity distribution by number of casualties
    with st.expander("Casualties Distribution by Road Accident Severity"):
        casualties_by_accident_severity = df.groupby(['Accident_severity'])[['Number_of_casualties']].sum()
        data = casualties_by_accident_severity['Number_of_casualties']
        label = casualties_by_accident_severity.index

        plt.style.use('ggplot')
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=label, autopct='%1.1f%%', wedgeprops={'edgecolor':'black'})
        ax1.set_title("Casualties' Distribution by Accident Severity")
        st.pyplot(fig1)
    
    # Construct a horizontal bar chart for displaying the distribution of road accidents by causes
    with st.expander("Distribution of Road Accidents by Causes"):
        count_of_road_accidents_by_causes = df['Cause_of_accident'].value_counts()
        count_of_road_accidents = count_of_road_accidents_by_causes.values
        causes_of_accidents = count_of_road_accidents_by_causes.index
        colors = ['red', '#C21807', '#960018', '#FF4500', 'orange', '#FEBA4F',
                  '#F2CA85', '#EABD8C', '#3F704D', '#2E8B57', '#9DC183']
        
        plt.style.use('ggplot')
        fig2, ax2 = plt.subplots()
        ax2.barh(causes_of_accidents, count_of_road_accidents_by_causes, color= colors)
        ax2.set_title("Distribution of Road Accidents by Causes")
        ax2.set_xlabel("Causes of Road Accidents")
        ax2.set_ylabel("Count of Road Accidents")

        #add in value at the top of bar for each bar
        for container in ax2.containers:
            ax2.bar_label(container)

        st.pyplot(fig2)

    # Constuct a histogram for displaying the distribution of road accidents by hour of day
    with st.expander("Distribution of Road Accidents by Hour of Day"):
        count_of_road_accidents_by_hour_of_day = df['Hour_of_day']

        plt.style.use('seaborn')
        fig3, ax3 = plt.subplots()
        ax3.hist(x=count_of_road_accidents_by_hour_of_day,bins=6, edgecolor = 'black')
        ax3.set_xticks([0, 4, 8, 12, 16, 20, 23])
        ax3.set_title("Distribution of Road Accidents by Hour of Day")
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Number of Road Accidents')

        #add in value at the top of each bin
        for container in ax3.containers:
            ax3.bar_label(container)
        
        st.pyplot(fig3)

    # Construct a point plot for displaying the central tendancy of number of casualties by driver's age
    with st.expander("Central Tendancy of Number of Casualties by Driver's Age Band"):
        plot = sns.catplot(data=df, y='Age_band_of_driver', x='Number_of_casualties', kind='point')
        plot.set_xlabels('The Number of Casualties')
        plot.set_ylabels("Driver's Age Band")

        st.pyplot(plot.fig)

    # Construct a boxplot for displaying the distribution of number of casualties by type of collision
    with st.expander("Distribution of Number of Casualties by Type of Collision"):
        fig4, boxplot = plt.subplots()
        boxplot = sns.boxplot(x=df['Number_of_casualties'], y=df['Type_of_collision'], showmeans=True,
                              meanprops={'markerfacecolor':'black'}, medianprops={'color': 'red', 'lw': 3, 'ls': ':'})
        boxplot.set_xlabel('The Number of Casualties')
        boxplot.set_ylabel("Type of Collision")
        
        st.pyplot(fig4)




