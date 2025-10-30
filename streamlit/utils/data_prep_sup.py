import numpy as np
import pandas as pd
import streamlit as st
from snowflake.ml.registry import Registry
from snowflake.snowpark.context import get_active_session

ROLL_KEYS = [
    "link_loss_count_log", "bad_rsl_count_log", "high_temp_count_log",
    "dying_gasp_count_log", "offline_ont_now_log"
]

@st.cache_resource
def get_registry(_session=None):
    if _session is None:
        _session = get_active_session()
    return Registry(session=_session)

def handling_skewness(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    skewed_feats = [
        "offline_ont_now", "bad_rsl_count", "link_loss_count",
        "dying_gasp_count", "high_temp_count"
    ]
    
    for col in skewed_feats:
        if col in df.columns:
            df[f"{col}_log"] = np.log1p(np.clip(df[col], 0, None))
        else:
            print(f"Warning: Column '{col}' not found; skipping log transform.")
   
    df.drop(columns=[c for c in skewed_feats if c in df.columns], inplace=True)
    return df

def add_time_feats(df):
    df = df.copy()
    df['hour_sin'] = np.sin(2*np.pi * df['hour_of_day']/24.0)
    df['hour_cos'] = np.cos(2*np.pi * df['hour_of_day']/24.0)
    return df

def _safe_numeric(df: pd.DataFrame, cols) -> pd.DataFrame:
    f = df.copy()
    for c in cols:
        if c in f.columns:
            f[c] = pd.to_numeric(f[c], errors="coerce")
    f.replace([np.inf, -np.inf], np.nan, inplace=True)
    return f

def add_roll_delta(f: pd.DataFrame, group_key: str | None = None, windows=(6, 24)) -> pd.DataFrame:
    f = _safe_numeric(f, ROLL_KEYS).copy()

    # choose grouping
    temp_group_col = None
    if group_key is not None and group_key in f.columns:
        grp = f.groupby(group_key, dropna=False)
    else:
        temp_group_col = "__grp__"
        f[temp_group_col] = 0
        grp = f.groupby(temp_group_col, dropna=False)

    # sort within groups if timestamp column exists
    if "timestamp_1h" in f.columns:
        f = f.sort_values(["timestamp_1h"] + ([group_key] if group_key in f.columns else [temp_group_col]))

    # deltas in log-space (multiplicative change); fill NaN with 0 for first row
    for col in ROLL_KEYS:
        if col in f.columns:
            d = grp[col].diff()
            f[col + "_delta_1h"] = d.fillna(0.0).astype(float)

    # rolling means in log-space; min_periods=1 makes 1-row safe
    for w in windows:
        for col in ROLL_KEYS:
            if col in f.columns:
                r = grp[col].rolling(w, min_periods=1).mean().reset_index(level=0, drop=True)
                f[f"{col}_roll{w}h_mean"] = r.astype(float)

    # cleanup temp group col
    if temp_group_col is not None:
        f.drop(columns=[temp_group_col], inplace=True)

    return f

@st.cache_data
def _load_feature_columns(path='data/features.csv'):
    return pd.read_csv(path, header=None)[0].tolist()

def validate_and_reorder_columns(df, feature_columns_path='data/features.csv'):
    feature_columns = _load_feature_columns(feature_columns_path)
    common_cols = [c for c in feature_columns if c in df.columns]
    return df[common_cols]

@st.cache_resource
def load_model(model_name: str = "catboost_outage_predictor", version: str = "v1", _session=None):
    registry = get_registry(_session=_session)
    try:
        model = registry.get_model(model_name)
        model_version = model.version(version)
        return model_version.load(force=True)
    except Exception as e:
        raise ValueError(f"❌ Error loading model '{model_name}' version '{version}': {e}")

def make_prediction(df: pd.DataFrame, threshold: float = 0.4753, session=None):
    try:
        model = load_model(_session=session)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    if model is None:
        proba = np.array([0.0])
        label = int(proba[0] >= threshold)
        return label, proba

    try:
        proba = model.predict_proba(df)[:, 1]
    except AttributeError:
        try:
            raw = model.decision_function(df)
            proba = 1 / (1 + np.exp(-np.asarray(raw)))
        except Exception:
            proba = np.zeros(len(df))

    label = int(proba[0] >= threshold)
    return label, proba

def display_sample_data_table():
    try:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader('📡 Sample Network Features')
        st.markdown("<br>", unsafe_allow_html=True)

        # Features ordered from intuitive → technical, target last
        data = {
            'Features': [
                "Hour of Day (0–23)",
                "Is Maintenance Window?",
                "Offline ONT Now",
                "Temperature Avg (°C)",
                "Link Loss Count",
                "Bad RSL Count",
                "High Temperature Count",
                "Dying Gasp Count",
                "Offline ONT Ratio (0–1)",
                "Fault Rate (0–1)",
                "SNR Average (dB)",
                "RX Power Avg (dBm)",
                "Trap Trend Score",
                "Outage in the next hour",  # target
            ],
            'No Outage Sample': [
                22,            # hour_of_day
                "No",          # is_maintenance_window
                0,             # offline_ont_now
                38.06,         # temperature_avg_c
                1,             # link_loss_count
                0,             # bad_rsl_count
                0,             # high_temp_count
                0,             # dying_gasp_count
                0.000371,      # offline_ont_ratio
                0.001311,      # fault_rate
                25.836,        # snr_avg
                -19.243,       # rx_power_avg_dbm
                0.007864,      # trap_trend_score
                0,             # label_outage_1h
            ],
            'Outage Sample': [
                19,             # hour_of_day
                "No",           # is_maintenance_window
                16,             # offline_ont_now
                38.63,          # temperature_avg_c
                0,              # link_loss_count
                0,              # bad_rsl_count
                0,              # high_temp_count
                0,              # dying_gasp_count
                0.043431,       # offline_ont_ratio
                0.000000,       # fault_rate
                24.452,         # snr_avg
                -20.044,        # rx_power_avg_dbm
                0.650829,       # trap_trend_score
                1,              # label_outage_1h
            ]
        }

        # Force string dtype for Arrow/Styler compatibility in Streamlit
        df = pd.DataFrame({
            'Features': pd.Series(data['Features'], dtype='string'),
            'No Outage Sample': pd.Series(list(map(str, data['No Outage Sample'])), dtype='string'),
            'Outage Sample': pd.Series(list(map(str, data['Outage Sample'])), dtype='string'),
        })

        # Highlight target row (last row)
        def highlight_row(row):
            return ['background-color: yellow' if row.name == len(df)-1 else '' for _ in row]

        styled_df = df.style.apply(highlight_row, axis=1)

        st.dataframe(
            styled_df,
            height=532,
            width="stretch",
            hide_index=False,
            column_config={
                "Features": st.column_config.TextColumn("Features"),
                "No Outage Sample": st.column_config.TextColumn("No Outage Sample"),
                "Outage Sample": st.column_config.TextColumn("Outage Sample"),
            },
        )

    except Exception as e:
        st.error(f"Error displaying sample data: {str(e)}")
        # Fallback display (unstyled)
        st.dataframe(pd.DataFrame(data), height=740, use_container_width=True)