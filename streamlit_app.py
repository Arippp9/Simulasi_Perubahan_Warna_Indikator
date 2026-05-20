import streamlit as st
import math

# ==========================================
# 1. KONFIGURASI HALAMAN & ENERGI ESTETIKA (NEON PURPLE)
# ==========================================
st.set_page_config(
    page_title="ChemClass Lab - Streamlit Edition",
    page_icon="🧪",
    layout="wide",
)

# Kustomisasi CSS untuk ambient ungu neon modern yang futuristik dan konsisten
st.markdown("""
<style>
    /* Mengubah latar belakang utama aplikasi Streamlit */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #16072b 0%, #070112 100%) !important;
        background-attachment: fixed;
    }
    
    /* Gelas Beaker area dengan bingkai ungu neon bersinar */
    .beaker-container {
        border: 2px solid rgba(168, 85, 247, 0.5);
        border-radius: 16px;
        padding: 30px;
        background: rgba(14, 2, 28, 0.85);
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.25), inset 0 0 15px rgba(168, 85, 247, 0.1);
        backdrop-filter: blur(8px);
    }
    
    /* HUD Panel info zat dengan border kiri neon ungu menyala */
    .chemical-hud {
        background-color: rgba(22, 10, 40, 0.9);
        border-left: 5px solid #a855f7;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.15);
        padding: 18px;
        border-radius: 10px;
        margin: 12px 0;
        border-top: 1px solid rgba(168, 85, 247, 0.15);
        border-right: 1px solid rgba(168, 85, 247, 0.15);
        border-bottom: 1px solid rgba(168, 85, 247, 0.15);
    }
    
    /* Penyelarasan warna teks agar ramah estetika gelap */
    h1, h2, h3, h4, h5, p, span, li, b {
        color: #f3e8ff !important;
    }

    code {
        background-color: #0b0214 !important;
        color: #d8b4fe !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
    }
    
    /* Label teks komponen input */
    .stSelectbox label, .stSlider label {
        font-family: monospace;
        font-weight: bold;
        color: #d8b4fe !important;
        letter-spacing: 0.05em;
    }
    
    /* Kustomisasi Box Input dropdown agar menyatu dengan tema */
    div[data-baseweb="select"] {
        background-color: #0a0314 !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATASET KIMIA (PRESETS ZAT & INDIKATOR)
# ==========================================
CHEMICALS = [
    {"id": "hcl", "name": "Asam Klorida (HCl)", "formula": "HCl", "pH": 1.0, "type": "asam", "category": "Laboratorium", "common": "Asam kuat pembersih porselen", "dissociation": "HCl → H⁺ + Cl⁻"},
    {"id": "h2so4", "name": "Asam Sulfat (Air Aki)", "formula": "H₂SO₄", "pH": 1.5, "type": "asam", "category": "Laboratorium", "common": "Air aki kendaraan pekat", "dissociation": "H₂SO₄ → 2H⁺ + SO₄²⁻"},
    {"id": "vinegar", "name": "Asam Asetat (Cuka Makan)", "formula": "CH₃COOH", "pH": 3.0, "type": "asam", "category": "Sehari-hari", "common": "Cuka dapur encer", "dissociation": "CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
    {"id": "lemon", "name": "Asam Sitrat (Sari Lemon)", "formula": "C₆H₈O₇", "pH": 2.2, "type": "asam", "category": "Sehari-hari", "common": "Air perasan jeruk segar", "dissociation": "C₆H₈O₇ ⇌ H⁺ + C₆H₇O₇⁻"},
    {"id": "water", "name": "Air Murni (H₂O)", "formula": "H₂O", "pH": 7.0, "type": "netral", "category": "Sehari-hari", "common": "Air suling / Aquades netral", "dissociation": "H₂O ⇌ H⁺ + OH⁻"},
    {"id": "baking_soda", "name": "Soda Kue (NaHCO₃)", "formula": "NaHCO₃", "pH": 8.5, "type": "basa", "category": "Sehari-hari", "common": "Bahan pengembang roti rumahan", "dissociation": "NaHCO₃ → Na⁺ + HCO₃⁻"},
    {"id": "limewater", "name": "Kalsium Hidroksida (Air Kapur)", "formula": "Ca(OH)₂", "pH": 11.5, "type": "basa", "category": "Laboratorium", "common": "Air kapur sirih jernih", "dissociation": "Ca(OH)₂ → Ca²⁺ + 2OH⁻"},
    {"id": "naoh", "name": "Natrium Hidroksida (Sodapi)", "formula": "NaOH", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Sodapi pekat penghancur sumbatan", "dissociation": "NaOH → Na⁺ + OH⁻"}
]

INDICATORS = {
    "lakmus": {
        "name": "Kertas Lakmus (Litmus)",
        "range": (4.5, 8.3),
        "low_color": "#ef4444", "low_label": "MERAH ASAM",
        "high_color": "#3b82f6", "high_label": "BIRU BASA",
        "mid_color": "#a855f7", "mid_label": "UNGU REAKSI"
    },
    "pp": {
        "name": "Phenolphthalein (PP)",
        "range": (8.2, 10.0),
        "low_color": "#f8fafc", "low_label": "TIDAK BERWARNA",
        "high_color": "#ec4899", "high_label": "MERAH MUDA PEKAT",
        "mid_color": "#fbcfe8", "mid_label": "MERAH MUDA SEMU"
    },
    "btb": {
        "name": "Bromothymol Blue (BTB)",
        "range": (6.0, 7.6),
        "low_color": "#eab308", "low_label": "KUNING ASAM",
        "high_color": "#1d4ed8", "high_label": "BIRU BASA",
        "mid_color": "#22c55e", "mid_label": "HIJAU NETRAL"
    },
    "mr": {
        "name": "Metil Merah (Methyl Red)",
        "range": (4.4, 6.2),
        "low_color": "#ef4444", "low_label": "MERAH ASAM",
        "high_color": "#eab308", "high_label": "KUNING BASA",
        "mid_color": "#f97316", "mid_label": "JINGGA TRANSISI"
    },
    "universal": {
        "name": "Indikator Universal",
        "range": (0.0, 14.0),
        "low_color": "#dc2626", "low_label": "MERAH (pH KOROSIF)",
        "high_color": "#581c87", "high_label": "UNGU (pH BASA KUAT)",
        "mid_color": "#16a34a", "mid_label": "HIJAU (pH NETRAL)"
    }
}

# ==========================================
# 3. HEADER UTAMA
# ==========================================
st.title("🧪 ChemClass Lab - Python Edition")
st.write("Belajar sains asam-basa dan koding Python pemula sekaligus dalam satu platform terpadu.")

menu = st.tabs(["📊 LAB SIMULATOR"])

# ==========================================
# HELPER: FUNGSI PENENTU WARNA CAIRAN
# ==========================================
def hitung_warna_indikator(ph, ind_data):
    low, high = ind_data["range"]
    if ind_data["name"] == "Indikator Universal":
        if ph < 3: return "#dc2626"  # Merah asam kuat
        elif ph < 5: return "#f97316"  # Oranye
        elif ph < 6.5: return "#eab308"  # Kuning
        elif ph < 7.5: return "#16a34a"  # Hijau netral
        elif ph < 9: return "#0284c7"  # Biru muda
        elif ph < 11: return "#1d4ed8"  # Biru tua
        else: return "#581c87"  # Ungu basa kuat
    
    if ph < low:
        return ind_data["low_color"]
    elif ph > high:
        return ind_data["high_color"]
    else:
        return ind_data["mid_color"]

# ==========================================
# TAB 1: LAB SIMULATOR
# ==========================================
with menu[0]:
    col_input, col_display = st.columns([5, 7])
    
    with col_input:
        st.subheader("💡 Parameter Simulasi")
        
        # Pilihan Preset Senyawa
        preset_names = [chem["name"] for chem in CHEMICALS]
        pilihan_preset = st.selectbox("Pilih Preset Zat Kimia:", preset_names, index=2) # Default cuka
        selected_chem = next(chem for chem in CHEMICALS if chem["name"] == pilihan_preset)
        
        # Pilihan Indikator
        pilihan_ind = st.selectbox(
            "Pilihan Kertas Indikator:",
            options=list(INDICATORS.keys()),
            format_func=lambda x: INDICATORS[x]["name"]
        )
        selected_ind_data = INDICATORS[pilihan_ind]
        
        # Slider pH Manual
        st.write("---")
        st.markdown("**Kontrol pH Manual (Dial):** Modifikasi nilai derajat keasaman secara langsung")
        simulated_ph = st.slider("Mengatur pH:", min_value=0.0, max_value=14.0, value=selected_chem["pH"], step=0.1)

    with col_display:
        st.subheader("🔮 Simulator Beaker Reaktif")
        
        # Ambil warna secara dinamis berdasarkan pH slider
        liquid_color = hitung_warna_indikator(simulated_ph, selected_ind_data)
        
        # Visualisasi Gelas Beaker khas dengan border bersinar ungu neon
        container_html = f"""
        <div class="beaker-container">
            <span style="font-size: 11px; font-weight: bold; color: #d8b4fe; display: block; margin-bottom: 15px; letter-spacing: 0.1em; font-family: monospace;">LABORATORIUM METRIK UNGU</span>
            <div style="
                width: 140px; 
                height: 160px; 
                border: 4px solid rgba(168, 85, 247, 0.4); 
                border-top: none;
                border-radius: 0 0 16px 16px; 
                margin: 0 auto; 
                position: relative;
                box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
            ">
                <!-- Cairan Kimia Reaktif -->
                <div style="
                    position: absolute; 
                    bottom: 8px; 
                    left: 6px; 
                    right: 6px; 
                    height: {int(simulated_ph * 4.5) + 50}px; 
                    background-color: {liquid_color}; 
                    border-radius: 0 0 10px 10px;
                    transition: background-color 0.4s ease, height 0.4s ease;
                    box-shadow: inset 0 4px 8px rgba(255,255,255,0.15);
                "></div>
                <!-- Garis Skala Pengukur -->
                <div style="position: absolute; left: 10px; top: 30px; border-left: 2px solid rgba(168, 85, 247, 0.3); height: 100px; display: flex; flex-direction: column; justify-content: space-between; text-align: left; padding-left: 5px; font-size: 8px; font-family: monospace; color: #d8b4fe;">
                    <span>-- 150ml</span>
                    <span>-- 100ml</span>
                    <span>-- 50ml</span>
                </div>
            </div>
            <div style="margin-top: 20px; font-weight: bold; font-size: 20px; color: #f3e8ff; text-shadow: 0 0 8px {liquid_color};">
                Nilai pH Cairan: <span style="color: {liquid_color};">{simulated_ph:.1f}</span>
            </div>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        # HUD Panel Informasi senyawa pilihan dengan aksen senada
        st.markdown(f"""
        <div class="chemical-hud">
            <h4 style="margin-top:0px; color: #e9d5ff !important; font-family: monospace;">📋 INFORMASI SENYAWA</h4>
            <b>Nama Senyawa:</b> {selected_chem['name']} ({selected_chem['formula']})<br/>
            <b>Nama Populer:</b> {selected_chem['common']}<br/>
            <b>Ionisasi Disosiasi:</b> <code>{selected_chem['dissociation']}</code><br/>
            <b>Kategori Kelas:</b> {selected_chem['category']}
        </div>
        """, unsafe_allow_html=True)
