import streamlit as st
import random
import time

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

prize_table = {
    '🍒': 5,
    '💎': 10,
    '7️⃣': 50,
    '🍋': 15,
    '🔔': 5000
}

# Suara online, bisa ganti link sesuai keinginan
sound_spin = "https://www.soundjay.com/buttons/sounds/button-16.mp3"
sound_win = "https://www.soundjay.com/button/sounds/button-3.mp3"

st.title("🎰 Simulasi Slot Edukasi - Animasi + Suara")

harga_per_spin = st.number_input("Harga per Spin (credit)", min_value=1, value=100)
total_spin = st.number_input("Total Spin", min_value=10, value=100, step=10)
target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)

# Fungsi putar simbol animasi
def animasi_putar(area):
    for _ in range(6):
        hasil = random.choices(symbols, weights_awal, k=3)
        area.markdown(f"<h1 style='text-align: center;'>{' '.join(hasil)}</h1>", unsafe_allow_html=True)
        time.sleep(0.1)

if st.button("Mulai Spin"):

    st.audio(sound_spin, autoplay=True)
    area_tampilan = st.empty()

    total_biaya = total_spin * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    jackpot_ke = random.randint(1, total_spin)
    jackpot_terjadi = False

    modal = harga_per_spin * 300
    total_kembali = 0
    total_menang = 0
    total_jackpot = 0

    for spin in range(1, total_spin + 1):
        modal -= harga_per_spin

        animasi_putar(area_tampilan)

        weights = weights_sulit if jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)

        hadiah = 0
        warna = "black"

        if spin == jackpot_ke:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔'] * harga_per_spin
            jackpot_terjadi = True
        elif hasil[0] == hasil[1] == hasil[2]:
            simbol_menang = hasil[0]
            hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

        if total_kembali + hadiah <= max_total_kembali:
            if hadiah > 0:
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1
                if hasil[0] == '🔔':
                    total_jackpot += 1
                warna = "red"
                area_tampilan.markdown(f"<h1 style='text-align: center; color: {warna};'>{' '.join(hasil)}</h1>", unsafe_allow_html=True)
                st.audio(sound_win, autoplay=True)
            else:
                area_tampilan.markdown(f"<h1 style='text-align: center;'>{' '.join(hasil)}</h1>", unsafe_allow_html=True)
        else:
            area_tampilan.markdown(f"<h1 style='text-align: center;'>{' '.join(hasil)}</h1>", unsafe_allow_html=True)

        st.write(f"Spin ke-{spin}: {'Menang' if hadiah > 0 else 'Kalah'}, Modal: {modal}")

        time.sleep(0.5)

        if modal <= 0:
            st.error(f"Modal habis di spin ke-{spin}")
            break

    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100

    st.success(f"Selesai! Total Spin: {spin}, Total Menang: {total_menang}, Jackpot 5000x: {total_jackpot}")
    st.info(f"Total Kemenangan: {total_kembali} credit | Modal Akhir: {modal} credit | RTP Realisasi: {rtp_real:.2f}%")

    st.warning("⚠️ Ini hanya simulasi edukasi. Slot dikendalikan agar jangka panjang tetap merugikan pemain.")
