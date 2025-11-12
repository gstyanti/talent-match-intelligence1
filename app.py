# ==========================================================
# 💼 AI Talent Match Dashboard - Final Version
# ==========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from openai import OpenAI


# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Talent Match Dashboard", layout="wide")

st.title("💼 AI Talent Match Dashboard")

# --- LOAD DATA (Fallback mode) ---
@st.cache_data
def load_data():
    try:
        with zipfile.ZipFile("match_results.zip", "r") as z:
            with z.open("match_results.csv") as f:
                df = pd.read_csv(f)
        return df
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# --- SIDEBAR FILTER ---
st.sidebar.header("🧭 Dashboard Control")
role = st.sidebar.selectbox("Pilih Department", sorted(df["name_department"].unique()))
level = st.sidebar.selectbox("Pilih Job Title", sorted(df["name_position"].unique()))

filtered = df[(df["name_department"] == role) & (df["name_position"] == level)]

st.write(f"Menampilkan hasil analisis untuk **{role}** — **{level}**")

# --- VISUALISASI DISTRIBUSI ---
st.subheader("📊 Distribusi Final Match Rate")
fig, ax = plt.subplots(figsize=(6, 3))
sns.histplot(filtered["final_match_rate"], bins=10, kde=True, ax=ax, color="skyblue")
plt.title("Distribusi Final Match Rate")
st.pyplot(fig)

# --- TOP KANDIDAT ---
st.subheader("🏅 Top 10 Kandidat Berdasarkan Match Rate")
top_candidates = filtered.nlargest(10, "final_match_rate")[["employee_id", "fullname", "final_match_rate", "match_category"]]
st.dataframe(top_candidates)



# --- CATATAN ---
st.caption("📄 Mode offline: data diambil dari match_results.csv")

st.markdown("---")
st.caption("Built by [Gusti Ayu Putu Febriyanti] — Rakamin Case Study 2025")



