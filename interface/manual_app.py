# manual_app.py – Main interface to launch Gripper and Sensor UI

import gradio as gr
from gripper_app import render as render_grippers
from sensor_app import render as render_sensors

with gr.Blocks(title="Weighted Model Evaluation Tool") as demo:
    with gr.Tab("🦾 Grippers"):
        render_grippers()
    with gr.Tab("🔬 Sensors"):
        render_sensors()

if __name__ == "__main__":
    demo.launch()
