# Gradio app for manual entry like Streamlit version (Compact UI)

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV file
GRIPPER_FILE = "grippers.csv"

# Load or create CSV
def load_data():
    default_data = [
        {'Name': 'Vacuum Gripper', 'Cost': 6, 'ISO Compliance': 8, 'Safety': 9, 'Performance': 7},
        {'Name': 'Soft Robotic Gripper', 'Cost': 7, 'ISO Compliance': 9, 'Safety': 8, 'Performance': 9}
    ]
    if os.path.exists(GRIPPER_FILE):
        df = pd.read_csv(GRIPPER_FILE)
        return df
    else:
        df = pd.DataFrame(default_data)
        df.to_csv(GRIPPER_FILE, index=False)
        return df

# Save entry
def add_gripper(name, mat, gtype, act, payload, dur, ctrl, custom,
                force_lim, surf, acc, algo, mon,
                impact, failsafe, force_limit, comp_design,
                versatility, precision, response, endurance, adapt):

    # Cost sub-score
    cost = round((mat + gtype + act + payload + dur + ctrl + custom) / 7, 2)
    # ISO sub-score
    iso = round((force_lim + surf + acc + algo + mon) / 5, 2)
    # Safety sub-score
    safety = round((impact + failsafe + force_limit + comp_design) / 4, 2)
    # Performance sub-score
    performance = round((versatility + precision + response + endurance + adapt) / 5, 2)

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

# Recalculate and show results
def update_output(w_cost, w_iso, w_safety, w_perf):
    df = load_data()
    df["Total Score"] = (df["Cost"] * w_cost +
                         df["ISO Compliance"] * w_iso +
                         df["Safety"] * w_safety +
                         df["Performance"] * w_perf)
    df["Rank"] = df["Total Score"].rank(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(df['Name'], df['Total Score'], color='skyblue')
    ax.set_ylabel("Score")
    ax.set_title("Gripper Score Ranking")
    return df[["Name", "Cost", "ISO Compliance", "Safety", "Performance", "Total Score", "Rank"]], fig

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🦾 Compact Gripper Entry UI")

    with gr.Accordion("Enter Gripper Details", open=True):
        name = gr.Textbox(label="Gripper Name")

        with gr.Row():
            mat = gr.Slider(1, 10, 5, label="Material")
            gtype = gr.Slider(1, 10, 5, label="Type")
            act = gr.Slider(1, 10, 5, label="Actuation")
            payload = gr.Slider(1, 10, 5, label="Payload")
        with gr.Row():
            dur = gr.Slider(1, 10, 5, label="Durability")
            ctrl = gr.Slider(1, 10, 5, label="Control")
            custom = gr.Slider(1, 10, 5, label="Customization")

        with gr.Row():
            force_lim = gr.Slider(1, 10, 5, label="Force Limiting")
            surf = gr.Slider(1, 10, 5, label="Surface Material")
            acc = gr.Slider(1, 10, 5, label="Accuracy")
            algo = gr.Slider(1, 10, 5, label="Algorithm")
            mon = gr.Slider(1, 10, 5, label="Monitoring")

        with gr.Row():
            impact = gr.Slider(1, 10, 5, label="Impact")
            failsafe = gr.Slider(1, 10, 5, label="Fail-safe")
            force_limit = gr.Slider(1, 10, 5, label="Force Limit")
            comp_design = gr.Slider(1, 10, 5, label="Compliance")

        with gr.Row():
            versatility = gr.Slider(1, 10, 5, label="Versatility")
            precision = gr.Slider(1, 10, 5, label="Precision")
            response = gr.Slider(1, 10, 5, label="Response Time")
            endurance = gr.Slider(1, 10, 5, label="Endurance")
            adapt = gr.Slider(1, 10, 5, label="Adaptability")

        add_button = gr.Button("Add Gripper")

    gr.Markdown("### Adjust Weights")
    with gr.Row():
        w_cost = gr.Slider(0, 1, 0.25, step=0.05, label="Weight: Cost")
        w_iso = gr.Slider(0, 1, 0.25, step=0.05, label="Weight: ISO")
        w_safety = gr.Slider(0, 1, 0.25, step=0.05, label="Weight: Safety")
        w_perf = gr.Slider(0, 1, 0.25, step=0.05, label="Weight: Performance")
        update_btn = gr.Button("Update Ranking")

    table = gr.Dataframe(label="Gripper Rankings")
    chart = gr.Plot()

    add_button.click(
        fn=add_gripper,
        inputs=[name, mat, gtype, act, payload, dur, ctrl, custom,
                force_lim, surf, acc, algo, mon,
                impact, failsafe, force_limit, comp_design,
                versatility, precision, response, endurance, adapt],
        outputs=[table, chart]
    )

    update_btn.click(
        fn=update_output,
        inputs=[w_cost, w_iso, w_safety, w_perf],
        outputs=[table, chart]
    )

if __name__ == "__main__":
    demo.launch()
