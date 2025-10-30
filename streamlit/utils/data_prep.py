import pandas as pd
import streamlit as st
from utils import data_prep_sup

def dt_prep(session=None):
    st.subheader("Input Features")

    left, right = st.columns(2)

    with left:
        hour_of_day = st.number_input("Hour of Day (0–23)", min_value=0, max_value=23, value=22, step=1)
        is_maintenance_window = st.selectbox("Is Maintenance Window?", options=["No", "Yes"], index=0)
        offline_ont_now = st.number_input("Offline ONT Now", min_value=0, max_value=500, value=0, step=1)

        temperature_avg_c = st.number_input("Temperature Avg (°C)", min_value=25.00, max_value=70.00, value=38.06, step=0.01, format="%.2f")
        link_loss_count = st.number_input("Link Loss Count", min_value=0, max_value=1_000, value=1, step=1)
        bad_rsl_count = st.number_input("Bad RSL Count", min_value=0, max_value=1_000, value=0, step=1)
        high_temp_count = st.number_input("High Temperature Count", min_value=0, max_value=1_000, value=0, step=1)

    with right:
        dying_gasp_count = st.number_input("Dying Gasp Count", min_value=0, max_value=1_000, value=0, step=1)
        offline_ont_ratio = st.number_input("Offline ONT Ratio (0–1)", min_value=0.000000, max_value=1.000000, value=0.000371, step=0.000001, format="%.6f")
        fault_rate = st.number_input("Fault Rate (0–1)", min_value=0.000000, max_value=1.000000, value=0.001311, step=0.000001, format="%.6f")
        snr_avg = st.number_input("SNR Average (dB)", min_value=10.000, max_value=50.000, value=25.836, step=0.001, format="%.3f")
        rx_power_avg_dbm = st.number_input("RX Power Avg (dBm)", min_value=-40.000, max_value=-10.000, value=-19.243, step=0.001, format="%.3f")
        trap_trend_score = st.number_input("Trap Trend Score", min_value=0.000000, max_value=2.000000, value=0.007864, step=0.000001, format="%.6f")

    is_maintenance_window_flag = 1 if is_maintenance_window == "Yes" else 0

    # Construct a single-row frame
    df = pd.DataFrame({
        "timestamp_1h": [pd.Timestamp.utcnow().floor("h")],
        "olt_id": ["abc"],
        "hour_of_day": [hour_of_day],
        "is_maintenance_window": [is_maintenance_window_flag],
        "offline_ont_now": [offline_ont_now],
        "temperature_avg_c": [temperature_avg_c],
        "link_loss_count": [link_loss_count],
        "bad_rsl_count": [bad_rsl_count],
        "high_temp_count": [high_temp_count],
        "dying_gasp_count": [dying_gasp_count],
        "offline_ont_ratio": [offline_ont_ratio],
        "fault_rate": [fault_rate],
        "snr_avg": [snr_avg],
        "rx_power_avg_dbm": [rx_power_avg_dbm],
        "trap_trend_score": [trap_trend_score],
    })

    if "timestamp_1h" in df.columns:
        df = df.sort_values("timestamp_1h")

    df = data_prep_sup.handling_skewness(df)
    df = data_prep_sup.add_time_feats(df)
    df = data_prep_sup.add_roll_delta(df, group_key="olt_id", windows=(6, 24))

    roll_cols = [
        c for c in df.columns
        if any(s in c for s in ["_delta_1h", "_roll6h_mean", "_roll24h_mean"])
    ]
 
    feature_cols_all = list(df.columns) + roll_cols
    feature_cols_all = list(dict.fromkeys(feature_cols_all))
    df = df[feature_cols_all]

    df = data_prep_sup.validate_and_reorder_columns(df)

    # show preview
    # st.write(df)

    # Button to make a prediction
    if st.button("🔮 Predict Network Incident"):
        with st.spinner("Analyzing network data... please wait."):
            # Get the prediction and probability
            prediction, probability = data_prep_sup.make_prediction(df, threshold=0.4753, session=session)
            
        # Display the result
        st.subheader("📊 Prediction Result")
        st.write(f"The model predicts: **{'Network Outage (1)' if prediction == 1 else 'No Outage (0)'}**")
        st.write(f"Predicted Probability (Threshold = 0.475): **{probability[0]:.4f}**")

        # Add feedback for the user
        if prediction == 1:
            st.error("⚠️ A network outage is **likely** within the next hour. Please take preventive action!")
        else:
            st.success("✅ The network is **stable** for the next hour. No outage expected.")  
  
    # show sample data
    data_prep_sup.display_sample_data_table()

    return df