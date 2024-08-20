import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta


def calculate_hours_worked(start_time, end_time):
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")

    total_time_worked = end_dt - start_dt

    total_time_worked -= timedelta(hours=1)

    total_hours_worked = total_time_worked.total_seconds() / 3600

    return total_hours_worked


def calculate_total_charged(hours_worked, rate_per_hour):
    return hours_worked * rate_per_hour


def on_calculate():
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    try:
        total_hours = calculate_hours_worked(start_time, end_time)
        rate_per_hour = 1000
        global total_charged
        total_charged = calculate_total_charged(total_hours, rate_per_hour)

        result_label.config(
            text=f"Total hours worked : {total_hours:.2f} hours\n"
            f"Total charged amount: Ksh{total_charged:.1f}"
        )
    except ValueError:
        messagebox.showerror(
            "Invalid Time Format", "Please enter time in HH:MM format."
        )


def on_export():
    if not result_label.cget("text"):
        messagebox.showwarning("No Results", "Please calculate the results first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if file_path:
        with open(file_path, "w") as file:
            file.write(result_label.cget("text"))
        messagebox.showinfo("Success", "Results have been saved successfully.")


root = tk.Tk()
root.title("Work Hours Calculator")

start_time_label = tk.Label(root, text="Enter start time (HH:MM):")
start_time_label.pack()
start_time_entry = tk.Entry(root)
start_time_entry.pack()

end_time_label = tk.Label(root, text="Enter end time (HH:MM):")
end_time_label.pack()
end_time_entry = tk.Entry(root)
end_time_entry.pack()

calculate_button = tk.Button(root, text="Calculate", command=on_calculate)
calculate_button.pack()

export_button = tk.Button(root, text="Export Results to File", command=on_export)
export_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
