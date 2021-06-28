import pandas as pd


def load_clean_excel(path, coltype, header=0, engine=None, sheet_name=0):
    """
    Load excel file, dropping fully empty columns
    :param path: String, path to the input file
    :param coltype: dictionary, set types of particular columns
    :param header: Int/Array, position of the beginning of dataframe
    :param engine: str, default None, openpyxl to support new excel formats
    :param sheet_name: str, int, list, or None, default 0, Sheet to be opened
    :return:
    """
    df = pd.read_excel(path, header=header, engine=engine, sheet_name=sheet_name, dtype=coltype)
    initial_count = len(df)

    # drop rows that are entirely empty
    df_clean = df.dropna(how='all')
    df_clean_count = len(df_clean)
    dropped = initial_count - df_clean_count

    print(f'Number of dropped empty rows: ${dropped}.')

    return df_clean


def load_multiple_sheets(path, header, na_vals):
    """
    Load excel file with multiple sheet as one dataframe
    :param path: String, path to the file
    :param header: Int/Array, position of the beginning of dataframe
    :param na_vals: String, NA values
    :return: dataframe
    """
    all_dfs = pd.read_excel(path, header=header, sheet_name=None, na_values=na_vals)
    concatenated = pd.concat(all_dfs, ignore_index=True)
    clean = concatenated.dropna(axis=1, how='all')
    return clean
