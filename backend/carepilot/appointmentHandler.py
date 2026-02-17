import pandas as pd
from datetime import datetime, date

def appointmentList(from_date_str, to_date_str, doctor, appointmentDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\appointments.xlsx'):
    """
    Returns a list of available appointment dates for a specific doctor
    within a given time range.
    """
    try:
        df = pd.read_excel(appointmentDB)
        
        # 1. Convert 'time' column to datetime objects
        # Format 'yy/mm/dd' is inferred as Y/m/d by pandas, which is correct here
        df['time_dt'] = pd.to_datetime(df['time'], format='%y/%m/%d %H:%M:%S')
        
        # 2. Convert string arguments to datetime objects for comparison
        # Assuming the input strings match a recognizable datetime format (e.g., '2024-02-10')
        from_dt = pd.to_datetime(from_date_str)
        to_dt = pd.to_datetime(to_date_str)
        
        # 3. Filter the DataFrame
        # Filter 1: By Doctor
        doctor_filter = (df['doctor'] == doctor)
        
        # Filter 2: By Date Range (inclusive)
        # We compare only the date parts for a fair range comparison
        date_range_filter = (df['time_dt'].dt.date >= from_dt.date()) & \
                            (df['time_dt'].dt.date <= to_dt.date())
        
        # Filter 3: Check for empty 'patient' column (Available appointment)
        patient_filter = (df['patient'].isna()) | (df['patient'] == '')
        
        # Combine all filters
        available_appointments = df[doctor_filter & date_range_filter & patient_filter]
        
        # 4. Format the output dates
        # Desired format: "[Month] [Day], [Year]" (e.g., "February 10, 2024")
        date_strings = available_appointments['time_dt'].dt.strftime('%B %d, %Y %H:%M:%S').tolist()
        
        return date_strings

    except FileNotFoundError:
        print(f"Error: Database file '{appointmentDB}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred in appointmentList: {e}")
        return []


def addAppointment(time_str, doctor, user, appointmentDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\appointments.xlsx'):
    """
    Books an appointment by updating the empty 'patient' column with the 'user' name.
    """
    try:
        df = pd.read_excel(appointmentDB)
        
        # 1. Convert input 'time_str' to datetime object in 'yy/mm/dd' format
        # Input format: "[month] [day], [year]" (e.g., "February 10, 2024")
        # Output format for comparison: 'yy/mm/dd' (e.g., '24/02/10')
        dt_obj = datetime.strptime(time_str, '%B %d, %Y')
        time_for_comparison = dt_obj.strftime('%y/%m/%d %H:%M:%S')
        
        # 2. Find the row to update
        # Find the index where 'time' and 'doctor' match AND 'patient' is empty
        condition = (df['time'] == time_for_comparison) & \
                    (df['doctor'] == doctor) & \
                    ((df['patient'].isna()) | (df['patient'] == ''))
        
        # Check if an available appointment exists
        if not df[condition].empty:
            # 3. Update the 'patient' column for the matching rows
            df.loc[condition, 'patient'] = user
            
            # 4. Write the updated DataFrame back to the Excel file
            df.to_excel(appointmentDB, index=False)
            return f"Appointment booked successfully for {user} with {doctor} on {time_str}."
        else:
            return f"Error: Appointment slot on {time_str} with {doctor} is already taken or does not exist."

    except ValueError:
        return f"Error: Time string '{time_str}' is not in the required '[month] [day], [year]' format."
    except FileNotFoundError:
        return f"Error: Database file '{appointmentDB}' not found."
    except Exception as e:
        return f"An error occurred in addAppointment: {e}"



def cancelAppointment(time_str, doctor, user, appointmentDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\appointments.xlsx'):
    """
    Cancels an appointment by setting the 'patient' column back to empty.
    """
    try:
        df = pd.read_excel(appointmentDB)
        
        # 1. Convert input 'time_str' to datetime object in 'yy/mm/dd' format
        # Input format: "[month] [day], [year]" (e.g., "February 10, 2024")
        dt_obj = datetime.strptime(time_str, '%B %d, %Y')
        time_for_comparison = dt_obj.strftime('%y/%m/%d')
        
        # 2. Find the row to update
        # Find the index where 'time', 'doctor', and 'patient' (user) match
        condition = (df['time'] == time_for_comparison) & \
                    (df['doctor'] == doctor) & \
                    (df['patient'] == user)
        
        # Check if the specific appointment exists
        if not df[condition].empty:
            # 3. Update the 'patient' column to an empty string
            df.loc[condition, 'patient'] = ''
            
            # 4. Write the updated DataFrame back to the Excel file
            df.to_excel(appointmentDB, index=False)
            return f"Appointment cancelled successfully for {user} with {doctor} on {time_str}."
        else:
            return f"Error: No appointment found for {user} with {doctor} on {time_str} to cancel."

    except ValueError:
        return f"Error: Time string '{time_str}' is not in the required '[month] [day], [year]' format."
    except FileNotFoundError:
        return f"Error: Database file '{appointmentDB}' not found."
    except Exception as e:
        return f"An error occurred in cancelAppointment: {e}"
    

def bookedAppointmentList(from_date_str, to_date_str, doctor, appointmentDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\appointments.xlsx'):
    """
    Returns a list of available appointment date-times for a specific doctor
    within a given date range.
    """
    try:
        df = pd.read_excel(appointmentDB)

        # 1. Convert 'time' column to datetime
        df['time_dt'] = pd.to_datetime(df['time'], format='%y/%m/%d %H:%M:%S')

        # 2. Convert input strings to datetime
        from_dt = pd.to_datetime(from_date_str)
        to_dt = pd.to_datetime(to_date_str)

        # 3. Apply filters
        doctor_filter = df['doctor'] == doctor

        date_range_filter = (
            (df['time_dt'].dt.date >= from_dt.date()) &
            (df['time_dt'].dt.date <= to_dt.date())
        )

        # Patient is empty OR patient == 'Sugam'
        patient_filter = (df['patient'] == 'Sugam')

        # Combined filters
        available = df[doctor_filter & date_range_filter & patient_filter]

        # 4. Format dates
        return available['time_dt'].dt.strftime('%B %d, %Y %H:%M:%S').tolist()

    except Exception as e:
        print("Error:", e)
        return []