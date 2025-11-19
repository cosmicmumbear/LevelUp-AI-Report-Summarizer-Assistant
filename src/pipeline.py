import gradio as gr

from .ocr_processor import get_text_from_file
from .data_interpreter import get_interpretation
from .summarizer import get_summary


def analyze_report_file(report_file: gr.File) -> tuple:
    """
    Executes the full analysis pipeline on uploaded file.

    Args:
        report_file(gr.File): The file object uploaded by the user via the Gradio interface.

    Returns:
        tuple: A 3-tuple of strings, in the following order, which corresponds to the 'outputs' in app.py:
            1. text (str): The raw text extracted by the OCR module.
            2. key_insights (str): Bullet list of key insights from the data.
            3. conclusion (str): Conclusion paragraph.

    Raises:
        Exception: Catches and logs any exceptions from the sub-modules,returning user-friendly error messages to
            all UI fields.
    """

    try:
        text = get_text_from_file(report_file)
        if not text:
            text = "No text could be extracted from the file."

        key_insights = get_interpretation(text)
        if not key_insights:
            key_insights = "Failed to generate key insights from the text."

        conclusion = get_summary(key_insights)
        if not conclusion:
            conclusion = "No conclusion available."

        return text, key_insights, conclusion

    except Exception as e:
        print(f"[Pipeline] CRITICAL ERROR: {e} !")
        error_msg = f"An unexpected error occurred during processing: {str(e)}"

    return error_msg, error_msg, error_msg
