import time
import os
import platform
import tkinter as tk
from datetime import datetime, timedelta


working_hours = 10 * 3600 + 30 * 60
warning_time = 10 * 60

start_time = time.time()
start_time_str = datetime.now().strftime("%H:%M:%S")


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def update_timer():
    elapsed_time = time.time() - start_time
    remaining_time_work = working_hours - elapsed_time

    if remaining_time_work <= 0:
        label.config(text="Time's up! Shutting down...")
        root.update()
        time.sleep(2)
        shutdown_computer()
    elif remaining_time_work <= warning_time:
        label.config(
            text=f"Warning: {format_time(remaining_time_work)} left! Save your work."
        )
        root.after(1000, update_timer)
    else:
        remaining_display = format_time(remaining_time_work)
        label.config(
            text=f"Started at: {start_time_str}\nTime Remaining: {remaining_display}"
        )
        root.after(1000, update_timer)


def shutdown_computer():
    system_name = platform.system()
    if system_name == "Windows":
        os.system("shutdown /s /t 1")
    elif system_name == "Linux" or system_name == "Darwin":
        os.system("shutdown -h now")
    else:
        label.config(text=f"Shutdown not supported for {system_name}.")


root = tk.Tk()
root.title("Work Time")


root.geometry("250x100")


label = tk.Label(root, text="Time Remaining: ", font=("Helvetica", 12), justify=tk.LEFT)
label.pack(expand=True)


update_timer()

root.mainloop()
