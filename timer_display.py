import time
import os
import platform
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


working_hours = 10 * 3600
break_time = 1 * 3600
warning_time = 10 * 60

log_file_path = "work_timer_log.txt"


start_time = time.time()
start_time_str = datetime.now().strftime("%H:%M:%S")
start_date_str = datetime.now().strftime("%A, %B %d, %Y")


def log_event(event):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{event}\n")


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def update_timer():
    elapsed_time = time.time() - start_time
    remaining_time_work = working_hours - elapsed_time

    progress_var.set((elapsed_time / working_hours) * 100)

    if remaining_time_work <= 0:
        label.config(text="Time's up!", fg="red")
        root.update()
        stop_timer()
    elif remaining_time_work <= warning_time:
        label.config(
            text=f"Warning: {format_time(remaining_time_work)} left! Save your work.",
            fg="orange",
        )
        root.after(1000, update_timer)
    else:
        remaining_display = format_time(remaining_time_work)
        label.config(
            text=f"Started at: {start_time_str}\nTime Remaining: {remaining_display}",
            fg="green",
        )
        root.after(1000, update_timer)


def stop_timer():
    end_time = datetime.now()
    end_time_str = end_time.strftime("%H:%M:%S")
    total_work_time = int(time.time() - start_time) - break_time
    total_work_hours = format_time(total_work_time)
    log_event(f"Session Ended: {end_time_str} on {end_time.strftime('%A, %B %d, %Y')}")
    log_event(f"Total Hours Worked (excluding 1-hour break): {total_work_hours}")
    log_event("-" * 40)
    open_log_file()
    root.quit()


def open_log_file():
    system_name = platform.system()
    if system_name == "Windows":
        os.system(f'notepad.exe "{log_file_path}"')
    elif system_name == "Linux":
        os.system(f'xdg-open "{log_file_path}"')
    elif system_name == "Darwin":  # macOS is 'Darwin'
        os.system(f'open "{log_file_path}"')
    else:
        label.config(text=f"Opening log file not supported for {system_name}.")


log_event(f"Session Started: {start_time_str} on {start_date_str}")


root = tk.Tk()
root.title("Work Timer")


root.geometry("400x200")
root.configure(bg="#282c34")


label = tk.Label(
    root, text="Time Remaining: ", font=("Helvetica", 16), fg="white", bg="#282c34"
)
label.pack(expand=True)


progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=300, mode="determinate", variable=progress_var
)
progress_bar.pack(pady=10)


exit_button = tk.Button(
    root,
    text="Exit",
    command=stop_timer,
    bg="#61afef",
    fg="white",
    font=("Helvetica", 12),
    relief="flat",
)
exit_button.pack(side="bottom", pady=10)


update_timer()

root.mainloop()
