Time Tracker
A simple Python script to calculate the total hours worked and total charged amount based on a given start and end time.

Usage
Run the script and enter the start time in the format HH:MM when prompted.
Enter the end time in the format HH:MM when prompted.
The script will calculate the total hours worked, excluding a 1-hour lunch break, and the total charged amount based on a rate of $1000 per hour.
Output
The script will print the total hours worked and the total charged amount to the console.

Code
The code consists of two functions:

calculate_hours_worked: calculates the total hours worked, excluding a 1-hour lunch break, based on the start and end times.
calculate_total_charged: calculates the total charged amount based on the total hours worked and the rate per hour.
Requirements
Python 3.x
Example Use Case
Edit
Copy code
Enter start time (HH:MM): 08:00
Enter end time (HH:MM): 17:00
Total hours worked (excluding 1 hour lunch): 8.00 hours
Total charged amount: $8000.0
