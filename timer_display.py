import time
import os
import platform
import tkinter as tk

working_hours = 9 * 3600 + 30 * 60
warning_time = 10 * 60


start_time = time.time()


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def update_timer():
    elapsed_time = time.time() - start_time
    remaining_time = working_hours - elapsed_time

    if remaining_time <= 0:
        label.config(text="Time's up! Shutting down...")
        root.update()
        time.sleep(2)
        shutdown_computer()
    elif remaining_time <= warning_time:
        label.config(
            text=f"Warning: {format_time(remaining_time)} left! Save your work."
        )
        root.after(1000, update_timer)
    else:
        label.config(text="Time Remaining: " + format_time(remaining_time))
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
root.title("Work Timer")

root.geometry("300x100")

label = tk.Label(root, text="Time Remaining: ", font=("Helvetica", 15))
label.pack(expand=True)

update_timer()

root.mainloop()
