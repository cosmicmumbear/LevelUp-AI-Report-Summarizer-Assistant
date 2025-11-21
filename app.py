import gradio as gr
import os
from src.pipeline import analyze_report_file

example_file_path = os.path.join(os.getcwd(), "data")
example_1 = os.path.join(example_file_path, "Wydatki.pdf")
example_2 = os.path.join(example_file_path, "Wydatki.png")

demo = gr.Interface(
    fn=analyze_report_file,
    inputs=gr.File(label="File"),
    outputs=[
        gr.Image(label="Chart Preview", type="filepath", height=300),
        gr.Textbox(label="Short Description"),
        gr.Textbox(label="Extracted Data"),
        gr.Textbox(label="Key Insights"),
        gr.Textbox(label="Conclusion"),
    ],
    examples=[example_1, example_2],
    title="Chart Analysis Assistant",
    description="Upload a PNG or PDF file with a chart to get detailed analysis and insights.",
    live=True,
)


if __name__ == "__main__":
    print("Launching Gradio application...")
    demo.launch()
