import os
import json
import time
from typing import List, Dict, Any, Set

import pandas as pd
import pdfplumber
import pypdfium2 as pdfium
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional
import re

try:
    # Optional translation dependency
    from googletrans import Translator  # type: ignore
    _GT_AVAILABLE = True
except Exception:
    Translator = None  # type: ignore
    _GT_AVAILABLE = False


# 📂 Resolve folders relative to this script's location
BASE_DIR = os.path.dirname(__file__)
INPUT_FOLDER = os.path.join(BASE_DIR, "pdfs")

# 📂 Output folder where JSON files will be saved
OUTPUT_FOLDER = os.path.join(BASE_DIR, "json_outputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ✅ Define keywords to detect form pages (case-insensitive)
KEYWORDS: List[str] = [
    # English
    "self-declaration",
    "declaration",
    "application form",
    "registration form",
    "form",
    "applicant",
    # Hindi (Devanagari)
    "आवेदन पत्र",
    "पंजीकरण फॉर्म",
    "स्व-घोषणा पत्र",
    "घोषणा",
]


def _scan_matching_pages_fast(pdf_path: str, keywords_lower: List[str]) -> Set[int]:
    """Fast pass using pypdfium2 to find 1-based page numbers containing any keyword.

    Returns a set of page numbers (1-based) to process in detail.
    """
    matching_pages: Set[int] = set()
    doc = pdfium.PdfDocument(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc.get_page(page_index)
            try:
                textpage = page.get_textpage()
                try:
                    text = (textpage.get_text_range() or "").lower()
                finally:
                    textpage.close()
                if text and any(keyword in text for keyword in keywords_lower):
                    matching_pages.add(page_index + 1)  # convert to 1-based
            finally:
                page.close()
    finally:
        doc.close()
    return matching_pages


def _extract_details_with_pdfplumber(
    pdf_path: str,
    matching_pages: Set[int],
    enable_ocr: bool = False,
    ocr_lang: str = "eng",
    devanagari_lang: Optional[str] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Extract text and tables only for matching pages using pdfplumber."""
    forms: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []

    if not matching_pages:
        return {"forms": forms, "tables": tables}

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in sorted(matching_pages):
            # pdfplumber uses 0-based indexing internally
            page = pdf.pages[page_number - 1]

            page_text = page.extract_text(
                x_tolerance=1.5,
                y_tolerance=1.0,
                keep_blank_chars=True,
            ) or ""

            # Detect legacy Hindi garble (e.g., Kruti/Chanakya encoded copy-paste)
            def looks_like_legacy_hindi_garble(txt: str) -> bool:
                if not txt:
                    return False
                # Already proper Devanagari? Then not garbled
                has_devanagari = any('\u0900' <= ch <= '\u097F' for ch in txt)
                if has_devanagari:
                    return False
                lowered = txt.lower()
                # Heuristic tokens commonly seen in garbled Hindi
                if re.search(r"(vkosn|vkokl|ik=|;kstuk|ykkwvjh|okf'k|qst|lwph)", lowered):
                    return True
                # Excess punctuation vs letters
                punct = sum(ch in "';\"&^%$#@!~`" for ch in txt)
                letters = sum(ch.isalpha() for ch in txt)
                total = max(1, letters)
                return (punct / total) > 0.2

            need_ocr = (
                not page_text.strip()
                or len(page_text.strip()) < 40
                or looks_like_legacy_hindi_garble(page_text)
            )

            bitmap_for_ocr = None
            if enable_ocr and need_ocr:
                try:
                    import pytesseract  # type: ignore
                    doc = pdfium.PdfDocument(pdf_path)
                    try:
                        p = doc.get_page(page_number - 1)
                        try:
                            # Higher render scale improves OCR accuracy
                            bitmap_for_ocr = p.render(scale=3.0).to_pil()
                        finally:
                            p.close()
                    finally:
                        doc.close()
                    ocr_text = pytesseract.image_to_string(
                        bitmap_for_ocr,
                        lang=ocr_lang,
                        config="--oem 1 --psm 6 -c preserve_interword_spaces=1",
                    ) or ""
                    if len(ocr_text.strip()) > len(page_text.strip()):
                        page_text = ocr_text
                except Exception:
                    pass

            # Optional dedicated Devanagari OCR (e.g., hin or hin+eng) to capture proper script
            page_text_hi: Optional[str] = None
            if devanagari_lang:
                try:
                    import pytesseract  # type: ignore
                    if bitmap_for_ocr is None:
                        doc = pdfium.PdfDocument(pdf_path)
                        try:
                            p = doc.get_page(page_number - 1)
                            try:
                                bitmap_for_ocr = p.render(scale=3.0).to_pil()
                            finally:
                                p.close()
                        finally:
                            doc.close()
                    page_text_hi = pytesseract.image_to_string(
                        bitmap_for_ocr,
                        lang=devanagari_lang,
                        config="--oem 1 --psm 6 -c preserve_interword_spaces=1",
                    ) or None
                except Exception:
                    page_text_hi = None
            if page_text.strip() or (page_text_hi and page_text_hi.strip()):
                entry = {
                    "page_number": page_number,
                    "page_text": page_text.strip(),
                }
                if page_text_hi and page_text_hi.strip():
                    entry["page_text_hi"] = page_text_hi.strip()
                forms.append(entry)

            table_settings_primary = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 5,
                "snap_tolerance": 3,
                "join_tolerance": 3,
                "edge_min_length": 3,
                "min_words_vertical": 3,
                "min_words_horizontal": 1,
            }

            table_settings_fallback = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "intersection_tolerance": 5,
                "snap_tolerance": 3,
                "join_tolerance": 3,
            }

            extracted_any = False
            try:
                for tbl in page.find_tables(table_settings=table_settings_primary):
                    grid = tbl.extract()
                    if not grid or len(grid) < 2:
                        continue
                    header_row = grid[0]
                    data_rows = [row for row in grid[1:] if any(row)]
                    if not data_rows:
                        continue
                    table_df = pd.DataFrame(data_rows, columns=header_row)
                    tables.append({
                        "page_number": page_number,
                        "table": table_df.to_dict(orient="records"),
                    })
                    extracted_any = True
            except Exception:
                pass

            if not extracted_any:
                try:
                    simple_table = page.extract_table(table_settings=table_settings_fallback)
                    if simple_table:
                        cleaned = [row for row in simple_table if any(row)]
                        if len(cleaned) > 1:
                            header_row = cleaned[0]
                            data_rows = cleaned[1:]
                            table_df = pd.DataFrame(data_rows, columns=header_row)
                            tables.append({
                                "page_number": page_number,
                                "table": table_df.to_dict(orient="records"),
                            })
                            extracted_any = True
                except Exception:
                    pass

            if not extracted_any:
                try:
                    import tabula  # type: ignore
                    dfs = tabula.read_pdf(
                        pdf_path,
                        pages=page_number,
                        multiple_tables=True,
                        lattice=True,
                        stream=True,
                    )
                    for df in dfs or []:
                        if df is None or df.empty:
                            continue
                        tables.append({
                            "page_number": page_number,
                            "table": df.fillna("").to_dict(orient="records"),
                        })
                        extracted_any = True
                except Exception:
                    pass

    return {"forms": forms, "tables": tables}


def _should_skip(pdf_path: str, json_path: str) -> bool:
    """Skip processing if JSON exists and is newer than PDF (already processed)."""
    if not os.path.exists(json_path):
        return False
    try:
        return os.path.getmtime(json_path) >= os.path.getmtime(pdf_path)
    except OSError:
        return False


def _maybe_translate(text: str, target_lang: Optional[str]) -> str:
    if not target_lang:
        return text
    if not _GT_AVAILABLE:
        return text
    try:
        tr = Translator()
        return tr.translate(text, dest=target_lang).text or text
    except Exception:
        return text


def process_pdf(
    pdf_path: str,
    mode: str = "keywords",
    enable_ocr: bool = False,
    ocr_lang: str = "eng",
    translate_lang: Optional[str] = None,
    devanagari_lang: Optional[str] = None,
) -> None:
    filename = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(filename)[0]
    json_path = os.path.join(OUTPUT_FOLDER, f"{pdf_name}.json")

    if _should_skip(pdf_path, json_path):
        print(f"⏭️  Skipping (up-to-date): {filename}")
        return

    print(f"📄 Processing: {filename}")
    start_time = time.time()

    if mode == "all":
        doc = pdfium.PdfDocument(pdf_path)
        try:
            matching_pages = set(range(1, len(doc) + 1))
        finally:
            doc.close()
    else:
        keywords_lower = [kw.lower() for kw in KEYWORDS]
        matching_pages = _scan_matching_pages_fast(pdf_path, keywords_lower)

    details = _extract_details_with_pdfplumber(
        pdf_path,
        matching_pages,
        enable_ocr=enable_ocr,
        ocr_lang=ocr_lang,
        devanagari_lang=devanagari_lang,
    )

    output_data = {
        "pdf_name": pdf_name,
        "forms": details["forms"] if details["forms"] else None,
        "tables": details["tables"] if details["tables"] else None,
    }

    if translate_lang and details["forms"]:
        translated_forms: List[Dict[str, Any]] = []
        for item in details["forms"]:
            translated_forms.append({
                "page_number": item.get("page_number"),
                "page_text": _maybe_translate(item.get("page_text", ""), translate_lang),
            })
        output_data["forms_translated"] = translated_forms

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    elapsed = time.time() - start_time
    print(f"✅ Saved JSON: {json_path} ({elapsed:.2f}s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fast and accurate PDF text/table extractor")
    parser.add_argument("--parallel", action="store_true", help="Process PDFs in parallel (per-file)")
    parser.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2))), help="Number of worker processes when using --parallel")
    parser.add_argument("--mode", choices=["keywords", "all"], default="keywords", help="Page selection: only keyword-matching pages or all pages")
    parser.add_argument("--enable-ocr", action="store_true", help="Enable OCR fallback for scanned/low-text pages (requires Tesseract + pytesseract)")
    parser.add_argument("--ocr-lang", type=str, default="eng", help="Tesseract languages, e.g., 'eng' or 'eng+hin'")
    parser.add_argument("--translate", type=str, default=None, help="Translate extracted form text to target language code, e.g., 'en' (requires googletrans)")
    parser.add_argument("--devanagari", action="store_true", help="Also run Hindi OCR and include Devanagari text as 'page_text_hi'")
    parser.add_argument("--devanagari-lang", type=str, default=None, help="Language for Devanagari OCR, e.g., 'hin' or 'hin+eng'")
    args = parser.parse_args()

    if not os.path.isdir(INPUT_FOLDER):
        print(f"❌ PDF folder not found: {INPUT_FOLDER}")
        return

    pdf_files = [
        os.path.join(INPUT_FOLDER, name)
        for name in os.listdir(INPUT_FOLDER)
        if name.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("ℹ️  No PDF files found to process.")
        return

    # Resolve devanagari language option
    dev_lang = args.devanagari_lang if args.devanagari_lang else ("hin+eng" if args.devanagari else None)

    if not args.parallel:
        # Sequential processing (fast scan already helps a lot)
        for pdf_path in pdf_files:
            try:
                process_pdf(
                    pdf_path,
                    mode=args.mode,
                    enable_ocr=args.enable_ocr,
                    ocr_lang=args.ocr_lang,
                    translate_lang=args.translate,
                    devanagari_lang=dev_lang,
                )
            except Exception as exc:
                print(f"❌ Error processing {os.path.basename(pdf_path)}: {exc}")
    else:
        # Parallel processing across PDFs
        max_workers = max(1, args.workers)
        print(f"⚙️  Parallel mode enabled with {max_workers} workers")
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    process_pdf,
                    path,
                    args.mode,
                    args.enable_ocr,
                    args.ocr_lang,
                    args.translate,
                    dev_lang,
                ): path
                for path in pdf_files
            }
            for future in as_completed(futures):
                path = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"❌ Error processing {os.path.basename(path)}: {exc}")


if __name__ == "__main__":
    main()
