import pandas as pd
import os
from tqdm import tqdm


def remove_and_move_duplicates(input_file, column_name):
    try:
        print("Reading the file...")
        if input_file.endswith(".csv"):
            data = pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            data = pd.read_excel(input_file)
        else:
            print("Unsupported file format. Please use .csv or .xlsx files.")
            return

        if column_name not in data.columns:
            print(f"Column '{column_name}' not found in the file.")
            return

        print("Identifying duplicates...")
        duplicates = data[data.duplicated(subset=[column_name], keep=False)]
        cleaned_data = data.drop_duplicates(subset=[column_name])

        base_name, ext = os.path.splitext(input_file)
        output_file_cleaned = f"{base_name}_cleaned{ext}"
        output_file_duplicates = f"{base_name}_duplicates{ext}"

        print("Writing the cleaned data...")
        for _ in tqdm(range(1), desc="Saving Cleaned Data"):
            if ext == ".csv":
                cleaned_data.to_csv(output_file_cleaned, index=False)
            elif ext == ".xlsx":
                cleaned_data.to_excel(output_file_cleaned, index=False)

        print("Writing the duplicate data...")
        for _ in tqdm(range(1), desc="Saving Duplicate Data"):
            if ext == ".csv":
                duplicates.to_csv(output_file_duplicates, index=False)
            elif ext == ".xlsx":
                duplicates.to_excel(output_file_duplicates, index=False)

        print(f"Cleaned data saved to {output_file_cleaned}")
        print(f"Duplicate data saved to {output_file_duplicates}")

    except Exception as e:
        print(f"An error occurred: {e}")


input_path = "C:\\Users\\stephensila\\Downloads\\JER\\Book1.xlsx"
column_to_check = "Industry"
remove_and_move_duplicates(input_path, column_to_check)
