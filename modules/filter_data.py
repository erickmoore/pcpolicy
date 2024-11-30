def filter_column(df, column, filters, match_function, exclude=False):
    """
    Filters a DataFrame based on inclusion or exclusion criteria for a given column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column to apply the filter to (string or list of strings).
        filters (list): The list of filter strings to apply.
        match_function (callable): Function to determine match logic (`any` or `all`).
        exclude (bool): Whether to exclude matches instead of including them.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    
    filters_lower = [f.lower() for f in filters]  # Normalize filters to lowercase

    # Handle array-like columns (e.g., labels)
    if df[column].apply(lambda x: isinstance(x, (list, tuple))).any():
        condition = df[column].apply(lambda values: 
            match_function(
                match_function(f in value.lower() for f in filters_lower) 
                for value in values
            )
        )
    else:  # Handle string columns
        condition = df[column].str.lower().apply(lambda x: match_function(f in x for f in filters_lower))

    # Apply exclusion or inclusion
    return df[~condition] if exclude else df[condition]


# def filter_column(df, column, filters, match_function, exclude=False):
#     """
#     Filters a DataFrame based on inclusion or exclusion criteria for a given column.

#     Args:
#         df (pd.DataFrame): The DataFrame to filter.
#         column (str): The column to apply the filter to (string or list of strings).
#         filters (list): The list of filter strings to apply.
#         match_function (callable): Function to determine match logic (`any` or `all`).
#         exclude (bool): Whether to exclude matches instead of including them.

#     Returns:
#         pd.DataFrame: The filtered DataFrame.
#     """
    
#     filters_lower = [f.lower() for f in filters]  # Normalize filters to lowercase

#     # Handle array-like columns (e.g., labels)
#     if df[column].apply(lambda x: isinstance(x, (list, tuple))).any():
#         def check_match(values):
#             # Handle empty list case
#             if not values:
#                 return False  # Exclude empty label lists by default
            
#             # Check if any filter matches any label
#             return match_function(
#                 match_function(f in str(value).lower() for f in filters_lower) 
#                 for value in values
#             )
        
#         condition = df[column].apply(check_match)
#     else:  # Handle string columns
#         condition = df[column].str.lower().apply(lambda x: match_function(f in x for f in filters_lower))

#     # Apply exclusion or inclusion
#     return df[~condition] if exclude else df[condition]