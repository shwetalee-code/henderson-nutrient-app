import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.markdown("## SCU/Henderson Farm Practicum 2025 Analytics Dashboard")

# Load the dataset
analysisDf = pd.read_csv("analysisDf_for_interactive.csv")

# --- DROPDOWN 1: Sample ID ---
sample_options = analysisDf[analysisDf['DataType'] == 'Nutrient']['SampleID'].unique()
setSample = st.selectbox("Select Sample ID", sorted(sample_options))

# --- DROPDOWN 2: Plot Type ---
plot_type = st.selectbox("Select Plot Type", ["WS", "Mehlich"])

# --- FIRST PLOT: Sample-wise WS or Mehlich chart ---
with st.container():
    filtered_df = analysisDf[
        (analysisDf["SampleID"] == setSample) &
        (analysisDf["DataType"] == "Nutrient")
    ]

    if not filtered_df.empty:
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.set_style("whitegrid")
        x = np.arange(len(filtered_df))
        width = 0.4

        if plot_type == "WS":
            ax1.bar(x - width/2, filtered_df["WS_Current"], width=width, color="lightblue", label="WS_Current")
            ax1.bar(x + width/2, filtered_df["WS_Ideal"], width=width, color="orange", label="WS_Ideal")
            ax1.set_title(f"Nutrient WS_Current vs WS_Ideal for Sample {setSample}")
        else:
            ax1.bar(x - width/2, filtered_df["Mehlich_Current"], width=width, color="lightblue", label="Mehlich_Current")
            ax1.bar(x + width/2, filtered_df["Mehlich_Ideal"], width=width, color="orange", label="Mehlich_Ideal")
            ax1.set_title(f"Nutrient Mehlich_Current vs Mehlich_Ideal for Sample {setSample}")

        ax1.set_xticks(x)
        ax1.set_xticklabels(filtered_df["Parameter"], rotation=45, ha="right")
        ax1.set_xlabel("Nutrient")
        ax1.set_ylabel("Value")
        ax1.legend()
        st.pyplot(fig1)
    else:
        st.warning("No nutrient data found for the selected sample.")

# --- SPACER BEFORE SAMPLE-WISE COMPARISON ---
st.markdown("---")

# --- DROPDOWN 3: Nutrient for Sample Comparison ---
nutrient_options = ['Calcium', 'Magnesium', 'Potassium', 'Sodium', 'Phosphorus',
       'Sulfur', 'Chloride', 'Silicon', 'Iodine', 'Boron', 'Molybdenum',
       'Selenium', 'Aluminum', 'Iron', 'Manganese', 'Zinc', 'Copper',
       'Cobalt']
setNutrient_sample = st.selectbox("Select Nutrient for Sample-wise Comparison", nutrient_options)

# --- SECOND PLOT: WS_Current values for selected nutrient across samples ---
nutrient_df_sample = analysisDf[analysisDf["Parameter"] == setNutrient_sample]

if not nutrient_df_sample.empty:
    ws_ideal = nutrient_df_sample["WS_Ideal"].dropna().unique()
    ws_ideal = ws_ideal[0] if len(ws_ideal) > 0 else None

    fig2, ax2 = plt.subplots(figsize=(12, 10))
    sns.set_style("whitegrid")

    sns.barplot(data=nutrient_df_sample, y="SampleID", x="WS_Current", color="#FF8899", ax=ax2, errorbar=None)

    for i, row in enumerate(nutrient_df_sample.itertuples()):
        ax2.text(row.WS_Current, i, f'{row.WS_Current:.2f}', va='center', ha='left', fontsize=10, color="black")

    if ws_ideal is not None:
        ax2.axvline(x=ws_ideal, color="#77BBDD", linestyle="--", label=f"Ideal Value: {ws_ideal}")
        ax2.legend()

    ax2.set_xlabel("WS_Current Value")
    ax2.set_ylabel("Sample ID")
    ax2.set_title(f"Water Soluble - {setNutrient_sample} - Across Samples")
    st.pyplot(fig2)
else:
    st.warning("No data found for the selected nutrient.")

# --- SPACER BEFORE FIELD-WISE COMPARISON ---
st.markdown("---")

# --- DROPDOWN 4: Nutrient for Field Comparison ---
setNutrient_field = st.selectbox("Select Nutrient for Field-wise Comparison", nutrient_options)

# --- THIRD PLOT: Mean/Min/Max WS_Current by Field ---
nutrient_df_field = analysisDf[analysisDf["Parameter"] == setNutrient_field]

if not nutrient_df_field.empty:
    stat_df = nutrient_df_field.groupby("Field", as_index=False)["WS_Current"].agg(["min", "max", "mean"]).reset_index()
    ws_ideal = nutrient_df_field["WS_Ideal"].dropna().unique()
    ws_ideal = ws_ideal[0] if len(ws_ideal) > 0 else None

    fig3, ax3 = plt.subplots(figsize=(12, 8))
    sns.set_style("whitegrid")

    sns.barplot(data=stat_df, y="Field", x="mean", color="#FF8899", ax=ax3, errorbar=None)

    for idx, row in stat_df.iterrows():
        ax3.hlines(y=row["Field"], xmin=row["min"], xmax=row["max"], color="#FFDD88", linewidth=2)
        ax3.text(row["mean"], row["Field"], f'{row["mean"]:.2f}', va='center', ha='left', fontsize=10, color="black")

    if ws_ideal is not None:
        ax3.axvline(x=ws_ideal, color="#7799CC", linestyle="--", label=f"Ideal Value: {ws_ideal}")
        ax3.legend()

    ax3.set_xlabel("WS_Current Value")
    ax3.set_ylabel("Field")
    ax3.set_title(f"Water Soluble - {setNutrient_field} - by Fields")
    st.pyplot(fig3)
else:
    st.warning("No data found for the selected nutrient.")

# --- SPACER BEFORE TOP FIELDS PLOT ---
st.markdown("---")

# --- DROPDOWN 5: Nutrient for Top 5 Fields ---
setNutrient_top_fields = st.selectbox("Select Nutrient to View Top 5 Fields by Mean Value", nutrient_options)

# --- FOURTH PLOT: Top 5 Fields by Mean WS_Current ---
nutrient_df_top = analysisDf[analysisDf["Parameter"] == setNutrient_top_fields]

if not nutrient_df_top.empty:
    stat_df_top = nutrient_df_top.groupby("Field", as_index=False)["WS_Current"].agg(["min", "max", "mean"]).reset_index()
    stat_df_top = stat_df_top.sort_values("mean", ascending=False).head(5)
    ws_ideal_top = nutrient_df_top["WS_Ideal"].dropna().unique()
    ws_ideal_top = ws_ideal_top[0] if len(ws_ideal_top) > 0 else None

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")

    sns.barplot(data=stat_df_top, y="Field", x="mean", color="#FF8899", ax=ax4, errorbar=None)

    for idx, row in stat_df_top.iterrows():
        ax4.hlines(y=row["Field"], xmin=row["min"], xmax=row["max"], color="#FFDD88", linewidth=2)
        ax4.text(row["mean"], row["Field"], f'{row["mean"]:.2f}',
                 va='center', ha='left', fontsize=10, color="black")

    if ws_ideal_top is not None:
        ax4.axvline(x=ws_ideal_top, color="#7799CC", linestyle="--", label=f"Ideal Value: {ws_ideal_top}")
        ax4.legend()

    ax4.set_xlabel("WS_Current Value")
    ax4.set_ylabel("Field")
    ax4.set_title(f"Top 5 Fields by Water Soluble {setNutrient_top_fields}")
    st.pyplot(fig4)
else:
    st.warning("No data found for the selected nutrient.")

# --- SPACER BEFORE DISTRIBUTION PLOT ---
st.markdown("---")

# --- DROPDOWN 6: Nutrient Distribution Strip Plot ---
WSD_options = analysisDf['Parameter'].dropna().unique()
setWSD = st.selectbox("Select Nutrient to View Distribution by Field", sorted(WSD_options))

# --- FIFTH PLOT: Strip Distribution by Field ---
WSD_byF_df = analysisDf[analysisDf["Parameter"] == setWSD]

if not WSD_byF_df.empty:
    fig5, ax5 = plt.subplots(figsize=(12, 10))
    sns.set_style("whitegrid")
    wsd_ideal = WSD_byF_df["Ideal"].dropna().unique()
    wsd_ideal = wsd_ideal[0] if len(wsd_ideal) > 0 else None

    sns.stripplot(data=WSD_byF_df, y="Field", x="Current", color="#FF8899", jitter=True, ax=ax5)

    if wsd_ideal is not None:
        ax5.axvline(x=wsd_ideal, color="#7799CC", linestyle="--", label=f"Ideal Value: {wsd_ideal}")
        ax5.legend()

    ax5.set_xlabel("Value")
    ax5.set_ylabel("Field")
    ax5.set_title(f"{setWSD} distribution by Fields")
    st.pyplot(fig5)
else:
    st.warning("No data found for the selected nutrient.")
