import pandas as pd
from datetime import datetime
import os

def addBPLog(date, systolic, diastolic, file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Blood Pressure.xlsx'):
    """
    Adds or updates a blood pressure record (systolic, diastolic) for a given date 
    in the specified Excel file, dropping older records with the same date.

    Args:
        date (str/datetime): The date of the measurement.
        systolic (int): The systolic blood pressure reading.
        diastolic (int): The diastolic blood pressure reading.
        file (str): The path to the Blood Pressure Excel file.
    """
    try:
        # 1. Convert the date to a standardized datetime object
        if isinstance(date, str):
            # Attempt to parse common date formats
            date_dt = pd.to_datetime(date).normalize()
        elif isinstance(date, datetime):
            date_dt = date.date()
        else:
            raise ValueError("Date argument must be a string or datetime object.")

        # 2. Define the new record
        new_record = pd.DataFrame({
            'date': [date_dt],
            'systolic': [systolic],
            'diastolic': [diastolic]
        })

        # 3. Read existing data or create an empty DataFrame if file is new
        try:
            df_existing = pd.read_excel(file)
            # Ensure 'date' is standardized for comparison
            df_existing['date'] = pd.to_datetime(df_existing['date']).dt.normalize()
        except FileNotFoundError:
            print(f"File '{file}' not found. Creating a new file.")
            df_existing = pd.DataFrame(columns=['date', 'systolic', 'diastolic'])

        # 4. Append the new record
        df_combined = pd.concat([df_existing, new_record], ignore_index=True)
        df_combined['date'] = df_combined['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # 5. Drop entries with duplicate dates, keeping the last (newest) record
        # Normalize date to keep only the date part for deduplication
        df_combined = df_combined.drop_duplicates(subset=['date'], keep='last')

        # 6. Save the updated DataFrame back to the Excel file
        df_combined.to_excel(file, index=False)
        print(f"Successfully added/updated Blood Pressure log for date: {date_dt.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f"An error occurred in addBPLog: {e}")

# --------------------------------------------------------------------------

def addWeightOrSugarLog(for_type, date, measurement):
    """
    Adds or updates a body weight or blood sugar measurement for a given date 
    in the appropriate Excel file, dropping older records with the same date.

    Args:
        for_type (str): 'sugar' or 'weight' to determine the file and column.
        date (str/datetime): The date of the measurement.
        measurement (float/int): The numerical measurement value.
    """
    for_type = for_type.lower()
    
    if for_type == 'weight':
        file = r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Body Weight.xlsx'
        column = 'weight'
    elif for_type == 'sugar':
        file = r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Blood Sugar.xlsx'
        column = 'blood sugar (mg/dL)'
    else:
        print("Error: 'for' argument must be 'sugar' or 'weight'.")
        return

    try:
        # 1. Convert the date to a standardized datetime object
        if isinstance(date, str):
            date_dt = pd.to_datetime(date).normalize()
        elif isinstance(date, datetime):
            date_dt = date.date()
        else:
            raise ValueError("Date argument must be a string or datetime object.")

        # 2. Define the new record
        new_record = pd.DataFrame({
            'date': [date_dt],
            column: [measurement]
        })

        # 3. Read existing data or create an empty DataFrame if file is new
        try:
            df_existing = pd.read_excel(file)
            df_existing['date'] = pd.to_datetime(df_existing['date']).dt.normalize()
        except FileNotFoundError:
            print(f"File '{file}' not found. Creating a new file.")
            df_existing = pd.DataFrame(columns=['date', column])

        # 4. Append the new record
        df_combined = pd.concat([df_existing, new_record], ignore_index=True)
        df_combined['date'] = df_combined['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # 5. Drop entries with duplicate dates, keeping the last (newest) record
        df_combined = df_combined.drop_duplicates(subset=['date'], keep='last')

        # 6. Save the updated DataFrame back to the Excel file
        df_combined.to_excel(file, index=False)
        print(f"Successfully added/updated {for_type.capitalize()} log for date: {date_dt.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f"An error occurred in addWeightOrSugarLog: {e}")


def goalList(file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\goals.xlsx'):
    file = pd.read_excel(file)
    return tuple(file['Goal'].unique())


def goalLog(goal, file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\goals.xlsx'):
    file = pd.read_excel(file)
    file = file[file['Goal'] == goal]
    return file[['day', 'completion']].to_string()