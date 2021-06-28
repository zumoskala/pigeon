import pytest, os
import pandas as pd
import numpy as np
from pigeon import load_clean_excel

test_data = {'Type': ['Cake', 'Cupcake', 'Cake', 'Cupcake'],
             'Brand': ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4'],
             'Price': [1.25, 2, 3.22, 2.5],
             'Weight': [100, 110, 220, 115],
             'Sales_2020': [100, 200, 300, 400],
             'Sales_2021': [110, 220, 330, 440]
             }

test_df = pd.DataFrame(test_data, columns=['Type', 'Brand', 'Price', 'Weight', 'Sales_2020', 'Sales_2021'])


@pytest.mark.parametrize("path, data, coltype, header, engine, sheet_name",
                         [("Example.xlsx", test_df, {'Brand': str}, 0, 'openpyxl', 'Potato')])
def test_load_clean_excel(tmp_path, path, data, coltype, header, engine, sheet_name):
    test_path = os.path.join(tmp_path, path)
    data.to_excel(test_path)

    with pytest.raises(ValueError, match=f"Worksheet named '{sheet_name}' not found"):
        load_clean_excel(test_path, coltype, header, engine, sheet_name)


