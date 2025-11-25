import streamlit as st
import pandas as pd
import plotly.express as px
#import fitz  # PyMuPDF for PDF export
from io import BytesIO
st.title("Advanced CTM Loss Calculator")

# Initialize session state for multiple modules
if "modules" not in st.session_state:
    st.session_state.modules = []

st.header("Add Module Parameters")

# Input fields for one module
cell_power = st.number_input("Cell Power (Wp)", min_value=0.0, value=5.0)
cell_efficiency = st.number_input("Cell Efficiency (%)", min_value=0.0, value=18.0)
num_cells = st.number_input("Number of Cells", min_value=1, value=60)
module_area = st.number_input("Module Area (m²)", min_value=0.0, value=1.6)
cell_length = st.number_input("Cell Length (mm)", min_value=0.0, value=156.0)
cell_width = st.number_input("Cell Width (mm)", min_value=0.0, value=156.0)
glass_transmission = st.number_input("Glass Transmission (%)", min_value=0.0, value=91.0)
encapsulant_transmission = st.number_input("Encapsulant Transmission (%)", min_value=0.0, value=95.0)
num_busbars = st.number_input("Number of Busbars", min_value=1, value=5)
ribbon_width = st.number_input("Ribbon Width (mm)", min_value=0.0, value=1.5)
ribbon_thickness = st.number_input("Ribbon Thickness (mm)", min_value=0.0, value=0.2)
cell_binning_tolerance = st.number_input("Cell Binning Tolerance (±%)", min_value=0.0, value=2.0)
junction_box_loss = st.number_input("Junction Box & Cable Loss (%)", min_value=0.0, value=0.5)

if st.button("Add Module"):
    total_cell_power = cell_power * num_cells
    optical_loss = 100 - ((glass_transmission * encapsulant_transmission) / 100)
    resistive_loss = 0.5  # Placeholder for advanced calculation
    mismatch_loss = cell_binning_tolerance
    additional_loss = junction_box_loss
    final_module_power = total_cell_power * (1 - (optical_loss + resistive_loss + mismatch_loss + additional_loss)/100)
    ctm_ratio = (final_module_power / total_cell_power) * 100

    st.session_state.modules.append({
        "Cell Power": cell_power,
        "Num Cells": num_cells,
        "Total Cell Power": total_cell_power,
        "Final Module Power": final_module_power,
        "CTM Ratio": ctm_ratio,
        "Optical Loss": optical_loss,
        "Resistive Loss": resistive_loss,
        "Mismatch Loss": mismatch_loss,
        "Additional Loss": additional_loss
    })

# Display all modules
if st.session_state.modules:
    st.subheader("Module Comparison")
    df = pd.DataFrame(st.session_state.modules)
    st.write(df)

    # Chart for CTM Ratio comparison
    fig_ctm = px.bar(df, x=df.index, y="CTM Ratio", title="CTM Ratio Comparison", labels={"x":"Module Index"})
    st.plotly_chart(fig_ctm)

    # Optimization suggestions
    st.subheader("Optimization Suggestions")
    st.write("- Improve glass and encapsulant transmission to reduce optical losses.")
    st.write("- Optimize busbar and ribbon design to minimize resistive losses.")
    st.write("- Reduce cell binning tolerance for better mismatch performance.")

    # PDF Export
    if st.button("Export to PDF"):
        pdf_buffer = BytesIO()
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "CTM Loss Analysis Report", fontsize=18)
        page.insert_text((50, 80), "Module Comparison Data" + df.to_string(index=False), fontsize=12)
        page.insert_text((50, 300), "Optimization Suggestions:- Improve optical transmission- Optimize busbar design- Reduce mismatch losses", fontsize=12)
        doc.save(pdf_buffer)
        doc.close()
        st.download_button("Download PDF", data=pdf_buffer.getvalue(), file_name="CTM_Loss_Analysis_Report.pdf", mime="application/pdf")

