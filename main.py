import numpy as np
import pandas as pd
import streamlit as st

from server import get_counties, get_county_house_value, get_county_rent_rates

indiana_counties = get_counties("IN")


def get_test(state: str, county: str):
    hv = get_county_house_value(state, county)
    rr = get_county_rent_rates(state, county)
    return (hv, rr)


def simulate_model_data(location):
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


def send_data(location):
    try:
        data = simulate_model_data(location)
        st.write("Data sent")
        return data
    except:
        st.write("Error sending data")

def app():
    location = st.selectbox("Select the location", indiana_counties, index=None, placeholder="Select a location")
    search_button = st.button("Search")

    # QUESTION: Use google maps instead?
    st.map(data())

    if search_button:
        if location is not None:
            predictions = send_data(location)
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
            hv, rr = get_test("IN", location)
            a = st.line_chart(hv)
            b = st.line_chart(rr)
        else:
            st.write("Please enter the house price and select the location")



app()