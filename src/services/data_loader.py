# src/services/data_loader.py
import pandas as pd
from typing import Optional
import os

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file and returns it as a pandas DataFrame.
    
    :param file_path: Path to the CSV file.
    return: DataFrame with the loaded data.
    :raises FileNotFoundError: If the file does not exist.
    :raises PermissionError: If you don't have permissions to read the file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} doesn't exist.")
    try:
        df = pd.read_csv(file_path)
    except PermissionError as e:
        raise PermissionError(f"We don't  have permisson for read the files {file_path}.") from e
    
    return df

def load_excel(file_path: str, sheet_name: Optional[str] = None ) -> pd.DataFrame:
    """
    Loads data from an Excel file (XLSX or XLS) and returns it as a DataFrame.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet to read (optional).
    :return: DataFrame with the loaded data.
    :raises FileNotFoundError: If the file does not exist.
    :raises PermissionError: If you do not have permissions to read the file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} doesn't exist.")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except PermissionError as e:
        raise PermissionError(f"We don't have permisson for read the file {file_path}.") from e
    
    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates and cleanses the data in a DataFrame.
    
    Clean-up tasks:
    - Remove duplicates.
    - Handle null values (here you choose to remove rows with nulls, but you can adapt the logic).
    - (Optional) Convert columns to appropriate types, if necessary.
    
    Param df: DataFrame to validate.
    return: DataFrame cleaned and validated.
    """
    # Remove duplicates
    df.drop_duplicates()

    # Handling null values: deleting rows with nulls
    df.dropna()

    # Example: if there is a ‘date’ column, convert it to datetime if it exists.
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime( df["fecha"], errors ="coerce")
        # Delete rows where the date could not be converted
        df = df.dropna(subset=["fecha"])

    return df