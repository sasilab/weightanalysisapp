import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import os

# File path
GRIPPER_FILE = "grippers.csv"

# Load or create data
default_data = [
    {'Name': 'Vacuum Gripper', 'Cost': 6, 'ISO Compliance': 8, 'Safety': 9, 'Performance': 7},
    {'Name': 'Soft Robotic Gripper', 'Cost': 7, 'ISO Compliance': 9, 'Safety': 8, 'Performance': 9}
]

def load_data():
    if os.path.exists(GRIPPER_FILE):
        df = pd.read_csv(GRIPPER_FILE)
        for col in default_data[0]:
            if col not in df.columns:
                df[col] = 0
        return df
    else:
        df = pd.DataFrame(default_data)
        df.to_csv(GRIPPER_FILE, index=False)
        return df

# Score calculation
def calculate_scores(df, weights):
    for factor, weight in weights.items():
        df[f"{factor} Weighted"] = df[factor] * weight
    df["Total Score"] = df[[f"{k} Weighted" for k in weights]].sum(axis=1)
    df["Rank"] = df["Total Score"].rank(ascending=False)
    return df

# Add new entry
def add_entry(name, cost, iso, safety, performance):
    df = load_data()
    new = pd.DataFrame([{
        "Name": name,
        "Cost": cost,
        "ISO Compliance": iso,
        "Safety": safety,
        "Performance": performance
    }])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(GRIPPER_FILE, index=False)
    return update_output(0.25, 0.25, 0.25, 0.25)

# Update and plot
def update_output(w_cost, w_iso, w_safety, w_perf):
    df = load_data()
    weights = {"Cost": w_cost, "ISO Compliance": w_iso, "Safety": w_safety, "Performance": w_perf}
    df = calculate_scores(df, weights)
    fig, ax = plt.subplots()
    ax.bar(df["Name"], df["Total Score"], color='skyblue')
    ax.set_ylabel("Score")
    ax.set_title("Gripper Score Ranking")
    return df[["Name", "Total Score", "Rank"]], fig

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🦾 Gripper Evaluation - Manual Entry")

    with gr.Row():
        name = gr.Textbox(label="Gripper Name")
        cost = gr.Slider(1, 10, value=5, label="Cost")
        iso = gr.Slider(1, 10, value=5, label="ISO Compliance")
        safety = gr.Slider(1, 10, value=5, label="Safety")
        performance = gr.Slider(1, 10, value=5, label="Performance")
        add_btn = gr.Button("➕ Add Gripper")

    add_output = gr.Dataframe()
    chart = gr.Plot()

    with gr.Row():
        w_cost = gr.Slider(0, 1, 0.25, label="Weight - Cost")
        w_iso = gr.Slider(0, 1, 0.25, label="Weight - ISO")
        w_safety = gr.Slider(0, 1, 0.25, label="Weight - Safety")
        w_perf = gr.Slider(0, 1, 0.25, label="Weight - Performance")
        update_btn = gr.Button("🔄 Update Ranking")

    update_output_table = gr.Dataframe()
    update_chart = gr.Plot()

    add_btn.click(fn=add_entry, inputs=[name, cost, iso, safety, performance], outputs=[add_output, chart])
    update_btn.click(fn=update_output, inputs=[w_cost, w_iso, w_safety, w_perf], outputs=[update_output_table, update_chart])

demo.launch()
