from datetime import datetime

def calculate_days_between_dates(start_date, end_date):

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    

    delta = end_date - start_date

    return delta.days


start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

days_between = calculate_days_between_dates(start_date, end_date)

print(f"Number of days between {start_date} and {end_date}: {days_between} Days")
