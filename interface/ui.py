# interface/ui.py

import gradio as gr
import requests
import plotly.graph_objs as go
import os

API_URL = "http://localhost:8000/upload/"

CATEGORY_MAP = {
    "Payload capacity": "Performance",
    "Impact resistance": "Safety",
    "Gripping material": "Cost",
    "Actuation mechanism": "Cost",
    "Control algorithm": "Performance"
}

def extract_numeric(value: str):
    try:
        return float("".join(c for c in value if c.isdigit() or c == "."))
    except:
        return 0.0

def compute_score(parameters, weights):
    score = 0
    for param, value in parameters.items():
        category = CATEGORY_MAP.get(param)
        if category and value not in ["Not available", None, ""]:
            score += extract_numeric(value) * weights[category]
    return round(score, 2)

def plot_rankings(gripper_data):
    if not gripper_data:
        return go.Figure()
    
    names = [g["name"] for g in gripper_data]
    scores = [g["score"] for g in gripper_data]

    fig = go.Figure([go.Bar(x=names, y=scores)])
    fig.update_layout(title="Gripper Rankings", xaxis_title="Gripper", yaxis_title="Score")
    return fig

def handle_upload(file, safety_weight, cost_weight, performance_weight, gripper_list):
    
    weights = {
        "Safety": safety_weight,
        "Cost": cost_weight,
        "Performance": performance_weight
    }

    with open(file.name, "rb") as f:
        response = requests.post(API_URL, files={"file": (file.name, f, "application/pdf")})
    if not response.ok:
        return "❌ Error uploading file", gripper_list, go.Figure()

    result = response.json()
    parameters = result["parameters"]
    gripper_name = os.path.basename(file.name)

    score = compute_score(parameters, weights)
    gripper = {"name": gripper_name, "score": score, "parameters": parameters}

    gripper_list.append(gripper)
    chart = plot_rankings(gripper_list)

    param_str = "\n".join(f"{k}: {v}" for k, v in parameters.items())
    info = f"✅ Uploaded: {gripper_name}\n\n📊 Score: {score}\n\n🧪 Parameters:\n{param_str}"

    return info, gripper_list, chart


with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Gripper Parameter Extractor + Ranking System")

    state = gr.State([])  # ✅ Initialize state to store gripper list

    with gr.Row():
        file_input = gr.File(label="Upload Gripper PDF")
        with gr.Column():
            safety = gr.Slider(0, 1, value=0.33, label="Safety Weight")
            cost = gr.Slider(0, 1, value=0.33, label="Cost Weight")
            perf = gr.Slider(0, 1, value=0.34, label="Performance Weight")

    output_text = gr.Textbox(label="Extracted Info", lines=12)
    plot_output = gr.Plot()

    submit = gr.Button("Upload and Score")
    submit.click(
        fn=handle_upload,
        inputs=[file_input, safety, cost, perf, state],
        outputs=[output_text, state, plot_output]
    )

demo.launch()
