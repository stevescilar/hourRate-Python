import fitz  # PyMuPDF
import re
import csv

pdf_path = "C://Users//stephensila//Downloads//cust_Z0005678_20241201.pdf"
output_csv = "C://Users//stephensila//Downloads//cust_Z0005678_20241201.csv"

doc = fitz.open(pdf_path)

data = []
subscriber_set = set()
itemised_data = {}  # {subscriber_number: {"duration": ..., "internet": ..., "points": ...}}

# First pass: Extract static fields and build subscriber list
for page in doc:
    text = page.get_text()

    sub_match = re.search(r"Subscriber Number\s*[:\-]?\s*(\d+)", text)
    plan_match = re.search(r"Tariff Plan\s*[:\-]?\s*(.+)", text)
    premium_match = re.search(r"Premium Rate Service.*?([\d,]+\.\d{2})", text, re.DOTALL)
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
    premium_rate_service = premium_match.group(1).replace(",", "") if premium_match else ""
    premium_sms = sms_match.group(1).replace(",", "") if sms_match else ""
    amount_due = amount_due_match.group(1).replace(",", "") if amount_due_match else ""
    internet_volume = internet_volume_match.group(1).replace(",", "") if internet_volume_match else ""

    # Placeholder for points balance to be filled in second pass
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
                points_balance,  # Will update in merge
            ]
        )

# Second pass: Extract call duration, internet volume, and points balance, matched to subscriber
for page in doc:
    text = page.get_text()

    if (
        "Total Duration of Calls" in text
        or "Total Volume of Internet Sessions" in text
        or "Points Balance as at Statement Date" in text
    ):
        call_duration_match = re.search(r"Total Duration of Calls\s+(\d{2}:\d{2}:\d{2})", text)
        internet_volume_match = re.search(
            r"Total Volume of Internet Sessions\s+[A-Za-z]*\s*([\d,]+\.\d{2})", text
        )
        points_balance_match = re.search(r"Points Balance as at Statement Date\s+(\d+)", text)

        call_duration = call_duration_match.group(1) if call_duration_match else ""
        internet_volume = internet_volume_match.group(1).replace(",", "") if internet_volume_match else ""
        points_balance = points_balance_match.group(1) if points_balance_match else ""

        # Identify subscriber number on the same page
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

# Merge second pass data with first pass rows
for row in data:
    sub_number = row[0]
    if sub_number in itemised_data:
        row[6] = itemised_data[sub_number].get("internet", row[6])  # Internet Volume
        row[7] = itemised_data[sub_number].get("points", row[7])    # Points Balance
        row.append(itemised_data[sub_number].get("duration", ""))   # Call Duration
    else:
        row.append("")

# Write CSV output
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
    writer.writerows(data)

print(f"✅ Done! Output saved to: '{output_csv}'")
