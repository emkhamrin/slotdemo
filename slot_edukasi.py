
import streamlit as st
import random
import matplotlib.pyplot as plt

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

st.title("🎰 Simulasi Slot - Edukasi Anti Judi")

harga_per_spin = st.number_input("Harga per Spin (credit)", min_value=1, value=100)
total_spin = st.number_input("Total Spin", min_value=100, value=1000, step=100)
target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)

modal_awal = harga_per_spin * 300

if st.button("Mulai Simulasi"):
    st.info("Simulasi dimulai, harap tunggu...")

    total_biaya = total_spin * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    jackpot_ke = random.randint(1, total_spin)
    jackpot_terjadi = False

    modal = modal_awal
    total_kembali = 0
    total_menang = 0
    total_jackpot = 0
    progres_modal = []

    for spin in range(1, total_spin + 1):
        modal -= harga_per_spin

        weights = weights_sulit if jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)
        hadiah = 0

        if spin == jackpot_ke:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔'] * harga_per_spin // 1
            jackpot_terjadi = True
        elif hasil[0] == hasil[1] == hasil[2]:
            simbol_menang = hasil[0]
            hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin // 1

        if total_kembali + hadiah <= max_total_kembali:
            if hadiah > 0:
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1
                if hasil[0] == '🔔':
                    total_jackpot += 1

        progres_modal.append(modal)

        if modal <= 0:
            st.warning(f"Modal habis di spin ke-{spin}")
            break

    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100

    st.subheader("📊 Hasil Simulasi:")
    st.write(f"Total Spin: {spin}")
    st.write(f"Total Menang: {total_menang}")
    st.write(f"Total Jackpot 5000x: {total_jackpot}")
    st.write(f"Total Kemenangan: {total_kembali} credit")
    st.write(f"Modal Akhir: {modal} credit")
    st.write(f"RTP Realisasi: {rtp_real:.2f}%")

    fig, ax = plt.subplots()
    ax.plot(progres_modal)
    ax.set_title("Perkembangan Modal Sepanjang Spin")
    ax.set_xlabel("Spin ke-")
    ax.set_ylabel("Modal (credit)")
    st.pyplot(fig)

    st.info("⚠️ Ini hanya simulasi edukasi. Slot selalu dikendalikan agar jangka panjang merugikan pemain.")
