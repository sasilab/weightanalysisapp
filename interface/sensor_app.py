# sensor_app.py - Sensor Evaluation UI

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

SENSOR_FILE = "sensors.csv"

def load_or_create(file, defaults):
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(defaults)
        df.to_csv(file, index=False)
    return df

def save_entry(file, df, new):
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def update_scores(df, weights):
    for key, w in weights.items():
        df[f"{key} Weighted"] = df[key] * w
    df["Total Score"] = df[[f"{k} Weighted" for k in weights]].sum(axis=1)
    df["Rank"] = df["Total Score"].rank(ascending=False)
    return df

def plot_chart(df):
    if df.empty:
        return None
    melted = df.melt(id_vars='Name', value_vars=['Cost', 'ISO Compliance', 'Safety', 'Performance'],
                     var_name='Factors', value_name='Scores')
    fig, ax = plt.subplots()
    sns.barplot(data=melted, x='Factors', y='Scores', hue='Name', ax=ax)
    plt.xticks(rotation=45)
    return fig

def render():
    sensor_defaults = [
        {'Name': 'Tactile Sensor A', 'Cost': 6, 'ISO Compliance': 7, 'Safety': 9, 'Performance': 8},
        {'Name': 'Proximity Sensor B', 'Cost': 5, 'ISO Compliance': 8, 'Safety': 8, 'Performance': 9}
    ]
    df = load_or_create(SENSOR_FILE, sensor_defaults)

    with gr.Blocks() as app:
        with gr.Row():
            name = gr.Textbox(label="📝 Sensor Name")

        with gr.Accordion("📃 ISO Sub-parameters", open=False):
            iso_accuracy = gr.Slider(1, 10, value=5, label="Accuracy Standard")
            iso_protocol = gr.Slider(1, 10, value=5, label="Compliance Protocol")
            iso_cert = gr.Slider(1, 10, value=5, label="Certification Level")

        with gr.Accordion("🔧 Global Weights", open=False):
            weight_cost = gr.Slider(0, 1, value=0.25, label="💰 Cost Weight")
            weight_iso = gr.Slider(0, 1, value=0.25, label="📃 ISO Compliance Weight")
            weight_safety = gr.Slider(0, 1, value=0.25, label="🛡️ Safety Weight")
            weight_perf = gr.Slider(0, 1, value=0.25, label="⚡ Performance Weight")
            update_btn = gr.Button("🔄 Update Rankings")

        add_btn = gr.Button("➕ Add Sensor")
        out_df = gr.Dataframe()
        out_plot = gr.Plot()

        def handle_add(name, iso_accuracy, iso_protocol, iso_cert):
            iso_score = round((iso_accuracy + iso_protocol + iso_cert) / 3, 2)
            new = {
                "Name": name,
                "Cost": 5,
                "ISO Compliance": iso_score,
                "Safety": 5,
                "Performance": 5,
                "ISO Accuracy": iso_accuracy,
                "ISO Protocol": iso_protocol,
                "ISO Certification": iso_cert,
                "Weight Cost": weight_cost.value,
                "Weight ISO": weight_iso.value,
                "Weight Safety": weight_safety.value,
                "Weight Performance": weight_perf.value
            }
            df = load_or_create(SENSOR_FILE, sensor_defaults)
            df = save_entry(SENSOR_FILE, df, new)
            weights = {"Cost": weight_cost.value, "ISO Compliance": weight_iso.value, "Safety": weight_safety.value, "Performance": weight_perf.value}
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        def handle_update(w_cost, w_iso, w_safety, w_perf):
            weights = {"Cost": w_cost, "ISO Compliance": w_iso, "Safety": w_safety, "Performance": w_perf}
            df = load_or_create(SENSOR_FILE, sensor_defaults)
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        add_btn.click(
            fn=handle_add,
            inputs=[name, iso_accuracy, iso_protocol, iso_cert],
            outputs=[out_df, out_plot]
        )

        update_btn.click(
            fn=handle_update,
            inputs=[weight_cost, weight_iso, weight_safety, weight_perf],
            outputs=[out_df, out_plot]
        )

    return app
