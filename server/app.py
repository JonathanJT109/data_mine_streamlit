import json
import os
import pickle

import pandas as pd


def get_counties(state: str):
    """
    Retrieves a list of counties for a given state from the 'counties.json' file.

    Args:
        state (str): The state for which to fetch counties (e.g., "Indiana").

    Returns:
        list: A list of counties in the specified state.

    Raises:
        FileNotFoundError: If the counties.json file for the state is missing.
        KeyError: If the 'counties' key is not found in the JSON data.
    """
    path = os.path.join(os.path.dirname(__file__), f"data/{state}/counties.json")
    with open(path, "r") as f:
        state_data = json.load(f)
    return state_data["counties"]


def get_house_values(state: str):
    """
    Loads house value data for a given state from the 'house_value.csv' file.

    Args:
        state (str): The state for which to fetch house values (e.g., "Indiana").

    Returns:
        pandas.DataFrame: A DataFrame containing house value data for the specified state.

    Raises:
        FileNotFoundError: If the house_value.csv file for the state is missing.
    """
    path = os.path.join(os.path.dirname(__file__), f"data/{state}/house_value.csv")
    house_values = pd.read_csv(path)
    return house_values


def get_rent_rates(state: str):
    """
    Loads rent rate data for a given state from the 'rent_rates.csv' file.

    Args:
        state (str): The state for which to fetch rent rates (e.g., "Indiana").

    Returns:
        pandas.DataFrame: A DataFrame containing rent rate data for the specified state.

    Raises:
        FileNotFoundError: If the rent_rates.csv file for the state is missing.
    """
    path = os.path.join(os.path.dirname(__file__), f"data/{state}/rent_rates.csv")
    rent_rates = pd.read_csv(path)
    return rent_rates


def get_employment(state: str):
    path = os.path.join(os.path.dirname(__file__), f"data/{state}/employment.csv")
    employment = pd.read_csv(path)
    return employment


def get_county_house_value(state: str, county: str):
    """
    Retrieves house value data for a specific county within a state.

    Args:
        state (str): The state in which the county is located (e.g., "Indiana").
        county (str): The county for which to fetch house values (e.g., "Adams County").

    Returns:
        pandas.DataFrame: A DataFrame containing house value data for the county. If no data
                          is found for the county, returns None.

    Raises:
        FileNotFoundError: If the required CSV files for house values are missing.
        ValueError: If the specified county is not found in the dataset.
    """
    state_house_value = get_house_values(state)

    # Filter the data for the specified county
    county_house_value = state_house_value.loc[
        (state_house_value["State"] == state)
        & (state_house_value["RegionName"] == county)
        ]

    # If no data is found for the county, return None
    if county_house_value.shape[0] == 0:
        return None

    # Clean the data by dropping unnecessary columns and rows with missing values
    county_house_value = county_house_value.drop(
        [
            "RegionID",
            "SizeRank",
            "RegionName",
            "RegionType",
            "State",
            "StateName",
            "Metro",
            "StateCodeFIPS",
            "MunicipalCodeFIPS",
        ],
        axis=1,
    )
    county_house_value.dropna(inplace=True, axis=1)

    # Rename the index for clarity
    county_house_value.index = ["Value"]

    return county_house_value.T["Value"]


def get_county_rent_rates(state: str, county: str):
    """
    Retrieves rent rate data for a specific county within a state.

    Args:
        state (str): The state in which the county is located (e.g., "Indiana").
        county (str): The county for which to fetch rent rates (e.g., "Adams County").

    Returns:
        pandas.DataFrame: A DataFrame containing rent rate data for the county. If no data is
                          found for the county, returns None.

    Raises:
        FileNotFoundError: If the required CSV files for rent rates are missing.
        ValueError: If the specified county is not found in the dataset.
    """
    state_rent_rate = get_rent_rates(state)

    # Filter the data for the specified county
    county_rent_rate = state_rent_rate.loc[
        (state_rent_rate["State"] == state) & (state_rent_rate["RegionName"] == county)
        ]

    # If no data is found for the county, return None
    if county_rent_rate.shape[0] == 0:
        return None

    # Clean the data by dropping unnecessary columns and rows with missing values
    county_rent_rate = county_rent_rate.drop(
        [
            "RegionID",
            "SizeRank",
            "RegionName",
            "RegionType",
            "State",
            "StateName",
            "Metro",
            "StateCodeFIPS",
            "MunicipalCodeFIPS",
        ],
        axis=1,
    )
    county_rent_rate.dropna(inplace=True, axis=1)

    # Rename the index for clarity
    county_rent_rate.index = ["Value"]

    return county_rent_rate.T["Value"]


def get_county_employment(state: str, county: str):
    """
    Retrieves employment data for a given county and state.

    This function pulls employment data from a state-level dataset and filters it
    for the specific county. The data is then cleaned by setting the 'Year' column
    as the index and dropping unnecessary columns. The function returns a list of
    DataFrames, each representing a different employment metric over time.

    Args:
        state (str): The name of the state (e.g., "California").
        county (str): The name of the county (e.g., "Los Angeles").

    Returns:
        list of pd.DataFrame: A list where each item is a DataFrame representing
                               a specific employment metric, with 'Year' and 'Value' columns.
                               If no data is available for the county, returns None.
    """
    state_employment = get_employment(state)
    geo = f"{county.split()[0]}, {state}"  # Assuming the first word of the county name is sufficient for matching
    county_employment = state_employment.loc[state_employment["GeoName"] == geo]
    county_employment.set_index("Year", inplace=True)
    county_employment = county_employment.drop("GeoName", axis=1)
    county_employment.dropna(inplace=True, axis=0)

    if county_employment.shape[0] == 0:
        return None

    county_employment.index = pd.to_datetime(county_employment.index.astype(str), format='%Y')

    employment = []
    for col in county_employment.columns:
        metric = county_employment[col]
        metric.columns = ["Year", "Value"]  # Renaming columns for clarity
        employment.append(metric)

    return employment


def open_model(name: str):
    """
    Opens a pre-trained model from a specified file.

    This function loads a pickle file containing a machine learning model or any other
    serialized object from disk. The model is expected to be located in the 'models' directory
    and is named according to the format 'model_{name}.pkl'.

    Args:
        name (str): The name of the model to be loaded (e.g., "housing_prediction").

    Returns:
        object: The deserialized model object.
    """
    path = os.path.join(os.path.dirname(__file__), f"models/model_{name}.pkl")
    with open(path, "rb") as f:
        data = pickle.load(f)
        return data


def get_county_info(state: str, county: str):
    """
    Retrieves a set of key county-level data metrics for a given state and county.

    This function combines data on various aspects of a county's economy, including house value,
    rent rates, employment, personal income, population, and wages and salaries. Each data type
    is retrieved by calling its respective function and is stored in a dictionary.

    Args:
        state (str): The name of the state (e.g., "California").
        county (str): The name of the county (e.g., "Los Angeles").

    Returns:
        dict: A dictionary containing the following metrics:
            - "House Value"
            - "Rent Rate"
            - "Personal Income"
            - "Population"
            - "Total Employment"
            - "Wages and Salaries"
          Each metric is associated with its corresponding data.
    """
    county_data = {}
    hv = get_county_house_value(state, county)
    rr = get_county_rent_rates(state, county)
    ind, pi, p, te, ws = get_county_employment(state, county)

    county_data["House Value"] = hv
    county_data["Rent Rate"] = rr
    county_data["Personal Income"] = pi
    county_data["Population"] = p
    county_data["Total Employment"] = te
    county_data["Wages and Salaries"] = ws

    return county_data


def get_percent_change(county_info: dict):
    """
    Calculates the percent change in each metric over the last 5 years.

    This function iterates through the dictionary of county-level metrics and calculates
    the percent change for each metric, comparing the most recent value to the value from
    5 years ago. The result is returned in a dictionary where each key represents the metric,
    and the value is a tuple containing:
    - The current metric value
    - The percent change compared to 5 years ago

    Args:
        county_info (dict): A dictionary containing county-level data (e.g., house value, rent rate, etc.).

    Returns:
        dict: A dictionary containing the percent change for each metric. The key is the metric name
              (e.g., 'house_value'), and the value is a tuple with the current value and the percent
              change over the last 5 years.
    """
    percent_change = {}
    for key, value in county_info.items():
        if value is not None:
            key_name = key.lower().replace(' ', '_')
            # (Current Metric, Change in Metric compared to 5 years)
            percent_change[key_name] = (value.iloc[-1], ((value.iloc[-1] - value.iloc[-5]) / value.iloc[-5] * 100))
    return percent_change


def get_county_owner(state: str, county: str):
    results = open_model("1")
    place_name = f"{county}, Indiana"  # Temporal fix
    results = results.loc[
        (results["Place Name"] == place_name)
    ]

    if results.shape[0] == 0:
        return None

    return results


if __name__ == "__main__":
    results = get_county_owner("IN", "Adams County")
    print(results["Year"])
    # counties = get_counties("indiana")
    # print(counties)
    # house = get_county_house_value("IN", "Adams County")
    # print(house)
    # info = get_county_info("IN", "Adams County")
    # change = get_percent_change(info)
    # print(change)
    # emp = get_county_employment("IN", "Adams County")
    # print(emp[0].index)
