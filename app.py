# aplikasi.py — ISI PERUT
# Instrumen Skrining dan Informasi Penyakit Saluran Cerna Untukmu
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang

import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO

# ==== Optional PDF dependency (graceful) ====
HAS_RL = True
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib import colors
except Exception:
    HAS_RL = False

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="ISI PERUT – Instrumen Skrining dan Informasi Penyakit Saluran Cerna",
    page_icon="🩺",
    layout="wide",
)

# ------------------ HELPER ------------------
def pick_first_existing(paths):
    for p in paths:
        if Path(p).exists():
            return p
    return None

# ------------------ ASSET PATHS ------------------
logo_kariadi = pick_first_existing(["logo_kariadi.png"])
logo_isi      = pick_first_existing(["logo_isi_perut.png"])
egd_img       = pick_first_existing(["ilustrasi_egd.png"])
colo_img      = pick_first_existing(["ilustrasi_kolonoskopi.png"])

# ------------------ CSS ------------------
CUSTOM_CSS = """
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}
.block-container { padding-top: 60px; padding-bottom: 2rem; }

h1, h2, h3 { color:#007C80; }
h1 { font-weight:800; }
h2, h3 { font-weight:700; }

/* (header-logos lama, sekarang tidak dipakai langsung)
.header-logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin-top: 20px;
  margin-bottom: 10px;
}
.header-logos img {
  max-height: 100px;
  height: auto;
}
*/

/* ====== Deskripsi ISI PERUT ====== */
.desc {
  text-align: center;
  font-size: 1.05rem;
  color: #333;
  margin: 0 auto 1.2rem auto;
  max-width: 980px;
}

/* ====== Ilustrasi ====== */
.illustrations {
  display: flex;
  justify-content: center;
  align-items: start;
  gap: 60px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.illustration { text-align: center; }
.illustration img {
  max-width: 340px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,.08);
}
.illustration-cap { color: #5b7580; font-size: .9rem; margin-top: .5rem; }

/* ====== Kartu hasil ====== */
.result-card {
  border: 2px solid #00B3AD22;
  border-radius: 14px;
  padding: 1rem 1.2rem;
  background: #ffffffcc;
  box-shadow: 0 6px 18px rgba(0,0,0,.06);
  margin-bottom: 1rem;
}
.badge { display:inline-block; padding:.35rem .65rem; border-radius:999px; font-weight:700; }
.badge-red  { background:#ffebee; color:#c62828; border:1px solid #ffcdd2; }
.badge-green{ background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9; }
.badge-gray { background:#eceff1; color:#37474f; border:1px solid #cfd8dc; }

.streamlit-expanderHeader {
  background:#f0fdfa; color:#007C80; font-weight:700; border:1px solid #b2dfdb; border-radius:10px;
}

/* ====== Responsif ====== */
@media (max-width: 768px){
  .illustrations { flex-direction: column; align-items: center; gap: 30px; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ HEADER (2 logo sejajar) ------------------
with st.container():
    pad_left, col_logo1, col_logo2, pad_right = st.columns([0.3, 1, 1, 0.3])

    with col_logo1:
        if logo_kariadi:
            # atur lebar logo RS di sini
            st.image(logo_kariadi, width=220)

    with col_logo2:
        if logo_isi:
            # atur lebar logo ISI PERUT di sini
            st.image(logo_isi, width=220)

    st.markdown(
        """
        <p class='desc'>
        <b>ISI PERUT</b> (<i>Instrumen Skrining dan Informasi Penyakit Saluran Cerna</i>)
        adalah aplikasi yang membantu Anda mengetahui informasi tentang teropong saluran cerna,
        baik atas maupun bawah. Aplikasi ini juga membantu Anda melakukan skrining mandiri
        untuk mengetahui apakah tindakan teropong saluran cerna diperlukan atau tidak,
        berdasarkan keluhan saluran cerna Anda.
        </p>
        """,
        unsafe_allow_html=True,
    )

# ------------------ ILUSTRASI ------------------
st.markdown("<div class='illustrations'>", unsafe_allow_html=True)
if egd_img:
    st.markdown("<div class='illustration'>", unsafe_allow_html=True)
    st.image(egd_img)
    st.markdown("<div class='illustration-cap'>Skema endoskopi saluran cerna atas (EGD)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
if colo_img:
    st.markdown("<div class='illustration'>", unsafe_allow_html=True)
    st.image(colo_img)
    st.markdown("<div class='illustration-cap'>Skema endoskopi saluran cerna bawah (Kolonoskopi)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------ DESKRIPSI SKRINING ------------------
st.markdown(
    """
    <h1 style='text-align:center;'>Apakah Saya Perlu Teropong Saluran Cerna?</h1>
    <p style='text-align:center; font-size:1.05rem; color:#333;'>
      Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan teropong
      saluran cerna atas (<i>esophagogastroduodenoscopy</i>/EGD) maupun saluran cerna bawah
      (<i>kolonoskopi</i>). Berdasarkan panduan klinis; hasil bersifat edukasi dan tidak
      menggantikan diagnosis medis.
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------ DATA DASAR ------------------
with st.expander("🧑‍⚕️ Data dasar (opsional)", expanded=False):
    name = st.text_input("Nama")
    age  = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    sex  = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

# ------------------ PERTANYAAN ------------------
ALARM_EGD = [
    "Saya **muntah darah** (hematemesis)",
    "BAB saya **hitam pekat seperti aspal** (melena)",
    "Saya makin **sulit menelan** (disfagia progresif)",
    "Saya **nyeri saat menelan** (odynofagia)",
    "Berat badan saya **turun banyak tanpa sebab jelas**",
    "Saya diberi tahu darah saya **kurang (anemia)** atau tampak pucat/lemas",
    "Saya **sering muntah berulang atau tidak bisa makan/minum**",
    "Perut bagian atas terasa **penuh / cepat kenyang / tersumbat** (curiga sumbatan lambung)",
]
RISK_EGD = [
    "Saya **baru mengalami keluhan lambung** setelah **usia ≥50 tahun**",
    "Ada **keluarga dekat** pernah terkena **kanker lambung**",
]
OTHER_EGD = [
    "Keluhan perut atas/nyeri ulu hati/panas di dada **>4–6 minggu** dan belum membaik",
    "**Nyeri ulu hati** tetap ada meski sudah minum PPI **4–8 minggu**",
    "Sering **asam/panas naik ke tenggorokan (refluks/GERD)** dan **tidak membaik** dengan obat",
    "Riwayat **tukak/ulkus** lambung atau duodenum dan keluhan berlanjut",
    "Riwayat **infeksi H. pylori** dan masih ada keluhan setelah pengobatan",
    "Sering memakai **NSAID/pengencer darah** disertai keluhan perut",
    "Dugaan **perdarahan samar** (tes darah feses positif) tanpa penyebab jelas",
    "Kontrol endoskopi pasca terapi (ulkus/varises/polipektomi) sesuai anjuran dokter",
]

with st.expander("Apakah Saya perlu teropong saluran cerna **atas (EGD)** ?", expanded=False):
    e1, e2, e3 = st.columns(3)
    egd_alarm_sel, egd_risk_sel, egd_other_sel = [], [], []
    with e1:
        st.subheader("🚨 Tanda Bahaya")
        for i, q in enumerate(ALARM_EGD):
            if st.checkbox(q, key=f"egd_alarm_{i}"): egd_alarm_sel.append(q)
    with e2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_EGD):
            if st.checkbox(q, key=f"egd_risk_{i}"): egd_risk_sel.append(q)
    with e3:
        st.subheader("🩹 Indikasi Elektif")
        for i, q in enumerate(OTHER_EGD):
            if st.checkbox(q, key=f"egd_other_{i}"): egd_other_sel.append(q)

ALARM_COLO = [
    "Saya **keluar darah segar dari dubur** sedang–berat / **menetes**",
    "Saya **anemia defisiensi besi** atau tampak pucat/lemas",
    "Berat badan saya **turun tanpa sebab jelas**",
    "Terjadi **perubahan pola BAB progresif** (>4–6 minggu) disertai darah",
    "Nyeri perut berat menetap, **diare berdarah/demam** (curiga kolitis/IBD berat)",
]
RISK_COLO = [
    "Usia **≥50 tahun** dengan keluhan saluran cerna bawah",
    "Ada **keluarga dekat** dengan **kanker kolorektal/polip adenoma**",
    "**FIT/FOBT positif**",
    "Riwayat **IBD** (kolitis ulseratif/Crohn) — evaluasi/monitoring",
    "Riwayat **polip/operasi CRC** — perlu **surveilans** berkala",
]
OTHER_COLO = [
    "**Perubahan kebiasaan BAB** >4–6 minggu tanpa tanda bahaya",
    "**Konstipasi kronik** tidak membaik dengan pengobatan awal",
    "**Diare kronik** >4 minggu",
    "Nyeri perut bawah berulang disertai perubahan BAB",
    "Keluar **lendir/darah sedikit** berulang dari anus",
    "Skrining polip/CRC **elektif** sesuai usia/risiko",
]

with st.expander("Apakah Saya perlu teropong saluran cerna **bawah (Kolonoskopi)** ?", expanded=False):
    c1, c2, c3 = st.columns(3)
    colo_alarm_sel, colo_risk_sel, colo_other_sel = [], [], []
    with c1:
        st.subheader("🚨 Tanda Bahaya")
        for i, q in enumerate(ALARM_COLO):
            if st.checkbox(q, key=f"colo_alarm_{i}"): colo_alarm_sel.append(q)
    with c2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_COLO):
            if st.checkbox(q, key=f"colo_risk_{i}"): colo_risk_sel.append(q)
    with c3:
        st.subheader("🩹 Indikasi Elektif")
        for i, q in enumerate(OTHER_COLO):
            if st.checkbox(q, key=f"colo_other_{i}"): colo_other_sel.append(q)

# ------------------ HASIL SKRINING ------------------
def verdict(alarm, risk, other, organ):
    if alarm:
        return f"🔴 Anda **perlu {organ} segera**", "badge badge-red", "Segera konsultasi ke dokter penyakit dalam."
    elif risk or other:
        return f"🟢 Anda **dapat menjadwalkan {organ} (elektif)**", "badge badge-green", "Buat janji di poliklinik untuk pemeriksaan lebih lanjut."
    else:
        return f"⚪ Saat ini **belum tampak kebutuhan mendesak untuk {organ}**", "badge badge-gray", (
            "Lanjutkan pemantauan dan pengobatan rutin. Bila keluhan menetap >4–6 minggu atau muncul tanda bahaya, segera konsultasi ke dokter."
        )

v_egd,  b_egd,  a_egd  = verdict(egd_alarm_sel,  egd_risk_sel,  egd_other_sel,  "endoskopi saluran cerna atas (EGD)")
v_colo, b_colo, a_colo = verdict(colo_alarm_sel, colo_risk_sel, colo_other_sel, "kolonoskopi (saluran cerna bawah)")

st.subheader("📋 Hasil Skrining")
colA, colB = st.columns(2)
with colA:
    st.markdown(f'<div class="result-card"><span class="{b_egd}">{v_egd}</span><br/>{a_egd}</div>', unsafe_allow_html=True)
with colB:
    st.markdown(f'<div class="result-card"><span class="{b_colo}">{v_colo}</span><br/>{a_colo}</div>', unsafe_allow_html=True)

# ------------------ PDF EXPORT (kop surat RS Kariadi) ------------------
def build_pdf_letterhead(
    name: str, age: int, sex: str, today: str,
    v_egd: str, a_egd: str, r_egd: list,
    v_colo: str, a_colo: str, r_colo: list,
    logo_rs_path: str | None, logo_isi_path: str | None
) -> bytes:
    """Bangun PDF hasil skrining dengan kop RS Kariadi dan dua kesimpulan (EGD & Kolonoskopi)."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=32, rightMargin=32, topMargin=30, bottomMargin=28)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1C", parent=styles["Title"], alignment=1, leading=22, spaceAfter=12))
    styles.add(ParagraphStyle(name="SmallGray", parent=styles["Normal"], textColor=colors.HexColor("#444"), fontSize=10))
    styles.add(ParagraphStyle(name="Label", parent=styles["Normal"], spaceAfter=2))
    styles.add(ParagraphStyle(name="Bold", parent=styles["Normal"], fontName=styles["Heading4"].fontName, spaceAfter=4))

    elems = []

    # Header: dua logo (RS & ISI PERUT)
    left_img = Image(logo_rs_path, width=120, height=54) if logo_rs_path and Path(logo_rs_path).exists() else ""
    right_img = Image(logo_isi_path, width=95, height=95) if logo_isi_path and Path(logo_isi_path).exists() else ""
    header_tbl = Table(
        [[left_img, Paragraph(
            "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
            "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
            "Telepon: (024) 8413993, 8413476, 8413764 &nbsp;&nbsp; "
            "<font color='#2e7d32'><b>Fax:</b> (024) 8318617</font><br/>"
            "Website: http://www.rskariadi.co.id", styles["Normal"]
        ), right_img]],
        colWidths=[130, 330, 95],
        hAlign="LEFT"
    )
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elems.append(header_tbl)
    elems += [Spacer(1,6), Table([[""]], colWidths=[555],
                                 style=[("LINEBELOW",(0,0),(0,0),1,colors.HexColor("#9dd8d3"))]), Spacer(1,8)]

    # Judul
    elems.append(Paragraph("HASIL SKRINING ENDOSKOPI SALURAN CERNA", styles["H1C"]))
    elems.append(Paragraph("(EGD & Kolonoskopi)", styles["SmallGray"]))
    elems.append(Spacer(1,6))

    # Identitas
    ident = [
        Paragraph(f"<b>Tanggal:</b> {today}", styles["Label"]),
        Paragraph(f"<b>Nama:</b> {name if name else '-'}", styles["Label"]),
        Paragraph(f"<b>Usia:</b> {age} tahun", styles["Label"]),
        Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Label"]),
    ]
    elems.extend(ident)
    elems.append(Spacer(1,10))

    # Seksi EGD
    elems.append(Paragraph("<b>1) Saluran Cerna Atas (EGD)</b>", styles["Bold"]))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_egd}", styles["Label"]))
    elems.append(Paragraph(a_egd, styles["Label"]))
    if r_egd:
        elems.append(Spacer(1,2))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Label"]))
        for r in r_egd:
            elems.append(Paragraph(f"• {r}", styles["Label"]))
    elems.append(Spacer(1,8))

    # Seksi Kolonoskopi
    elems.append(Paragraph("<b>2) Saluran Cerna Bawah (Kolonoskopi)</b>", styles["Bold"]))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_colo}", styles["Label"]))
    elems.append(Paragraph(a_colo, styles["Label"]))
    if r_colo:
        elems.append(Spacer(1,2))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Label"]))
        for r in r_colo:
            elems.append(Paragraph(f"• {r}", styles["Label"]))
    elems.append(Spacer(1,12))

    # Catatan
    elems.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        styles["SmallGray"]
    ))

    doc.build(elems)
    return buf.getvalue()

# Kumpulkan alasan yang dipilih untuk dicetak di PDF
r_egd_all  = (egd_alarm_sel if 'egd_alarm_sel' in locals() else []) + \
             (egd_risk_sel  if 'egd_risk_sel'  in locals() else []) + \
             (egd_other_sel if 'egd_other_sel' in locals() else [])
r_colo_all = (colo_alarm_sel if 'colo_alarm_sel' in locals() else []) + \
             (colo_risk_sel  if 'colo_risk_sel'  in locals() else []) + \
             (colo_other_sel if 'colo_other_sel' in locals() else [])

st.markdown("")

if HAS_RL:
    pdf_bytes = build_pdf_letterhead(
        name or "", int(age), sex, today,
        v_egd, a_egd, r_egd_all,
        v_colo, a_colo, r_colo_all,
        logo_kariadi, logo_isi
    )
    st.download_button(
        "⬇️ Unduh Surat Hasil (PDF)",
        data=pdf_bytes,
        file_name=f"Hasil_Skrining_ISI_PERUT_{today.replace(' ','_')}.pdf",
        mime="application/pdf"
    )
else:
    st.info(
        "Fitur unduh PDF membutuhkan paket **reportlab**.\n\n"
        "Tambahkan file `requirements.txt` dengan isi:\n"
        "`streamlit>=1.37` dan `reportlab>=3.6.12`, lalu deploy ulang.",
        icon="ℹ️"
    )

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
