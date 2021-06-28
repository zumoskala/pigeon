import pandas as pd


def grouped_stats(data, grouped_cols, calculation_col, mean_colname, min_colname, max_colname):
    """
    Calculate basic statistics and return results in the form of a new dataframe.
    :param data: dataframe
    :param grouped_cols: Array/String, columns of values used to group data
    :param calculation_col: String, name of the column which stats will be calculated
    :param mean_colname: String, chosen name for mean column
    :param min_colname: String, chosen name for min column
    :param max_colname: String, chosen name for max column
    :return: dataframe
    """
    mean = data.groupby(grouped_cols)[calculation_col].mean()
    minimum = data.groupby(grouped_cols)[calculation_col].min()
    maximum = data.groupby(grouped_cols)[calculation_col].max()

    tab = create_stat_df(mean_colname, mean, min_colname, minimum, max_colname, maximum)
    return tab


def compute_year_stats(data, phrase, mean_colname, min_colname, max_colname):
    """

    :param data: dataframe
    :param phrase: String, phrase used to select columns
    :param mean_colname: String, chosen name for mean column
    :param min_colname: String, chosen name for min column
    :param max_colname: String, chosen name for max column
    :return: dataframe
    """
    filter_col = [col for col in data if phrase in col]
    filter_col.sort()
    frame = data[filter_col]
    frame_mean = frame.mean(skipna=True)
    frame_min = frame.min(skipna=True)
    frame_max = frame.max(skipna=True)
    final_stats = create_stat_df(mean_colname, frame_mean, min_colname, frame_min, max_colname, frame_max)
    return final_stats


def create_stat_df(mean_colname, frame_mean, min_colname, frame_min, max_colname, frame_max):
    """
    Create dataframe with statistics: mean, min, max
    :param mean_colname: String, name of a column
    :param frame_mean: Array, mean
    :param min_colname: String, name of a column
    :param frame_min: Array, min
    :param max_colname: String, name of a column
    :param frame_max: Array, max
    :return: dataframe
    """
    frame_cols = {mean_colname: frame_mean, min_colname: frame_min, max_colname: frame_max}
    final_stats = pd.DataFrame(frame_cols)
    return final_stats


def save_xls(dict_df, path):
    """
    Save a dictionary of dataframes to an excel file, with each dataframe as a separate page
    :param dict_df: dictionary of data
    :param path: String, path to the output file
    """
    writer = pd.ExcelWriter(path)
    for key in dict_df:
        dict_df[key].to_excel(writer, key)

    writer.save()
    writer.close()
