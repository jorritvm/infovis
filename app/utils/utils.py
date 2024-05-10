"""
this module contains utilities functions for the app
"""


def filter_data(df, continent, sub_region, country, status, itype, time_range):
    """
    Filter the provided dataframe based on the values of the provided filters
    Args:
        df:
        continent: string
        sub_region: string
        country: string
        status: list of string
        itype: list of string
        time_range: tuple (int, int)

    Returns:
        a filtered df
    """
    # # keep this output for debug purposes
    # print(continent)
    # print(sub_region)
    # print(country)
    # print(status)
    # print(itype)
    # print(time_range)

    # Filter DataFrame based on status and time range
    filtered_df = df.copy()

    # Filter by active continent
    if continent != "Total":
        filtered_df = filtered_df[filtered_df["Region"] == continent]

    # Filter by sub region
    if sub_region is not None and sub_region != "":
        filtered_df = filtered_df[filtered_df["Subregion"] == sub_region]

    # Filter by country
    if country is not None and country != "":
        filtered_df = filtered_df[filtered_df["Country"] == country]

    # Filter by status
    if status is not None and status != []:
        filtered_df = filtered_df[filtered_df["Status"].isin(status)]

    # Filter by type
    if itype is not None and itype != []:
        filtered_df = filtered_df[filtered_df["Installation Type"].isin(itype)]

    # Filter by time range
    if time_range is not None:
        start_year, end_year = time_range
        filtered_df = filtered_df[(filtered_df["Start year"] >= start_year) & (filtered_df["Start year"] <= end_year)]

    return filtered_df

