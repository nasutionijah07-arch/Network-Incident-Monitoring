import pandas as pd
import streamlit as st
import plotly.express as px

def show_model_metrics():
    """
    Displays a simple, styled table for ML model performance metrics.
    """
    st.subheader('🔧 Machine Learning Metrics')

    # Data
    data = {
        'Model': ['CatBoost'],
        'Recall': ['93.6%'],
        'Interpretation': [
            'The model correctly identifies about 94 out of every 100 real network outages. '
            'This means it is very good at catching true problems early, helping the team take '
            'preventive actions before users are affected.'
        ]
    }

    df = pd.DataFrame(data)

    # CSS for custom column widths + wrapping
    st.markdown("""
        <style>
        table {
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
        }
        th, td {
            white-space: normal !important;
            word-wrap: break-word !important;
            text-align: left !important;
            padding: 8px;
            border: 1px solid #dee2e6;
            vertical-align: top;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        th:nth-child(1), td:nth-child(1) { width: 25%; }
        th:nth-child(2), td:nth-child(2) { width: 25%; }
        th:nth-child(3), td:nth-child(3) { width: 50%; }
        </style>
    """, unsafe_allow_html=True)

    # Render table
    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

def show_feature_importance(csv_path="data/feature_importance.csv"):
    """
    Displays an interactive horizontal bar chart of top 5 feature importances
    """

    st.subheader('🔑 Feature Importance - Top 5 Influential Features')

    # Load CSV
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"Error: File not found at {csv_path}")
        return
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return

    # Validate required columns
    required_cols = {'feature', 'importance_mean'}
    if not required_cols.issubset(df.columns):
        st.error("CSV file must contain 'feature' and 'importance_mean' columns.")
        return

    # Keep only the top 5
    df = df.sort_values('importance_mean', ascending=False).head(5)

    # Create bar chart
    fig = px.bar(
        df,
        x='importance_mean',
        y='feature',
        orientation='h',
        color='importance_mean',
        color_continuous_scale='Viridis',
        text='importance_mean',
        height=450
    )

    # Layout & style adjustments
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        hovermode='y',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={
            'categoryorder': 'total ascending',
            'tickfont': dict(size=14)
        },
        xaxis=dict(
            showticklabels=False,
            ticks='',
            showgrid=False
        ),
        margin=dict(t=20, b=0)
    )

    # Trace style
    fig.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0.5,
        textfont=dict(size=14, color='black')
    )

    st.plotly_chart(fig, use_container_width=True)

def show_outage_distribution(csv_path="data/outage_distribution.csv"):
    """
    Displays an elegant, modern donut chart showing the outage vs no-outage distribution.
    CSV must contain columns: 'Category', 'Percentage', and 'Count'.
    """

    st.subheader("📉 Outage Distribution")

    # Load CSV safely
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"Error: File not found at {csv_path}")
        return
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return

    # Validate required columns
    required_cols = {"Category", "Percentage", "Count"}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain columns: 'Category', 'Percentage', and 'Count'.")
        return

    df = df.sort_values("Percentage", ascending=False)

    # --- Enhanced Donut Chart with emphasis on small slice ---
    fig = px.pie(
        df,
        names="Category",
        values="Count",
        color="Category",
        # brighter blue for main, vivid red for outage
        color_discrete_map={
            "Outage": "#dc3545",        # red accent for visibility
            "No Outage": "#007bff",     # clear blue
            "Normal": "#6c757d",        # fallback grey if extra category
        },
        hole=0.55,
    )

    # Emphasize small slice (Outage)
    fig.update_traces(
        pull=[0.25 if c.lower() == "outage" else 0 for c in df["Category"]],
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(size=16, color="white", family="Segoe UI, sans-serif"),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "🧮 Count: %{value:,}<br>"
            "📊 Share: %{percent}<extra></extra>"
        ),
        marker=dict(
            line=dict(color="rgba(255,255,255,0.9)", width=2),
        ),
    )

    # Layout refinements
    fig.update_layout(
        title=dict(
            text="<b>Network Outage vs Normal Operation</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=22, color="#0d6efd", family="Segoe UI, sans-serif"),
        ),
        annotations=[
            dict(
                text="Total<br>{:,}".format(df["Count"].sum()),
                x=0.5, y=0.5,
                font=dict(size=18, color="#212529", family="Segoe UI, sans-serif"),
                showarrow=False,
            )
        ],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color="#343a40", family="Segoe UI, sans-serif"),
            bgcolor="rgba(255,255,255,0.6)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
        ),
        margin=dict(t=80, b=40, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=520,
        uniformtext_minsize=14,
        uniformtext_mode="hide",
    )

    st.plotly_chart(fig, use_container_width=True)
