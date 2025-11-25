import ipywidgets as widgets
from IPython.display import display, HTML
import pandas as pd
import plotly.graph_objects as go
import io

# ======================================================================
#                       CALCULATION FUNCTION
# ======================================================================

def calculate_ctm(cell_power, num_cells, ctm):
    total_cell_power = cell_power * num_cells
    module_power = total_cell_power * ctm
    loss_w = total_cell_power - module_power
    loss_pct = (1 - ctm) * 100
    return total_cell_power, module_power, loss_w, loss_pct


# ======================================================================
#                       UI ELEMENTS (WIDGETS)
# ======================================================================

style = {'description_width': '150px'}
layout = widgets.Layout(width='400px')

cell_power_input = widgets.FloatText(
    value=5.2, description="Cell Power (W):", style=style, layout=layout
)

num_cells_input = widgets.IntText(
    value=60, description="Num Cells:", style=style, layout=layout
)

ctm_input = widgets.FloatSlider(
    value=0.97, min=0.90, max=1.00, step=0.001,
    description="CTM Ratio:", style=style, layout=layout
)

calc_button = widgets.Button(
    description="Calculate", button_style="success", layout=layout
)

download_button = widgets.Button(
    description="Download CSV", button_style="info", layout=layout
)
download_button.disabled = True  # enabled after calculation

output_box = widgets.Output()
graph_box = widgets.Output()


# ======================================================================
#                       CSV BUFFER
# ======================================================================

csv_buffer = None


# ======================================================================
#                   CALCULATION BUTTON CALLBACK
# ======================================================================

def on_calculate_clicked(b):
    global csv_buffer
    with output_box:
        output_box.clear_output()

        cell_power = cell_power_input.value
        num_c = num_cells_input.value
        ctm = ctm_input.value

        total_cell, mod_power, loss_w, loss_pct = calculate_ctm(cell_power, num_c, ctm)

        # Prepare CSV
        df = pd.DataFrame({
            "Metric": ["Total Cell Power", "Module Power", "CTM Loss (W)", "CTM Loss (%)"],
            "Value": [total_cell, mod_power, loss_w, loss_pct]
        })

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Display results
        display(HTML(f"""
        <div style="
            background:#f8faff;
            padding:20px;
            margin-top:10px;
            border-radius:10px;
            width:480px;
            font-family:Arial; font-size:15px;">
            <h3 style="color:#0A3D91;">CTM Calculation Results</h3>
            <p><b>Total Cell Power:</b> {total_cell:.3f} W</p>
            <p><b>Module Power:</b> {mod_power:.3f} W</p>
            <p><b>CTM Loss:</b> {loss_w:.3f} W</p>
            <p><b>CTM Loss (%):</b> {loss_pct:.2f} %</p>
        </div>
        """))

        download_button.disabled = False

    # Update graph
    with graph_box:
        graph_box.clear_output()

        ctm_values = [x / 1000 for x in range(900, 1001)]
        module_power_curve = [(cell_power * num_c) * c for c in ctm_values]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ctm_values,
            y=module_power_curve,
            mode='lines',
            name="Module Power Curve",
            line=dict(color="blue", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=[ctm], y=[mod_power],
            mode='markers',
            marker=dict(color="red", size=12),
            name="Selected CTM"
        ))

        fig.update_layout(
            title="Module Power vs CTM Ratio",
            xaxis_title="CTM Ratio",
            yaxis_title="Module Power (W)",
            template="plotly_white",
            width=700, height=450
        )

        fig.show()


calc_button.on_click(on_calculate_clicked)


# ======================================================================
#                         CSV DOWNLOAD CALLBACK
# ======================================================================

def on_download_clicked(b):
    with output_box:
        data = csv_buffer.getvalue().encode()
        b.data = data
        b.filename = "ctm_results.csv"
        b._repr_mimebundle_ = lambda *args: {}


download_button.on_click(on_download_clicked)


# ======================================================================
#                       DISPLAY FINAL UI
# ======================================================================

display(HTML("""
<h2 style="font-family:Arial; color:#0A3D91;">CTM Loss of PV Module Calculator</h2>
<p style="font-family:Arial; font-size:15px; width:600px;">
A complete interactive CTM (Cell-to-Module) loss calculator with Bootstrap-like UI, Plotly graph, and CSV export.
</p>
"""))

ui = widgets.VBox([
    cell_power_input,
    num_cells_input,
    ctm_input,
    calc_button,
    download_button,
    output_box,
    graph_box
])

display(ui)
