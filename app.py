import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Zabsi Vehicle Control", page_icon="🛻", layout="wide")

st.title("📊 ZABSI Fleet & Booking Control System")
st.markdown("Sistem Log Penggunaan Kenderaan, Lokasi Projek, dan Jenis Bahan Bakar Syarikat.")

csv_file = "vehicle_data.csv"

if not os.path.exists(csv_file):
    st.error(f"Fail '{csv_file}' tidak dijumpai. Sila pastikan fail CSV berada di dalam folder project PyCharm.")
else:
    df = pd.read_csv(csv_file)

    # Tukar format tarikh kepada datetime agar boleh dikira oleh Python
    df["Tarikh Mula"] = pd.to_datetime(df["Tarikh Mula"])
    df["Tarikh Tamat"] = pd.to_datetime(df["Tarikh Tamat"])

    today = datetime.datetime.now()

    # --- INTERFACE UTAMA: PAPARAN JADUAL ---
    st.subheader("📋 Log Induk Tempahan Kenderaan")
    st.dataframe(df, width="stretch")

    # --- LOGIK STATUS TUGASAN PROJEK ---
    st.subheader("⚡ Status Tugasan Semasa Semasa Projek")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏃‍♂️ Kenderaan Sedang Bergerak / Aktif")
        active_count = 0
        for index, row in df.iterrows():
            # Semak jika hari ini berada di dalam lingkungan tarikh mula dan tamat
            if pd.notnull(row["Tarikh Mula"]) and pd.notnull(row["Tarikh Tamat"]):
                if row["Tarikh Mula"] <= today <= row["Tarikh Tamat"]:
                    st.info(f"**{row['Kenderaan']} ({row['No. Pendaftaran']})**\n\n"
                            f"📍 **Lokasi:** {row['Lokasi']} | 👤 **PIC:** {row['PIC']}\n\n"
                            f"⛽ **Jenis Minyak:** `{row['Jenis Minyak']}`")
                    active_count += 1
        if active_count == 0:
            st.write("Tiada pergerakan aktif dikesan untuk hari ini.")

    with col2:
        st.markdown("### ⚠️ Peringatan Pengisian Minyak Syarikat")
        st.warning("Sila pastikan pemandu mengisi jenis bahan bakar yang betul mengikut spesifikasi kenderaan:")

        diesel_cars = df[df["Jenis Minyak"] == "DIESEL"][["Kenderaan", "No. Pendaftaran"]].drop_duplicates()
        petrol_cars = df[df["Jenis Minyak"] == "PETROL"][["Kenderaan", "No. Pendaftaran"]].drop_duplicates()

        tab1, tab2 = st.tabs(["⛽ Senarai Kenderaan DIESEL", "⛽ Senarai Kenderaan PETROL"])
        with tab1:
            st.table(diesel_cars)
        with tab2:
            st.table(petrol_cars)