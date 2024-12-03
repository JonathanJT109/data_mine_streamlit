import pandas as pd
import streamlit as st

from server import get_county_info, get_counties, get_percent_change

indiana_counties = get_counties("IN")
indiana_counties.sort()
colors = [
    "#FFAB91",
    "#C5E1A5",
    "#CE93D8",
    "#F06292",
    "#A1887F",
    "#7986CB",
    "#00ACC1",
]


def get_info(state: str, county: str):
    data = get_county_info(state, county)
    for key in data.keys():
        if data[key] is not None:
            data[key].index = pd.to_datetime(data[key].index)
    return data


def app():
    st.title("🏠 **County Market Information**")
    st.markdown(
        """
        Welcome to the **County Metrics Dashboard**! 🌟

        This app lets you explore detailed metrics for each county in **Indiana**, including key data on:

        - 🏡 **Housing** trends
        - 💼 **Employment** rates
        - 📈 **Economic indicators** and more!

        Simply choose a county from the dropdown, and the app will display various statistics such as housing prices, employment rates, and other important metrics.
    """
    )
    st.markdown("<hr>", unsafe_allow_html=True)  # Adds a line break after each error
    location = st.selectbox(
        "Select the location",
        indiana_counties,
        index=None,
        placeholder="Select a location",
    )
    search_button = st.button("Search")
    warn = st.empty()
    error_state = []
    for _ in range(5):
        error_state.append(st.empty())

    # QUESTION: Use Google Maps instead?
    # st.map()

    if search_button:
        if location is not None:
            county_data = get_info("IN", location)
            metrics = get_percent_change(county_data)
            st.header("Change of Metrics through Time")
            i = 0  # quick fix
            row1 = st.columns(3, vertical_alignment="center")
            row2 = st.columns(3, vertical_alignment="center")
            for key, metric in metrics.items():
                # name = key.upper().replace("_", " ")
                name = key
                current, change = metric
                current = current / 1000
                if "House Value" in key or "Rent Rate" in key:
                    if i > 2:
                        row2[i % 3].metric(name, f"${current:.2f}k", f"{change:.2f}%")
                    else:
                        row1[i % 3].metric(name, f"${current:.2f}k", f"{change:.2f}%")
                else:
                    if i > 2:
                        row2[i % 3].metric(name, f"{current:.2f}k", f"{change:.2f}%")
                    else:
                        row1[i % 3].metric(name, f"{current:.2f}k", f"{change:.2f}%")

                i = i + 1

            st.header("Graphs")
            i = 0
            j = 0
            row1 = st.columns(3, vertical_alignment="center")
            row2 = st.columns(3, vertical_alignment="center")
            for key, value in county_data.items():
                if value is not None:
                    if i > 2:
                        row2[i % 3].subheader(f"{key} in {location}")
                        row2[i % 3].line_chart(
                            value,
                            y_label=key,
                            x_label="Date",
                            color=colors[i],
                        )
                    else:
                        row1[i % 3].subheader(f"{key} in {location}")
                        row1[i % 3].line_chart(
                            value,
                            y_label=key,
                            x_label="Date",
                            color=colors[i],
                        )
                else:
                    error_state[j].error(
                        f"No {key} data found for this county.", icon="❌"
                    )
                    j = j + 1
                    i = i - 1
                i = i + 1
        else:
            warn.warning(
                "\tPlease enter the county you would like to explore.", icon="⚠️"
            )


app()
