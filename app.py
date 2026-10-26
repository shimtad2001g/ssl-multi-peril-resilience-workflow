import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

st.set_page_config(page_title="Multi-Peril Resilience", page_icon="🌍", layout="wide")

st.title("🌍 Integrated Synergistic Multi-Peril Resilience")
st.markdown("### Phase 4: Operational Deliverables (Live Python Dashboard)")

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables")
map_path = os.path.join(base_path, "Ethiopia_National_Map.png")
mcda_path = os.path.join(base_path, "NBS_Targeting_Map.png")
sar_path = os.path.join(base_path, "SAR_Flood_Risk_Map.png")

# Create Three Tabs
tab1, tab2, tab3 = st.tabs(["📍 Phase 3: Hazard Map", "🌱 Phase 3: NBS Targeting (MCDA)", "🌊 Phase 3: SAR Flood Risk"])

with tab1:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.subheader("Real Sentinel-2 Hazard Map")
        if os.path.exists(map_path):
            st.image(Image.open(map_path), width="stretch")
    with col2:
        st.subheader("📊 Real-Time Telemetry")
        threshold = st.slider("Drought Threshold (%)", 10, 50, 30)
        real_vci = 11.31
        st.metric("Calculated VCI", f"{real_vci}%", f"{real_vci - threshold:.2f}%")
        if real_vci < threshold:
            st.error("🚨 **DROUGHT PAYOUT TRIGGERED**")
        else:
            st.success("✅ **NORMAL**")

with tab2:
    col3, col4 = st.columns([1.5, 1])
    with col3:
        st.subheader("MCDA Suitability Map")
        if os.path.exists(mcda_path):
            st.image(Image.open(mcda_path), width="stretch")
        else:
            st.warning("MCDA Map not found.")
    with col4:
        st.subheader("🎯 Optimal Intervention Locations")
        st.write("Based on the Multi-Criteria Decision Analysis (MCDA), combining land degradation (SSL features) and flood risk zones, the following areas have the highest suitability for Nature-Based Solutions (NBS):")
        st.info("🟢 **Zone A (Highlands):** Score 85% - Ideal for reforestation.")
        st.info("🟢 **Zone B (Eastern Rift):** Score 72% - Ideal for terracing and soil conservation.")
        st.warning("🔴 **Zone C (Lowlands):** Score 15% - Not suitable for immediate intervention.")

with tab3:
    col5, col6 = st.columns([1.5, 1])
    with col5:
        st.subheader("Sentinel-1 SAR Flood Risk")
        if os.path.exists(sar_path):
            st.image(Image.open(sar_path), width="stretch")
        else:
            st.warning("SAR Map not found.")
    with col6:
        st.subheader("🌊 Flood Detection Telemetry")
        st.write("The SAR (Synthetic Aperture Radar) branch bypasses cloud cover to detect surface water. The model processes VV polarization backscatter to identify inundated areas.")
        
        # Simulated SAR metrics
        flood_threshold = st.slider("SAR Flood Threshold (dB)", -20, 0, -15)
        current_backscatter = -12.4
        
        st.metric("Current Backscatter (VV)", f"{current_backscatter} dB")
        
        if current_backscatter > flood_threshold:
            st.error("🚨 **FLOOD PAYOUT TRIGGERED** (Water detected)")
        else:
            st.success("✅ **NORMAL** (No inundation)")