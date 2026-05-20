import streamlit as st
import math

# ==========================================
# 1. KONFIGURASI HALAMAN & ENERGI ESTETIKA
# ==========================================
st.set_page_config(
    page_title="ChemClass Lab - Streamlit Edition",
    page_icon="🧪",
    layout="wide"
)

# Kustomisasi CSS untuk ambient gelap modern dan sentuhan UI yang halus
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .beaker-container {
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        background-color: #08080a;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .chemical-hud {
        background-color: #111217;
        border-left: 4px solid #4f46e5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .terminal-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #000000;
        color: #10b981;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #1e293b;
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
# 3. HEADER & MENU NAVIGASI UTAMA
# ==========================================
st.title("🧪 ChemClass Lab - Python Edition")
st.write("Belajar sains asam-basa dan koding Python pemula sekaligus dalam satu platform terpadu.")

menu = st.tabs(["📊 LAB SIMULATOR", "🐍 KODING PYTHON", "📝 KUIS INTERAKTIF", "📚 RINGKASAN TEORI"])

# ==========================================
# HELPER: FUNGSI PENENTU WARNA CAIRAN
# ==========================================
def hitung_warna_indikator(ph, ind_data):
    low, high = ind_data["range"]
    if ind_data["name"] == "Indikator Universal":
        # Spectrum interpolasi manual sederhana untuk kelas universal
        if ph < 3: return "#dc2626"  # Red
        elif ph < 5: return "#f97316"  # Orange
        elif ph < 6.5: return "#eab308"  # Yellow
        elif ph < 7.5: return "#16a34a"  # Green
        elif ph < 9: return "#0284c7"  # Light blue
        elif ph < 11: return "#1d4ed8"  # Dark blue
        else: return "#581c87"  # Purple
    
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
        pilihan_preset = st.selectbox("Pilih Preset Zat Kimia:", preset_names, index=2) # default cuka
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
        
        # Visualisasi Gelas Beaker menggunakan Formatted HTML
        container_html = f"""
        <div class="beaker-container">
            <span style="font-size: 11px; font-weight: bold; color: #94a3b8; display: block; margin-bottom: 15px;">BEAKER LAB METRIK</span>
            <div style="
                width: 140px; 
                height: 160px; 
                border: 4px solid rgba(255, 255, 255, 0.4); 
                border-top: none;
                border-radius: 0 0 16px 16px; 
                margin: 0 auto; 
                position: relative;
                box-shadow: inset 0 -10px 20px rgba(255,255,255,0.05);
            ">
                <!-- Cairan Kimia Reaktif -->
                <div style="
                    position: absolute; 
                    bottom: 8px; 
                    left: 6px; 
                    right: 6px; 
                    height: {int(simulated_ph * 4) + 60}px; 
                    background-color: {liquid_color}; 
                    border-radius: 0 0 10px 10px;
                    transition: background-color 0.5s ease, height 0.5s ease;
                "></div>
                <!-- Garis Skala Pengukur -->
                <div style="position: absolute; left: 10px; top: 30px; border-left: 2px solid rgba(255,255,255,0.2); height: 100px; display: flex; flex-direction: column; justify-content: space-between; text-align: left; padding-left: 5px; font-size: 8px; color: rgba(255,255,255,0.4);">
                    <span>--- 150ml</span>
                    <span>--- 100ml</span>
                    <span>--- 50ml</span>
                </div>
            </div>
            <div style="margin-top: 20px; font-weight: bold; font-size: 18px; color: {liquid_color};">
                Nilai pH Cairan: {simulated_ph:.1f}
            </div>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        # HUD Panel Informasi senyawa terpilih
        st.markdown(f"""
        <div class="chemical-hud">
            <h4>📋 Informasi Senyawa Terpilih</h4>
            <b>Nama Senyawa:</b> {selected_chem['name']} ({selected_chem['formula']})<br/>
            <b>Nama Populer:</b> {selected_chem['common']}<br/>
            <b>Reaksi Ionisasi Disosiasi:</b> <code>{selected_chem['dissociation']}</code><br/>
            <b>Kategori Kelas:</b> {selected_chem['category']}
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: KODING PYTHON
# ==========================================
with menu[1]:
    st.subheader("🐍 Belajar Menghitung dengan Python Bawaan")
    st.write("Ubah parameter di sebelah kiri, lihat bagaimana kode program Python yang dinamis di bawah memperbarui variabelnya secara instan!")
    
    col_code, col_run = st.columns([5, 5])
    
    with col_code:
        # Menghitung molaritas bayangan untuk demonstrasi koding
        valency_val = 1
        molarity_val = 10**(-simulated_ph) if simulated_ph <= 7 else 10**(-(14-simulated_ph))
        
        python_code_str = f"""# hitung_ph.py - Program Menghitung pH Sederhana
import math

# --- INPUT DATA ---
nama_zat = "{selected_chem['name'].split('(')[0].strip()}"
molaritas = {molarity_val:.5f}  # Konsentrasi molar (M)
valensi = {valency_val}          # Jumlah pengantar ion asam/basa

# --- ALUR LOGIKA PENENTU ---
if {simulated_ph:.1f} <= 7.0:
    konsentrasi_ion = molaritas * valensi
    nilai_ph = -math.log10(konsentrasi_ion)
    sifat = "ASAM"
else:
    konsentrasi_ion = molaritas * valensi
    p_oh = -math.log10(konsentrasi_ion)
    nilai_ph = 14 - p_oh
    sifat = "BASA"

# --- OUTPUT HASIL ---
print("====== KONSOL LOG KELUARAN ======")
print(f"Nama Zat Cair : {{nama_zat}}")
print(f"Hasil Akhir  : pH {{nilai_ph:.1f}}")
print(f"Sifat Larutan : {{sifat}}")
"""
        st.code(python_code_str, language="python")
        
    with col_run:
        btn_run = st.button("RUN / JALANKAN PROGRAM ⏯️")
        st.write("---")
        st.markdown("**🖥️ Output Konsol Komputer:**")
        
        if btn_run:
            sifat_text = "ASAM" if simulated_ph < 7.0 else ("BASA" if simulated_ph > 7.0 else "NETRAL")
            color_text = "#ff4b4b" if sifat_text == "ASAM" else ("#5b8bff" if sifat_text == "BASA" else "#2bcf5c")
            
            # Simulasi output terminal komputer nyata
            st.markdown(f"""
            <div class="terminal-box">
                $ python hitung_ph.py<br/>
                ====== KONSOL LOG KELUARAN ======<br/>
                Nama Zat Cair : {selected_chem['name'].split('(')[0].strip()}<br/>
                Hasil Akhir  : pH <span style="font-weight:bold; color:{color_text};">{simulated_ph:.1f}</span><br/>
                Sifat Larutan : <span style="font-weight:bold; color:{color_text};">{sifat_text}</span><br/>
                =================================<br/>
                <span style="color:#555;">[Program selesai dijalankan dengan sukses]</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Klik tombol di atas untuk mengeksekusi (simulasi compile) kode Python.")

# ==========================================
# TAB 3: KUIS INTERAKTIF
# ==========================================
with menu[2]:
    st.subheader("📝 Latihan Uji Pemahaman Kimiawan")
    st.write("Uji pengetahuan dasar Anda mengenai kekuatan pH larutan sehari-hari.")
    
    # Soal 1
    q1 = st.radio(
        "1. Larutan dapur manakah di bawah ini yang tergolong asam lemah pengubah warna lakmus biru menjadi merah?",
        options=["Sabun Cair", "Asam Asetat (Cuka Makan)", "Detergen Pekat", "Garam Dapur Netral"],
        index=0
    )
    
    # Soal 2
    q2 = st.radio(
        "2. Di laboratorium, jika indikator Phenolphthalein (PP) ditetesi larutan pH 12, warna apakah yang akan teramati?",
        options=["Tidak berwarna", "Biru Langit", "Merah Muda Pekat/Fuchsia", "Kuning Terang"],
        index=0
    )
    
    btn_submit = st.button("Ulas Hasil Penilaian Kuis")
    
    if btn_submit:
        score = 0
        feedback = []
        
        # Pengecekan Soal 1
        if q1 == "Asam Asetat (Cuka Makan)":
            score += 50
            feedback.append("✅ **Soal 1 Benar!** Cuka makan adalah asam organik lemah dengan rentang pH sekitar 3.")
        else:
            feedback.append("❌ **Soal 1 Salah.** Pilihan Anda salah. Asam Asetat (Cuka) adalah asam organik yang mengubah lakmus menjadi merah.")
            
        # Pengecekan Soal 2
        if q2 == "Merah Muda Pekat/Fuchsia":
            score += 50
            feedback.append("✅ **Soal 2 Benar!** Phenolphthalein (PP) berganti warna menjadi fuchsia cerah pada pH basa kuat (di atas 10.0).")
        else:
            feedback.append("❌ **Soal 2 Salah.** Phenolphthalein (PP) akan berubah menjadi fuchsia pekat jika direaksikan dalam media berkuatan basa pekat.")
            
        st.write("---")
        st.write(f"### Hasil Skor Anda: **{score} / 100**")
        for fb in feedback:
            st.write(fb)

# ==========================================
# TAB 4: RINGKASAN TEORI
# ==========================================
with menu[3]:
    st.subheader("📚 Teori Ringkas Reaksi Asam-Basa")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        #### 🧪 Konsep Klasik Svante Arrhenius
        * **Asam:** Zat yang meningkatkan konsentrasi ion hidrogen ($H^+$) dalam media air ($H_2O$).
        * **Basa:** Zat yang meningkatkan konsentrasi ion hidroksida ($OH^-$) dalam media air ($H_2O$).
        
        #### 📖 Rumus Logaritma Sørensen
        Nilai derajat keasaman ($pH$) dirumuskan sebagai negatif logaritma dari konsentrasi ion hidrogen bebas:
        $$pH = -\\log_{10}[H^+]$$
        """)
    with col_t2:
        st.markdown("""
        #### 📏 Karakteristik Pembagi Skala pH
        * **ASAM:** Senyawa dengan nilai pH di kisaran **0 hingga 6**. Larutan kaya ion hidrogen.
        * **NETRAL:** Nilai pH persis melingkar di **7.0** (air murni seimbang).
        * **BASA:** Senyawa dengan nilai pH di kisaran **8 hingga 14**. Larutan kaya ion hidroksida.
        """)
