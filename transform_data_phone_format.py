import pandas as pd
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def format_phone(phone):
    phone_digits = ''.join(filter(str.isdigit, phone))

    if len(phone_digits) == 10:
        return f"{phone_digits[:3]}-{phone_digits[3:6]}-{phone_digits[6:]}"
    elif len(phone_digits) == 11 and phone_digits.startswith("1"):
        return f"{phone_digits[0]}-{phone_digits[1:4]}-{phone_digits[4:7]}-{phone_digits[7:]}"
    else:
        logger.warning(f"Irregular phone number detected: {phone}")
        return phone

@timer
def transform_data_phone_format(df):
    # each element in df["phone"] Series, value element passed to function as phone argument
    if "phone" in df.columns:
        df["phone"] = df["phone"].astype(str).apply(format_phone)
    else:
        logger.warning("No 'phone' column found. Nothing renamed.")

    return df

