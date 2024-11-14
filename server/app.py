import json
import os

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
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/counties.json')
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
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/house_value.csv')
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
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/rent_rates.csv')
    rent_rates = pd.read_csv(path)
    return rent_rates


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
        (state_house_value["State"] == state) & (state_house_value["RegionName"] == county)
        ]

    # If no data is found for the county, return None
    if county_house_value.shape[0] == 0:
        return None

    # Clean the data by dropping unnecessary columns and rows with missing values
    county_house_value = county_house_value.drop(
        ["RegionID", "SizeRank", "RegionName", "RegionType", "State", "StateName", "Metro",
         "StateCodeFIPS", "MunicipalCodeFIPS"], axis=1)
    county_house_value.dropna(inplace=True, axis=1)

    # Rename the index for clarity
    county_house_value.index = ["Value"]

    return county_house_value.T


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
        ["RegionID", "SizeRank", "RegionName", "RegionType", "State", "StateName", "Metro",
         "StateCodeFIPS", "MunicipalCodeFIPS"], axis=1)
    county_rent_rate.dropna(inplace=True, axis=1)

    # Rename the index for clarity
    county_rent_rate.index = ["Value"]

    return county_rent_rate.T

if __name__ == "__main__":
    # counties = get_counties("indiana")
    # print(counties)
    df = get_county_rent_rates("IN", "Adams County")
    print(df.head())
    print(df.tail())
