import pandas as pd
import random
import logging
import string
import numpy as np 
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    Generates a random log entry with a timestamp, log level, action and user.
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d  %H:%M:%S")
    log_level = random.choice(["INFO", "DEBUG", "ERROR", "WARNING"])
    action = random.choice(["Login", "Logout", "Data Request", "File Upload", "Download", "Error"])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # Random 6 characters user id will be formed
    return f"{timestamp} - {log_level} - {action} - {user}"

# Fuction to write logs to a file
def write_logs_to_file(log_filename, num_entries=100):
    """
    Write the specified number of logs in the given file.
    """
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')
        print(f"Logs have been successfully written to the file {log_filename}")
    except Exception as e:
        logging.error(f"Error in write_logs_to_file: {e}")
        print("An error occured while writing logs to the file.")

# Function to read the log file and process it.
def load_and_process_logs(log_filename="generated_logs.txt"):
    """"
    Loads and processes the logs from the given file, cleaning and parsing the timestamps.
    """
    try:
        # Read the log file into a Pandas DataFrame, splitting by the ' - ' separator
        df = pd.read_csv(log_filename, sep=' - ', header=None, names=["Timestamp", "Log_Level", "Action", "User"], engine='python')

        # Clean and trim spaces around the timestamp
        df['Timestamp'] = df['Timestamp'].str.strip()

        # Convert the timestamp column to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # Drop rows with invalid timestamp
        df = df.dropna(subset=['Timestamp'])

        if df.empty:
            print("No valid data found after timestamp conversion.")
        else:
            print("Data after timestamp conversion: ")
            print(df.head())  # Show the data after clening

        # Set the timestamp column as the index for time-based operations/calculations
        df.set_index('Timestamp', inplace=True)

        return df
    except Exception as e:
        print(f"Error processing log file: {e}")
        return None

# Function to perform basic statical analysis using Pandas and Numpy
def analyze_data(df):
    """
    Perform the basic analysis, such as counting log levels and actions, and computing basic statistic such as mean, max, etc.
    """
    try:
        if df is None or df.empty:
            print("No data available for analysis.")
            return None, None
        
        # Count the occurance of each log level
        log_level_counts = df['Log_Level'].value_counts()

        # Count the occurrences of each action
        action_counts = df['Action'].value_counts()

        log_count = len(df)  # TOtal no of logs
        unique_users = df['User'].nunique()   # Number of unique users
        logs_per_day = df.resample('D').size()   # Number of logs per day

        # Averages of actions per day
        average_logs_per_day = logs_per_day.mean()

        # Max logs per day
        max_logs_per_day = logs_per_day.max()

        # Display summary statistics
        print("\nLog Level Counts:\n", log_level_counts)
        print("\nAction Counts:\n", action_counts)
        print(f"\nTotal Number of Logs: {log_count}")
        print(f"Number of unique Users: {unique_users}")
        print(f"Average Logs per Day: {average_logs_per_day:.2f}")
        print(f"Maximum Logs Per Day: {max_logs_per_day}")

        # Create a dictionary to return the analysis results
        stats = {
            "log_level_counts": log_level_counts,
            "action_counts": action_counts,
            "total_number_of_logs": log_count,
            "number_of_unique_users": unique_users,
            "average_logs_per_day": average_logs_per_day,
            "maximum_logs_per_day": max_logs_per_day
        }
         
        return stats
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None
    
# Function to visualize trends over time using Matplotlib
def visualize_trends(df):
    """
    Visualises log frequency trends over time using Matplotlib.
    """
    try:
        # Resample data to get the number of logs per day
        logs_by_day = df.resample('D').size()

        # Plotting log frequency over time using Matplotlib
        plt.figure(figsize=(10,5))
        plt.plot(logs_by_day.index, logs_by_day.values, marker='o', linestyle='-', color='b')

        # Customize the plot
        plt.title("Log Frequency Over Time")
        plt.xlabel('Date')
        plt.ylabel('Number of Logs')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Show the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error visualising data: {e}")

log_filename = 'generated_logs.txt' # Assumed that this file exists

#Step 1: Write random logs to the file
write_logs_to_file(log_filename, num_entries=200)

#Step 2: Load and process the logs from the file
df_logs = load_and_process_logs(log_filename)

#Step 3: Perform basic analysis on the log data
if df_logs is not None:
    stats = analyze_data(df_logs)

    #Step 4: Visualise trends over time
    visualize_trends(df_logs)
    