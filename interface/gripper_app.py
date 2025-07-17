# gripper_app.py - Gripper Evaluation UI

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

GRIPPER_FILE = "grippers.csv"

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
    gripper_defaults = [
        {'Name': 'Soft Gripper A', 'Cost': 6, 'ISO Compliance': 7, 'Safety': 9, 'Performance': 8},
        {'Name': 'Vacuum Gripper B', 'Cost': 5, 'ISO Compliance': 8, 'Safety': 8, 'Performance': 9}
    ]
    df = load_or_create(GRIPPER_FILE, gripper_defaults)

    with gr.Blocks() as app:
        with gr.Row():
            name = gr.Textbox(label="📝 Gripper Name")
        with gr.Accordion("💰 Cost Sub-parameters", open=False):
            mat = gr.Slider(1, 10, value=5, label="Material")
            typ = gr.Slider(1, 10, value=5, label="Type")
            act = gr.Slider(1, 10, value=5, label="Actuation")
            load = gr.Slider(1, 10, value=5, label="Payload")
            dur = gr.Slider(1, 10, value=5, label="Durability")
            ctrl = gr.Slider(1, 10, value=5, label="Control Systems")
            cust = gr.Slider(1, 10, value=5, label="Customization")
        with gr.Accordion("📃 ISO Sub-parameters", open=False):
            lim = gr.Slider(1, 10, value=5, label="Force Limiting")
            surf = gr.Slider(1, 10, value=5, label="Surface Material")
            acc = gr.Slider(1, 10, value=5, label="Accuracy Standards")
            algo = gr.Slider(1, 10, value=5, label="Control Algorithm")
            mon = gr.Slider(1, 10, value=5, label="Monitoring Systems")
        with gr.Accordion("🛡️ Safety Sub-parameters", open=False):
            imp = gr.Slider(1, 10, value=5, label="Impact Resistance")
            fail = gr.Slider(1, 10, value=5, label="Fail Safe")
            force = gr.Slider(1, 10, value=5, label="Force Limitation")
            comp = gr.Slider(1, 10, value=5, label="Compliant Design")
        with gr.Accordion("⚡ Performance Sub-parameters", open=False):
            vers = gr.Slider(1, 10, value=5, label="Grip Versatility")
            prec = gr.Slider(1, 10, value=5, label="Precision")
            resp = gr.Slider(1, 10, value=5, label="Response Time")
            end = gr.Slider(1, 10, value=5, label="Endurance")
            env = gr.Slider(1, 10, value=5, label="Environmental Adaptability")

        add_btn = gr.Button("➕ Add Gripper")

        with gr.Accordion("🔧 Global Weights", open=False):
            weight_cost = gr.Slider(0, 1, value=0.25, label="💰 Cost Weight")
            weight_iso = gr.Slider(0, 1, value=0.25, label="📃 ISO Compliance Weight")
            weight_safety = gr.Slider(0, 1, value=0.25, label="🛡️ Safety Weight")
            weight_perf = gr.Slider(0, 1, value=0.25, label="⚡ Performance Weight")
            update_btn = gr.Button("🔄 Update Rankings")

        out_df = gr.Dataframe()
        out_plot = gr.Plot()

        def handle_add(name, mat, typ, act, load, dur, ctrl, cust,
                       lim, surf, acc, algo, mon,
                       imp, fail, force, comp,
                       vers, prec, resp, end, env):

            cost_score = round(mat*0.143 + typ*0.143 + act*0.143 + load*0.143 + dur*0.143 + ctrl*0.143 + cust*0.142, 2)
            iso_score = round(lim*0.2 + surf*0.2 + acc*0.2 + algo*0.2 + mon*0.2, 2)
            safe_score = round(imp*0.25 + fail*0.25 + force*0.25 + comp*0.25, 2)
            perf_score = round(vers*0.2 + prec*0.2 + resp*0.2 + end*0.2 + env*0.2, 2)

            new = {"Name": name, "Cost": cost_score, "ISO Compliance": iso_score, "Safety": safe_score, "Performance": perf_score}
            df = load_or_create(GRIPPER_FILE, gripper_defaults)
            df = save_entry(GRIPPER_FILE, df, new)
            weights = {"Cost": weight_cost.value, "ISO Compliance": weight_iso.value, "Safety": weight_safety.value, "Performance": weight_perf.value}
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        def handle_update(w_cost, w_iso, w_safety, w_perf):
            weights = {"Cost": w_cost, "ISO Compliance": w_iso, "Safety": w_safety, "Performance": w_perf}
            df = load_or_create(GRIPPER_FILE, gripper_defaults)
            df = update_scores(df, weights)
            return df[['Name', 'Total Score', 'Rank']], plot_chart(df)

        add_btn.click(
            fn=handle_add,
            inputs=[name, mat, typ, act, load, dur, ctrl, cust,
                    lim, surf, acc, algo, mon,
                    imp, fail, force, comp,
                    vers, prec, resp, end, env],
            outputs=[out_df, out_plot]
        )

        update_btn.click(
            fn=handle_update,
            inputs=[weight_cost, weight_iso, weight_safety, weight_perf],
            outputs=[out_df, out_plot]
        )

    return app
