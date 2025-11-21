from typing import Any
import os

from .modul_ocr import get_text_from_file
from .data_interpreter import interpret
from .summarizer import create_summary, create_short_summary


def analyze_report_file(report_file: Any) -> tuple:
    """
    Executes the full analysis pipeline on uploaded file.

    Args:
        report_file(gr.File): The file object uploaded by the user via the Gradio interface.

    Returns:
        tuple: A 5-tuple of strings, in the following order, which corresponds to the 'outputs' in app.py:
            1. image_path (str): Path to the image preview (or PDF icon).
            2. short_desc (str): A brief, one-line description of the chart.
            3. text (str): The raw text extracted by the OCR module.
            4. key_insights (str): Bullet list of key insights from the data.
            5. conclusion (str): Conclusion paragraph.

    Raises:
        Exception: Catches and logs any exceptions from the sub-modules,returning user-friendly error messages to
            all UI fields.
    """

    print("--- [Pipeline] Analysis started... ---")

    image_preview_path = None

    if report_file:

        filename = getattr(report_file, "name", "").lower()

        if filename.endswith((".png", ".jpg", ".jpeg")):
            image_preview_path = report_file.name

        elif filename.endswith(".pdf"):

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "assets", "pdf_icon.png")

            if os.path.exists(icon_path):
                image_preview_path = icon_path
            else:
                print(f"File not found error: assets/pdf_icon.png!")

    err_msg = "Processing Error"

    try:
        # 1 OCR
        print("[Pipeline] Step 1: OCR...")
        text = get_text_from_file(report_file)
        if not text:
            text = "No text could be extracted from the file."

        # 2 Interpretation
        print("[Pipeline] Step 2: Interpretation...")
        key_insights = interpret(text)
        if not key_insights:
            key_insights = "Failed to generate key insights from the text."

        # Summary
        print("[Pipeline] Step 3: Generating summaries...")
        short_desc = create_short_summary(key_insights)
        if not short_desc:
            short_desc = "No short description available."
        conclusion = create_summary(key_insights)
        if not conclusion:
            conclusion = "No conclusion available."

        print("[Pipeline] Finished successfully.")

        return image_preview_path, short_desc, text, key_insights, conclusion

    except Exception as e:
        print(f"[Pipeline] CRITICAL ERROR: {e} !")
        error_msg = f"An unexpected error occurred during processing: {str(e)}"

    return image_preview_path, error_msg, error_msg, error_msg, err_msg
