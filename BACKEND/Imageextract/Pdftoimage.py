import os
from pdf2image import convert_from_path

# Input and output folders
pdf_folder = "pdfs"
output_folder = "pdfimages"

# Create output folder if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Path to Poppler bin
poppler_path = r"C:\Users\Nitin\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

# Loop through each PDF
pdfs = os.listdir(pdf_folder)
for pdf in pdfs:
    pdf_file_path = os.path.join(pdf_folder, pdf)

    # Convert only the first page
    pages = convert_from_path(pdf_file_path, dpi=200, first_page=1, last_page=1, poppler_path=poppler_path)

    # Save first page
    if pages:  # check if conversion returned pages
        image_path = os.path.join(output_folder, f"{os.path.splitext(pdf)[0]}_page1.png")
        pages[0].save(image_path, "PNG")
        print(f"Saved: {image_path}")
