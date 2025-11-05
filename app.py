# app.py — Skrining Terpadu EGD + Kolonoskopi
# Tema RS Kariadi • Dua logo bersebelahan (responsif) • Ilustrasi rata tengah • Export PDF Kopsurat
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang

import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime

import streamlit as st

# ==== PDF ====
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna?",
    page_icon="🩺",
    layout="wide",
)


# ------------------ HELPERS ------------------
def pick_first_existing(paths):
    """Ambil path pertama yang ada."""
    for p in paths:
        if Path(p).exists():
            return p
    return None


def img_to_b64(path: str) -> str | None:
    """Ubah file image ke base64 data URI (PNG/JPG)."""
    if not path or not Path(path).exists():
        return None
    mime = "image/png" if str(path).lower().endswith("png") else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


# ------------------ ASSET PATHS ------------------
logo_kariadi = pick_first_existing(["logo_kariadi.png", "./logo_kariadi.png", "/app/logo_kariadi.png"])
logo_isi_perut = pick_first_existing(["logo_isi_perut.png", "logo_isi_perut.jpg", "logo_isi_perut.jpeg"])
egd_img = pick_first_existing(["ilustrasi_egd.png", "egd_illustration.png", "egd_image.png"])
colo_img = pick_first_existing(["ilustrasi_colonoscopy.png", "colonoscopy.png"])


# ------------------ UI STATE (bisa diubah dari panel) ------------------
if "ui" not in st.session_state:
    st.session_state.ui = {
        "rs_w": 190,     # lebar logo RS (px)
        "isi_w": 190,    # lebar logo ISI PERUT (px)
        "gap": 34,       # jarak antar logo (px)
        "rs_y": -8,      # offset naik/turun logo RS (px; negatif = naik)
        "egd_w": 320,    # max width EGD (px)
        "colo_w": 340,   # max width Kolonoskopi (px)
    }
ui = st.session_state.ui


# ------------------ BASE CSS ------------------
st.markdown("""
<style>
/* Sembunyikan sidebar */
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }

/* Latar & tipografi */
.stApp { background: linear-gradient(135deg,#e8f5e9 0%,#ffffff 55%,#e6fffb 100%); color:#1c1c1c; }
.block-container { padding-top: 18px; padding-bottom: 2rem; }
h1,h2,h3 { color:#007C80; } h1{ font-weight:800; } h2,h3{ font-weight:700; }

/* ===== Header: dua logo sejajar (desktop), responsif (mobile) ===== */
.header-wrap { display:flex; justify-content:center; margin-top:34px; }
.header-inner {
  display:flex; align-items:center; justify-content:center; gap: var(--gap, 28px);
  max-width: 980px; width: 92%; margin:auto;
  flex-wrap: nowrap;            /* cegah pindah baris di desktop */
}
.header-inner img { height:auto; object-fit:contain; border:none; }
.header-inner .rs { width: var(--rsw, 150px); position:relative; top: var(--rsy, -6px); }
.header-inner .isi{ width: var(--isiw, 150px); }

/* Deskripsi tengah */
.desc { text-align:center; font-size:1.05rem; line-height:1.6; max-width:900px; margin: 10px auto 18px; }

/* ===== Ilustrasi: selalu rata tengah ===== */
.illus-wrap { display:flex; justify-content:center; gap: 32px; flex-wrap: wrap; }
.fig {
  display:flex; flex-direction:column; align-items:center;
  max-width: min(100%, 480px);
}
.fig .imgbox { width:100%; text-align:center; }
.fig .imgbox img {
  width:100% !important; height:auto !important; border-radius:10px;
  box-shadow:0 3px 10px rgba(0,0,0,.05);
}
.fig .cap { color:#5b7580; font-size:.92rem; margin-top:.45rem; }

/* Mobile tweaks */
@media (max-width: 900px){
  .header-inner { flex-wrap: wrap; gap: 12px; }
  .header-inner .rs, .header-inner .isi { width: clamp(120px, 42vw, 170px); top: 0; }
}
</style>
""", unsafe_allow_html=True)

# apply CSS variables for dynamic sizes
st.markdown(f"""
<style>
:root {{
  --rsw: {ui['rs_w']}px;
  --isiw:{ui['isi_w']}px;
  --gap: {ui['gap']}px;
  --rsy: {ui['rs_y']}px;
}}
</style>
""", unsafe_allow_html=True)


# ------------------ HEADER (dua logo bersebelahan) ------------------
rs_b64  = img_to_b64(logo_kariadi)
isi_b64 = img_to_b64(logo_isi_perut)

st.markdown("<div class='header-wrap'><div class='header-inner'>", unsafe_allow_html=True)
if rs_b64:
    st.markdown(f"<img class='rs' src='{rs_b64}' alt='RS Kariadi'/>", unsafe_allow_html=True)
if isi_b64:
    st.markdown(f"<img class='isi' src='{isi_b64}' alt='ISI PERUT'/>", unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------ DESKRIPSI ISI PERUT ------------------
st.markdown("""
<div class='desc'>
  <b>ISI PERUT</b> <i>(Instrumen Skrining dan Informasi Penyakit Saluran Cerna)</i> adalah aplikasi yang membantu Anda
  mengetahui informasi tentang teropong saluran cerna baik atas maupun bawah, serta membantu Anda melakukan skrining mandiri
  apakah tindakan teropong saluran cerna ini diperlukan atau tidak berdasarkan keluhan saluran cerna Anda.
</div>
""", unsafe_allow_html=True)

# ------------------ ILUSTRASI (rata tengah; wrap jika sempit) ------------------
st.markdown("<div class='illus-wrap'>", unsafe_allow_html=True)

# EGD
st.markdown("<div class='fig'>", unsafe_allow_html=True)
st.markdown("<div class='imgbox'>", unsafe_allow_html=True)
if egd_img:
    st.image(egd_img, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='cap'>Skema endoskopi saluran cerna atas (EGD)</div></div>", unsafe_allow_html=True)

# Kolonoskopi
st.markdown("<div class='fig'>", unsafe_allow_html=True)
st.markdown("<div class='imgbox'>", unsafe_allow_html=True)
if colo_img:
    st.image(colo_img, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='cap'>Skema endoskopi saluran cerna bawah (Kolonoskopi)</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close illus-wrap
st.markdown("---")

# Terapkan max-width ilustrasi via CSS inline (berdasarkan panel)
st.markdown(f"""
<style>
.fig:nth-of-type(1) .imgbox img {{ max-width:{ui['egd_w']}px !important; }}
.fig:nth-of-type(2) .imgbox img {{ max-width:{ui['colo_w']}px !important; }}
</style>
""", unsafe_allow_html=True)

# ------------------ DATA DASAR (opsional) ------------------
with st.expander("🧑‍⚕️ Data dasar (opsional)", expanded=False):
    name = st.text_input("Nama")
    age  = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    sex  = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")


# ------------------ PERTANYAAN: EGD (Atas) ------------------
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

egd_alarm_sel, egd_risk_sel, egd_other_sel = [], [], []
with st.expander("Apakah Saya perlu teropong saluran cerna **atas (EGD)** ?", expanded=False):
    e1, e2, e3 = st.columns(3)
    with e1:
        st.subheader("🚨 Tanda Bahaya")
        st.caption("Jika ada salah satu, endoskopi biasanya **dianjurkan segera**.")
        for i, q in enumerate(ALARM_EGD):
            if st.checkbox(q, key=f"egd_alarm_{i}"): egd_alarm_sel.append(q)
    with e2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_EGD):
            if st.checkbox(q, key=f"egd_risk_{i}"): egd_risk_sel.append(q)
    with e3:
        st.subheader("🩹 Indikasi Lain (Elektif)")
        for i, q in enumerate(OTHER_EGD):
            if st.checkbox(q, key=f"egd_other_{i}"): egd_other_sel.append(q)


# ------------------ PERTANYAAN: KOLONOSKOPI (Bawah) ------------------
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
    "**Perubahan kebiasaan BAB** >4–6 minggu (lebih sering/konstipasi/mengecil) tanpa alarm",
    "**Konstipasi kronik** tidak membaik meski sudah tata laksana awal",
    "**Diare kronik** >4 minggu",
    "Nyeri perut bawah berulang disertai perubahan BAB (evaluasi lanjut bila tidak membaik)",
    "Keluar **lendir/darah sedikit** berulang dari anus",
    "Skrining polip/CRC **elektif** sesuai usia/risiko",
]

colo_alarm_sel, colo_risk_sel, colo_other_sel = [], [], []
with st.expander("Apakah Saya perlu teropong saluran cerna **bawah (Kolonoskopi)** ?", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🚨 Tanda Bahaya")
        st.caption("Jika ada salah satu, kolonoskopi biasanya **dianjurkan segera**.")
        for i, q in enumerate(ALARM_COLO):
            if st.checkbox(q, key=f"colo_alarm_{i}"): colo_alarm_sel.append(q)
    with c2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_COLO):
            if st.checkbox(q, key=f"colo_risk_{i}"): colo_risk_sel.append(q)
    with c3:
        st.subheader("🩹 Indikasi Lain (Elektif)")
        for i, q in enumerate(OTHER_COLO):
            if st.checkbox(q, key=f"colo_other_{i}"): colo_other_sel.append(q)

st.markdown("---")


# ------------------ PENILAIAN HASIL ------------------
def verdict_and_advice(alarm_list, risk_list, other_list, organ_name):
    alarm = len(alarm_list) > 0
    risk  = len(risk_list)  > 0
    other = len(other_list) > 0

    if alarm:
        verdict = f"🔴 Anda **perlu {organ_name} segera**"
        badge = "badge badge-red"
        advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda.**"
    elif risk or other:
        verdict = f"🟢 Anda **dapat menjadwalkan {organ_name} (elektif)**"
        badge = "badge badge-green"
        advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    else:
        verdict = f"⚪ Saat ini **belum tampak kebutuhan mendesak untuk {organ_name}**"
        badge = "badge badge-gray"
        advice = ("Lanjutkan tata laksana konservatif dan pemantauan. Bila keluhan **tidak membaik 4–6 minggu** "
                  "atau muncul **tanda bahaya**, segera periksa ke dokter penyakit dalam.")
    reasons = alarm_list + risk_list + other_list
    return verdict, badge, advice, reasons


v_egd,  b_egd,  a_egd,  r_egd  = verdict_and_advice(egd_alarm_sel, egd_risk_sel, egd_other_sel, "endoskopi saluran cerna atas (EGD)")
v_colo, b_colo, a_colo, r_colo = verdict_and_advice(colo_alarm_sel, colo_risk_sel, colo_other_sel, "kolonoskopi (saluran cerna bawah)")

st.subheader("📋 Hasil Skrining")
colA, colB = st.columns(2)

with colA:
    st.markdown(f'<div class="result-card"><span class="{b_egd}">{v_egd}</span><br/>{a_egd}</div>', unsafe_allow_html=True)
    with st.expander("Alasan (Atas/EGD)"):
        if r_egd:
            for i, r in enumerate(r_egd, 1):
                st.write(f"{i}. {r}")
        else:
            st.write("Tidak ada pilihan yang tercentang.")

with colB:
    st.markdown(f'<div class="result-card"><span class="{b_colo}">{v_colo}</span><br/>{a_colo}</div>', unsafe_allow_html=True)
    with st.expander("Alasan (Bawah/Kolonoskopi)"):
        if r_colo:
            for i, r in enumerate(r_colo, 1):
                st.write(f"{i}. {r}")
        else:
            st.write("Tidak ada pilihan yang tercentang.")


# ------------------ PDF EXPORT (Kopsurat RS Kariadi) ------------------
def build_pdf_letterhead(
    name: str, age: int, sex: str, today: str,
    v_egd: str, a_egd: str, r_egd: list,
    v_colo: str, a_colo: str, r_colo: list,
    logo_path: str | None
) -> bytes:
    """Bangun PDF surat hasil dengan kop RS Kariadi (logo + alamat) + 2 ringkasan hasil."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=32, rightMargin=32, topMargin=30, bottomMargin=28)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1", parent=styles["Title"], alignment=1, leading=20, spaceAfter=12))
    styles.add(ParagraphStyle(name="SmallGray", parent=styles["Normal"], textColor=colors.HexColor("#444"), fontSize=10))

    elems = []

    # Kop RS
    img_width = 110
    img = None
    if logo_path and Path(logo_path).exists():
        img = Image(logo_path, width=img_width, height=img_width*0.45)
    kop_left  = img if img else ""
    kop_right = Paragraph(
        "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
        "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
        "Telepon : (024) 8413993, 8413476, 8413764 &nbsp;&nbsp; "
        "<b>Fax :</b> (024) 8318617<br/>"
        "Website : http://www.rskariadi.co.id",
        styles["Normal"]
    )
    kop_tbl = Table([[kop_left, kop_right]], colWidths=[img_width+8, 450], hAlign="LEFT")
    kop_tbl.setStyle(TableStyle([("VALIGN",(0,0),(1,0),"MIDDLE")]))
    elems += [kop_tbl, Spacer(1,10), Table([[""]], colWidths=[530],
                                           style=[("LINEBELOW",(0,0),(0,0),1,colors.HexColor("#9dd8d3"))]), Spacer(1,6)]

    # Judul
    elems.append(Paragraph("HASIL SKRINING ENDOSKOPI SALURAN CERNA", styles["H1"]))
    elems.append(Paragraph("(EGD & Kolonoskopi)", styles["SmallGray"]))
    elems.append(Spacer(1,6))

    # Identitas
    ident = [
        Paragraph(f"<b>Tanggal:</b> {today}", styles["Normal"]),
        Paragraph(f"<b>Nama:</b> {name if name else '-'}", styles["Normal"]),
        Paragraph(f"<b>Usia:</b> {age} tahun", styles["Normal"]),
        Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Normal"]),
    ]
    for p in ident: elems.append(p)
    elems.append(Spacer(1,10))

    # Seksi 1: EGD
    elems.append(Paragraph("<b>1) Saluran Cerna Atas (EGD)</b>", styles["Normal"]))
    elems.append(Spacer(1,2))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_egd}", styles["Normal"]))
    elems.append(Paragraph(a_egd.replace("\n","<br/>"), styles["Normal"]))
    if r_egd:
        elems.append(Spacer(1,4))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Normal"]))
        for r in r_egd: elems.append(Paragraph(f"- {r}", styles["Normal"]))
    elems.append(Spacer(1,10))

    # Seksi 2: Kolonoskopi
    elems.append(Paragraph("<b>2) Saluran Cerna Bawah (Kolonoskopi)</b>", styles["Normal"]))
    elems.append(Spacer(1,2))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_colo}", styles["Normal"]))
    elems.append(Paragraph(a_colo.replace("\n","<br/>"), styles["Normal"]))
    if r_colo:
        elems.append(Spacer(1,4))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Normal"]))
        for r in r_colo: elems.append(Paragraph(f"- {r}", styles["Normal"]))
    elems.append(Spacer(1,12))

    # Catatan
    elems.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        styles["Italic"]
    ))

    doc.build(elems)
    return buf.getvalue()


# Bangun PDF
pdf_bytes = build_pdf_letterhead(
    name or "", int(age), sex, today,
    v_egd, a_egd, r_egd,
    v_colo, a_colo, r_colo,
    logo_kariadi
)

st.download_button(
    label="⬇️ Unduh Surat Hasil (PDF)",
    data=pdf_bytes,
    file_name=f"Hasil_Skrining_Saluran_Cerna_{today.replace(' ','_')}.pdf",
    mime="application/pdf",
)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.",
    help="Tidak ada penyimpanan server."
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
