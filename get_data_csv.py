import pandas as pd


def get_data_csv():
    data = pd.read_csv("data.csv")
    return data
