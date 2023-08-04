import pandas as pd
import transform_data_person_type_to_id


def transform_data_full_name_to_id(df):
    person_type = ""
    # if the first column is 'Provider' or 'Providers'
    # split the 'Providers' column into 'first_name' and 'last_name' columns
    if df.columns[0] == "Provider":
        df[["last_name", "first_name"]] = df["Provider"].str.split(
            ", ", n=1, expand=True
        )
        person_type = "Provider"
    elif df.columns[0] == "Providers":
        df[["last_name", "first_name"]] = df["Providers"].str.split(
            ", ", n=1, expand=True
        )
        person_type = "Provider"
    elif df.columns[0] == "Patient":
        # if the first column is 'Patient'
        # split the 'Patient' column into 'first_name' and 'last_name' columns
        df[["last_name", "first_name"]] = df["Patient"].str.split(
            ", ", n=1, expand=True
        )
        person_type = "Patient"
    else:
        # if the first column is not 'Provider' or 'Patient'
        print("The first column is not 'Provider(s)' or 'Patient; Cannot parse name: ")
        person_type = "Unknown"

    # remove the former named first column
    if person_type == "Provider":
        print("Provider detected")
        df.drop("Providers", axis="columns", inplace=True)
        print("Dropped Providers column")
    elif person_type == "Patient":
        print("Patient detected")
        df.drop("Patient", axis="columns", inplace=True)
        print("Dropped Patient column")
    else:
        print("Unknown person type, first column will not be dropped.")

    # add a new column 'employee_id' and drop the former named first column
    transform_data_person_type_to_id.transform_data_person_type_to_id(df, person_type)

    return df
