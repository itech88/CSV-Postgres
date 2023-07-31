import pandas as pd


def transform_data_person_type_to_id(df, person_type):
    if person_type == "Provider":
        # add a new column 'employee_id' with default value 'Unknown'
        df.insert(0, "employee_id", "Unknown")
        # will manually enter IDs for now
        # need a way to get the employee_id from the employee_name
        # in the 'employee' table
    elif person_type == "Patient":
        # add a new column for 'patient_id' with default value 'Unknown'
        # will manually enter IDs for now
        # need a way to get the patient_id
        # from the patient_name in the 'patient' table
        df.insert(0, "patient_id", "Unknown")
    else:
        print(f"Person type is {person_type} type. Primary ID field will not be added.")

    return df
