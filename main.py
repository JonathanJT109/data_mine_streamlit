import streamlit as st
import pandas as pd
import numpy as np

indiana_counties = ["Tippecanoe"]

def simulate_model_data(house_price, location):
    num_rows = 1
    data = {
        'house_value': np.random.randint(100000, 500000, size=num_rows),
        'rent_value': np.random.randint(800, 3000, size=num_rows),
        'crime_rate': np.random.uniform(0, 10, size=num_rows),
        'vacancy_rate': np.random.uniform(0, 1, size=num_rows)
    }

    df = pd.DataFrame(data)
    return df


@st.cache_data
def data():
    df = pd.DataFrame(
        (np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4]),
        columns=["lat", "lon"],
    )
    return df

def send_data(house_price, location):
    try:
        data = simulate_model_data(house_price, location)
        st.write("Data sent")
        return data
    except:
        st.write("Error sending data")

def app():
    house_price = st.number_input('Enter the house price', min_value=0.0, max_value=1000000.0, value=0.0, step=1000.0)
    location = st.selectbox("Select the location", indiana_counties, index=None, placeholder="Select a location")
    search_button = st.button("Search")

    # QUESTION: Use google maps instead?
    st.map(data())

    if search_button:
        if house_price > 0 and location is not None:
            predictions = send_data(house_price, location)
            if predictions is not None:
                house_price = f"${predictions['house_value'][0]:.2f}"
                rent_value = f"${predictions['rent_value'][0]:.2f}" 
                crime_rate = f"{predictions['crime_rate'][0]:.2f}%"
                vacancy_rate = f"{predictions['crime_rate'][0]:.2f}%"
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("House Value", house_price, "4%")
                col2.metric("Rent Rates", rent_value, "10%")
                col3.metric("Crime Rate", crime_rate, "-14%")
                col4.metric("Vacancy Rate", vacancy_rate, "-17%")
                # st.write(predictions)
        else:
            st.write("Please enter the house price and select the location")



app()
