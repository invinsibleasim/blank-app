import ipywidgets as widgets
from IPython.display import display, Markdown

# -----------------------------------------------------
# CTM LOSS CALCULATOR
# -----------------------------------------------------

def calculate_ctm(cell_power, num_c, ctm):
    """
    Calculates:
      - Total cell power
      - Module power using CTM ratio
      - CTM losses in watts and %
    """
    total_cell_power = cell_power * num_c
    module_power = total_cell_power * ctm
    ctm_loss_w = total_cell_power - module_power
    ctm_loss_percent = (1 - ctm) * 100

    return total_cell_power, module_power, ctm_loss_w, ctm_loss_percent


# -----------------------------------------------------
# WIDGETS (WEB UI INSIDE JUPYTER)
# -----------------------------------------------------

cell_power_input = widgets.FloatText(
    value=5.2,
    description="Cell Power (W):",
    style={'description_width': '150px'},
)

num_cells_input = widgets.IntText(
    value=60,
    description="Num Cells:",
    style={'description_width': '150px'},
)

ctm_input = widgets.FloatSlider(
    value=0.97,
    min=0.90,
    max=1.00,
    step=0.001,
    description='CTM Ratio:',
    style={'description_width': '150px'},
    readout=True,
)

output = widgets.Output()


def on_calculate_clicked(b):
    with output:
        output.clear_output()

        cell_power = cell_power_input.value
        num_c = num_cells_input.value
        ctm = ctm_input.value

        total_cell_power, module_power, ctm_loss_w, ctm_loss_percent = calculate_ctm(
            cell_power, num_c, ctm
        )

        display(
            Markdown(f"""
# 🔍 CTM Loss Calculation Results

### **Input**
- **Cell Power:** {cell_power:.3f} W  
- **Number of Cells:** {num_c}  
- **CTM Ratio:** {ctm:.3f}

---

### **Output**
- **Total Cell Power:** {total_cell_power:.3f} W  
- **Module Power:** {module_power:.3f} W  
- **CTM Loss:** {ctm_loss_w:.3f} W  
- **CTM Loss Percentage:** {ctm_loss_percent:.2f} %

---
""")
        )


calc_button = widgets.Button(description="Calculate CTM", button_style='success')
calc_button.on_click(on_calculate_clicked)

# -----------------------------------------------------
# DISPLAY UI
# -----------------------------------------------------

ui = widgets.VBox([
    cell_power_input,
    num_cells_input,
    ctm_input,
    calc_button,
    output
])

display(ui)
