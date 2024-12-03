import numpy as np
import pandas as pd
import streamlit as st

from server import (
    get_county_info,
    get_counties, get_percent_change
)

indiana_counties = get_counties("IN")
indiana_counties.sort()


def get_info(state: str, county: str):
    data = get_county_info(state, county)
    return data


def app():
    st.title("County Market Information")
    location = st.selectbox(
        "Select the location",
        indiana_counties,
        index=None,
        placeholder="Select a location",
    )
    search_button = st.button("Search")
    warn = st.empty()

    # QUESTION: Use Google Maps instead?
    st.map()

    if search_button:
        if location is not None:
            county_data = get_info("IN", location)
            metrics = get_percent_change(county_data)
            for key, metric in metrics.items():
                name = key.upper().replace('_', ' ')
                current, change = metric
                st.metric(name, f"{current:.2f}", f"{change:.2f}%")

            st.header("Change of Metrics through Time")
            for key, value in county_data.items():
                if value is not None:
                    st.subheader(f"{key} in {location}")
                    st.line_chart(
                        value,
                        y_label=key,
                        x_label="Date",
                    )
                else:
                    st.error(f"No {key} data found for this county.")
        else:
            warn.warning(
                "\tPlease enter the county you would like to explore.", icon="⚠️"
            )


app()
