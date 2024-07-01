import re
import sqlite3

def validate_input(pattern, input_string):
    """Validates input based on the provided regex pattern."""
    if re.match(pattern, input_string):
        return True
    return False

def float_to_time(time_float):
    """Converts float to time in HH:MM:SS format."""
    hours = int(time_float)
    minutes = int((time_float * 60) % 60)
    seconds = int((time_float * 3600) % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def connect_and_insert(database, table, data):
    """Connects to database and inserts the provided data."""
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            task TEXT,
            working_hours TEXT
        )
        """)
        
        cursor.execute(f"""
        INSERT INTO {table} (name, task, working_hours) 
        VALUES (?, ?, ?)
        """, data)
        
        conn.commit()
        print("Data has been successfully inserted into the database.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def main():
    name = input("Enter your name: ")
    task_count = int(input("Enter the number of tasks you want to do: "))

    tasks = []
    total_hours = 0.0

    for _ in range(task_count):
        while True:
            print("Please choose your tasks:")
            print("LG : Login")
            print("RG : Register")
            print("US : User")
            print("EMP : Employee")
            print("TS : Timesheets")
            
            task = input("Choose a task: ").strip()
            if task not in ['LG', 'RG', 'US', 'EMP', 'TS']:
                print("Invalid input, please try again!")
                continue

            hours = input("Enter your working hour (in float, e.g. 1.5 for 1 hour 30 minutes): ")
            if not validate_input(r'^\d+(\.\d+)?$', hours):
                print("Invalid input, please try again!")
                continue

            hours_float = float(hours)
            total_hours += hours_float
            tasks.append((task, hours_float))
            break

    print(f"\nSummary of Tasks for {name}:")
    for task, hours in tasks:
        converted_time = float_to_time(hours)
        print(f"Task: {task}, Working Hours: {hours} ({converted_time})")

    total_time = float_to_time(total_hours)
    print(f"\nTotal Working Hours: {total_hours} ({total_time})")

    for task, hours in tasks:
        data = (name, task, float_to_time(hours))
        connect_and_insert("example.db", "time_entries", data)

if __name__ == "__main__":
    main()
