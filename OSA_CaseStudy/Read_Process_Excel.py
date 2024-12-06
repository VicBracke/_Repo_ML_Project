import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

def read_excel_file(file_path):
    """
    Read an Excel file and return a pandas DataFrame.

    Parameters:
    file_path (str): The path to the Excel file.

    Returns:
    pandas.DataFrame: The DataFrame containing the data from the Excel file.

    Raises:
    Exception: If there is an error reading the Excel file.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def rename_columns(df, column_mapping):
    """
    Rename the columns of a DataFrame based on a column mapping.

    Parameters:
    df (pandas.DataFrame): The DataFrame to rename columns.
    column_mapping (dict): A dictionary mapping old column names to new column names.

    Returns:
    pandas.DataFrame: The DataFrame with renamed columns.
    """
    return df.rename(columns=column_mapping)

def explore_nan_values(df):
    """
    Explore NaN values in a DataFrame and visualize them.

    Parameters:
    df (pandas.DataFrame): The DataFrame to explore NaN values.

    Returns:
    None
    """
    # Check for NaN values in the DataFrame
    nan_values = df.isnull().sum()

    # Display the columns with NaN values
    print("Columns with NaN values:")
    print(nan_values[nan_values > 0])

    # Display the rows with NaN values
    print("Rows with NaN values:")
    print(df[df.isnull().any(axis=1)])

    # Visualize NaN values
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cmap='viridis', cbar=False)
    plt.title("NaN Values in DataFrame")
    plt.show()

column_mapping = {
    'Patient': 'Patient',
    'Gender': 'Gender',
    'IAH': 'IAH',
    'Peso': 'Weight',
    'Edad': 'Age',
    'Talla': 'Height',
    'PerCervical': 'Cervical',
}

filepath = "D:\OSA_COPILOT\DATA\Info_BDApnea_QuironMalaga.xlsx"

df = read_excel_file(filepath)

df = rename_columns(df, column_mapping)[list(column_mapping.values())]

# Display the column names
print(df.columns)

# Display the first few rows of the DataFrame 
print(df.head())

# Display the shape of the DataFrame
print(df.shape)

# Display the data types of the columns
print(df.dtypes)

# Assuming df is your DataFrame and 'Weight' is the column you're interested in
df['Weight_numeric'] = pd.to_numeric(df['Weight'], errors='coerce')

# Find rows where 'Weight_numeric' is NaN, indicating a non-numeric value in the 'Weight' column
non_numeric_rows = df[df['Weight_numeric'].isna()]

# Display these rows
print(non_numeric_rows)

# Drop the 'Weight_numeric' column if you no longer need it
df.drop('Weight_numeric', axis=1, inplace=True)

# Coerce 'Weight' to be numeric or NaN
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')

# Explore NaN values in the DataFrame
explore_nan_values(df)

# Drop rows with NaN values
df_cleaned = df.dropna()

# Assuming df_cleaned is a slice from another DataFrame, ensure it's a copy
df_cleaned = df_cleaned.copy()

# Display the shape of the cleaned DataFrame
print(df_cleaned.shape)

# Explore NaN values in the cleaned DataFrame
explore_nan_values(df_cleaned)

# Change the 'Gender' column to categorical
df_cleaned['Gender'] = df_cleaned['Gender'].astype('category')

# Change the 'Patient' column to categorical
df_cleaned['Patient'] = df_cleaned['Patient'].astype('category')

# Display the data types of the columns in the cleaned DataFrame
print(df_cleaned.dtypes)

# Replace -1 with NaN in the entire DataFrame
df_cleaned.replace(-1, np.nan, inplace=True)

# Drop rows with any NaN values (which were originally -1)
df_cleaned.dropna(inplace=True)

# Write the cleaned DataFrame to a new Excel file
output_filepath = "D:\OSA_COPILOT\DATA\OSA_DB_UPM.xlsx"
df_cleaned.to_excel(output_filepath, index=False)
