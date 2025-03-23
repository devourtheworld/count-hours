# Time Tracker

This project is a Python program that tracks the time spent on specific tasks or programs. It provides a graphical user interface (GUI) for starting and stopping a timer, displaying the last used programs, and saving the total time spent on a chosen program to a text file.

## Features

- **Start and Stop Tracking**: Start tracking time for a specific program and stop to calculate the total duration.
- **Last Used Programs**: Displays the last 3 programs used, including their total time and last used date.
- **Save Data**: Saves the total time spent to a text file (`time_log.txt`) and a JSON file (`time_log.json`).
- **Open TXT File**: Open the `time_log.txt` file directly from the GUI.
- **Save to Git**: Save updated files to a Git repository with a commit message.
- **Exit Program**: Close the program from the GUI.

## Requirements

To run this program, you need to have Python installed on your machine. Additionally, you may need to install the required libraries listed in `requirements.txt`.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/time-tracker.git
   ```

2. Navigate to the project directory:
   ```
   cd time-tracker
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
   ```
   python main.py
   ```

2. Use the GUI to:
   - Enter a program name and click "Start Tracking" to begin tracking time.
   - Click "Stop Tracking" to stop tracking and save the data.
   - View the last 3 used programs in the "Last Used Apps" section.
   - Use the buttons at the bottom of the window:
     - **Open TXT File**: Opens the `time_log.txt` file in your default text editor.
     - **Save to Git**: Saves updated files to the Git repository with a commit message "data updated."
     - **Exit**: Closes the program.

## Launching the Program Using a `.bat` File

You can create a `.bat` file to easily launch the program without using the command line. Follow these steps:

1. Open a text editor (e.g., Notepad).
2. Add the following lines to the file:
   ```
   @echo off
   python main.py
   pause
   ```
   - The `@echo off` hides the command output.
   - The `pause` keeps the terminal open after the program finishes.

3. Save the file as `launch_time_tracker.bat` in the same directory as `main.py`.
4. Double-click the `.bat` file to launch the program.

## Data Storage

- **Text File (`time_log.txt`)**: Stores the program name, total time spent (in hours and minutes), and last used date.
- **JSON File (`time_log.json`)**: Stores detailed information about each program, including:
  - `title`: The program name.
  - `total_time`: The total time spent (in minutes).
  - `last_launched`: The last time the program was tracked (date and time).

## Example Output

### `time_log.txt`:
```
Program A: 2 hours 15 minutes
Program B: 1 hour 30 minutes
Program C: 0 hours 45 minutes
```

### `time_log.json`:
```json
{
    "program_a": {
        "title": "Program A",
        "total_time": 135,
        "last_launched": "2025-03-23 14:30:00"
    },
    "program_b": {
        "title": "Program B",
        "total_time": 90,
        "last_launched": "2025-03-23 15:00:00"
    }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.