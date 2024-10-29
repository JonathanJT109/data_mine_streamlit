import streamlit as st
import pandas as pd
import numpy as np
import base64

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
    # house_price = st.number_input('Enter the house price', min_value=0.0, max_value=1000000.0, value=0.0, step=1000.0)
    with open("mag.svg", "r") as svg_file:
        svg_data = svg_file.read()
        encoded_svg = base64.b64encode(svg_data.encode()).decode()
    st.markdown(
        """
        <style>
        /* Target the text input field specifically */
        input[type="text"]::placeholder {
            color: #888; /* Change the placeholder text color */
            font-weight: 500; /* Set placeholder text weight */
            font-size: 16px; /* Adjust the placeholder font size */
        }

        /* Additional styles for the input field */
        input[type="text"] {
            padding-left: 35px; /* Add space for potential icon */
            height: 40px; /* Adjust height */
            border: 2px solid #ddd; /* Custom border style */
            border-radius: 5px; /* Rounded corners */
        }

        /* Optional: Add an SVG icon in the text input */
        .text-input-icon input {
            background-image: url("data:image/svg+xml;base64,{encoded_svg}");
            background-repeat: no-repeat;
            background-position: 10px center; /* Position the SVG icon */
            background-size: 20px 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="text-input-icon">', unsafe_allow_html=True)
    house_price_text = st.text_input("",placeholder="Price")
    st.markdown('</div>', unsafe_allow_html=True)
    # Validate that the input is a number
    try:
        house_price = float(house_price_text) if house_price_text else 0.0
        if house_price < 0 or house_price > 1000000:
            st.error("Price should be between 0 and 1,000,000")
    except ValueError:
        st.error("Please enter a valid number")
        location = st.selectbox("Select the location", indiana_counties, index=None, placeholder="Select a location")
        search_button = st.button("Search")

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
            st.write("Price")

app()
