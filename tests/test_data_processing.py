import pytest
import pandas as pd
import numpy as np
from pigeon.data_processing import reshape_to_row, join_rows, concat_cols, create_subdf, filter_by_column, sum_columns, \
    divide_cols, create_location_codes

test_column_data = {'Type': ['Cake', np.nan, np.nan, 'Cupcake', np.nan, np.nan],
                    'Brand': ['Brand 1', 'Sales_2020', 'Sales_2021', 'Brand 2', 'Sales_2020', 'Sales_2021'],
                    'Total': [3, 1, 2, 4, 2, 2]
                    }
d1 = {'Type': ['Cake', 'Cake', 'Cake', 'Cake'], 'Price': [10, 11, 12, 13]}
d2 = {'Type': ['Cupcake', 'Cupcake', 'Cupcake', 'Cupcake'], 'Price': [5, 6, 7, 8]}
test_data = {'Type': ['Cake', 'Cupcake', 'Cake', 'Cupcake'],
             'Brand': ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4'],
             'Price': [1.25, 2, 3.22, 2.5],
             'Weight': [100, 110, 220, 115],
             'Sales_2020': [100, 200, 300, 400],
             'Sales_2021': [110, 220, 330, 440]
             }

test_df = pd.DataFrame(test_data, columns=['Type', 'Brand', 'Price', 'Weight', 'Sales_2020', 'Sales_2021'])
test_columns_df = pd.DataFrame(test_column_data, columns=['Brand', 'Type', 'Total'])
test_df1 = pd.DataFrame(d1, columns=['Type', 'Price'])
test_df2 = pd.DataFrame(d2, columns=['Type', 'Price'])


@pytest.mark.parametrize("data, col_names, idx, cols, source_column, filler, vals",
                         [(test_columns_df, ['Brand', 'Type', 'Total'], 'Type', 'Num', 'Brand', 'Sum', ['Total'])])
def test_reshape_to_row(data, col_names, idx, cols, source_column, filler, vals):
    assert len(data[idx].dropna().unique()) == len(
        reshape_to_row(data, col_names, idx, cols, source_column, filler, vals))


@pytest.mark.parametrize("t1, t2", [(test_df1, test_df2)])
def test_join_rows(t1, t2):
    assert len(join_rows(t1, t2) == len(t1) + len(t2))


@pytest.mark.parametrize("data, colname, agg_functions", [(test_df, 'Type', {'Weight': 'mean'})])
def test_concat_cols(data, colname, agg_functions):
    assert len(concat_cols(data, colname, agg_functions)) == len(data[colname].dropna().unique())


@pytest.mark.parametrize("data, columns", [(test_df, ['Type', 'Pigeon']),
                                           (test_df, ['Type', 'Potato'])])
def test_create_subdf(data, columns):
    with pytest.raises(KeyError):
        create_subdf(data, columns)


@pytest.mark.parametrize("data, colname, filter_list", [(test_df, 'Type', {'Cake'})])
def test_filter_by_column(data, colname, filter_list):
    assert len(filter_by_column(data, colname, filter_list)) == len(data.loc[data[colname].isin(filter_list)])


@pytest.mark.parametrize("data, new_colname, col1, col2", [(test_df, 'Total sales', 'Sales_2020', 'Sales_2021')])
def test_sum_columns(data, new_colname, col1, col2):
    temp_df = sum_columns(data, new_colname, col1, col2)
    assert temp_df[new_colname].equals(data[col1] + data[col2])


@pytest.mark.parametrize("data, new_col, col1, col2", [(test_df, 'Price per gramm', 'Price', 'Weight')])
def test_divide_cols(data, new_col, col1, col2):
    temp_df = divide_cols(data, new_col, col1, col2)
    assert temp_df[new_col].equals(data[col1] / data[col2])


@pytest.mark.parametrize("data, type_to_code, dist_type_colname, dist_code_colname, code_colname, woj, pow, gm",
                         [(test_df, [1, 2], 'Product Code', 'Type', 'Type_Code', 'Type', 'Type', 'Type')])
def test_create_location_codes(data, type_to_code, dist_type_colname, dist_code_colname, code_colname, woj, pow, gm):
    with pytest.raises(TypeError, match=f"'list' object is not callable"):
        create_location_codes(data, type_to_code, dist_type_colname, dist_code_colname, code_colname, woj, pow, gm)

