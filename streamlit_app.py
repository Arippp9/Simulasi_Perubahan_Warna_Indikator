import streamlit as st

# data larutan
data = {
    "HCl": {
        "pH": 1,
        "sifat": "Asam",
        "warna": "Tidak berwarna"
    },

    "NaOH": {
        "pH": 13,
        "sifat": "Basa",
        "warna": "Pink"
    },

    "CH3COOH": {
        "pH": 3,
        "sifat": "Asam",
        "warna": "Tidak berwarna"
    },

    "NH4OH": {
        "pH": 11,
        "sifat": "Basa",
        "warna": "Pink"
    }
}

# title
st.title("🧪 ChemIndicator")
st.write("Simulasi indikator asam basa")

# pilih larutan
larutan = st.selectbox(
    "Pilih Larutan",
    list(data.keys())
)

# tombol cek
if st.button("Cek Hasil"):

    hasil = data[larutan]

    st.subheader("Hasil Simulasi")

    st.write(f"**Larutan :** {larutan}")
    st.write(f"**Sifat :** {hasil['sifat']}")
    st.write(f"**pH :** {hasil['pH']}")
    st.write(f"**Warna indikator :** {hasil['warna']}")

    # warna visual
    if hasil["sifat"] == "Asam":
        st.error("🔴 Larutan Bersifat Asam")

    else:
        st.success("🔵 Larutan Bersifat Basa")
