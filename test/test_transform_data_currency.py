import sys
sys.path.append(
    "/Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/"
)
from transform_data_currency import transform_data_currency as tdc
import numpy as np
import pandas as pd
from icecream import ic, install
install() # this installs ic project wise to other modules


def test_transform_currency_columns():
    # Test data
    data = {
        'gross': ['$100.00', '$200.00'],
        'discounts': ['$10.00', '$20.00'],
        'name': ['A', 'B'],
        "taxes": ['$0.50,', '$40.00'], 
        "adjustments": ['$90.00', '$320.00'], 
        "net": ['$650.00', '$320.00'],  
        "amount": ['$880.00', '$320.00'],  
        "balance": ['$9000.00', '$3250.00'],  
        "total $ paid": ['$940.00', '$3220.00']
    }
    df = pd.DataFrame(data)
    
    transformed_df = tdc(df)
    
    assert transformed_df['gross'].dtype == 'float64'
    assert transformed_df['gross'].iloc[0] == 100.0
    assert transformed_df['discounts'].dtype == 'float64'
    assert transformed_df['discounts'].iloc[1] == 20.0
    assert transformed_df['total $ paid'].iloc[1] == 3220.0
    assert transformed_df['amount'].iloc[0] == 880.0
    assert transformed_df['adjustments'].iloc[1] == 320.0

def test_no_currency_columns():
    # Test data with no dollar columns
    data = {
        'name': ['A', 'B'],
        'age': [25, 30]
    }
    df = pd.DataFrame(data)
    
    transformed_df = tdc(df)
    
    assert 'gross' not in transformed_df.columns
    assert 'discounts' not in transformed_df.columns

def test_problematic_values():
    # Data with problematic value in 'gross' column
    data = {
        'gross': ['$100.00', np.nan],
        'discounts': ['$10.00', '$20.00'],
        'name': ['A', 'B']
    }
    df = pd.DataFrame(data)
    
    transformed_df = tdc(df)
    
    # Depending on your intention, assert for specific behavior. 
    # Here, assuming you expect a NaN value after conversion attempt:
    assert pd.isna(transformed_df['gross'].iloc[1])
