import pytest, os
import pandas as pd
from pigeon.data_stats import grouped_stats, compute_year_stats, save_xls

test_data = {'Type': ['Cake', 'Cupcake', 'Cake', 'Cupcake'],
             'Brand': ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4'],
             'Price': [1.25, 2, 3.22, 2.5],
             'Weight': [100, 110, 220, 115],
             'Sales_2020': [100, 200, 300, 400],
             'Sales_2021': [110, 220, 330, 440]
             }
test_df = pd.DataFrame(test_data, columns=['Brand', 'Type', 'Price', 'Weight', 'Sales_2020', 'Sales_2021'])


@pytest.mark.parametrize("data, grouped_cols, calculation_col, mean_colname, min_colname, max_colname",
                         [(test_df, 'Type', 'Type', 'mean', 'min', 'max'),
                          (test_df, 'Type', 'Brand', 'mean', 'min', 'max')])
def test_grouped_stats(data, grouped_cols, calculation_col, mean_colname, min_colname, max_colname):
    with pytest.raises(Exception, match=f"No numeric types to aggregate"):
        grouped_stats(data, grouped_cols, calculation_col, mean_colname, min_colname, max_colname)


@pytest.mark.parametrize("data, phrase, mean_colname, min_colname, max_colname",
                         [(test_df, 'Blob', 'mean', 'min', 'max'),
                          (test_df, 'Potato', 'mean', 'min', 'max')])
def test_compute_year_stats(data, phrase, mean_colname, min_colname, max_colname):
    assert len(compute_year_stats(data, phrase, mean_colname, min_colname, max_colname)) == 0


@pytest.mark.parametrize("test_df, dict_df, filename", [(test_df, {"Cake": test_df}, "TestFile.xlsx")])
def test_save_xls(test_df, dict_df, filename, tmp_path):
    # create test path
    output_path = os.path.join(tmp_path, filename)

    # save example file
    save_xls(dict_df, output_path)

    # read saved file
    test_frame = pd.read_excel(output_path, index_col=[0])

    # compare with test_df
    assert test_df.equals(test_frame)
