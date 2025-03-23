import time
import os
import json
from datetime import datetime
import tkinter as tk
import subprocess  # For running Git commands
import sys  # For exiting the program

# Global variables
start_time = None
program_name = None

def load_last_used_apps():
    """Load the last 3 apps based on 'last_launched'."""
    if os.path.exists("time_log.json"):
        try:
            with open("time_log.json", "r") as file:
                time_log = json.load(file)
            # Sort by 'last_launched' in descending order
            sorted_apps = sorted(
                time_log.values(),
                key=lambda x: datetime.strptime(x["last_launched"], "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )
            return sorted_apps[:3]  # Return the last 3 apps
        except (json.JSONDecodeError, KeyError, ValueError):
            return []
    return []

def update_last_used_apps():
    """Update the display of the last 3 apps in the GUI."""
    last_apps = load_last_used_apps()
    last_used_label.config(text="\n\n".join(
        [
            f"{app['title']}\n{round(app['total_time'])} minutes / {datetime.strptime(app['last_launched'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')}"
            for app in last_apps
        ]
    ))

def start_tracking():
    """Start tracking time for the entered program."""
    global start_time, program_name
    program_name = program_name_entry.get().strip()
    if not program_name:
        status_label.config(text="Error: Program name cannot be empty!", fg="red")
        return
    start_time = time.time()
    status_label.config(text=f"Tracking '{program_name}'...", fg="green")

def stop_tracking():
    """Stop tracking time and save the data."""
    global start_time, program_name
    if start_time is None or program_name is None:
        status_label.config(text="Error: No tracking in progress!", fg="red")
        return

    end_time = time.time()
    total_time = end_time - start_time
    total_time_minutes = total_time / 60

    # Normalize the program name to lowercase for case-insensitivity
    normalized_name = program_name.lower()

    # Read existing data from the JSON file
    time_log = {}
    if os.path.exists("time_log.json"):
        try:
            with open("time_log.json", "r") as file:
                time_log = json.load(file)
        except json.JSONDecodeError:
            time_log = {}

    # Update or add the program's information
    if normalized_name in time_log:
        time_log[normalized_name]["total_time"] += total_time_minutes
    else:
        time_log[normalized_name] = {
            "title": program_name,  # Keep the original capitalization for display
            "total_time": total_time_minutes,
            "last_launched": None
        }

    # Update the last launched time
    time_log[normalized_name]["last_launched"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write the updated data back to the JSON file
    with open("time_log.json", "w") as file:
        json.dump(time_log, file, indent=4)

    # Update the TXT file
    update_txt_file(time_log)

    # Reset tracking variables
    start_time = None
    program_name = None

    # Update the last used apps display
    update_last_used_apps()

    # Notify the user
    status_label.config(text="Tracking stopped and saved!", fg="green")

def update_txt_file(time_log):
    """Write the title and total time in 'xx hours xx minutes' format to the TXT file."""
    with open("time_log.txt", "w") as file:
        for program_name, data in time_log.items():
            total_time_minutes = data['total_time']
            total_time_rounded = round(total_time_minutes)  # Round up minutes
            hours = total_time_rounded // 60
            minutes = total_time_rounded % 60
            file.write(f"{data['title']}: {hours} hours {minutes} minutes\n")

# Function to open the TXT file
def open_txt_file():
    """Open the TXT file with the default text editor."""
    if os.path.exists("time_log.txt"):
        os.startfile("time_log.txt")  # Windows-specific command to open the file
    else:
        status_label.config(text="Error: TXT file not found!", fg="red")

# Function to save updates to Git
def save_to_git():
    """Save updated files to the Git repository with a commit."""
    try:
        # Run Git commands to add, commit, and push changes
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "data updated"], check=True)
        subprocess.run(["git", "push"], check=True)
        status_label.config(text="Changes saved to Git!", fg="green")
    except subprocess.CalledProcessError:
        status_label.config(text="Error: Failed to save to Git!", fg="red")

# Function to exit the program
def exit_program():
    """Exit the program."""
    root.destroy()

# Create the GUI
root = tk.Tk()
root.title("Time Tracker")

# Set the window size to a square format (e.g., 500x500 pixels)
root.geometry("300x500")

# Disable resizing
root.resizable(False, False)

# Program Name Input
tk.Label(root, text="What Do We Track Here?").pack(pady=5)
program_name_entry = tk.Entry(root, width=35)
program_name_entry.pack(pady=5)

# Buttons Frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5)

# Start Tracking Button
start_button = tk.Button(buttons_frame, text="Start Tracking", command=start_tracking)
start_button.pack(side="left", padx=5)

# Stop Tracking Button
stop_button = tk.Button(buttons_frame, text="Stop Tracking", command=stop_tracking)
stop_button.pack(side="left", padx=5)

# Status Label
status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

# Last Used Apps Display
tk.Label(root, text="Last Used Apps:").pack(pady=5)
last_used_label = tk.Label(root, text="", justify="left", fg="black")
last_used_label.pack(pady=5)

# Add buttons at the bottom
bottom_buttons_frame = tk.Frame(root)
bottom_buttons_frame.pack(pady=10)

# Open TXT File Button
open_txt_button = tk.Button(bottom_buttons_frame, text="Open TXT File", command=open_txt_file)
open_txt_button.pack(side="left", padx=5)

# Save to Git Button
save_to_git_button = tk.Button(bottom_buttons_frame, text="Save to Git", command=save_to_git)
save_to_git_button.pack(side="left", padx=5)

# Exit Button
exit_button = tk.Button(bottom_buttons_frame, text="Exit", command=exit_program)
exit_button.pack(side="left", padx=5)

# Initialize the last used apps display
update_last_used_apps()

# Run the GUI
root.mainloop()