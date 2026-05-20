import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="ChemIndicator",
    page_icon="🧪",
    layout="centered"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stButton>button {
    background-color: #38bdf8;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stSelectbox label {
    color: white !important;
}

.box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
data = {

    "HCl": {
        "sifat": "Asam",
        "pH": 1,
        "warna": "Tidak berwarna",
        "indikator": "Fenolftalein"
    },

    "CH3COOH": {
        "sifat": "Asam",
        "pH": 3,
        "warna": "Tidak berwarna",
        "indikator": "Fenolftalein"
    },

    "NaOH": {
        "sifat": "Basa",
        "pH": 13,
        "warna": "Pink",
        "indikator": "Fenolftalein"
    },

    "NH4OH": {
        "sifat": "Basa",
        "pH": 11,
        "warna": "Pink",
        "indikator": "Fenolftalein"
    }

}

# =========================
# TITLE
# =========================
st.title("🧪 ChemIndicator")

st.write("""
Website simulasi indikator asam basa 
untuk membantu memahami perubahan warna indikator.
""")

# =========================
# PILIH LARUTAN
# =========================
larutan = st.selectbox(
    "Pilih Larutan",
    list(data.keys())
)

# =========================
# BUTTON
# =========================
if st.button("Cek Hasil"):

    hasil = data[larutan]

    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.subheader("📋 Hasil Simulasi")

    st.write(f"### Larutan : {larutan}")
    st.write(f"### Sifat : {hasil['sifat']}")
    st.write(f"### pH : {hasil['pH']}")
    st.write(f"### Indikator : {hasil['indikator']}")
    st.write(f"### Warna : {hasil['warna']}")

    # status warna
    if hasil["sifat"] == "Asam":

        st.error("🔴 Larutan Bersifat Asam")

    else:

        st.success("🔵 Larutan Bersifat Basa")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TEORI
# =========================
st.markdown("---")

st.header("📚 Teori Singkat")

st.write("""
- Asam memiliki pH kurang dari 7
- Basa memiliki pH lebih dari 7
- Indikator digunakan untuk mengetahui sifat larutan
- Fenolftalein berwarna pink dalam basa
""")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.caption("ChemIndicator © 2026")
