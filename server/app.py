import json
import os

import pandas as pd


def get_counties(state: str):
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/counties.json')
    with open(path, "r") as f:
        state = json.load(f)
    return state["counties"]


def get_house_values(state: str):
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/house_value.csv')
    house_values = pd.read_csv(path)
    return house_values


def get_rent_rates(state: str):
    path = os.path.join(os.path.dirname(__file__), f'data/{state}/rent_rates.csv')
    rent_rates = pd.read_csv(path)
    return rent_rates


def get_county_house_value(state: str, county: str):
    state_house_value = get_house_values(state)
    county_house_value = state_house_value.loc[
        (state_house_value["State"] == state) & (state_house_value["RegionName"] == county)]
    county_house_value = county_house_value.drop(
        ["RegionID", "SizeRank", "RegionName", "RegionType", "State", "StateName", "Metro", "StateCodeFIPS",
         "MunicipalCodeFIPS"], axis=1)
    county_house_value.dropna(inplace=True, axis=1)
    return county_house_value.T


def get_county_rent_rates(state: str, county: str):
    state_rent_rate = get_rent_rates(state)
    county_rent_rate = state_rent_rate.loc[
        (state_rent_rate["State"] == state) & (state_rent_rate["RegionName"] == county)]
    county_rent_rate = county_rent_rate.drop(
        ["RegionID", "SizeRank", "RegionName", "RegionType", "State", "StateName", "Metro", "StateCodeFIPS",
         "MunicipalCodeFIPS"], axis=1)
    county_rent_rate.dropna(inplace=True, axis=1)
    return county_rent_rate.T


if __name__ == "__main__":
    # counties = get_counties("indiana")
    # print(counties)
    df = get_county_house_value("IN", "Adams County")
    print(df.T.head())
