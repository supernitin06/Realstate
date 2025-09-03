import fitz  # PyMuPDF
import os
from PIL import Image

# Path to PDFs folder
pdf_folder = "pdfs"
output_folder = "extracted_images"

# Create output folder if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all PDFs in the folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, pdf_file)
        pdf_doc = fitz.open(file_path)

        # Loop through pages
        for page_num in range(0, 1): 
            page = pdf_doc[page_num]
            images = page.get_images(full=True)

            # Extract each image
            for img_index, img in enumerate(images, start=1):
                xref = img[0]  # image reference
                base_image = pdf_doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_name = f"{os.path.splitext(pdf_file)[0]}_page{page_num+1}_img{img_index}.{image_ext}"
                image_path = os.path.join(output_folder, image_name)

                # Save image
                with open(image_path, "wb") as f:
                    f.write(image_bytes)

        pdf_doc.close()

print("✅ Images extracted and saved in 'extracted_images' folder")
