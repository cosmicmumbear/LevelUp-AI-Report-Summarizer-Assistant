import gradio as gr

from .modul_ocr import get_text_from_file
from .data_interpreter import interpret
from .summarizer import create_summary, create_short_summary


def analyze_report_file(report_file: gr.File) -> tuple:
    """
    Executes the full analysis pipeline on uploaded file.

    Args:
        report_file(gr.File): The file object uploaded by the user via the Gradio interface.

    Returns:
        tuple: A 4-tuple of strings, in the following order, which corresponds to the 'outputs' in app.py:
            1. short_desc (str): A brief, one-line description of the chart.
            2. text (str): The raw text extracted by the OCR module.
            3. key_insights (str): Bullet list of key insights from the data.
            4. conclusion (str): Conclusion paragraph.

    Raises:
        Exception: Catches and logs any exceptions from the sub-modules,returning user-friendly error messages to
            all UI fields.
    """

    print("--- [Pipeline] Analysis started... ---")

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

        return short_desc, text, key_insights, conclusion

    except Exception as e:
        print(f"[Pipeline] CRITICAL ERROR: {e} !")
        error_msg = f"An unexpected error occurred during processing: {str(e)}"

    return error_msg, error_msg, error_msg
