import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
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

def simulate_price_trend(initial_price, periods=12):
    dates = pd.date_range(start="2023-01-01", periods=periods, freq="M")
    prices = initial_price * (1 + 0.01 * np.random.randn(periods)).cumprod()
    return pd.DataFrame({"Date": dates, "Price": prices})

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
        return data
    except:
        st.write("Error sending data")

def app():
    st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Yeseva+One&display=swap" rel="stylesheet">
    
    <style>
    /* Style for the number input */
    .stApp {
     background-color: #FFFFFF;
    }
        /* Set the default font for the entire app */
        * {
            font-family: 'Poppins', sans-serif;
        }

        /* Specific styles for headers or other components */
        .main-title {
            font-family: 'Yeseva One', cursive;
            font-size: 2.5em;
        }
        .sub-heading {
            font-family: 'Merriweather', serif;
            font-weight: 700;
            font-size: 1.5em;
        }
    [data-testid="stNumberInputContainer"] {
        border: 2px solid #444; /* Darker border */
        border-radius: 2px; /* Rounded corners */
        box-shadow: none; /* Remove any default shadow */
        width: 100%;
        height: 50px;
    }
    [data-testid="stNumberInput"] {
        width: 100%;
        height: 50px;
    }
    [data-baseweb="select"] {
        border: 2px solid #444; /* Darker border */
        box-shadow: none; /* Remove any default shadow */
        width: 100%;
        height: 50px;
    }
    .st-d6, .st-d5, .st-d4, .st-d3 {
        border-width: 0px;
     }
    .st-ap, .st-ao, .st-an, .st-am {
        border-width: 0px;
    }
    .st-emotion-cache-hz80o9.focused {
        border: 2px solid #444; /* Darker border */
        border-radius: 2px; /* Rounded corners */
        box-shadow: none; /* Remove any default shadow */
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        /* Set up the navbar style */
        .navbar {
            overflow: hidden;
            background-color: #F39C12;
            padding: 10px 10px;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }


        </style>

        <div class="navbar">

        </div>

        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([1, 1])  # Adjust ratios as needed

    with col1:
        house_price = st.number_input('', min_value=0.0, max_value=1000000.0, value=None, step=1000.00, placeholder="Price")

    with col2:
        location = st.selectbox("", indiana_counties, index=None, placeholder="Location")


    search_button = st.button("Search")

    # QUESTION: Use google maps instead?
    col3, col4 = st.columns([1, 1])  # Map and metrics side by side
    st.markdown('''
        <style>
            .metric-container {
                border: 1px solid black; /* Border styling */
                padding: 10px; /* Padding inside the container */
                border-radius: 15px; /* Rounded corners */
                margin-bottom: 50px; 
            }
            .metric-label {
                font-family: Poppins;
                font-size: 24px;
                font-weight: 400;
                line-height: 36px;
                text-align: center;
            }
            .metric-value {
                font-size: 1.5em; /* Increase value font size */
                color: #333; /* Darker color for the value */
            }

            .metric-container {
                display: flex;
                flex-direction: column;
            }
            .head {
                border-bottom: 1px solid black;
            }
        </style>
    ''', unsafe_allow_html=True)
    with col3:
        st.map(data())
    with col4:
        if search_button:
            if house_price > 0 and location is not None:
                predictions = send_data(house_price, location)
                if predictions is not None:
                    house_price = f"${predictions['house_value'][0]:.2f}"
                    rent_value = f"${predictions['rent_value'][0]:.2f}" 
                    crime_rate = f"{predictions['crime_rate'][0]:.2f}%"
                    vacancy_rate = f"{predictions['crime_rate'][0]:.2f}%"
       
                    # Wrap each metric in a container
                    # st.write(predictions)
                    col10, col12 = st.columns([1, 1])  # Adjust ratios as needed
                    col11, col13 = st.columns([1,1])
                    with col10:
                        with st.container():
                            st.markdown(f'''
                                <div class="metric-container">
                                    <div class="head">House Value</div> 
                                    <div class="bottom">
                                        <div class="price">{house_price}</div>
                                        <div class="change">Change: 4%</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                    with col12:
                        with st.container():
                            st.markdown(f'''
                                <div class="metric-container">
                                    <div class="head">Rent Rate</div> 
                                    <div class="bottom">
                                        <div class="price">{rent_value}</div>
                                        <div class="change">Change: 10%</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                    with col11:
                        with st.container():
                            st.markdown(f'''
                                <div class="metric-container">
                                    <div class="head">Crime Rate</div> 
                                    <div class="bottom">
                                        <div class="price">{crime_rate}</div>
                                        <div class="change">Change: -14%</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                    with col13:
                        with st.container():
                            st.markdown(f'''
                                <div class="metric-container">
                                    <div class="head">Vacancy Rate</div> 
                                    <div class="bottom">
                                        <div class="price">{vacancy_rate}</div>
                                        <div class="change">Change: -17%</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                         # Display the price trend over time as a graph
                        # price_trend_df = simulate_price_trend(predictions['house_value'][0])
                        # line_chart = alt.Chart(price_trend_df).mark_line().encode(
                        #     x='Date:T',
                        #     y='Price:Q'
                        # ).properties(width=1000)
                        # st.altair_chart(line_chart, use_container_width=True)
            else:
                st.write("Please enter the house price and select the location")



app()