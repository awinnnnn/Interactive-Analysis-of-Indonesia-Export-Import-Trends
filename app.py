import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_excel(
    io="data_perdagangan.xlsx",
    engine="openpyxl",
    sheet_name="exim", # Nama sheet (sesuai nama yang ada di pojok kiri bawah excel)
    skiprows=0, # Lewati baris pertama (header)
    usecols="A:H", # Pilih kolom A sampai H
)

# emoji: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title = "Dashboard Perdagangan Indonesia",
    page_icon = "📊",
    layout="wide",
)

# --- SIDE BAR ---
st.sidebar.header("Please Filter Here: ")

Negara = st.sidebar.multiselect(
    "Select the country: ",
    options=df["Negara"].unique(),
    default=df["Negara"].unique()
)

Tahun = st.sidebar.multiselect(
    "Select the year: ",
    options=df["Tahun"].unique(),
    default=df["Tahun"].unique()
)

Indikator = st.sidebar.multiselect(
    "Select the indicator: ",
    options=df["Indikator"].unique(),
    default=df["Indikator"].unique()
)

df_selection = df.query(
    "Negara == @Negara & Tahun == @Tahun & Indikator == @Indikator"
)

# --- MAIN PAGE ---
st.title(":bar_chart: Dashboard Perdagangan Indonesia")
st.markdown("")

# TOP Key Performance Indicators (KPI)
total_jumlah = int(df_selection["Jumlah"].sum())
average_jumlah = round(df_selection["Jumlah"].mean(),2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total transaksi: ")
    st.subheader(f"US$ {total_jumlah:,}")
with right_column:
    st.subheader("Rata-rata transaksi")
    st.subheader(f"US$ {average_jumlah:,}")

st.markdown("---")

# st.dataframe(df_selection)

# --- Visualization ---
jumlah_by_label = df_selection.groupby(by=["Label"]).sum()[["Jumlah"]].sort_values(by="Jumlah", ascending=True).tail(10)

fig_tahun_jumlah = px.bar(
    jumlah_by_label,
    x="Jumlah",
    y=jumlah_by_label.index,
    orientation="h",
    title="<b>Top 10 Jumlah Transaksi Berdasakan Label</b>",
    color_discrete_sequence=["#3333FF"] * len(jumlah_by_label),
    template="plotly_white",
)

# Assuming jumlah_by_tahun.index is your y-axis (year or long text)
original_labels = jumlah_by_label.index.astype(str).tolist()

# Truncate each label to first 15 characters
truncated_labels = [label[:30] + "..." if len(label) > 30 else label for label in original_labels]

fig_tahun_jumlah.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=dict(
        tickmode='array',
        tickvals=original_labels,
        ticktext=truncated_labels
    )
)

st.plotly_chart(fig_tahun_jumlah, use_container_width=True)

# --- HIDE STREAMLIT STYLE ---
hide_st_style="""
    <style>
    #MainMenu {visibility: hiddem;}
    footer {visibility: hiddem;}
    header {visibility: hiddem;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Increase sidebar text size */
    [data-testid="stSidebar"] * {
        font-size: 15px !important;  /* Change to desired font size */
    }
    /* Change background color of the entire app */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Change multiselect choice background */
    span[data-baseweb="tag"] {
        background-color: #3333FF !important;
        color: white !important;
    }
    /* Change selectbox dropdown border */
    div[data-baseweb="select"] > div:first-child {
        border-color: #3333FF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)