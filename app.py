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
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Image,
        Table,
        TableStyle,
    )
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
# logo header gabungan
logo_header = pick_first_existing(["logo_header.png", "Logo_Header.png"])

# (opsional) tetap boleh disimpan untuk keperluan PDF, kalau masih dipakai
logo_kariadi = pick_first_existing(["logo_kariadi.png"])
logo_isi = pick_first_existing(["logo_isi_perut.png"])

endo_img = pick_first_existing(["ilustrasi_endoskopi.png", "ilustrasi_endoskopi.jpg"])

# Link e-book
EBOOK_URL = "https://read.bookcreator.com/RNDNIaOmuObU91dWx81iBOosFZP2/f0KVVnM6SNysvTmFOPMOWA"

# ------------------ CSS ------------------
CUSTOM_CSS = """
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}

/* Atur lebar maksimum konten + rata tengah */
.block-container {
  max-width: 1000px;
  padding-top: 40px;
  padding-bottom: 2rem;
  margin-left: auto;
  margin-right: auto;
}

h1, h2, h3 { color:#007C80; }
h1 { font-weight:800; }
h2, h3 { font-weight:700; }

/* ====== Deskripsi ISI PERUT ====== */
.desc {
  text-align: center;
  font-size: 1.1rem;
  color: #333;
  margin: 0 auto 1.4rem auto;
  max-width: 980px;
}

/* ====== Ilustrasi ====== */
.illustrations {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}
.illustration { text-align: center; }
.illustration img {
  max-width: 800px;
  width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,.08);
}
.illustration-cap { color: #5b7580; font-size: .9rem; margin-top: .5rem; }

/* ====== Kartu e-book ====== */
.ebook-card {
  border-radius: 16px;
  background:#ffffffdd;
  box-shadow: 0 4px 16px rgba(0,0,0,.06);
  padding: 1.1rem 1.4rem 1.3rem 1.4rem;
  margin-top: 0.8rem;
  margin-bottom: 0.6rem;
  text-align:center;
  border:1px solid #b2dfdb;
}
.ebook-title {
  font-weight:700;
  color:#00695c;
  margin-bottom:0.3rem;
}
.ebook-btn {
  display:inline-block;
  margin-top:0.6rem;
  padding:0.5rem 1.6rem;
  border-radius:999px;
  background:#00b3ad;
  color:#ffffff !important;
  text-decoration:none;
  font-weight:600;
  font-size:0.95rem;
  box-shadow:0 3px 8px rgba(0,0,0,.12);
}
.ebook-btn:hover {
  background:#009188;
}

/* ====== Kartu hasil ====== */
.result-card {
  border: 2px solid #00B3AD22;
  border-radius: 14px;
  padding: 1rem 1.2rem;
  background: #ffffffcc;
  box-shadow: 0 6px 18px rgba(0,0,0,.06);
  margin-bottom: 1rem;
}
.badge {
  display:inline-block;
  padding:.35rem .65rem;
  border-radius:999px;
  font-weight:700;
}
.badge-red   { background:#ffebee; color:#c62828; border:1px solid #ffcdd2; }
.badge-green { background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9; }
.badge-gray  { background:#eceff1; color:#37474f; border:1px solid #cfd8dc; }

.streamlit-expanderHeader {
  background:#f0fdfa; color:#007C80; font-weight:700; border:1px solid #b2dfdb; border-radius:10px;
}

/* ====== Responsif ====== */
@media (max-width: 768px){
  .illustrations { flex-direction: column; align-items: center; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ HEADER (2 logo sejajar) ------------------
with st.container():
    if logo_header:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.image(logo_header, width=700)  # bisa diubah 600–750 sesuai selera
        st.markdown("</div>", unsafe_allow_html=True)

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
if endo_img:
    st.markdown(
        "<div class='illustrations'><div class='illustration'>",
        unsafe_allow_html=True,
    )
    st.image(endo_img)
    st.markdown(
        "<div class='illustration-cap'>Ilustrasi pemeriksaan endoskopi saluran cerna atas dan bawah</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )

# ------------------ KARTU E-BOOK ------------------
st.markdown(
    f"""
    <div class='ebook-card'>
      <div class='ebook-title'>Ingin tahu lebih jauh tentang pemeriksaan teropong saluran cerna?</div>
      <div style='margin-bottom:0.4rem;'>
        Baca e-book edukasi pasien yang berisi penjelasan langkah pemeriksaan, persiapan sebelum tindakan,
        serta hal-hal penting yang perlu Anda ketahui.
      </div>
      <a href="{EBOOK_URL}" target="_blank" class="ebook-btn">📘 Buka e-book edukasi ISI PERUT</a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ------------------ DESKRIPSI SKRINING ------------------
st.markdown(
    """
    <h1 style='text-align:center;'>Apakah Saya Perlu Teropong Saluran Cerna?</h1>
    <p style='text-align:center; font-size:1.05rem; color:#333;'>
      Aplikasi ini membantu menilai apakah Anda memiliki gejala yang perlu dievaluasi lebih lanjut
      dan faktor risiko kanker kolorektal, serta apakah perlu pemeriksaan endoskopi
      (EGD atau kolonoskopi). Hasil bersifat edukasi dan tidak menggantikan penilaian dokter.
    </p>
    """,
    unsafe_allow_html=True,
)

# ------------------ DATA PRIBADI (bukan expander) ------------------
st.markdown("### 🧑‍⚕️ Data Pribadi")

name = st.text_input("Nama lengkap")
col_x, col_y = st.columns(2)
with col_x:
    age = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
with col_y:
    sex = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)

today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ------------------ PERTANYAAN EGD (Gejala dyspepsia) ------------------
ALARM_EGD = [
    "Usia saya **≥50 tahun** dengan keluhan rasa tidak nyaman di ulu hati, perut terasa penuh/kembung, cepat kenyang, atau nyeri/panas di perut bagian atas (dispepsia).",
    "Ada **riwayat keluarga derajat pertama** (orang tua / saudara kandung) dengan **keganasan saluran cerna atas**.",
    "Berat badan saya **turun tanpa sebab jelas**.",
    "Saya mengalami **perdarahan saluran cerna** atau diberitahu ada **anemia defisiensi besi**.",
    "Saya **kesulitan menelan**, makanan/minuman terasa tersangkut di tenggorokan atau dada (**disfagia**).",
    "Saya **nyeri saat menelan**, seperti rasa perih/terbakar/menusuk di dada atau kerongkongan saat makanan/minuman lewat (**odynofagia**).",
    "Saya mengalami **muntah menetap / persisten**.",
]

egd_alarm_sel = []
gerd_q_score = 0
gerd_q_summary = ""

with st.expander(
    "Apakah Saya perlu teropong saluran cerna atas (EGD)?",
    expanded=False,
):
    st.subheader("1. Gejala yang Perlu Dievaluasi Lebih Lanjut")
    for i, q in enumerate(ALARM_EGD):
        if st.checkbox(q, key=f"egd_alarm_{i}"):
            egd_alarm_sel.append(q)

    st.markdown(
        """
        **Istilah penting:**
        - **Dispepsia**: rasa tidak nyaman di ulu hati, perut terasa penuh/kembung, cepat kenyang, atau nyeri/panas di perut bagian atas.
        - **Disfagia**: kesulitan menelan, makanan/minuman terasa tersangkut di tenggorokan atau dada.
        - **Odynofagia**: nyeri saat menelan, seperti rasa perih/terbakar/menusuk ketika makanan atau minuman lewat di kerongkongan.
        """,
        unsafe_allow_html=False,
    )

# ------------------ GERD-Q: Skrining GERD ------------------
GERDQ_OPTIONS = ["0 hari", "1 hari", "2–3 hari", "4–7 hari"]

with st.expander(
    "Apakah Saya mengidap GERD (Gastroesophageal Reflux Disease)?",
    expanded=False,
):
    st.write(
        "Jawablah seberapa sering dalam **1 minggu terakhir** Anda mengalami keluhan berikut:"
    )

    q1 = st.radio(
        "1. Seberapa sering Anda mengalami rasa terbakar di bagian belakang tulang dada (heartburn)?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq1",
    )
    q2 = st.radio(
        "2. Seberapa sering Anda mengalami naiknya isi lambung ke arah tenggorokan atau mulut (regurgitasi asam)?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq2",
    )
    q3 = st.radio(
        "3. Seberapa sering Anda mengalami nyeri ulu hati?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq3",
    )
    q4 = st.radio(
        "4. Seberapa sering Anda mengalami mual?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq4",
    )
    q5 = st.radio(
        "5. Seberapa sering keluhan di dada atau perut mengganggu tidur malam Anda?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq5",
    )
    q6 = st.radio(
        "6. Seberapa sering Anda minum obat tambahan (misal obat maag bebas) untuk mengurangi keluhan di dada atau perut?",
        GERDQ_OPTIONS,
        index=0,
        key="gerdq6",
    )

    # Skoring GERD-Q: 1–2 positif (0,1,2,3); 3–4 terbalik (3,2,1,0); 5–6 positif (0,1,2,3)
    def score_pos(ans: str) -> int:
        return GERDQ_OPTIONS.index(ans)

    def score_neg(ans: str) -> int:
        idx = GERDQ_OPTIONS.index(ans)
        return [3, 2, 1, 0][idx]

    gerd_q_score = (
        score_pos(q1)
        + score_pos(q2)
        + score_neg(q3)
        + score_neg(q4)
        + score_pos(q5)
        + score_pos(q6)
    )

    if gerd_q_score >= 8:
        badge_gerd = "badge badge-red"
        gerd_title = f"Skor GERD-Q: {gerd_q_score} — kemungkinan **menderita GERD**."
        gerd_text = (
            "Skor ≥8 meningkatkan kemungkinan adanya penyakit refluks asam lambung "
            "(GERD). Konsultasikan hasil ini ke dokter untuk evaluasi dan penatalaksanaan lebih lanjut."
        )
        gerd_q_summary = (
            f"Skor GERD-Q {gerd_q_score} (≥8) – hasil mengarah ke penyakit refluks asam lambung (GERD)."
        )
    else:
        badge_gerd = "badge badge-green"
        gerd_title = f"Skor GERD-Q: {gerd_q_score} — kemungkinan **tidak menderita GERD bermakna**."
        gerd_text = (
            "Skor <8 membuat kemungkinan GERD menurun. Namun bila keluhan menetap atau berat, "
            "tetap dianjurkan berkonsultasi ke dokter."
        )
        gerd_q_summary = (
            f"Skor GERD-Q {gerd_q_score} (<8) – kemungkinan kecil penyakit refluks asam lambung (GERD)."
        )

    st.markdown(
        f"""
        <div class="result-card">
          <span class="{badge_gerd}">{gerd_title}</span><br/>
          {gerd_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------ PERTANYAAN KOLO ------------------
ALARM_COLO = [
    "Saya **keluar darah segar dari dubur** sedang–berat / **menetes**.",
    "Saya **anemia defisiensi besi** atau tampak pucat/lemas.",
    "Berat badan saya **turun tanpa sebab jelas**.",
    "Terjadi **perubahan pola BAB progresif** (>4–6 minggu) disertai darah.",
    "Nyeri perut berat menetap, **diare berdarah/demam** (curiga kolitis/IBD berat).",
]
RISK_COLO = [
    "Usia **≥50 tahun** dengan keluhan saluran cerna bawah.",
    "Ada **keluarga dekat** dengan **kanker kolorektal atau polip adenoma**.",
    "**Pemeriksaan tinja darah samar positif**.",
    "Riwayat **IBD** (kolitis ulseratif atau penyakit Crohn) — evaluasi/monitoring.",
    "Riwayat **polip atau operasi kanker kolorektal** — perlu **surveilans** berkala.",
]
OTHER_COLO = [
    "**Perubahan kebiasaan BAB** >4–6 minggu tanpa darah atau demam.",
    "**Konstipasi kronik** tidak membaik dengan pengobatan awal.",
    "**Diare kronik** >4 minggu.",
    "Nyeri perut bawah berulang disertai perubahan BAB.",
    "Keluar **lendir/darah sedikit** berulang dari anus.",
    "Skrining polip/kanker kolorektal **secara elektif** sesuai usia/risiko.",
]

colo_alarm_sel, colo_risk_sel, colo_other_sel = [], [], []

with st.expander(
    "Apakah Saya perlu teropong saluran cerna bawah (Kolonoskopi)?",
    expanded=False,
):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("1. Gejala yang Perlu Dievaluasi Lebih Lanjut")
        for i, q in enumerate(ALARM_COLO):
            if st.checkbox(q, key=f"colo_alarm_{i}"):
                colo_alarm_sel.append(q)

    with c2:
        st.subheader("2. Keluhan atau Kondisi yang Dapat Ditangani Secara Elektif")
        st.caption(
            "Keluhan ini umumnya tidak mendesak, tetapi bila berlangsung menetap atau mengganggu, "
            "kolonoskopi dapat membantu mencari penyebabnya."
        )
        for i, q in enumerate(OTHER_COLO):
            if st.checkbox(q, key=f"colo_other_{i}"):
                colo_other_sel.append(q)

    with c3:
        st.subheader("3. Faktor Risiko yang Perlu Diperhatikan")
        for i, q in enumerate(RISK_COLO):
            if st.checkbox(q, key=f"colo_risk_{i}"):
                colo_risk_sel.append(q)

    st.markdown(
        """
        **Keterangan:**
        - **IBD (Inflammatory Bowel Disease)** adalah peradangan kronik pada usus, misalnya kolitis ulseratif atau penyakit Crohn,
          yang meningkatkan risiko kanker kolorektal.
        - **CRC (Colorectal Cancer)** adalah kanker yang berasal dari usus besar atau rektum. Banyak kasus berawal dari polip
          yang tumbuh perlahan dan dapat dideteksi serta diangkat dengan kolonoskopi.
        """,
        unsafe_allow_html=False,
    )

# ------------------ APCS: Skor Risiko Kanker Kolorektal ------------------
st.markdown("---")
st.markdown("### 📊 Skrining Risiko Kanker Kolorektal (APCS)")

if age < 45:
    age_score = 0
elif 45 <= age <= 69:
    age_score = 2
else:  # age >= 70
    age_score = 3

sex_score = 1 if sex == "Laki-laki" else 0

fhx = st.radio(
    "Riwayat keluarga kanker kolorektal derajat pertama (Ayah/Ibu/Kakak/Adik kandung)",
    ["Tidak ada", "Ada"],
    index=0,
)
fhx_score = 0 if fhx == "Tidak ada" else 2

smoke = st.radio(
    "Riwayat merokok",
    ["Tidak pernah merokok", "Saat ini merokok atau dulu pernah merokok"],
    index=0,
)
smoke_score = 0 if smoke.startswith("Tidak") else 1

score_apcs = age_score + sex_score + fhx_score + smoke_score

if score_apcs <= 1:
    kategori_apcs = "Risiko Rendah (0–1)"
    pesan_apcs = (
        "Anda termasuk kelompok risiko rendah kanker kolorektal berdasarkan skor APCS. "
        "Tetap jaga pola hidup sehat dan lakukan penilaian ulang secara berkala sesuai anjuran tenaga kesehatan."
    )
    badge_apcs = "badge badge-green"
elif score_apcs <= 3:
    kategori_apcs = "Risiko Sedang (2–3)"
    pesan_apcs = (
        "Anda termasuk kelompok risiko sedang. Disarankan berkonsultasi ke fasilitas kesehatan "
        "untuk mempertimbangkan skrining Tes Darah Samar Feses (iFOBT) secara berkala."
    )
    badge_apcs = "badge badge-gray"
else:
    kategori_apcs = "Risiko Tinggi (4–7)"
    pesan_apcs = (
        "Anda termasuk kelompok risiko tinggi kanker kolorektal. Disarankan berkonsultasi ke fasilitas kesehatan "
        "untuk pemeriksaan lebih lanjut, seperti colok dubur, Tes Darah Samar Feses (iFOBT), dan kemungkinan kolonoskopi."
    )
    badge_apcs = "badge badge-red"

st.markdown(
    f"""
    <div class="result-card">
      <span class="{badge_apcs}">Skor APCS: <b>{score_apcs}</b> — {kategori_apcs}</span><br/>
      {pesan_apcs}
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------ HASIL SKRINING EGD & KOLO ------------------
def verdict(alarm, risk, other, organ):
    if alarm:
        return (
            f"🔴 Anda **perlu {organ} segera**",
            "badge badge-red",
            "Segera konsultasi ke dokter penyakit dalam atau IGD, terutama bila keluhan berat atau mendadak.",
        )
    elif risk or other:
        return (
            f"🟢 Anda **dapat menjadwalkan {organ} (elektif)**",
            "badge badge-green",
            "Buat janji di poliklinik untuk pemeriksaan dan penilaian lebih lanjut.",
        )
    else:
        return (
            f"⚪ Saat ini **belum tampak kebutuhan mendesak untuk {organ}**",
            "badge badge-gray",
            "Lanjutkan pemantauan dan pengobatan rutin. Bila keluhan menetap >4–6 minggu atau muncul gejala yang perlu dievaluasi lebih lanjut, segera konsultasi ke dokter.",
        )

v_egd, b_egd, a_egd = verdict(
    egd_alarm_sel, [], [], "endoskopi saluran cerna atas (EGD)"
)

v_colo, b_colo, a_colo = verdict(
    colo_alarm_sel,
    colo_risk_sel,
    colo_other_sel,
    "kolonoskopi (saluran cerna bawah)",
)

if score_apcs >= 4:
    v_colo = (
        "🟠 Risiko tinggi berdasarkan skor APCS — perlu evaluasi lebih lanjut untuk kanker kolorektal"
    )
    b_colo = "badge badge-red"
    a_colo += (
        " Selain itu, skor APCS Anda berada pada kelompok risiko tinggi (4–7). "
        "Disarankan berkonsultasi ke fasilitas kesehatan untuk pemeriksaan colok dubur, Tes Darah Samar Feses (iFOBT), "
        "dan pertimbangan kolonoskopi."
    )
elif 2 <= score_apcs <= 3:
    a_colo += (
        " Skor APCS menunjukkan risiko sedang (2–3). "
        "Diskusikan dengan dokter mengenai kebutuhan skrining iFOBT dan evaluasi lanjutan."
    )

st.subheader("📋 Ringkasan Hasil Skrining Endoskopi")
colA, colB = st.columns(2)
with colA:
    st.markdown(
        f'<div class="result-card"><span class="{b_egd}">{v_egd}</span><br/>{a_egd}</div>',
        unsafe_allow_html=True,
    )
with colB:
    st.markdown(
        f'<div class="result-card"><span class="{b_colo}">{v_colo}</span><br/>{a_colo}</div>',
        unsafe_allow_html=True,
    )

# ------------------ PDF EXPORT (kop surat RS Kariadi) ------------------
def build_pdf_letterhead(
    name: str,
    age: int,
    sex: str,
    today: str,
    v_egd: str,
    a_egd: str,
    r_egd: list,
    gerd_q_summary: str,
    v_colo: str,
    a_colo: str,
    r_colo: list,
    logo_rs_path: str | None,
    logo_isi_path: str | None,
) -> bytes:
    """Bangun PDF hasil skrining endoskopi (EGD & Kolonoskopi) + ringkasan GERD-Q."""
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, leftMargin=32, rightMargin=32, topMargin=30, bottomMargin=28
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="H1C",
            parent=styles["Title"],
            alignment=1,
            leading=22,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallGray",
            parent=styles["Normal"],
            textColor=colors.HexColor("#444"),
            fontSize=10,
        )
    )
    styles.add(ParagraphStyle(name="Label", parent=styles["Normal"], spaceAfter=2))
    styles.add(
        ParagraphStyle(
            name="Bold",
            parent=styles["Normal"],
            fontName=styles["Heading4"].fontName,
            spaceAfter=4,
        )
    )

    elems = []

    left_img = (
        Image(logo_rs_path, width=130, height=60)
        if logo_rs_path and Path(logo_rs_path).exists()
        else ""
    )
    right_img = (
        Image(logo_isi_path, width=120, height=120)
        if logo_isi_path and Path(logo_isi_path).exists()
        else ""
    )

    kop_text = Paragraph(
        "<para align='center'>"
        "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
        "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
        "Telepon: (024) 8413993<br/>"
        "Website: www.rskariadi.co.id"
        "</para>",
        styles["Normal"],
    )

    header_tbl = Table(
        [[left_img, kop_text, right_img]],
        colWidths=[135, 300, 120],
        hAlign="CENTER",
    )
    header_tbl.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("RIGHTPADDING", (2, 0), (2, 0), 0),
            ]
        )
    )

    elems.append(header_tbl)
    elems += [
        Spacer(1, 6),
        Table(
            [[""]],
            colWidths=[555],
            style=[("LINEBELOW", (0, 0), (0, 0), 2, colors.HexColor("#2fa3a0"))],
        ),
        Spacer(1, 10),
    ]

    elems.append(
        Paragraph("HASIL SKRINING ENDOSKOPI SALURAN CERNA", styles["H1C"])
    )
    elems.append(Paragraph("(EGD & Kolonoskopi)", styles["SmallGray"]))
    elems.append(Spacer(1, 6))

    ident = [
        Paragraph(f"<b>Tanggal:</b> {today}", styles["Label"]),
        Paragraph(f"<b>Nama:</b> {name if name else '-'}", styles["Label"]),
        Paragraph(f"<b>Usia:</b> {age} tahun", styles["Label"]),
        Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Label"]),
    ]
    elems.extend(ident)
    elems.append(Spacer(1, 10))

    elems.append(Paragraph("<b>1) Saluran Cerna Atas (EGD)</b>", styles["Bold"]))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_egd}", styles["Label"]))
    elems.append(Paragraph(a_egd, styles["Label"]))
    if r_egd:
        elems.append(Spacer(1, 2))
        elems.append(Paragraph("<b>Gejala yang terdeteksi:</b>", styles["Label"]))
        for r in r_egd:
            elems.append(Paragraph(f"• {r}", styles["Label"]))

    if gerd_q_summary:
        elems.append(Spacer(1, 6))
        elems.append(
            Paragraph("<b>Skor GERD-Q (keluhan refluks lambung):</b>", styles["Label"])
        )
        elems.append(Paragraph(gerd_q_summary, styles["Label"]))

    elems.append(Spacer(1, 8))

    elems.append(Paragraph("<b>2) Saluran Cerna Bawah (Kolonoskopi)</b>", styles["Bold"]))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_colo}", styles["Label"]))
    elems.append(Paragraph(a_colo, styles["Label"]))
    if r_colo:
        elems.append(Spacer(1, 2))
        elems.append(Paragraph("<b>Gejala / faktor yang terdeteksi:</b>", styles["Label"]))
        for r in r_colo:
            elems.append(Paragraph(f"• {r}", styles["Label"]))
    elems.append(Spacer(1, 12))

    elems.append(
        Paragraph(
            "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
            "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
            styles["SmallGray"],
        )
    )

    doc.build(elems)
    return buf.getvalue()


def build_pdf_apcs(
    name: str,
    age: int,
    sex: str,
    today: str,
    score_apcs: int,
    kategori_apcs: str,
    pesan_apcs: str,
    logo_rs_path: str | None,
    logo_isi_path: str | None,
) -> bytes:
    """Bangun PDF hasil skrining risiko kanker kolorektal (APCS)."""
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, leftMargin=32, rightMargin=32, topMargin=30, bottomMargin=28
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Judul",
            parent=styles["Title"],
            alignment=1,
            fontSize=14,
            leading=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#555"),
        )
    )
    styles.add(
        ParagraphStyle(name="Label", parent=styles["Normal"], fontSize=11, spaceAfter=4)
    )

    elems = []

    left_img = (
        Image(logo_rs_path, width=130, height=60)
        if logo_rs_path and Path(logo_rs_path).exists()
        else ""
    )
    right_img = (
        Image(logo_isi_path, width=130, height=130)
        if logo_isi_path and Path(logo_isi_path).exists()
        else ""
    )

    kop_text = Paragraph(
        "<para align='center'>"
        "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
        "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
        "Telepon: (024) 8413993<br/>Website: www.rskariadi.co.id"
        "</para>",
        styles["Small"],
    )

    header_tbl = Table(
        [[left_img, kop_text, right_img]],
        colWidths=[135, 300, 120],
        hAlign="CENTER",
    )
    header_tbl.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("RIGHTPADDING", (2, 0), (2, 0), 0),
            ]
        )
    )

    elems.append(header_tbl)
    elems.append(Spacer(1, 8))

    elems.append(
        Table(
            [[""]],
            colWidths=[555],
            style=[("LINEBELOW", (0, 0), (0, 0), 2, colors.HexColor("#2fa3a0"))],
        )
    )
    elems.append(Spacer(1, 10))

    elems.append(
        Paragraph("HASIL SKRINING RISIKO KANKER KOLOREKTAL", styles["Judul"])
    )
    elems.append(
        Paragraph("(APCS – Asia-Pacific Colorectal Screening Score)", styles["Small"])
    )
    elems.append(Spacer(1, 12))

    elems.append(Paragraph(f"<b>Tanggal:</b> {today}", styles["Label"]))
    elems.append(Paragraph(f"<b>Nama:</b> {name}", styles["Label"]))
    elems.append(Paragraph(f"<b>Usia:</b> {age} tahun", styles["Label"]))
    elems.append(Paragraph(f"<b>Jenis Kelamin:</b> {sex}", styles["Label"]))
    elems.append(Spacer(1, 12))

    elems.append(Paragraph("<b>Hasil Perhitungan APCS:</b>", styles["Label"]))
    elems.append(
        Paragraph(
            f"<b>Skor:</b> {score_apcs} — <b>Kategori Risiko:</b> {kategori_apcs}",
            styles["Label"],
        )
    )
    elems.append(Spacer(1, 6))
    elems.append(Paragraph(pesan_apcs, styles["Label"]))
    elems.append(Spacer(1, 12))

    elems.append(
        Paragraph(
            "Catatan: Hasil ini merupakan skrining awal berdasarkan formulir APCS. "
            "Pemeriksaan lanjutan seperti Tes Darah Samar Feses (iFOBT), colok dubur, "
            "atau kolonoskopi akan ditentukan oleh dokter sesuai protokol nasional.",
            styles["Small"],
        )
    )

    doc.build(elems)
    return buf.getvalue()


r_egd_all = egd_alarm_sel
r_colo_all = colo_alarm_sel + colo_risk_sel + colo_other_sel

st.markdown("")

if HAS_RL:
    pdf_bytes = build_pdf_letterhead(
        name or "",
        int(age),
        sex,
        today,
        v_egd,
        a_egd,
        r_egd_all,
        gerd_q_summary,
        v_colo,
        a_colo,
        r_colo_all,
        logo_kariadi,
        logo_isi,
    )

    pdf_apcs_bytes = build_pdf_apcs(
        name=name or "",
        age=int(age),
        sex=sex,
        today=today,
        score_apcs=score_apcs,
        kategori_apcs=kategori_apcs,
        pesan_apcs=pesan_apcs,
        logo_rs_path=logo_kariadi,
        logo_isi_path=logo_isi,
    )

    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        st.download_button(
            "⬇️ Unduh Surat Hasil Endoskopi (PDF)",
            data=pdf_bytes,
            file_name=f"Hasil_Skrining_ISI_PERUT_{today.replace(' ','_')}.pdf",
            mime="application/pdf",
        )
    with col_pdf2:
        st.download_button(
            "⬇️ Unduh Surat Hasil Risiko Kanker Kolorektal (APCS)",
            data=pdf_apcs_bytes,
            file_name=f"Hasil_APCS_{today.replace(' ','_')}.pdf",
            mime="application/pdf",
        )
else:
    st.info(
        "Fitur unduh PDF membutuhkan paket **reportlab**.\n\n"
        "Tambahkan file `requirements.txt` dengan isi:\n"
        "`streamlit>=1.37` dan `reportlab>=3.6.12`, lalu deploy ulang.",
        icon="ℹ️",
    )

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption(
    "© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam"
)
