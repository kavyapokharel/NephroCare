import pandas as pd
from datetime import datetime
import ollama 

def call(user, model='healthSummarizerFinal', appointmentDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\appointments.xlsx', goalDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\goals.xlsx', expenditureDB=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\expenditure.xlsx'):
    """
    Reads and filters data by 'user', formats it into the concise structured input, 
    and calls the specified Ollama model for a personalized health summary.
    
    Args:
        user (str): The patient's name used to filter appointment, goal, and expenditure logs.
        model (str): The name of the Ollama model (default 'gravenessScorer').
        appointmentDB (str): File path for the appointments database.
        goalDB (str): File path for the goals database.
        expenditureDB (str): File path for the expenditure database.
    """
    
    # --- 1. Data Loading ---
    try:
        app_df = pd.read_excel(appointmentDB)
        goal_df = pd.read_excel(goalDB)
        exp_df = pd.read_excel(expenditureDB)
    except FileNotFoundError as e:
        return f"Error: Database file not found: {e.filename}"
    except Exception as e:
        return f"An error occurred while reading files: {e}"

    # --- 2. Data Filtering by User ---
    
    # Filter appointments where the patient column matches the user
    user_appointments_df = app_df[app_df['patient'] == user].copy()
    
    # Filter goals where the patient column matches the user
    user_goals_df = goal_df[goal_df['patient'] == user].copy()
    
    # Filter expenditures where the patient column matches the user
    user_exp_df = exp_df[exp_df['patient'] == user].copy()


    # --- 3. Data Formatting for Prompt ---

    # A. Appointments
    appointments_list = []
    for t in user_appointments_df['time'].tolist():
        try:
            dt = pd.to_datetime(t)
            appointments_list.append(dt.strftime('%Y-%m-%d'))
        except:
            appointments_list.append(str(t))

    appointments_str = str(appointments_list)


    # B. Goals
    goals_parts = []
    unique_goals = user_goals_df['Goal'].unique()
    
    for goal_def in unique_goals:
        log_df = user_goals_df[user_goals_df['Goal'] == goal_def]
        
        # Log completed days (True)
        completed_dates = log_df[log_df['completion'] == True]['day'].tolist()
        
        # Log not completed days (False) - Added as it's relevant log data
        not_completed_dates = log_df[log_df['completion'] == False]['day'].tolist()
        
        # Format the log to include both completed and not completed days
        log_data = {
            "Completed": completed_dates, 
            "Not Completed": not_completed_dates
        }
        log_str = str(log_data)
        
        # The prompt structure: [a definition of a healthy goal followed by a list...]
        goals_parts.append(f"{goal_def}: {log_str}")
    
    goals_str = " | ".join(goals_parts)
    if not goals_str:
        goals_str = "No defined goals."


    # C. Expenditure
    # Create the required list of tuples (item, date, price)
    expenditure_list = []
    for index, row in user_exp_df.iterrows():
        # Handle date conversion
        date_val = row['date']
        if isinstance(date_val, datetime):
            date_str = date_val.strftime('%Y-%m-%d')
        else:
            try:
                date_str = pd.to_datetime(date_val).strftime('%Y-%m-%d')
            except:
                date_str = str(date_val)

        expenditure_list.append(
            (row['item'], date_str, round(row['price'], 2))
        )

    expenditure_str = str(expenditure_list)

    # --- 4. Construct the Concise, Structured Input ---
    
    # The final input must match the exact format the model was trained on.
    structured_input_prompt = (
        f"\"Appointments: {appointments_str}\n"
        f"Goals: {goals_str}\n"
        f"Expenditure: {expenditure_str}\n"
        "\""
    )
    
    # --- 5. Call the Ollama Model ---
    try:
        client = ollama.Client()
        response = client.generate(model=model, prompt=structured_input_prompt)
        
        # The response is typically in the 'response' key
        summary = response['response']
        return summary
    
    except ollama.OllamaError as e:
        # Handle specific Ollama connection or model errors
        return f"Error calling Ollama model '{model}': {e}"
    except Exception as e:
        # Catch other unexpected errors
        return f"An unexpected error occurred during the Ollama call: {e}"