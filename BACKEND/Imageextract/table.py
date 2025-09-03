import pdfplumber
import os
import pandas as pd
import json
from deep_translator import GoogleTranslator

# Initialize translator
translator = GoogleTranslator(source='hi', target='en')

# Directories
pdf_folder = "pdfs"
output_folder = "outputs_json"
os.makedirs(output_folder, exist_ok=True)

# Function to translate list of headers from Hindi to English
def translate_headers(headers):
    translated = []
    for header in headers:
        if header.strip() == "":
            translated.append("Unknown")
        else:
            try:
                translation = translator.translate(header)
                translated.append(translation.strip())
            except Exception as e:
                print(f"⚠️ Translation failed for '{header}': {e}")
                translated.append(header.strip())  # fallback
    return translated

# Process each PDF
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        base_name = os.path.splitext(filename)[0]
        json_filename = base_name + ".json"
        output_path = os.path.join(output_folder, json_filename)

        all_rows = []
        table_count = 0

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if not tables:
                    print(f"⚠️ {filename}: No tables found on page {page_num}")
                    continue

                print(f"✅ {filename}: Found {len(tables)} table(s) on page {page_num}")
                for table_index, table in enumerate(tables, start=1):
                    if not table or len(table) < 2:
                        print(f"⚠️ Skipped table {table_index} on page {page_num} due to insufficient rows")
                        continue

                    # Extract and clean header (second row assumed)
                    raw_header = table[1]
                    cleaned_headers = [cell.strip() if cell else f"Column_{i}" for i, cell in enumerate(raw_header)]
                    translated_headers = translate_headers(cleaned_headers)
                    expected_col_count = len(translated_headers)

                    print(f"🧠 Page {page_num}, Table {table_index}: Header -> {translated_headers}")

                    # Extract data rows (excluding the header)
                    for row in table[2:]:
                        cleaned_row = [cell.strip() if cell else "" for cell in row]
                        if len(cleaned_row) == expected_col_count:
                            all_rows.append(dict(zip(translated_headers, cleaned_row)))
                        else:
                            print(f"⚠️ Skipped row due to column mismatch: {cleaned_row}")

                    table_count += 1

        # Save JSON
        if all_rows:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_rows, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {table_count} table(s) from {filename} to {output_path}")
        else:
            print(f"❌ No valid data rows extracted from: {filename}")
