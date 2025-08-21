import streamlit as st
import pandas as pd
import os

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(layout="centered") 
st.title("Referensi Motor Bekas Mouza Motor")

st.markdown("""
    <style>
    /* Style untuk tombol */
    div.stButton > button {
        background-color: #dc3545;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #a71d2a;
        color: white;
    }

    /* Style untuk selectbox: ubah cursor jadi pointer */
    div[data-baseweb="select"] * {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stExpander"] {
    border: 1px solid #E0E0E0; 
    border-radius: 8px; 
    overflow: hidden; 
    margin-bottom: 15px; 
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
}
</style>
""", unsafe_allow_html=True)


# --- PEMUATAN DATASET DAN PRA-PEMROSESAN DATAFRAME ---
df = pd.read_csv("klaster_baru_data_motor_mouza.csv")


# --- MEMASUKAN GAMBAR KE DALAM DATAFRAME ---
def get_image_path(row): 
    model_name_for_path = row['Model'] 
    image_extensions = ['.jpeg', '.jfif'] 

    for ext in image_extensions:
        path = f"images/{model_name_for_path}{ext}" 
        return path

    return None

df['path_gambar'] = df['Model'].apply(lambda x: f"https://raw.githubusercontent.com/RatriYulia123/Mouzamotor-app/main/images/{x}.jpeg")


# --- DEFINISI INFORMASI KLASTER ---
klaster_harga_rentang = {
    0: {'min': 8000000.0,  'max': 30000000.0},
    1: {'min': 13500000.0, 'max': 36000000.0},
    2: {'min': 23000000.0, 'max': 24000000.0},
    3: {'min': 14500000.0, 'max': 60000000.0}
}


klaster_deskripsi_detail = {
    0: """Unit ini termasuk dalam kategori motor ekonomis, dengan harga jual yang terjangkau.
      Motor ini cocok bagi pengguna yang menyukai motor matik keluaran merek Honda dan membutuhkan kendaraan untuk aktivitas harian ringan, seperti pergi ke sekolah, bekerja, atau menjalankan kebutuhan sehari-hari lainnya
 """,
    1: """Unit ini termasuk dalam kategori motor kelas menengah, dengan harga yang relatif terjangkau. 
    Motor ini cocok bagi pengguna yang menyukai motor matik keluaran merek Yamaha, karena menawarkan performa yang baik serta desain yang modern
  """,
    2: """Unit ini termasuk dalam kategori motor sport entry level, dengan harga jual yang cukup terjangkau di kelasnya. Motor ini cocok bagi pengguna yang menginginkan tampilan motor sporty, dengan performa baik namun tetap ekonomis harganya
  """,
  3:""" Unit ini termasuk dalam kategori motor premium, dengan kapasitas mesin besar, motor ini cocok bagi pengguna yang menyukai motor sport keluaran merek Honda dengan performa unggul dan tampilan modern"""

}


# --- INISIALISASI SESSION STATE ---
for key, default in {
    "show_result": False,
    "search_triggered": False,
    "filter_applied": False,
    "reset_filter": False,
    "harga_input": 0,
    "model_input": "Semua",
    "jenis_input": "Semua",
    "tahun_input": "Semua",
    "transmisi_input": "Semua"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---  RESET FILTER  ---
if st.session_state.reset_filter:
    st.session_state["harga_input"] = 0
    st.session_state["model_input"] = "Semua"
    st.session_state["jenis_input"] = "Semua"
    st.session_state["tahun_input"] = "Semua"
    st.session_state["transmisi_input"] = "Semua"
    st.session_state.reset_filter = False
    st.rerun()


# --- SIDEBAR INPUT ---
st.sidebar.subheader('Cari harga motor bekas sesuai anggaran dan preferensimu di sini ')

# Harga input
st.sidebar.markdown("""
<div style='margin-bottom: -30px'>
    <label style=' font-size: 14px; font-weight: 600; '>Masukan budgetmu:</label><br>
    <span style='font-size: 15px; color: #666 '><i>minimal budget yang harus dimasukan 8.000.000</i></span>
</div>
""", unsafe_allow_html=True)

harga_input = st.sidebar.number_input(
    label="",
    min_value=0, 
    key="harga_input"
)

# Model input
model_input = st.sidebar.selectbox(
    f'**Tentukan pilihan motormu(opsional):**',
    ['Semua'] + sorted(df['Model'].unique().tolist()), key="model_input"
)

# Jenis input
jenis_input = st.sidebar.selectbox(
    f'**Pilih Jenis Motor(opsional):**',
    ['Semua'] + sorted(df['Jenis'].unique().tolist()), key="jenis_input"
)

# Tahun Input
tahun_input = st.sidebar.selectbox(
    f'**Pilih Tahun produksi (opsional):**',
    ['Semua'] + sorted(df['Tahun Produksi'].unique().tolist()), key="tahun_input"
)

# Transmisi Input
transmisi_input = st.sidebar.selectbox(
    f'**Pilih Transmisi (opsional):**',
    ['Semua'] + sorted(df['Transmisi'].unique().tolist()), key="transmisi_input"
)

# Tombol cari motor
if st.sidebar.button("Cari Motor"):
    st.session_state.show_result = True
    st.session_state.search_triggered = True
    st.session_state.filter_applied = False


# --- PROSES REKOMENDASI BERDASARKAN KLASTER ---
if not st.session_state.search_triggered:
    st.image("https://raw.githubusercontent.com/RatriYulia123/Mouzamotor-app/main/images/Gambar_home.jpeg", width=670)
    st.markdown("""
        📍 **Alamat dealer:**  
        Ruko Fitra Jaya, Jl. Kali Abang Tengah No.1-2  Perwira, Kec. Bekasi Utara

        📞 **No telp:**  
        [📲 0898-7567-677](https://wa.me/628987567677)

        🕘 **Jam Operasional:**  
        Senin - Sabtu, 09.00 - 19.00
    """)

# --- Budget tetap ---
budget_min = 8000000
budget_max = 60000000

# --- Validasi setelah tombol "Cari Motor" ditekan ---
if st.session_state.search_triggered and not st.session_state.filter_applied:

    # Budget terlalu rendah
    if st.session_state.harga_input < budget_min:
        st.warning("Tidak ditemukan motor dengan harga di bawah Rp8.000.000.")
        st.info("Silakan masukkan budget minimal Rp8.000.000 atau lebih untuk mendapatkan referensi motor bekas.")

        col1, col2 = st.columns([5, 1])  
        with col2:
            if st.button("Kembali", use_container_width=True, key="btn_kembali_min"):
                st.session_state.search_triggered = False
                st.session_state.show_result = False
                st.session_state.filter_applied = False
                st.session_state.reset_filter = True
                st.rerun()

        st.stop()

    # Budget terlalu tinggi
    elif st.session_state.harga_input > budget_max:
        st.warning("Tidak ditemukan motor dengan harga di atas Rp65.000.000.")
        st.info("Silakan masukkan budget maksimal Rp65.000.000 atau kurang untuk mendapatkan referensi motor bekas.")

        col1, col2 = st.columns([5, 1])  # Kolom 1 lebih besar, kolom 2 kecil di kanan
        with col2:
            if st.button("Kembali", use_container_width=True, key="btn_kembali_max"):
                st.session_state.search_triggered = False
                st.session_state.show_result = False
                st.session_state.filter_applied = False
                st.session_state.reset_filter = True
                st.rerun()

        st.stop()

    # Budget valid → lanjut proses
    else:
        st.session_state.show_result = True
        st.session_state.filter_applied = True

        
    klaster_cocok_ids = []

    # Mendefinisikan rentang harga klaster
    for klaster_id, rentang in klaster_harga_rentang.items():
        min_harga = rentang['min'] 
        max_harga = rentang['max'] 

        if min_harga <= harga_input <= max_harga:
            klaster_cocok_ids.append(klaster_id)

    # --- PROSES FILTERING DATA ---
    df_rekomendasi = df[df['Klaster'].isin(klaster_cocok_ids)]
    df_rekomendasi = df_rekomendasi[df_rekomendasi['Harga'] <= harga_input]

    if tahun_input != 'Semua':
        tahun_input = int(tahun_input)

        df_tahun_spesifik = df_rekomendasi[df_rekomendasi['Tahun Produksi'] == tahun_input]

        if df_tahun_spesifik.empty:
            tahun_berikutnya = tahun_input + 1
            df_tahun_spesifik = df_rekomendasi[df_rekomendasi['Tahun Produksi'] == tahun_berikutnya]

            df_rekomendasi = df_tahun_spesifik

    
    if jenis_input != 'Semua' and 'Jenis' in df_rekomendasi.columns:
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Jenis'] == jenis_input]

    if transmisi_input != 'Semua' and 'Transmisi' in df_rekomendasi.columns:
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Transmisi'] == transmisi_input]

    if model_input != 'Semua' and 'Model' in df_rekomendasi.columns:
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Model'] == str(model_input)]

    # Sorting data otomatis dari harga termurah ke mahal
    df_rekomendasi = df_rekomendasi.sort_values(by="Harga", ascending=True)
    
    #simpan hasil filtering
    st.session_state.df_hasil = df_rekomendasi


# --- TAMPILAN OUTPUT PENGGUNA ---
if st.session_state.search_triggered and st.session_state.filter_applied:
    st.subheader('Hasil Referensi')

    df_rekomendasi = st.session_state.get("df_hasil", pd.DataFrame())    
    
    if not df_rekomendasi.empty:
        # Menampilkan pesan sukses ketika motor sesuai kriteria
        st.success(f" Di temukan motor yang sesuai dengan kriteria kamu:")

        # Melakukan perulangan
        for index, row in df_rekomendasi.iterrows():
            klaster_id_motor = row['Klaster']
            kriteria_motor_friendly = klaster_deskripsi_detail.get(row['Klaster'], "kriteria motor tidak tersedia")
            deskripsi_motor=f"{kriteria_motor_friendly}"

            # Format harga dan odometer
            format_harga = f"Rp{int(row['Harga']):,}".replace(",", ".") 
            format_odometer = f"{int(row['Jarak Tempuh']):,} km".replace(",", ".") 

            # --- BAGIAN KARTU REKOMENDASI PERTAMA ---
            with st.container(border=True):
                col1, col2 = st.columns([1, 1]) 

                with col1:
                    st.markdown(f"""
                    <h4 style="margin-bottom:10px;">{row['Model']}</h4>
                    <p><strong>Harga:</strong> {format_harga}</p>
                    <p><strong>Tahun produksi:</strong> {int(row['Tahun Produksi'])}</p>
                    <p><strong>Jarak Tempuh:</strong> {format_odometer}</p>
                    """, unsafe_allow_html=True)

                with col2:
                 
                    if 'path_gambar' in row and pd.notna(row['path_gambar']):
                        st.image(str(row['path_gambar']), caption=row['Model'], use_container_width=True)
                    else:
                        st.info(f"Gambar untuk {row['Model']} tidak tersedia.")
                
                with st.expander(f"**🔍 lihat informasi detailnya**"):
                    st.write(f"**Transmisi :** {row['Transmisi']}")
                    st.write(f"**Jenis motor :** {row['Jenis']}")
                    st.write(f"**Kondisi motor :**")
                    st.write(row['Kondisi Motor'])
                    st.write(f"**Deskripsi :** {deskripsi_motor}")
                    

        st.markdown("<hr style='margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
             
        st.write("Dari hasil referensi yang di peroleh bagi yang berminat silahkan :")
        st.markdown("""
        📍 **Datang langsung ke dealer kami:**  
            Ruko Fitra Jaya, Jl. Kali Abang Tengah No.1-2  Perwira, Kec. Bekasi Utara

        📞 **Atau Hubungi kami di:**  
        [📲 0898-7567-677](https://wa.me/628987567677)
        """)
    else:
        st.warning(f"Maaf, tidak ada motor yang cocok dengan kategori yang tersedia")
        st.info("Silahkan ubah nominal budget atau kurangi filter pencarian dengan memilih opsi 'semua' ke beberapa kolom pencarian seperti tahun produksi, jenis motor dan tahun produksi")
    

    col1, col2 = st.columns([5, 1])  # Kolom 1 lebih besar, kolom 2 kecil di kanan
    with col2:
        if st.button("Kembali", use_container_width=True):
            st.session_state.show_result = False
            st.session_state.search_triggered = False
            st.session_state.filter_applied = False
            st.session_state.reset_filter = True
            st.rerun()
            


    

            





        
















