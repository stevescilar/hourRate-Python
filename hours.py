from datetime import datetime, timedelta

def calculate_hours_worked(start_time, end_time):
    
    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = datetime.strptime(end_time, '%H:%M')
    
    
    total_time_worked = end_dt - start_dt
    
   
    total_time_worked -= timedelta(hours=1)
    
    # Convert the result to hours
    total_hours_worked = total_time_worked.total_seconds() / 3600
    
    return total_hours_worked

def calculate_total_charged(hours_worked, rate_per_hour):
    return hours_worked * rate_per_hour

# Example usage
start_time = input("Enter start time (HH:MM): ")
end_time = input("Enter end time (HH:MM): ")

# Calculate total hours worked
total_hours = calculate_hours_worked(start_time, end_time)
# Calculate total charged amount
rate_per_hour = 1000
total_charged = calculate_total_charged(total_hours, rate_per_hour)

print(f"Total hours worked (excluding 1 hour lunch): {total_hours:.2f} hours")
print(f"Total charged amount: ${total_charged:.1f}")
