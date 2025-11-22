import gradio as gr
import os
from src.pipeline import analyze_report_file

example_file_path = os.path.join(os.getcwd(), "data")
example_1 = os.path.join(example_file_path, "Wydatki.pdf")
example_2 = os.path.join(example_file_path, "Wydatki.png")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

demo = gr.Interface(
    fn=analyze_report_file,
    inputs=gr.File(label="File"),
    outputs=[
        gr.Image(label="Chart Preview", type="filepath", height=300),
        gr.Textbox(label="Short Description-Elevator Pitch in 2 Lines", lines=5),
        gr.Textbox(label="Key Insights-Aha! Moments", lines=20),
        gr.Textbox(label="Conclusion-Final Boss Level", lines=20),
        gr.Textbox(label="Extracted Data-Nerd Nuggets", lines=8),
    ],
    examples=[example_1, example_2],
    title="Awesome&Best Ever Chart Analysis Assistant",
    description="Hello My Dear Friend! Upload a PNG or PDF file with a chart to get detailed analysis and insights.",
    live=True,
)


if __name__ == "__main__":
    print("Launching Gradio application...")
    demo.launch(allowed_paths=[BASE_DIR])
