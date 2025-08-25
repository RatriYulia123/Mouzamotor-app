import streamlit as st
import pandas as pd
import os

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(layout="centered") 
st.title("Referensi Pembelian Motor Bekas di Mouza Motor 🏍️")

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
df = pd.read_csv("clustering new mouza motor.csv")


# --- MEMASUKAN GAMBAR KE DALAM DATAFRAME ---
def get_image_path(row): 
    model_name_for_path = row['Model'] 
    image_extensions = ['.jpeg', '.jfif'] 

    for ext in image_extensions:
        path = f"images/{model_name_for_path}{ext}" 
        if os.path.exists(path): 
            return path

    return None

df['path_gambar'] = df.apply(get_image_path, axis=1) 


# --- DEFINISI INFORMASI KLASTER ---
klaster_harga_rentang = {
    0: {'min': 8000000.0,  'max': 30000000.0},
    1: {'min': 13500000.0, 'max': 36000000.0},
    2: {'min': 23000000.0, 'max': 24000000.0},
    3: {'min': 14500000.0, 'max': 21000000.0}
}


klaster_deskripsi_detail = {
    0: """Unit ini termasuk dalam kategori motor matic ekonomis dari Honda. Jarak tempuhnya sudah tinggi, kapasitas mesin dalam unit ini mayoritas 110 cc, tetapi terdapat beberapa unit dengan kapasitas mesin besar 160 cc dan harga jualnya terjangkau. Motor ini cocok untuk pengguna yang menyukai motor matic Honda dan membutuhkan kendaraan untuk aktivitas harian, terutama untuk perjalanan jarak dekat.
 """,
    1: """Unit ini termasuk dalam kategori motor matic kelas menengah dari Yamaha dengan jarak tempuh relatif rendah, rata-rata kapasitas mesin didalam unit ini besar sekitar 125-155 cc dan harga jualnya yang relatif terjangkau. Motor ini cocok untuk pengguna yang menyukai motor matic Yamaha dan membutuhkan kendaraan yang nyaman untuk aktivitas harian di perkotaan, terutama bagi mereka yang sering menempuh perjalanan jauh seperti pulang-pergi kerja.
  """,
    2: """Unit ini termasuk dalam kategori motor sport premium dari Yamaha. Dengan jarak tempuh yang masih sangat rendah dan kapasitas mesin 155 cc, motor ini menawarkan performa yang tangguh untuk kelasnya. Cocok bagi pengguna yang mengutamakan performa, menyukai desain sporty, dan menginginkan fitur-fitur canggih dengan harga yang masih relatif terjangkau.
  """,
  3:""" Unit ini termasuk dalam kategori motor sport entry level dari Honda. Dengan kapasitas mesin 150 cc dan jarak tempuh yang sudah tinggi, motor ini menawarkan bahan bakar yang irit dan harga yang sangat terjangkau untuk kelasnya. Cocok bagi pengguna yang menyukai motor sport Honda dan mencari harga yang ekonomis"""

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
    st.image("images/Gambar_home.jpeg", width=670)
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
budget_max = 36000000

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
        st.warning("Tidak ditemukan motor dengan harga di atas Rp36.000.000.")
        st.info("Silakan masukkan budget maksimal Rp36.000.000 atau kurang untuk mendapatkan referensi motor bekas.")

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
    for klaster_id, rentang in klaster_harga_rentang.items():
        if rentang['min'] <= st.session_state.harga_input:
            klaster_cocok_ids.append(klaster_id)

    df_rekomendasi = df[df['Klaster'].isin(klaster_cocok_ids)] 
    df_rekomendasi = df_rekomendasi[df_rekomendasi['Harga'] <= st.session_state.harga_input]

    # Filter tahun
    if st.session_state.tahun_input != 'Semua':
        tahun_input_int = int(st.session_state.tahun_input)
        df_tahun_sesuai = df_rekomendasi[df_rekomendasi['Tahun Produksi'] == tahun_input_int]
        if not df_tahun_sesuai.empty:
            df_rekomendasi = df_tahun_sesuai
        else:
            df_tahun_diatas = df_rekomendasi[df_rekomendasi['Tahun Produksi'] > tahun_input_int]
            if not df_tahun_diatas.empty:
                df_rekomendasi = df_tahun_diatas

    # Filter jenis
    if st.session_state.jenis_input != 'Semua':
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Jenis'] == st.session_state.jenis_input]

    # Filter transmisi
    if st.session_state.transmisi_input != 'Semua':
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Transmisi'] == st.session_state.transmisi_input]

    # Filter model
    if st.session_state.model_input != 'Semua':
        df_rekomendasi = df_rekomendasi[df_rekomendasi['Model'] == str(st.session_state.model_input)]

    # Sorting
    df_rekomendasi = df_rekomendasi.sort_values(by="Harga", ascending=True)

    # simpan hasil filtering hanya setelah tombol ditekan
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
                    <p><strong>Merek:</strong> {(row['Merk'])}</p>
                    <p><strong>Harga:</strong> {format_harga}</p>
                    <p><strong>Tahun produksi:</strong> {int(row['Tahun Produksi'])}</p>
                    <p><strong>Jarak Tempuh:</strong> {format_odometer}</p>
                    """, unsafe_allow_html=True)

                with col2:
                    if 'path_gambar' in row and pd.notna(row['path_gambar']) and os.path.exists(row['path_gambar']):
                        st.image(str(row['path_gambar']), caption=row['Model'], use_container_width=True)
                    else:
                        st.info(f"Gambar untuk {row['Model']} tidak tersedia.")
                
                with st.expander(f"**🔍 lihat informasi detailnya**"):
                    st.write(f"**Transmisi :** {row['Transmisi']}")
                    st.write(f"**Jenis motor :** {row['Jenis']}")
                    st.write(f"**Kapasitas mesin :** {row['Mesin']}")
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
            


    

            





        













