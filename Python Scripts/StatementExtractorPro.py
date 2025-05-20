import fitz  # PyMuPDF
import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def extract_pdf_data(pdf_path, output_csv):
    doc = fitz.open(pdf_path)
    data = []
    subscriber_set = set()
    itemised_data = {}

    # First pass
    for page in doc:
        text = page.get_text()

        sub_match = re.search(r"Subscriber Number\s*[:\-]?\s*(\d+)", text)
        plan_match = re.search(r"Tariff Plan\s*[:\-]?\s*(.+)", text)
        premium_match = re.search(
            r"Premium Rate Service.*?([\d,]+\.\d{2})", text, re.DOTALL
        )
        sms_match = re.search(r"Premium SMS.*?([\d,]+\.\d{2})", text, re.DOTALL)
        amount_due_match = re.search(r"Amount Due.*?([\d,]+\.\d{2})", text, re.DOTALL)
        internet_volume_match = re.search(
            r"Total Volume of Internet Sessions\s+[A-Za-z]*\s*([\d,]+\.\d{2})", text
        )

        description = ""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "P.O Box 40612" in line and i > 0:
                description = lines[i - 1].strip()
                break

        subscriber_number = sub_match.group(1) if sub_match else ""
        tariff_plan = plan_match.group(1).strip() if plan_match else ""
        premium_rate_service = (
            premium_match.group(1).replace(",", "") if premium_match else ""
        )
        premium_sms = sms_match.group(1).replace(",", "") if sms_match else ""
        amount_due = (
            amount_due_match.group(1).replace(",", "") if amount_due_match else ""
        )
        internet_volume = (
            internet_volume_match.group(1).replace(",", "")
            if internet_volume_match
            else ""
        )

        points_balance = ""

        if subscriber_number:
            subscriber_set.add(subscriber_number)

        if (
            subscriber_number
            or tariff_plan
            or description
            or premium_rate_service
            or premium_sms
            or amount_due
            or internet_volume
        ):
            data.append(
                [
                    subscriber_number,
                    tariff_plan,
                    description,
                    premium_rate_service,
                    premium_sms,
                    amount_due,
                    internet_volume,
                    points_balance,
                ]
            )

    # Second pass
    for page in doc:
        text = page.get_text()

        if (
            "Total Duration of Calls" in text
            or "Total Volume of Internet Sessions" in text
            or "Points Balance as at Statement Date" in text
        ):
            call_duration_match = re.search(
                r"Total Duration of Calls\s+(\d{2}:\d{2}:\d{2})", text
            )
            internet_volume_match = re.search(
                r"Total Volume of Internet Sessions\s+[A-Za-z]*\s*([\d,]+\.\d{2})", text
            )
            points_balance_match = re.search(
                r"Points Balance as at Statement Date\s+(\d+)", text
            )

            call_duration = call_duration_match.group(1) if call_duration_match else ""
            internet_volume = (
                internet_volume_match.group(1).replace(",", "")
                if internet_volume_match
                else ""
            )
            points_balance = (
                points_balance_match.group(1) if points_balance_match else ""
            )

            found_subscriber = None
            for sub_number in subscriber_set:
                if sub_number in text:
                    found_subscriber = sub_number
                    break

            if found_subscriber:
                if found_subscriber not in itemised_data:
                    itemised_data[found_subscriber] = {}
                if call_duration:
                    itemised_data[found_subscriber]["duration"] = call_duration
                if internet_volume:
                    itemised_data[found_subscriber]["internet"] = internet_volume
                if points_balance:
                    itemised_data[found_subscriber]["points"] = points_balance

    # Merge
    for row in data:
        sub_number = row[0]
        if sub_number in itemised_data:
            row[6] = itemised_data[sub_number].get("internet", row[6])
            row[7] = itemised_data[sub_number].get("points", row[7])
            row.append(itemised_data[sub_number].get("duration", ""))
        else:
            row.append("")

    # Write CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Subscriber Number",
                "Tariff Plan",
                "User Description",
                "Premium Rate Service",
                "Premium SMS",
                "Amount Due",
                "Internet Volume (Mb)",
                "Points Balance",
                "Total Call Duration",
            ]
        )
        # writer.writerows(data)
        # Filter out rows with empty 'Tariff Plan' (index 1)
        filtered_data = [row for row in data if row[1].strip()]
        writer.writerows(filtered_data)


def select_file_and_run():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            output_path = file_path.replace(".pdf", ".csv")
            extract_pdf_data(file_path, output_path)
            messagebox.showinfo("Success", f"✅ Done! CSV saved at:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Simple UI
root = tk.Tk()
root.title("Statement Extractor Pro(PDF)")
root.geometry("400x200")

label = tk.Label(
    root, text="Select a PDF file to extract statement data", font=("Arial", 12)
)
label.pack(pady=20)

btn = tk.Button(
    root,
    text="Choose PDF File",
    command=select_file_and_run,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
)
btn.pack(pady=10)

root.mainloop()
