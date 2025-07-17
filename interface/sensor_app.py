# sensor_app.py - Tactile and Proximity Sensor UI

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

TACTILE_FILE = "tactile_sensors.csv"
PROXIMITY_FILE = "proximity_sensors.csv"


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

def tactile_tab():
    tactile_defaults = [
        {'Name': 'Capacitive Sensor', 'Cost': 5, 'ISO Compliance': 8, 'Safety': 8, 'Performance': 9},
        {'Name': 'Piezoresistive Sensor', 'Cost': 6, 'ISO Compliance': 9, 'Safety': 9, 'Performance': 8}
    ]
    tactile = load_or_create(TACTILE_FILE, tactile_defaults)

    with gr.Tab("Tactile Sensors"):
        with gr.Row():
            name = gr.Textbox(label="📝 Sensor Name")
        with gr.Row():
            cost = gr.Slider(1, 10, value=5, label="💰 Cost")
            safety = gr.Slider(1, 10, value=8, label="🛡️ Safety")
            performance = gr.Slider(1, 10, value=7, label="⚡ Performance")
        with gr.Row():
            sens = gr.Slider(1, 10, value=5, label="🎯 ISO ➜ Sensitivity")
            dur = gr.Slider(1, 10, value=5, label="🏋️ ISO ➜ Durability")
            integ = gr.Slider(1, 10, value=5, label="🔌 ISO ➜ Integration Ease")

        add_btn = gr.Button("➕ Add Tactile Sensor")

        with gr.Accordion("🔧 Global Weights", open=False):
            weight_cost = gr.Slider(0, 1, value=0.25, label="💰 Cost Weight")
            weight_iso = gr.Slider(0, 1, value=0.25, label="📃 ISO Compliance Weight")
            weight_safety = gr.Slider(0, 1, value=0.25, label="🛡️ Safety Weight")
            weight_perf = gr.Slider(0, 1, value=0.25, label="⚡ Performance Weight")
            update_btn = gr.Button("🔄 Update Rankings")

        out_df = gr.Dataframe()
        out_plot = gr.Plot()

        def handle_add(name, cost, safety, performance, sens, dur, integ):
            iso_score = round(sens * 0.5 + dur * 0.3 + integ * 0.2, 2)
            new = {"Name": name, "Cost": cost, "ISO Compliance": iso_score, "Safety": safety, "Performance": performance}
            df = load_or_create(TACTILE_FILE, tactile_defaults)
            df = save_entry(TACTILE_FILE, df, new)
            return df[['Name', 'Cost', 'ISO Compliance', 'Safety', 'Performance']], plot_chart(df)

        def handle_update(w_cost, w_iso, w_safety, w_perf):
            weights = {"Cost": w_cost, "ISO Compliance": w_iso, "Safety": w_safety, "Performance": w_perf}
            df = load_or_create(TACTILE_FILE, tactile_defaults)
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        add_btn.click(fn=handle_add, inputs=[name, cost, safety, performance, sens, dur, integ], outputs=[out_df, out_plot])
        update_btn.click(fn=handle_update, inputs=[weight_cost, weight_iso, weight_safety, weight_perf], outputs=[out_df, out_plot])

def proximity_tab():
    proximity_defaults = [
        {'Name': 'Ultrasonic Sensor', 'Cost': 4, 'ISO Compliance': 7, 'Safety': 9, 'Performance': 8},
        {'Name': 'LIDAR Sensor', 'Cost': 8, 'ISO Compliance': 9, 'Safety': 8, 'Performance': 10}
    ]
    prox = load_or_create(PROXIMITY_FILE, proximity_defaults)

    with gr.Tab("Proximity Sensors"):
        with gr.Row():
            name = gr.Textbox(label="📝 Sensor Name")
        with gr.Row():
            cost = gr.Slider(1, 10, value=5, label="💰 Cost")
            iso = gr.Slider(1, 10, value=7, label="📃 ISO Compliance")
            safety = gr.Slider(1, 10, value=8, label="🛡️ Safety")
        with gr.Row():
            rng = gr.Slider(1, 10, value=5, label="📡 Performance ➜ Range")
            acc = gr.Slider(1, 10, value=5, label="🎯 Performance ➜ Accuracy")
            resp = gr.Slider(1, 10, value=5, label="⚡ Performance ➜ Response Time")

        add_btn = gr.Button("➕ Add Proximity Sensor")

        with gr.Accordion("🔧 Global Weights", open=False):
            weight_cost = gr.Slider(0, 1, value=0.25, label="💰 Cost Weight")
            weight_iso = gr.Slider(0, 1, value=0.25, label="📃 ISO Compliance Weight")
            weight_safety = gr.Slider(0, 1, value=0.25, label="🛡️ Safety Weight")
            weight_perf = gr.Slider(0, 1, value=0.25, label="⚡ Performance Weight")
            update_btn = gr.Button("🔄 Update Rankings")

        out_df = gr.Dataframe()
        out_plot = gr.Plot()

        def handle_add(name, cost, iso, safety, rng, acc, resp):
            perf_score = round(rng * 0.4 + acc * 0.4 + resp * 0.2, 2)
            new = {"Name": name, "Cost": cost, "ISO Compliance": iso, "Safety": safety, "Performance": perf_score}
            df = load_or_create(PROXIMITY_FILE, proximity_defaults)
            df = save_entry(PROXIMITY_FILE, df, new)
            return df[['Name', 'Cost', 'ISO Compliance', 'Safety', 'Performance']], plot_chart(df)

        def handle_update(w_cost, w_iso, w_safety, w_perf):
            weights = {"Cost": w_cost, "ISO Compliance": w_iso, "Safety": w_safety, "Performance": w_perf}
            df = load_or_create(PROXIMITY_FILE, proximity_defaults)
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        add_btn.click(fn=handle_add, inputs=[name, cost, iso, safety, rng, acc, resp], outputs=[out_df, out_plot])
        update_btn.click(fn=handle_update, inputs=[weight_cost, weight_iso, weight_safety, weight_perf], outputs=[out_df, out_plot])

def render():
    with gr.Blocks() as sensor_app:
        with gr.Tab("🔬 Tactile Sensors"):
            tactile_tab()
        with gr.Tab("📡 Proximity Sensors"):
            proximity_tab()
    return sensor_app
