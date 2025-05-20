import fitz  # PyMuPDF
import re
from collections import defaultdict

# Load PDF
pdf_path = (
    "C://Users//stephensila//Downloads//March 2025.pdf"  # Replace with actual PDF path
)
doc = fitz.open(pdf_path)

subscriber_set = {
    "796105283",
    "743616175",
    "799503238",
    "709576525",
    "794490277",  # truncated for brevity
    # ... insert full subscriber set here ...
}

# Store results
summary_data = {}
itemised_data = {}

# Iterate through PDF pages
for page_num, page in enumerate(doc, start=1):
    text = page.get_text()

    # Extract subscriber number (first 9-12 digit number)
    subscriber_match = re.search(r"\b(\d{9,12})\b", text)
    # if subscriber_match:
    #     subscriber_number = subscriber_match.group(1)
    #     if subscriber_number not in subscriber_set:
    #         continue  # Skip if number not in our list

    #     print(f"📄 Found subscriber: {subscriber_number} on page {page_num}")

    # Summary Page: Look for indicators like "BILL SUMMARY"
    if (
        "Total Duration of Calls" in text
        and "Total Volume of Internet Sessions" in text
    ):
        duration_match = re.search(
            r"Total Duration of Calls\s+[A-Za-z]*\s*([\d:]{8})", text
        )
        volume_match = re.search(
            r"Total Volume of Internet Sessions\s+[A-Za-z]*\s*([\d,]+\.\d{2})", text
        )

        duration = duration_match.group(1) if duration_match else ""
        internet_volume = volume_match.group(1).replace(",", "") if volume_match else ""

        summary_data[subscriber_number] = {
            "duration": duration,
            "internet": internet_volume,
        }

    # Itemised Data Page (fall back if subscriber wasn't caught above)
    elif (
        "Total Duration of Calls" in text
        and "Total Volume of Internet Sessions" in text
    ):
        print(f"🔍 Found itemised table on page {page_num}")

        duration_match = re.search(
            r"Total Duration of Calls\s+[A-Za-z]*\s*([\d:]{8})", text
        )
        volume_match = re.search(
            r"Total Volume of Internet Sessions\s+[A-Za-z]*\s*([\d,]+\.\d{2})", text
        )

        duration = duration_match.group(1) if duration_match else ""
        internet_volume = volume_match.group(1).replace(",", "") if volume_match else ""

        possible_numbers = re.findall(r"\d{9,12}", text)
        matched_subscriber = None

        for number in possible_numbers:
            if number in subscriber_set:
                matched_subscriber = number
                break

        if matched_subscriber:
            print(
                f"✅ Matched Subscriber: {matched_subscriber} -> Duration: {duration}, Internet: {internet_volume}"
            )
            itemised_data[matched_subscriber] = {
                "duration": duration,
                "internet": internet_volume,
            }

# 🧾 Combine summary + itemised (prefer summary if available)
final_data = {}
for number in subscriber_set:
    if number in summary_data:
        final_data[number] = summary_data[number]
    elif number in itemised_data:
        final_data[number] = itemised_data[number]

# 🖨️ Output results
for number, data in final_data.items():
    print(f"{number}: Duration = {data['duration']}, Internet = {data['internet']} MB")
