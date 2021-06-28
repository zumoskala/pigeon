import pandas as pd
import numpy as np


def reshape_to_row(data, col_names, idx, cols, source_column, filler, vals):
    """
    Use repeated values from one column as new columns, reshape dataframe.
    :param data: dataframe
    :param col_names: Array, names of columns to be used
    :param idx: String, column name to be used as index
    :param cols: String, column name to be used to create new columns
    :param source_column: String, name of the column
    :param filler: String, to fill empty term in created columns
    :param vals: Array/String, columns from initial df used as new df values
    :return: dataframe
    """
    # rename columns
    if col_names:
        data.columns = col_names

    # clean NaNs
    data_frame = data.replace(r'^\s*$', np.nan, regex=True)
    data_frame = data_frame.replace('X', np.nan)

    data_frame[cols] = data_frame.loc[data_frame[idx].isna(), source_column]
    data_frame[cols] = data_frame[cols].fillna(filler)

    data_frame[cols] = data_frame[cols].apply(lambda x: x.strip())
    data_frame[idx] = data_frame[idx].ffill()
    data_frame[idx] = data_frame[idx].astype(pd.StringDtype())
    data_frame = data_frame.pivot_table(index=idx, columns=cols,
                                        values=vals)
    return data_frame


def join_rows(*tables):
    """
    :param tables: list of dataframes
    :return: dataframe
    """
    table = pd.concat(tables, axis=0, ignore_index=True)
    return table


def concat_cols(data, colname, agg_functions):
    """

    :param data: dataframe
    :param colname: column name by which data to be aggregated will be grouped
    :param agg_functions: list of aggregation functions
    :return:
    """
    return data.groupby(data[colname]).aggregate(agg_functions)


def create_subdf(data, columns):
    """

    :param data: dataframe
    :param columns: selected columns
    :return: dataframe with only columns from columns argument

    """

    return data[columns]


def filter_by_column(data, colname, filter_list):
    """

    :param data: dataframe
    :param colname: name of the column according to which data will be filtered
    :param filter_list: list of element names accepted
    :return: filtered dataframe

    """
    return data[data[colname].isin(filter_list)]


def facility_proportions(data, fac_type_colname, student_amount_colname, fac_proportions=True):
    """
    Calculate proportions of:
     - facility type in all facilities
     - total students of facility type in all students

     If fac_proportions = True, sort by proportions of facility in all facilities,
     else sort by student proportions.

     """
    all_data = len(data)

    total_students = data[student_amount_colname].sum()

    facilities_type_list = data[fac_type_colname].unique()
    facilities_stats = []

    for facility in facilities_type_list:
        df_filtered = data[data[fac_type_colname] == facility]

        fac_students = df_filtered[student_amount_colname].sum()
        facilities_stats.append(
            {'facility': facility,
             'total': len(df_filtered),
             'proportions': len(df_filtered) / all_data,
             'students': fac_students,
             'students/total_students': fac_students / total_students
             })

    proportions_df = pd.DataFrame.from_dict(facilities_stats)
    proportions_df_sorted = proportions_df.sort_values(
        by=['proportions' if fac_proportions else 'students/total_students'])
    return proportions_df_sorted


def sum_columns(data, new_colname, *argv):
    """
    Sum columns into new column. ONLY FOR NUMERIC DATA.

    :param data: dataframe
    :param new_colname: name for the column to be created
    :param argv:columns that will be summed to create new column values
    :return: dataframe with new column

    """
    data[new_colname] = 0
    for arg in argv:
        data[new_colname] += data[arg]
    return data


def divide_cols(data, new_col, col1, col2):
    """

    :param data: dataframe
    :param new_col: name of the new column with proportions col1:col2
    :param col1: name of column that will be divided
    :param col2: name of column 2
    :return: dataframe with new column containing proportions of col1:col2
    """
    data[new_col] = (data[col1]) / (data[col2])

    return data


def create_location_codes(data, type_to_code, dist_type_colname, dist_code_colname, code_colname, woj, pow, gm):
    """
    Create location codes from codes of Województwo, Powiat, Gmina and type of Gmina
    :param data:
    :param type_to_code:
    :param dist_type_colname:
    :param dist_code_colname:
    :param code_colname:
    :param woj:
    :param pow:
    :param gm:
    :return:
    """
    data[dist_type_colname] = data[dist_code_colname].map(type_to_code)
    data[code_colname] = data[woj] + data[pow] + data[gm] + data[dist_type_colname]
    return data


def process_school_type(grouped_df, group_name, ages, curr_year, area_type):
    """

    :param grouped_df: grouped dataframe
    :param group_name: String - group name
    :param ages: Array - list of ages
    :param curr_year: int - current year
    :return: dataframe
    """
    selected = grouped_df.get_group(group_name)
    selected["Proportions"] = selected.groupby('Code').apply(
        lambda x: x['Uczniowie, wychow., słuchacze'] / x['Uczniowie, wychow., słuchacze'].sum()).values

    for age in ages:
        year = curr_year - age
        selected[str(year)] = selected[(area_type, str(age))]
        selected["Approximate_" + str(year)] = selected.groupby('Code').apply(
            lambda x: (1 / 3) * x[str(year)] * x['Proportions']).values

    return selected
